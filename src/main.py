#!/usr/bin/env python
import logging
import sys
from os import getenv

from cloudflare_service import CloudflareService
from ip_service import get_external_ip
from settings import Settings

application_name = "CloudFlare DYNDNS Updater"
version = "1.1.0"

LOG_LEVEL = getenv("LOG_LEVEL", "INFO")


def setup_logging():
    """
    Configure logging
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """
    Main function
    """
    setup_logging()

    logging.info(f"{application_name} {version}")

    try:
        settings: Settings = Settings()
    except Exception():
        logging.error("There was a problem loading the settings.")
        sys.exit()

    cloudflare_service = CloudflareService(settings.auth_email, settings.auth_key)

    previous_ip: str = ""
    current_ip: str = get_external_ip()

    if previous_ip == current_ip:
        logging.info(
            f"The current IP {current_ip} is the same as the old IP {previous_ip} so no update required."
        )
        sys.exit()
    else:
        logging.info(f"Updating records to {current_ip}")

    zone_identifier: str = cloudflare_service.get_zone_identifier(settings.zone_name)

    for record in settings.records:
        record_identifier: str = cloudflare_service.get_record_identifier(
            zone_identifier, record
        )
        if record_identifier == "":
            logging.warning(
                f"Failed to get the record id for {record}. Skipping record."
            )
            continue
        cloudflare_service.update_record(
            zone_identifier,
            record_identifier,
            record,
            current_ip,
        )


if __name__ == "__main__":
    main()
