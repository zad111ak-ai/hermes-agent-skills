---
name: russia-hacks
description: "Настройка прокси и работа с API из России: конфиги, подключения, альтернативы заблокированным сервисам."
tags: ["russia", "proxy", "networking", "api", "configuration"]
---

# Russia — Настройка прокси и работа с API

Активировать: когда нужен доступ к API или сервису из России.

**Цель:** Работать с любыми API и сервисами через локальный прокси.

---

## Сетевая среда

В России ряд сервисов имеют ограничения на доступ. Решение — локальный прокси-сервер (HTTP/SOCKS5), через который маршрутизируются все запросы.

### Конфигурация прокси

```yaml
# Типичная конфигурация (Hysteria 2 или аналогичный прокси-сервер)
socks5:
  listen: 127.0.0.1:1081

http:
  listen: 127.0.0.1:1082
```

### Использование в коде

```python
import httpx

proxy = "http://127.0.0.1:1082"
async with httpx.AsyncClient(proxy=proxy) as client:
    response = await client.get("https://api.example.com/v1/models")
```

```bash
# curl
curl -x http://127.0.0.1:1082 https://api.example.com/v1/models

# npm/node
export HTTP_PROXY=http://127.0.0.1:1082
npm install

# git
git config --global http.proxy http://127.0.0.1:1082
```

---

## Альтернативы заблокированным сервисам

| Заблокирован | Альтернатива | Как использовать |
|-------------|-------------|-----------------|
| OpenAI API | Zhipu GLM-4 | `GLM_API_KEY` через OmniRoute |
| OpenAI API | DeepSeek | `DEEPSEEK_API_KEY` |
| OpenAI API | Kimi/Moonshot | `KIMI_API_KEY` |
| Twitter API | Nitter | Временное решение |
| GitHub (частично) | Прокси | `git config --global http.proxy http://127.0.0.1:1082` |
| Anthropic | OmniRoute | `localhost:3000` |

---

## Правила

1. **НИКОГДА** не удаляй `HTTP_PROXY` из systemd-сервисов — без прокси соединения могут обрываться
2. **НИКОГДА** не создавай бриджи/прокси — они умирают и ломают OmniRoute
3. **ВСЕГДА** проверяй статус прокси перед запросами
4. **ВСЕГДА** используй `localhost:1082` (HTTP) или `localhost:1081` (SOCKS5)
5. **Если что-то сломалось** — проверь порты, логи, статус сервисов

---

## Диагностика

```bash
# Проверь что прокси работает
curl -x http://127.0.0.1:1082 https://httpbin.org/ip

# Проверь порты
ss -tlnp | grep -E "1081|1082"

# Проверь логи прокси
journalctl --user -u hysteria -f
```
