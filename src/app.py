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
    if not is_docker_socket_available():
        app.logger.error("Docker socket not available.")
        return {"error": "Docker socket not available"}

    try:
        client = docker.from_env()
        containers = client.containers.list()
        labels_info = {
            c.name: c.labels.get("flip-flop.url")
            for c in containers
            if "flip-flop.url" in c.labels
        }
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