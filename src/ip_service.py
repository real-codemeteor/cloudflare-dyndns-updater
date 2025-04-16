import logging
import sys

import requests
from requests import Response


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
