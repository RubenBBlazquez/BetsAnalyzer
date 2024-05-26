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
    def schedule(self) -> str | list[Dataset]:
        """
        method to obtain the schedule from a dag
        """
        return "@daily"

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

    Attributes:
    -----------
    _entity: DownloaderEntityBase
        downloader entity
    _writer: IWriter
        writer to insert data

    """

    _entity: DownloaderEntityBase
    _writer: IWriter

    @property
    def entity(self):
        return self._entity

    @property
    def writer(self):
        return self._writer

    def get_downloader_tasks(self) -> list[Operator]:
        """
        method to get downloader tasks
        """
        raise NotImplementedError()
