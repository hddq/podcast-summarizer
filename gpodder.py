import requests
from config import GPODDER_BASE_URL, AUTH, SINCE_TIMESTAMP

def fetch_episode_actions(since=None):
    if not GPODDER_BASE_URL or not AUTH[0]:
        raise ValueError("GPODDER_BASE_URL and GPODDER_USERNAME must be set in .env")

    timestamp = since if since is not None else SINCE_TIMESTAMP
    url = f"{GPODDER_BASE_URL}/api/2/episodes/{AUTH[0]}.json"
    params = {"since": timestamp}

    r = requests.get(url, auth=AUTH, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
