from .calibrate import calibrate_internal
from .camera import generate_points_through_chessboard

def calibrate_internal_parameters():
    obj, img, size = generate_points_through_chessboard()
    calibrate_internal(obj, img, size)

if __name__ == '__main__':
    calibrate_internal_parameters()
