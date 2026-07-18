# Telegram Tutorial Series — Workflow & Templates

## Overview

Educational multi-post series published on a Telegram channel, distributed through scheduling bots like @Wb_daybot. Designed for Russian-speaking tech beginners. Key principle: **reduce barrier to entry to absolute minimum**.

## Audience Profile

- Russian-speaking, Windows users (vast majority)
- Non-technical or semi-technical (heard about AI, want to try)
- Zero budget or minimal ($0-5 for API)
- Skeptical of "infobiznes" and paid courses
- Want copy-paste ready commands, not theory

## Series Structure (6-post template)

```
Post 0: MANIFEST — "Зачем вам это" + cost comparison (free vs paid)
Post 1: PREPARE — 3 critical pre-requisites (most people fail here)
Post 2: INSTALL CORE — Step-by-step with copy-paste commands
Post 3: INSTALL MAIN TOOL — The actual product/setup
Post 4: SHORTCUT — Helper tool that does the hard part automatically
Post 5: TROUBLESHOOT — Error handling + free AI tech support
Post 6: WHAT NEXT — Real use cases + monetization hints
```

### Post count rationale
- 6 posts = ~1 week of daily content
- Short enough to not lose attention
- Long enough to be comprehensive
- Each post standalone (can be read in any order, but flows sequentially)

## Writing Rules

### Language
- **Russian** for all body text
- **Latin** for tool/service names: Hermes Agent, WSL 2, Node.js, MiMo Code, OpenRouter, Claude, ChatGPT
- NEVER transliterate: ❌ "Чат-ДжиПиТи" ✅ "ChatGPT"
- Short sentences. One idea per sentence.

### Structure per post
```
📌 Title: [Hook or clear description]

🔧 Series tag: "Локальный AI-агент своими руками" — Пост N/6

[1-2 sentence intro — what this post covers]

⚠️/🔧/💡 Section with clear emoji marker
[Content]

✅ Чек-лист or summary at end
👉 Teaser for next post
```

### Formatting for Telegram
- Use `**bold**` for key terms and warnings
- Use ``` for code blocks (single backtick for inline commands)
- Use bullet points (• not —)
- Use ✅ ❌ ⚠️ 🔧 💡 📌 🎯 emojis as visual anchors
- Max ~2000 chars per post (Telegram message limit)
- Code blocks should be individually copy-pasteable

### Beginner-friendly principles
1. **Every command** should be copy-paste ready
2. **Every step** should say what to EXPECT (output, behavior)
3. **Every error** should have a quick fix
4. **Never assume** the reader knows what a terminal is
5. **Always mention** that "password not showing while typing is normal"
6. **Always mention** free AI help (DeepSeek, Gemini, Claude free tier) for troubleshooting
7. **Mention Ctrl+Shift+C/V** for WSL clipboard — non-obvious, catches 90% of beginners

### Content checklist per post
- [ ] Command blocks are complete and tested
- [ ] Expected output described
- [ ] Error scenarios covered
- [ ] Link/teaser to next post
- [ ] No untranslated English jargon without explanation
- [ ] Under 2000 chars

## Publishing Workflow

### Via @Wb_daybot
1. Copy post text from markdown file
2. Strip markdown headers (# title) and horizontal rules (---)
3. Send to @Wb_daybot
4. Set schedule: 1 post/day at 19:00 (peak Telegram activity in RU)
5. Repeat for each post

### Distribution
- Post announcements in 3-5 relevant Telegram chats
- Cross-post first post to IT/tech channels
- Pin series announcement on channel

## Series Topics That Work

Based on user's experience:
- **AI agent setup** (Hermes, local LLMs, automation)
- **Free tools replacing paid SaaS** (n8n vs Make.com, local AI vs cloud)
- **Russian-specific tech** (payment methods, VPN-free tools, local services)
- **Privacy/security** (local AI vs cloud data leaks)

## Anti-patterns (don't do these)

- ❌ Long paragraphs without structure
- ❌ Assuming user knows什么是WSL
- ❌ Untranslated technical jargon
- ❌ Commands without expected output description
- ❌ "Just google it" — give specific free AI troubleshooting steps
- ❌ Selling courses or paid consulting in the series (save for later)
- ❌ More than 6 posts in a series (attention span drops)
