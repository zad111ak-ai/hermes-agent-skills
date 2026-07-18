# Free Visual Sources for Content Pipeline

## Video Backgrounds

### 1. Pexels (официальное API)
- **Статус:** ✅ Бесплатно, официально
- **Лимиты:** 200 запросов/час (с бесплатным ключом)
- **Регистрация:** pexels.com → API key (2 мин)
- **API:** `GET https://api.pexels.com/videos/search?query=nature&per_page=15`
- **Интеграция:** `https://api.pexels.com/videos/{id}/files` → скачать MP4
- **Совет:** Искать "nature", "city timelapse", "ocean waves" для фонов

### 2. Pixabay Video
- **Статус:** ✅ Бесплатно
- **Лимиты:** Нет строгих квот
- **API:** `https://pixabay.com/api/videos/`

### 3. Coverr
- **Статус:** ✅ Бесплатно
- **Лимиты:** Безлимитно
- **Формат:** Royalty-free MP4

## Image Generation (Free APIs)

### 1. doubao2api (⭐77)
- **Модели:** Doubao Image, Doubao SD (text-to-image, image-to-image)
- **Лимиты:** ~50 ген/день/аккаунт
- **Формат:** OpenAI-совместимый API
- **Установка:** см. `api-key-hunting` skill → `references/reverse-engineered-api-tools.md`

### 2. imageFX-api (⭐128)
- **Модели:** Google Imagen 4
- **Установка:** `npm i -g @rohitaryal/imagefx-api`
- **Использование:** `imagefx generate "prompt" --output img.png`
- **Риск:** Google может прикрыть

### 3. free-dall-e-proxy (⭐389)
- **Модели:** DALL-E 3
- **Требует:** Docker + Coze Telegram бот
- **Формат:** REST API на localhost:8000

## Video Generation (Free APIs)

### 1. doubao2api
- **Модели:** Doubao text-to-video
- **Лимиты:** ~10-20 видео/день (дороже картинок)
- **API:** `POST /v1/video/generations` — OpenAI-совместимый
- **Время генерации:** 10-20 минут на видео

### 2. jimeng-free-tool-cli
- **Модели:** 5 video моделей от Jimeng (ByteDance)
- **Лимиты:** ~5-10 видео/день/аккаунт
- **Требует:** Cookie Jimeng

## Gradient Backgrounds (100% offline, без лимитов)

```python
from PIL import Image, ImageDraw
import numpy as np

def gradient(w=1080, h=1920, color1=(20,20,40), color2=(60,30,90)):
    base = Image.new('RGB', (w, h))
    top = Image.new('RGB', (w, h), color1)
    bottom = Image.new('RGB', (w, h), color2)
    mask = Image.new('L', (w, h))
    for y in range(h):
        for x in range(w):
            mask.putpixel((x, y), int(255 * y / h))
    return Image.composite(bottom, top, mask)
```

## Pexels Integration (Python)

```python
import requests

PEXELS_KEY = "your_key"
query = "nature timelapse"
resp = requests.get(
    f"https://api.pexels.com/videos/search?query={query}&per_page=15",
    headers={"Authorization": PEXELS_KEY}
)
videos = resp.json()["videos"]
# Берём первый Free video с MP4
for v in videos:
    for f in v["video_files"]:
        if f["quality"] == "hd" and f["width"] <= 1920:
            download_url = f["link"]
            break
```

## Мощность: Pexels + Gradient + doubao2api + imageFX-api

Комбинируй:
- Pexels → фон (реальное видео, бесплатно, 200/час)
- Gradient → запасной фон если Pexels не нашёл
- doubao2api → генерация изображений/видео по сценарию
- imageFX-api → генерация обложек/thumbnails

Это даёт faceless pipeline с 100% бесплатным визуалом.
