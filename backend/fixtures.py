import requests
from backend.config import API_KEY
from backend.team_mapping import map_team_name
from datetime import date, timedelta

BASE_URL = "https://api.football-data.org/v4/competitions"

COMPETITIONS = ["WC"]

headers = {
    "X-Auth-Token" : API_KEY
}


def _fetch_competition_matches(code, date_from, date_to):
    url = f"{BASE_URL}/{code}/matches"
    params = {"dateFrom": date_from, "dateTo": date_to}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get("matches", [])


def _build_match_dict(match, include_score=False):
    home_team_raw = match["homeTeam"]["name"]
    away_team_raw = match["awayTeam"]["name"]

    result = {
        "home_team": map_team_name(home_team_raw),
        "away_team": map_team_name(away_team_raw),
        "home_crest": match["homeTeam"].get("crest"),
        "away_crest": match["awayTeam"].get("crest"),
        "date": match["utcDate"],
        "competition": match.get("competition", {}).get("code", "N/A"),
        "status": match["status"],
    }

    if include_score:
        score = match.get("score", {}).get("fullTime", {})
        result["actual_home_goals"] = score.get("home")
        result["actual_away_goals"] = score.get("away")

    return result


def get_fixtures():
    today = date.today()
    date_from = (today - timedelta(days=7)).isoformat()
    date_to = (today + timedelta(days=21)).isoformat()

    upcoming = []
    past = []

    for code in COMPETITIONS:
        matches = _fetch_competition_matches(code, date_from, date_to)

        for match in matches:
            status = match["status"]
            if match["homeTeam"].get("name") is None or match["awayTeam"].get("name") is None:
                continue

            if status == "FINISHED":
                past.append(_build_match_dict(match, include_score=True))
            elif status in ("SCHEDULED", "TIMED"):
                upcoming.append(_build_match_dict(match))
            # IN_PLAY, PAUSED, POSTPONED, CANCELLED, SUSPENDED, AWARDED are skipped for now

    upcoming.sort(key=lambda m: m["date"])
    past.sort(key=lambda m: m["date"], reverse=True)

    return {
        "upcoming": upcoming,
        "past": past
    }