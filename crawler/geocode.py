import requests
import os
from loguru import logger

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def geocode_fetch(address: str):
    """
    Fetch geocode information for a given address.
    """
    res = requests.get(
        f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&language=zh-TW&key={API_KEY}"
    )

    data = res.json()

    if data['status'] != 'OK' or 'results' not in data:
        logger.error(f"Geocoding failed: {data['status']}")
        return None

    return data['results']
