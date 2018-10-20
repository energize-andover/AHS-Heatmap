import pdfminer
import pandas as pd
from pdfminer.pdfpage import *
from pdfminer.pdfinterp import *
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from PyPDF2 import PdfFileReader


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
                # Use some basic filtering: Remove letters, add hyphens, ignore combined rooms
                text = re.sub('[^0-9]', '', obj.get_text())
                text_len = len(text)

                if text_len > 0:
                    bbox = obj.bbox
                    width = bbox[2] - bbox[0]
                    height = bbox[3] - bbox[1]

                    if text_len == 5:
                        text = text[:3] + '-' + text[3:]
                    elif text_len > 5:
                        continue  # Currently just ignoring those few rooms which are problematic

                    df_dictionary['x0'].append(bbox[0])
                    df_dictionary['y0'].append(bbox[1])
                    df_dictionary['x1'].append(bbox[2])
                    df_dictionary['y1'].append(bbox[3])
                    df_dictionary['width'].append(width)
                    df_dictionary['height'].append(height)
                    df_dictionary['text'].append(text)

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


def get_media_box(pdf_path):
    return PdfFileReader(open(pdf_path, 'rb')).getPage(0).mediaBox
