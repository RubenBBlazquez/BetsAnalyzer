from typing import Iterable

import attr

from data_pipelines.common.writers.writer import IEntity, IWriter


@attr.s(auto_attribs=True, frozen=True)
class MongoDBWriter(IWriter):
    """
    Class for writing data to MongoDB
    """

    _database_name: str

    def write(self, entities: Iterable[IEntity], collection: str):
        pass
