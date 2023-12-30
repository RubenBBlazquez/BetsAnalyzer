import logging

import attr
import pandas as pd
from common.db_client.mongo_db_client import MongoDBConnection
from pymongo import MongoClient

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
    _db_connection: MongoClient = MongoDBConnection().db_conn

    def write(self, entities: pd.DataFrame):
        logging.info(
            f"Writing data in {self._collection} "
            f"from {self._database_name} "
            f"to Mongodb: {entities.shape[0]}"
        )
        (
            self._db_connection.get_database(self._database_name)
            .get_collection(self._collection)
            .insert_many(entities.to_dict("records"))
        )
