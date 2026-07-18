# Hacker News Publishing Guide

## Show HN — Best for Open-Source Projects

HN has a dedicated `show` page for "anything you've made": https://news.ycombinator.com/show

## Format

Show HN submission is dead simple:
- **Title:** `Show HN: Your Project – short description`
- **URL:** Your project's GitHub repo or landing page
- **Text (optional):** 1-3 lines max. HN prefers URL-only with brief context in the title.

## Key Rules

1. **Title must be honest and descriptive** — HN community despises clickbait
2. **No "Ask HN" or "Show HN"** if it's not your own project
3. **Repository must work** — people will clone and try it within minutes
4. **Be ready to answer questions** in comments for 24+ hours

## What Works (from HN front page analysis)

- **Short, descriptive titles** that explain the value: "I built a web scraper that fixes itself when websites change"
- **URL to GitHub** with a star-worthy README (screenshots, benchmarks, comparison table)
- **Honest limitations** section in README — HN upvotes honesty
- **Unique angle** — why this exists despite alternatives
- **Real code works** — first commenters will run `pip install` or `git clone`

## What Doesn't Work

- **Clickbait** — "This will change everything" → instant flagging
- **"We raised $X"** — Show HN is for makers, not startups
- **Landing pages without substance** — HN wants the actual project
- **Thin README** — first impression is the GitHub page
- **Asking for stars** — violates HN guidelines

## New Account Restrictions

**New HN accounts CANNOT submit URLs.** When trying to submit, you get:
```
Sorry, your account isn't able to submit this site.
```
This is an anti-spam measure. New accounts need karma/time before they can submit external links. Options:
- Wait and build karma by commenting on existing posts
- Ask a friend with established account to post for you
- Email hn@ycombinator.com to request URL submission ability
- Post as "Ask HN" instead (text-only, no URL restriction)

## Technical Access

**HN blocks via Cloudflare.** You cannot submit programmatically through the proxy (1082):
- `curl --proxy http://127.0.0.1:1082 news.ycombinator.com` → "Sorry."
- SOCKS5 (1081) — same result
- Scrapling/Playwright via browser — blocked
- HN API (https://github.com/HackerNews/API) is READ-ONLY — no write endpoints

**Only option: manual submission through a real browser** (phone or PC without proxy).

## Manual Steps

1. Open https://news.ycombinator.com/login in a real browser
2. Log in with your account
3. Open https://news.ycombinator.com/submit
4. Fill in:
   - **Title:** `Show HN: Harvest – open-source web scraper with self-healing parsers, semantic cache, MCP server`
   - **URL:** `https://github.com/zad111ak-ai/harvest`
5. Click submit

## After Submission

- Post goes to `/show` page (not `/newest`!)
- If it gets upvoted, it appears on the front page under `/show`
- Moderators may edit the title if it's misleading
- Respond to ALL comments — engagement keeps the post alive
- Post at US morning time (6-9 AM Pacific = ~3-6 PM Moscow) for max visibility

## Promotion Sequencing (Proven Order)

1. **Show HN first** — single best source of quality traffic for open-source
2. **Dev.to** — second, with more detailed article (link back to HN)
3. **X/Twitter** — short post with link to both HN + Dev.to
4. **Reddit r/Python** — if account works

## Platform Access Summary

| Platform | Programmatic? | Blocker | Workaround |
|----------|--------------|---------|------------|
| HN Show | No | Cloudflare + new accounts can't submit URLs | Manual (phone/real browser) |
| Dev.to | Partial | API creates drafts only, PUT publish unreliable | API for drafts → manual publish via web UI |
| X/Twitter | Yes | OAuth2 setup required | xurl with headless OAuth2 flow |
| Reddit | No | Bot detection, new account restrictions | Manual posting from phone |

## xurl OAuth2 Headless Flow (WSL2 / no browser)

When running on a headless server (WSL2, Docker, VPS), xurl can't open a browser. Use `--headless`:

```bash
# Step 1: Get auth URL (user opens on phone/another device)
xurl auth oauth2 --app <app-name> <username> --headless
# Output: "Open this URL in a browser on any device: https://x.com/i/oauth2/authorize?..."

# Step 2: User authorizes → browser redirects to localhost:8080/callback?code=...
# Page won't load (headless), but code is in the address bar

# Step 3: User pastes the code back
# xurl prompts for the code, user pastes it

# Step 4: Verify
xurl auth status
xurl whoami
```

**Pitfall:** The `--headless` flag is essential on WSL2. Without it, xurl tries to open a browser and times out.
