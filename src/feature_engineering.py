def extract_recent_form_features(team_name,team_records):
    recent_matches = team_records[team_name]["recent_matches"]

    if len(recent_matches) == 0:
        return [0, 0, 0, 0]

    recent_wins = 0
    recent_goals = 0
    recent_conceded = 0
    recent_draws = 0    

    
    for match in recent_matches:
        if match["result"] == "W":
            recent_wins += 1

        elif match["result"] == "D":
            recent_draws += 1

       
        recent_goals += match["goals"]
        recent_conceded += match["conceded"]

    recent_match_count = len(recent_matches)
    recent_win_percentage = recent_wins / recent_match_count
    recent_draw_percentage = recent_draws / recent_match_count
    recent_average_goals = recent_goals / recent_match_count
    recent_average_conceded = recent_conceded / recent_match_count
    
    return [
        recent_win_percentage,
        recent_draw_percentage,
        recent_average_goals,
        recent_average_conceded,
    ]

def extract_team_features(team_name,team_records):
    record = team_records[team_name] 
    matches = record["matches"] 
    wins = record["wins"]       
    draws = record["draws"] 
    losses = record["losses"]    
    total_goals = record["total_goals"]   
    total_conceded = record["total_conceded"]
    home_matches = record["home_matches"]
    home_wins = record["home_wins"]
    away_matches = record["away_matches"]
    away_wins = record["away_wins"]
    home_goals = record["home_goals"]
    home_conceded = record["home_conceded"]
    away_goals = record["away_goals"]
    away_conceded = record["away_conceded"]

    if matches == 0:                              
        win_percentage = 0
        draw_percentage = 0
        loss_percentage = 0
        average_goals_per_match = 0
        average_conceded_per_match = 0
    else:                                         
        win_percentage = wins / matches
        draw_percentage = draws / matches
        loss_percentage = losses / matches
        average_goals_per_match = total_goals / matches
        average_conceded_per_match = total_conceded / matches

    if home_matches == 0:
        home_win_percentage = 0
        home_average_goals = 0
        home_average_conceded = 0

    else:
        home_win_percentage = home_wins / home_matches
        home_average_goals = home_goals / home_matches
        home_average_conceded = home_conceded / home_matches

    if away_matches == 0:
        away_win_percentage = 0
        away_average_goals = 0
        away_average_conceded = 0
    else:
        away_win_percentage = away_wins / away_matches
        away_average_goals = away_goals / away_matches
        away_average_conceded = away_conceded / away_matches

    goal_difference = total_goals - total_conceded              
    recent_form_features = extract_recent_form_features(team_name,team_records)
    return [win_percentage, draw_percentage, loss_percentage, average_goals_per_match, average_conceded_per_match, goal_difference,home_win_percentage,
    away_win_percentage, home_average_goals, home_average_conceded, away_average_goals, away_average_conceded] + recent_form_features


def calculate_win_percentage_difference(home_win_percentage, away_win_percentage):
    return home_win_percentage - away_win_percentage