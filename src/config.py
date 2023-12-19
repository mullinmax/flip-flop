import os
import logging
import yaml

logging.basicConfig(level=logging.INFO)

default_config = {
    "FLIP_FLOP_NAME": "Flip Flop",
    "FLIP_FLOP_FAVICON": "",
    "FLIP_FLOP_THEME": "",
    "FLIP_FLOP_PORT": 80,
    "FLIP_FLOP_INSTANCE": "default",
    "FLIP_FLOP_BANNER_TITLE": "hello",
    "FLIP_FLOP_BANNER_BODY": "this is a test",
    "FLIP_FLOP_CONFIG_PATH": "/config/flip_flop.yaml",
    "FLIP_FLOP_DOCKER_SOCKET_PATH": "/var/run/docker.sock",
}


class Config:
    def __init__(self):
        self.conf = {}
        self.config_file_path = self.get("FLIP_FLOP_CONFIG_PATH")
        self.load_config_file()

    def load_config_file(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                self.conf = yaml.safe_load(file)
        else:
            logging.warning(
                "Config file not found at: {}".format(self.config_file_path)
            )

    def get(self, key):
        # try self
        if key in self.conf:
            return self.conf[key]

        # try environment variables
        env_value = os.getenv(key)
        if env_value is not None:
            self.conf[key] = env_value
            return env_value

        # try defaults
        if key in default_config:
            self.conf[key] = default_config[key]
            return default_config[key]

        # Key not found
        logging.error(f"Key '{key}' not found in any configuration source.")
        return None


config = Config()
