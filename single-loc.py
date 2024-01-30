import cv2
import numpy as np


def rotationMatrixToEulerAngles(R):
    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    return np.array([x, y, z])


# 相机内参和畸变系数（需要根据您的相机进行调整）
focal_length = [fx, fy]  # 替换为您的相机焦距
center = [cx, cy]  # 替换为您的相机中心点
camera_matrix = np.array(
    [[focal_length[0], 0, center[0]], [0, focal_length[1], center[1]], [0, 0, 1]],
    dtype="double",
)
dist_coeffs = np.zeros((4, 1))  # 如果有精确值，请替换

# Apriltag检测器
detector = cv2.aruco.Dictionary_get(cv2.aruco.DICT_APRILTAG_36h11)
parameters = cv2.aruco.DetectorParameters_create()

# 打开相机
cap = cv2.VideoCapture(0)

# 检测并显示
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 检测Apriltags
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(
        frame, detector, parameters=parameters
    )

    # 如果检测到Apriltag
    if ids is not None:
        # 估算位姿
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, 0.15, camera_matrix, dist_coeffs
        )

        # 可视化
        for rvec, tvec in zip(rvecs, tvecs):
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.1)

            R, _ = cv2.Rodrigues(rvec)
            eulerAngles = rotationMatrixToEulerAngles(R)
            cv2.putText(
                frame,
                f"Angles: {np.degrees(eulerAngles)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.putText(
                frame,
                f"Translation: {tvec}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

    # 显示结果
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC键退出
        break

cap.release()
cv2.destroyAllWindows()
