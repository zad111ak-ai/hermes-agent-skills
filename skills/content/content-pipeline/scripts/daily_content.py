#!/usr/bin/env python3
"""Daily content generation pipeline script.

Usage: python daily_content.py [niche] [platforms]

Called by Hermes cron — outputs content plan to stdout for agent processing.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

CONTENT_DIR = Path.home() / "content_output"
TRACKER_FILE = CONTENT_DIR / "tracker.json"

def load_tracker():
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text())
    return {"published": [], "ideas": [], "stats": {}}

def save_tracker(data):
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    TRACKER_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def get_recent_topics(tracker, n=10):
    return [p.get("topic", "") for p in tracker.get("published", [])[-n:]]

def main():
    niche = sys.argv[1] if len(sys.argv) > 1 else "technology"
    platforms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["telegram", "youtube", "blog"]

    tracker = load_tracker()
    recent = get_recent_topics(tracker)

    plan = {
        "date": datetime.now().isoformat(),
        "niche": niche,
        "platforms": platforms,
        "recent_topics_to_avoid": recent,
        "request": f"Generate 3 content ideas for {niche} targeting {', '.join(platforms)}. "
                   f"Avoid these recent topics: {recent}. "
                   f"For each idea provide: title, platform, format (video/post/thread), "
                   f"estimated_time, monetization_angle."
    }

    print(json.dumps(plan, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
