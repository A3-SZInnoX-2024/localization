from cv2 import VideoCapture
from .localization.kernel import Location
from .recognition.kernel import BlockRecognition
from pupil_apriltags import Detector
import numpy as np
from cv2.typing import MatLike
import threading
import cv2
import tkinter
from .configuration.colors import get_color_presets
from socketio import Client
import tkinter.messagebox
from .calibration.internal.file import load_internal_parameters
from .calibration.external.file import load_external_parameters


class Core:
    cap: VideoCapture
    camera_matrix: np.ndarray
    distortion_coefficients: np.ndarray
    homogeneous_matrix: np.ndarray
    location: Location
    capturing: bool = False
    detector: Detector
    frame: MatLike
    thread_locate = None
    thread_recognize = None
    blocks: list[tuple[str, np.ndarray]]
    client: Client

    def __init__(self, capture: VideoCapture):
        self.cap = capture
        client = Client()
        client.connect("http://localhost:8000")
        self.client = client

        cont = tkinter.messagebox.askyesno(
            "Confirm",
            "Please confirm the camera is calibrated. If not, please calibrate it now with `python -m src.calibration.internal.core` and `python -m src.calibration.external.calibrate`",
        )

        if cont is False:
            exit(0)

        internal_parameters = load_internal_parameters()
        external_parameters = load_external_parameters()

        self.camera_matrix = internal_parameters["camera_matrix"]
        self.distortion_coefficients = internal_parameters["dist_coeffs"]
        self.homogeneous_matrix = external_parameters["homo_matrix"]

        self.location = Location(self.camera_matrix, self.distortion_coefficients, self.homogeneous_matrix)
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

            if self.location.is_adjusted():
                if len(tags) > 0:
                    self.location.locate(tags)

                    result = self.client.emit(
                        "location-cv",
                        (self.location.x, self.location.y, self.location.yaw),
                    )

                    recognition = BlockRecognition(
                        self.location, colors=get_color_presets()
                    )

                    self.blocks = recognition.recognize(self.cap)

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
    Core(VideoCapture(0))


if __name__ == "__main__":
    main()
