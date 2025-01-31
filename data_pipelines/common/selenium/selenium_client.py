import logging
import os
import time
from abc import ABC, abstractmethod

import pandas as pd
from attrs import define
from selenium import webdriver


class NormalSeleniumStepException(Exception):
    pass

class SeleniumStep(ABC):
    """
    Interface that defines one step to be executed by the SeleniumClient
    """

    @abstractmethod
    def execute(self, driver: webdriver.Remote) -> webdriver.Remote:
        raise NotImplementedError("Method execute not implemented")


class DownloaderSeleniumStep(SeleniumStep):
    """
    Final step that returns the final DataFrame
    """

    @abstractmethod
    def execute(self, driver: webdriver.Remote) -> pd.DataFrame:
        raise NotImplementedError("Method execute not implemented")


class SeleniumStepsGenerator(ABC):
    """
    Interface that defines a method to generate a list of steps based on some selenium logic
    """

    @abstractmethod
    def generate_steps(self) -> list[SeleniumStep]:
        raise NotImplementedError("Method generate_steps not implemented")


@define(auto_attribs=True)
class SeleniumClient:
    """
    Selenium Client that executes a list of steps

    Attributes:
    -----------
    steps: list[SeleniumStep]
        list of steps to be executed
    retries_per_step: int = 2
        Number of retries for each step
    """

    steps: list[SeleniumStep]
    retries_per_step: int = 2

    def _execute_step(
        self, step: SeleniumStep, driver: webdriver.Remote
    ) -> webdriver.Remote | pd.DataFrame:
        """
        Method to execute and retry a step if needed
        """
        retries = self.retries_per_step

        while retries > 0:
            try:
                return step.execute(driver)
            except Exception as e:
                retries -= 1
                print(f"Error executing step: {e}")
                print(f"Retries left: {retries}")

                if retries == 0 and isinstance(e, NormalSeleniumStepException):
                    return pd.DataFrame()

                if retries == 0:
                    raise e


                time.sleep(1)

    def execute(self) -> pd.DataFrame:
        """
        Method to execute the steps and return the final DataFrame with the result
        """
        options = webdriver.ChromeOptions()
        options.enable_downloads = True
        options.headless = True

        driver = webdriver.Remote(
            command_executor=os.getenv("SELENIUM_HUB_SERVER"), options=options
        )
        result = pd.DataFrame()

        for step in self.steps:
            result_step = self._execute_step(step, driver)

            if isinstance(result_step, pd.DataFrame):
                result = pd.concat([result, result_step], ignore_index=True)
                continue

        return result.reset_index(drop=True)
