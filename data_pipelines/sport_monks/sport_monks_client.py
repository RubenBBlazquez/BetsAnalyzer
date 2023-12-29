import os
from enum import Enum
from typing import Iterable

import attr

from data_pipelines.common.api_client_base import ApiClientBase


class SportMonksGetEndpoints(Enum):
    """
    Enum for SportMonks API endpoints to get and download data
    """

    PLAYERS = "players"
    TEAMS = "teams"


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_players(self) -> Iterable[dict]:
        """
        Method to get players from SportMonks API
        """
        next_page = 1
        while next_page:
            response = self.get(
                url=f"{self.api_url}/football/players",
                params={"api_token": self.api_key, "page": next_page},
            )
            next_page = response["pagination"]["next_page"]
            import web_pdb

            web_pdb.set_trace()
            yield from response["data"]
