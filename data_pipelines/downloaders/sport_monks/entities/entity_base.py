from __future__ import annotations

from typing import Type

import attr
from common.downloader_base import DownloaderEntityBase
from common.utils import EntityWrapper


@attr.s(auto_attribs=True)
class SportMonksDownloaderEntityBase(DownloaderEntityBase):
    """
    Base Downloader Entity information
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[EntityWrapper]:
        """
        method to obtain the entity that wraps the endpoint data from sportMonks

        Returns
        -------
        endpoint entity wrapper
        """
        raise NotImplementedError()

    @property
    def endpoints(self) -> list[str]:
        """
        endpoints where you will obtain data in sportMonks for each entity

        Returns
        -------
        list[str]
        """
        raise NotImplementedError()

    @property
    def middle_endpoint(self) -> str:
        """
        middle endpoint to obtain data in sportMonks for each entity

        Returns
        -------
        middle endpoint
        """
        return "football"

    @property
    def dag_name(self) -> str:
        """
        method to obtain dag name for each entity

        Returns
        -------
        dag name
        """
        if len(self.endpoints) == 0:
            raise NotImplementedError()

        return self.endpoints[0].capitalize().replace("/", "_")

    @property
    def includes(self) -> list[str]:
        """
        method to obtain includes in sportMonks for each entity

        Returns
        -------
        list of includes
        """
        return []
