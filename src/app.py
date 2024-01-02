from flask import Flask, render_template
import logging
import threading
import time
import os
import rcssmin
import rjsmin
import base64

from src.config import config
from src.docker import get_docker_labels

flask_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": config.get("FLIP_FLOP_CACHE_SECONDS"),
}

app = Flask(__name__)
app.config.from_mapping(flask_config)

logging.basicConfig(level=logging.INFO)


def read_encoded_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@app.route("/trigger-render")
def render_index():
    try:
        # Load minified CSS
        with open("src/static/css/index.css", "r") as f:
            index_css = f.read()
            index_css = rcssmin.cssmin(index_css)

        # Load minified JavaScript
        with open("src/static/js/index.js", "r") as f:
            index_js = f.read()
            index_js = rjsmin.jsmin(index_js)

        # Load and base64 encode an image
        index_favicon = read_encoded_image("src/static/img/flip_flop_favicon.png")

        version = config.get("FLIP_FLOP_VERSION")

        # Load and encode each image
        apps = get_docker_labels(app)
        for a in apps:
            path = os.path.join("src/static/img/generated/", a["icon"])
            a["icon"] = read_encoded_image(path)

        html = render_template(
            "index.html",
            css=index_css,
            js=index_js,
            favicon=index_favicon,
            name=config.get("FLIP_FLOP_NAME"),
            host=config.get("FLIP_FLOP_HOST"),
            banner_title=config.get("FLIP_FLOP_BANNER_TITLE"),
            banner_body=config.get("FLIP_FLOP_BANNER_BODY"),
            tabs=apps,
            version=version,
        )

        # save html
        directory = "src/static/html/generated/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, "index.html"), "w") as f:
            f.write(html)
        return "done", 200
    except Exception as e:
        app.logger.error(f"error while rendering index.html: {e}")
        return str(e), 500


def background_render_index():
    with app.app_context():
        with app.test_client() as client:
            while True:
                try:
                    client.get("/trigger-render")
                except Exception as e:
                    print(f"Error triggering render: {e}")
                time.sleep(config.get("FLIP_FLOP_CACHE_SECONDS"))


@app.route("/")
def index():
    path = "html/generated/index.html"
    if not os.path.exists(os.path.join("src/static/", path)):
        app.logger.info("pre-rendered index not found, rendering now")
        render_index()
    return app.send_static_file(path)


@app.route("/<path:path>")
def catch_all(path):
    return app.send_static_file("html/generated/index.html")


@app.route("/robots.txt")
def robots_txt():
    if config.get("FLIP_FLIP_ALLOW_ROBOTS"):
        robots_content = "User-agent: *\nAllow: /"
    else:
        robots_content = "User-agent: *\nDisallow: /"

    return robots_content, 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    thread = threading.Thread(target=background_render_index)
    thread.daemon = True  # Daemon threads will shut down when the main thread exits
    thread.start()

    port = int(config.get("FLIP_FLOP_PORT"))
    app.run(host="0.0.0.0", port=port)
