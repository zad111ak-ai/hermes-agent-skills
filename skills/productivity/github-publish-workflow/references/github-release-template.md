---
title: GitHub Release Template
version: 1.0.0
audience: Developers publishing open-source tools
tags:
  - github
  - release
  - template
  - changelog
---

## GitHub Release Template

### v0.5.0 — LLM Extraction + Enhanced Stealth

```markdown
## v0.5.0 — LLM Extraction + Enhanced Stealth

### New Features
- **LLM extraction** — describe what you want in natural language, get structured JSON. No CSS selectors needed
- **Enhanced stealth** — 24 rotating User-Agents (Chrome/Firefox/Edge/Safari), randomized viewport/timezone/locale/platform
- **Response caching** — in-memory TTL cache (5 min default), zero-cost repeat requests
- **Rate limiting** — token bucket (10 req/min default), configurable
- **Persistent browser session** — one session reused across requests
- **Adaptive error logging** — self-learning loop integration

### Fixes
- CaptchaSolver import fix
- Removed old GIF artifacts

### Package
- PyPI package: `harvest-agent` (CLI commands unchanged: `harvest`, `harvest-mcp`)
- Install: `pip install harvest-agent` or `git clone`

### Breaking Changes
- Version bumped to 0.5.0 (SemVer x.5 cadence: 0.5.5, 0.6.0, 0.6.5...)

### Tests
- 75/75 passed (14 new tests for cache, rate_limiter, stealth)
```

### v0.5.5 — Bug Fixes and Minor Improvements

```markdown
## v0.5.5 — Bug Fixes and Minor Improvements

### Fixes
- Rate limiter edge case on burst requests
- Cache TTL precision fix
- Stealth UA rotation fix for Safari

### Improvements
- Better error messages for LLM extraction
- Reduced memory usage for cache

### Tests
- 75/75 passed (no regressions)
```

### v0.6.0 — New Features

```markdown
## v0.6.0 — New Features

### New Features
- **Smart crawl** — adaptive depth based on content
- **Diff monitor** — track changes on target sites
- **Multi-export** — XLSX, JSONL, Markdown
- **One-command pipeline** — `harvest run pipeline.yaml`

### Improvements
- Faster LLM extraction
- Better stealth fingerprinting

### Tests
- 80/80 passed (5 new tests)
```

### Pitfalls
- **Changelog:** Always include **New Features**, **Fixes**, **Improvements**, **Tests** sections
- **Tests:** Always report test count and new tests added
- **Breaking Changes:** Always mention if version cadence changes (e.g., SemVer x.5)
- **Install:** Always include PyPI package name and CLI commands

### References
- [GitHub Publish Workflow](../SKILL.md) — full publish cycle
- [SemVer x.5](semver-x5.md) — versioning rules