from flask import Flask, render_template, request
import logging
import threading
import time
import os
import rcssmin
import rjsmin
import base64
from functools import wraps
from datetime import datetime
import traceback

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


def log_route_info(f):
    if not config.get("FLIP_FLOP_LOG_REQUESTS"):
        return f

    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if not client_ip:
            client_ip = request.headers.get("X-Real-IP", "Unknown IP")

        user_agent = request.headers.get("User-Agent", "Unknown Agent")
        referrer = request.headers.get("Referer", "No Referrer")

        request_info = (
            f"{current_time}|{client_ip},{request.path},{user_agent},{referrer}"
        )
        app.logger.info(request_info)

        return f(*args, **kwargs)

    return decorated_function


@app.route("/trigger-render")
@log_route_info
def render_index():
    try:
        # Load minified CSS
        with open("src/static/css/index.css", "r") as f:
            index_css = f.read()
            if not config.get("FLIP_FLOP_SKIP_MINIFY"):
                index_css = rcssmin.cssmin(index_css)

        # Load minified JavaScript
        with open("src/static/js/index.js", "r") as f:
            index_js = f.read()
            if not config.get("FLIP_FLOP_SKIP_MINIFY"):
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
        stack_trace = traceback.format_exc()
        app.logger.error(f"Error while rendering index.html: {e}\n{stack_trace}")
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


@app.route("/robots.txt")
@log_route_info
def robots_txt():
    if config.get("FLIP_FLIP_ALLOW_ROBOTS"):
        robots_content = "User-agent: *\nAllow: /"
    else:
        robots_content = "User-agent: *\nDisallow: /"

    return robots_content, 200, {"Content-Type": "text/plain"}


@app.route("/")
@app.route("/<path:path>")
@log_route_info
def index(path=None):
    path = "html/generated/index.html"
    if not os.path.exists(os.path.join("src/static/", path)):
        app.logger.info("pre-rendered index not found, rendering now")
        render_index()
    return app.send_static_file(path)


if __name__ == "__main__":
    thread = threading.Thread(target=background_render_index)
    thread.daemon = True  # Daemon threads will shut down when the main thread exits
    thread.start()

    port = int(config.get("FLIP_FLOP_PORT"))
    app.run(host="0.0.0.0", port=port)
