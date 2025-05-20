from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from os import getenv
import yaml
import logging
import sys
import tomllib
import pathlib


SETTINGS_FILE = Path(getenv("SETTINGS_FILE", pathlib.Path.home() / ".config/cloudflare-dyndns-updater/config.toml"))


@dataclass
class Settings:
    """
    Settings class
    """

    auth_email: str
    auth_key: str
    zones: list

    def __init__(self) -> None:
        """
        Load the settings
        """
        self.read_settings()

    def read_settings(self) -> Dict:
        """
        Read the settings from the config.toml file
        """
        try:
            with open(SETTINGS_FILE, "rb") as settings_file:
                settings: Dict = tomllib.load(settings_file)
            self.auth_email = settings["auth_email"]
            self.auth_key = settings["auth_key"]
            self.zones = settings["zone_name"]

        except Exception:
            logging.error("Failed to load the settings")

            sys.exit()
