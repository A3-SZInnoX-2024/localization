from adjustment import adjustment
import numpy as np
import cv2
from pupil_apriltags import Detector
from kernel import Location


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

    location = Location(np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=np.float32), np.zeros(4))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the frame
        tags = detector.detect(gray)

        if (not location.is_adjusted()) and (len(tags) >= 6):
            result = location.adjust(tags)

            if result is not None:
                print(result.z, result.pitch, result.yaw)

        # Process each tag
        for tag in tags:
            # Draw a rectangle around the tag

            cv2.rectangle(
                frame,
                (int(tag.corners[0][0]), int(tag.corners[0][1])),
                (int(tag.corners[2][0]), int(tag.corners[2][1])),
                (0, 255, 0),
                2,
            )
            loc, lab = tag.center, str(tag.tag_id)

            result = location.locate(tags)

            print(result)

            # Display tag ID
            cv2.putText(
                frame,
                str(tag.tag_id),
                (int(tag.center[0]), int(tag.center[1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

            # Here you can also extract tag pose, location, etc.

        # Display the result
        cv2.imshow("AprilTag Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
