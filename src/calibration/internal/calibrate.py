import tkinter.messagebox as tkmb
import cv2
from typing import Sequence
from cv2.typing import MatLike, Size
from .file import save_internal_parameters

def calibrate_internal(
    object_points: Sequence[MatLike],
    image_points: Sequence[MatLike],
    size: Size,
) -> tuple[MatLike, MatLike]:

    if len(object_points) != len(image_points):
        tkmb.showerror("Error", "The number of object points and image points must be the same")
        exit(1)

    (ret, camera_matrix, dist_coeffs, rvecs, tvecs) = cv2.calibrateCamera(
        object_points, image_points, size, None, None
    )

    if ret is False:
        raise Exception("The calibration was not successful")

    save_internal_parameters(camera_matrix, dist_coeffs)

    return camera_matrix, dist_coeffs

