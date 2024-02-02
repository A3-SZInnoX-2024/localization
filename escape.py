import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def find_and_merge_close_contours(image, threshold=50):
    """
    在给定的图像中找到并合并距离小于threshold的轮廓。

    参数:
    - image: 二值图像
    - threshold: 合并轮廓的最大距离

    返回:
    - image_with_contours: 绘制了合并后轮廓的图像
    """
    # 找到图像中的轮廓
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 合并轮廓的列表
    merged_contours = []

    # 遍历轮廓进行合并
    for contour in contours:
        # 如果已经合并，则跳过
        if any([(cv2.pointPolygonTest(contour, tuple(pt[0]), False) >= 0) for pt in merged_contours]):
            continue
        # 查找并合并靠近当前轮廓的所有轮廓
        close_contours = [contour]
        for other_contour in contours:
            if np.any([cv2.pointPolygonTest(other_contour, tuple(pt[0]), False) >= 0 for pt in close_contours]):
                continue
            distance = cv2.matchShapes(contour, other_contour, 1, 0.0)
            if distance < threshold:
                close_contours.append(other_contour)
        # 合并轮廓
        merged_contour = np.vstack(close_contours)
        merged_contours.append(merged_contour)

    # 在原图上绘制合并后的轮廓
    image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image_with_contours, merged_contours, -1, (0, 255, 0), 2)

    return image_with_contours


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # 转换到HSV色彩空间
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # opening = cv2.morphologyEx(hsv, cv2.MORPH_OPEN, (5, 5), iterations=5)

    # # 定义黑色的范围
    # lower_black = np.array([0, 0, 0])
    # upper_black = np.array([160, 255, 50])

    # # 根据定义的黑色范围创建掩码
    # mask = cv2.inRange(opening, lower_black, upper_black)

    # # 轮廓检测
    # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 合并轮廓
    merged_image = find_and_merge_close_contours(binary_image, threshold=50)

    # 显示结果
    cv2.imshow('Binary Image', binary_image)
    cv2.imshow('Merged Contours Image', merged_image)

    # 在原图上绘制轮廓
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # 显示结果
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Mask", mask)

    # 检测如果有大于 80 * 80 以上的黑色区域，就标出正方形 (红色)

    # 按'q'退出循环
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
