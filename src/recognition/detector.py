from cv2 import Mat
import cv2
import numpy as np


def n2_average(data: np.ndarray):
    if np.shape(data)[2] != 2:
        return None

    x = np.square(data[0, :][:, 0])
    y = np.square(data[0, :][:, 1])

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    return np.sqrt(x_mean), np.sqrt(y_mean)


def detect(image: Mat, colors: list[dict[str, tuple[int, int, int]]]):
    # Change to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Opening operation
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel, iterations=2)

    # Find contours
    contours = []
    for color in colors:
        mask = cv2.inRange(opening, color["lower"], color["upper"])
        contours += cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
            0
        ]

    # Filter contours
    result = []
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area < 800:
            continue

        avg = n2_average(cnt)

        print(avg)

        if area > 2000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            result.append(box)

    # Draw contours
    cv2.drawContours(image, result, -1, (0, 0, 255), 3)

    return result
