from datetime import datetime
from gpodder import fetch_episode_actions
from utils import parse_timestamp
from downloader import download_file
from transcriber import transcribe

def main():
    try:
        data = fetch_episode_actions()
    except Exception as e:
        print(f"Failed to fetch actions: {e}")
        return

    actions = data.get("actions", [])
    plays = [a for a in actions if a.get("action") == "play"]

    # sort safely using parsed timestamp
    plays.sort(key=lambda a: parse_timestamp(a.get("timestamp")) or datetime.min)

    print(f"\n🎧 Played episodes: {len(plays)}\n")

    for a in plays:
        dt = parse_timestamp(a.get("timestamp"))
        time_str = dt.isoformat() if dt else "unknown"
        episode_url = a.get('episode')
        podcast_url = a.get('podcast')

        print("─" * 80)
        print(f"🕒 {time_str}")
        print(f"📡 Podcast: {podcast_url}")
        print(f"🎙 Episode: {episode_url}")
        print(f"▶️  Position: {a.get('position')} / {a.get('total')}")

        if episode_url:
             filepath = download_file(episode_url)
             if filepath:
                 transcribe(filepath)
        else:
             print("⚠️ No episode URL found, skipping download.")

if __name__ == "__main__":
    main()
