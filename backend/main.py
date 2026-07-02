from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 
import sys

# lets backend import model from predict file

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))

from model.predict import predict_score

app = FastAPI()

# allows frontend to call the backend 

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_headers = ["*"],
    allow_methods = ["*"],
)

@app.get("/")
def root():
    return{"message":"football prediction api is running"}

@app.get("/predict")
def predict(home_team: str, away_team: str, is_neutral: int = 0, is_world_cup: int = 0, is_continental: int = 0):
    home_g, away_g, probs = predict_score(home_team, away_team, is_neutral, is_world_cup, is_continental)
    return{
        "home_team" : home_team,
        "away_team" : away_team,
        "predicted_home_goals" : home_g,
        "predicted_away_goals" : away_g,
        "probability" : round(probs * 100, 1)
    }

from backend.fixtures import get_fixtures

@app.get("/fixtures")
def fixtures():
    return get_fixtures()
