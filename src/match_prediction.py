import pandas as pd 
from feature_engineering import (extract_team_features, calculate_win_percentage_difference)
from model_evaluation import reverse_result_mapping

def convert_prediction(prediction):

    if prediction == "H":
        return "Home Win"

    elif prediction == "D":
        return "Draw"

    else:
        return "Away Win"

    
def predict_match(home_team, away_team,team_records,logistic_model,random_forest_model,xgboost_model):
    if home_team not in team_records:
        return {
            "error": f"{home_team} is not in this league"
        }

    if away_team not in team_records:
        return {
            "error": f"{away_team} is not in this league"
        }

    home_features = extract_team_features(home_team,team_records)
    away_features = extract_team_features(away_team,team_records)

    win_percentage_difference = calculate_win_percentage_difference(home_features[0],away_features[0])

    home_away_features = (home_features + away_features + [win_percentage_difference])

    dataframe_input = pd.DataFrame(
        [home_away_features],
        columns=[
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
    "win_percentage_difference"
    ]) 
    prediction_models = {
        "Logistic Regression": logistic_model,
        "Random Forest": random_forest_model,
        "XGBoost": xgboost_model
    }
    
    prediction_results = {}

    for model_name, model in prediction_models.items():

        prediction = model.predict(dataframe_input)[0]
        probabilities = model.predict_proba(dataframe_input)[0]

        if model_name == "XGBoost":

            prediction = reverse_result_mapping[int(prediction)]

            home_win_probability = probabilities[0]
            draw_probability = probabilities[1]
            away_win_probability = probabilities[2]

        else:
            home_win_probability = probabilities[2]
            draw_probability = probabilities[1]
            away_win_probability = probabilities[0]

        prediction_results[model_name] = {
            "prediction": prediction,
            "prediction_result": convert_prediction(prediction),
            "home_win_probability": float(home_win_probability),
            "draw_probability": float(draw_probability),
            "away_win_probability": float(away_win_probability)
        }

    results = {
        "home_team": home_team,
        "away_team": away_team
    }

    for model_name, information in prediction_results.items():

        results[model_name.lower().replace(" ", "_")] = {
            "prediction": information["prediction_result"],
            "home_win_probability": information["home_win_probability"],
            "draw_probability": information["draw_probability"],
            "away_win_probability": information["away_win_probability"]
        }

    return results