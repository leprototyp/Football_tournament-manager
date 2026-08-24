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
