from pupil_apriltags import Detection
from .tag_location import get_points


def generate_points(tags: list[Detection], tag_width: float = 205):
    object_points, image_points = [], []

    tags_object, tags_image = get_points(tags)

    for i in range(len(tags)):
        tag = tags[i]
        tag_object = tags_object[i]

        x, y, z = tag_object

        lt_image, rt_image, rb_image, lb_image = tag.corners

        lt_object = (x - tag_width / 2, y + tag_width / 2, z)
        rt_object = (x + tag_width / 2, y + tag_width / 2, z)
        rb_object = (x + tag_width / 2, y - tag_width / 2, z)
        lb_object = (x - tag_width / 2, y - tag_width / 2, z)

        object_points.append(lb_object)
        object_points.append(lt_object)
        object_points.append(rt_object)
        object_points.append(rb_object)

        image_points.append(lb_image)
        image_points.append(lt_image)
        image_points.append(rt_image)
        image_points.append(rb_image)

        object_points.append(tag_object)
        image_points.append(tag.center)

    return object_points, image_points
