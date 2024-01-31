import cv2
import numpy as np
import sys
import os
from ..localization.kernel import Location


def scan(
    location: Location,
    image: cv2.Mat,
    colors: list[dict[str, tuple[int, int, int]]],
):
    # Change to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Opening operation
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel)

    cv2.imshow('opening', opening)

    # Find contours
    contours = []
    for color in colors:
        mask = cv2.inRange(opening, color['lower'], color['upper'])
        contours += cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # Filter contours
    result = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            result.append(box)

    # Draw contours
    # cv2.drawContours(image, result, -1, (0, 0, 255), 3)

    # Show image
    cv2.imshow('Scan', image)

    return result
