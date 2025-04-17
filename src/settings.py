from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from os import getenv
import yaml
import logging
import sys


SETTINGS_FILE = Path(getenv("SETTINGS_FILE", "./config/settings.yaml"))


@dataclass
class Settings:
    """
    Settings class
    """

    auth_email: str
    auth_key: str
    zone_name: str
    records: list

    def __init__(self) -> None:
        """
        Load the settings
        """
        self.read_settings()

    def read_settings(self) -> Dict:
        """
        Read the settings from the settings.yaml file
        """
        try:
            with open(SETTINGS_FILE) as settings_file:
                settings: Dict = yaml.load(settings_file, Loader=yaml.FullLoader)
            self.auth_email = settings["auth_email"]
            self.auth_key = settings["auth_key"]
            self.zone_name = settings["zone_name"]
            self.records = settings["records"]
        except Exception:
            logging.error("Failed to load the settings")

            sys.exit()
