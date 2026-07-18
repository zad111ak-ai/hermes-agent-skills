# Telegram Bot API — Programmatic Channel Publishing

## Overview

Publish posts with images to Telegram channels via Bot API (`sendPhoto`). 
Script: `publish_posts.py` in project root.

## Token Discovery

Multiple env vars checked in order:
1. `WB_DAYBOT_TOKEN` (primary — @Wb_daybot)
2. `SCAM_BOT_TOKEN` (fallback)
3. `.env` file in project root (`WB_DAYBOT_TOKEN=...`)

Verify token: `GET /bot{token}/getMe` → should return `ok: true` with bot info.

## Prerequisites

1. Bot must be **admin** in the channel with "post messages" permission
2. Channel must have **comments** enabled (for engagement)
3. Bot token must be in env or `.env`

## Key API Limits

| Parameter | Limit | Workaround |
|-----------|-------|------------|
| `sendPhoto` caption | **1024 chars** | Split: photo with short caption + separate `sendMessage` for full text |
| `sendMessage` text | **4096 chars** | Split into multiple messages |
| Rate limit | ~30 msg/sec (global) | 1.5s delay between posts (conservative) |
| File size (photo) | 10 MB | Compress if needed |

## Long Text Splitting Strategy

When post text > 1024 chars (common for educational posts):
1. Send photo with truncated caption (first 1000 chars + "...")
2. Wait 1.5s
3. Send full text as separate `sendMessage` with `disable_web_page_preview: true`

This preserves the visual hook (image) while delivering complete content.

## Chat ID Discovery

Bot's `getUpdates` returns empty until bot has interacted with a chat. Methods:
- **Forward** a message from the channel to the bot → extract `chat.id` from update
- **@username**: use `@channel_name` directly as `chat_id` in API calls
- **getUpdates** after adding bot as admin + posting once → channel appears

Format: `chat_id` can be `@channel_username` or numeric `-100XXXXXXXXXX`

## Script Usage

```bash
# Discover channels (requires at least one update)
python3 publish_posts.py --discover

# Dry run (preview without sending)
python3 publish_posts.py --channel @my_channel --dry-run

# Publish all posts
python3 publish_posts.py --channel @my_channel

# Publish single post
python3 publish_posts.py --channel @my_channel --post 3
```

## Post File Convention

```
content/series_<name>/
├── 00_manifest.md      # Post text (markdown)
├── 01_prepare.md
├── ...
├── images/
│   ├── post0_manifest.jpg  # Image for each post
│   ├── post1_bios.jpg
│   └── ...
```

The script strips image reference lines from post text before sending.

## Pitfalls

1. **`async def` without `await`** — Python silently returns coroutine object, no error. 
   `RuntimeWarning: coroutine was never awaited`. Always define publish functions as 
   regular `def` unless actually using async HTTP.

2. **`sendPhoto` caption > 1024 chars** → Telegram returns 400 Bad Request. 
   Always check `len(text)` before sending.

3. **Bot not admin** → `sendPhoto` returns "not enough rights" or "chat not found". 
   Verify bot is admin with correct permissions.

4. **Markdown parsing errors** — Telegram's Markdown parser is strict. 
   Unclosed `**`, backticks in wrong places, or special chars (`_`, `*`, `` ` ``) 
   inside code blocks can break parsing. Test with dry-run first.

5. **Webhook blocks getUpdates** — if a webhook is set, `getUpdates` returns empty. 
   Check with `getWebhookInfo` and delete webhook if needed: `DELETE /bot{token}/webhook`.

6. **httpx picks up HTTP_PROXY from env** — when calling Telegram API locally, 
   use `httpx.Client(trust_env=False)` or explicit `proxies=None` to avoid 
   routing through Hysteria proxy unnecessarily.

## Ad-Hoc Verification Pattern

For scripts without canonical test suites:
1. Create `/tmp/hermes-verify-<name>.py`
2. Test: import, config, file existence, key functions, token validity
3. Run and verify all pass
4. Clean up temp file

```python
#!/usr/bin/env python3
"""Ad-hoc verification"""
import sys
sys.path.insert(0, "/path/to/project")

# Import check
import my_module
print("✅ import: OK")

# Config checks
assert my_module.CONSTANT == expected_value
print("✅ config: OK")

# File existence
from pathlib import Path
assert Path("expected/file.txt").exists()
print("✅ files: OK")
```
