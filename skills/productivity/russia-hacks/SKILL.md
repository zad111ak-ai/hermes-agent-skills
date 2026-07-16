---
name: russia-hacks
description: "Обход DPI и блокировок из РФ: прокси, Hysteria 2, альтернативы заблокированным сервисам. Конкретные команды и конфиги."
tags: ["russia", "proxy", "bypass", "dpi", "hysteria", "vpn"]
---

# Russia Hacks — Обход блокировок из РФ

Активировать: когда нужен доступ к заблокированному ресурсу из России.

**Цель:** Работать с любыми API и сервисами, несмотря на блокировки DPI.

---

## Зачем

Из РФ заблокированы десятки сервисов: OpenAI, Anthropic, GitHub (частично), Twitter, ManyAPI. DPI (Deep Packet Inspection) перехватывает и рвёт соединения. Обычный VPN не помогает — провайдеры научились детектить даже протоколы обфускации.

---

## Решение: Hysteria 2

Самый надёжный протокол для обхода DPI. Использует QUIC (UDP), который DPI не может глубоко inspectить.

### Конфигурация клиента
```yaml
# /etc/hysteria/config.yaml
server: your-server:36712
auth: your-password

tls:
  sni: your-domain.com
  insecure: false

socks5:
  listen: 127.0.0.1:1081

http:
  listen: 127.0.0.1:1082
```

### Запуск
```bash
systemctl --user start hysteria
# Или напрямую
hysteria -c /etc/hysteria/config.yaml client
```

### Использование в коде
```python
import httpx

proxy = "http://127.0.0.1:1082"
async with httpx.AsyncClient(proxy=proxy) as client:
    response = await client.get("https://api.openai.com/v1/models")
```

```bash
# curl
curl -x http://127.0.0.1:1082 https://api.openai.com/v1/models

# npm/node
export HTTP_PROXY=http://127.0.0.1:1082
npm install
```

---

## Альтернативы заблокированным сервисам

| Заблокирован | Альтернатива | Как использовать |
|-------------|-------------|-----------------|
| OpenAI API | Zhipu GLM-4 | `GLM_API_KEY` через omni-route |
| OpenAI API | DeepSeek | `DEEPSEEK_API_KEY` |
| OpenAI API | Kimi/Moonshot | `KIMI_API_KEY` |
| Twitter API | Nitter | Временное решение |
| GitHub (частично) | Готово через прокси | `git config --global http.proxy http://127.0.0.1:1082` |
| Anthropic | OmniRoute | `localhost:3000` |

---

## Правила

1. **НИКОГДА** не удаляй `HTTP_PROXY` из systemd-сервисов — без прокси DPI блокирует
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

# Проверь логи Hysteria
journalctl --user -u hysteria -f
```
