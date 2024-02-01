from pathlib import Path
import numpy as np


def get_calibration_file_path():
    path = Path(__file__)

    while not str(path).endswith("src"):
        path = path.parent

    if not path.exists():
        raise Exception("The path does not exist")

    dir = path.parent.joinpath("data")

    if not dir.exists():
        dir.mkdir()

    return path.parent.joinpath("data", "calibration.npz")


def load_calibration():
    return np.load(get_calibration_file_path())


def save_calibration(camera_matrix: np.ndarray, dist_coeffs: np.ndarray):
    np.savez(
        get_calibration_file_path(),
        camera_matrix=camera_matrix,
        dist_coeffs=dist_coeffs,
    )
