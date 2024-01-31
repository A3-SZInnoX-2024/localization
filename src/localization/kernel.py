from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .adjustment import adjustment
from .three_point import three_point_localization


class Location:
    z, roll, yaw = None, None, None  # It won't change after initialization
    camera_matrix = None
    dist_coeffs = None
    adjusted = False

    def __init__(self, camera_matrix: ndarray, dist_coeffs: ndarray = np.zeros(4)):
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs

    def adjust(self, tags: list[Detection]):
        result = adjustment(tags, self.camera_matrix, self.dist_coeffs)

        self.z = result[0][2]
        self.roll = result[1][0]
        self.yaw = result[1][2]

        print(f"z: {self.z}, roll: {self.roll}, yaw: {self.yaw}")

        self.adjusted = True

    def is_adjusted(self):
        return self.adjusted

    def get_z(self):
        return self.z

    def locate(self, tags: list[Detection]):
        if not self.adjusted:
            print("Because the camera is not adjusted, return None")
            return None

        if len(tags) >= 3:
            location = three_point_localization(
                tags, self.z, self.roll, self.yaw, self.camera_matrix, self.dist_coeffs
            )
        else:
            location = None, None
        return location
