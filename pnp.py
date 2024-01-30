import cv2
import numpy as np

# Define the 3D coordinates of the cube corners
object_points = np.array(
    [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],  # Bottom face
        [0, 0, -1],
        [1, 0, -1],
        [1, 1, -1],
        [0, 1, -1],  # Top face
    ],
    dtype=np.float32,
)

# Corresponding 2D coordinates in the image
# (these would normally be found through feature matching)
image_points = np.array(
    [
        [320, 200],
        [400, 200],
        [400, 280],
        [320, 280],
        [290, 220],
        [370, 220],
        [370, 300],
        [290, 300],
    ],
    dtype=np.float32,
)

# Camera matrix (assuming a hypothetical camera)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)

# Distortion coefficients (assuming no distortion)
dist_coeffs = np.zeros(4)

# SolvePnP
ret, rvecs, tvecs = cv2.solvePnP(
    object_points, image_points, camera_matrix, dist_coeffs
)

# Convert rotation vector to a rotation matrix
R_mtx, jac = cv2.Rodrigues(rvecs)

# Output the rotation matrix and translation vector
print("Rotation Matrix:\n", R_mtx)
print("Translation Vector:\n", tvecs)
R_mtx, jac = cv2.Rodrigues(rvecs)
sy = np.sqrt(R_mtx[0,0] * R_mtx[0,0] +  R_mtx[1,0] * R_mtx[1,0])
singular = sy < 1e-6
if not singular: # 一般情况
    roll = np.arctan2(R_mtx[2,1] , R_mtx[2,2])
    pitch = np.arctan2(-R_mtx[2,0], sy)
    yaw = np.arctan2(R_mtx[1,0], R_mtx[0,0])
else: # 奇异情况
    roll = np.arctan2(-R_mtx[1,2], R_mtx[1,1])
    pitch = np.arctan2(-R_mtx[2,0], sy)
    yaw = 0

# 输出位置 (x, y, z)
print("位置 (x, y, z):\n", tvecs.flatten())

# 输出方向 (roll, pitch, yaw)
print("方向 (roll, pitch, yaw):\n", np.degrees([roll, pitch, yaw]))  # 转换为度
