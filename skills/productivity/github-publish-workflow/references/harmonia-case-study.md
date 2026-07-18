# Harmonia Case Study — Loop Collector & Optimizer

Full workflow from niche discovery → naming → build → publish → verify.

## 1. Niche Discovery

**Pain point:** LLM agent loops (reflection, self-correction, RAG) are invisible. Users have no tool to see what their agent is actually doing across multiple calls — how many correction cycles, which models used, time per iteration.

**Existing solutions research:**
- langfuse (31K⭐) — LLM observability platform, cloud/SDK
- opik (21K⭐) — debug, evaluate, monitor LLMs
- promptfoo (23K⭐) — prompt testing/red-teaming
- plany (6.7K⭐) — AI-native proxy
- claude-tap (2.5K⭐) — Claude Code traffic intercept

**Gap identified:** No CLI tool that:
- Works as a transparent proxy between agent and API
- Builds a graph of call chains with correction loops highlighted
- Gives actionable optimization recommendations
- Stores everything locally (no cloud)
- Works with ANY OpenAI-compatible API (not tied to a provider)

**Selection criterion:** "решает много головных болей за раз" — Harmonia solves: debugging agents, visualizing call chains, detecting inefficiency, optimizing costs, understanding agent behavior. All with one command.

## 2. Naming & Identity

**Candidates considered:** looppulse, cyclens, loopgate, loopkit, traceflow, roundtrip

**Chosen:** Harmonia — from Greek Ἁρμονία (harmony, joint, agreement). Three interlinked loops as visual motif. The name evokes balanced, efficient cycles — the tool brings harmony to LLM agent loops.

**Name uniqueness check:**
```bash
gh search repos "harmonia" --sort stars -L 5 --json name,stargazersCount
```
Result: only non-English music-related repos. Clean for an AI tool.

**Logo:** SVG with three intertwined rounded-corner loop paths in sky-blue to purple gradient on dark background. Minimalist, no text, works at small size.

## 3. Architecture

```
harmonia/
├── harmonia           # CLI entrypoint (shebang python3)
│   └── subcommands: track, proxy, optimize, viz, sessions, models
├── logo.svg           # Project identity
├── README.md          # English-only docs
├── .env.example       # API_BASE_URL with fallback ports
├── .gitignore         # secrets, *.db, .env
├── pyproject.toml     # hatchling build
└── .github/
    └── workflows/
        ├── ci.yml       # test on push/pr
        └── release.yml  # auto-release on tag
```

**Key design decisions:**
- Single-file CLI (easy to install: `pip install harmonia` or just copy one file)
- SQLite local storage at `~/.harmonia/harmonia.db` — no cloud dependency
- Universal API: user sets `API_BASE_URL` in `.env`, works with any OpenAI-compatible endpoint
- Mermaid graph output — renders in GitHub, Obsidian, or any Markdown viewer
- Detects correction loops algorithm: same prompt + same model within short time window = loop

## 4. Implementation Details

**Loop detection algorithm:**
1. Group calls by session
2. Within session, look for sequences: Call A (prompt X, model M) → Call B (different) → Call C (prompt X, model M again)
3. Flag as correction loop when same prompt → model pair appears with ≤2 different calls in between
4. Track: total calls, loops found, wasted tokens estimate, time saved recommendation

**Proxy mode concept:** Acts as MITM between agent and API server. All requests/responses logged to SQLite. Optimize command then analyzes the full session.

## 5. Verification

After publishing, ran `/tmp/hermes-verify-harmonia.py`:

| Check | Result |
|-------|--------|
| CLI --version | ✅ |
| harmonia track | ✅ Creates session |
| harmonia sessions | ✅ Lists sessions |
| SQLite has data | ✅ 8+ calls stored |
| harmonia optimize | ✅ Analyzes loops |
| harmonia viz | ✅ Mermaid output |

Cache was populated by `simulate.py` which generated 8 calls with 2 correction cycles.

## 6. Publishing Timeline

```
14:00 — Concept & niche research
14:15 — Logo design (SVG)
14:30 — CLI implementation (harmonia subcommands)
15:00 — Simulation data & test
15:15 — README & config files
15:20 — git init → gh repo create → push
15:22 — tag v0.1.0 + gh release create
15:25 — Verification script run (6/6 pass)
```

## 7. Lessons Learned

- **Universal API is non-negotiable** — user explicitly rejected provider lock-in. Always `.env`-configurable `API_BASE_URL`.
- **Niche first, code second** — research existing solutions thoroughly. If 3+ alternatives exist with 1K+ stars, find a narrower angle.
- **Logo sets tone** — took 15 minutes but makes the repo look professional. Always include one.
- **Ad-hoc verification catches post-publish issues** — simulate real usage, don't just check imports.
- **Simple CLI with subcommands** beats complex API — `harmonia track`, `harmonia optimize`, `harmonia viz` is intuitive and easy to document.
