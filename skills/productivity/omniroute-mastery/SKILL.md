---
name: omniroute-mastery
description: "Работа с OmniRoute: роутинг моделей,灰ые запросы, провайдеры, fallback, оптимизация расходов. Конкретные конфиги и команды."
tags: ["omniroute", "routing", "models", "proxy", "russia", "cost"]
---

# OmniRoute Mastery — Роутинг моделей

Активировать: когда нужно настроить роутинг между AI-моделями.

**Цель:** Использовать нужную модель в нужный момент, экономя деньги.

---

## Зачем

OmniRoute — это AI-шлюз, который роутит запросы между провайдерами. Работает через локальный прокси (HTTP/SOCKS5) на `localhost:1082`.

---

## Базовая конфигурация

### Конфигурация OmniRoute
```yaml
# ~/.omniroute/config.yaml
providers:
  groq:
    api_key: ${GROQ_API_KEY}
    base_url: https://api.groq.com/openai/v1
  
  deepseek:
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
  
  zhipu:
    api_key: ${GLM_API_KEY}
    base_url: https://open.bigmodel.cn/api/paas/v4

routing:
  default: groq/llama-3.1-8b-instant
  fallback: deepseek/deepseek-chat
```

### Запуск
```bash
# Через systemd
systemctl --user start omniroute

# Или напрямую
omniroute --config ~/.omniroute/config.yaml
```

### Проверка
```bash
curl http://localhost:3000/v1/models
```

---

## Роутинг моделей

### Как работает роутинг
1. Запрос приходит в OmniRoute
2. OmniRoute проверяет какой провайдер доступен
3. Если основной не работает → fallback
4. Если все не работают → ошибка

### Модели по категориям

| Категория | Модель | Провайдер | Стоимость |
|-----------|--------|-----------|-----------|
| Дешёвые | Llama 3.1 8B | Groq | 0.05$ |
| Средние | DeepSeek V3 | DeepSeek | 0.14$ |
| Дорогие | GPT-4 | OpenAI (через прокси) | 3.00$ |
|灰ые | GLM-4 | Zhipu | 0.07¥ |
|灰ые | Kimi | Moonshot | ~0.10¥ |

###灰ые запросы (gray-query)
Из РФ некоторые запросы блокируются OpenAI/Anthropic. Используй:

```python
# Через OmniRoute
import httpx

response = httpx.post(
    "http://localhost:3000/v1/chat/completions",
    json={
        "model": "zhipu/glm-4",
        "messages": [{"role": "user", "content": "запрос"}],
        "extra_body": {"gray_query": True}
    }
)
```

```bash
# curl
curl -X POST http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"zhipu/glm-4","messages":[{"role":"user","content":"запрос"}],"extra_body":{"gray_query":true}}'
```

**Какие запросы "серые":**
- Геополитика
- Взрослый контент
- Пиратство
- Мошенничество
- Взлом

**Провайдеры, которые пропускают灰ые:**
- Zhipu GLM-4 ✅
- Moonshot Kimi ✅
- Qwen ✅
- DeepSeek ✅

---

## Использование в Hermes Agent

### Конфигурация
```yaml
# ~/.hermes/config.yaml
model:
  default: auto/best-chat
  provider: custom:omniroute
  base_url: http://localhost:3000/v1
```

### Переключение моделей
```bash
# Через CLI
hermes model groq/llama-3.1-8b-instant

# Через slash-команду
/model deepseek/deepseek-chat
```

### Автоматический выбор
OmniRoute автоматически выбирает лучшую модель для задачи:
- Простые задачи → Groq (дешёво)
- Сложные задачи → DeepSeek (качество)
-灰ые запросы → Zhipu (свободный контент)

---

## Диагностика

```bash
# Проверь статус OmniRoute
systemctl --user status omniroute

# Проверь порты
ss -tlnp | grep 3000

# Проверь логи
journalctl --user -u omniroute -f

# Проверь доступные модели
curl http://localhost:3000/v1/models | jq
```

---

## Правила

1. **НИКОГДА** не удаляй `HTTP_PROXY` из systemd-сервисов — без прокси DPI блокирует
2. **НИКОГДА** не переключай модель на `auto/best-free` — это цикл смерти
3. **ВСЕГДА** используй `auto/best-chat` как основную модель
4. **ВСЕГДА** проверяй статус OmniRoute перед запросами
5. **Если что-то сломалось** — проверь порты, логи, статус сервисов
