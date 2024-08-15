import os
from typing import Any

import attr
from common.cache_client.base import BaseCacheClient
from redis import Redis


@attr.s(auto_attribs=True)
class RedisCacheClient(BaseCacheClient):
    """
    Redis Client

    Attributes
    ----------
    _host: str
        host of the redis server
    _port: int
        port of the redis server
    _db: int
        db number
    """

    _host: str = attr.ib(default=os.getenv("REDIS_HOST", "localhost"))
    _port: int = attr.ib(default=os.getenv("REDIS_PORT", 6379))
    _db: int = attr.ib(default=os.getenv("REDIS_DB", 5))
    _client: Redis = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._client = Redis(host=self._host, port=self._port, db=self._db).client()

    def get(self, key: str) -> str:
        return self._client.get(key)

    def set(self, key: str, value: Any, timeout: int = 100000):
        self._client.set(key, value, ex=timeout)
