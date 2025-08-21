import time
from loguru import logger
from modules.webdriver import driver
from crawler.selectors.search import RESULT_ITEM_A
from crawler.selectors.detail import FIELD_CONTAINER, CLOSE_PANEL_BTN
from crawler.detail import get_spot_detail
from crawler.comment import get_comments
from crawler.action import wait_element, wait_elements, scroll_into_view
from crawler.geocode import geocode_fetch
from modules.db import db_insert


def map_keyword_search(keyword: str) -> None:
    """
    Scrape all search results for a given keyword.
    Not support only spot result.
    """
    logger.info("\n")
    logger.info(f"Searching for keyword: {keyword}")

    # Open search page
    url = f'https://www.google.com/maps/search/{keyword}/'
    driver.get(url)

    # Press the first item to init page
    first_item = wait_element(RESULT_ITEM_A)
    if first_item:
        first_item.click()
        logger.info("Clicked on the first search result.")
    else:
        logger.error("First search result not found.")
        return

    # Wait detail panel to open
    if not wait_element(FIELD_CONTAINER):
        logger.error(
            "Field container not found after clicking the first item.")
        return
    logger.info("Detail panel opened successfully.")

    # Scrape loop START
    results = []
    list_a = None  # list of result items
    counter = 0  # finished count
    while True:
        time.sleep(0.5)
        list_a = wait_elements(RESULT_ITEM_A)[counter:]
        a = list_a[0]

        # Update scroll position every 6 items
        if counter % 6 == 0 and counter != 0:
            scroll_into_view(a)

        # Close last panel
        if counter != 0:
            wait_element(CLOSE_PANEL_BTN).click()

        # Check if finished
        if not list_a:
            logger.info("No more search results to process.")
            break
        counter += 1

        # Open item
        a.click()
        logger.info(f"Opened search result")
        time.sleep(0.3)  # wait loading
        a.click()  # click again to ensure the panel is open
        time.sleep(0.3)

        # Get detail
        detail = get_spot_detail()
        if not detail:
            continue
        time.sleep(0.5)

        # Get comments
        comments = get_comments()
        if not comments:
            continue
        time.sleep(0.5)

        # Fetch Google Geocode API
        address = detail.get('address', '')
        if address:
            geocode = geocode_fetch(address)
            if not geocode:
                continue
        else:
            geocode = None
            logger.warning("No address found for geocoding.")

        # Insert to db
        db_insert({
            **detail,
            'comments': comments,
            'geocode': geocode
        }, keyword)

        logger.info(
            f"Inserted search result: {detail['title']} into database.")

    return results
