#!/usr/bin/env python3
"""Daily memory consolidation — extracts facts from recent sessions and saves to MEMORY.md.

Run via Hermes cron at 3am daily. Reads session dumps, finds important info,
and appends to MEMORY.md if not already there.
"""
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
MEMORY_FILE = HERMES_HOME / "MEMORY.md"
SESSIONS_DIR = HERMES_HOME / "sessions"
FACTS_DB = HERMES_HOME / "memory_store.db"
LOG_FILE = HERMES_HOME / "logs" / "memory_consolidation.log"

# Patterns that indicate important info worth saving
IMPORTANT_PATTERNS = [
    r"(?:user|пользователь|юзер).*(?:хочет| wants?|нужно|needs?|планирует|plans?)",
    r"(?:решили|decided|решение|decision)",
    r"(?:установи|install|настрой|configure|setup|внедри|implement)",
    r"(?:api[_ ]?key|token|пароль|password|секрет|secret)",
    r"(?:важно|important|критично|critical|никогда|never|всегда|always)",
    r"(?:баг|bug|ошибка|error|проблема|problem|fix|исправил)",
    r"(?:монетиз|monetiz|контент|content|видео|video|блог|blog)",
]


def load_memory():
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return ""


def save_memory(content):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(content, encoding="utf-8")


def find_recent_sessions(days=2):
    """Find session dump files from the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    sessions = []
    for f in SESSIONS_DIR.glob("request_dump_*.json"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime > cutoff:
            sessions.append(f)
    return sorted(sessions, key=lambda f: f.stat().st_mtime, reverse=True)


def extract_important_lines(text, max_lines=20):
    """Find lines matching important patterns."""
    found = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) < 10 or len(line) > 500:
            continue
        for pattern in IMPORTANT_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                found.append(line)
                break
        if len(found) >= max_lines:
            break
    return found


def main():
    log_dir = LOG_FILE.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    current_memory = load_memory()
    recent_files = find_recent_sessions(days=1)

    new_entries = []
    for session_file in recent_files:
        try:
            data = json.loads(session_file.read_text(encoding="utf-8"))
            # Extract conversation text
            messages = data.get("messages", [])
            for msg in messages:
                content = msg.get("content", "")
                if isinstance(content, str):
                    important = extract_important_lines(content)
                    new_entries.extend(important)
        except Exception:
            continue

    # Deduplicate against existing memory
    existing_lines = set(current_memory.lower().split("\n"))
    truly_new = [e for e in new_entries if e.lower() not in existing_lines]

    if truly_new:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        section = f"\n\n## Auto-saved [{timestamp}]\n"
        for entry in truly_new[:10]:  # Max 10 new entries per run
            section += f"- {entry}\n"

        save_memory(current_memory + section)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] Added {len(truly_new)} entries to MEMORY.md\n")
    else:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] No new entries to save\n")


if __name__ == "__main__":
    main()
