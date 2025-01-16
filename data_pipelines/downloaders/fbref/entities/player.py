from typing import Type

from airflow import Dataset
from attrs import define
from downloaders.fbref.entities.base import FBRefDownloaderEntityBase
from downloaders.fbref.specialized_selenium_steps.player_stats import (
    PLayerStatsDownloaderStepsGenerator,
)


@define(auto_attribs=True)
class PlayerStatsPerSeasonFBRef(FBRefDownloaderEntityBase):
    """
    Entity that represents the information to create a team stats downloader dag from fbref page

    Attributes:
    -----------
    team_collection: str
        collection where the team stats are stored
    """

    _team_collection: str

    @property
    def dag_name(self) -> str:
        return "FBRef_Player_Stats_per_season"

    @property
    def schedule(self) -> str | list[Dataset]:
        return [Dataset(self._team_collection)]

    @property
    def update_fields(self) -> list[str]:
        return ["season", "team", "player"]

    @property
    def steps_generator(self) -> Type[PLayerStatsDownloaderStepsGenerator]:
        return PLayerStatsDownloaderStepsGenerator
