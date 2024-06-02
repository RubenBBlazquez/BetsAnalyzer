from typing import Any

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def get_text_or_none(element, is_percentage=False):
    text = element.text
    if not text:
        return None

    if is_percentage:
        return float(text) / 100

    if text.isdigit():
        return int(text)

    return text


def get_element_or_none(driver: Any, xpath: str):
    try:
        return get_text_or_none(driver.find_element(By.XPATH, xpath))
    except NoSuchElementException:
        return None
