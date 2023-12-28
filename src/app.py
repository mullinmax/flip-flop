from PIL import Image, ImageFont
import requests
from io import BytesIO
from pilmoji import Pilmoji
import os
import hashlib
from flask import Flask, render_template
from flask_caching import Cache
from urllib.parse import urlparse
import docker
import logging

from src.config import config

flask_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": config.get("FLIP_FLOP_CACHE_SECONDS"),
}

app = Flask(__name__)
app.config.from_mapping(flask_config)
cache = Cache(app)

logging.basicConfig(level=logging.INFO)

# TODO crop to content
# TODO break out cropping/saving/hashing to seperate function/file
# TODO make render size configurable
# TODO get favicon getter check svg and other formats


def save_url_as_image(url):
    favicon_url = get_favicon_url(url)
    response = requests.get(favicon_url)
    if response.status_code == 200:
        image_content = response.content
        md5_hash = hashlib.md5(image_content).hexdigest()
        filename = f"{md5_hash}.png"
        image_path = os.path.join("./src/static/img/", filename)

        if not os.path.exists(image_path):
            image = Image.open(BytesIO(image_content))
            image.save(image_path)

        return filename
    return None


def save_emoji_as_image(emoji):
    base_image_size = 300  # Size of the base image
    font_size = 300  # Larger font size for a larger emoji

    # Create a base image with a white background
    with Image.new(
        "RGBA", (base_image_size, base_image_size), (255, 255, 255, 0)
    ) as image:
        font = ImageFont.truetype("./src/Roboto-Regular.ttf", font_size)

        with Pilmoji(image) as pilmoji:
            # Calculate the position to center the text (and emoji) in the image
            text_width, text_height = pilmoji.getsize(emoji, font=font)
            text_x = int((image.width - text_width) / 2)
            text_y = int((image.height - text_height) / 2)
            pilmoji.text((text_x, text_y), emoji, (0, 0, 0), font)

        # Save the image
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()
        md5_hash = hashlib.md5(image_bytes).hexdigest()
        filename = f"{md5_hash}.png"
        image_path = os.path.join("src/static/img/", filename)

        if not os.path.exists(image_path):
            image.save(image_path)

        return filename


def get_favicon_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"


def get_docker_containers():
    if config.get("FLIP_FLOP_DEV_MODE"):
        return config.get("FLIP_FLOP_MOCK_CONTAINERS")

    socket_path = config.get("FLIP_FLOP_DOCKER_SOCKET_PATH")
    try:
        client = docker.DockerClient(base_url=f"unix:/{socket_path}")
        return {c.name: c.labels for c in client.containers.list()}
    except Exception as e:
        app.logger.error(str(e))
        app.logger.error(f"Failed to connect to docker socket at {socket_path}")


def get_label(key, labels, instance):
    instance_label = f"flip-flop.{instance}.{key}"
    if instance_label in labels:
        return labels[instance_label]

    generic_label = f"flip-flop.{key}"
    if generic_label in labels:
        return labels[generic_label]

    defaults = {"priority": 9999, "icon": ""}
    if key in defaults:
        return defaults[key]

    raise Exception(f"no value or default found for key {key}")


def get_docker_labels():
    containers = get_docker_containers()
    instance = config.get("FLIP_FLOP_INSTANCE")
    tabs = []
    for container, labels in containers.items():
        try:
            tab = {
                "name": get_label("name", labels, instance),
                "url": get_label("url", labels, instance),
                "icon": get_label("icon", labels, instance),
                "priority": get_label("priority", labels, instance),
            }

            if tab["icon"] == "":
                tab["icon"] = save_url_as_image(tab["url"])
            else:
                tab["icon"] = save_emoji_as_image(tab["icon"])

            tabs.append(tab)
            app.logger.info(f"Added container {container}: {tab}")
        except Exception as e:
            app.logger.info(f"Not adding container {container} because {str(e)}")
    tabs.sort(key=lambda x: int(x["priority"]))
    return tabs


@app.route("/")
@cache.cached()
def index():
    tabs = get_docker_labels()
    app.logger.info(tabs)
    return render_template(
        "index.html",
        name=config.get("FLIP_FLOP_NAME"),
        host=config.get("FLIP_FLOP_HOST"),
        banner_title=config.get("FLIP_FLOP_BANNER_TITLE"),
        banner_body=config.get("FLIP_FLOP_BANNER_BODY"),
        tabs=tabs,
    )


if __name__ == "__main__":
    port = int(config.get("FLIP_FLOP_PORT"))
    app.run(host="0.0.0.0", port=port)
