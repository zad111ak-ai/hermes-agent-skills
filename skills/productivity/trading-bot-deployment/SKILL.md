---
name: trading-bot-deployment
description: Patterns for deploying and running CEX trading bots (freqtrade, custom) in DPI-restricted environments — proxy configuration, exchange API access, WebSocket vs REST, and bot lifecycle.
tags: [trading, bybit, freqtrade, proxy, cex, exchange, bot]
related_skills:
  - crypto-scanner-development
  - omniroute-management
---

# Trading Bot Deployment

Patterns for setting up CEX trading bots (freqtrade, custom scripts) in restricted network environments (DPI/Russia).

## Architecture

```
DPI-restricted host (WSL2/RF VPS)
  ├── Hysteria2 SOCKS5/HTTP proxy (port 1081/1082)
  │   └── Routes to non-blocked exit IP
  ├── Trading bot (freqtrade / custom)
  │   ├── REST API calls → via HTTP proxy ✅
  │   ├── WebSocket streams → blocked by DPI ❌
  │   └── Config: enable_ws=false, aiohttp_proxy set
  └── Exchange (Bybit/OKX/Binance)
      ├── api.bybit.com → works via proxy ✅
      ├── api2.bybit.com → blocked by Akamai CDN ❌ (not DPI)
      ├── api-testnet.bybit.com → works via proxy ✅
      └── stream.bybit.com → blocked by DPI ❌ (even via proxy)
```

## ⚠️ PITFALL: DPI vs CDN Blocking — Different Problems, Different Fixes

**DPI blocking** (Russia): ISP deep packet inspection blocks exchange domains. Fix: route through proxy (Hysteria2/SOCKS5).

**CDN blocking** (Akamai/Cloudflare): Exchange's own CDN blocks datacenter IPs. Fix: residential proxy or different endpoint. Datacenter proxy IPs (even through Hysteria) get blocked.

**Diagnostic pattern:**
```bash
# 1. Test direct (DPI blocks this)
curl -s https://api.bybit.com/v5/market/time

# 2. Test through proxy (if CDN blocks → 404/403)
curl -x http://127.0.0.1:1082 https://api.bybit.com/v5/market/time

# 3. If proxy works → DPI was the problem
# 4. If proxy returns 404/403 → CDN blocks proxy IP → need different endpoint or residential proxy
```

**PITfall:** If `api2.bybit.com` is blocked by Akamai (not DPI), switching proxy providers won't help. Use `api.bybit.com` instead — same API, different CDN edge.

## ⚠️ PITFALL: aiohttp Ignores HTTP_PROXY

Python's aiohttp does NOT respect `HTTP_PROXY`/`HTTPS_PROXY` environment variables. This breaks most trading bots that use async HTTP.

**freqtrade fix** — use ccxt config:
```json
{
    "ccxt_config": {
        "aiohttp_proxy": "http://127.0.0.1:1082"
    },
    "ccxt_async_config": {
        "aiohttp_proxy": "http://127.0.0.1:1082"
    }
}
```

**Custom bot fix** — pass connector directly:
```python
import aiohttp
connector = aiohttp.TCPConnector()
session = aiohttp.ClientSession(connector=connector)
# Or set proxy per-request:
async with session.get(url, proxy="http://127.0.0.1:1082") as resp:
    ...
```

**requests library** DOES respect HTTP_PROXY — no extra config needed.

## ⚠️ PITFALL: WebSocket Blocked by DPI Even Through Proxy

WebSocket upgrade requests are often blocked by DPI even when REST HTTP works through the same proxy. The DPI inspects the `Upgrade: websocket` header.

**freqtrade fix:**
```json
{
    "enable_ws": false
}
```
This forces REST polling (every candle close) instead of real-time WS. Slower but reliable.

**Custom bot fix:** Use REST polling with `fetch_ohlcv()` or `fetch_ticker()` on interval.

**Performance impact:** REST polling adds latency (up to candle interval, e.g. 15m). For high-frequency strategies this matters. For swing/day trading it's fine.

## freqtrade Setup (DPI-Restricted Environment)

### Dependencies
```bash
# Use existing venv if available
source ~/harvest/venv/bin/activate
pip install freqtrade
```

### Minimum Working Config (Bybit + Proxy)
```json
{
    "trading_mode": "spot",
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "stake_amount": 5,
    "dry_run": true,
    "dry_run_wallet": 100,
    "enable_ws": false,
    "exchange": {
        "name": "bybit",
        "ccxt_config": {
            "aiohttp_proxy": "http://127.0.0.1:1082"
        },
        "ccxt_async_config": {
            "aiohttp_proxy": "http://127.0.0.1:1082"
        },
        "pair_whitelist": ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    },
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1
    },
    "exit_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1
    },
    "pairlists": [{"method": "StaticPairList"}]
}
```

### ⚠️ PITFALL: freqtrade run.py Entry Point (v2024+)

Newer freqtrade versions changed `start_trading()` signature — it now requires `args` parameter. Using `python run.py trade` directly fails.

**Fix:** Use `-m freqtrade` module invocation:
```bash
python3 -m freqtrade trade --config config.json --strategy MyStrategy --dry-run
```

**Or** create a wrapper `run.py` that injects proxy env vars via subprocess:
```python
#!/usr/bin/env python3
import os, sys, subprocess
proxy_env = os.environ.copy()
proxy_env.update({
    'HTTP_PROXY': 'http://127.0.0.1:1082',
    'HTTPS_PROXY': 'http://127.0.0.1:1082',
    'http_proxy': 'http://127.0.0.1:1082',
    'https_proxy': 'http://127.0.0.1:1082',
})
result = subprocess.run([sys.executable, '-m', 'freqtrade'] + sys.argv[1:], env=proxy_env)
sys.exit(result.returncode)
```

### Leverage Tiers Issue

freqtrade fetches leverage tiers on startup for futures mode. This often fails through proxies.

**Fix:** Use `"trading_mode": "spot"` to skip leverage tier fetching entirely.

### Dry Run → Live Transition

1. Start with `dry_run: true` + `dry_run_wallet: 100` to verify strategy works
2. Check logs for `state: RUNNING` and REST polling (no WS errors)
3. Set `dry_run: false` and add API keys to config
4. **Start with minimum stake amount** ($5) to test live execution

## Bybit API Reference

### Endpoints
| Endpoint | Purpose | DPI | CDN |
|----------|---------|-----|-----|
| `api.bybit.com` | Main REST API | ✅ via proxy | ✅ |
| `api2.bybit.com` | Backup REST API | ✅ via proxy | ❌ Akamai blocks |
| `api-testnet.bybit.com` | Testnet REST | ✅ via proxy | ✅ |
| `stream.bybit.com` | WebSocket | ❌ DPI blocks | N/A |

### V5 Signature (HMAC-SHA256)
```python
import hmac, hashlib, time, urllib.parse

def sign_request(api_key, secret, params=None):
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    query_string = ""
    if params:
        query_string = urllib.parse.urlencode(sorted(params.items()))
    
    sign_str = f"{timestamp}{api_key}{recv_window}{query_string}"
    signature = hmac.new(secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
```

### Testnet vs Mainnet
- Keys created on **mainnet** → only work on `api.bybit.com`
- Keys created on **testnet** → only work on `api-testnet.bybit.com`
- API: `POST /v5/user/create-api` on respective domain
- If getting 401 → wrong key/domain combination

### Account Info
```bash
# Balance
curl -H "X-BAPI-API-KEY: <key>" -H "X-BAPI-SIGN: <sig>" \
     -H "X-BAPI-TIMESTAMP: <ts>" -H "X-BAPI-RECV-WINDOW: 5000" \
     "https://api.bybit.com/v5/account/wallet-balance?accountType=unified"
```

## Bot Lifecycle

### Start (Background)
```bash
cd /path/to/bot && source venv/bin/activate
python3 -m freqtrade trade --config config.json --strategy MyStrategy --dry-run
```
Use `terminal(background=True)` — never `nohup` in foreground terminal.

### Verify
```bash
# Check process alive
ps aux | grep freqtrade | grep -v grep

# Check logs for RUNNING state
process(action='log', limit=30)
```

### Stop
```bash
pkill -f "freqtrade trade"
# Or via process(action='kill', session_id=...)
```

## ⚠️ PITFALL: Small Balance Economics ($5–$50)

On tiny balances, fees dominate:
- Bybit spot fee: ~0.1% per trade (maker/taker)
- A round-trip (buy+sell) costs ~0.2%
- On $5 stake = $0.01 per trade — fees are negligible
- But stop-loss + ROI targets must be > fees to be profitable
- **Rule of thumb:** minimum profitable trade = stake × 0.5% (covers fees + slippage)

### Strategy Tuning for Small Balances
- Increase `minimum_roi` thresholds (don't exit for 0.3% gains)
- Use trailing stop (e.g. -5% stoploss, trailing offset +2%)
- Fewer but higher-confidence entries (RSI < 25 instead of < 30)
- 15m+ timeframe (1m/5m too noisy, fees eat micro-gains)
- Max 2–3 concurrent positions (capital too thin for more)

### Fiat→Crypto On-Ramp (Russia)
See `references/fiat-to-crypto-russia.md` for methods to fund exchange accounts from Russian bank cards (Bybit P2P, Telegram bots, BestChange).

## Relevant References

- `references/bybit-api.md` — Bybit V5 API details, endpoint testing, signature patterns
- `references/fiat-to-crypto-russia.md` — Fiat→crypto funding methods for RF users
- `references/freqtrade-proxy.md` — freqtrade proxy configuration deep-dive
