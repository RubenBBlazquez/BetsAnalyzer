import logging
import os

import attr
import pandas as pd
from attrs import define
from common.extractors.base import ExtractorConfig
from common.extractors.mongo_db import MongoDBExtractor
from common.selenium.common_steps import GoToStep
from common.selenium.parsing_methods import get_element_or_none
from common.selenium.selenium_client import (
    DownloaderSeleniumStep,
    SeleniumStep,
    SeleniumStepsGenerator,
)
from selenium import webdriver
from selenium.webdriver.common.by import By


@attr.s(auto_attribs=True)
class PLayerStatsDownloaderStepsGenerator(SeleniumStepsGenerator):
    """
    Class to generate the steps to download the team stats from the fbref page

    Attributes:
    -----------
    teams_collection: str
        Collection of the teams
    """

    _teams_collection: str
    _db_project_name = os.getenv("PROJECT_DATABASE", "bets_analyzer")
    _seasons: list[str] = [
        "2000-2001",
        "2001-2002",
        "2002-2003",
        "2003-2004",
        "2004-2005",
        "2005-2006",
        "2006-2007",
        "2007-2008",
        "2008-2009",
        "2009-2010",
        "2010-2011",
        "2011-2012",
        "2012-2013",
        "2013-2014",
        "2014-2015",
        "2015-2016",
        "2016-2017",
        "2017-2018",
        "2018-2019",
        "2019-2020",
        "2020-2021",
        "2021-2022",
        "2022-2023",
        "2023-2024",
    ]

    def _get_teams_from_season(self, season: str) -> pd.DataFrame:
        return MongoDBExtractor(
            [ExtractorConfig(self._teams_collection, query={"season": season})],
            self._db_project_name,
        ).extract()[self._teams_collection]

    @staticmethod
    def _generate_steps(season: str, team: str) -> list[SeleniumStep]:
        return [
            GoToStep(
                url=f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats",
            ),
            GoToStep(
                url="",
                by=By.XPATH,
                anchor_selector=f"//a[contains(text(), '{team}')]",
            ),
            DownloadSeasonPlayerStatsStep(season, team),
        ]

    def generate_steps(self) -> list[SeleniumStep]:
        steps = []

        logging.info("::group:: Teams per seasons extraction logs")

        for season in self._seasons:
            teams = self._get_teams_from_season(season)

            if teams.empty:
                logging.info("No teams found for season %s", season)
                continue

            season_teams = teams.team_name

            for team in season_teams:
                steps.extend(self._generate_steps(season, team))

        logging.info("::endgroup::")

        return steps


@define(auto_attribs=True)
class DownloadSeasonPlayerStatsStep(DownloaderSeleniumStep):
    """
    Step to download the team stats from the fbref page

    Attributes:
    -----------
    season: str
        Season of the player stats
    team: str
        Team of the player stats
    """

    season: str
    team: str

    @staticmethod
    def _get_standard_stats(rows_standard_table, index) -> dict[str, str]:
        if not rows_standard_table:
            return {
                "nation": None,
                "position": None,
                "age": None,
                "matches_played": None,
                "starts": None,
                "minutes_played": None,
                "ninetys_played": None,
                "goals": None,
                "assists": None,
                "goals_plus_assists": None,
                "goals_minus_penalties": None,
                "penalties_made": None,
                "penalties_attempted": None,
                "yellow_cards": None,
                "red_cards": None,
                "expected_goals": None,
                "non_penalty_expected_goals": None,
                "expected_assists": None,
                "npxg_plus_xa": None,
                "progressive_carries": None,
                "progressive_passes": None,
                "progressive_passes_received": None,
                "goals_per_90": None,
            }

        row_standard_table = rows_standard_table[index]

        return {
            "nation": get_element_or_none(row_standard_table, './td[@data-stat="nationality"]'),
            "position": get_element_or_none(row_standard_table, './td[@data-stat="position"]'),
            "age": get_element_or_none(row_standard_table, './td[@data-stat="age"]'),
            "matches_played": get_element_or_none(row_standard_table, './td[@data-stat="games"]'),
            "starts": get_element_or_none(row_standard_table, './td[@data-stat="games_starts"]'),
            "minutes_played": get_element_or_none(row_standard_table, './td[@data-stat="minutes"]'),
            "ninetys_played": get_element_or_none(
                row_standard_table, './td[@data-stat="minutes_90s"]'
            ),
            "goals": get_element_or_none(row_standard_table, './td[@data-stat="goals"]'),
            "assists": get_element_or_none(row_standard_table, './td[@data-stat="assists"]'),
            "goals_plus_assists": get_element_or_none(
                row_standard_table, './td[@data-stat="goals_assists"]'
            ),
            "goals_minus_penalties": get_element_or_none(
                row_standard_table, './td[@data-stat="goals_pens"]'
            ),
            "penalties_made": get_element_or_none(
                row_standard_table, './td[@data-stat="pens_made"]'
            ),
            "penalties_attempted": get_element_or_none(
                row_standard_table, './td[@data-stat="pens_att"]'
            ),
            "yellow_cards": get_element_or_none(
                row_standard_table, './td[@data-stat="cards_yellow"]'
            ),
            "red_cards": get_element_or_none(row_standard_table, './td[@data-stat="cards_red"]'),
            "expected_goals": get_element_or_none(row_standard_table, './td[@data-stat="xg"]'),
            "non_penalty_expected_goals": get_element_or_none(
                row_standard_table, './td[@data-stat="npxg"]'
            ),
            "expected_assists": get_element_or_none(
                row_standard_table, './td[@data-stat="xg_assist"]'
            ),
            "npxg_plus_xa": get_element_or_none(
                row_standard_table, './td[@data-stat="npxg_xg_assist"]'
            ),
            "progressive_carries": get_element_or_none(
                row_standard_table, './td[@data-stat="progressive_carries"]'
            ),
            "progressive_passes": get_element_or_none(
                row_standard_table, './td[@data-stat="progressive_passes"]'
            ),
            "progressive_passes_received": get_element_or_none(
                row_standard_table, './td[@data-stat="progressive_passes_received"]'
            ),
            "goals_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="goals_per90"]'
            ),
            "assists_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="assists_per90"]'
            ),
            "goals_plus_assists_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="goals_assists_per90"]'
            ),
            "goals_minus_penalties_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="goals_pens_per90"]'
            ),
            "expected_goals_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="xg_per90"]'
            ),
            "expected_assists_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="xg_assist_per90"]'
            ),
            "expected_goals_plus_assists_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="xg_xg_assist_per90"]'
            ),
            "non_penalty_expected_goals_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="npxg_per90"]'
            ),
            "npxg_plus_xa_per_90": get_element_or_none(
                row_standard_table, './td[@data-stat="npxg_xg_assist_per90"]'
            ),
        }

    @staticmethod
    def _get_shooting_stats(rows_shooting_table, index) -> dict[str, str]:
        if not rows_shooting_table or index >= len(rows_shooting_table):
            return {
                "shots": None,
                "shots_on_target": None,
                "shots_on_target_percentage": None,
                "shots_per_90": None,
                "shots_on_target_per_90": None,
                "goals_per_shot": None,
                "goals_per_shot_on_target": None,
                "average_shot_distance": None,
                "free_kick_shots": None,
                "penalty_kick_attempts": None,
                "expected_goals_shooting": None,
                "non_penalty_expected_goals_shooting": None,
                "non_penalty_expected_goals_per_shot": None,
                "goals_minus_expected_goals": None,
                "non_penalty_goals_minus_expected_goals": None,
            }

        row_shooting_table = rows_shooting_table[index]
        return {
            "shots": get_element_or_none(row_shooting_table, './td[@data-stat="shots_total"]'),
            "shots_on_target": get_element_or_none(
                row_shooting_table, './td[@data-stat="shots_on_target"]'
            ),
            "shots_on_target_percentage": get_element_or_none(
                row_shooting_table, './td[@data-stat="shots_on_target_pct"]'
            ),
            "shots_per_90": get_element_or_none(
                row_shooting_table, './td[@data-stat="shots_per90"]'
            ),
            "shots_on_target_per_90": get_element_or_none(
                row_shooting_table, './td[@data-stat="shots_on_target_per90"]'
            ),
            "goals_per_shot": get_element_or_none(
                row_shooting_table, './td[@data-stat="goals_per_shot"]'
            ),
            "goals_per_shot_on_target": get_element_or_none(
                row_shooting_table, './td[@data-stat="goals_per_shot_on_target"]'
            ),
            "average_shot_distance": get_element_or_none(
                row_shooting_table, './td[@data-stat="average_shot_distance"]'
            ),
            "free_kick_shots": get_element_or_none(
                row_shooting_table, './td[@data-stat="free_kick_shots"]'
            ),
            "penalty_kick_attempts": get_element_or_none(
                row_shooting_table, './td[@data-stat="pens_att"]'
            ),
            "expected_goals_shooting": get_element_or_none(
                row_shooting_table, './td[@data-stat="xg"]'
            ),
            "non_penalty_expected_goals_shooting": get_element_or_none(
                row_shooting_table, './td[@data-stat="npxg"]'
            ),
            "non_penalty_expected_goals_per_shot": get_element_or_none(
                row_shooting_table, './td[@data-stat="npxg_per_shot"]'
            ),
            "goals_minus_expected_goals": get_element_or_none(
                row_shooting_table, './td[@data-stat="goals_minus_xg"]'
            ),
            "non_penalty_goals_minus_expected_goals": get_element_or_none(
                row_shooting_table, './td[@data-stat="non_penalty_goals_minus_xg"]'
            ),
        }

    @staticmethod
    def _get_passing_stats(rows_passing_table, index) -> dict[str, str]:
        if not rows_passing_table or index >= len(rows_passing_table):
            return {
                "passes_completed": None,
                "passes_attempted": None,
                "pass_completion_percentage": None,
                "total_pass_distance": None,
                "progressive_pass_distance": None,
                "short_passes_completed": None,
                "short_passes_attempted": None,
                "short_pass_completion_percentage": None,
                "medium_passes_completed": None,
                "medium_passes_attempted": None,
                "medium_pass_completion_percentage": None,
                "long_passes_completed": None,
                "long_passes_attempted": None,
                "long_pass_completion_percentage": None,
                "assists_passing": None,
                "expected_assists_passing": None,
                "expected_assists_minus_actual_assists": None,
                "key_passes": None,
                "passes_into_final_third": None,
                "passes_into_penalty_area": None,
                "crosses_into_penalty_area": None,
                "progressive_passes_passing": None,
            }

        row_passing_table = rows_passing_table[index]
        return {
            "passes_completed": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completed"]'
            ),
            "passes_attempted": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_attempted"]'
            ),
            "pass_completion_percentage": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completion"]'
            ),
            "total_pass_distance": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_total_distance"]'
            ),
            "progressive_pass_distance": get_element_or_none(
                row_passing_table, './td[@data-stat="progressive_pass_distance"]'
            ),
            "short_passes_completed": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completed_short"]'
            ),
            "short_passes_attempted": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_attempted_short"]'
            ),
            "short_pass_completion_percentage": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completion_short"]'
            ),
            "medium_passes_completed": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completed_medium"]'
            ),
            "medium_passes_attempted": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_attempted_medium"]'
            ),
            "medium_pass_completion_percentage": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completion_medium"]'
            ),
            "long_passes_completed": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completed_long"]'
            ),
            "long_passes_attempted": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_attempted_long"]'
            ),
            "long_pass_completion_percentage": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_completion_long"]'
            ),
            "assists_passing": get_element_or_none(row_passing_table, './td[@data-stat="assists"]'),
            "expected_assists_passing": get_element_or_none(
                row_passing_table, './td[@data-stat="xg_assist"]'
            ),
            "expected_assists_minus_actual_assists": get_element_or_none(
                row_passing_table, './td[@data-stat="xg_assist_minus_actual_assist"]'
            ),
            "key_passes": get_element_or_none(row_passing_table, './td[@data-stat="key_passes"]'),
            "passes_into_final_third": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_into_final_third"]'
            ),
            "passes_into_penalty_area": get_element_or_none(
                row_passing_table, './td[@data-stat="passes_into_penalty_area"]'
            ),
            "crosses_into_penalty_area": get_element_or_none(
                row_passing_table, './td[@data-stat="crosses_into_penalty_area"]'
            ),
            "progressive_passes_passing": get_element_or_none(
                row_passing_table, './td[@data-stat="progressive_passes"]'
            ),
        }

    @staticmethod
    def _get_pass_types_stats(rows_pass_types_table, index) -> dict[str, str]:
        if not rows_pass_types_table or index >= len(rows_pass_types_table):
            return {
                "live_passes": None,
                "dead_passes": None,
                "free_kick_passes": None,
                "through_ball_passes": None,
                "switches": None,
                "crosses": None,
                "corner_kicks": None,
                "corner_kicks_in": None,
                "corner_kicks_out": None,
                "corner_kicks_straight": None,
                "completed_passes": None,
                "offside_passes": None,
                "blocked_passes": None,
            }

        row_pass_types_table = rows_pass_types_table[index]

        return {
            "live_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_live"]'
            ),
            "dead_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_dead"]'
            ),
            "free_kick_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_free_kicks"]'
            ),
            "through_ball_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="through_balls"]'
            ),
            "switches": get_element_or_none(row_pass_types_table, './td[@data-stat="switches"]'),
            "crosses": get_element_or_none(row_pass_types_table, './td[@data-stat="crosses"]'),
            "corner_kicks": get_element_or_none(
                row_pass_types_table, './td[@data-stat="corner_kicks"]'
            ),
            "corner_kicks_in": get_element_or_none(
                row_pass_types_table, './td[@data-stat="corner_kicks_in"]'
            ),
            "corner_kicks_out": get_element_or_none(
                row_pass_types_table, './td[@data-stat="corner_kicks_out"]'
            ),
            "corner_kicks_straight": get_element_or_none(
                row_pass_types_table, './td[@data-stat="corner_kicks_straight"]'
            ),
            "completed_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_completed"]'
            ),
            "offside_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_offside"]'
            ),
            "blocked_passes": get_element_or_none(
                row_pass_types_table, './td[@data-stat="passes_blocked"]'
            ),
        }

    @staticmethod
    def _get_goal_shot_creation_stats(rows_goal_shot_creation_table, index) -> dict[str, str]:
        if not rows_goal_shot_creation_table or index >= len(rows_goal_shot_creation_table):
            return {
                "sca": None,
                "sca_per_90": None,
                "sca_pass_live": None,
                "sca_pass_dead": None,
                "sca_shots": None,
                "sca_fouled": None,
                "sca_defense": None,
                "gca": None,
                "gca_per_90": None,
                "gca_pass_live": None,
                "gca_pass_dead": None,
                "gca_shots": None,
                "gca_fouled": None,
                "gca_defense": None,
            }

        row_goal_shot_creation_table = rows_goal_shot_creation_table[index]

        return {
            "sca": get_element_or_none(row_goal_shot_creation_table, './td[@data-stat="sca"]'),
            "sca_per_90": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca90"]'
            ),
            "sca_pass_live": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca_passes_live"]'
            ),
            "sca_pass_dead": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca_passes_dead"]'
            ),
            "sca_shots": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca_shots"]'
            ),
            "sca_fouled": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca_fouled"]'
            ),
            "sca_defense": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="sca_defense"]'
            ),
            "gca": get_element_or_none(row_goal_shot_creation_table, './td[@data-stat="gca"]'),
            "gca_per_90": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca90"]'
            ),
            "gca_pass_live": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca_passes_live"]'
            ),
            "gca_pass_dead": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca_passes_dead"]'
            ),
            "gca_shots": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca_shots"]'
            ),
            "gca_fouled": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca_fouled"]'
            ),
            "gca_defense": get_element_or_none(
                row_goal_shot_creation_table, './td[@data-stat="gca_defense"]'
            ),
        }

    @staticmethod
    def _get_defensive_actions_stats(rows_defensive_actions_table, index) -> dict[str, str]:
        if not rows_defensive_actions_table or index >= len(rows_defensive_actions_table):
            return {
                "tackles": None,
                "tackles_won": None,
                "defensive_third_tackles": None,
                "midfield_third_tackles": None,
                "attacking_third_tackles": None,
                "challenges": None,
                "challenges_won": None,
                "challenge_win_percentage": None,
                "blocks": None,
                "blocked_shots": None,
                "blocked_passes": None,
                "interceptions": None,
                "tackles_plus_interceptions": None,
                "clearances": None,
                "errors": None,
            }

        row_defensive_actions_table = rows_defensive_actions_table[index]
        return {
            "tackles": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles"]'
            ),
            "tackles_won": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles_won"]'
            ),
            "defensive_third_tackles": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles_def_3rd"]'
            ),
            "midfield_third_tackles": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles_mid_3rd"]'
            ),
            "attacking_third_tackles": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles_att_3rd"]'
            ),
            "challenges": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="challenges"]'
            ),
            "challenges_won": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="challenges_won"]'
            ),
            "challenge_win_percentage": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="challenges_won_pct"]'
            ),
            "blocks": get_element_or_none(row_defensive_actions_table, './td[@data-stat="blocks"]'),
            "blocked_shots": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="blocked_shots"]'
            ),
            "blocked_passes": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="blocked_passes"]'
            ),
            "interceptions": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="interceptions"]'
            ),
            "tackles_plus_interceptions": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="tackles_interceptions"]'
            ),
            "clearances": get_element_or_none(
                row_defensive_actions_table, './td[@data-stat="clearances"]'
            ),
            "errors": get_element_or_none(row_defensive_actions_table, './td[@data-stat="errors"]'),
        }

    @staticmethod
    def _get_playing_time_stats(rows_playing_time_table, index) -> dict[str, str]:
        if not rows_playing_time_table or index >= len(rows_playing_time_table):
            return {
                "matches_played": None,
                "minutes_played": None,
                "minutes_per_match": None,
                "ninety_minute_matches": None,
                "starts": None,
                "minutes_per_start": None,
                "complete_matches": None,
                "substitute_appearances": None,
                "minutes_per_sub": None,
                "unsubstituted_appearances": None,
                "points_per_match": None,
                "on_goals": None,
                "on_goals_against": None,
                "goal_difference_per_90": None,
                "on_off": None,
                "expected_goals_on": None,
                "expected_goals_against_on": None,
                "expected_goal_difference_per_90_on": None,
                "expected_goal_difference_on_off": None,
            }

        row_playing_time_table = rows_playing_time_table[index]
        return {
            "matches_played": get_element_or_none(
                row_playing_time_table, './td[@data-stat="games"]'
            ),
            "minutes_played": get_element_or_none(
                row_playing_time_table, './td[@data-stat="minutes"]'
            ),
            "minutes_per_match": get_element_or_none(
                row_playing_time_table, './td[@data-stat="minutes_per_game"]'
            ),
            "ninety_minute_matches": get_element_or_none(
                row_playing_time_table, './td[@data-stat="minutes_90s"]'
            ),
            "starts": get_element_or_none(
                row_playing_time_table, './td[@data-stat="games_starts"]'
            ),
            "minutes_per_start": get_element_or_none(
                row_playing_time_table, './td[@data-stat="minutes_per_start"]'
            ),
            "complete_matches": get_element_or_none(
                row_playing_time_table, './td[@data-stat="games_complete"]'
            ),
            "substitute_appearances": get_element_or_none(
                row_playing_time_table, './td[@data-stat="games_subs"]'
            ),
            "minutes_per_sub": get_element_or_none(
                row_playing_time_table, './td[@data-stat="minutes_per_sub"]'
            ),
            "unsubstituted_appearances": get_element_or_none(
                row_playing_time_table, './td[@data-stat="games_subs_unused"]'
            ),
            "points_per_match": get_element_or_none(
                row_playing_time_table, './td[@data-stat="points_per_match"]'
            ),
            "on_goals": get_element_or_none(
                row_playing_time_table, './td[@data-stat="on_goals_for"]'
            ),
            "on_goals_against": get_element_or_none(
                row_playing_time_table, './td[@data-stat="on_goals_against"]'
            ),
            "goal_difference_per_90": get_element_or_none(
                row_playing_time_table, './td[@data-stat="plus_minus_per90"]'
            ),
            "on_off": get_element_or_none(row_playing_time_table, './td[@data-stat="on_off"]'),
            "expected_goals_on": get_element_or_none(
                row_playing_time_table, './td[@data-stat="xg_on"]'
            ),
            "expected_goals_against_on": get_element_or_none(
                row_playing_time_table, './td[@data-stat="xga_on"]'
            ),
            "expected_goal_difference_per_90_on": get_element_or_none(
                row_playing_time_table, './td[@data-stat="xg_plus_minus_per90"]'
            ),
            "expected_goal_difference_on_off": get_element_or_none(
                row_playing_time_table, './td[@data-stat="xg_on_off"]'
            ),
        }

    @staticmethod
    def _get_miscellaneous_stats(rows_miscellaneous_stats_table, index) -> dict[str, str]:
        if not rows_miscellaneous_stats_table or index >= len(rows_miscellaneous_stats_table):
            return {
                "cards_yellow": None,
                "cards_red": None,
                "fouls": None,
                "fouls_drawn": None,
                "offsides": None,
                "crosses": None,
                "interceptions": None,
                "tackles_won": None,
                "pens_won": None,
                "pens_conceded": None,
                "own_goals": None,
                "ball_recoveries": None,
                "aerials_won": None,
                "aerials_lost": None,
                "aerials_won_percentage": None,
                "minutes_per_goal": None,
                "minutes_per_goal_or_assist": None,
            }

        row_miscellaneous_stats_table = rows_miscellaneous_stats_table[index]

        return {
            "cards_yellow": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="cards_yellow"]'
            ),
            "cards_red": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="cards_red"]'
            ),
            "fouls": get_element_or_none(row_miscellaneous_stats_table, './td[@data-stat="fouls"]'),
            "fouls_drawn": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="fouls_drawn"]'
            ),
            "offsides": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="offsides"]'
            ),
            "crosses": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="crosses"]'
            ),
            "interceptions": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="interceptions"]'
            ),
            "tackles_won": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="tackles_won"]'
            ),
            "pens_won": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="pens_won"]'
            ),
            "pens_conceded": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="pens_conceded"]'
            ),
            "own_goals": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="own_goals"]'
            ),
            "ball_recoveries": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="ball_recoveries"]'
            ),
            "aerials_won": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="aerials_won"]'
            ),
            "aerials_lost": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="aerials_lost"]'
            ),
            "aerials_won_percentage": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="aerials_won_pct"]'
            ),
            "minutes_per_goal": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="minutes_per_goal"]'
            ),
            "minutes_per_goal_or_assist": get_element_or_none(
                row_miscellaneous_stats_table, './td[@data-stat="minutes_per_goal_or_assist"]'
            ),
        }

    def execute(self, driver: webdriver.Remote) -> pd.DataFrame:
        result = []

        rows_standard_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_standard_12"]/tbody/tr'
        )
        rows_shooting_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_shooting_12"]/tbody/tr'
        )
        rows_passing_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_passing_12"]/tbody/tr'
        )
        rows_pass_types_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_passing_types_12"]/tbody/tr'
        )
        rows_goal_shot_creation_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_gca_12"]/tbody/tr'
        )
        rows_defensive_actions_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_defense_12"]/tbody/tr'
        )
        rows_playing_time_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_playing_time_12"]/tbody/tr'
        )
        rows_miscellaneous_stats_table = driver.find_elements(
            By.XPATH, '//table[@id="stats_misc_12"]/tbody/tr'
        )

        logging.info(
            "::group::Downloading player stats from team %s and season %s", self.team, self.season
        )

        for index in range(len(rows_standard_table)):
            row_standard_table = rows_standard_table[index]
            player_name = get_element_or_none(row_standard_table, './th[@data-stat="player"]')
            logging.info(f"Downloading player stats for player {player_name}")

            if not player_name or player_name == "Player":
                continue

            player_stats = {
                "season": self.season,
                "team": self.team,
                "player": player_name,
            }
            player_stats.update(self._get_standard_stats(rows_standard_table, index))
            player_stats.update(self._get_shooting_stats(rows_shooting_table, index))
            player_stats.update(self._get_passing_stats(rows_passing_table, index))
            player_stats.update(self._get_pass_types_stats(rows_pass_types_table, index))
            player_stats.update(
                self._get_goal_shot_creation_stats(rows_goal_shot_creation_table, index)
            )
            player_stats.update(
                self._get_defensive_actions_stats(rows_defensive_actions_table, index)
            )
            player_stats.update(self._get_playing_time_stats(rows_playing_time_table, index))
            player_stats.update(
                self._get_miscellaneous_stats(rows_miscellaneous_stats_table, index)
            )
            result.append(player_stats)

        logging.info("::endgroup::")

        return pd.DataFrame(result)
