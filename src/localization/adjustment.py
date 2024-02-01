from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .tag_location import get_points
import cv2
from .utils import handle_pnp_result


def adjustment(
    tags: list[Detection], camera_matrix: ndarray, dist_coeffs: ndarray = np.zeros(4)
):
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

    position, orientation = handle_pnp_result(tvecs, R_mtx)

    return position, orientation
