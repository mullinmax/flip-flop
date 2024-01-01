import docker
from src.config import config
from src.icon import get_icon


def get_docker_containers(app):
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


def get_docker_labels(app):
    containers = get_docker_containers(app)
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

            tab["icon"] = get_icon(app, tab)

            tabs.append(tab)
            app.logger.info(f"Added container {container}: {tab}")
        except Exception as e:
            app.logger.info(f"Not adding container {container} because {str(e)}")
    tabs.sort(key=lambda x: int(x["priority"]))
    return tabs
