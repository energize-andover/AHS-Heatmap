from openCV_tools import *


def get_svg_measure(pdf_measure, svg_axis_measure, pdf_axis_measure):
    return pdf_measure * svg_axis_measure / pdf_axis_measure


def get_svg_coords(png_coords, svg_view_box, pdf_media_box):
    x_coord = png_coords[0] * svg_view_box[2] / pdf_media_box[2]
    y_coord = svg_view_box[3] - png_coords[1] * svg_view_box[3] / pdf_media_box[3]
    coords = [x_coord, y_coord]
    return tuple(coords)


def get_room_pdf_coords(room, text_and_coords):
    text = text_and_coords['text']
    global roomIndex
    roomIndex = None

    # Check for exact matches first
    if len(text_and_coords[text_and_coords['text'] == room].index) > 0:
        roomIndex = text_and_coords.index[text_and_coords['text'] == room].tolist()
    else:
        # Then check with less exact methods
        for indx, col_room in text.iteritems():
            if col_room.startswith(room) or col_room.endswith(room):
                roomIndex = indx

    if roomIndex is None:
        return None

    room_row = text_and_coords.iloc[roomIndex]
    return [room_row['x0'], room_row['y0'], room_row['x1'], room_row['y1']]


def get_room_contour(room, media_box, text_and_coords):
    coords = get_room_pdf_coords(str(room), text_and_coords)
    if coords is None:
        return None
    room_text_coords = [int(coord) for coord in coords]
    room_text_coords[1] = media_box[3] - room_text_coords[1]  # OpenCV measures the y-axis from the other side
    room_text_coords[3] = media_box[3] - room_text_coords[3]

    return get_room_max_contour(room_text_coords)
