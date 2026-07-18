#!/bin/bash
# Auto-save Hermes memory after each significant session
# Called by cron or session-end hook

HERMES_HOME="$HOME/.hermes"
MEMORY_FILE="$HERMES_HOME/MEMORY.md"
SESSIONS_DB="$HERMES_HOME/sessions/sessions.json"
FACTS_DB="$HERMES_HOME/memory_store.db"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Don't run if memory was saved in last 10 minutes
if [ -f "$HERMES_HOME/.last_memory_save" ]; then
    LAST_SAVE=$(stat -c %Y "$HERMES_HOME/.last_memory_save" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_SAVE))
    if [ "$DIFF" -lt 600 ]; then
        exit 0
    fi
fi

# Count facts in DB
FACT_COUNT=$(sqlite3 "$FACTS_DB" "SELECT COUNT(*) FROM facts;" 2>/dev/null || echo "0")

# Count entries in MEMORY.md
MEMORY_LINES=$(wc -l < "$MEMORY_FILE" 2>/dev/null || echo "0")

# Log the state
echo "[$TIMESTAMP] Memory check: $FACT_COUNT facts in DB, $MEMORY_LINES lines in MEMORY.md" >> "$HERMES_HOME/logs/memory_guardian.log"

# Mark as saved
touch "$HERMES_HOME/.last_memory_save"
