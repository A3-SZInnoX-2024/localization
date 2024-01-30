import cv2
import numpy as np


def detect_color(frame, lower_bound, upper_bound):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # You can add size filtering here
        cv2.drawContours(frame, [contour], -1, (255, 0, 0), 3)

    return frame


# Start capturing video from the first camera device
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Color ranges in HSV
    blue_lower = np.array([100, 150, 0], np.uint8)
    blue_upper = np.array([140, 255, 255], np.uint8)
    # ... Define other colors similarly

    # Detect each color
    frame = detect_color(frame, blue_lower, blue_upper)
    # ... Detect other colors similarly

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()
