from .recognition.scan import scan
import cv2
from .localization.kernel import Location
import numpy as np
from pupil_apriltags import Detector
from .recognition.detector import detect

location = Location(
    np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32), np.zeros(4)
)


def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Initialize AprilTag detector
    detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0,
    )

    location = Location(
        np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32),
        np.zeros(4),
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fishes = detect(
            frame,
            [
                {
                    # "lower": (60, 120, 80),
                    # "upper": (90, 200, 255),
                    "lower": (10, 120, 150),
                    "upper": (30, 200, 255),
                },
            ],
        )

        if fishes is not None and len(fishes) > 0:
            print(fishes)

        for fish in fishes:
            cv2.drawContours(frame, [fish], 0, (0, 0, 255), 3)

        # Display the result
        cv2.imshow("AprilTag Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
