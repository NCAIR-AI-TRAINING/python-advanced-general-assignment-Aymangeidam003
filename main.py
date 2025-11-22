from datetime import datetime, timedelta
import os

VISITOR_LOG = "visitors.txt"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

class DuplicateVisitorError(Exception):
    pass

class WaitTimeError(Exception):
    pass

def ensure_file():
    if not os.path.exists(VISITOR_LOG):
        with open(VISITOR_LOG, "w", encoding="utf-8") as f:
            pass

def read_last_entry():
    ensure_file()
    with open(VISITOR_LOG, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return None, None
    last = lines[-1]
    name, ts = last.split(" | ")
    return name, datetime.fromisoformat(ts)

def add_visitor(name):
    name = name.strip()
    if not name:
        raise ValueError("Name must be non-empty")
    ensure_file()
    last_name, last_ts = read_last_entry()

    # Duplicate consecutive check
    if last_name == name:
        raise DuplicateVisitorError("Duplicate consecutive visitor not allowed")

    # 5-minute wait check
    now = datetime.now()
    if last_ts is not None and (now - last_ts) < timedelta(minutes=5):
        raise WaitTimeError("5-minute wait required between different visitors")

    with open(VISITOR_LOG, "a", encoding="utf-8") as f:
        f.write(f"{name} | {now.isoformat()}\n")
