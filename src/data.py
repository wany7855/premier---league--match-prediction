import pandas as pd 
csv_file_path = "data/E0.csv"
df = pd.read_csv(csv_file_path)

all_matches = df[["HomeTeam", "AwayTeam", "FTR", "FTHG", "FTAG"]]

teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

team_records = {}

for team in teams:
    team_records[team] = {
        "matches": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "total_goals": 0,
        "total_conceded": 0,
        "recent_matches": [],
        "home_matches": 0,
        "home_wins": 0,
        "home_draws": 0,
        "home_losses": 0,
        "home_goals": 0,
        "home_conceded": 0,
        "away_matches": 0,
        "away_wins": 0,
        "away_draws": 0,
        "away_losses": 0,
        "away_goals": 0,
        "away_conceded": 0
    }