---
name: telegram-bot-patterns
description: "Паттерны Telegram-ботов на aiogram 3: FSM, middleware, rate limiting, SQLite WAL. Готовые сниппеты для быстрого старта."
tags: ["telegram", "bot", "aiogram", "python", "patterns", "russia"]
---

# Telegram Bot Patterns — Паттерны ботов

Активировать: когда нужно создать или улучшить Telegram-бота на Python.

**Цель:** Не изобретать велосипед. Готовые паттерны, которые работают.

---

## Зачем

80% Telegram-ботов ломаются на одних и тех же вещах: FSM без таймаутов, SQLite без WAL, rate limiting без логики. Эти паттерны решают типовые проблемы.

---

## Паттерн 1: SQLite WAL Mode

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("bot.db")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=10000")
    return conn
```

**Почему WAL:**
- Параллельный доступ (читатели + писатели)
- Не ломается при аварийном завершении
- Быстрее чем стандартный режим

---

## Паттерн 2: FSM с таймаутом

```python
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
import asyncio

class Form(StatesGroup):
    name = State()
    email = State()

router = Router()

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?")

@router.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.email)
    await message.answer("Email?")

@router.message(Form.email)
async def email(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Готово: {data['name']}, {message.text}")

# Таймаут FSM (в middleware или в хэндлере)
async def fsm_timeout(state: FSMContext, timeout: int = 300):
    await asyncio.sleep(timeout)
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        # Отправь сообщение пользователю
```

---

## Паттерн 3: Rate Limiting

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, limit: int = 10, window: int = 60):
        self.limit = limit
        self.window = window
        self.calls = defaultdict(list)
    
    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        self.calls[user_id] = [
            t for t in self.calls[user_id] 
            if now - t < self.window
        ]
        if len(self.calls[user_id]) >= self.limit:
            return False
        self.calls[user_id].append(now)
        return True

limiter = RateLimiter(limit=10, window=60)

# В хэндлере
@router.message()
async def handler(message: Message):
    if not limiter.is_allowed(message.from_user.id):
        await message.answer("⚠️ Слишком много запросов. Подожди минуту.")
        return
    # ... основная логика
```

---

## Паттерн 4: Работа через прокси

```python
import httpx

# Локальный прокси
PROXY = "http://127.0.0.1:1082"

async def make_request(url: str):
    async with httpx.AsyncClient(proxy=PROXY) as client:
        response = await client.get(url)
        return response.json()
```

```bash
# curl
curl -x http://127.0.0.1:1082 https://api.example.com

# npm/node
export HTTP_PROXY=http://127.0.0.1:1082
npm install
```

---

## Паттерн 5: Cron (APScheduler)

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job(CronTrigger(hour=9, minute=0))
async def daily_post():
    # Ежедневный пост в 9:00
    await bot.send_message(channel_id, "Доброе утро!")

scheduler.start()
```

---

## Паттерн 6: Доступ толькоOWNER

```python
OWNER_ID = 405065016  # твой Telegram ID

def owner_only(func):
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id != OWNER_ID:
            await message.answer("⛔ Нет доступа")
            return
        return await func(message, *args, **kwargs)
    return wrapper

@router.message(F.text == "/admin")
@owner_only
async def admin(message: Message):
    await message.answer("Панель администратора")
```

---

## Паттерн 7: PNG-отчёты (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont

def create_report(data: dict) -> str:
    img = Image.new("RGB", (800, 600), "#1a1a2e")
    draw = ImageDraw.Draw(img)
    
    # Заголовок
    draw.text((20, 20), data["title"], fill="white")
    
    # Данные
    y = 60
    for key, value in data.items():
        draw.text((20, y), f"{key}: {value}", fill="#00ff41")
        y += 30
    
    path = "/tmp/report.png"
    img.save(path)
    return path
```

---

## Правила

1. **ВСЕГДА** используй SQLite WAL для production
2. **ВСЕГДА** добавляй таймаут для FSM
3. **ВСЕГДА** делай rate limiting (10 запросов/мин)
4. **НИКОГДА** не храни токены в коде — используй `.env`
5. **НИКОГДА** не делай блокирующие вызовы в хэндлерах
