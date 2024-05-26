from downloaders.fbref.entities.team import TeamStatsFBRef

TEAM_STATS_FB_REF_KEY = "team_stats_fb_ref"

RAW_DATA_COLLECTIONS_SWITCHER = {
    TEAM_STATS_FB_REF_KEY: "raw_data_fb_ref_team_stats",
}

DOWNLOADER_ENTITY_SWITCHER = {
    TEAM_STATS_FB_REF_KEY: TeamStatsFBRef(),
}
