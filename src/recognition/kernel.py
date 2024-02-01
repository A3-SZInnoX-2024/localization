import numpy as np
from ..localization.kernel import Location
from .camera import capture_image

class BlockRecognition:
    blocks: list[tuple[str, np.ndarray]] # List of tuple[color, position]
    location: Location

    def __init__(self, loc: Location):
        if loc is None:
            raise Exception('You must specify the camera position detecting blocks')

        self.location = loc

    def recognize():
        image = capture_image()
