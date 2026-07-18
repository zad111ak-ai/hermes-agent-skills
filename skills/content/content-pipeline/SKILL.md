---
name: content-pipeline
description: End-to-end content creation from idea to monetization.
version: 1.0.0
author: Dima
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [content, automation, monetization, video, blog, social-media]
    category: content-creation
    config:
      content.default_niche: "Your content niche"
      content.youtube_channel: "YouTube channel name"
      content.tg_channel: "Telegram channel link"
---

# Content Pipeline Skill

Automated content creation from idea to publication across all platforms.

## When to Use

- User asks to create, generate, or publish content
- Scheduled content generation tasks
- Research trending topics and create content around them
- Repurpose existing content across platforms

## Prerequisites

- `yt-dlp` installed (`pipx install yt-dlp`)
- `ffmpeg` available at `/home/dima/bin/ffmpeg`
- `moviepy` Python package (в venv при PEP 668 — `python3 -m venv venv && venv/bin/pip install moviepy`)
- `pillow` Python package
- Telegram bot token configured in `.env`
- Python 3.14+ с PEP 668: используй `pip install --user` или `venv` для пакетов

## Content Types Supported

### 1. Short-form Video (YouTube Shorts, TikTok, Instagram Reels)
Pipeline: Idea → Script → TTS → Visuals → Subtitles → Video → Upload

### 2. Blog Posts / Articles
Pipeline: Research → Outline → Write → SEO → Publish

### 3. Telegram Posts
Pipeline: Topic → Write → Format → Post to channel

**Manual:** @Wb_daybot scheduling bot. See `references/telegram-tutorial-series.md` — 6-post template with beginner-friendly writing rules.

**Programmatic (Bot API):** `publish_posts.py` — publishes posts with images directly via Telegram Bot API. Handles sendPhoto caption splitting (1024 char limit), rate limiting, and dry-run mode. Requires bot as channel admin. See `references/telegram-bot-api-publishing.md` for API limits, pitfalls, and usage.

### 4. Image Content (Instagram, Pinterest)
Pipeline: Idea → Generate/Design → Caption → Post

### 5. Thread Content (X/Twitter)
Pipeline: Topic → Research → Thread draft → Post

## Procedure

### Step 1: Research Trends
```
1. Use web_search to find trending topics in the niche
2. Check competitor content via web_extract
3. Identify high-engagement formats
```

### Step 2: Generate Script/Content
```
1. Create outline based on research
2. Write full script with hooks and CTAs
3. Add monetization touchpoints (affiliate links, product mentions)
```

### Step 3: Create Visuals
```
For AI video (priority — «кровь из носа»):
  - **OmniRoute video models** (порт 3000) — Veo, WAN, Pollinations (требуют Hysteria прокси)
  - **Hugging Face Spaces** — Stable Video Diffusion, LTX-Video, Instant-Video (бесплатные GPU)
  - **Gemini AI Studio** → Veo 2 (1500 запросов/день, 3 аккаунта)
  - **Pipeline v3** — `~/.hermes/tools/pipeline.py` — слайд-шоу из Pollinations картинок + TTS + субтитры + Ken Burns.
    - **Кадры:** тёмные градиенты + glow-эффекты + крупный текст (Pillow), каждый с уникальной Pollinations-иллюстрацией
    - **Ken Burns zoompan** — замена `loop+setpts` на `zoompan`:
      ```
      [{i}:v]scale=2160:-2:force_original_aspect_ratio=increase,\
      crop=2160:3840,\
      zoompan=z='1.0+0.0003*on':d={seg_frames}:x='iw/2-(iw/zoom/2)':\
      y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[z{i}]
      ```
      Метки выхода — `[z0]`, `[z1]`, ... (а не `[v{i}]`), чтобы передать их в xfade цепочку.
    - **Чётные кадры** — zoom in (z=1.0→1.1 за ~10с), **нечётные** — панорамирование влево/вправо + лёгкий зум
    - **2x resolution** для zoompan (2160×3840), zoompan ресайзит обратно в 1080×1920 → без пикселизации при зуме
    - **Crossfade между кадрами (xfade)** — плавные переходы вместо резких стыков. Цепочка: `[z0][z1]xfade=transition=fade:duration=...:offset=...[f1];[f1][z2]xfade=...`. Метки: `f1`, `f2`, ..., последний → `vid`. Формула offset: `offset_frames = i * (seg_frames - fade_duration)`, где `i` — номер перехода (1-based), `fade_duration` ~ 30 кадров/1с. Пример: `[z0][z1]xfade=transition=fade:duration=1.00:offset=5.17[f1];[f1][z2]xfade=transition=fade:duration=1.00:offset=10.33[vid]`.
    - Детали xfade: `references/crossfade-xfade.md`
    - **Голос:** мужской — `ru-RU-DmitryNeural` (русский) / `en-US-GuyNeural` (английский)
    - **Скрипт:** названия сервисов пишутся **латиницей** (ChatGPT, Midjourney, Claude, Veo 2) даже в русскоязычном тексте
    - **Субтитры:** Whisper (`faster-whisper`) → `fix_subtitle_text()` — словарь замен для AI-моделей (см. раздел Subtitle Correction)
    - `httpx.AsyncClient(trust_env=False)` — HTTP_PROXY из env перехватывает локальные запросы к OmniRoute
    - OmniRoute возвращает SSE (`data: {...}`, `data: [DONE]`) даже при `stream: false`
    - Детали zoompan: `references/ken-burns-zoompan.md`
  - Полные детали всех подходов: `references/free-video-sources.md`

For slideshow/background video:
  - Use pillow to create title cards and thumbnails
  - Use moviepy to compose video from clips
  - Add TTS voiceover via faster-whisper (for STT) or external TTS
  - Add subtitles using ffmpeg ASS/SRT
  - **Backgrounds:** Pollinations free image API (бесплатно, без ключа) или Pexels API (200 req/h free) или gradient (offline)

  **Pollinations free image (для кадров в pipeline.py):**
  - Эндпоинт: `https://image.pollinations.ai/prompt/{url_encoded_prompt}`
  - Старый `pollinations.ai/p/` больше НЕ РАБОТАЕТ (возвращает HTML вместо JPEG)
  - Формат: JPEG (первые 2 байта `\\xff\\xd8`), ~85‑170 KB
  - Через Hysteria прокси: `httpx.Client(proxy='http://127.0.0.1:1082')`
  - Rate limit: **~1 req / 7 sec** (429 при быстрее) → `time.sleep(7)` между запросами
  - Таймаут: 45+ секунд (иногда долго генерирует)
  - Валидация: проверять `status_code == 200 and len(content) > 1000`
  - **ПРОМПТ: НИКАКИХ ЛЮДЕЙ И ЛИЦ.** Генерация лиц у Pollinations даёт криповые/уродливые результаты. Всегда явно указывать в промпте: `no people, no faces, no characters — only abstract futuristic technology background, holographic UI, glowing circuits, data streams, sci-fi interface style, octane render`. Без этого — гарантированный nightmarish результат. Если промпт обрезается по длине — первым удалять упоминания людей/персонажей, последним — ключевые техно-слова (glowing, circuits, holographic).
  - Длина промпта: до ~200 символов (при обрезке сохранять суть: техно-арт, без людей)
  - Детали: `references/free-image-sources-pollinations.md`
  - Pollinations не требует регистрации, ключа или cookie — нулевой риск блокировки

For images:
  - Generate with ComfyUI skill or pillow
  - Add text overlays, branding
  - **Free gen:** doubao2api, imageFX-api (см. free-visual-sources.md)

- **Ресурсы:**
  - `references/free-visual-sources.md` — стоковые видео-фоны, изображения (Pexels, doubao2api, imageFX-api)
  - `references/free-video-sources.md` — AI генерация видео (OmniRoute, HF Spaces, Gemini Veo 2, Pipeline 2.0)
  - `references/video-models-omniroute.md` — 31 видео-модель в OmniRoute (Veo, WAN, Seedance, Grok Video Pro), тесты и риски
  - `references/content-pipeline-tools-landscape.md` — обзор GitHub репозиториев для контента (сравнение, звёзды, совместимость со стеком), методология self-improving loop (LLM-as-a-judge, A/B тестирование, analytics-driven feedback)

### Step 4: Publish
```
For Telegram:
  - Use Telegram bot API (already configured)
  - Send to channel with media

For YouTube:
  - Use YouTube Data API v3 (needs API key)
  - Upload with metadata

For X/Twitter:
  - Use xurl skill (already installed)

For Dev.to:
  - Full article: POST /api/articles with api-key and Accept header to create a draft
  - CRITICAL: `published: true` on POST is IGNORED by the API — always creates a draft
  - To publish: PUT /api/articles/{id} with `published: true` in the body
  - Auth: api-key from dev.to settings, NOT OAuth
  - Always route through Hysteria HTTP proxy (http://127.0.0.1:1082) — SOCKS5 (1081) resets
  - Python+curl pipe via file (JSON to stdin) — Harvest is NOT used for API calls
  - Before writing: study top Dev.to articles in t/showdev for patterns. See references/devto-publishing.md for full workflow.
  - Detailed API reference: references/devto-publishing.md

For Reddit:
  - Post strategy: honest approach, no clickbait, genuine value
  - Cross-post sequencing: opensource/selfhosted first → programming later
  - Detailed guide: references/reddit-post-strategy.md

For GitHub Releases:
  - Fully autonomous — `gh release create` / `gh release edit`
  - Gets indexed by search engines immediately
  - Good fallback when all social channels need manual auth
  - Include feature highlights, benchmarks, and donation links in body

For Hacker News:
  - Show HN — best single source for open-source projects
  - HN blocks via Cloudflare — no programmatic access through proxy
  - Manual submission required (phone or real browser)
  - Format: `Show HN: Project – description` + URL to GitHub
  For X/Twitter:
    - Use xurl skill (already installed)
    - Short honest post with link to GitHub

  For Hacker News (Show HN):
    - Best for open-source projects — highest quality traffic
    - Submit via https://news.ycombinator.com/submit
    - Format: `Show HN: Harvest – open-source web scraper with self-healing parsers, semantic cache, MCP server`
    - URL: GitHub repo
    - Manual only — Cloudflare blocks programmatic access
    - **New accounts cannot submit URLs** — need karma or email hn@ycombinator.com
    - HN API is READ-ONLY — no write endpoints
    - Detailed guide: references/hackernews-publishing.md

 **Full platform autonomy map:** references/platform-autonomy-map.md

 For X/Twitter:
   - Use xurl skill (already installed)
    - Short honest post with link to GitHub
    - On headless/WSL2: use `xurl auth oauth2 --app <name> <user> --headless` for OAuth
    - Detailed guide: references/hackernews-publishing.md (xurl section)
  ## Step 5: Track Performance

```
1. Log published content to ~/content_output/tracker.json
2. Track views, engagement per platform
3. Report weekly via cron
```

### Step 6: Self-Improving Quality Loop (LLM-as-a-Judge)

Цель: каждый следующий ролик качественнее предыдущего. Не публиковать до оценки.

```
1. LLM-as-a-Judge: после генерации отправить метрики (длительность, кол-во кадров, score от LLM) на оценку через OmniRoute
   - Критерии: качество визуала, читаемость субтитров, плавность переходов, вовлекающий hook, синхронизация аудио/видео
   - Score 0-10. Если < 7 — корректировать промпты и перезапустить
   - Если >= 7 — публиковать и записать в историю

2. Хранить историю: ~/content_output/quality_history.json (50 последних записей)

3. A/B варианты: если время позволяет — генерировать 2 варианта скрипта/промпта, выбирать лучший по LLM-judge

4. Analytics feedback: после публикации (когда появятся просмотры/удержание) — учитывать что сработало для следующего цикла

Детали: references/content-pipeline-tools-landscape.md (раздел Self-Improving Loop)

## Quick Reference Commands

```bash
# Download video for remixing
yt-dlp -f "best[height<=720]" -o "%(title)s.%(ext)s" <URL>

# Extract audio for TTS reference
ffmpeg -i input.mp4 -vn -acodec pcm_s16le audio.wav

# Create short video from images
ffmpeg -framerate 1 -i img%d.png -c:v libx264 -pix_fmt yuv420p output.mp4

# Add subtitles to video
ffmpeg -i video.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24'" output.mp4

# Resize for vertical (9:16)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" -c:v libx264 vertical.mp4
```

## Pitfalls

- YouTube API requires OAuth2 setup — not just API key
- Instagram blocks automation — use sparingly, add delays
- Telegram has 50MB file size limit for bots — compress if needed
- Always add your watermark/branding to content
- Track which content performs best to double down on winners
- **httpx.AsyncClient** подхватывает `HTTP_PROXY`/`HTTPS_PROXY`/`http_proxy` из env без спроса. При работе через локальный сервис (OmniRoute на localhost) всегда передавать `trust_env=False` или `proxies=None` при создании клиента. Иначе запросы валятся в прокси, а не на localhost.
- **ffmpeg concat** с `-c:v copy` НЕ работает для PNG-кадров — нет keyframe для стрим-копи. Решение: использовать **filter_complex loop+concat** — каждый PNG лупится N раз (`loop=N:1:0,setpts=N/30/TB`), scale+pad в фильтре, concat в конце. Пример: `[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,loop=240:1:0,setpts=N/30/TB,format=yuv420p[v0]` + `[v0][v1]...[vN]concat=n=N:v=1:a=0[vid]`. Работает без segfault и без промежуточных файлов.
- **OmniRoute** возвращает SSE (`data: {...}`) даже при `stream: false`. Парсер должен искать `data: ` префиксы, а не просто голый JSON в теле ответа.
- **fact_store — agent tool, не Python модуль.** В скриптах (pipeline.py, deerflow, и т.д.) НЕЛЬЗЯ импортировать `from hermes_tools_lib import fact_store` или `from fact_store import fact_store` — этих модулей нет. Для логирования из скриптов используй `knowledge_base` (есть как модуль) или пиши в `~/content_output/tracker.json`. Hermes-агент записывает в fact_store через свой встроенный tool.
- **Research before acting.** Если задача новая или неочевидная — сначала `web_search`/`web_extract`, потом команды. Не тыкать случайными командами. «По смыслу почему не ищешь» означает: сначала изучи, потом делай.
- **Edge-TTS** на русском: предпочтительный голос **ru-RU-DmitryNeural** (мужской, естественнее женского SvetlanaNeural). На английском — **en-US-GuyNeural**. Устанавливать `edge-tts` через pip.
- **Скрипт:** названия сервисов, инструментов и AI-моделей всегда писать **латиницей** (ChatGPT, Midjourney, Claude, Veo 2, Suno, FLUX), даже в русскоязычном тексте. Не транслитерировать («Чат-ДжиПиТи», «Мижурни»).
- **Subtitle Correction (Whisper→Latin):** Whisper (`faster-whisper`) транскрибирует английские названия AI-моделей как русские近似жения («дип сик» → DeepSeek, «люма» → Luma). Обязательно применять `fix_subtitle_text()` — словарь замен:
  ```python
  replacements = {
      "чат джи пи ти": "ChatGPT",
      "дип сик": "DeepSeek",
      "люма": "Luma", "люмы": "Luma", "люме": "Luma", "люму": "Luma",
      "люма дреам машин": "Luma Dream Machine",  # и все падежные варианты
      "соpa 2": "Sora 2",
      "опен ай": "OpenAI",
      "миджорни": "Midjourney",
      "стабил дифьюжн": "Stable Diffusion",
      "клод": "Claude", "антропик": "Anthropic",
      "вейо 3": "Veo 3",
      "грок": "Grok",
      "ниантропик": "Anthropic",
      "стабил": "Stable",
      "дип си": "DeepSeek",
  }
  ```
  Замены сортируются по длине (сначала длинные, потом короткие), чтобы полные фразы не разбивались на части. Варианты в разных падежах (`люмы`, `люме`, `люму`) — каждый отдельной строкой.
- **User preference: каждый кадр динамичен.** Никаких статичных картинок. Каждый слайд в Pipeline v3 должен иметь движение (zoom in/out, pan). Использовать ffmpeg `zoompan` filter для Ken Burns эффекта: scale→crop в 2× разрешение, затем zoompan с чередующимися типами движения (zoom-in на чётных, pan на нечётных). Это базовое ожидание качества, не опция.
- **User preference: названия AI-моделей в субтитрах только латиницей.** Whisper часто ошибается, транскрибируя их по-русски. `fix_subtitle_text()` — обязательный шаг в пайплайне, без него видео выглядит непрофессионально.
- **User preference: проверяй качество сам.** Пользователь не хочет указывать на очевидные проблемы. Перед тем как показать результат — сам проверь: (1) нет ли кривых лиц на картинках, (2) читаются ли субтитры, (3) есть ли движение в кадрах, (4) нормально ли синхронизирован звук. Если проблема очевидна — чини ДО показа, не жди пока укажут. "Ты сам должен видеть что не так."
- **Dev.to API `published` field is create-only AND PUT may silently fail.** POST always creates draft (documented). PUT with `published: true` sometimes also returns `published: None` — caused by duplicate titles, rate limiting, or recent similar drafts. Fallback: publish manually via Dev.to web UI (Dashboard → Posts → Edit → Publish). Before creating: check for existing drafts with similar titles and delete them. See `references/devto-publishing.md`.
- **Telegram `sendPhoto` caption limit is 1024 chars, not 4096.** Posts longer than 1024 chars must be split: photo with truncated caption + separate `sendMessage` for full text. This catches everyone the first time. See `references/telegram-bot-api-publishing.md`.
- **`async def` without `await` silently does nothing.** Python returns a coroutine object and prints RuntimeWarning, but the function never executes. If a publish/discover function seems to return empty results, check it's not `async def` when called synchronously.
- **HN new accounts cannot submit URLs.** Error: "Sorry, your account isn't able to submit this site." Need karma or email hn@ycombinator.com. See `references/hackernews-publishing.md`.
- **xurl on headless/WSL2 requires `--headless` flag for OAuth2.** Without it, xurl tries to open a browser and times out. Use: `xurl auth oauth2 --app <name> <username> --headless` — user opens URL on phone, pastes code back. See `references/hackernews-publishing.md`.
- **Research before building — особенно для визуала.** Если делаешь контент с визуальным рядом — сначала изучи методологию: как правильно делать такие видео, какие приёмы работают, какие нет. web_search по "faceless video methodology", "ken burns effect tutorial", "video hook strategies", "best background for text shorts". Не тупи — сперва исследуй, потом делай. Пользователь явно просил: "Изучи методологию как правильно делать такие видео", "Правь методологию изучай интернет".
- **HF Spaces Gradio 5** — POST `/gradio_api/call/{fn}` работает (event_id), но WebSocket `/gradio_api/queue/join` возвращает **403** из РФ. Результат без WS не получить. Решение: браузерная автоматизация (Scrapling/Playwright) через SOCKS5 прокси. Детали: `references/free-video-sources.md` (раздел "Hugging Face Spaces / Решение: браузерная автоматизация")

## Monetization Touchpoints

- **YouTube**: Ad revenue, affiliate links in description, sponsorships
- **Telegram**: Paid channel, affiliate, digital products
- **Blog**: AdSense, affiliate, sponsored posts
- **Instagram**: Brand deals, affiliate, product sales
- **X/Twitter**: Monetization program, affiliate, consulting leads
