from downloaders.fbref.entities.player import PlayerStatsPerSeasonFBRef
from downloaders.fbref.entities.team import TeamStatsPerSeasonFBRef

TEAM_STATS_FB_REF_KEY = "team_stats_fb_ref_per_season"
PLAYER_STATS_FB_REF_KEY = "player_stats_fb_ref_per_season"

RAW_DATA_COLLECTIONS_SWITCHER = {
    TEAM_STATS_FB_REF_KEY: "raw_data_fb_ref_team_stats_per_season",
    PLAYER_STATS_FB_REF_KEY: "raw_data_fb_ref_player_stats_per_season_and_team",
}

DOWNLOADER_ENTITY_SWITCHER = {
    TEAM_STATS_FB_REF_KEY: TeamStatsPerSeasonFBRef(),
    PLAYER_STATS_FB_REF_KEY: PlayerStatsPerSeasonFBRef(
        RAW_DATA_COLLECTIONS_SWITCHER[TEAM_STATS_FB_REF_KEY],
    ),
}
