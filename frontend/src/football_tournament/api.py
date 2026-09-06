import requests

API_URL = "http://localhost:8000"
API_KEY = "your-secret-api-token-here"

def set_config(url: str, key: str = None):
    global API_URL, API_KEY
    if url:
        API_URL = url.rstrip('/')
    if key:
        API_KEY = key

def get_headers():
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["x-api-token"] = API_KEY
    return headers

def check_health():
    try:
        res = requests.get(f"{API_URL}/health", headers=get_headers(), timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def get_tournaments():
    res = requests.get(f"{API_URL}/tournaments/", headers=get_headers())
    res.raise_for_status()
    return res.json()

def create_tournament(name: str, start_date: str, end_date: str):
    payload = {
        "name": name,
        "start_date": start_date,
        "end_date": end_date
    }
    # Tentative avec slash puis sans slash pour contourner la redirection 405
    res = requests.post(f"{API_URL}/tournaments/", json=payload, headers=get_headers())
    if res.status_code == 405:
        res = requests.post(f"{API_URL}/tournaments", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()

def get_teams():
    res = requests.get(f"{API_URL}/teams/", headers=get_headers())
    res.raise_for_status()
    return res.json()

def create_team(name: str, coach_name: str):
    payload = {"name": name, "coach_name": coach_name}
    res = requests.post(f"{API_URL}/teams/", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()

def get_matches():
    res = requests.get(f"{API_URL}/matches/", headers=get_headers())
    res.raise_for_status()
    return res.json()

def create_match_scheduled(tournament_id: int, home_team_id: int, away_team_id: int, match_date: str, referee: str):
    payload = {
        "tournament_id": tournament_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "match_date": match_date,
        "referee": referee
    }
    res = requests.post(f"{API_URL}/matches/", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()

def update_match_result(match_id: int, home_score: int, away_score: int):
    payload = {"home_score": home_score, "away_score": away_score}
    params = {"home_score": home_score, "away_score": away_score}
    
    attempts = [
        ("PUT", f"{API_URL}/matches/{match_id}/score", payload, None),
        ("PUT", f"{API_URL}/matches/{match_id}", payload, None),
        ("PATCH", f"{API_URL}/matches/{match_id}", payload, None),
        ("PUT", f"{API_URL}/matches/{match_id}/score", None, params),
        ("POST", f"{API_URL}/matches/{match_id}/score", payload, None),
    ]
    
    last_res = None
    for method, url, json_data, req_params in attempts:
        res = requests.request(method, url, json=json_data, params=req_params, headers=get_headers())
        if res.status_code < 400:
            return res.json()
        last_res = res
        
    if last_res is not None:
        last_res.raise_for_status()

def update_score(match_id: int, home_score: int, away_score: int):
    payload = {
        "home_score": home_score,
        "away_score": away_score
    }
    res = requests.put(f"{API_URL}/matches/{match_id}/score", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()


def get_standings(tournament_id: int):
    res = requests.get(f"{API_URL}/tournaments/{tournament_id}/ranking", headers=get_headers())
    res.raise_for_status()
    return res.json()

def create_match_scheduled(tournament_id: int, home_team_id: int, away_team_id: int, match_date: str, referee: str):
    payload = {
        "tournament_id": tournament_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "match_date": match_date,
        "referee": referee
    }
    res = requests.post(f"{API_URL}/matches/", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()
