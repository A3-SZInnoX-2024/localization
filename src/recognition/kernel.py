import numpy as np
from ..localization.kernel import Location
from .camera import capture_image
from .detector import detect
from .locate import locate_block


class BlockRecognition:
    blocks: list[tuple[str, np.ndarray]]  # List of tuple[color, position]
    location: Location

    def __init__(self, loc: Location):
        if loc is None:
            raise Exception("You must specify the camera position detecting blocks")

        self.location = loc

    def recognize(
        self,
        *colors: tuple[str, tuple[tuple[int, int, int], tuple[int, int, int]]],
        z: float = 3.0
    ):
        image = capture_image()

        image_points = [(detect(image, color), color[0]) for color in colors]

        result = []

        for points in image_points:
            for point in points:
                position = locate_block(self.location, point, z)
                result.append((points[0], position))

        self.blocks = result

        return result
