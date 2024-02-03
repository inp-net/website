import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from jinja2 import Environment, Template
from munch import DefaultMunch


def media_blocks(blocks):
    return [b for b in blocks if b.type == "media"]


def thumbnail(media, resolution):
    return "media/" + media.thumbnails.__dict__[str(resolution)]

def length_more_than(items, length):
    return len(items) >= length

def repository_url(metadata):
    url = metadata.additionalMetadata.git
    if not url:
        return None
    if re.match(r"^https?://.*", url):
        return url
    if "/" in url:
        return f"https://git.inpt.fr/{url}"
    return f"https://git.inpt.fr/net7/{url}"

def has_vertical_images(blocks):
    return any(b.dimensions.aspectRatio <= 1 for b in media_blocks(blocks))

projects = [
    DefaultMunch.fromDict(p)
    for (id, p) in json.loads(Path("database.json").read_text()).items()
    if id != "#meta"
]

important_projects = ["churros", "loca7"] # todo utiliser .metadata.additionalMetadata.important

def projects_sorter(p):
    if p.id in important_projects:
        return important_projects.index(p.id)
    return len(important_projects) + 1

projects.sort(key=projects_sorter)

pad_length = len("       Finished")
for p in projects:
    print(f"{'Included':>{pad_length}} {p.content.default.title}")

environment = Environment()
environment.filters["media_blocks"] = media_blocks
environment.filters["enumerate"] = enumerate
environment.filters["first_paragraph_text"] = lambda blocks: BeautifulSoup(
    [b for b in blocks if b.type == "paragraph"][0].content, "html.parser"
)("p")[0].text
environment.filters["thumbnail"] = thumbnail
environment.filters["repository_url"] = repository_url
environment.filters["length_more_than"] = length_more_than
environment.filters["has_vertical_images"] = has_vertical_images


template_code = environment.compile(Path("realisation.html.j2").read_text())
template = Template.from_code(environment, template_code, {})
rendered = template.render(projects=projects)

Path("realisation.html").write_text(rendered)
