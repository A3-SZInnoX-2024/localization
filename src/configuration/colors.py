import numpy as np
import json


# Create a list of color tuples
class Color:
    name: str
    range: list[tuple[tuple[int, int, int], tuple[int, int, int]]]

    def __init__(self, name, color_range):
        self.name = name
        self.range = color_range


def get_color_presets():
    # Load the color data
    with open("colors.json", "r") as file:
        color_data = json.load(file)

    colors = []

    for color in color_data["colors"]:
        print(color)
        name = color["color"]
        color_range = np.array(color["range"])
        colors.append(Color(name, color_range))
