import numpy as np
from ..localization.kernel import Location
from .camera import capture_image
from .detector import detect
from .locate import locate_block
from cv2 import VideoCapture
from ..configuration.colors import get_color_presets, Color


class BlockRecognition:
    blocks: list[tuple[str, np.ndarray]]  # List of tuple[color, position]
    location: Location
    colors: list[Color]

    def __init__(
        self,
        loc: Location,
        colors: list[Color] = None,
    ):
        if loc is None:
            raise Exception("You must specify the camera position detecting blocks")

        if colors is not None:
            self.colors = colors
        elif get_color_presets() is not None:
            self.colors = get_color_presets()
        else:
            raise Exception("You must specify the colors to detect")
        self.location = loc

    def recognize(self, capture: VideoCapture, z: float = 3.0):
        image = capture_image(capture)

        print(self.colors)

        image_points = detect(image, self.colors)

        print(image_points)

        result = []

        for points in image_points:
            for point in points:
                position = locate_block(self.location, point, z)
                result.append((points[0], position))

        self.blocks = result

        return result

    def get_blocks(self):
        return self.blocks
