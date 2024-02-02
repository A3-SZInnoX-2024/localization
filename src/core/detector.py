from cv2 import VideoCapture
from ..localization.kernel import Location
from ..recognition.kernel import BlockRecognition
from pupil_apriltags import Detector
import numpy as np
from ..calibration.file import load_calibration
from cv2.typing import MatLike
import threading
import cv2

class RobotCamera:
    cap: VideoCapture
    camera_matrix: np.ndarray
    distortion_coefficients: np.ndarray
    location: Location

    capturing: bool = False

    detector: Detector

    thread_locate = None

    def __init__(self, capture: VideoCapture):
        self.cap = capture

        try:
            calibration = load_calibration()
            self.camera_matrix = calibration["camera_matrix"]
            self.distortion_coefficients = calibration["dist_coeffs"]
        except:
            raise Exception("Calibration not found")

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

            if self.location.is_adjusted():
                if len(tags) > 0:
                    self.location.locate(tags)

    def stop_continuous_capture(self):
        self.capturing = False
        self.thread_locate.join()

    def get_capture(self):
        return self.cap

    def set_capture(self, capture: VideoCapture):
        self.cap = capture
        return self.cap

    def capture_image(self):
        ret, image = self.cap.read()

        if ret is None:
            raise Exception("Can't recognize the image")

        return image



