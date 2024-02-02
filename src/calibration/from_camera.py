import cv2
import numpy as np

def calibrate_with_chessboard(board_size: tuple[int, int] = (8, 6)):
    cap = cv2.VideoCapture(0)

    chessboard_size = board_size

    objp = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
    objp[:, :2] = np.indices(chessboard_size).T.reshape(-1, 2)

    object_points = []
    image_points = []

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if not ret:
            continue

        object_points.append(objp)
        image_points.append(corners)

        cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

        if len(object_points) > 25:
            break

    cap.release()
    cv2.destroyAllWindows()

    return object_points, image_points, gray.shape[::-1]
