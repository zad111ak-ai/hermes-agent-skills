# Telegram Adapter — Source Patching (когда .env нельзя трогать)

Когда `.env` защищён (пользователь запретил модификацию), а `TELEGRAM_PROXY` там висит с `override=True` — обычные env-экспорты не помогают. Нужны точечные патчи в исходниках адаптера.

## Два бага в цепочке

### Баг 1: adapter.py — прокси не игнорируется при fallback_ips

Файл: `plugins/platforms/telegram/adapter.py`, строка ~2437.

Логика: если `proxy_url` (из env) truthy — используется прокси, даже если настроены `fallback_ips`.

Патч: после строки `proxy_url = resolve_proxy_url(...)` добавить:

```python
if fallback_ips and proxy_url:
    proxy_url = None
```

### Баг 2: telegram_network.py — транспорт сам перечитывает TELEGRAM_PROXY

Файл: `plugins/platforms/telegram/telegram_network.py`, строка `_resolve_proxy_url()`.

Транспорт ВНУТРИ себя вызывает `resolve_proxy_url("TELEGRAM_PROXY", ...)`, которая читает `.env` снова — обходя патч адаптера. В результате fallback-транспорты (`self._primary`, `self._fallbacks[...]`) создаются с `proxy=socks5h://...`.

Патч: добавить `import os` и в `_resolve_proxy_url()`:

```python
def _resolve_proxy_url(target_hosts=None) -> str | None:
    if os.getenv("HERMES_TELEGRAM_DISABLE_PROXY", "").strip().lower() in {"1", "true", "yes", "on"}:
        return None
    from gateway.platforms.base import resolve_proxy_url
    return resolve_proxy_url("TELEGRAM_PROXY", target_hosts=target_hosts)
```

### Баг 3: _is_retryable_connect_error — не retryable для ReadError/ProtocolError

Файл: `plugins/platforms/telegram/telegram_network.py`, функция `_is_retryable_connect_error`.

Исходно:

```python
def _is_retryable_connect_error(exc):
    return isinstance(exc, (httpx.ConnectTimeout, httpx.ConnectError))
```

Патч:

```python
def _is_retryable_connect_error(exc):
    return isinstance(exc, (
        httpx.ConnectTimeout,
        httpx.ConnectError,
        httpx.ReadError,
        httpx.ProtocolError,
        httpx.RemoteProtocolError,
        httpx.TransportError,
    ))
```

Без этого фолбэк к 149.154.167.220 никогда не пробуется — `ProtocolError('Malformed reply')` не retryable, транспорт сразу рейзит исключение.

## Запуск после патчей

```bash
unset ALL_PROXY HTTPS_PROXY HTTP_PROXY
export TELEGRAM_PROXY=""
export HERMES_TELEGRAM_DISABLE_PROXY="true"
export HERMES_TELEGRAM_DISABLE_FALLBACK_IPS="false"
cd ~/.hermes && python3 -m hermes_cli.main gateway run
```

- `.env` НЕ трогается
- `HERMES_TELEGRAM_DISABLE_PROXY=true` не перезаписывается `.env` (его там нет)
- Fallback IP из конфига (149.154.167.220) работает

## Очистка кэша

Если после патча gateway всё равно грузит старый код:

```bash
find /home/dima/Hermes-Agent -path "*/__pycache__/*" -name "*.pyc" -delete
```

## Верификация

Проверить, что патчи работают, можно прямым тестом кода:

```bash
python3 -c "
import sys; sys.path.insert(0, '/home/dima/Hermes-Agent')
from plugins.platforms.telegram.telegram_network import (
    _is_retryable_connect_error, _resolve_proxy_url,
)
import httpx, os

# 1 — retryable errors
assert _is_retryable_connect_error(httpx.ReadError('x'))
assert _is_retryable_connect_error(httpx.ProtocolError('x'))
assert _is_retryable_connect_error(httpx.RemoteProtocolError('x'))
assert _is_retryable_connect_error(httpx.TransportError('x'))
assert not _is_retryable_connect_error(ValueError('x'))

# 2 — disable proxy
os.environ['HERMES_TELEGRAM_DISABLE_PROXY'] = 'true'
assert _resolve_proxy_url() is None
os.environ.pop('HERMES_TELEGRAM_DISABLE_PROXY', None)

print('All assertions passed ✓')
"
```
