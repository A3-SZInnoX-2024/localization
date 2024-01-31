class Position:
    x: int
    y: int
    z: int

class Orientation:
    yaw: int
    pitch: int
    roll: int

class Fish:
    color: str
    location: Position

class Positure:
    position: Position
    orientation: Orientation
    def __init__(self, position: Position, orientation: Orientation):
        self.position = position
        self.orientation = orientation
