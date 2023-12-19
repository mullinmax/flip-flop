from flask import Flask, jsonify, render_template
import docker
import os
import logging

from src.config import config

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def is_docker_socket_available():
    return os.path.exists(config.get("FLIP_FLOP_DOCKER_SOCKET_PATH"))


def get_docker_labels():
    instance_name = config.get("FLIP_FLOP_INSTANCE")

    if not is_docker_socket_available():
        app.logger.error("Docker socket not available.")
        return {"error": "Docker socket not available"}

    try:
        client = docker.from_env()
        containers = client.containers.list()

        # Filter containers that have the relevant labels
        def container_filter(c):
            intances = set(
                c.labels.get("flip-flop.instance", "").split(",")
                + c.labels.get("flip-flop.instances", "").split(",")
            )

            return instance_name in intances

        relevant_containers = [c for c in containers if container_filter(c)]

        # Extract the required label information
        labels_info = []
        for c in relevant_containers:
            try:
                name = c.labels.get("flip-flop.name")
                url = c.labels.get("flip-flop.url")
                icon = c.labels.get("flip-flop.icon", "")
                priority = c.labels.get("flip-flop.priority", 0)

                if name is None:
                    raise Exception("flip-flop.name was not found in labels")

                if url is None:
                    raise Exception("flip-flop.url was not found in labels")

                labels_info.append(
                    {"name": name, "url": url, "icon": icon, "priority": priority}
                )
            except Exception as e:
                app.logger.error(
                    f"Error fetching Docker labels for container named {c.name}\n{e}"
                )

        labels_info.sort(key=lambda x: int(x["priority"]))
        return labels_info
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
