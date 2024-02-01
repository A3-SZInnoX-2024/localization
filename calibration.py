import numpy as np
import cv2

# 定义棋盘格尺寸
chessboard_size = (8, 6)

# 准备在现实世界中的点
objp = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
objp[:, :2] = np.indices(chessboard_size).T.reshape(-1, 2)

# 存储现实世界中的点和图像中的点
objpoints = []
imgpoints = []

# 启动摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法获取帧, 请检查摄像头连接")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)

    cv2.imshow("frame", frame)

    if len(objpoints) >= 100:  # 收集足够的点后停止，这里以10为例
        break

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# 相机标定
(
    ret,
    camera_matrix,
    distortion_coefficients,
    rotation_vectors,
    translation_vectors,
) = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.save("data/camera_matrix.npy", camera_matrix)
np.save("data/distortion_coefficients.npy", distortion_coefficients)

print("相机内参:", camera_matrix)
print("畸变系数:", distortion_coefficients)
