from __future__ import annotations

import attr
from airflow import Dataset
from airflow.models import Operator
from common.writers.base import IWriter


@attr.s(auto_attribs=True)
class DownloaderEntityBase:
    """
    Base Downloader Entity information
    """

    @property
    def dag_name(self) -> str:
        """
        method to obtain dag name for each entity

        Returns
        -------
        dag name
        """
        raise NotImplementedError()

    @property
    def update_fields(self) -> list[str]:
        """
        method to obtain the fields by which we are going to update/upsert the data

        Returns
        -------
        list of update fields
        """
        return ["id"]


@attr.s(auto_attribs=True)
class Downloader:
    """
    Base Downloader Entity information

    Attributes
    -----------
    _name: str
        name of the Downloader
    _schedule: str | Dataset
        schedule to run the Downloader
    _writer: IWriter
        writer to insert data
    """

    _name: str
    _schedule: str | list[Dataset]
    _writer: IWriter

    def get_downloader_tasks(self) -> list[Operator]:
        """
        method to get downloader tasks
        """
        raise NotImplementedError()
