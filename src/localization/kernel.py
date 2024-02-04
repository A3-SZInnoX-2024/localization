from pupil_apriltags import Detection
from numpy import ndarray
import numpy as np
from .adjustment import adjustment
from .localization import localization
from ..calibration.internal.file import load_internal_parameters
from ..calibration.external.file import load_external_parameters


class Location:
    z, roll, pitch = None, None, None  # It won't change after initialization
    x, y, yaw = None, None, None  # It will change after initialization
    camera_matrix = None
    dist_coeffs = None
    homo_matrix = None
    adjusted = False

    def __init__(self, camera_matrix: ndarray, dist_coeffs: ndarray, homo_matrix: ndarray):
        if camera_matrix is None or dist_coeffs is None:
            internal = load_internal_parameters()
            external = load_external_parameters()
            if internal is None or external is None:
                raise Exception("Calibration file does not exist")
            camera_matrix = internal["camera_matrix"]
            dist_coeffs = internal["dist_coeffs"]
            homo_matrix = external["homogeneous_matrix"]
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.homo_matrix = homo_matrix

    def adjust(self, tags: list[Detection]):
        if len(tags) < 6:
            raise Exception("At least 6 tags are required to adjust the camera")

        result = adjustment(tags, self.camera_matrix, self.dist_coeffs, self.homo_matrix)

        if result is not None:
            self.x, self.y, self.z, self.roll, self.pitch, self.yaw = result

        self.adjusted = True

        return result

    def is_adjusted(self):
        return self.adjusted

    def get_z(self):
        return self.z

    def locate(self, tags: list[Detection]):
        if not self.adjusted:
            return None

        if len(tags) > 0:
            result = localization(tags, self.camera_matrix, self.dist_coeffs, self.homo_matrix)
            if result is not None:
                self.x, self.y, _, _, _, self.yaw = result
                return result
            else:
                return None

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
