from pathlib import Path
import os

def svg_to_png(svg_path, png_path, dpi):
    # Delete the file if it exists, as inkscape won't overwrite
    remove_file(png_path)

    options = '--without-gui --export-area-page --export-background="#ffffff"'
    os.system('inkscape %s "%s" --export-dpi=%s --export-png="%s"' % (
        options, svg_path, dpi, png_path))

    wait_for_creation(png_path)


def svg_to_pdf(svg_path, pdf_path):
    # Delete the file if it exists, as inkscape won't overwrite
    remove_file(pdf_path)

    options = '--without-gui --export-area-page'
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
