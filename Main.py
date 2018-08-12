import os
from PyPDF2 import PdfFileReader
from FileHelpers import *

pdf_path = os.path.join('pdf', 'Andover HS level 3.pdf')
svg_path = os.path.join('svg', 'Andover HS level 3.svg')
png_path = os.path.join('png', 'Andover HS level 3.png')

df = get_text_and_coordinates(pdf_path)

# Gets PDF size in pts (1pt = 1/72 in) [0, 0, width, height]
media_box = PdfFileReader(open(pdf_path, 'rb')).getPage(0).mediaBox

print(df.head())
