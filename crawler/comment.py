import time
import os
from loguru import logger
from selenium.common.exceptions import TimeoutException
from crawler.selectors.comment import SCROLL_CONTAINER, COMMENT_BTN, AVG_RATING, TOTAL_COUNT_CONTAINER, SINGLE_CONTAINER, AUTHOR, AUTHOR_DETAIL, RATING, CONTENT, READ_MORE_BTN, ITEM_BTNS, TAG_TXT, TAG_CONTAINER, TAG_COUNT
from crawler.action import wait_elements, wait_element, scroll_down, check_element

cmt_limit = int(os.getenv("COMMENT_LIMIT", 100))


def get_comments(limit=cmt_limit) -> dict:
    """
    Get comments for the current spot.
    """
    # Open comments section
    comments_button = wait_element(COMMENT_BTN)
    if not comments_button:
        logger.info('No comments section found, returning None.')
        return None
    comments_button.click()
    time.sleep(1.5)

    logger.info('Start scraping comments...')
    average_rating = float(wait_element(AVG_RATING).text)
    total_count = int(wait_element('.fontBodySmall', wait_element(
        TOTAL_COUNT_CONTAINER)).text.split('篇')[0][:-1].replace(',', ''))

    # Get tags
    tags = []
    tag_elements = wait_elements(
        TAG_CONTAINER) if check_element(TAG_CONTAINER) else []
    for tag_element in tag_elements:
        try:
            tag_count = wait_element(
                TAG_COUNT, tag_element, raise_error=True, timeout=0.001).text
            tag_text = wait_element(
                TAG_TXT, tag_element, raise_error=True, timeout=0.001).text
            tags.append((tag_text, int(tag_count)))
        except TimeoutException:
            logger.info('Tag text or count not found, skipping this tag.')
            continue
        except AttributeError:
            logger.info('Not tag label, skipping.')
            continue

    logger.info(
        f'Average Rating: {average_rating}, Total Comments: {total_count}, Tags: {len(tags)}')

    # Scrape START
    comments_data = []
    comments = None
    counter = 0
    while True:
        comments = wait_elements(SINGLE_CONTAINER)[counter:]
        if counter != 0:
            # Scroll down every 4 times
            if counter % 4 == 0:
                sec = wait_element(SCROLL_CONTAINER)
                scroll_down(sec)
            if not comments or len(comments_data) >= total_count or len(comments_data) >= limit:
                logger.info("No more comments to process or limit reached.")
                break
        counter += 1

        # Unfold long content
        read_more_buttons = wait_elements(
            READ_MORE_BTN, timeout=0.001, ignore_error=True)
        for button in read_more_buttons:
            if button.is_displayed():
                button.click()

        # CORE - Get details
        comment = comments[0]
        author = wait_element(AUTHOR, comment).text
        rating = int(wait_element(
            RATING, comment).get_attribute('aria-label')[:1])
        try:
            author_detail = wait_element(
                AUTHOR_DETAIL, comment, timeout=0.001, ignore_error=True).text
            content = wait_element(
                CONTENT, comment, timeout=0.001, ignore_error=True).text
        except AttributeError:
            logger.info('Comment content is not found, exiting...')
            break

        # Update comments 
        comments_data.append({
            'author': author,
            'author_detail': author_detail,
            'rating': rating,
            'content': content,
        })

    if comments_data:
        logger.info(f"Comments retrieved successfully.")
    else:
        logger.error(f"Failed to retrieve comments.")

    return {
        'average_rating': average_rating,
        'total_count': total_count,
        'comments': comments_data,
        'tags': tags
    }
