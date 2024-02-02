from cv2 import VideoCapture
from ..localization.kernel import Location
from ..recognition.kernel import BlockRecognition
from pupil_apriltags import Detector
import numpy as np
from ..calibration.file import load_calibration, save_calibration
from cv2.typing import MatLike
import threading
import cv2
import tkinter
from ..calibration.from_camera import calibrate_with_chessboard
from ..calibration.calibrate import calibrate
from ..configuration.colors import get_color_presets


class Core:
    cap: VideoCapture
    camera_matrix: np.ndarray
    distortion_coefficients: np.ndarray
    location: Location
    capturing: bool = False
    detector: Detector
    frame: MatLike
    thread_locate = None
    thread_recognize = None
    blocks: list[tuple[str, np.ndarray]]

    def __init__(self, capture: VideoCapture):
        self.cap = capture

        try:
            calibration = load_calibration()
            self.camera_matrix = calibration["camera_matrix"]
            self.distortion_coefficients = calibration["dist_coeffs"]
        except:
            measure = tkinter.messagebox.askokcancel(
                "Do you want to calibrate it now?",
                "Calibration file does not exist. Do you want to launch your camera to capture and calculate the calibration?",
            )

            if not measure:
                tkinter.messagebox.showerror("Error", "Calibration file does not exist")
                exit(1)
            else:
                tkinter.messagebox.showinfo(
                    "Information",
                    "Please show the chessboard to the camera with different angles and distances",
                )
                object_points, image_points, shape = calibrate_with_chessboard()

                self.camera_matrix, self.distortion_coefficients = calibrate(
                    object_points, image_points, shape
                )

                save_calibration(self.camera_matrix, self.distortion_coefficients)

                tkinter.messagebox.showinfo("Information", "Calibration was successful")

        self.location = Location(self.camera_matrix, self.distortion_coefficients)
        self.detector = Detector(families="tag36h11", nthreads=1)
        self.start_continuous_capture()

    def start_continuous_capture(self):
        self.capturing = True
        self.thread_locate = threading.Thread(target=self.continuous_capture)
        self.thread_locate.start()

    def continuous_capture(self):
        while self.capturing:
            image = self.capture_image()

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            tags = self.detector.detect(gray)

            if self.location.is_adjusted() is False and len(tags) > 6:
                self.location.adjust(tags)
                # self.start_block_detection()
                print(
                    "Camera adjusted.",
                    f"Location: {self.location.x, self.location.y, self.location.z},",
                    f"Rotation: {self.location.roll, self.location.pitch, self.location.yaw}",
                )

            if self.location.is_adjusted():
                if len(tags) > 0:
                    self.location.locate(tags)

                    recognition = BlockRecognition(
                        self.location, colors=get_color_presets()
                    )

                    self.blocks = recognition.recognize(self.cap)
                    print(
                        "Camera located.",
                        f"Location: {self.location.x, self.location.y, self.location.z},",
                        f"Rotation: {self.location.roll, self.location.pitch, self.location.yaw}",
                    )

    def stop_continuous_capture(self):
        self.capturing = False
        self.cap.release()
        self.thread_locate.join()

    def start_block_detection(self):
        self.thread_recognize = threading.Thread(target=self.block_detection)
        self.thread_recognize.start()

    def block_detection(self):
        while self.capturing and self.location.is_adjusted():
            recognition = BlockRecognition(self.location, colors=get_color_presets())
            result = recognition.recognize(self.cap)
            print(result)

    def stop_block_detection(self):
        self.thread_recognize.join()

    def get_capture(self):
        return self.cap

    def set_capture(self, capture: VideoCapture):
        self.cap = capture
        return self.cap

    def capture_image(self):
        ret, self.frame = self.cap.read()

        if ret is None:
            raise Exception("Can't recognize the image")

        return self.frame

    def get_available_blocks(self):
        return self.blocks

    def get_location(self):
        return self.location


def main():
    try:
        cap = cv2.VideoCapture(0)
        camera = Core(cap)
    except Exception as e:
        tkinter.messagebox.showerror("Error", e)
        exit(1)


if __name__ == "__main__":
    main()
