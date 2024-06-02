import logging
from typing import Optional

from attrs import define
from common.selenium.selenium_client import SeleniumStep
from selenium import webdriver
from selenium.webdriver.common.by import By


@define(auto_attribs=True)
class ClickStep(SeleniumStep):
    """
    Step that clicks a button

    Attributes
    ----------
    by: By
        method to find the element
    selector: str
        selector to find the element
    """

    by: By
    selector: str

    def execute(self, driver: webdriver.Remote) -> webdriver.Remote:
        element = driver.find_element(self.by, self.selector)
        element.click()

        return driver


@define(auto_attribs=True)
class SendKeysStep(SeleniumStep):
    """
    Step that sends keys to an input

    Attributes
    ----------
    selector: str
        selector to find the element
    by: By
        method to find the element
    keys: str
        keys to send
    """

    selector: str
    by: By
    keys: str

    def execute(self, driver: webdriver.Remote) -> webdriver.Remote:
        element = driver.find_element(self.by, self.selector)
        element.send_keys(self.keys)

        return driver


@define(auto_attribs=True)
class GoToStep(SeleniumStep):
    """
    Step that goes to a url

    Attributes
    ----------
    url: str
        url to go to
    """

    url: str
    by: By = By.TAG_NAME
    anchor_selector: Optional[str] = None

    def execute(self, driver: webdriver.Remote) -> webdriver.Remote:
        if self.anchor_selector:
            element = driver.find_element(self.by, self.anchor_selector)
            self.url = element.get_attribute("href")

        logging.info(f"Going to {self.url}")
        driver.get(self.url)

        return driver
