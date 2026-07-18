# Iterative Release Walkthrough — Harvest v0.5.0

Case study of releasing v0.5.0 for the Harvest project (zad111ak-ai/harvest).

## Starting State
- v0.4.0 on GitHub with 61 tests passing
- New features added: LLM extraction, enhanced stealth, rate limiter, cache, persistent session
- Need to clean secrets, update README, bump version, tag, push

## Step 1: Version Bump (Multiple Files)

Found all version references with grep:
```bash
grep -rn "0.4.0" --include="*.py" --include="*.toml"
```

Updated in 5 files simultaneously:
- `harvest/__init__.py` — `__version__ = "0.5.0"`
- `pyproject.toml` — `version = "0.5.0"`
- `harvest/server.py` — MCP server status response
- `harvest_mcp.py` — MCP entrypoint version
- `tests/test_all.py` — version assertion tests

**Lesson:** Version strings live in surprising places. Always grep, never assume.

## Step 2: Secret Audit

```bash
# Check source code (not venv)
grep -rn "185.161.228\|tokyo\|c6y7b2n0\|dima\|sk-" --include="*.py" harvest/ .harvest/
# Result: clean

# Check config files
grep -rn "password\|token\|secret" .harvest/config.example.yaml
# Result: only empty placeholder fields — safe to commit
```

## Step 3: .gitignore Patterns

For projects with user-specific configs:
```gitignore
# Config (user-specific)
.harvest/config.yaml
.harvest/config*.yaml
!.harvest/config.example.yaml
```

The `!` prefix whitelists the example while ignoring real configs.

## Step 4: Pre-commit Hook Sequence

First commit attempt:
```
trailing-whitespace: auto-fixed browser.py, extract.py
end-of-file-fixer: auto-fixed 4 files
ruff: F401 unused import (AdaptiveCore) — auto-removed
ruff-format: 6 files reformatted
→ exit code 1, commit blocked
```

Fix: Run linter first, then commit:
```bash
ruff check --fix . && ruff format .
git add -A
git commit -m "v0.5.0 — ..."
```

## Step 5: Tag and Push

```bash
git tag v0.5.0
git push origin main --tags
gh release create v0.5.0 --title "v0.5.0" --generate-notes
```

## SemVer Cadence (User Preference)

After v0.5.0, user requested slower cadence: step by 0.5
- `0.5.0` → `0.5.5` (patch cluster)
- `0.5.5` → `0.6.0` (minor feature batch)
- `0.6.0` → `0.6.5` (patch cluster)

## Key Pitfalls
1. **Don't forget test version assertions** — tests that check `__version__` or MCP status version will fail if missed
2. **Pre-commit auto-fix ≠ success** — hooks fix the file but still exit 1, must re-stage and re-commit
3. **.harvest/ vs .gitignore** — `!.harvest/config.example.yaml` pattern is tricky, verify with `git status`
4. **GIF files in git** — if removing, stage deletion (`git rm`) or let `git add -A` catch it
5. **venv grep pollution** — always exclude `venv/` from secret scans, false positives everywhere
