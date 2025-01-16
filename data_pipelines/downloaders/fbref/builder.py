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
    Class for downloading data from the fbref page.
    This class implements the downloading logic for fbref data.
    """

    def _generate_selenium_steps(self):
        """
        Method to generate selenium steps for data extraction.
        """
        return self.entity.steps_generator.generate_steps()

    def _download_and_save_data(self):
        """
        Method to download and save data from the fbref API.
        """
        if not isinstance(self._entity, FBRefDownloaderEntityBase):
            raise ValueError("FBRef Downloader entity must be an instance of FBRefEntityBase")

        selenium_client = SeleniumClient(self.entity.steps_generator)
        result = selenium_client.execute()
        self.writer.write(result)

    def get_downloader_tasks(self) -> list[Operator]:
        """
        Method to get downloader tasks for Airflow.

        Returns
        -------
        list[Operator]
            List of Airflow operators for downloading tasks.
        """
        return [
            PythonOperator(
                python_callable=self._generate_selenium_steps,
                task_id="get_selenium_steps_task_mapping",
                do_xcom_push=True,
            ),
            PythonOperator(
                python_callable=self._download_and_save_data,
                task_id="download_and_save_data",
            ),
        ]


def get_fb_ref_downloaders():
    """
    Method to get fb_ref downloaders.

    Yields
    ------
    FBRefDownloader
        Instances of FBRefDownloader for each downloader entity.
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
