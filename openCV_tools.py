from collections import Counter

import cv2
import numpy as np

img = None
img_size = None


def initialize_cv(png_path):
    global img, img_size
    img = cv2.imread(png_path)

    if img is None:
        raise FileNotFoundError("There is no image located at '" + png_path + "'")

    img_size = tuple(img.shape[1::-1])  # Extract only the width and height, not the channels


def get_img_size():
    return img_size


def get_room_corner_coords(room_text_coords, png_path):
    bottom_left = (room_text_coords[0], room_text_coords[1])
    top_right = (room_text_coords[2], room_text_coords[3])

    background_color = BackgroundColorDetector(png_path).detect()
    lower_bound = np.array(np.clip([value - 5 for value in background_color], 0, 255))
    upper_bound = np.array(np.clip([value + 5 for value in background_color], 0, 255))
    binary = cv2.inRange(img, lower_bound, upper_bound)

    replacement_color = 128

    cv2.floodFill(binary, None, bottom_left, replacement_color)
    binary = cv2.inRange(binary, replacement_color, replacement_color)
    cv2.rectangle(binary, bottom_left, top_right, 255, -1)  # Fill in the room-number-shaped hole for shape recognition

    ret, thresh = cv2.threshold(binary, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    contour = contours[0]

    contour_perimeter = cv2.arcLength(contour, True)
    approx_poly_curve = cv2.approxPolyDP(contour, 0.05 * contour_perimeter, True)
    room_coords = cv2.boundingRect(approx_poly_curve)  # Format: (x, y, width, height)

    return list(room_coords)


def get_pixel_color(x, y):
    # Returns in RGB
    color = img[y, x]
    return tuple([color[2], color[1], color[0]])


def get_opposite_color(color):
    # Takes in and returns RGB
    return tuple([255 - val for val in color])


class BackgroundColorDetector:
    def __init__(self, imageLoc):
        self.img = cv2.imread(imageLoc, 1)
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w * self.h
        self.percentage_of_first = 0
        self.number_counter = None

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_color(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        return [average_red, average_green, average_blue]

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)

    def detect(self):
        self.twenty_most_common()
        self.percentage_of_first = (float(self.number_counter[0][1]) / self.total_pixels)
        return self.number_counter[0][
            0] if self.percentage_of_first and self.percentage_of_first > 0.5 else self.average_color()
