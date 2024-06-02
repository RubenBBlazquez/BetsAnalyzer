import os

import attr
from airflow.models import Operator
from airflow.operators.python import PythonOperator
from common.downloader_base import Downloader
from common.selenium.selenium_client import SeleniumClient
from common.writers.mongo_db import MongoDBWriter
from downloaders.fbref.entities.base import FBRefDownloaderEntityBase
from downloaders.fbref.factories import DOWNLOADER_ENTITY_SWITCHER, RAW_DATA_COLLECTIONS_SWITCHER


@attr.s(auto_attribs=True)
class FBRefDownloader(Downloader):
    """
    Class for downloading data from fbref page
    """

    def _download_and_save_data(self):
        """
        Method to download and save data from sport_monks api
        """
        if not isinstance(self._entity, FBRefDownloaderEntityBase):
            raise ValueError("FBRef Downloader entity must be an instance of FBRefEntityBase")

        selenium_client = SeleniumClient(self.entity.steps_generator)
        result = selenium_client.execute()
        self.writer.write(result)

    def get_downloader_tasks(self) -> list[Operator]:
        """
        method to get downloader tasks
        """
        return [
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
            )
        ]


def get_fb_ref_downloaders():
    """
    Method to get fb_ref downloaders
    """
    for downloader_entity in DOWNLOADER_ENTITY_SWITCHER.keys():
        entity = DOWNLOADER_ENTITY_SWITCHER[downloader_entity]
        collection = RAW_DATA_COLLECTIONS_SWITCHER[downloader_entity]
        writer = MongoDBWriter(
            os.getenv("PROJECT_DATABASE", ""),
            collection,
            update_fields=entity.update_fields,
        )

        yield FBRefDownloader(
            entity=entity,
            writer=writer,
        )
