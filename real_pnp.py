import cv2
import numpy as np

# 定义3D点 (在世界坐标系中)
object_points = np.array(
    [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0], [5, 0, 0]], dtype=np.float32
)

# 定义2D点 (在图像坐标系中)
image_points = np.array(
    [[50, 50], [100, 50], [150, 50], [200, 50], [250, 50], [300, 50]], dtype=np.float32
)

# 假设的摄像头内参矩阵
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32)

# 假设无畸变
dist_coeffs = np.zeros(4)

# 使用solvePnP求解摄像头位姿
ret, rvecs, tvecs = cv2.solvePnP(
    object_points, image_points, camera_matrix, dist_coeffs
)

# 输出
print("旋转向量:\n", rvecs)
print("平移向量:\n", tvecs)
