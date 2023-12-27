import os
import logging
import yaml

logging.basicConfig(level=logging.INFO)

default_config = {
    "FLIP_FLOP_NAME": "Flip Flop",
    "FLIP_FLOP_FAVICON": "",
    "FLIP_FLOP_THEME": "",
    "FLIP_FLOP_HOST": "https://github.com/mullinmax/flip-flop",
    "FLIP_FLOP_PORT": 80,
    "FLIP_FLOP_INSTANCE": "default",
    "FLIP_FLOP_BANNER_TITLE": "hello",
    "FLIP_FLOP_BANNER_BODY": "this is a test",
    "FLIP_FLOP_CONFIG_PATH": "/config/flip_flop.yaml",
    "FLIP_FLOP_DOCKER_SOCKET_PATH": "/var/run/docker.sock",
    "FLIP_FLOP_DEV_MODE": False,
    "FLIP_FLOP_CACHE_SECONDS": 30,
    "FLIP_FLOP_MOCK_CONTAINERS": {
        "mock 1": {
            "flip-flop.name": "App 1",
            "flip-flop.url": "https://example.com/app1",
            "flip-flop.icon": "🌐",
        },
        "mock 2": {
            "flip-flop.name": "App 2",
            "flip-flop.url": "https://example.com/app2",
            "flip-flop.icon": "🔧",
        },
        "mock 3": {},
    },
}


class Config:
    _instance = None  # Class attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Check if instance is already initialized
            self.initialized = True
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

    def set(self, key, value):
        """
        This funciton should probably only be used for tests
        """
        self.conf[key] = value

    def get(self, key):
        value = self._get(key)
        if key not in self.conf:
            self.conf[key] = value
        logging.info(f"Config Value used: {key}={value}")
        return value

    def _get(self, key):
        # try self
        if key in self.conf:
            return self.conf[key]

        # try environment variables
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value

        # try defaults
        if key in default_config:
            return default_config[key]

        # Key not found
        logging.error(f"Key '{key}' not found in any configuration source.")
        return None


config = Config()
