from scipy.stats import poisson
import joblib
import pandas as pd

df = pd.read_csv("data/international_matches.csv")

home_model = joblib.load("model/home_model.joblib")
away_model = joblib.load("model/away_model.joblib")
featured_cols = joblib.load("model/featured_model.joblib")
scaler = joblib.load("model/scaler.joblib")

print("number of features:", len(featured_cols))

def get_latest_teams_stats(team_name, as_home=True):
    if as_home:
        team_matches = df[df['_home_team'] == team_name].copy()
    else:
        team_matches = df[df['_away_team'] == team_name].copy()

    if team_matches.empty:
        raise ValueError(f"No matches found for: '{team_name}' — check spelling")

    team_matches['_date'] = pd.to_datetime(team_matches['_date'])
    team_matches_sorted = team_matches.sort_values(by='_date', ascending=False)
    latest_match = team_matches_sorted.iloc[0]
    return latest_match

def predict_score(home_team, away_team):
    home_row = get_latest_teams_stats(home_team, as_home=True)
    away_row = get_latest_teams_stats(away_team, as_home=False)

    combined_data = {}

    for col in featured_cols:
        if col.startswith("home_"):
            combined_data[col] = home_row[col]
        elif col.startswith("away_"):
            combined_data[col] = away_row[col]

    combined_data['elo_diff'] = home_row['home_elo'] - away_row['away_elo']
    combined_data['overall_diff'] = home_row['home_avg_overall'] - away_row['away_avg_overall']
    combined_data['attack_diff'] = home_row['home_avg_attack'] - away_row['away_avg_attack']
    combined_data['defense_diff'] = home_row['home_avg_defense'] - away_row['away_avg_defense']

    combined_data['is_neutral'] = 0
    combined_data['is_world_cup'] = 0
    combined_data['is_continental'] = 0

    print("home_elo:", combined_data['home_elo'])
    print("away_elo:", combined_data['away_elo'])
    print("home_avg_attack:", combined_data['home_avg_attack'])
    print("away_avg_attack:", combined_data['away_avg_attack'])

    # create dataframe first, then scale, then predict
    combined = pd.DataFrame([combined_data])[featured_cols]
    combined_scaled = scaler.transform(combined)

    home_goals_expected = home_model.predict(combined_scaled)[0]
    away_goals_expected = away_model.predict(combined_scaled)[0]

    print(f"Expected goals → {home_team}: {home_goals_expected:.2f}, {away_team}: {away_goals_expected:.2f}")

    max_goals = 5
    scorelines = []

    for home_g in range(max_goals + 1):
        for away_g in range(max_goals + 1):
            probability = poisson.pmf(home_g, home_goals_expected) * poisson.pmf(away_g, away_goals_expected)
            scorelines.append((home_g, away_g, probability))

    scorelines = sorted(scorelines, key=lambda x: x[2], reverse=True)
    return scorelines[:5]

result = predict_score("Portugal", "Croatia")
for home_g, away_g, prob in result:
    print(f"{home_g}-{away_g}: {prob*100:.1f}%")