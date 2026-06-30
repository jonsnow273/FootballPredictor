# ⚽ Football Match Score Predictor

A web app that predicts football match scores using historical data and a Poisson regression model. Pulls live upcoming fixtures from a football API, predicts the most likely scoreline for each match, and displays results through a simple web interface.

## How It Works

1. **Training (offline, one-time):** A Poisson regression model is trained on historical match data to learn each team's attack and defense strength.
2. **Fixtures:** The backend fetches upcoming real-world matches (Champions League, Premier League, La Liga, etc.) from the football-data.org API.
3. **Prediction:** For each fixture, the model calculates expected goals for both teams and converts that into a probability distribution over possible scorelines using the Poisson distribution.
4. **Frontend:** Displays upcoming matches with their predicted scores and probabilities.

## Tech Stack

| Layer | Tools |
|---|---|
| Model | scikit-learn (`PoissonRegressor`), scipy |
| Data handling | pandas, numpy |
| Backend | FastAPI, uvicorn, pydantic |
| External data | football-data.org API |
| Frontend | HTML, CSS, JavaScript |
| Model persistence | joblib |

## Project Structure
football-prediction/
├── backend/          # FastAPI app, API integration, endpoints
├── data/              # Historical match data (CSV)
├── frontend/          # HTML/CSS/JS interface
├── model/             # Training script, prediction logic, saved model
├── .env               # API keys (not committed)
├── requirements.txt
└── README.md

## Setup

1. Clone the repo
```bash
   git clone https://github.com/yourusername/football-prediction.git
   cd football-prediction
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Add your API key
   Create a `.env` file in the root folder:
   API_KEY=your_football_data_org_key_here

4. Train the model
```bash
   python model/train.py
```

5. Run the backend
```bash
   uvicorn backend.main:app --reload
```

6. Open `frontend/index.html` in your browser

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /fixtures` | Returns upcoming real matches |
| `GET /h2h?team1=X&team2=Y` | Returns head-to-head history |
| `GET /predict?home=X&away=Y` | Returns predicted scoreline + probabilities |

## Limitations

- Predictions are based on historical scoring patterns, not real-time factors like injuries or lineups.
- Exact-score predictions carry inherent uncertainty — the model outputs the most probable scoreline along with alternative probabilities, not a guaranteed outcome.

## Author

Pranit — built as a personal project exploring applied machine learning in sports analytics.
