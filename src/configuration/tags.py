import json

def get_tags():
    with open('tags.json') as f:
        tags = json.load(f)

    tgs = {}

    for tag in tags['tags']:
        print(tag)

        tgs[str(tag['id'])] = tuple(tag['position'])

    return tgs
