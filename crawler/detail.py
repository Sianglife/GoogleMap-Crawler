import time
from loguru import logger
from selenium.common.exceptions import NoSuchElementException
import crawler.selectors.google_icon as gicon
from crawler.selectors.detail import FIELD_CONTAINER, FIELD_ICON, FIELD_VALUE, TITLE, WEBSITE_LINK, SHARE_BTN, SHARE_URL_TXT, CLOSE_SHARE_BTN, CLOSE_PANEL_BTN, SPOT_TYPE
from crawler.action import wait_element, wait_elements


def get_map_url():
    """
    Get the share URL of the current spot.
    """
    time.sleep(0.5)
    wait_element(SHARE_BTN).click()
    share_url = wait_element(SHARE_URL_TXT).get_attribute('value')
    wait_element(CLOSE_SHARE_BTN).click()
    if share_url:
        return share_url
    else:
        raise ValueError("Failed to get share URL.")


def get_spot_detail():
    """
    Get detailed information about the current spot.
    """
    detail_containers = wait_elements(FIELD_CONTAINER)

    detail_results = {
        'title': wait_element(TITLE).text,
        'map_url': get_map_url(),
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        'spot_type': wait_element(SPOT_TYPE).text
    }
    counter = 0
    for i in range(len(detail_containers)):
        counter += 1
        detail = wait_elements(FIELD_CONTAINER)[i]
        try:
            icon = wait_element(FIELD_ICON, detail).text
            if icon == gicon.ADDRESS:
                value = wait_element(FIELD_VALUE, detail).text
                detail_results['address'] = value
            elif icon == gicon.PHONE:
                value = wait_element(FIELD_VALUE, detail).text
                detail_results['phone'] = value
            elif icon == gicon.WEBSITE:
                value = wait_element(
                    WEBSITE_LINK, detail).get_attribute('href')
                detail_results['website'] = value
        except (NoSuchElementException, AttributeError):
            pass

    if detail_results:
        title = detail_results.get('title', 'Unknown')
        logger.info(f"Detail of {title} retrieved successfully.")
    else:
        logger.error(f"Failed to retrieve detail.")

    return detail_results
