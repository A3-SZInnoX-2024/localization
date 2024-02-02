from .recognition.scan import scan
import cv2
from .localization.kernel import Location
import numpy as np
from pupil_apriltags import Detector
from .recognition.detector import detect
from .configuration.colors import get_color_presets

location = Location(
    np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32), np.zeros(4)
)

colors = get_color_presets()

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Initialize AprilTag detector
    detector = Detector(
        families="tag36h11",
    )

    location = Location(
        np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32),
        np.zeros(4),
    )

    while True:
        ret, image = cap.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detection = detector.detect(gray)

        if not location.is_adjusted() and len(detection) < 6:
            # print('No data. Please move to the place with at least 6 tags')
            continue

        if not location.is_adjusted() and len(detection) >= 6:
            # print("Adjusting the camera")
            result = location.adjust(detection)

            if result is not None:
                print(f"z: {location.get_z()}, roll: {location.roll}, pitch: {location.pitch}")

        if location.is_adjusted():
            loc = location.locate(detection)

            colors = get_color_presets()

            det_res = detect(image, colors)

            # print(det_res)

            # print(loc)

        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
