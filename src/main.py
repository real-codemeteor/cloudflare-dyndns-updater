#!/usr/bin/env python
import logging
import sys
from os import getenv

import requests

from settings import Settings
from ip_service import get_external_ip

application_name = "CloudFlare DYNDNS Updater"
version = "1.1.0"

LOG_LEVEL = getenv("LOG_LEVEL", "INFO")


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
        settings: Settings = Settings()
    except Exception():
        logging.error("There was a problem loading the settings.")
        sys.exit()

    previous_ip: str = ""
    current_ip: str = get_external_ip()

    if previous_ip == current_ip:
        logging.info(
            f"The current IP {current_ip} is the same as the old IP {previous_ip} so no update required."
        )
        sys.exit()
    else:
        logging.info(f"Updating records to {current_ip}")

    zone_identifier: str = get_zone_identifier(
        settings.zone_name, settings.auth_email, settings.auth_key
    )

    for record in settings.records:
        record_identifier: str = get_record_identifier(
            zone_identifier, record, settings.auth_email, settings.auth_key
        )
        if record_identifier == "":
            logging.warning(
                f"Failed to get the record id for {record}. Skipping record."
            )
            continue
        update_record(
            zone_identifier,
            record_identifier,
            record,
            current_ip,
            settings.auth_email,
            settings.auth_key,
        )


if __name__ == "__main__":
    main()
