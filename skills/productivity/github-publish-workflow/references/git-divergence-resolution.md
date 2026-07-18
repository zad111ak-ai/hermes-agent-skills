# Git Branch Divergence & Conflict Resolution

## When branches diverge
Local and remote have different commits. `git push` fails with "branch tip is behind".

## Correct flow (avoids rebase hell)
```bash
# 1. Diagnose
git status
# "Your branch and 'origin/main' have diverged, and have N and M different commits"

# 2. Merge (NOT rebase) — preserves history, simpler conflict resolution
git pull --no-rebase origin main

# 3. Resolve conflicts if any
grep -n "<<<<<<" FILE.md   # find markers
# Pick correct version per conflict

# 4. Commit merge + push
git add -A && git commit -m "merge: resolve conflict"
git push origin main
```

## If rebase went wrong mid-way
```bash
# Abort
git rebase --abort 2>/dev/null
rm -rf .git/rebase-merge .git/rebase-apply 2>/dev/null

# Reset clean
git reset --hard HEAD

# Use --no-rebase instead
git pull --no-rebase origin main
```

## Python script for bulk conflict resolution
When you need to pick one side programmatically:
```python
with open('FILE.md', 'r') as f:
    content = f.read()

# Replace entire conflict block with desired version
old = """<<<<<<< HEAD
<local content>
=======
<remote content>
>>>>>>> ..."""

new = """<desired content>"""

content = content.replace(old, new)
with open('FILE.md', 'w') as f:
    f.write(content)
```

## Pitfalls
- **NEVER use `git pull --rebase`** when branches have diverged with conflicting changes — cascading rebase conflicts are harder than merge conflicts
- **Detached HEAD after abort:** `git checkout main` first
- **Prevention:** always `git pull --no-rebase` before pushing when remote might have commits (long sessions, context compression)
- **Divergence detection:** after context compression or if push fails, check `git status` immediately — don't blind-push
