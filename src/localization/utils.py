from cv2 import Mat
import numpy as np

def handle_pnp_result(tvec: Mat, R_mtx: Mat):
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

    RT = np.column_stack((R_mtx, tvec))
    RT_homogeneous = np.vstack((RT, [0, 0, 0, 1]))
    RT_inverse = np.linalg.inv(RT_homogeneous)
    camera_position = RT_inverse[:3, 3]

    return camera_position, np.degrees([roll, pitch, yaw])
