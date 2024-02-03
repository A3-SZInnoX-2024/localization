import cv2
import numpy as np
import tkinter.messagebox as tkmb
from .file import is_internal_parameters_exists


def generate_points_through_chessboard(board_size: tuple[int, int] = (8, 6)):
    if is_internal_parameters_exists():
        result = tkmb.askokcancel(
            "Calibration",
            "The camera is already calibrated. Do you want to recalibrate?",
        )

        if not result:
            tkmb.showinfo("Info", "The calibration was canceled")
            exit(0)

    tkmb.showinfo(
        "Info",
        "Please, press 'q' to stop the calibration. You should move the chessboard to different positions. Make sure that the chessboard is visible in the camera.",
    )

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
