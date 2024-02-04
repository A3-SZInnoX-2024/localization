import cv2
import numpy as np
from ..localization.kernel import Location
from .vtoc import restore_from_vehicle

def locate_block(camera_location: Location, block_image_position: tuple[float, float], Z_c: np.float32):
    camera_position = camera_location.get_position()
    camera_orientation = camera_location.get_orientation()
    camera_matrix = camera_location.get_camera_matrix()
    dist_coeffs = camera_location.get_dist_coeffs()

    print(block_image_position)

    # Rotation matrix
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(camera_orientation[0]), -np.sin(camera_orientation[0])],
                    [0, np.sin(camera_orientation[0]), np.cos(camera_orientation[0])]])
    R_y = np.array([[np.cos(camera_orientation[1]), 0, np.sin(camera_orientation[1])],
                    [0, 1, 0],
                    [-np.sin(camera_orientation[1]), 0, np.cos(camera_orientation[1])]])
    R_z = np.array([[np.cos(camera_orientation[2]), -np.sin(camera_orientation[2]), 0],
                    [np.sin(camera_orientation[2]), np.cos(camera_orientation[2]), 0],
                    [0, 0, 1]])
    R = np.dot(R_z, np.dot(R_y, R_x))
    T = camera_position.reshape(3, 1)
    matrix_vtow = np.hstack((R, T))
    matrix_vtow = np.vstack((matrix_vtow, [0, 0, 0, 1]))
    matrix_ctov = restore_from_vehicle()

    transformation_matrix = np.dot(matrix_ctov, matrix_vtow)

    u, v = block_image_position

    uv_point = np.array([[u, v]], dtype=np.float32)

    undistorted_point = cv2.undistortPoints(uv_point, camera_matrix, dist_coeffs, P=camera_matrix)
    X_c = (undistorted_point[0][0][0] - camera_matrix[0, 2]) / camera_matrix[0, 0] * Z_c
    Y_c = (undistorted_point[0][0][1] - camera_matrix[1, 2]) / camera_matrix[1, 1] * Z_c

    point_camera = np.array([X_c, Y_c, Z_c, 1])
    point_world = np.dot(transformation_matrix, point_camera)
    X_w, Y_w, Z_w = point_world[:3]

    return X_w, Y_w, Z_w
