import numpy as np
import os
from tkinter import messagebox as tkmb

# Internal Parameters

# save to: /data/internal_parameters.npz


def load_path():
    cwd = os.getcwd()
    path = os.path.join(cwd, "data", "internal_parameters.npz")
    return path


def save_internal_parameters(camera_matrix: np.ndarray, dist_coeffs: np.ndarray):
    np.savez(
        load_path(),
        camera_matrix=camera_matrix,
        dist_coeffs=dist_coeffs,
    )


def load_internal_parameters():
    if not is_internal_parameters_exists():
        tkmb.showerror("Error", "The internal parameters do not exist. You need run `python -m src.calibration.internal.calibrate` first.")
        exit(1)
    result = np.load(load_path())
    return result


def is_internal_parameters_exists():
    return os.path.exists(load_path())
