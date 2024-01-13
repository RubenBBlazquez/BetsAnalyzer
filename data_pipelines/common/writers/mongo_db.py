import logging

import attr
import pandas as pd
from common.db_client.mongo_db_client import MongoDBConnection
from pymongo import MongoClient, UpdateOne

from data_pipelines.common.writers.base import IWriter


@attr.s(auto_attribs=True)
class MongoDBWriter(IWriter):
    """
    Class for writing data to MongoDB

    Attributes
    -----------
    _database_name: str
        database where we are going to write data
    _collection: str
        collection where we are going to write data
    """

    _database_name: str
    _collection: str
    _db_connection: MongoClient = attr.s(init=False)
    _update_fields: list = attr.ib(factory=lambda: [])

    def __attrs_post_init__(self):
        self._db_connection = MongoDBConnection().db_conn
        self.db = self._db_connection.get_database(self._database_name)

    def _generate_update_fields_query(self, entities: pd.DataFrame):
        data_to_update = []

        for row in entities.itertuples(index=False):
            update_fields = {}

            for field in self._update_fields:
                update_fields[field] = getattr(row, field)

            data_to_update.append(UpdateOne(update_fields, {"$set": row._asdict()}, upsert=True))

        return data_to_update

    def write(self, entities: pd.DataFrame):
        logging.info(
            f"Writing data in {self._collection} "
            f"from {self._database_name} "
            f"to Mongodb: {entities.shape[0]}"
        )

        self.db.get_collection(self._collection).bulk_write(
            self._generate_update_fields_query(entities)
        )
