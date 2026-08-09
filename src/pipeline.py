import pandas as pd
from data import all_matches, team_records
from feature_engineering import (extract_team_features, calculate_win_percentage_difference)
from model_training import (create_models, train_models)


def prepare_prediction_pipeline():
    training_dataset = []

    for _, row in all_matches.iterrows():
        home_team = row["HomeTeam"]
        away_team = row["AwayTeam"]
        home_goals = row["FTHG"]
        away_goals = row["FTAG"]
        ftr = row["FTR"]

        home_features = extract_team_features(home_team, team_records)
        away_features = extract_team_features(away_team, team_records)
        win_percentage_difference = (calculate_win_percentage_difference(home_features[0], away_features[0]))
        training_row = (home_features + away_features + [win_percentage_difference] + [ftr])

        training_dataset.append(training_row)

        team_records[home_team]["matches"] += 1
        team_records[away_team]["matches"] += 1

        team_records[home_team]["total_goals"] += home_goals
        team_records[home_team]["total_conceded"] += away_goals

        team_records[away_team]["total_goals"] += away_goals
        team_records[away_team]["total_conceded"] += home_goals

        team_records[home_team]["home_matches"] += 1
        team_records[away_team]["away_matches"] += 1

        team_records[home_team]["home_goals"] += home_goals
        team_records[away_team]["away_goals"] += away_goals

        team_records[home_team]["home_conceded"] += away_goals
        team_records[away_team]["away_conceded"] += home_goals

        if ftr == "H":
            team_records[home_team]["wins"] += 1
            team_records[away_team]["losses"] += 1

            home_result = "W"
            away_result = "L"

            team_records[home_team]["home_wins"] += 1
            team_records[away_team]["away_losses"] += 1

        elif ftr == "D":
            team_records[home_team]["draws"] += 1
            team_records[away_team]["draws"] += 1

            home_result = "D"
            away_result = "D"

            team_records[home_team]["home_draws"] += 1
            team_records[away_team]["away_draws"] += 1

        else:
            team_records[home_team]["losses"] += 1
            team_records[away_team]["wins"] += 1

            home_result = "L"
            away_result = "W"

            team_records[home_team]["home_losses"] += 1
            team_records[away_team]["away_wins"] += 1

        team_records[home_team]["recent_matches"].append(
            {
                "result": home_result,
                "goals": home_goals,
                "conceded": away_goals
            }
        )

        team_records[away_team]["recent_matches"].append(
            {
                "result": away_result,
                "goals": away_goals,
                "conceded": home_goals
            }
        )

        if len(team_records[home_team]["recent_matches"]) > 5:
            team_records[home_team]["recent_matches"].pop(0)

        if len(team_records[away_team]["recent_matches"]) > 5:
            team_records[away_team]["recent_matches"].pop(0)

    columns = [
        "home_win_percentage",
        "home_draw_percentage",
        "home_loss_percentage",
        "home_average_goals_per_match",
        "home_average_conceded_per_match",
        "home_goal_difference",
        "home_home_win_percentage",
        "home_away_win_percentage",
        "home_average_goals",
        "home_average_conceded",
        "home_away_average_goals",
        "home_away_average_conceded",
        "home_recent_win_percentage",
        "home_recent_draw_percentage",
        "home_recent_average_goals",
        "home_recent_average_conceded",

        "away_win_percentage",
        "away_draw_percentage",
        "away_loss_percentage",
        "away_average_goals_per_match",
        "away_average_conceded_per_match",
        "away_goal_difference",
        "away_home_win_percentage",
        "away_away_win_percentage",
        "away_home_average_goals",
        "away_home_average_conceded",
        "away_away_average_goals",
        "away_away_average_conceded",
        "away_recent_win_percentage",
        "away_recent_draw_percentage",
        "away_recent_average_goals",
        "away_recent_average_conceded",
        "win_percentage_difference",
        "ftr"
    ]

    training_dataframe = pd.DataFrame(training_dataset, columns=columns)
    feature_columns = columns[:-1]

    x = training_dataframe[feature_columns]
    y = training_dataframe["ftr"]

    split_index = int(len(all_matches) * 0.8)

    train_x = x.iloc[:split_index]
    train_y = y.iloc[:split_index]

    result_mapping = {
        "H": 0,
        "D": 1,
        "A": 2
    }

    xgboost_train_y = train_y.map(result_mapping)

    (logistic_model, random_forest_model, xgboost_model) = create_models()
    (logistic_model, random_forest_model, xgboost_model) = train_models(logistic_model, random_forest_model, xgboost_model, train_x, train_y, xgboost_train_y)

    return (team_records, logistic_model, random_forest_model, xgboost_model)