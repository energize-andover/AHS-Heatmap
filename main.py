from file_conversion_tools import svg_to_pdf
from pdf_tools import *
import pandas as pd

svg_path = "Andover HS level 3.svg"
pdf_path = "Andover HS level 3.pdf"

svg_to_pdf(svg_path, pdf_path)
text_and_coords = get_text_and_coordinates(pdf_path)

# Formula for SVG coordinate:
# (x * viewBox width / mediaBox width, viewBox height - y * viewBox height / mediaBox height)