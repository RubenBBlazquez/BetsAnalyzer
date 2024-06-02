from common.downloader_base import DownloaderEntityBase
from common.selenium.selenium_client import SeleniumStepsGenerator


class FBRefDownloaderEntityBase(DownloaderEntityBase):
    """
    Entity that represents the information to create a team stats downloader dag
    """

    @property
    def dag_name(self) -> str:
        raise NotImplementedError(
            "You must implement the dag_name property in your FBRefEntityBase subclass"
        )

    def get_steps_generator(self) -> SeleniumStepsGenerator:
        raise NotImplementedError(
            "You must implement the steps_generator property in your FBRefEntityBase subclass"
        )
