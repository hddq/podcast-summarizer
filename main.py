import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

BASE_URL = os.getenv("GPODDER_BASE_URL").rstrip("/")
USERNAME = os.getenv("GPODDER_USERNAME")
PASSWORD = os.getenv("GPODDER_PASSWORD")
SINCE = int(os.getenv("SINCE_TIMESTAMP", "0"))

AUTH = (USERNAME, PASSWORD)

def parse_timestamp(ts):
    if ts is None:
        return None

    # UNIX timestamp (int or numeric string)
    if isinstance(ts, (int, float)) or (isinstance(ts, str) and ts.isdigit()):
        return datetime.fromtimestamp(int(ts))

    # ISO 8601 string
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            return None

    return None

def fetch_episode_actions():
    url = f"{BASE_URL}/api/2/episodes/{USERNAME}.json"
    params = {"since": SINCE}

    r = requests.get(url, auth=AUTH, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def main():
    data = fetch_episode_actions()

    actions = data.get("actions", [])
    plays = [a for a in actions if a.get("action") == "play"]

    # sort safely using parsed timestamp
    plays.sort(key=lambda a: parse_timestamp(a.get("timestamp")) or datetime.min)

    print(f"\n🎧 Played episodes: {len(plays)}\n")

    for a in plays:
        dt = parse_timestamp(a.get("timestamp"))
        time_str = dt.isoformat() if dt else "unknown"

        print("─" * 80)
        print(f"🕒 {time_str}")
        print(f"📡 Podcast: {a.get('podcast')}")
        print(f"🎙 Episode: {a.get('episode')}")
        print(f"▶️  Position: {a.get('position')} / {a.get('total')}")

if __name__ == "__main__":
    main()