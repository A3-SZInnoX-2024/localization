from pupil_apriltags import Detection
from ..configuration.tags import get_tags

def get_tag_location(tag_id: int) -> tuple:
    tag_list = get_tags()
    if str(tag_id) not in tag_list:
        return None
    return tag_list[str(tag_id)]


def get_points(tags: list[Detection]):
    object_points: list[tuple[int, int, int]] = []
    image_points: list[tuple[int, int]] = []

    for tag in tags:
        id = str(tag.tag_id)

        # Get object point with tag ID
        object_x, object_y = get_tag_location(id)
        object_point = [object_x, object_y, 0]
        object_points.append(object_point)

        # Get image point with tag center
        image_point = tag.center
        image_points.append(image_point)

    return object_points, image_points
