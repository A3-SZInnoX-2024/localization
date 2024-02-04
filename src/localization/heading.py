from cv2.typing import MatLike
from ..calibration.external.calibrate import generate_homogeneous_matrix
import numpy as np
from ..calibration.external.file import load_external_parameters


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
    homogeneous_matrix: np.ndarray
):
    homo_rotate_matrix = homogeneous_matrix[:3, :3]
    rotate_matrix = np.dot(homo_rotate_matrix, R_mtx)

    eular = matrix_to_eular_angle(rotate_matrix)

    roll, pitch, yaw = eular
    x, y, z = tvecs
    vec = np.array([x, y, z, [1]])

    vec_vehicle = np.dot(np.linalg.inv(homogeneous_matrix), vec)
    x_vehicle, y_vehicle, z_vehicle, _ = list(map(lambda x: x[0], vec_vehicle))
    return x_vehicle, y_vehicle, z_vehicle, roll, pitch, yaw


def matrix_to_eular_angle(R_mtx: MatLike):
    sy = np.sqrt(R_mtx[0, 0] * R_mtx[0, 0] + R_mtx[1, 0] * R_mtx[1, 0])
    singular = sy < 1e-6

    if not singular:
        roll = np.arctan2(R_mtx[2, 1], R_mtx[2, 2])
        pitch = np.arctan2(-R_mtx[2, 0], sy)
        yaw = np.arctan2(R_mtx[1, 0], R_mtx[0, 0])
    else:
        roll = np.arctan2(-R_mtx[1, 2], R_mtx[1, 1])
        pitch = np.arctan2(-R_mtx[2, 0], sy)
        yaw = 0

    return np.degrees([roll, pitch, yaw])
