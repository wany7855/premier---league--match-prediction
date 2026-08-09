from team_metrics import team_stats


def compare_teams(team1, team2):

    team1_stats = team_stats(team1)
    team2_stats = team_stats(team2)

    if team1_stats is None:
        print(f"There is no {team1} in the Premier League")
        return

    if team2_stats is None:
        print(f"There is no {team2} in the Premier League")
        return

    print("=" * 30)
    print(f"{team1} vs {team2} Statistics")
    print("=" * 30)

    print(f"{team1} wins: {team1_stats['total_wins']}                         | {team2} wins: {team2_stats['total_wins']}")
    print(f"{team1} draws: {team1_stats['total_draws']}                         | {team2} draws: {team2_stats['total_draws']}")
    print(f"{team1} losses: {team1_stats['total_losses']}                       | {team2} losses: {team2_stats['total_losses']}")
    print(f"{team1} home goals: {team1_stats['home_goals']}                   | {team2} home goals: {team2_stats['home_goals']}")
    print(f"{team1} away goals: {team1_stats['away_goals']}                   | {team2} away goals: {team2_stats['away_goals']}")
    print(f"{team1} home conceded: {team1_stats['home_conceded']}                | {team2} home conceded: {team2_stats['home_conceded']}")
    print(f"{team1} away conceded: {team1_stats['away_conceded']}                | {team2} away conceded: {team2_stats['away_conceded']}")
    print(f"{team1} total goals: {team1_stats['total_goals']}                  | {team2} total goals: {team2_stats['total_goals']}")
    print(f"{team1} total conceded: {team1_stats['total_conceded']}               | {team2} total conceded: {team2_stats['total_conceded']}")
    print(f"{team1} goal difference: {team1_stats['goal_difference']}              | {team2} goal difference: {team2_stats['goal_difference']}")
    print(f"{team1} total matches: {team1_stats['total_matches']}                | {team2} total matches: {team2_stats['total_matches']}")
    print(f"{team1} average goals per match: {team1_stats['average_goals_per_match']:.2f}    | {team2} average goals per match: {team2_stats['average_goals_per_match']:.2f}")
    print(f"{team1} average conceded per match: {team1_stats['average_conceded_per_match']:.2f} | {team2} average conceded per match: {team2_stats['average_conceded_per_match']:.2f}")
    print(f"{team1} winning percentage: {team1_stats['win_percentage']:.2f}%       | {team2} winning percentage: {team2_stats['win_percentage']:.2f}%")
    print(f"{team1} drawing percentage: {team1_stats['draw_percentage']:.2f}%       | {team2} drawing percentage: {team2_stats['draw_percentage']:.2f}%")
    print(f"{team1} losing percentage: {team1_stats['loss_percentage']:.2f}%        | {team2} losing percentage: {team2_stats['loss_percentage']:.2f}%")


