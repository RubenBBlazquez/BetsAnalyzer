import logging
from datetime import datetime

import numpy as np
import pandas as pd


def _transform_matches_lineups(matches: pd.DataFrame, seasons: pd.DataFrame):
    """
    Transforms the matches data to get the lineups of each match and each_season

    Parameters
    ----------
    matches: pd.DataFrame
        The matches data of all seasons of one league
    seasons: pd.DataFrame
        The seasons data of one league
    """
    # now we get lineups from each match to append to the unique players of each team in each season
    lineups = matches["lineups"].apply(pd.DataFrame).to_list()
    lineups = pd.concat(lineups).reset_index(drop=True).drop(columns=["id"])
    lineups = lineups.merge(
        matches[["season_id", "match_id"]], left_on="fixture_id", right_on="match_id"
    )
    lineups.drop(
        columns=[
            "sport_id",
            "fixture_id",
            "position_id",
            "formation_field",
            "type_id",
            "formation_position",
            "player_name",
            "jersey_number",
            "match_id",
        ],
        inplace=True,
    )
    lineups.drop_duplicates(inplace=True)
    lineups["season"] = lineups["season_id"].map(seasons.set_index("season_id")["season"])

    return lineups.drop(columns=["season_id"])


def transform_teams_where_players_have_been_playing(valid_teams: list[str], players: pd.DataFrame):
    """
    Method to transform the teams where the players have been
    playing and the number of seasons in each team that the player has been

    Parameters
    ----------
    valid_teams: list[str]
        list of valid teams that are in the league we are processing
    players: pd.DataFrame
        players data
    """
    players_by_team_and_season = pd.concat(
        players["teams"].apply(pd.DataFrame).to_list()
    ).reset_index(drop=True)
    players_by_team_and_season = players_by_team_and_season.loc[
        players_by_team_and_season["team_id"].isin(valid_teams),
        ["player_id", "team_id", "start", "end", "transfer_id"],
    ]

    players_by_team_and_season[["start", "end"]] = players_by_team_and_season[
        ["start", "end"]
    ].fillna(datetime.now().strftime("%Y-%m-%d"))
    players_by_team_and_season["start"] = pd.to_datetime(players_by_team_and_season["start"])
    players_by_team_and_season["start_year"] = players_by_team_and_season["start"].dt.year
    players_by_team_and_season["start_month"] = players_by_team_and_season["start"].dt.month

    players_by_team_and_season["end"] = pd.to_datetime(players_by_team_and_season["end"])
    players_by_team_and_season["end_year"] = players_by_team_and_season["end"].dt.year
    players_by_team_and_season["end_month"] = players_by_team_and_season["end"].dt.month

    players_by_team_and_season["start_season"] = (
        players_by_team_and_season["start_year"].astype(str)
        + "/"
        + (players_by_team_and_season["start_year"] + 1).astype(str)
    )
    players_by_team_and_season["end_season"] = (
        players_by_team_and_season["end_year"].astype(str)
        + "/"
        + (players_by_team_and_season["end_year"] + 1).astype(str)
    )

    for row in players_by_team_and_season.itertuples():
        seasons_range = [row.start_season]

        if row.start_season != row.end_season:
            date_range = pd.date_range(row.start, row.end, freq="YS").strftime("%Y")
            seasons_range = (
                date_range.astype(str) + "/" + (date_range.astype(int) + 1).astype(str)
            ).to_list()

        players_by_team_and_season.loc[
            players_by_team_and_season.index == row.Index, "seasons_in_team"
        ] = pd.Series(index=[row.Index], data=[",".join(seasons_range)])

    players_by_team_and_season = players_by_team_and_season[
        ["player_id", "team_id", "transfer_id", "seasons_in_team"]
    ].drop_duplicates()
    season_columns = (
        players_by_team_and_season["seasons_in_team"]
        .str.split(",", expand=True)
        .add_prefix("season_")
    )
    players_by_team_and_season = pd.concat(
        [players_by_team_and_season, season_columns], axis=1
    ).drop(columns="seasons_in_team")

    return (
        players_by_team_and_season.melt(id_vars=["player_id", "team_id", "transfer_id"])
        .dropna()
        .drop(columns="variable")
        .reset_index(drop=True)
        .rename(columns={"value": "season"})
    )


def transform_player_transfers(
    players: pd.DataFrame, valid_teams: list[str], seasons: pd.DataFrame, current_season: str
):
    """
    Method to transform the players transfers data

    Parameters
    ----------
    players: pd.DataFrame
        players data
    valid_teams: list[str]
        list of valid teams that are in the league we are processing
    seasons: pd.DataFrame
        seasons data
    current_season: str
        current season of the league we are processing
    """
    valid_player_transfers = pd.concat(players["transfers"].apply(pd.DataFrame).to_list())
    valid_player_transfers.rename(columns={"id": "transfer_id"}, inplace=True)
    valid_player_transfers.reset_index(drop=True, inplace=True)
    valid_player_transfers = valid_player_transfers[
        (valid_player_transfers["date"] != "None")
        & (valid_player_transfers["completed"])
        & (valid_player_transfers["to_team_id"].isin(valid_teams))
    ]
    valid_player_transfers["date"] = pd.to_datetime(valid_player_transfers["date"])
    valid_player_transfers["year"] = valid_player_transfers["date"].dt.year
    valid_player_transfers["month"] = valid_player_transfers["date"].dt.month

    player_transfers = pd.DataFrame(columns=["player_id", "team_id", "transfer_id", "season"])

    for season in seasons.itertuples():
        logging.info(f"Processing transfers from season {season.season}")

        season_year_start = pd.to_datetime(season.starting_at).year
        season_year_end = pd.to_datetime(season.ending_at).year
        season_month_end = pd.to_datetime(season.ending_at).month

        transfers = valid_player_transfers[
            valid_player_transfers["year"].between(season_year_start, season_year_end)
        ]
        transfers["season_where_will_play"] = np.where(
            transfers["month"] >= season_month_end,
            transfers["year"].astype(str) + "/" + (transfers["year"] + 1).astype(str),
            f"{season_year_start}/{season_year_end}",
        )

        # we filter the players that will play in the current season
        # because that players are already given by the teams endpoint
        transfers = transfers[transfers["season_where_will_play"] != current_season]
        transfers = (
            transfers[["transfer_id", "player_id", "to_team_id", "season_where_will_play"]]
            .drop_duplicates()
            .reset_index(drop=True)
            .rename(columns={"to_team_id": "team_id", "season_where_will_play": "season"})
        )
        player_transfers = pd.concat([player_transfers, transfers])

    return player_transfers.reset_index(drop=True)


def transform_players_data(
    final_data: pd.DataFrame,
    players: pd.DataFrame,
    teams: pd.DataFrame,
    seasons: pd.DataFrame,
    matches: pd.DataFrame,
):
    current_season = seasons[seasons["is_current"]].season[0]
    seasons = seasons[~seasons["is_current"]]

    players.loc[players["date_of_birth"] == "None", "date_of_birth"] = datetime.now()
    players["age"] = (datetime.now() - pd.to_datetime(players["date_of_birth"])).dt.days // 365
    valid_teams = teams["team_id"].unique()

    current_season_players = pd.concat(teams["players"].apply(pd.DataFrame).to_list()).reset_index(
        drop=True
    )
    current_season_players = current_season_players[["player_id", "team_id", "transfer_id"]]
    current_season_players["season"] = current_season

    matches_lineups = _transform_matches_lineups(matches, seasons)
    player_teams = transform_teams_where_players_have_been_playing(valid_teams, players)
    player_transfers = transform_player_transfers(players, valid_teams, seasons, current_season)

    players_by_team_and_season = (
        pd.concat(
            [current_season_players, player_teams, player_transfers, matches_lineups],
        )
        .reset_index(drop=True)
        .drop(columns=["transfer_id"])
        .drop_duplicates()
    )
    players_by_team_and_season = players_by_team_and_season.merge(
        players[["id", "name", "height", "weight", "age"]], left_on="player_id", right_on="id"
    )
    players_by_team_and_season.drop(columns=["id"], inplace=True)
    players_by_team_and_season = (
        players_by_team_and_season.groupby(by=["team_id", "season"])
        .apply(lambda row_: row_.to_dict("records"))
        .reset_index()
        .rename(columns={0: "players"})
    )

    final_data = final_data.merge(players_by_team_and_season, on=["team_id", "season"], how="left")
    final_data["players"] = final_data["players"].apply(
        lambda x: [] if not isinstance(x, list) and pd.isna(x) else x
    )

    return final_data
