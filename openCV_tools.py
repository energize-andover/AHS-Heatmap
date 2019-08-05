import cv2
import numpy as np

img_path = None
img = None


def initialize_cv(png_path):
    global img, img_path
    img = cv2.imread(png_path)
    img_path = png_path

    if img is None:
        raise FileNotFoundError("There is no image located at '" + png_path + "'")


def get_room_max_contour(room_text_coords):
    bottom_left = (room_text_coords[0], room_text_coords[1])
    top_right = (room_text_coords[2], room_text_coords[3])

    background_color = (255, 255, 255)  # Runs much, much, much faster if we don't try to detect the dominant colors
    lower_bound = np.array(np.clip([value - 5 for value in background_color], 0, 255))
    upper_bound = np.array(np.clip([value + 5 for value in background_color], 0, 255))
    binary = cv2.inRange(img, lower_bound, upper_bound)

    # cv2.imshow('binary 1', binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    replacement_color = 128

    cv2.floodFill(binary, None, bottom_left, replacement_color)
    binary = cv2.inRange(binary, replacement_color, replacement_color)

    # cv2.imshow('binary 2', binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.rectangle(binary, bottom_left, top_right, 255, -1)  # Fill in the room-number-shaped hole for shape recognition

    # cv2.imshow('binary 3', binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ret, thresh = cv2.threshold(binary, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    contour = max(contours, key=cv2.contourArea) # grab largest contours

    return contour


def get_pixel_color(x, y):
    # Returns in RGB
    color = img[y, x]
    return tuple([color[2], color[1], color[0]])


def get_opposite_color(color):
    # Takes in and returns RGB
    return tuple([255 - val for val in color])
