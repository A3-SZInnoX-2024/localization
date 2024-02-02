import json
from hashlib import md5 # check if the file is the same

def get_tags():
    global tgs

    if tgs is not None:
        return tgs

    with open('tags.json') as f:
        tags = json.load(f)

    tgs = {}

    for tag in tags['tags']:
        print(tag)

        tgs[str(tag['id'])] = tuple(tag['position'])

    return tgs
