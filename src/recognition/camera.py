import cv2


def capture_image(capture: cv2.VideoCapture):
    ret, image = capture.read()

    if ret is None:
        raise Exception("Can't recognize the image")

    return image
