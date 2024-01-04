import os
from enum import Enum
from typing import Any, Iterator

import attr
from sport_monks.downloaders.entities.entity_base import DownloaderEntityBase

from data_pipelines.common.api_client_base import ApiClientBase

DEFAULT_ENGLAND_COUNTRY_ID = 462
DEFAULT_GERMANY_COUNTRY_ID = 11
DEFAULT_SPAIN_COUNTRY_ID = 32


class SportMonksEndpoints(Enum):
    """
    Enum for SportMonks API endpoints to get and download data
    """

    PLAYERS = "players"
    PLAYERS_SPAIN = f"players/countries/{DEFAULT_SPAIN_COUNTRY_ID}"
    PLAYERS_ENGLAND = f"players/countries/{DEFAULT_ENGLAND_COUNTRY_ID}"
    PLAYERS_GERMANY = f"players/countries/{DEFAULT_GERMANY_COUNTRY_ID}"
    TEAMS = "teams"
    LEAGUES = "leagues"
    MATCHES = "fixtures"
    COUNTRIES = "countries"
    TYPES = "types"
    SEASONS = "seasons"


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_data_in_batches(self, entity: DownloaderEntityBase) -> Iterator[Any]:
        has_more_pages = True
        page = 1
        per_page = 50

        while has_more_pages:
            response = self.get(
                url=f"{self.api_url}/{entity.get_middle_endpoint()}/{entity.get_endpoint()}",
                params={
                    "api_token": self.api_key,
                    "page": page,
                    "per_page": per_page,
                    "include": ";".join(entity.get_includes()),
                },
            )

            has_more_pages = response["pagination"]["has_more"]
            page += 1

            yield [entity.from_dict(data) for data in response["data"]]
