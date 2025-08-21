import requests
from loguru import logger


def geocode_fetch(address: str):
    """
    Fetch geocode information for a given address.
    """
    res = requests.get(
        f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&language=zh-TW&key=AIzaSyDrYH3m2pWPLa841_6x62jI9xIwqB4iwUI"
    )

    data = res.json()

    if data['status'] != 'OK' or 'results' not in data:
        logger.error(f"Geocoding failed: {data['status']}")
        return None

    return data['results']
