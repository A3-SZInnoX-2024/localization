import cv2
import numpy as np
from numpy import ndarray
from pupil_apriltags import Detector
from .heading import calculate_position
from .emergency import generate_points


def localization(
    dots: list[Detector],
    camera_matrix: ndarray,
    dist_coeffs: ndarray,
    homo_matrix: ndarray,
):
    object_points, image_points = generate_points(dots)

    _, rvecs, tvecs = cv2.solvePnP(
        np.array(object_points, dtype=np.float32),
        np.array(image_points, dtype=np.float32),
        camera_matrix,
        dist_coeffs,
    )

    R_mtx, _ = cv2.Rodrigues(rvecs)

    return calculate_position(R_mtx, tvecs, homo_matrix)
