"""
1. 确定 AprilTag 的位置, 调用 `solvePnP` 函数获取旋转向量和平移向量
2. 通过 `Rodrigues` 函数将旋转向量转换为旋转矩阵
3. 拼接矩阵 (R, T) 作为 camera - world 的变换矩阵, 并且逆运算得到 world - camera 的变换矩阵
4. 通过已知机器人的位置, 获得 vehicle - world 的变换矩阵
5. 通过 `np.dot` 函数将两个变换矩阵相乘, 得到 vehicle - camera 的变换矩阵, 并且逆运算得到 camera - vehicle 的变换矩阵
"""

import cv2
from pupil_apriltags import Detection
from cv2.typing import MatLike
import tkinter.simpledialog as tksd
import tkinter.messagebox as tkmb
from ...localization.tag_location import get_points, get_tag_location
import numpy as np
from ..internal.file import load_internal_parameters
from .file import save_external_parameters
from ...configuration.tags import get_tags


def matrix_ctow(tags: list[Detection], camera_matrix: MatLike, dist_coeffs: MatLike):

    # Check if there are any detections
    if len(tags) < 6:
        tkmb.showerror("Error", "There are not enough tags to calibrate the camera.")
        exit(1)

    # Initialize lists
    object_points, image_points = get_points(tags)

    # Check if `camera_matrix` is a 3x3 matrix
    if camera_matrix.shape != (3, 3):
        tkmb.showerror("Error", "The camera matrix is not a 3x3 matrix.")
        exit(1)

    # Check if `dist_coeffs` is a 1x5 matrix
    if dist_coeffs.shape != (1, 5):
        tkmb.showerror("Error", "The distortion coefficients are not a 1x5 matrix.")
        exit(1)

    _, rvecs, tvecs = cv2.solvePnP(
        np.array(object_points, dtype=np.float32),
        np.array(image_points, dtype=np.float32),
        camera_matrix,
        dist_coeffs,
    )

    R_mtx, _ = cv2.Rodrigues(rvecs)

    return generate_homogeneous_matrix(R_mtx, tvecs, invert=True)


def generate_homogeneous_matrix(R_mtx: MatLike, tvecs: MatLike, invert=False):
    # Initialize the homogeneous matrix
    homogeneous_matrix = np.zeros((4, 4))

    # Set the rotation matrix
    homogeneous_matrix[:3, :3] = R_mtx

    print(homogeneous_matrix[:3, 3], tvecs.flatten(), tvecs, 'hello')

    # Set the translation vector
    homogeneous_matrix[:3, 3] = tvecs.flatten()

    # Set the bottom row
    homogeneous_matrix[3, 3] = 1

    if invert:
        return np.linalg.inv(homogeneous_matrix)
    return homogeneous_matrix


def matrix_wtov(tagid: int):
    x_world, y_world = get_tag_location(tagid)
    world_location = np.array([x_world, y_world, 0])
    vehicle_location = np.array([0, 0, 0])

    R_mtx = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    tvecs = world_location - vehicle_location

    return generate_homogeneous_matrix(R_mtx, tvecs, invert=True)


def matrix_ctov(tags: list[Detection], camera_matrix: MatLike, dist_coeffs: MatLike, position_tag: int):
    matrix_ctow_result = matrix_ctow(tags, camera_matrix, dist_coeffs)
    matrix_wtov_result = matrix_wtov(position_tag)

    return np.dot(matrix_ctow_result, matrix_wtov_result)

def calibrate_external(
    tags: list[Detection]
):
    tag_id = tksd.askinteger("Tag ID", "Enter the tag ID of the vehicle.")

    if tag_id is None:
        tkmb.showerror("Error", "The tag ID is required.")
        exit(1)

    if tag_id > len(get_tags()) or tag_id < 0:
        tkmb.showerror("Error", "The tag ID must be between 0 and 55.")
        exit(1)

    internal_parameters = load_internal_parameters()
    camera_matrix = internal_parameters["camera_matrix"]
    dist_coeffs = internal_parameters["dist_coeffs"]

    homogeneous_matrix = matrix_ctov(tags, camera_matrix, dist_coeffs, tag_id)

    save_external_parameters(homogeneous_matrix)

    return homogeneous_matrix

    # return matrix_ctov_result

if __name__ == '__main__':
    from pupil_apriltags import Detector
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = Detector(families='tag36h11')
        tags = detector.detect(gray)
        if len(tags) > 5:
            calibrate_external(tags)
            break
        for tag in tags:
            for idx in range(len(tag.corners)):
                cv2.line(frame, tuple(tag.corners[idx - 1].astype(int)), tuple(tag.corners[idx].astype(int)), (0, 255, 0))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
