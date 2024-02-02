import cv2
import numpy as np
from cv2.typing import MatLike
from ..configuration.colors import Color


def filter_color(image: MatLike, color: Color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    identified_colors = []
    for lower, upper in color.range:
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Draw it
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if contours:
            print("found", color.name)
            for countour in contours:
                print(countour)
                identified_colors.append(countour)

    return color.name, identified_colors

    # print(result)


def n2_average(data: np.ndarray):
    if np.shape(data)[2] != 2:
        return None

    x = np.square(data[0, :][:, 0])
    y = np.square(data[0, :][:, 1])

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    return np.sqrt(x_mean), np.sqrt(y_mean)


def detect(image: MatLike, colors: list[Color]):
    # Change to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Opening operation
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, kernel, iterations=2)

    # Filter colors

    for color in colors:
        color, contours = filter_color(image, color)

        for cnt in contours:
            # Draw a bounding box around the detected object
            x, y, w, h = cv2.boundingRect(cnt)
            if (w * h < 2000):
                continue
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Put the color name text on the object
            cv2.putText(
                image, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

        cv2.imshow("image", image)

    # # Filter contours
    # result = []
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)

    #     if area < 800:
    #         continue

    #     avg = n2_average(cnt)

    #     print(avg)

    #     if area > 2000:
    #         rect = cv2.minAreaRect(cnt)
    #         box = cv2.boxPoints(rect)
    #         box = np.intp(box)
    #         result.append(box)

    # # Draw contours
    # cv2.drawContours(image, result, -1, (0, 0, 255), 3)

    # return result
