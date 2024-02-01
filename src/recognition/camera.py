import cv2

def capture_image():
    caputor = cv2.VideoCapture

    ret, image = caputor.read()

    if ret is None:
        raise Exception('Can\'t recognize the image')

    return image
