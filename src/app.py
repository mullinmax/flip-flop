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
                tab["icon"] = get_favicon_url(tab["url"])

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
