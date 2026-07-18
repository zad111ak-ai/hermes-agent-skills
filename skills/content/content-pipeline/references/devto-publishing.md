# Dev.to Publishing Guide

## API Overview
- `POST https://dev.to/api/articles` — create a draft or article
- `PUT https://dev.to/api/articles/{id}` — update a draft (change title, body, or publish it)
- Auth: `api-key: <key from dev.to/settings/account>` (NOT OAuth, NOT Bearer)
- Accept header: `Accept: application/vnd.forem.api-v1+json`
- Always route through Hysteria proxy: `--proxy http://127.0.0.1:1082`
- SOCKS5 (1081) **does not work** with dev.to — connections reset. Use HTTP proxy (1082).

## CRITICAL: `published: true` on POST is IGNORED

**This is the single most important thing to know:**
- `POST /api/articles` with `published: true` in the JSON body **silently ignores the flag** and always creates a draft (unpublished).
- This is NOT documented but is the real behavior. The API responds with `"published": None` regardless.
- `/api/articles/{id}/publish` endpoint does NOT exist (returns 404).
- The `/api/articles/me/all` endpoint does exist to list published articles.

### How to actually publish:
1. POST to create the draft → get `id` from response
2. PUT `/api/articles/{id}` with `published: true`:

```bash
curl -sL --proxy http://127.0.0.1:1082 -X PUT \
  "https://dev.to/api/articles/{id}" \
  -H "api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"article":{"title":"...","body_markdown":"...","published":true}}'
```

- Once published, the final URL is: `https://dev.to/{username}/{slug}`

### PUT may also fail (observed in practice)
Even PUT with `published: true` sometimes returns `published: None`. Common causes:
- **Same title used recently** — API returns 422 "Title has already been used". Change the title slightly.
- **Duplicate drafts** — creating multiple drafts with similar titles causes conflicts. Delete old drafts first.
- **Rate limiting** — rapid create/update cycles may silently fail

**Fallback: publish manually through Dev.to web UI.**
1. Go to https://dev.to → Dashboard → Posts
2. Click the draft → Edit → Publish

## Request Format

POST with full article:
```json
{
  "article": {
    "title": "...",
    "body_markdown": "---\ntags: tag1, tag2, tag3, tag4 (max 4)\n---\n\nContent in markdown...",
    "tags": ["tag1", "tag2", "tag3", "tag4"]
  }
}
```

PUT to publish an existing draft — add `"published": true`:
```json
{
  "article": {
    "published": true
  }
}
```

PUT full update (change title/body AND publish in one call):
```json
{
  "article": {
    "title": "...",
    "body_markdown": "...",
    "tags": ["...", "...", "...", "..."],
    "published": true
  }
}
```

## Important Notes
- Tags: max 4, must match existing Dev.to tags (case-insensitive, lowercase is safe)
- Body markdown starts with YAML frontmatter `---\ntags: ...\n---`
- The API may return `temp-slug` for drafts — that's fine, final slug appears after publish
- `published: None` in response means draft; `published: "2024-..."` timestamp = published
- Reading time: 2-4 min ideal for Dev.to (IMPORTANT: keep body concise)

## Content Research Methodology

**Before writing a Dev.to post, study what works on the platform:**

1. Search `dev.to/t/showdev` — filter by top/month for recent successful showdev posts
2. Analyze top articles for: title structure, formatting, code snippets, tags, length
3. Patterns that work on Dev.to (from analysis of top showdev / open-source announcement posts):
   - **Personal story opening** — "I spent X building Y because Z was broken"
   - **Honest comparison tables** — feature matrix vs. alternatives (works VERY well)
   - **Code snippets** — Dev.to audience reads code, show real examples
   - **Limitations section** — trust builder, not weakness
   - **showdev tag** — essential for open-source announcements
   - **Reading time: 2-6 min** ideal (8+ min only for deep tutorials)
   - **Headers: problem intro → features → comparison → limitations → quick start**

## Content structure that works (validated):

```
--- tags: python, opensource, webscraping, showdev ---

I spent [time] building [tool] because [problem].

## The problem
What's broken, what you tried, why existing solutions don't work.

## Features
- **Feature 1** — concise description. Code example.
- **Feature 2** — concise description. Code example.
- Feature 3, Feature 4...

## Comparison with alternatives
| Feature | My Tool | Alternative A | Alternative B |
|---|---|---|---|
| Key feature 1 | Yes | No | Paid |
| Key feature 2 | Yes | No | No |

## Honest limitations
- What it doesn't do well
- What's new/beta about it
- What dependencies it needs

## Quick start
```bash
# 3-4 lines of setup
```

MIT / GitHub link.
```

## What to avoid
- **Clickbait titles** — Dev.to community is experienced, they can smell it
- **Over-promising** — be honest about limitations, it builds trust
- **"Please star on GitHub"** appeals — let the post speak for itself
- **Wall of text** — use headers, bullet points, code blocks
- **Too many features listed without code** — Dev.to audience wants to see real usage
- **More than 4 tags** — API rejects >4
- **Same title within 5 minutes** — API returns 422 "Title has already been used"

## Technology Stack
- Python script writing JSON to stdin via `subprocess.run(cmd, input=data)`
- curl for the actual HTTP call (simplest, no Python HTTP client quirks)
- Harvest is NOT used for API calls — only for data collection / web research
- Always route through Hysteria proxy

## API Key
- Stored in memory: generated from dev.to → Settings → Account
- Key is static, permanent
