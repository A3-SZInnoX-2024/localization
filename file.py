import cv2
import pupil_apriltags
import numpy as np

image = cv2.imread("test.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

detector = pupil_apriltags.Detector()

tags = detector.detect(gray)

for tag in tags:
    corners = np.array(tag.corners, dtype=np.int32)
    pts = corners.reshape((-1, 1, 2))
    cv2.polylines(image, np.array([pts], dtype=np.int32), True, (0, 255, 0), 2)

    cv2.putText(image, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

cv2.imshow("AprilTag Detector", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

