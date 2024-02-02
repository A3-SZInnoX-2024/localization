import cv2
import numpy as np

# 初始化摄像机捕获
cap = cv2.VideoCapture(0)  # 使用默认摄像机，也可以指定摄像机索引

# 创建窗口
cv2.namedWindow('Camera Feed')

# 声明全局变量 frame
frame = None

result = []

def get_hsv(event, x, y, flags, param):

    if frame is not None:
        pixel = frame[y, x]  # 获取鼠标点击位置的像素值
        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]  # 转换为HSV颜色空间
        hsv_text = f'H: {hsv_pixel[0]}, S: {hsv_pixel[1]}, V: {hsv_pixel[2]}'  # 创建要显示的文本
        print(hsv_text)
        cv2.putText(frame, hsv_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # 在图像上绘制文本
        result.append([y, x, hsv_pixel[0], hsv_pixel[1], hsv_pixel[2]])

# 设置鼠标回调函数
cv2.setMouseCallback('Camera Feed', get_hsv)

while True:
    ret, frame = cap.read()  # 从摄像机捕获帧

    cv2.imshow('Camera Feed', frame)  # 显示摄像机内容

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像机捕获
cap.release()
cv2.destroyAllWindows()

np.save('hsv.npy', result)
np.savetxt('hsv.txt', result, fmt='%d')
