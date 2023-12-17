from flask import Flask, jsonify, render_template
import docker
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DOCKER_SOCKET_PATH = os.getenv("DOCKER_SOCKET_PATH", "/var/run/docker.sock")


def is_docker_socket_available():
    return os.path.exists(DOCKER_SOCKET_PATH)


def get_docker_labels():
    instance_name = os.getenv("FLIP_FLOP_INSTANCE_NAME", "default")

    if not is_docker_socket_available():
        app.logger.error("Docker socket not available.")
        return {"error": "Docker socket not available"}

    try:
        client = docker.from_env()
        containers = client.containers.list()

        # Filter containers that have the relevant labels
        relevant_containers = [
            c
            for c in containers
            if "flip-flop.url" in c.labels
            and instance_name in c.labels.get("flip-flop.instances", "").split(",")
        ]

        # Extract the required label information
        labels_info = [
            {
                "name": c.name,
                "url": c.labels.get("flip-flop.url"),
                "icon": c.labels.get("flip-flop.icon", ""),
            }
            for c in relevant_containers
        ]

        return labels_info
    except Exception as e:
        app.logger.error(f"Error fetching Docker labels: {e}")
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/docker-labels")
def docker_labels():
    labels = get_docker_labels()
    print(labels)
    return jsonify(labels)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 80))
    app.run(host="0.0.0.0", port=port)
