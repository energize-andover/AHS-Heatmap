from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pathlib import Path
from PIL import Image, ImageDraw
import pdfminer
import pandas as pd
import os


def get_text_and_coordinates(pdf_path):
    # Open a PDF file.
    fp = open(pdf_path, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    resource_manager = PDFResourceManager()

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    la_params = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(resource_manager, laparams=la_params)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(resource_manager, device)

    def parse_obj(lt_objects):

        # (x0, y0) = Bottom left corner, (x1, y1) = Top right corner
        df_dictionary = {
            'x0': [],
            'y0': [],
            'x1': [],
            'y1': [],
            'width': [],
            'height': [],
            'text': []
        }

        # loop over the object list
        for obj in lt_objects:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                df_dictionary['x0'].append(obj.bbox[0])
                df_dictionary['y0'].append(obj.bbox[1])
                df_dictionary['x1'].append(obj.bbox[2])
                df_dictionary['y1'].append(obj.bbox[3])
                df_dictionary['width'].append(obj.bbox[2] - obj.bbox[0])
                df_dictionary['height'].append(obj.bbox[3] - obj.bbox[1])
                df_dictionary['text'].append(obj.get_text().replace('\n', ''))

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(obj._objs)

        return pd.DataFrame.from_dict(df_dictionary)

    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        # extract text from this object
        df = parse_obj(layout._objs)
        return df


def svg_to_png(svg_path, output_path, dpi):
    # Delete the file if it exists, as inkscape won't overwrite
    try:
        os.remove(output_path)
    except OSError:
        pass

    options = '--without-gui --export-area-page --export-background="#ffffff"'
    os.system('inkscape %s "%s" --export-dpi=%s --export-png="%s"' % (
        options, svg_path, dpi, output_path))

    while not Path(output_path).is_file():
        continue  # Wait until it's completed


def svg_to_pdf(svg_path, pdf_path):
    # Delete the file if it exists, as inkscape won't overwrite
    try:
        os.remove(pdf_path)
    except OSError:
        pass

    options = '--without-gui --export-area-page'
    os.system('inkscape %s "%s" --export-pdf="%s"' % (options, svg_path, pdf_path))

    while not Path(pdf_path).is_file():
        continue  # Wait until it's completed


def flood_fill(png_path, room_coords, color):
    img = Image.open(png_path)

    width, height = img.size

    coordinate = (room_coords[0], height - room_coords[1])

    ImageDraw.floodfill(img, coordinate, value=color, thresh=5)
    img.save(png_path)
