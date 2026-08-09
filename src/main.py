import pandas as pd 
from data import all_matches, team_records
from feature_engineering import (
    extract_team_features,
    calculate_win_percentage_difference
)
from model_training import (
    create_models,
    train_models
)
from model_evaluation import (
    convert_xgboost_predictions,
    evaluate_predictions,
    print_evaluation
)

from team_compare import compare_teams
from match_prediction import predict_match

training_dataset = []                                   

for _, row in all_matches.iterrows():  

    home_team = row["HomeTeam"]               
    away_team = row["AwayTeam"]                  
    home_goals = row["FTHG"]                      
    away_goals = row["FTAG"]                       
    ftr = row["FTR"]                                
   
    home_features = extract_team_features(home_team,team_records)       
    away_features = extract_team_features(away_team,team_records)   
    win_percentage_difference = calculate_win_percentage_difference(home_features[0], away_features[0])

    home_away_ftr_features = home_features + away_features + [win_percentage_difference] + [ftr]
    training_dataset.append(home_away_ftr_features)         
 
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

    elif ftr == "D":
        team_records[home_team]["draws"] += 1      
        team_records[away_team]["draws"] += 1

    elif ftr == "A":
        team_records[home_team]["losses"] += 1
        team_records[away_team]["wins"] += 1

    if ftr == "H":
        home_result = "W"
        team_records[home_team]["home_wins"] += 1
        team_records[away_team]["away_losses"] += 1
    elif ftr == "D":
        home_result = "D"
        team_records[home_team]["home_draws"] += 1
        team_records[away_team]["away_draws"] += 1
    else:
        home_result = "L"
        team_records[home_team]["home_losses"] += 1
        team_records[away_team]["away_wins"] += 1

    if ftr == "H":
        away_result = "L"
    elif ftr == "D":
        away_result = "D"
    else:
        away_result = "W"

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


training_dataframe = pd.DataFrame(training_dataset, columns=["home_win_percentage","home_draw_percentage","home_loss_percentage",
                                                             "home_average_goals_per_match","home_average_conceded_per_match",
                                                             "home_goal_difference","home_home_win_percentage",
                                                             "home_away_win_percentage","home_average_goals",
                                                             "home_average_conceded",
                                                             "home_away_average_goals",
                                                             "home_away_average_conceded","home_recent_win_percentage","home_recent_draw_percentage",
                                                             "home_recent_average_goals","home_recent_average_conceded","away_win_percentage","away_draw_percentage",
                                                             "away_loss_percentage","away_average_goals_per_match","away_average_conceded_per_match",
                                                             "away_goal_difference","away_home_win_percentage",
                                                             "away_away_win_percentage","away_home_average_goals",
                                                             "away_home_average_conceded",
                                                             "away_away_average_goals",
                                                             "away_away_average_conceded",
                                                             "away_recent_win_percentage","away_recent_draw_percentage", "away_recent_average_goals",
                                                              "away_recent_average_conceded","win_percentage_difference","ftr"])

feature_columns = [
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
]

x = training_dataframe[feature_columns]
y = training_dataframe["ftr"]

split_index = int(len(all_matches) * 0.8)

train_x = x.iloc[:split_index]
test_x = x.iloc[split_index:]

train_y = y.iloc[:split_index]
test_y = y.iloc[split_index:]

test_matches = all_matches.iloc[split_index:]

result_mapping = {
    "H": 0,
    "D": 1,
    "A": 2
}

xgboost_train_y = train_y.map(result_mapping)

logistic_model, random_forest_model, xgboost_model = create_models()

logistic_model, random_forest_model, xgboost_model = train_models(
    logistic_model,
    random_forest_model,
    xgboost_model,
    train_x,
    train_y,
    xgboost_train_y
)

logistic_predictions = logistic_model.predict(test_x)
random_forest_predictions = random_forest_model.predict(test_x)
xgboost_predictions_number = xgboost_model.predict(test_x)
xgboost_predictions = convert_xgboost_predictions(xgboost_predictions_number)

prediction_results = {
    "Logistic Regression": logistic_predictions,
    "Random Forest": random_forest_predictions,
    "XGBoost": xgboost_predictions
}

for model_name, model_predictions in prediction_results.items():
    accuracy, matrix, classification = evaluate_predictions(
        model_predictions,
        test_y,
        test_matches
    )

    print_evaluation(
        model_name,
        accuracy,
        matrix,
        classification
    )
team1 = input("Enter team 1: ").strip()
team2 = input("Enter team 2: ").strip()

# 두 팀의 통계 비교
compare_teams(team1, team2)

# 머신러닝 경기 결과 예측
match_results = predict_match(
    team1,
    team2,
    team_records,
    logistic_model,
    random_forest_model,
    xgboost_model
)
print("\n==============================")
print("Match Prediction")
print("==============================")

if "error" in match_results:
    print(match_results["error"])
else:
    print(match_results)