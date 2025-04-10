import os
import json

class Config:
    REQUIRED_KEYS = {
        "SECRET_KEY": str,
        "SQLALCHEMY_DATABASE_URI": str,
        "SQLALCHEMY_TRACK_MODIFICATIONS": bool,
        "DEBUG": bool,
        "PORT": int
    }

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        config_data = self.load_config()
        self.validate_config(config_data)

        self.SECRET_KEY = config_data["SECRET_KEY"]
        self.SQLALCHEMY_DATABASE_URI = config_data["SQLALCHEMY_DATABASE_URI"]
        self.SQLALCHEMY_TRACK_MODIFICATIONS = config_data["SQLALCHEMY_TRACK_MODIFICATIONS"]
        self.DEBUG = config_data["DEBUG"]
        self.PORT = config_data["PORT"]

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' does not exist.")
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            return config_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing config file '{self.config_file}': {e}")

    def validate_config(self, config_data):
        missing = []
        for key, expected_type in self.REQUIRED_KEYS.items():
            if key not in config_data:
                missing.append(key)
            elif not isinstance(config_data[key], expected_type):
                raise ValueError(f"Invalid type for key '{key}': Expected {expected_type.__name__}, got {type(config_data[key]).__name__}")
        if missing:
            raise KeyError(f"Missing required config key(s): {', '.join(missing)}")