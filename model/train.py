import pandas as pd
import joblib
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# load the csv file dataset

df = pd.read_csv("data/international_matches.csv")
print("loaded data:", df.shape)

# missing colomns

cols_with_missing = [
    "home_avg_pace", "home_avg_shooting", "home_avg_passing",
    "away_avg_pace", "away_avg_shooting", "away_avg_passing",
]

for col in cols_with_missing:
    df[col] = df[col].fillna(df[col].mean())

# featured cols

featured_cols = [
    "home_elo", "away_elo", "elo_diff",
    "home_avg_overall", "home_max_overall", "home_avg_attack",
    "home_avg_defense", "home_avg_pace", "home_avg_shooting", "home_avg_passing",
    "away_avg_overall", "away_max_overall", "away_avg_attack",
    "away_avg_defense", "away_avg_pace", "away_avg_shooting", "away_avg_passing",
    "overall_diff", "attack_diff", "defense_diff",
    "home_form_scored", "home_form_conceded", "home_form_win_rate",
    "away_form_scored", "away_form_conceded", "away_form_win_rate",
    "is_neutral", "is_world_cup", "is_continental",
]

x = df[featured_cols]
y_home = df["home_goals"]
y_away = df["away_goals"]

# train, test and split

x_train, x_test, y_away_train, y_away_test, y_home_train, y_home_test = train_test_split(
    x, y_away, y_home, test_size=0.2, random_state=42
)

# train 2 diffrent poisson models

print("home model train")
home_model = PoissonRegressor(max_iter=1000)
home_model.fit(x_train, y_home_train)

print("awaay model train")
away_model = PoissonRegressor(max_iter=1000)
away_model.fit(x_train, y_away_train)

# evaluate

home_pred = home_model.predict(x_test)
away_pred = away_model.predict(x_test)

home_mae = mean_absolute_error(y_home_test, home_pred)
away_mae = mean_absolute_error(y_away_test, away_pred)

print(f"\nhome goals mae:{home_mae:.3f} ")
print(f"\naway goal mae:{away_mae:.3f}")

# save modules

joblib.dump(home_model, "model/home_model.joblib")
joblib.dump(away_model, "model/away_model.joblib")
joblib.dump(featured_cols, "model/featured_model.joblib")

print("\nModels saved to model/home_model.joblib and model/away_model.joblib")