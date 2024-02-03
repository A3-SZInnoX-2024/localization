import cv2
import numpy as np
from numpy import float32, ndarray
from pupil_apriltags import Detector
from .tag_location import get_points
from .utils import handle_pnp_result
from .heading import calculate_position_with_heading


def three_point_localization(
    dots: list[Detector],
    z: float32,
    roll: float32,
    pitch: float32,
    camera_matrix: ndarray,
    dist_coeffs: ndarray = np.zeros(4),
):
    # Check if `camera_matrix` is a 3x3 matrix
    if camera_matrix.shape != (3, 3):
        return None

    # Check if `dots` has at least 3 dots
    if len(dots) < 3:
        return None

    # Initialize parameters
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])

    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])

    R = np.dot(R_x, R_y)

    T = np.array([[0], [0], [-z]])

    Rv, _ = cv2.Rodrigues(R)

    # Initialize lists
    object_points, image_points = get_points(dots)

    _, rvecs, tvecs = cv2.solvePnP(
        np.array(object_points, dtype=np.float32),
        np.array(image_points, dtype=np.float32),
        camera_matrix,
        dist_coeffs,
        rvec=Rv,
        tvec=T,
        useExtrinsicGuess=True,
    )

    R_mtx, _ = cv2.Rodrigues(rvecs)

    return handle_pnp_result(R_mtx, tvecs)
