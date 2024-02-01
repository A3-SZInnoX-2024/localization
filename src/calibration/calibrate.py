from typing import Sequence
import numpy as np
import cv2
from .file import save_calibration

def calibrate(
    object_points: Sequence[np.ndarray],
    image_points: Sequence[np.ndarray],
    size: np.ndarray,
):
    (ret, camera_matrix, dist_coeffs, rvecs, tvecs) = cv2.calibrateCamera(
        object_points, image_points, size, None, None
    )

    if ret is False:
        raise Exception("The calibration was not successful")

    save_calibration(camera_matrix, dist_coeffs)

    return camera_matrix, dist_coeffs
