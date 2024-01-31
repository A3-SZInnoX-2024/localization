import cv2
import numpy as np

# 读取图像
image = cv2.imread('test.jpg')

# 将BGR图像转换为HSV颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定义绿色在HSV空间中的范围
# 这些值可能需要调整以匹配图像中绿色的具体调
lower_green = np.array([40, 40, 40])
upper_green = np.array([70, 255, 255])

# 创建掩码以仅保留绿色
mask = cv2.inRange(hsv, lower_green, upper_green)

# 在掩码上找到轮廓
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓并筛选结果
for cnt in contours:
    # 可以根据需要添加更多条件来过滤轮廓
    area = cv2.contourArea(cnt)
    if area > 100:  # 假设绿色方块面积大于100
        # 绘制轮廓（可选）
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 3)

# 显示图像
cv2.imshow('Green Object', image)
cv2.waitKey(0)
cv2.imshow('Mask', mask)  # 显示掩码
cv2.waitKey(0)
cv2.destroyAllWindows()
