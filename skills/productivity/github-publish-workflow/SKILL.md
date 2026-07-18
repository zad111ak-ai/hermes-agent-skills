---
name: GitHub Publish Workflow
version: 1.1.0
description: Полный цикл публикации open-source проекта на GitHub — от инициализации до релиза v1.0.0. Включает создание логотипа, проверку валидности SVG, шаблон README, MIT лицензию, pre-commit hooks, тесты, версионирование x.5, и публикацию релиза.
summary: Полный цикл публикации open-source проекта на GitHub — от инициализации до релиза v1.0.0. Включает создание логотипа, проверку валидности SVG, шаблон README, MIT лицензию, pre-commit hooks, тесты, версионирование x.5, и публикацию релиза.
audience: Разработчики, публикующие инструменты на GitHub
tags:
  - github
  - open-source
  - release
  - semver
  - monetization
  - documentation
  - branding
  - harvest
trigger:
  - "выложить на гитхаб"
  - "сделать релиз"
  - "опубликовать проект"
  - "подготовить к публикации"
  - "версионирование"
  - "донаты"
  - "shields.io"
  - "README"
  - "gitignore"
  - "pre-commit"
  - "тесты"
  - "чистка кода"
  - "v0.5.0"
  - "LLM extraction"
  - "stealth"
  - "rate limiter"
  - "cache"
---

## Цель
Опубликовать open-source проект на GitHub так, чтобы:
- Работал из коробки
- Не содержал личной информации и секретов
- Имел качественную документацию и примеры
- Поддерживал монетизацию через криптовалюты
- **SemVer 0.0.1 step:** 0.6.2 → 0.6.3 → 0.6.4 → 0.7.0. v1.0.0 = full product readiness.


## Шаги

### 1. Инициализация репозитория
```bash
git init
# Создать logo.svg (минималистичный, dark background, golden palette)
echo '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 10 L60 30 L80 30 L65 45 L70 65 L50 55 L30 65 L35 45 L20 30 L40 30 Z" fill="#F5D76E"/></svg>' > logo.svg

# Добавить в .gitignore
cat << 'EOF' > .gitignore
.harvest/
.env
*.log
*.pyc
__pycache__/
.DS_Store
*.swp
*.swo
*.db
*.sqlite
*.sqlite3
*.db-journal
*.bak
*.tmp
*.temp
*.orig
*.rej
*.egg-info/
dist/
build/
*.egg
*.whl
*.tar.gz
*.zip
EOF
```

### 2. README.md
**Bilingual (Russian + English):** All public repos use bilingual READMEs with anchor-based language switcher. See [references/bilingual-readme.md](references/bilingual-readme.md) for the template.

**Structure:**
```markdown
# 🌾 Harvest

<p align="center">
  <a href="#russian">🇷🇺 Русский</a> &nbsp;|&nbsp; <a href="#english">🇬🇧 English</a>
</p>

[![GitHub Stars](https://img.shields.io/github/stars/zad111ak-ai/harvest?style=social)](https://github.com/zad111ak-ai/harvest)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<a id="russian"></a>
## 🇷🇺 О проекте
... (Russian content first) ...

---

<a id="english"></a>
## 🇬🇧 About
... (English content second) ...

## 💖 Donate / Донаты
[![BTC](https://img.shields.io/badge/BTC-bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j?logo=bitcoin)](https://blockchain.info/address/bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j)
[![ETH](https://img.shields.io/badge/ETH-0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3?logo=ethereum)](https://etherscan.io/address/0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3)
[![TON](https://img.shields.io/badge/TON-UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP?logo=ton)](https://tonviewer.com/UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP)
[![SOL](https://img.shields.io/badge/SOL-99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK?logo=solana)](https://solscan.io/address/99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK)

## 📜 License / Лицензия

MIT
```

**Pitfalls:**
- **Bilingual mandatory:** Every public repo MUST have Russian + English sections. Russian goes first (primary audience).
- **Language switcher:** Use `<a id="...">` anchors + `<p align="center">` nav bar at the very top, before badges.
- **Donation table format:** For repos with less content, use a simple table instead of shields.io badges — both formats are acceptable.
- **Comparison table:** Always include competitors relevant to the project
- **Live examples:** Always show real code snippets with output
- **Donate badges:** Always verify block explorer URLs (see [references/donate-badges.md](references/donate-badges.md))
- **Logo:** Always use `logo.svg` (not PNG, not GIF)
- **Multi-repo batch updates:** When updating multiple repos, commit each separately, then push all. Verify `git log -1 --oneline` before pushing.

### 3. Версионирование
- **SemVer 0.0.1 step:** 0.6.2 → 0.6.3 → 0.6.4 → 0.7.0
- **Теги:** `git tag v0.6.3 && git push --tags`
- **Релиз:** `gh release create v0.6.3 --notes "## v0.6.3 — ..."`

### 4. Чистка перед публикацией
- **Удалить:**
  - Личные конфиги (`config.yaml` → `config.example.yaml`)
  - Артефакты (GIF, лого старых версий, временные файлы)
  - Секреты (API ключи, прокси, OAuth токены)
- **Проверить:**
  ```bash
git grep -i "proxy\|secret\|token\|password" -- "*.py" "*.yaml" "*.md"
scripts/audit-secrets.sh
```

### 5. Тесты и хуки
- **Pre-commit:** ruff, black, pyright
- **Тесты:** `pytest tests/test_all.py` (минимум 75 тестов для v0.5.0)
- **Линтинг:** `ruff check .`

### 6. Публикация
```bash
gh repo create zad111ak-ai/harvest --public --source=. --remote=origin --push
git push origin main --tags
gh release create v0.5.0 --title "v0.5.0" --notes "## v0.5.0 — LLM Extraction + Enhanced Stealth..."
```


## Post-Publication Profile & Repo Polish

After initial publish, batch-polish all repos for discoverability:

### 1. Shields.io Badges (README)
Add at the top of each README, after the H1:
```markdown
[![Stars](https://img.shields.io/github/stars/OWNER/REPO?style=social)](https://github.com/OWNER/REPO)
[![Contributors](https://img.shields.io/github/contributors/OWNER/REPO)](https://github.com/OWNER/REPO)
[![Issues](https://img.shields.io/github/issues/OWNER/REPO)](https://github.com/OWNER/REPO)
[![PRs](https://img.shields.io/github/issues-pr/OWNER/REPO)](https://github.com/OWNER/REPO)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
```
For repos with CI: add `[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](...)`.

Batch workflow: update README → `git add -A && git commit` → push. Do all repos, then push all.

### 2. Enable GitHub Discussions
```bash
gh api repos/OWNER/REPO --method PATCH -f has_discussions=true
```
Works via REST API. Do for all repos in one pass.

### 3. Good First Issues
Create beginner-friendly issues to attract contributors:
```bash
gh issue create --repo OWNER/REPO --title "Title" --label "good first issue" --body "Description..."
```
Pick issues that are real features/fixes, not manufactured busywork. Keep descriptions clear and scoped.

### 4. Pinned Repos (Profile) — MANUAL ONLY
**⚠️ GitHub does NOT allow pinning repos via API** (REST or GraphQL). No mutation exists — tested `updateUserPinnedItems`, `updatePinnedItems`, `pinStarredRepository` — all undefined on Mutation type. The `addStar` mutation works for starring but does not pin.

**Only the web UI works:** go to profile → "Customize your pins" → select up to 6 repos.

Always flag this as a manual step for the user at the end of a batch setup.

## Pitfalls
- **PyPI token not configured:** workflow references `secrets.PYPI_API_TOKEN` but it may never have been set. One-time setup: `echo "pypi-TOKEN" | gh secret set PYPI_API_TOKEN -r OWNER/REPO`. Verify: `gh secret list --repo OWNER/REPO`. Re-run failed workflow: `gh run rerun <ID> --failed`.
- **Конфликт имён на PyPI:** если имя занято, использовать суффикс (`harvest-agent`)
- **Личные данные:** всегда проверять `.gitignore` и `git grep` перед пушем
- **Битые ссылки:** shields.io бейджи должны вести на обозреватели (solscan, etherscan, tonviewer)
- **SemVer:** increment 0.0.1 per release. v1.0.0 = full product readiness.
- **README:** живые примеры, сравнительные таблицы, крипто-донаты
- **Pre-commit hooks:** Run linter BEFORE committing to avoid auto-fix loops
- **Secret audit:** Always run `scripts/audit-secrets.sh` before push
- **Version consistency:** Update ALL version references (pyproject.toml, __init__.py, README badges, MCP server, tests)
- **ASCII art:** NEVER use box-drawing characters (╔═╗╦ ╦╦═╗ etc.) for ASCII art logos — they render misaligned/garbled on GitHub and many terminals, spelling wrong words. Always use standard ASCII: underscores, pipes, slashes (`|`, `/`, `\`, `_`). Example that works:
  ```
   _   _   ___   _   _  _____  ___   _   _
  | | | | / _ \ | \ | ||  ___|/ _ \ | \ | |
  | |_| |/ /_\ \|  \| || |_  / /_\ \|  \| |
  |  _  ||  _  || . ' ||  _| |  _  || . ' |
  | | | || | | || |\  || |   | | | || |\  |
  \_| |_/\_| |_/\_| \_/\_|   \_| |_/\_| \_/
  ```
  To generate: `pip install pyfiglet && python3 -c "import pyfiglet; print(pyfiglet.figlet_format('NAME', font='standard'))"` — or write by hand. **ALWAYS verify** by reading the art letter-by-letter before committing.
- **README full rewrite preservation:** When rewriting a README completely, FIRST make a checklist of ALL existing sections (donation badges, logo, comparison tables, feature lists, examples). NEVER drop existing content — the user will notice missing badges/logos. Diff old vs new before committing.
- **Donate badges in README:** User wants shields.io badges with crypto icons (BTC, ETH, USDT TON, SOL) — clickable, linking to blockchain explorers. These are PUBLIC addresses (safe to commit). Always include in open-source READMEs.
- **Donation methods:** Crypto wallets (BTC, ETH, USDT TON, SOL) + Ko-fi (accepts cards/PayPal/crypto). NO Boosty, NO card-only methods. Ko-fi is the accessible bridge for non-crypto users. If a repo has Boosty references, REMOVE them.
- **LICENSE file validation:** Before pushing, verify the LICENSE file contains actual MIT license text (`grep "MIT License" LICENSE`), not project description or other content. Files named `LICENSE` can contain project docs instead of the actual license.
- **Git diverged branches:** If `git push` fails with "diverged" or "behind its remote counterpart", use `git pull --no-rebase origin main` — NEVER `git pull --rebase` when conflicts exist. See [references/git-divergence-resolution.md](references/git-divergence-resolution.md).
- **`.pyc` files trigger false-positive pickle detection:** Some pre-commit hooks (e.g. security scanners) flag `.pyc` compiled bytecode files as "pickle usage detected". The fix: `git reset HEAD <file>.pyc` to unstage the `.pyc`, then commit. Better: add `*.pyc` to `.gitignore` so they're never staged in the first place.


## Release Cadence

User preference: increment by **0.0.1** per release. v1.0.0 = full product readiness.
- 0.6.2 → 0.6.3 → 0.6.4 → 0.7.0
- No breaking changes until v1.0.0

**Release checklist:**
```bash
# 1. Version bump (all files)
# Update pyproject.toml, __init__.py, README.md, tests, MCP server

# 2. Run full test suite
python3 -m pytest tests/test_all.py -x -q

# 3. Lint
ruff check harvest/

# 4. Commit + tag + push
git add -A && git commit -m "v0.6.X — description"
git tag v0.6.X
git push origin main --tags

# 5. GitHub release
gh release create v0.6.X --generate-notes
```


## References
- [references/bilingual-readme.md](references/bilingual-readme.md) — bilingual README template (rus+eng, language switcher, donation formats)
- [references/skill-repo-structure.md](references/skill-repo-structure.md) — структура skill/educational репозиториев (отличия от code package publishing)
- [references/semver-x5.md](references/semver-x5.md) — правила версионирования x.5
- [references/github-release-template.md](references/github-release-template.md) — шаблон релиза
- [references/donate-badges.md](references/donate-badges.md) — shields.io бейджи для криптовалют
- [references/iterative-release.md](references/iterative-release.md) — подробный разбор итеративного релиза (Harvest v0.5.0 case study)
