from ..calibration.external.file import load_external_parameters
import numpy as np
import cv2
from cv2.typing import MatLike

def restore_from_vehicle():
    external_parameters = load_external_parameters()
    homogeneous_matrix = external_parameters["homo_matrix"]
    result = np.linalg.inv(homogeneous_matrix)
    return result

def get_restore_matrix(matrix: MatLike):
    R_mtx = matrix[:3, :3]
    tvecs = matrix[:3, 3]
    return R_mtx, tvecs

def get_restore_vectors(matrix: MatLike):
    R_mtx, tvecs = get_restore_matrix(matrix)
    rvecs = cv2.Rodrigues(R_mtx)
    return rvecs, tvecs
