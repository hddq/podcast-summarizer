import requests
from config import GPODDER_BASE_URL, AUTH, SINCE_TIMESTAMP

def fetch_episode_actions():
    if not GPODDER_BASE_URL or not AUTH[0]:
        raise ValueError("GPODDER_BASE_URL and GPODDER_USERNAME must be set in .env")

    url = f"{GPODDER_BASE_URL}/api/2/episodes/{AUTH[0]}.json"
    params = {"since": SINCE_TIMESTAMP}

    r = requests.get(url, auth=AUTH, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
