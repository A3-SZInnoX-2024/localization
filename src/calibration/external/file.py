import numpy as np
import os

# External Parameters

# save to: /data/extrernal_parameters.npz


def load_path():
    cwd = os.getcwd()
    path = os.path.join(cwd, "data", "external_parameters.npz")
    return path


def save_external_parameters(homogeneous_matrix: np.ndarray):
    np.savez(
        load_path(),
        homogeneous_matrix=homogeneous_matrix,
    )


def load_external_parameters():
    return np.load(load_path())


def is_extetnal_parameters_exists():
    return os.path.exists(load_path())
