from typing import Type

import attr
from downloaders.sport_monks.entities.entity_base import DownloaderEntityBase, SportMonksEntityBase


@attr.s(auto_attribs=True)
class Season(SportMonksEntityBase):
    """
    Entity that represents a season in sportmonks API
    """

    id: int
    sport_id: int
    league_id: int
    tie_breaker_rule_id: int
    name: str
    finished: bool
    pending: bool
    is_current: bool
    starting_at: str
    ending_at: str
    standings_recalculated_at: str
    games_in_current_week: bool


class SeasonsDownloader(DownloaderEntityBase):
    """
    Entity that represents the information to create a seasons downloader dag
    """

    @property
    def endpoint_entity_wrapper(self) -> Type[SportMonksEntityBase]:
        return Season

    @property
    def endpoints(self) -> list[str]:
        return ["seasons"]
