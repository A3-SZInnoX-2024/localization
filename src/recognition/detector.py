import cv2
import numpy as np
from cv2.typing import MatLike
from ..configuration.colors import Color
from sklearn.cluster import DBSCAN


def dbscan(data: np.ndarray, eps: float = 2, min_samples: int = 5):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(data)
    return clusters


def merge_duplicates(contours: list[np.ndarray], threshold: int = 10):
    # result = []
    # for cnt in contours:
    #     if not result:
    #         result.append(cnt)
    #         continue

    #     for r in result:
    #         if np.linalg.norm(cnt - r) < threshold:
    #             r = np.concatenate((r, cnt))
    #             break
    #     else:
    #         result.append(cnt)

    # return result
    # Use DBSCAN to merge the contours
    data = np.array([np.mean(cnt, axis=0) for cnt in contours])
    clusters = dbscan(data)
    result = []
    for i in range(len(clusters)):
        result.append(
            np.concatenate(
                [contours[j] for j in range(len(clusters)) if clusters[j] == i]
            )
        )
    return result


def filter_color(image: MatLike, hsv: MatLike, color: Color):
    identified_colors: list[np.ndarray] = []
    for lower, upper in color.range:
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Draw it
        contours, _ = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # contours = merge_duplicates(contours)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 1200:
                continue

            identified_colors.append(cnt)

    return color.name, identified_colors


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

    result = []

    for color in colors:
        name = color.name
        color, contours = filter_color(opening, hsv, color)

        if len(contours) == 0:
            continue

        for cnt in contours:
            # Draw a bounding box around the detected object
            x, y, w, h = cv2.boundingRect(cnt)

            if w * h < 2000:
                continue

            # Get average

            result.append((name, [x + w / 2, y + h / 2]))


    return result
