from flask import Flask, jsonify, render_template
import docker
import logging

from src.config import config

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def get_docker_containers():
    socket_path = config.get("FLIP_FLOP_DOCKER_SOCKET_PATH")
    try:
        client = docker.DockerClient(base_url=f"unix:/{socket_path}")
        return client.containers.list()
    except Exception as e:
        app.logger.error(str(e))
        app.logger.error(f"Failed to connect to docker socket at {socket_path}")


def get_label(key, labels):
    instance_label = f'flip-flop.{config.get("FLIP_FLOP_INSTANCE")}.{key}'
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
    tabs = []
    keys = ["name", "url", "icon", "priority"]
    try:
        for c in containers:
            labels = c.labels
            tab = {}
            for key in keys:
                try:
                    tab[key] = get_label(key, labels)
                except Exception:
                    break
            if len(tab) == len(keys):
                tabs.append(tab)
        print(tabs)
        tabs.sort(key=lambda x: int(x["priority"]))
        return tabs
    except Exception as e:
        app.logger.error(f"Error fetching Docker labels: {e}")
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template(
        "index.html",
        name=config.get("FLIP_FLOP_NAME"),
        banner_title=config.get("FLIP_FLOP_BANNER_TITLE"),
        banner_body=config.get("FLIP_FLOP_BANNER_BODY"),
    )


@app.route("/docker-labels")
def docker_labels():
    labels = get_docker_labels()
    print(labels)
    return jsonify(labels)


if __name__ == "__main__":
    port = int(config.get("FLIP_FLOP_PORT"))
    app.run(host="0.0.0.0", port=port)
