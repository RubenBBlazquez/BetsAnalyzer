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


def get_home_matches():
    pass


def transform_matches_data(
    final_data: pd.DataFrame,
    matches: pd.DataFrame,
    teams: pd.DataFrame,
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

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        tuple of clean data for home and away matches
    """
    match_scores = transform_match_scores(matches, teams)

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
