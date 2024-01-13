from __future__ import annotations

from copy import deepcopy
from typing import Type

import attr
import cattrs


@attr.s(auto_attribs=True)
class SportMonksEntityBase:
    def to_dict(self) -> dict:
        """
        method to convert entity to dict

        Returns
        -------
        dict representation of entity
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, dict_: dict) -> SportMonksEntityBase:
        """
        method to cast dict to entity

        Returns
        -------
        entity
        """
        converter = deepcopy(cattrs.global_converter)
        return converter.structure(dict_, cls)


@attr.s(auto_attribs=True)
class DownloaderEntityBase:
    """
    Base Downloader Entity information
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
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

    @property
    def update_fields(self) -> list[str]:
        """
        method to obtain the fields by which we are going to update/upsert the data

        Returns
        -------
        list of update fields
        """
        return ["id"]
