import logging
import os
from typing import Iterable

import attr
from pymongo import MongoClient

from data_pipelines.common.writers.writer import IEntity, IWriter


class MongoDBConnection:
    def __init__(self):
        user = os.getenv("MONGO_USER")
        password = os.getenv("MONGO_PASSWORD")
        host = os.getenv("MONGO_HOST")
        port = os.getenv("MONGO_PORT")
        auth_db = os.getenv("MONGO_AUTH_DATABASE")
        connection_uri = f"mongodb://{user}:{password}@{host}:{port}?authSource={auth_db}"
        self.db_conn = MongoClient(connection_uri)

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance


@attr.s(auto_attribs=True)
class MongoDBWriter(IWriter):
    """
    Class for writing data to MongoDB

    Parameters
    -----------
    _database_name: str
        database where we are going to write data
    """

    _database_name: str
    _db_connection: MongoClient = MongoDBConnection().db_conn

    def write(self, entities: Iterable[IEntity], collection: str):
        logging.info(
            f"Writing data in {collection} "
            f"from {self._database_name} "
            f"to Mongodb: {len(list(entities))}"
        )
        (
            self._db_connection.get_database(self._database_name)
            .get_collection(collection)
            .insert_many(entity.to_dict() for entity in entities)
        )
