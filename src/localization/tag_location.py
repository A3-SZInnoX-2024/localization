from pupil_apriltags import Detection

def get_tag_location(tag_id: int) -> tuple:
    tag_list = {
      "0": (0, 0),
      "1": (0, 1),
      "2": (0, 2),
      "3": (0, 3),
      "4": (0, 4),
      "5": (0, 9),
      "6": (0, 10),
      "7": (0, 11),
      "8": (0, 12),
      "9": (0, 13),
      "10": (1, 0),
      "11": (1, 1),
      "12": (1, 2),
      "13": (1, 3),
      "14": (1, 4),
      "15": (1, 6),
      "16": (1, 7),
      "17": (1, 9),
      "18": (1, 10),
      "19": (1, 11),
      "20": (1, 12),
      "21": (1, 13),
      "22": (2, 2),
      "23": (2, 3),
      "24": (2, 4),
      "25": (2, 9),
      "26": (2, 10),
      "27": (2, 11),
      "28": (4, 2),
      "29": (4, 3),
      "30": (4, 4),
      "31": (4, 9),
      "32": (4, 10),
      "33": (4, 11),
      "34": (5, 0),
      "35": (5, 1),
      "36": (5, 2),
      "37": (5, 3),
      "38": (5, 4),
      "39": (5, 6),
      "40": (5, 7),
      "41": (5, 9),
      "42": (5, 10),
      "43": (5, 11),
      "44": (5, 12),
      "45": (5, 13),
      "46": (6, 0),
      "47": (6, 1),
      "48": (6, 2),
      "49": (6, 3),
      "50": (6, 4),
      "51": (6, 9),
      "52": (6, 10),
      "53": (6, 11),
      "54": (6, 12),
      "55": (6, 13),
    }
    return tag_list[str(tag_id)]

def get_points(tags: list[Detection]):
    object_points = []
    image_points = []

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
