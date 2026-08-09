from team_metrics import team_stats
from data import df
import pandas as pd 

teams_in_league = pd.concat((df["HomeTeam"],df["AwayTeam"])).unique()

def league_table():
    team_result = []
    for team in teams_in_league:
        team_name = team
        stats = team_stats(team_name)
        total_matches = stats["total_matches"]
        total_wins = stats["total_wins"]
        total_draws = stats["total_draws"]
        total_losses = stats["total_losses"]
        total_goals = stats["total_goals"]
        home_goals = stats["home_goals"]
        away_goals = stats["away_goals"]
        total_conceded =stats["total_conceded"]
        home_conceded = stats["home_conceded"]
        away_conceded = stats["away_conceded"]
        goal_difference = stats["goal_difference"]
        points = (total_wins * 3) + total_draws
        team_result.append([team_name,total_matches,total_wins,total_draws,total_losses,total_goals,home_goals,away_goals,total_conceded,home_conceded,away_conceded,goal_difference,points])

    league_table_df = pd.DataFrame(
        team_result,
        columns=[
            "team_name",
            "total_matches",
            "total_wins",
            "total_draws",
            "total_losses",
            "total_goals",
            "home_goals",
            "away_goals",
            "total_conceded",
            "home_conceded",
            "away_conceded",
            "goal_difference",
            "points"
        ]
    )
    # Sort teams by points, goal difference, and goals scored.
    # Then reset the index after sorting.
    
    sorted_league_table = league_table_df.sort_values(
        by=["points", "goal_difference", "total_goals"],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    return sorted_league_table

if __name__ == "__main__":
    print(league_table())

