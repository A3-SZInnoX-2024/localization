from pupil_apriltags import Detection
from .tag_location import get_points
import numpy as np
import cv2
from .heading import calculate_position


def generate_points(tags: list[Detection], tag_width: float = 205):
    object_points, image_points = [], []

    tags_object, tags_image = get_points(tags)

    for i in range(len(tags)):
        tag = tags[i]
        tag_object = tags_object[i]

        x, y, z = tag_object

        lb_image, lt_image, rt_image, rb_image = tag.corners

        lb_object, lt_object, rt_object, rb_object = (
            (x - tag_width / 2, y - tag_width / 2, z),
            (x - tag_width / 2, y + tag_width / 2, z),
            (x + tag_width / 2, y + tag_width / 2, z),
            (x + tag_width / 2, y - tag_width / 2, z),
        )

        object_points.append(lb_object)
        object_points.append(lt_object)
        object_points.append(rt_object)
        object_points.append(rb_object)

        image_points.append(lb_image)
        image_points.append(lt_image)
        image_points.append(rt_image)
        image_points.append(rb_image)

        object_points.append(tag_object)
        image_points.append(tag.center)

    return object_points, image_points


def emergency_localization(
    tags: list[Detection],
    z: np.float32,
    roll: np.float32,
    pitch: np.float32,
    camera_matrix: np.ndarray,
    dist_coeffs: np.ndarray,
    tag_width: float = 20.0,
):
    object_points, image_points = generate_points(tags, tag_width)

    # Initialize parameters
    R_x = np.array(
        [[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]]
    )

    R_y = np.array(
        [
            [np.cos(pitch), 0, np.sin(pitch)],
            [0, 1, 0],
            [-np.sin(pitch), 0, np.cos(pitch)],
        ]
    )

    R = np.dot(R_x, R_y)

    T = np.array([[0], [0], [-z]])

    Rv, _ = cv2.Rodrigues(R)

    # print(len(object_points), len(image_points))

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

    return calculate_position(R_mtx, tvecs)
