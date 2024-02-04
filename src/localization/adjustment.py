from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .tag_location import get_points
import cv2
from cv2.typing import MatLike
from .heading import calculate_position

def adjustment(
    tags: list[Detection], camera_matrix: MatLike, dist_coeffs: MatLike = np.zeros(5)
) -> ndarray:
    # Initialize lists
    object_points, image_points = get_points(tags)

    # Check if `camera_matrix` is a 3x3 matrix
    if camera_matrix.shape != (3, 3):
        raise Exception("Because camera_matrix is not a 3x3 matrix, return None")

    # Check if `tags` has at least 6 tags
    if len(tags) < 6:
        raise Exception("Because tags has less than 6 tags, return None")

    _, rvecs, tvecs = cv2.solvePnP(
        np.array(object_points, dtype=np.float32),
        np.array(image_points, dtype=np.float32),
        camera_matrix,
        dist_coeffs,
    )

    R_mtx, _ = cv2.Rodrigues(rvecs)

    return calculate_position(R_mtx, tvecs)
