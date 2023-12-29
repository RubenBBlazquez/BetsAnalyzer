import os
from copy import deepcopy
from enum import Enum
from typing import Any, Iterator

import attr
import cattrs

from data_pipelines.common.api_client_base import ApiClientBase
from data_pipelines.sport_monks.entities import Leagues, Player


class SportMonksCollections(Enum):
    """
    Enum for SportMonks API endpoints to get and download data
    """

    PLAYERS = "players"
    TEAMS = "teams"
    LEAGUES = "leagues"


ENTITY_SWITCHER = {
    SportMonksCollections.PLAYERS: Player,
    SportMonksCollections.LEAGUES: Leagues,
}


@attr.s(auto_attribs=True)
class SportMonksClient(ApiClientBase):
    """
    Class for SportMonks API client
    """

    def __attrs_post_init__(self):
        self.api_key = os.getenv("SPORT_MONKS_API_KEY", default="")
        self.api_url = os.getenv("SPORT_MONKS_BASE_URL", default="")

    def get_data_in_batches(self, collection: SportMonksCollections, entity: Any) -> Iterator[Any]:
        has_more_pages = True
        page = 1
        per_page = 50

        while has_more_pages:
            response = self.get(
                url=f"{self.api_url}/football/{collection.value}",
                params={"api_token": self.api_key, "page": page, "per_page": per_page},
            )
            has_more_pages = response["pagination"]["has_more"]
            page += 1

            converter = deepcopy(cattrs.global_converter)
            yield [converter.structure(data, entity) for data in response["data"]]
