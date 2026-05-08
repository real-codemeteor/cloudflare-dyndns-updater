from dataclasses import dataclass
from pathlib import Path
from os import getenv
import logging
import sys
import tomllib
import pathlib


SETTINGS_FILE = Path(
    getenv(
        "SETTINGS_FILE",
        pathlib.Path.home() / ".config/cloudflare-dyndns-updater/config.toml",
    )
)


@dataclass
class Settings:
    """
    Settings class
    """

    account_id: str
    api_token: str
    zones: list

    def __init__(self) -> None:
        """
        Load the settings
        """
        self.read_settings()

    def read_settings(self) -> dict | None:
        """
        Read the settings from the config.toml file
        """
        try:
            with open(SETTINGS_FILE, "rb") as settings_file:
                settings: dict = tomllib.load(settings_file)
            self.account_id = settings["account_id"]
            self.api_token = settings["api_token"]
            self.zones = settings["zone_name"]

        except Exception:
            logging.error("Failed to load the settings")

            sys.exit()
