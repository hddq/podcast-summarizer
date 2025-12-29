from datetime import datetime

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
