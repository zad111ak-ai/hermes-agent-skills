---
name: self-hosted-ai
description: "Запуск AI локально: Ollama, Llama 3, подключение к Telegram-ботам, n8n. Полный гайд от установки до продакшна."
tags: ["self-hosted", "ollama", "llama", "local-ai", "russia", "docker"]
---

# Self-Hosted AI — Локальный AI

Активировать: когда нужно запустить AI без облака и платных API.

**Цель:** Иметь своего AI-агента, который работает 24/7 на твоём компьютере.

---

## Зачем

Из РФ заблокированы OpenAI, Anthropic, Google. Даже через прокси — дорого и ненадёжно. Локальный AI:
- Бесплатен
- Не зависит от блокировок
- Работает офлайн
- Данные не уходят на серверы

---

## Установка Ollama

### Windows
1. Скачай с [ollama.com](https://ollama.com)
2. Установи
3. Запусти

### Linux (WSL2)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Проверка
```bash
ollama --version
ollama list
```

---

## Модели

### Какую модель выбрать

| Модель | Размер | ОЗУ | Качество | Скорость |
|--------|--------|-----|----------|----------|
| Llama 3.1 8B | 4.7 GB | 8 GB | Среднее | Быстро |
| Llama 3.1 70B | 40 GB | 48 GB | Высокое | Медленно |
| Mistral 7B | 4 GB | 8 GB | Среднее | Быстро |
| DeepSeek V3 | 16 GB | 24 GB | Высокое | Средне |

**Для начинающих:** Llama 3.1 8B — баланс качество/скорость.

### Скачивание
```bash
ollama pull llama3.1:8b
ollama pull mistral:7b
```

### Запуск
```bash
# Интерактивный режим
ollama run llama3.1:8b

# API (для ботов)
ollama serve
# Доступен на http://localhost:11434
```

---

## Подключение к Telegram-боту

### Через aiogram 3
```python
import httpx
from aiogram import Bot, Router, F
from aiogram.types import Message

bot = Bot(token="YOUR_TOKEN")
router = Router()

async def ask_ollama(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

@router.message(F.text)
async def handle(message: Message):
    answer = await ask_ollama(message.text)
    await message.answer(answer)
```

---

## Подключение к Hermes Agent

### Конфигурация
```yaml
# ~/.hermes/config.yaml
model:
  default: ollama/llama3.1:8b
  provider: ollama
  base_url: http://localhost:11434/v1
```

### Запуск
```bash
hermes chat
```

---

## Docker Compose (продакшн)

```yaml
version: "3.8"
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
  
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - OLLAMA_API=http://ollama:11434
    restart: unless-stopped

volumes:
  ollama_data:
```

```bash
docker-compose up -d
```

---

## Автоматизация (n8n)

n8n — визуальный конструктор автоматизаций. Работает с Ollama.

### Установка
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

### Пример workflow
1. Telegram Trigger → получено сообщение
2. HTTP Request → Ollama API
3. Telegram Send → ответ пользователю

---

## Правила

1. **ВСЕГДА** используй `stream: False` для API-вызовов
2. **ВСЕГДА** проверяй доступную ОЗУ перед скачиванием модели
3. **НИКОГДА** не запускай больше одной модели одновременно (без GPU)
4. **НИКОГДА** не используй модели больше 8B без GPU
5. **Если тормозит** — уменьши контекст или используй более мелкую модель
