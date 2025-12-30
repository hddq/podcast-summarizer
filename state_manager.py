import json
import os
from config import SINCE_TIMESTAMP

STATE_FILE = "state.json"

def load_last_timestamp():
    """
    Loads the last timestamp from state.json.
    If the file doesn't exist or is invalid, returns the default SINCE_TIMESTAMP from config.
    """
    if not os.path.exists(STATE_FILE):
        return SINCE_TIMESTAMP
    
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            return data.get("last_timestamp", SINCE_TIMESTAMP)
    except (json.JSONDecodeError, IOError):
        print(f"Warning: Could not read {STATE_FILE}. Using default SINCE_TIMESTAMP.")
        return SINCE_TIMESTAMP

def save_last_timestamp(timestamp):
    """
    Saves the given timestamp to state.json.
    """
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({"last_timestamp": int(timestamp)}, f)
        print(f"State saved: last_timestamp={int(timestamp)}")
    except IOError as e:
        print(f"Error saving state: {e}")
