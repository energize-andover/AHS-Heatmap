import cv2

img = None
img_size = None


def initialize_cv(png_path):
    global img, img_size
    img = cv2.imread(png_path)

    if img is None:
        raise FileNotFoundError("There is no image located at '" + png_path + "'")

    img_size = tuple(img.shape[1::-1])  # Extract only the width and height, not the channels

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(get_pixel_color(627, 316))


def get_img_size():
    return img_size


def get_pixel_color(x, y):
    # Returns in RGB
    color = img[y, x]
    return tuple(color[2], color[1], color[0])
