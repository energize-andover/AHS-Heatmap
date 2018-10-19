from file_conversion_tools import *
from pdf_tools import *
from openCV_tools import *
import pandas as pd

svg_path = "Andover HS level 3.svg"
pdf_path = svg_path[0:-4] + ".pdf"
png_path = svg_path[0:-4] + ".png"

svg_to_pdf(svg_path, pdf_path)
text_and_coords = get_text_and_coordinates(pdf_path)

svg_to_png(svg_path, png_path, 72)
initialize_cv(png_path)

# Formula for SVG coordinate:
# (x * viewBox width / mediaBox width, viewBox height - y * viewBox height / mediaBox height)
