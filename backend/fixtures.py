import requests
from backend.config import API_KEY

url = "https://api.football-data.org/v4/matches"

headers = {
    "X-Auth-Token" : API_KEY
}

def get_fixtures():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch fixtures", "status": response.status_code}
    
    data = response.json()
    print("API status:", response.status_code)
    print("API response:", data)

    fixtures = []

    if "matches" not in data:
        return {"error": "No matches found", "details": data}

    for match in data["matches"]:
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        date = match["utcDate"]
        competition = match.get("competition", {}).get("code", "N/A")
        fixtures.append({
            "home_team" : home_team,
            "away_team" : away_team,
            "date" : date,
            "competition" : competition,
        })
    return fixtures

