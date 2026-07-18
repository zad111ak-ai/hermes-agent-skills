---
title: SemVer x.5 Cadence
version: 1.0.0
audience: Developers publishing open-source tools
tags:
  - semver
  - versioning
  - release
  - cadence
---

## SemVer x.5 Cadence

After v0.5.0, version cadence slows to **x.5 steps**:

```text
0.5.0 → 0.5.5 → 0.6.0 → 0.6.5 → 0.7.0 → 0.7.5 → 0.8.0...
```

### Rationale
- **v0.5.0** is a stability milestone — core features complete, 75+ tests, no regressions, works out of the box
- After v0.5.0, only **patch-level changes** (0.5.5, 0.6.5) for bug fixes and minor improvements
- **Minor-level changes** (0.6.0, 0.7.0) for new features, but only after thorough testing
- No breaking changes until v1.0.0

### Version Bump Rules

| Change Type | Version Bump | Example | Notes |
|---|---|---|---|
| Bug fix | 0.5.0 → 0.5.5 | Fix rate limiter edge case | Patch-level, no new features |
| Minor feature | 0.5.5 → 0.6.0 | Add LLM extraction | Minor-level, backward compatible |
| Major feature | 0.6.0 → 0.7.0 | Add persistent session | Minor-level, backward compatible |
| Breaking change | 0.7.0 → 1.0.0 | Remove deprecated API | Major-level, breaking change |

### Release Checklist for x.5 Steps

```bash
# 1. Version bump (all files)
sed -i 's/0\.5\.0/0.5.5/g' pyproject.toml README.md __init__.py

# 2. Run full test suite
pytest tests/ -v

# 3. Pre-commit lint
ruff check --fix . && ruff format .

# 4. Secret audit
scripts/audit-secrets.sh

# 5. Commit
git add -A && git commit -m "v0.5.5 — bug fixes and minor improvements"

# 6. Tag
git tag v0.5.5

# 7. Push
git push origin main --tags

# 8. GitHub release
gh release create v0.5.5 --title "v0.5.5" --generate-notes
```

### Pitfalls
- **Version consistency:** Update ALL version references (pyproject.toml, __init__.py, README badges, MCP server, tests)
- **Secret audit:** Always run `scripts/audit-secrets.sh` before push
- **Pre-commit hooks:** Run linter BEFORE committing to avoid auto-fix loops
- **GitHub release:** Use `--generate-notes` for auto-generated changelog

### References
- [GitHub Publish Workflow](../SKILL.md) — full publish cycle
- [Iterative Release](iterative-release.md) — detailed iterative release walkthrough (Harvest v0.5.0 case study)