from flask import Flask, render_template
from flask_caching import Cache
import logging

from src.config import config
from src.docker import get_docker_labels

flask_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": config.get("FLIP_FLOP_CACHE_SECONDS"),
}

app = Flask(__name__)
app.config.from_mapping(flask_config)
cache = Cache(app)

logging.basicConfig(level=logging.INFO)


@app.route("/")
@cache.cached()
def index():
    tabs = get_docker_labels(app)
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
