# Pollinations Free Image API

Бесплатная генерация изображений без ключа, регистрации и cookie.

## Эндпоинт

```
GET https://image.pollinations.ai/prompt/{url_encoded_prompt}
```

**⚠️ Старый эндпоинт `pollinations.ai/p/` НЕ РАБОТАЕТ** — возвращает HTML вместо JPEG.

## Параметры

| Параметр | Значение |
|----------|----------|
| Base URL | `https://image.pollinations.ai` |
| Path | `/prompt/{prompt}` |
| Промпт | URL-encoded, до 200 символов (обрезать) |
| Формат | JPEG |
| Content-Type | `image/jpeg` (первые 2 байта: `\xff\xd8`) |
| Размер | ~85‑170 KB |

## Hysteria Proxy

Запросы из РФ блокируются. Только через Hysteria SOCKS5/HTTP:

```python
import httpx
with httpx.Client(proxy='http://127.0.0.1:1082') as c:
    r = c.get(f'https://image.pollinations.ai/prompt/{clean_prompt}', timeout=45)
```

Hysteria HTTP прокси на `127.0.0.1:1082` (AmneziaWG SOCKS5 на `127.0.0.1:1081`).

## Rate Limits

- **~1 запрос / 7 секунд** (через Hysteria прокси — 429 при быстрее)
- Для pipeline.py: `time.sleep(7)` между запросами к Pollinations
- Без прокси rate limit может быть другой (IP-зависимый)
- Первый запрос обычно проходит, второй+ без паузы — 429

## Пример рабочего вызова

```bash
curl -x http://127.0.0.1:1082 \
  "https://image.pollinations.ai/prompt/beautiful%20cinematic%20digital%20art" \
  -o test.jpg
```

## Промптинг для faceless-контента

**⚠️ КРИТИЧЕСКОЕ ПРАВИЛО: НИКАКИХ ЛЮДЕЙ И ЛИЦ.**

Pollinations генерирует лица крайне плохо — результат выглядит как ночной кошмар (уродливые искажённые лица, uncanny valley). Для faceless AI-контента всегда указывать в промпте:

```
[описание темы], abstract futuristic technology visualization, no people, no faces, no characters, holographic UI, glowing circuits, data streams, sci-fi interface, octane render, 8k, high quality
```

### Примеры рабочих промптов

| Тема | Промпт |
|------|--------|
| ИИ в медицине | `AI diagnosis visualization, abstract medical holographic display, DNA helix, glowing neural network, no people no faces, futuristic UI` |
| Нейросети | `deep learning neural network visualization, abstract glowing neurons, holographic processor, no people, futuristic technology` |
| Будущее | `futuristic smart city data stream, abstract holographic interfaces, glowing circuits, no people, cyberpunk aesthetic` |
| YouTube | `digital content creation abstract, holographic play button, data analytics visualization, no people, glowing UI elements` |

### Приоритет усечения

Если промпт >200 символов — обрезать в таком порядке:
1. Сначала удалять упоминания людей/персонажей (их там и так быть не должно)
2. `cinematic`, `photorealistic`, `trending on artstation` — мало влияют
3. `octane render`, `8k` — можно убрать в крайнем случае
4. **Последним трогать:** `no people, no faces`, glowing, holographic, circuits, data — база рабочего промпта

## Валидация ответа

```python
if r.status_code == 200 and len(r.content) > 1000 and r.content[:2] == b'\xff\xd8':
    # это JPEG
else:
    # rate limit или ошибка
```

## Модели генерации

Pollinations также предоставляет модели через OmniRoute (порт 3000):
- `pollinations/flux` — Flux изображения
- `pollinations/gptimage` — GPT Image
- `pollinations/seedream5` — Seedream
- `pollinations/veo` — Veo видео
- `pollinations/wan` — Wan видео
- `pollinations/wan-pro` — Wan Pro видео

Для видео-моделей Hysteria прокси не обязателен — OmniRoute уже настроен.
