import logging

import attr
import pandas as pd
from common.db_client.mongo_db_client import MongoDBConnection
from common.extractors.base import BaseExtractor
from pymongo import MongoClient


@attr.s(auto_attribs=True)
class MongoDBExtractor(BaseExtractor):
    """
    Class for extracting data to MongoDB

    Attributes
    -----------
    _database_name: str
        database where we are going to extract data
    """

    _database_name: str
    _db_connection: MongoClient = attr.s(init=False)

    def __attrs_post_init__(self):
        self._db_connection = MongoDBConnection().db_conn

    def extract(self) -> dict[str, pd.DataFrame]:
        extracted_information = {}

        for extractor_config in self._extractors_config:
            collection = extractor_config.collection

            logging.info(
                f"extracting data from {extractor_config.collection}"
                f" with config {extractor_config}"
            )
            db = self._db_connection.get_database(self._database_name)

            limit = extractor_config.limit
            offset = extractor_config.offset
            query = extractor_config.query
            sort = extractor_config.sort

            if limit and offset:
                extracted_information[collection] = pd.DataFrame(
                    db.get_collection(collection).find(query).sort(sort).skip(offset).limit(limit)
                )

            extracted_information[collection] = pd.DataFrame(
                db.get_collection(collection).find(query).sort(sort)
            )

        return extracted_information
