from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from tag_location import get_tag_location
import cv2


def adjustment(
    tags: list[Detection], camera_matrix: ndarray, dist_coeffs: ndarray = np.zeros(4)
):
    result = {
      "matrix": {
        "rotation": None,
        "translation": None
      },
      "posture": {
        "rotation": None,
        "attitude": None
      }
    }

    # Initialize lists
    object_points = []
    image_points = []

    # Check if `camera_matrix` is a 3x3 matrix
    if camera_matrix.shape != (3, 3):
        print("Because camera_matrix is not a 3x3 matrix, return None")
        return None

    # Check if `tags` has at least 6 tags
    if len(tags) < 6:
        print("Because tags has less than 6 tags, return None")
        return None

    for tag in tags:
        id = str(tag.tag_id)

        # Get object point with tag ID
        object_x, object_y = get_tag_location(tag.tag_id)
        object_point = [object_x, object_y, 0]
        object_points.append(object_point)

        # Get image point with tag center
        image_point = tag.center
        image_points.append(image_point)

    ret, rvecs, tvecs = cv2.solvePnP(
        np.array(object_points, dtype=np.float32),
        np.array(image_points, dtype=np.float32),
        camera_matrix,
        dist_coeffs,
    )

    R_mtx, jac = cv2.Rodrigues(rvecs)

    result["matrix"]["rotation"] = R_mtx
    result["matrix"]["translation"] = tvecs

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

    result["posture"]["rotation"] = tvecs.flatten()
    result["posture"]["attitude"] = np.degrees([roll, pitch, yaw])

    return result
