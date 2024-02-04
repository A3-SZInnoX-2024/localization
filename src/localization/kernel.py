from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .adjustment import adjustment
from .three_point import three_point_localization
from .emergency import emergency_localization
from ..calibration.file import load_calibration


class Location:
    z, roll, pitch = None, None, None  # It won't change after initialization
    x, y, yaw = None, None, None  # It will change after initialization
    camera_matrix = None
    dist_coeffs = None
    adjusted = False

    def __init__(self, camera_matrix: ndarray, dist_coeffs: ndarray = np.zeros(4)):
        if camera_matrix is None or dist_coeffs is None:
            calibration = load_calibration()
            if calibration is None:
                raise Exception("Calibration file does not exist")
            camera_matrix = calibration["camera_matrix"]
            dist_coeffs = calibration["dist_coeffs"]
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs

    def adjust(self, tags: list[Detection]):
        if len(tags) < 6:
            raise Exception("At least 6 tags are required to adjust the camera")

        result = adjustment(tags, self.camera_matrix, self.dist_coeffs)

        if result is not None:
            self.x, self.y, self.z, self.roll, self.pitch, self.yaw = result
        # print(f"z: {self.z}, roll: {self.roll}, pitch: {self.pitch}")

        self.adjusted = True

        return result

    def is_adjusted(self):
        return self.adjusted

    def get_z(self):
        return self.z

    def locate(self, tags: list[Detection]):
        if not self.adjusted:
            # print("Because the camera is not adjusted, return None")
            return None

        if len(tags) >= 3:
            location = three_point_localization(
                tags,
                self.z,
                self.roll,
                self.pitch,
                self.camera_matrix,
                self.dist_coeffs,
                use_corners=True,
            )
            self.x, self.y, self.yaw = location[0], location[1], location[5]
        elif len(tags) > 0:
            location = emergency_localization(
                tags,
                self.z,
                self.roll,
                self.pitch,
                self.camera_matrix,
                self.dist_coeffs,
            )

            if location is not None:
                self.x, self.y, self.yaw = location[0], location[1], location[5]
        else:
            location = None
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
