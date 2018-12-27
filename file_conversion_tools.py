from pathlib import Path
from sys import platform
import time
import os


def svg_to_png(svg_path, png_path, dpi):
    # Delete the file if it exists, as inkscape won't overwrite
    remove_file(png_path)

    # run the command to convert the svg, adding '> /dev/null' on the end to silence the output by storing it into null
    options = '--without-gui --export-area-page --export-background="#ffffff"'

    if platform == "linux" or platform == "linux2":
        # run command to convert the svg, adding '> /dev/null' on the end to silence the output by storing it into null
        os.system('inkscape %s "%s" --export-dpi=%s --export-png="%s"  > /dev/null' % (options, svg_path, dpi, png_path))
    else:
        os.system(
            'inkscape %s "%s" --export-dpi=%s --export-png="%s"' % (options, svg_path, dpi, png_path))

    wait_for_creation(png_path)


def svg_to_pdf(svg_path, pdf_path):
    # Delete the file if it exists, as inkscape won't overwrite
    remove_file(pdf_path)

    options = '--without-gui --export-area-page'

    if platform == "linux" or platform == "linux2":
        # run command to convert the svg, adding '> /dev/null' on the end to silence the output by storing it into null
        os.system('inkscape %s "%s" --export-pdf="%s" > /dev/null' % (options, svg_path, pdf_path))
    else:
        os.system('inkscape %s "%s" --export-pdf="%s"' % (options, svg_path, pdf_path))

    wait_for_creation(pdf_path)


def remove_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def wait_for_creation(path):
    while not Path(path).is_file():
        continue  # Wait until it's completed
