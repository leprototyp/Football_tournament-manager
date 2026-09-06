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
    """Vérifie si le backend est joignable"""
    try:
        res = requests.get(f"{API_URL}/health", headers=get_headers(), timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def get_tournaments():
    res = requests.get(f"{API_URL}/tournaments/", headers=get_headers())
    res.raise_for_status()
    return res.json()

def get_teams():
    res = requests.get(f"{API_URL}/teams/", headers=get_headers())
    res.raise_for_status()
    return res.json()

def get_matches():
    res = requests.get(f"{API_URL}/matches/", headers=get_headers())
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





def create_tournament(name: str, start_date: str, end_date: str):
    import requests
    token = globals().get('API_TOKEN') or globals().get('API_KEY', '')
    url = globals().get('BASE_URL', 'http://localhost:8000').rstrip('/')
    payload = {
        "name": name,
        "start_date": start_date,
        "end_date": end_date
    }
    headers = {"X-API-Token": token} if token else {}
    
    # Essai sans slash puis avec slash en cas de redirection backend
    try:
        res = requests.post(f"{url}/tournaments", json=payload, headers=headers)
    except requests.exceptions.HTTPError:
        res = requests.post(f"{url}/tournaments/", json=payload, headers=headers)
        
    res.raise_for_status()
    return res.json()

def create_team(name: str, coach_name: str):
    payload = {"name": name, "coach_name": coach_name}
    res = requests.post(f"{API_URL}/teams/", json=payload, headers=get_headers())
    res.raise_for_status()
    return res.json()

def create_team(name: str, coach_name: str):
    payload = {"name": name, "coach_name": coach_name}
    res = requests.post(f"{API_URL}/teams/", json=payload, headers=get_headers())
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
    """Envoie une requête PUT ou POST au backend pour mettre à jour le score du match."""
    payload = {
        "home_score": home_score,
        "away_score": away_score
    }
    # Adaptez l'URL '/matches/{match_id}/score' selon la route exacte définie dans votre backend FastAPI
    response = requests.put(
        f"{BASE_URL}/matches/{match_id}/score",
        json=payload,
        headers=get_headers()
    )
    if response.status_code not in (200, 204):
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    return response.json() if response.text else {}
