#!/bin/python
import urllib.request
import pathlib
import sys
import requests
import yaml
import logging
from os import path
import os
import time

application_name = "CloudFlare DYNDNS Updater"
version = "1.1.0"


def read_settings():
    """
    Read the settings from the settings.yaml file
    """
    try:
        with open(r"/app/config/settings.yaml") as settings_file:
            return yaml.load(settings_file, Loader=yaml.FullLoader)
    except Exception:
        logging.error("Failed to load the settings")

        sys.exit()


def get_external_ip():
    """
    Get the external IP address using the https://ident.me service
    """
    try:
        return urllib.request.urlopen("https://ident.me").read().decode("utf-8")
    except Exception:
        logging.error(
            "Failed to get the public IP address, check your internet connection."
        )
        sys.exit()


def get_previous_ip():
    """
    Get the previous IP address from the previousip file
    """
    try:
        oldip = pathlib.Path("/app/previousip").read_text("utf-8")
    except FileNotFoundError:
        return ""

    return oldip


def save_ip(ip):
    """
    Save the IP address to the previousip file
    """
    try:
        with open("/app/previousip", "w", encoding="utf-8") as ipfile:
            ipfile.write(ip)
    except Exception:
        logging.error("Failed to save the old IP address.")
        sys.exit()


def get_zone_identifier(zone_name, auth_email, auth_key):
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


def get_record_identifier(zone_identifier, record, auth_email, auth_key):
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


def update_record(zone_identifier, record_identifier, record, ip, auth_email, auth_key):
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


def main():
    """
    Main function
    """
    if not path.exists("/app/logs"):
        os.makedirs("/app/logs")

    logging.basicConfig(
        level=logging.DEBUG,
        filename="/app/logs/cloudflare-dyndns-updater.log",
        filemode="a",
        format="%(name)s - %(levelname)s - %(message)s",
    )
    logging.info(f"{application_name} {version}")

    settings = read_settings()
    auth_email = ""
    auth_key = ""
    zone_name = ""
    records = []

    try:
        auth_email = settings["auth_email"]
        auth_key = settings["auth_key"]
        zone_name = settings["zone_name"]
        records = settings["records"]
    except Exception():
        logging.error("There was a problem loading the settings.")
        sys.exit()

    oldip = get_previous_ip()
    ip = get_external_ip()

    if oldip == ip:
        logging.info(
            f"The current IP {ip} is the same as the old IP {oldip} so no update required."
        )
        sys.exit()
    else:
        logging.info(f"Updating records to {ip}")

    zone_identifier = get_zone_identifier(zone_name, auth_email, auth_key)

    for record in records:
        record_identifier = get_record_identifier(
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

