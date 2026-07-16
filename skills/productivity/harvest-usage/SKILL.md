---
name: harvest-usage
description: "Практическое использование Harvest для веб-скрейпинга: scrape, extract, crawl. Конкретные команды и примеры из жизни."
tags: ["harvest", "scraping", "web", "extraction", "russia"]
---

# Harvest Usage — Практическое использование

Активировать: когда нужно собрать данные с веб-страницы.

**Цель:** Получить данные с сайта за 3 команды, без написания кода.

---

## Зачем

Веб-скрейпинг — это боль. Playwright тормозит, BeautifulSoup ломается на динамических страницах, anti-bot блокирует. Harvest решает все эти проблемы одной командой.

---

## Установка

```bash
pip install harvest-agent
```

Проверь:
```bash
harvest --version
```

---

## Основные команды

### 1. `harvest scrape` — Полное содержимое страницы

```bash
# Просто текст (для чтения/анализа)
harvest scrape --mode full --output txt "https://example.com"

# С конкретными элементами
harvest scrape --selector ".price, .product-title" "https://example.com/pricing"

# JSON для программного использования
harvest scrape --mode economy --output json "https://example.com"
```

**Режимы:**
- `full` — безопасно, весь контент (по умолчанию)
- `economy` — экономит токены, только основное
- `hybrid` — оба варианта
- `auto` — умное определение

**Формат вывода:**
- `txt` — простой текст (для LLM)
- `json` — структурированные данные
- `md` — Markdown
- `csv` — таблица

### 2. `harvest extract` — Извлечение конкретных полей

```bash
# Извлечь цену, название и изображение
harvest extract --schema '{"price":".price", "title":"h1", "image":"img.product-photo"}' "https://example.com/product"

# Схема из файла
harvest extract --schema file://schema.json "https://example.com"
```

**Возвращает JSON:**
```json
{
  "price": "$99.99",
  "title": "Product Name",
  "image": "https://example.com/photo.jpg"
}
```

Если элемент не найден — `null`.

### 3. `harvest crawl` — Глубокий обход сайта

```bash
# Базовый обход
harvest crawl https://example.com

# Со скриншотом
harvest crawl https://example.com --screenshot shot.png

# С vision-извлечением (через GPT-4V)
harvest crawl https://example.com --vision

# Гибридный режим
harvest crawl https://example.com --mode hybrid-vision
```

### 4. `harvest batch` — Пакетная обработка

```bash
# Обработать список URL из файла
harvest batch urls.txt --output results.json
```

### 5. `harvest compliance` — Проверка robots.txt

```bash
harvest compliance https://example.com
harvest compliance https://example.com --format json
```

---

## Практические примеры

### Пример 1: Собрать цены с Wildberries
```bash
harvest scrape --selector ".product-card__price" --output json "https://www.wildberries.ru/catalog/12345/detail.aspx"
```

### Пример 2: Сравнить цены на Ozon
```bash
harvest extract --schema '{"name":".product-title", "price":".price-current", "rating":".rating-value"}' "https://www.ozon.ru/product/12345/"
```

### Пример 3: Собрать новости с Habr
```bash
harvest scrape --selector ".tm-title__link" --output txt "https://habr.com/ru/news/"
```

### Пример 4: Проверить доступность API
```bash
harvest compliance https://api.example.com
```

---

## Правила

1. **ВСЕГДА** используй `--mode full --output txt` для чтения контента
2. **ВСЕГДА** проверяй `harvest compliance` перед массовым скрейпингом
3. **НИКОГДА** не используй Harvest для API-вызовов (curl/httpx лучше)
4. **НИКОГДА** не превышай rate limiting — 10 запросов/мин на домен
5. **Если что-то сломалось** — попробуй `--mode economy` или другой селектор

---

## Частые ошибки

| Ошибка | Решение |
|--------|---------|
| `--css` не работает | Используй `--selector` для scrape, `--schema` для extract |
| Пустой вывод | Попробуй другой CSS-селектор или `--mode full` |
| Anti-bot блокирует | Harvest уже имеет anti-bot, ноบาง sites могут блокировать |
| Нет JSON | Добавь `--output json` |

---

## Продвинутое

### Через Python (программно)
```python
import asyncio
from harvest import Scraper

async def main():
    scraper = Scraper()
    result = await scraper.scrape("https://example.com", mode="full", output="txt")
    print(result)

asyncio.run(main())
```

### Через MCP (для Hermes Agent)
```bash
# Harvest работает как MCP-сервер
harvest mcp serve
```

Hermes автоматически подключит Harvest как инструмент.
