from itertools import chain

import pandas as pd


def transform_match_scores(matches: pd.DataFrame, teams: pd.DataFrame):
    """
    Method to transform match scores

    Parameters
    ----------
    matches: pd.DataFrame
        matches data
    teams: pd.DataFrame
        teams data
    """
    match_scores = matches[["match_id", "scores"]]
    scores = pd.DataFrame(chain.from_iterable(match_scores["scores"].to_list()))
    scores = scores.drop(columns=["id", "type_id"])
    match_scores = match_scores.merge(scores, left_on="match_id", right_on="fixture_id")
    match_scores.drop(columns=["scores", "fixture_id"], inplace=True)
    match_scores[["goals", "participant"]] = match_scores["score"].apply(pd.Series)
    match_scores.drop(columns=["score"], inplace=True)
    match_scores = (
        match_scores.groupby(["match_id", "participant_id", "participant"]).sum().reset_index()
    )

    match_teams = matches[["match_id", "name"]]
    match_teams[["team_1", "team_2"]] = match_teams["name"].str.split(" vs ", expand=True)
    match_teams.drop(columns="name", inplace=True)
    match_teams = match_teams.melt(
        id_vars=["match_id"], value_vars=["team_1", "team_2"], value_name="team_name"
    ).drop(columns="variable")
    match_teams = match_teams.merge(
        teams[["team_id", "name"]], left_on="team_name", right_on="name"
    )
    match_teams.drop(columns="name", inplace=True)

    match_scores = match_scores.merge(
        match_teams, left_on=["participant_id", "match_id"], right_on=["team_id", "match_id"]
    )
    match_scores.drop(columns=["participant_id"], inplace=True)

    home_match_scores = match_scores[match_scores["participant"] == "home"].drop(
        columns=["participant"]
    )
    away_match_scores = match_scores[match_scores["participant"] == "away"].drop(
        columns=["participant"]
    )

    return pd.merge(
        home_match_scores, away_match_scores, on="match_id", suffixes=("_home", "_away")
    )


def transform_match_events(matches: pd.DataFrame, types: pd.DataFrame):
    """
    method to transform match events

    Parameters
    ----------
    matches: pd.DataFrame
        matches data
    types: pd.DataFrame
        types data
    """
    # we set the index as the match id because events are
    # lists of dicts and don't have the match id to reference it later
    matches_events = pd.concat(
        matches.apply(
            lambda row: pd.DataFrame(row["events"], index=[row["match_id"]] * len(row["events"])),
            axis=1,
        ).to_list()
    )
    matches_events = matches_events.reset_index().rename(columns={"index": "match_id"})
    matches_events = matches_events[
        [
            "match_id",
            "type_id",
            "participant_id",
            "player_id",
            "related_player_id",
            "result",
            "minute",
            "injured",
        ]
    ]
    matches_events = matches_events.merge(types[["id", "name"]], left_on="type_id", right_on="id")
    matches_events.drop(columns=["id"], inplace=True)
    matches_events.rename(columns={"name": "type", "participant_id": "team_id"}, inplace=True)
    matches_events["type"] = matches_events["type"].str.lower().replace(" ", "_")

    return matches_events


def transform_lineups(matches: pd.DataFrame, match_events: pd.DataFrame, types: pd.DataFrame):
    """
    method to transform lineups as home_players and away_players

    Parameters
    ----------
    matches: pd.DataFrame
        matches data
    match_events: pd.DataFrame
        match events data
    types: pd.DataFrame
        types data
    """
    match_lineups = pd.DataFrame(chain.from_iterable(matches["lineups"].to_list()))
    match_lineups = match_lineups[["fixture_id", "team_id", "player_id", "player_name", "type_id"]]
    match_lineups = match_lineups.merge(types[["id", "code"]], left_on="type_id", right_on="id")
    match_lineups.drop(columns=["id"], inplace=True)
    match_lineups.rename(columns={"fixture_id": "match_id", "code": "type"}, inplace=True)
    match_lineups["duration"] = match_lineups["match_id"].map(
        matches.set_index("match_id")["duration"]
    )

    match_events = match_events[
        ["match_id", "player_id", "related_player_id", "team_id", "type", "minute", "injured"]
    ]

    # now we reset the index to count the number of events per player, match and type
    match_events = match_events.reset_index().rename(columns={"index": "count"})
    events_count_per_player_match_and_type = (
        match_events.drop(columns=["minute", "injured"])
        .groupby(["match_id", "team_id", "player_id", "type"])
        .count()
        .reset_index()
        .pivot(index=["match_id", "team_id", "player_id"], columns="type", values="count")
        .reset_index()
    )
    statistics_columns = events_count_per_player_match_and_type.columns[3:]

    events_count_per_player_match_and_type = events_count_per_player_match_and_type.merge(
        matches[["match_id", "date", "season_id"]], on=["match_id"]
    )
    events_count_per_player_match_and_type.rename(columns={"date": "match_date"}, inplace=True)

    # now we get the players that have substitutions to set the duration that they played in the match
    substitution_events = match_events.loc[
        match_events["type"] == "substitution",
        ["match_id", "team_id", "player_id", "related_player_id", "minute"],
    ]
    substitution_events["duration"] = substitution_events["match_id"].map(
        matches.set_index("match_id")["duration"]
    )
    substitution_events["related_player_minutes"] = (
        substitution_events["duration"] - substitution_events["minute"]
    )
    substitution_events.drop(columns=["duration"], inplace=True)

    related_substitution_events = substitution_events[
        ["match_id", "team_id", "related_player_id", "related_player_minutes"]
    ]
    related_substitution_events.rename(columns={"related_player_id": "player_id"}, inplace=True)
    player_substitution_events = substitution_events[["match_id", "team_id", "player_id", "minute"]]

    events_count_per_player_match_and_type.sort_values(
        ["player_id", "season_id", "match_date"], inplace=True, ascending=True
    )
    events_count_per_player_match_and_type.reset_index(drop=True, inplace=True)

    # we make the group by player id and season, because I think that the previous match statistics
    # cant be from another season, so I have the previous season statistics
    events_count_per_player_match_and_type[
        statistics_columns
    ] = events_count_per_player_match_and_type.groupby(["player_id", "season_id"])[
        statistics_columns
    ].shift(
        1
    )
    events_count_per_player_match_and_type.rename(
        columns={
            col: f"previous_match_{col.lower().replace(' ', '_')}" for col in statistics_columns
        },
        inplace=True,
    )
    events_count_per_player_match_and_type.fillna(0, inplace=True)
    events_count_per_player_match_and_type.drop(columns=["match_date", "season_id"], inplace=True)

    match_lineups = match_lineups.merge(
        events_count_per_player_match_and_type, on=["match_id", "team_id", "player_id"], how="left"
    ).drop_duplicates()
    match_lineups.fillna(0, inplace=True)

    # we merge de minutes of the substitutions after merge to lineups
    # because could be players that not have events and they can be related in a substitution,
    # so in the events_count_per_player_match_and_type we could not have the player there
    match_lineups = match_lineups.merge(
        player_substitution_events, on=["match_id", "team_id", "player_id"], how="left"
    ).fillna(0)
    match_lineups = match_lineups.merge(
        related_substitution_events, on=["match_id", "team_id", "player_id"], how="left"
    ).fillna(0)
    match_lineups["minutes_played"] = (
        match_lineups["minute"] + match_lineups["related_player_minutes"]
    )
    match_lineups.drop(columns=["minute", "related_player_minutes"], inplace=True)

    # now we will get the players who were not in bench to set the minutes played,
    # if they have played and there's no substitution event of them, we suppose
    # that they have played all the match, so we set the duration of the match as minutes played
    non_bench_players = (match_lineups["type"] != "bench") & (match_lineups["minutes_played"] == 0)
    match_lineups.loc[non_bench_players, "minutes_played"] = match_lineups.loc[
        non_bench_players, "duration"
    ]
    match_lineups.drop(columns=["duration"], inplace=True)

    players_from_home_matches = match_lineups[
        match_lineups["team_id"].isin(matches["team_id_home"].unique())
    ]
    home_matches_lineup = (
        players_from_home_matches.groupby(["match_id", "team_id"])
        .apply(lambda row: row.to_dict("records"))
        .reset_index()
        .rename(columns={0: "team_home_lineup", "team_id": "team_id_home"})
    )

    players_from_away_matches = match_lineups[
        match_lineups["team_id"].isin(matches["team_id_away"].unique())
    ]
    away_matches_lineup = (
        players_from_away_matches.groupby(["match_id", "team_id"])
        .apply(lambda row: row.to_dict("records"))
        .reset_index()
        .rename(columns={0: "team_away_lineup", "team_id": "team_id_away"})
    )

    matches = matches.merge(home_matches_lineup, on=["match_id", "team_id_home"], how="left")
    matches = matches.merge(away_matches_lineup, on=["match_id", "team_id_away"], how="left")
    matches.drop(columns=["lineups"], inplace=True)

    return matches


def transform_matches_data(
    final_data: pd.DataFrame, matches: pd.DataFrame, teams: pd.DataFrame, types: pd.DataFrame
) -> pd.DataFrame:
    """
    Method to clean matches data

    Parameters
    ----------
    final_data: pd.DataFrame
        final transformed data
    matches: pd.DataFrame
        matches data
    teams: pd.DataFrame
        teams data
    types: pd.DataFrame
        types data

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        tuple of clean data for home and away matches
    """
    match_scores = transform_match_scores(matches, teams)
    match_events = transform_match_events(matches, types)

    clean_data_matches = matches[
        [
            "match_id",
            "season_id",
            "league_id",
            "starting_at",
            "starting_at_timestamp",
            "length",
            "weatherreport",
            "lineups",
        ]
    ]
    clean_data_matches.rename(
        columns={
            "starting_at": "date",
            "starting_at_timestamp": "date_timestamp",
            "length": "duration",
        },
        inplace=True,
    )
    clean_data_matches = clean_data_matches.merge(match_scores, on="match_id")
    clean_data_matches = transform_lineups(clean_data_matches, match_events, types)

    clean_data_home_matches = (
        clean_data_matches.groupby(["season_id", "league_id", "team_id_home"])
        .apply(
            lambda row: pd.DataFrame(row)
            .drop(columns=["season_id", "league_id"])
            .to_dict("records")
        )
        .reset_index()
        .rename(columns={0: "home_matches", "team_id_home": "team_id"})
    )
    clean_data_away_matches = (
        clean_data_matches.groupby(["season_id", "league_id", "team_id_away"])
        .apply(
            lambda row: pd.DataFrame(row)
            .drop(columns=["season_id", "league_id"])
            .to_dict("records")
        )
        .reset_index()
        .rename(columns={0: "away_matches", "team_id_away": "team_id"})
    )

    final_data = final_data.merge(
        clean_data_home_matches, on=["season_id", "league_id", "team_id"], how="outer"
    )
    final_data.loc[:, "home_matches"] = final_data.loc[:, "home_matches"].apply(
        lambda x: [] if not isinstance(x, list) and pd.isna(x) else x
    )

    final_data = final_data.merge(
        clean_data_away_matches, on=["season_id", "league_id", "team_id"], how="outer"
    )
    final_data.loc[:, "away_matches"] = final_data.loc[:, "away_matches"].apply(
        lambda x: [] if not isinstance(x, list) and pd.isna(x) else x
    )

    return final_data
