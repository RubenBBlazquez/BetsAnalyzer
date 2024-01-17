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
    scores = match_scores["scores"].apply(pd.DataFrame).to_list()
    scores = pd.concat(scores).reset_index(drop=True).drop(columns=["id", "type_id"])
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
        ["match_id", "type_id", "participant_id", "player_id", "player_name", "result"]
    ]
    matches_events = matches_events.merge(types[["id", "name"]], left_on="type_id", right_on="id")
    matches_events.drop(columns=["id"], inplace=True)
    matches_events.rename(columns={"name": "type"}, inplace=True)
    matches_events["type"] = matches_events["type"].str.lower().replace(" ", "_")

    return matches_events


def transform_lineups(matches: pd.DataFrame, match_events: pd.DataFrame):
    """
    method to transform lineups as home_players and away_players

    Parameters
    ----------
    matches: pd.DataFrame
        matches data
    match_events: pd.DataFrame
        match events data
    """
    match_lineups = pd.concat(matches["lineups"].apply(pd.DataFrame).to_list())
    match_lineups = match_lineups[["fixture_id", "team_id", "player_id", "player_name"]]
    match_events = match_events[["match_id", "player_id", "type"]]

    # now we reset the index to count the number of events per player, match and type
    match_events = match_events.reset_index().rename(columns={"index": "count"})
    events_count_per_player_match_and_type = (
        match_events.groupby(["match_id", "player_id", "type"])
        .count()
        .reset_index()
        .pivot(index=["match_id", "player_id"], columns="type", values="count")
        .reset_index()
    )
    events_count_per_player_match_and_type = events_count_per_player_match_and_type.merge(
        matches[["match_id", "duration"]], on="match_id"
    )

    # now we get the players that have substitutions to get the duration that they played
    match_players_with_substitutions = events_count_per_player_match_and_type.loc[
        ~events_count_per_player_match_and_type["substitution"].isna(), ["match_id", "player_id"]
    ]
    substitutions = match_events.loc[
        (match_events["match_id"] == match_players_with_substitutions["match_id"])
        & (match_events["player_id"] == match_players_with_substitutions["player_id"]),
        ["match_id", "player_id", "minute"],
    ]

    return substitutions


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

    transform_lineups(clean_data_matches, match_events)

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
