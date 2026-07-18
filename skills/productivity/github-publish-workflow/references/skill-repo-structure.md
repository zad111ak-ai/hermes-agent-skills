# Skill/Educational Repo Structure

When publishing a **skills repository** (or any educational/template-based repo), the structure differs from Python package publishing. No PyPI, no semver — the value is in the SKILL.md files and documentation.

## Canonical Structure

```
repo/
├── README.md                    # Overview, table of skills, quick start, donations
├── CONTRIBUTING.md              # How to add new skills (on Russian if RU audience)
├── SKILL_TEMPLATE.md            # Copy-paste starter with YAML frontmatter
├── LICENSE                      # MIT
├── examples/
│   └── BEFORE_AFTER.md          # Visual before/after comparisons
├── skills/
│   ├── category1/
│   │   └── skill-name/
│   │       └── SKILL.md         # One skill per directory
│   ├── category2/
│   │   └── ...
└── .github/
    └── FUNDING.yml              # Donation links
```

## Key Patterns

### README.md (skill repos)
- **Language:** Match audience (RU for RU users, EN for international)
- **Table of all skills** with one-line descriptions and metrics ("saves ~50% tokens")
- **Quick Start:** 3-step install (clone → copy → verify)
- **Structure section** showing the tree
- **Donation block** at bottom (BTC, ETH, USDT/TON, SOL + Boosty/GitHub Sponsors)

### CONTRIBUTING.md
- Step-by-step: copy template → edit → test locally → PR
- **Checklist** of requirements (YAML frontmatter, tags, examples, pitfalls)
- **Tag vocabulary** — defined list of allowed tags for consistency
- **Commit format** — conventional commits (`feat:`, `fix:`, `docs:`)

### SKILL_TEMPLATE.md
- Minimal YAML frontmatter example (name, description, tags)
- Section skeleton: Зачем → Как работает → Правила → Примеры → Метрики
- **Pre-submit checklist** with checkboxes

### BEFORE_AFTER examples
- 3-5 concrete comparisons showing the skill's impact
- Format: **ДО ❌** (problem) vs **ПОСЛЕ ✅** (solution with metrics)
- Cover different skill types (meta, productivity, security)

## Differences from Code Package Publishing

| Aspect | Code Package | Skill Repo |
|--------|-------------|------------|
| Versioning | SemVer (0.1.0, 0.2.0) | No versioning needed |
| PyPI/pip | Yes | No |
| Tests | Required | Optional (validation scripts) |
| Pre-commit hooks | ruff, black, pyright | Markdown lint (optional) |
| README language | English-only | Match audience |
| Donation format | Badges + table | Badges + table + Boosty |
| Primary value | Working code | Documentation quality |

## Promotion Strategy for Skill Repos

1. **Telegram AI/Dev channels** — post 2-3 best skills with metrics
2. **Habr** — article with 3 skill deep-dives (Russian tech audience)
3. **GitHub Discussions** — enable for Q&A
4. **Reddit** — r/LocalLLaMA, r/selfhosted (if relevant)
5. **Cross-link** — add to Hermes Agent docs/community pages

## Pitfalls

- **Don't version skill repos** like code packages — skills evolve independently
- **English-only** rule from monetization-publish does NOT apply to RU-audience skill repos — match your audience
- **SKILL.md is the product** — invest in quality writing, not clever code
- **Examples > descriptions** — show before/after, not feature lists
- **Tag taxonomy matters** — define allowed tags upfront or you get chaos
