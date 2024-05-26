import os
import time
from abc import ABC, abstractmethod

import pandas as pd
from attrs import define
from selenium import webdriver


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
    def generate_steps(self, driver: webdriver.Remote) -> list[SeleniumStep]:
        raise NotImplementedError("Method generate_steps not implemented")


@define(auto_attribs=True)
class SeleniumClient:
    """
    Selenium Client that executes a list of steps

    Attributes:
    -----------
    steps: SeleniumStepsGenerator
        Generator of steps
    retries_per_step: int = 2
        Number of retries for each step
    """

    steps_generator: SeleniumStepsGenerator
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
        steps = self.steps_generator.generate_steps(driver)

        for step in steps:
            if isinstance(step, DownloaderSeleniumStep):
                result = pd.concat([result, step.execute(driver)], ignore_index=True)
                continue

            self._execute_step(step, driver)

        return result.reset_index(drop=True)
