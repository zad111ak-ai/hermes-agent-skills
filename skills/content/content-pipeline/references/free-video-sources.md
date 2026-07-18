# Free AI Video Generation Sources

## ⚡ Quick Decision Tree

```
Нужно AI видео?
├── Есть терпение и прокси
│   └── OmniRoute (порт 3000) → Pollinations/Veo/WAN через Hysteria SOCKS5
├── Нужно быстро (2-5 мин)
│   └── Pipeline 2.0: FAL FLUX картинки → ffmpeg слайд-шоу → TTS → субтитры
├── Есть HF токен
│   └── HF Inference API (SVD, CogVideo, LTX-Video)
└── Нужно качественное без вотермарки
    └── Gemini AI Studio → Veo 2 (через Google-аккаунт, 1500/день)
```

---

## 1. OmniRoute Video Models (через прокси)

OmniRoute на порту **3000** содержит 35+ видео-моделей.

### Доступные модели (через Pollinations API)

| Модель | Тип | Статус |
|--------|-----|--------|
| `veo` (Google) | T2V | ⚠️ Требует прокси |
| `wan` | T2V | ⚠️ Требует прокси |
| `seedance` | T2V | ⚠️ Требует прокси |
| `ltx-2` | T2V | ⚠️ Требует прокси |
| `nova-reel` | T2V | ⚠️ Требует прокси |
| `grok-video-pro` | T2V | ⚠️ Требует прокси |
| `p-video` | T2V | ⚠️ Требует прокси |

### Проверка доступных моделей

```bash
curl http://localhost:3000/v1/models | python3 -m json.tool | grep -i "video\|veo\|wan\|kling\|pika\|runway\|ltx"
```

### Проблема: Pollinations заблокирован в РФ

Pollinations API не отвечает напрямую. **Решение:** настроить HTTP_PROXY через Hysteria.

Проверка доступности Pollinations:
```bash
# Без прокси — не работает
curl -s https://text-pollinations.openai.azure.com/v1/models

# Через Hysteria SOCKS5 — работает (возвращает JPEG, не видео)
curl -s --socks5 127.0.0.1:1081 "https://pollinations.ai/p/красивый_пейзаж" -o test.jpg
```

### Настройка прокси для OmniRoute

OmniRoute нужно указать `HTTP_PROXY` / `HTTPS_PROXY`:
```bash
export HTTP_PROXY=socks5h://127.0.0.1:1081
export HTTPS_PROXY=socks5h://127.0.0.1:1081
export NO_PROXY=localhost,127.0.0.1
# Перезапустить OmniRoute
```

---

## 2. Hugging Face Spaces (бесплатные GPU)

### Доступные Space с видео-моделями

| Space | Модель | Тип | Плюсы | Минусы |
|-------|--------|-----|-------|--------|
| `multimodalart/stable-video-diffusion` | SVD (Stability AI) | img2vid | ✓ Стабильный | Требует картинку на вход |
| `Lightricks/ltx-video-distilled` | LTX-Video | T2V | ✓ Быстрый | Gradio 5 API |
| `KingNish/Instant-Video` | Кастомная | T2V | ✓ Простой | Gradio 5 API |
| `ali-vilab/modelscope-text-to-video-synthesis` | ModelScope | T2V | ✓ Классика | Медленный |

### Проблема: Gradio 5 WebSocket блокирован

Gradio 5+ использует WebSocket для очереди, не прямое REST.

**Экспериментально установлено:** HF Spaces возвращает **403 на WebSocket** (`/gradio_api/queue/join`) из определённых регионов, даже через Hysteria SOCKS5. curl, aiohttp, websockets lib — все дают 403. POST-запрос на `/gradio_api/call/{fn_name}` **работает** (200, event_id), но результата без WS не получить.

### Gradio 5 — точный флоу (на примере LTX-Video)

**Space:** `Lightricks/ltx-video-distilled`  
**OpenAPI spec:** `GET /gradio_api/openapi.json` (самый полезный endpoint — показывает все функции, параметры, типы)

**Функции (fn_name):** `text_to_video`, `image_to_video`, `video_to_video`

```python
import httpx, json

# Шаг 1: POST → event_id (✅ работает)
payload = {
    "data": [
        "a cute orange cat walking on a sunny beach, cinematic",  # prompt
        "",            # negative_prompt
        None,          # input_image
        None,          # input_video
        512,           # height_ui (256-1280)
        512,           # width_ui (256-1280)
        "text-to-video",  # mode: text-to-video|image-to-video|video-to-video
        4.0,           # duration_ui (0.3-8.5)
        97,            # ui_frames_to_use (9-257)
        -1,            # seed_ui
        True,          # randomize_seed
        3.5,           # ui_guidance_scale (1.0-10.0)
        True           # improve_texture_flag
    ]
}
r = httpx.post(
    "https://Lightricks-ltx-video-distilled.hf.space/gradio_api/call/text_to_video",
    json=payload, headers={"Content-Type": "application/json"}
)
event_id = r.json()["event_id"]  # ✅ работает

# Шаг 2: WebSocket → получить результат (❌ НЕ РАБОТАЕТ — 403)
# wss://Lightricks-ltx-video-distilled.hf.space/gradio_api/queue/join
```

### Эндпоинты Space

| Endpoint | Метод | Описание | Статус |
|----------|-------|----------|--------|
| `/gradio_api/config` | GET | Список функций (JSON) | ✅ |
| `/gradio_api/openapi.json` | GET | OpenAPI 3.0 spec | ✅ |
| `/gradio_api/call/{fn_name}` | POST | Запустить функцию → event_id | ✅ |
| `/gradio_api/call/{fn_name}/data/{event_id}` | GET | SSE поток результата | ⚠️ |
| `/gradio_api/run/{fn_name}` | POST | HTTP REST (Gradio <5) | ❌ Gradio 5: "use queue" |
| `/gradio_api/queue/join` | WS | WebSocket очередь | ❌ 403 в РФ |

### Параметры LTX-Video (из OpenAPI)

| Параметр | Тип | Диапазон | Описание |
|----------|-----|---------|----------|
| prompt | string | — | Текстовый промпт |
| negative_prompt | string | — | Негативный промпт |
| mode | enum | text-to-video / image-to-video / video-to-video | Режим |
| duration_ui | number | 0.3–8.5 | Длительность (сек) |
| ui_frames_to_use | number | 9–257 | Количество кадров |
| seed_ui | integer | — | Сид |
| randomize_seed | boolean | — | Случайный сид |
| ui_guidance_scale | number | 1.0–10.0 | Guidance scale |
| height_ui / width_ui | number | 256–1280 | Разрешение |
| improve_texture_flag | boolean | — | Улучшение текстуры |

### Через HF Inference API (если есть токен)

```bash
# Stable Video Diffusion (img2vid)
curl -X POST https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid \
  -H "Authorization: Bearer hf_YOUR_TOKEN" \
  -F "inputs=@input.jpg" \
  -o output.mp4

# CogVideo (если доступна)
curl -X POST https://api-inference.huggingface.co/models/THUDM/CogVideoX-5B \
  -H "Authorization: Bearer hf_YOUR_TOKEN" \
  -d '{"inputs": "a cat walking"}' \
  -o output.mp4
```

**Важно:** Не все модели доступны через Inference API (требуют GPU). Проверить:
```bash
curl -s https://api-inference.huggingface.co/status/<model_id> \
  -H "Authorization: Bearer hf_TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print('loaded:', d.get('loaded', False))"
```

### Решение: браузерная автоматизация (Deer подход)

Поскольку WebSocket API заблокирован, а POST без WS результата не даёт — **единственный рабочий путь через браузер:**

1. Открыть Space через Chromium с SOCKS5 прокси
2. Ввести промпт в текстовое поле
3. Нажать кнопку Generate
4. Дождаться завершения генерации
5. Скачать готовое видео

```python
# Прототип через Playwright/Scrapling
from playwright.sync_api import sync_playwright

PROXY = {"server": "socks5://127.0.0.1:1081"}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, proxy=PROXY)
    page = browser.new_page()
    page.goto("https://Lightricks-ltx-video-distilled.hf.space")
    
    page.fill("textarea", "a cat walking on a sunny beach, cinematic")
    page.click("button:has-text('Generate')")
    page.wait_for_selector("video", timeout=300000)  # 5 мин
    
    video_url = page.get_attribute("video source", "src")
    print(f"Video URL: {video_url}")
```

**Scrapling StealthyFetcher** (BrowserAct) — предпочтительнее Playwright: использует Chromium через прокси, уже знаком по `api-key-hunting`, меньше зависимостей.

### Пробуждение спящего Space

```bash
# Space спит после бездействия — нужно разбудить (может занять 30-60 сек)
curl -s "https://Lightricks-ltx-video-distilled.hf.space/" > /dev/null
sleep 60  # Ждать загрузки модели
# Теперь можно дёргать API
```

---

## 3. Gemini / Veo 2 через AI Studio

**Самый рабочий путь для качественного видео без вотермарки.**

- Бесплатно: 1500 запросов/день на Google-аккаунт
- У нас: 3 аккаунта → 4500 запросов/день
- API ключ: AI Studio → Get API Key → `AIzaSy...`
- Формат: Gemini API через OmniRoute или напрямую

```bash
# Через OmniRoute (порт 3000)
curl http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini/veo-2",
    "messages": [{"role": "user", "content": "Generate a video of a cat walking"}]
  }'
```

---

## 4. Pipeline 2.0 — Слайд-шоу из AI-картинок

Если AI-видео недоступно — **мощный запасной вариант:**

1. **Генерация серии изображений** через `image_generate` (FAL FLUX 2 Klein 9B)
2. **Сборка видео** через ffmpeg filter_complex loop+concat — без промежуточных файлов, нет segfault
3. **TTS озвучка** через `edge-tts` (мужской голос ru-RU-DmitryNeural)
4. **Субтитры** через `faster-whisper` (вшиваются в видео)

```bash
# Pipeline 2.0 (установлен в ~/.hermes/tools/pipeline.py)
python3 ~/.hermes/tools/pipeline.py --topic "Тема видео" --lang ru
```

**Плюсы:** работает без ключей, без прокси, без лимитов  
**Минусы:** не AI-видео, а слайд-шоу

### Известные проблемы и их решения

| Проблема | Симптом | Решение |
|----------|---------|---------|
| **httpx + HTTP_PROXY** | Pipeline висит или падает при генерации script через OmniRoute | `httpx.AsyncClient(trust_env=False)` — env vars (HTTP_PROXY=127.0.0.1:8080 from old config) перехватывают запросы |
| **ffmpeg concat PNG segfault** | Concat .ts сегментов падает с segfault, выход 139 | Использовать **filter_complex loop+concat** вместо .ts: `loop=N:1:0,setpts=N/30/TB` на каждый кадр, затем `concat`. Никаких промежуточных файлов |
| **SSE response** | Тело ответа содержит `data: {...}` строки, а не чистый JSON | Даже с `stream: false` OmniRoute возвращает SSE. Парсить строки с префиксом `data: `, собирать content из delta |
| **Женский голос неестественный** | TTS звучит синтетически, пользователь жалуется | Переключить на мужской — `ru-RU-DmitryNeural` (русский) / `en-US-GuyNeural` (английский) |
| **Названия сервисов по-русски** | В скрипте «ЧатДжиПиТи» вместо ChatGPT | Всегда писать названия латиницей в промпте генерации скрипта |

---

## 5. Reverse-Engineered API (GitHub находки)

Из `api-key-hunting` skill:

| Инструмент | Модели | Лимиты | Статус |
|------------|--------|--------|--------|
| **doubao2api** | ByteDance Doubao — text + image + video + music | ~10-20 видео/день/акк | ⚠️ Хрупкий |
| **jimeng-free-tool-cli** | Jimeng — 5 video моделей, 2K HD | ~5-10/день | ⚠️ Требует cookie |
| **free-dall-e-proxy** | DALL-E 3 через Coze | DALL-E только image | ❌ Не видео |

---

## Сводка: что и когда использовать

| Ситуация | Решение | Время | Качество |
|----------|---------|-------|----------|
| Любой контент, срочно | Pipeline 2.0 (слайд-шоу + TTS) | 2-5 мин | Среднее |
| Есть ключ Gemini | Veo 2 через AI Studio | 1-3 мин | Высокое |
| Настроен прокси OmniRoute | Pollinations/Veo/WAN | 30-60 сек | Среднее-высокое |
| Есть HF токен | HF Inference API | 1-5 мин | Среднее |
| Не срочно, эксперимент | HF Space через gradio_client | 5-15 мин | Зависит от модели |
