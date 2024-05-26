from attrs import define
from downloaders.fbref.entities.base import FBRefDownloaderEntityBase
from downloaders.fbref.specialized_selenium_steps.team_stats import (
    TeamStatsDownloaderStepsGenerator,
)


@define(auto_attribs=True)
class TeamStatsFBRef(FBRefDownloaderEntityBase):
    """
    Entity that represents the information to create a team stats downloader dag from fbref page
    """

    @property
    def dag_name(self) -> str:
        return "FBRef_Team_Stats_from_all_seasons"

    @property
    def schedule(self) -> str:
        return "@daily"

    @property
    def update_fields(self) -> list[str]:
        return ["season", "team_name"]

    @property
    def steps_generator(self) -> type[TeamStatsDownloaderStepsGenerator]:
        return TeamStatsDownloaderStepsGenerator
