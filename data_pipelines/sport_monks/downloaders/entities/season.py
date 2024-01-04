import attr
from sport_monks.downloaders.entities.entity_base import DownloaderEntityBase


@attr.s(auto_attribs=True)
class Season(DownloaderEntityBase):
    """ """

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

    @staticmethod
    def get_middle_endpoint() -> str:
        return "football"

    @staticmethod
    def get_endpoint() -> str:
        return "seasons"
