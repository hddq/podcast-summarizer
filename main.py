import time
import sys
from datetime import datetime
from gpodder import fetch_episode_actions
from utils import parse_timestamp
from downloader import download_file
from transcriber import transcribe
from summarizer import summarize
from state_manager import load_last_timestamp, save_last_timestamp

POLL_INTERVAL = 600  # 10 minutes

def process_actions(since_ts):
    """
    Fetches and processes actions since the given timestamp.
    Returns the updated timestamp (max of current and processed actions).
    """
    try:
        data = fetch_episode_actions(since=since_ts)
    except Exception as e:
        print(f"Failed to fetch actions: {e}")
        return since_ts

    actions = data.get("actions", [])
    plays = [a for a in actions if a.get("action") == "play"]
    
    if not plays:
        print("No new 'play' actions found.")
        return since_ts

    # sort safely using parsed timestamp
    plays.sort(key=lambda a: parse_timestamp(a.get("timestamp")) or datetime.min)

    print(f"\n🎧 New played episodes: {len(plays)}\n")

    max_ts = since_ts

    for a in plays:
        raw_ts = a.get("timestamp")
        dt = parse_timestamp(raw_ts)
        time_str = dt.isoformat() if dt else "unknown"
        episode_url = a.get('episode')
        podcast_url = a.get('podcast')

        print("─" * 80)
        print(f"🕒 {time_str}")
        print(f"📡 Podcast: {podcast_url}")
        print(f"🎙 Episode: {episode_url}")
        print(f"▶️  Position: {a.get('position')} / {a.get('total')}")

        # Update max_ts if this action is newer
        if dt:
             ts_val = int(dt.timestamp())
             if ts_val > max_ts:
                 max_ts = ts_val

        if episode_url:
             filepath = download_file(episode_url)
             if filepath:
                 transcript_path = transcribe(filepath)
                 if transcript_path:
                     summarize(transcript_path)
        else:
             print("⚠️ No episode URL found, skipping download.")
        
    return max_ts

def main():
    print("🚀 Starting Podcast Summarizer Loop...")
    current_since = load_last_timestamp()
    print(f"📅 Starting check from timestamp: {current_since}")

    try:
        while True:
            print(f"\nChecking for new actions (since {current_since})...")
            new_since = process_actions(current_since)
            
            if new_since > current_since:
                current_since = new_since
                save_last_timestamp(current_since)
            
            print(f"💤 Sleeping for {POLL_INTERVAL} seconds...")
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping loop. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
