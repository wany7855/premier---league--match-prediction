from data import df

def team_wins(team_name):
    team_winning_matches = df[
        ((df["HomeTeam"] == team_name) & (df["FTR"] == "H")) 
        | ((df["AwayTeam"] == team_name) & (df["FTR"] == "A"))
    ]
    return len(team_winning_matches)


def team_draws(team_name):
    team_drawing_matches = df[
        ((df["HomeTeam"] == team_name) & (df["FTR"] == "D")) 
        | ((df["AwayTeam"] == team_name) & (df["FTR"] == "D"))
    ] 
    return len(team_drawing_matches)


def team_losses(team_name):
    team_losing_matches = df[
        ((df["HomeTeam"] == team_name) & (df["FTR"] == "A")) 
         | ((df["AwayTeam"] == team_name) & (df["FTR"] == "H"))
    ]
    return len(team_losing_matches)


def team_home_goals(team_name):
    home_goals = df[df["HomeTeam"] == team_name]["FTHG"].sum()
    return home_goals


def team_away_goals(team_name):
    away_goals = df[df["AwayTeam"] == team_name]["FTAG"].sum()
    return away_goals


def team_home_conceded(team_name):
    home_conceded = df[df["HomeTeam"] == team_name]["FTAG"].sum()
    return home_conceded


def team_away_conceded(team_name):
    return df[df["AwayTeam"] == team_name]["FTHG"].sum()

    
def team_total_goals(team_name):
    return team_home_goals(team_name) + team_away_goals(team_name)

   
def team_total_conceded(team_name):
    return team_home_conceded(team_name) + team_away_conceded(team_name)

    
def team_goal_difference(team_name):
    return team_total_goals(team_name) - team_total_conceded(team_name)

   
def team_total_matches(team_name):
    return len(df[((df["HomeTeam"] == team_name) | (df["AwayTeam"] == team_name))])

    
def team_average_goals_per_match(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return 0
    return team_total_goals(team_name) / total_matches

   
def team_average_conceded_per_match(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return 0
    return team_total_conceded(team_name) / total_matches

    
def team_winning_percentage(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return 0
    return team_wins(team_name) / total_matches * 100

    
def team_drawing_percentage(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return 0
    return team_draws(team_name) / total_matches * 100


def team_losing_percentage(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return 0
    return team_losses(team_name) / total_matches * 100

   
def team_stats(team_name):
    total_matches = team_total_matches(team_name)
    if total_matches == 0:
        return None
    total_wins = team_wins(team_name)
    total_draws = team_draws(team_name)
    total_losses = team_losses(team_name)
    home_goals = team_home_goals(team_name)
    away_goals = team_away_goals(team_name)
    total_goals = team_total_goals(team_name)
    home_conceded = team_home_conceded(team_name)
    away_conceded = team_away_conceded(team_name)
    total_conceded = team_total_conceded(team_name)
    goal_difference = team_goal_difference(team_name)
    average_goals_per_match = team_average_goals_per_match(team_name)
    average_conceded_per_match = team_average_conceded_per_match(team_name)
    win_percentage = team_winning_percentage(team_name)
    draw_percentage = team_drawing_percentage(team_name)
    loss_percentage = team_losing_percentage(team_name)
    return {
        "team": team_name,
        "total_matches": total_matches,
        "total_wins": total_wins,
        "total_draws": total_draws,
        "total_losses": total_losses,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "total_goals": total_goals,
        "home_conceded": home_conceded,
        "away_conceded": away_conceded,
        "total_conceded": total_conceded,
        "goal_difference": goal_difference,
        "average_goals_per_match": average_goals_per_match,
        "average_conceded_per_match": average_conceded_per_match,
        "win_percentage": win_percentage,
        "draw_percentage": draw_percentage,
        "loss_percentage": loss_percentage
    }


def display_team_stats(team_name):
    stats = team_stats(team_name)

    if stats is None:
        print(f"Team '{team_name}' was not found in the dataset.")
        return

    print("=" * 35)
    print(f"{stats['team']} Statistics")
    print("=" * 35)
    print(f"Matches: {stats['total_matches']}")
    print(f"Wins: {stats['total_wins']}")
    print(f"Draws: {stats['total_draws']}")
    print(f"Losses: {stats['total_losses']}")
    print(f"Goals scored: {stats['total_goals']}")
    print(f"Goals conceded: {stats['total_conceded']}")
    print(f"Goal difference: {stats['goal_difference']}")
    print(f"Average goals: {stats['average_goals_per_match']:.2f}")
    print(f"Average conceded: {stats['average_conceded_per_match']:.2f}")
    print(f"Win percentage: {stats['win_percentage']:.2f}%")
    print(f"Draw percentage: {stats['draw_percentage']:.2f}%")
    print(f"Loss percentage: {stats['loss_percentage']:.2f}%")

if __name__ == "__main__":
    team_name = input("Enter the team name: ").strip()
    display_team_stats(team_name)
    