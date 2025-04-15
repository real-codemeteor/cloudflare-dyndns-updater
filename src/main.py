#!/usr/bin/env python
import pathlib
import sys
from requests import Response
import requests
import yaml
import logging
import time
from typing import Dict
from pathlib import Path
from os import getenv

application_name = "CloudFlare DYNDNS Updater"
version = "1.1.0"

SETTINGS_FILE = Path(getenv("SETTINGS_FILE", "./config/settings.yaml"))
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")


def read_settings() -> Dict:
    """
    Read the settings from the settings.yaml file
    """
    try:
        with open(SETTINGS_FILE) as settings_file:
            return yaml.load(settings_file, Loader=yaml.FullLoader)
    except Exception:
        logging.error("Failed to load the settings")

        sys.exit()


def get_external_ip() -> str:
    """
    Get the external IP address using the https://ident.me service
    """
    try:
        response: Response = requests.get("https://4.ident.me")
        return response.text
    except Exception as e:
        logging.error(
            "Failed to get the public IP address, check your internet connection.", e
        )
        sys.exit()


def get_previous_ip() -> str:
    """
    Get the previous IP address from the previousip file
    """
    try:
        oldip = pathlib.Path("/app/previousip").read_text("utf-8")
    except FileNotFoundError:
        return ""

    return oldip


def save_ip(ip) -> None:
    """
    Save the IP address to the previousip file
    """
    try:
        with open("/app/previousip", "w", encoding="utf-8") as ipfile:
            ipfile.write(ip)
    except Exception:
        logging.error("Failed to save the old IP address.")
        sys.exit()


def get_zone_identifier(zone_name: str, auth_email: str, auth_key: str) -> str:
    """
    Get the zone identifier for the zone name
    """
    logging.info(f"Getting the zone id for {zone_name}...")
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones?name={zone_name}",
            headers={
                "X-Auth-Email": auth_email,
                "X-Auth-Key": auth_key,
                "Content-Type": "application/json",
            },
        )
        return response.json()["result"][0]["id"]

    except Exception:
        logging.error(f"Failed to get the zone id for {zone_name}")
        sys.exit()


def get_record_identifier(
    zone_identifier: str, record: str, auth_email: str, auth_key: str
) -> str:
    """
    Get the record identifier for the record name
    """
    logging.info(f"Getting the record id for {record}...")
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?name={record}",
            headers={
                "X-Auth-Email": auth_email,
                "X-Auth-Key": auth_key,
                "Content-Type": "application/json",
            },
        )
        return response.json()["result"][0]["id"]
    except Exception:
        return ""


def update_record(
    zone_identifier: str,
    record_identifier: str,
    record: str,
    ip: str,
    auth_email: str,
    auth_key: str,
) -> None:
    """
    Update the record to the new IP address
    """
    logging.info(f"Updating record {record} to {ip}...")
    try:
        result = requests.put(
            f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{record_identifier}",
            headers={
                "X-Auth-Email": auth_email,
                "X-Auth-Key": auth_key,
                "Content-Type": "application/json",
            },
            json={"id": zone_identifier, "type": "A", "name": record, "content": ip},
        )
        if result.status_code != 200:
            logging.error(f"Failed to update {record} to {ip}")
    except Exception:
        logging.error(f"Failed to update {record} to {ip}")


def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
    )
    logging.info(f"{application_name} {version}")


def main() -> None:
    """
    Main function
    """
    setup_logging()

    try:
        settings: Dict = read_settings()
        auth_email: str = settings["auth_email"]
        auth_key: str = settings["auth_key"]
        zone_name: str = settings["zone_name"]
        records: list = settings["records"]
    except Exception():
        logging.error("There was a problem loading the settings.")
        sys.exit()

    oldip: str = get_previous_ip()
    ip: str = get_external_ip()

    if oldip == ip:
        logging.info(
            f"The current IP {ip} is the same as the old IP {oldip} so no update required."
        )
        sys.exit()
    else:
        logging.info(f"Updating records to {ip}")

    zone_identifier: str = get_zone_identifier(zone_name, auth_email, auth_key)

    for record in records:
        record_identifier: str = get_record_identifier(
            zone_identifier, record, auth_email, auth_key
        )
        if record_identifier == "":
            logging.warning(
                f"Failed to get the record id for {record}. Skipping record."
            )
            continue
        update_record(
            zone_identifier, record_identifier, record, ip, auth_email, auth_key
        )

    save_ip(ip)
    time.sleep(20)


if __name__ == "__main__":
    main()

