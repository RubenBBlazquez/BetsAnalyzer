import os

from pymongo import MongoClient


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
