import time
import os
from loguru import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.webdriver import driver

wait_timeout = os.getenv("WAIT_TIMEOUT_DEFAULT", 7)

def wait_element(selector, parent=driver, timeout=wait_timeout, raise_error=False, ignore_error=False):
    """
    Wait for an element to be present in the DOM.
    """
    if raise_error and ignore_error:
        logger.warning(
            "Both raise_error and ignore_error are set to True.")
    try:
        WebDriverWait(parent, timeout, poll_frequency=0.5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return parent.find_element(By.CSS_SELECTOR, selector)
    except TimeoutException:
        if raise_error:
            raise TimeoutException(
                f"Element with selector '{selector}' not found within {timeout} seconds.")
        if not ignore_error:
            logger.error(
                f"Element with selector '{selector}' not found within {timeout} seconds.")
        return None


def wait_elements(selector, parent=driver, timeout=wait_timeout, raise_error=False, ignore_error=False) -> list:
    """
    Wait for multiple elements to be present in the DOM.
    """
    if raise_error and ignore_error:
        logger.warning(
            "Both raise_error and ignore_error are set to True.")
    try:
        WebDriverWait(parent, timeout, poll_frequency=0.5).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return parent.find_elements(By.CSS_SELECTOR, selector)
    except TimeoutException:
        if raise_error:
            raise TimeoutException(
                f"Elements with selector '{selector}' not found within {timeout} seconds.")
        if not ignore_error:
            logger.error(
                f"Elements with selector '{selector}' not found within {timeout} seconds.")
        return []


def check_element(selector, parent=driver):
    """
    Check if an element is present in the DOM.
    """
    try:
        return parent.find_element(By.CSS_SELECTOR, selector)
    except Exception:
        return None


def wait_clickable(selector, timeout=wait_timeout):
    """
    Wait until an element is clickable.
    """
    try:
        WebDriverWait(driver, timeout, poll_frequency=0.5).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        return driver.find_element(By.CSS_SELECTOR, selector)
    except TimeoutException:
        logger.error(
            f"Element with selector '{selector}' not clickable within {timeout} seconds.")
        return None


def scroll_into_view(target):
    """
    Scroll the page to the target element.
    """
    driver.execute_script("""arguments[0].scrollIntoView();""", target)


def scroll_down(target, times=1, stop_condition=None):
    """
    Scroll down the specified number of times.
    """
    for _ in range(times):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", target)
        logger.info("Scrolled down.")
        time.sleep(0.1)
        if stop_condition and stop_condition():
            break

def press_end(target, times=1, stop_condition=None):
    """
    Press the End key on the target element the specified number of times.
    """
    for _ in range(times):
        target.send_keys(Keys.END)
        logger.info("End pressed.")
        time.sleep(0.1)
        if stop_condition and stop_condition():
            break
