# OmniRoute Video Models — Обзор (2026-07-04)

## 31 видео-моделей в OmniRoute через Pollinations backend

Все бесплатные, через Hysteria прокси. Без ключей.

### Полный список

| Модель | Тип |
|--------|-----|
| veo-free/veo | Google Veo |
| veo-free/seedance | ByteDance Seedance |
| pol/veo, pollinations/veo | Google Veo |
| pol/seedance-pro, pollinations/seedance-pro | Seedance Pro |
| pol/seedance-2.0, pollinations/seedance-2.0 | Seedance 2.0 |
| pol/wan, pollinations/wan | WAN |
| pol/wan-fast, pollinations/wan-fast | WAN Fast |
| pol/wan-pro, pollinations/wan-pro | WAN Pro |
| pol/wan-pro-1080p, pollinations/wan-pro-1080p | WAN Pro 1080p |
| pol/wan-image, pollinations/wan-image | WAN Image |
| pol/wan-image-pro, pollinations/wan-image-pro | WAN Image Pro |
| pol/grok-video-pro, pollinations/grok-video-pro | Grok Video Pro |
| pol/p-video-720p, pollinations/p-video-720p | P-Video 720p |
| pol/p-video-1080p, pollinations/p-video-1080p | P-Video 1080p |
| veoaifree-web/veo | Veo (web) |
| veoaifree-web/seedance | Seedance (web) |

### Проблема: chat/completions не работает
Все модели возвращают 400 при текстовом промпте. Нужен другой эндпоинт.

### Pollinations direct API
- **GET /p/{prompt}** — ✅ возвращает картинку (работает через Hysteria)
- **POST /api/video/generate** — ❌ возвращает JPEG (768×768), не видео

### Рабочий подход (риск 0)
```
Pollinations GET /p/{prompt} (кадры) → ffmpeg loop+concat → edge-tts → sub
```
Реализован в `~/.hermes/tools/pipeline.py` (v3).

### Риски
- Pollinations изобр. — 🟢 нулевой
- OmniRoute video — 🟢 низкий
- Gemini Veo 2 — 🟡 средний (нужен cookie)
- Qwen/Kling — 🟡 средний (аккаунт, бан)
- OpenAI — 🔴 не трогаем
