#!/usr/bin/env python
import logging
import sched
import sys
from dataclasses import dataclass
from os import getenv
from time import sleep, time
from typing import Optional

from services import CloudflareService, get_external_ip
from settings import Settings

application_name = "CloudFlare DYNDNS Updater"
version = "1.1.0"

LOG_LEVEL = getenv("LOG_LEVEL", "INFO")


@dataclass
class Main:
    previous_ip: Optional[str] = ""
    current_ip: Optional[str] = ""
    scheduler: Optional[sched.scheduler] = None

    @staticmethod
    def setup_logging():
        """
        Configure logging
        """
        logging.basicConfig(
            level=LOG_LEVEL,
            format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
        )

    def run(self) -> None:
        """
        Main function
        """
        Main.setup_logging()

        logging.info(f"{application_name} {version}")

        try:
            self.settings: Settings = Settings()
        except Exception():
            logging.error("There was a problem loading the settings.")
            sys.exit(1)

        self.cloudflare_service = CloudflareService(
            self.settings.auth_email, self.settings.auth_key
        )

        self.scheduler = sched.scheduler(time, sleep)

        self.update_ip()
        self.scheduler.run()

    def update_ip(self):
        self.scheduler.enter(60, 1, self.update_ip)
        self.current_ip = get_external_ip()

        if self.current_ip == "":
            return

        if self.previous_ip == self.current_ip:
            logging.info(
                f"The current IP {self.current_ip} is the same as the old IP, no update required."
            )
            return

        self.previous_ip = self.current_ip
        logging.info(f"Updating records to {self.current_ip}")

        zone_identifier: str = self.cloudflare_service.get_zone_identifier(
            self.settings.zone_name
        )

        if zone_identifier == "":
            logging.error(f"Failed to get the zone id for {self.settings.zone_name}")
            return

        for record in self.settings.records:
            record_identifier: str = self.cloudflare_service.get_record_identifier(
                zone_identifier, record
            )
            if record_identifier == "":
                logging.warning(
                    f"Failed to get the record id for {record}. Skipping record."
                )
                continue
            self.cloudflare_service.update_record(
                zone_identifier,
                record_identifier,
                record,
                self.current_ip,
            )

        logging.info("Update completed!")


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt. Exiting...")
        sys.exit()
