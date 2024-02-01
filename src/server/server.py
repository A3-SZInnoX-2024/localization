from fastapi import FastAPI
import json
from typing import Union
from pydantic import BaseModel

app = FastAPI()


class Color(BaseModel):
    color: str
    range: list[tuple[tuple[int, int, int], tuple[int, int, int]]]


class Tag(BaseModel):
    id: str
    position: tuple[int, int]


@app.get("/")
def root():
    return {
        "colors": "/colors",
        "tags": "/tags",
    }


@app.get("/colors")
def colors():
    with open("../configuration/colors.json") as f:
        colors = json.load(f)
        return colors["colors"]


@app.get("/colors/{color_id}")
def color(color_id: int):
    with open("../configuration/colors.json") as f:
        colors = json.load(f)
        return colors["colors"][color_id]


@app.get("/tags")
def tags():
    with open("../configuration/tags.json") as f:
        tags = json.load(f)
        return tags["tags"]


@app.get("/tags/{tag_id}")
def tag(tag_id: int):
    with open("../configuration/tags.json") as f:
        tags = json.load(f)
        return tags["tags"][tag_id]


@app.post("/colors")
def create_color(item: Color):
    with open("../configuration/colors.json", "r") as f:
        colors = json.load(f)["colors"]
    colors.append(item.model_dump())
    with open("../configuration/colors.json", "w") as f:
        json.dump({"colors": colors}, f)

    return None

@app.post("/tags")
def create_tag(item: Tag):
    with open("../configuration/tags.json", "r") as f:
        tags = json.load(f)["tags"]
    tags.append(item.model_dump())
    with open("../configuration/tags.json", "w") as f:
        json.dump({"tags": tags}, f)

    return None


@app.put("/colors/{color_id}")
def update_color(color_id: int, item: Color):
    with open("../configuration/colors.json", "r") as f:
        colors = json.load(f)["colors"]
    colors[color_id] = item.model_dump()
    with open("../configuration/colors.json", "w") as f:
        json.dump({"colors": colors}, f)

    return None


@app.put("/tags/{tag_id}")
def update_tag(tag_id: int, item: Tag):
    with open("../configuration/tags.json", "r") as f:
        tags = json.load(f)["tags"]
    tags[tag_id] = item.model_dump()
    with open("../configuration/tags.json", "w") as f:
        json.dump({"tags": tags}, f)

    return None
