from cv2.typing import MatLike
from ..calibration.external.calibrate import generate_homogeneous_matrix
import numpy as np
from ..calibration.external.file import load_external_parameters
import cv2

def calculate_position_with_heading(
    R_mtx: MatLike,
):
    tvecs = [1, 0, 0]
    homogeneous_matrix = generate_homogeneous_matrix(R_mtx, tvecs)

    heading = np.arctan2(homogeneous_matrix[1, 0], homogeneous_matrix[0, 0])

    return heading

def calculate_position(
    R_mtx: MatLike,
    tvecs: MatLike,
):
    external_parameters = load_external_parameters()

    homogeneous_matrix = external_parameters['homogeneous_matrix']

    homo_rotate_matrix = homogeneous_matrix[:3, :3]

    rotate_matrix = np.dot(homo_rotate_matrix, R_mtx)

    roll, pitch, yaw = cv2.decomposeProjectionMatrix(rotate_matrix)[:3]

    x, y, z = tvecs

    vec = np.array([[x], [y], [z], [1]])

    vec_vehicle = np.dot(np.linalg.inv(homogeneous_matrix), vec)

    x_vehicle, y_vehicle, z_vehicle, _ = vec_vehicle

    return x_vehicle, y_vehicle, z_vehicle, roll, pitch, yaw
