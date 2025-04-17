import logging
import sys
from dataclasses import dataclass

import requests


@dataclass
class CloudflareService:
    auth_email: str
    auth_key: str

    def get_zone_identifier(self, zone_name: str) -> str:
        """
        Get the zone identifier for the zone name
        """
        logging.info(f"Getting the zone id for {zone_name}...")
        try:
            response = requests.get(
                f"https://api.cloudflare.com/client/v4/zones?name={zone_name}",
                headers={
                    "X-Auth-Email": self.auth_email,
                    "X-Auth-Key": self.auth_key,
                    "Content-Type": "application/json",
                },
            )
            return response.json()["result"][0]["id"]

        except Exception:
            logging.warn(f"Failed to get the zone id for {zone_name}")
            return ""

    def get_record_identifier(self, zone_identifier: str, record: str) -> str:
        """
        Get the record identifier for the record name
        """
        logging.info(f"Getting the record id for {record}...")
        try:
            response = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records?name={record}",
                headers={
                    "X-Auth-Email": self.auth_email,
                    "X-Auth-Key": self.auth_key,
                    "Content-Type": "application/json",
                },
            )
            return response.json()["result"][0]["id"]
        except Exception:
            logging.warn(f"Failed to get the record id for {record}")
            return ""

    def update_record(
        self,
        zone_identifier: str,
        record_identifier: str,
        record: str,
        ip: str,
    ) -> None:
        """
        Update the record to the new IP address
        """
        logging.info(f"Updating record {record} to {ip}...")
        try:
            result = requests.put(
                f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records/{record_identifier}",
                headers={
                    "X-Auth-Email": self.auth_email,
                    "X-Auth-Key": self.auth_key,
                    "Content-Type": "application/json",
                },
                json={
                    "id": zone_identifier,
                    "type": "A",
                    "name": record,
                    "content": ip,
                },
            )
            if result.status_code != 200:
                logging.error(f"Failed to update {record} to {ip}")
        except Exception:
            logging.error(f"Failed to update {record} to {ip}")
