from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .adjustment import adjustment
from .three_point import three_point_localization


class Location:
    z, roll, yaw = None, None, None  # It won't change after initialization
    x, y, pitch = None, None, None  # It will change after initialization
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

        self.x = result[0][0]
        self.y = result[0][1]
        self.pitch = result[1][1]

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
            position, orientation = location
            self.x, self.y, self.pitch = position[0], position[1], orientation[1]
        else:
            location = None, None
        return location

    def get_position(self):
        return np.array([self.x, self.y, self.z])

    def get_orientation(self):
        return np.array([self.roll, self.pitch, self.yaw])

    def get_camera_matrix(self):
        return self.camera_matrix

    def get_dist_coeffs(self):
        return self.dist_coeffs

    def get_location_matrix(self):
        return np.array(
            [[self.x], [self.y], [self.z], [self.roll], [self.pitch], [self.yaw]]
        )
