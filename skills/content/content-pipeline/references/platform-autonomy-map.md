# Platform Autonomy Map — What the Agent Can Do Without User

Generated from session experience (July 2026). Use when planning content promotion.

## Tier 1: Fully Autonomous (no user interaction needed)

| Channel | Tool | What works | Notes |
|---------|------|------------|-------|
| GitHub Release | `gh` CLI | Create/edit releases, set body, add assets | Gets indexed by search engines, appears in repo feed |
| GitHub Issues | `gh` CLI | Create, label, assign | For tracking, not promotion |
| Dev.to Draft | `curl` + API key | Create draft articles | API `published: true` on POST is IGNORED. PUT to publish is unreliable. See devto-publishing.md |
| Dev.to Publish | Scrapling/Playwright | Publish draft via web UI | Fallback when API PUT fails |

## Tier 2: Requires One-Time Manual Setup

| Channel | Setup needed | Then autonomous? | Blocker |
|---------|-------------|-------------------|---------|
| X/Twitter | OAuth2 via xurl (user opens URL on phone) | Yes, once tokens are set | Tokens expire, need refresh (auto-refresh works) |
| Dev.to (full publish) | API key from settings | Partial — drafts yes, publish via API flaky | PUT with `published: true` sometimes fails silently |

## Tier 3: Manual Only (no programmatic access)

| Channel | Why manual | Workaround |
|---------|-----------|------------|
| HackerNews | Cloudflare blocks proxy + new accounts can't submit URLs | Real browser on phone/PC |
| Reddit | Bot detection, new accounts restricted | Manual posting |
| Lobsters | Needs account + manual submit | Manual |
| ProductHunt | Needs maker account + manual submit | Manual |

## Promotion Sequence for Open-Source Projects

Based on what actually worked:

1. **GitHub Release** — autonomous, immediate, indexed by Google
2. **Dev.to article** — API draft + manual publish (or Scrapling automation)
3. **Show HN** — manual but highest quality traffic
4. **X/Twitter** — short post with links (needs OAuth2 setup)
5. **Reddit r/opensource, r/Python** — manual posting

## Dev.to Tag Popularity (Week of July 14, 2026)

Research via Dev.to API `?top=7` (reactions across top 10 articles per tag):

| Tag | Total Reactions | For Harvest? |
|-----|----------------|--------------|
| `ai` | 405 | ✅ primary |
| `webdev` | 358 | ⚠️ secondary |
| `showdev` | 286 | ✅ essential for project showcases |
| `opensource` | 169 | ✅ primary |
| `agents` | 118 | ✅ Harvest is an AI agent tool |
| `llm` | 107 | ✅ Harvest uses LLM |
| `devops` | 92 | ⚠️ if targeting devops audience |
| `python` | 61 | ✅ Harvest is Python |
| `rag` | 43 | ⚠️ Harvest supports RAG use cases |
| `mcp` | 38 | ✅ Harvest is MCP server |
| `automation` | 30 | ⚠️ secondary |

**Recommended tags for Harvest:** `ai`, `opensource`, `llm`, `mcp` (4 max on Dev.to)

**Tag research method:**
```bash
for tag in "ai" "llm" "python" "opensource" "agents" "mcp" "showdev"; do
  curl -sL --proxy http://127.0.0.1:1082 \
    "https://dev.to/api/articles?tag=$tag&top=7&per_page=10" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(f'$tag: {len(d)} articles, {sum(a.get(\"public_reactions_count\",0) for a in d)} reactions')"
done
```
