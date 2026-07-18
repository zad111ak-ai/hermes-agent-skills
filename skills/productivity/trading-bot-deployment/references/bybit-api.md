# Bybit API — Detailed Findings (2026-07-18)

## Tested Endpoints

### api.bybit.com (Mainnet REST) ✅
```bash
# Works through Hysteria2 proxy (1082)
curl -x http://127.0.0.1:1082 https://api.bybit.com/v5/market/time
# Returns: {"retCode":0,"retMsg":"OK","time":1752806355634}
```

### api-testnet.bybit.com (Testnet REST) ✅
```bash
curl -x http://127.0.0.1:1082 https://api-testnet.bybit.com/v5/market/time
# Returns: {"retCode":0,"retMsg":"OK","time":1752806355634}
```

### api2.bybit.com (Backup) ❌ Akamai CDN
```bash
curl -x http://127.0.0.1:1082 https://api2.bybit.com/v5/market/time
# Returns: "Access Denied" (Akamai — blocks datacenter IPs regardless of proxy)
```

### stream.bybit.com (WebSocket) ❌ DPI
```python
# Connection refused even through proxy — DPI inspects WS upgrade headers
ccxt.base.errors.NetworkError: Cannot connect to host stream.bybit.com:443
```

## Proxy IP That Gets Blocked
- Hysteria2 exit IP: `YOUR_PROXY_IP` (Netherlands)
- Akamai blocks this IP class — it's a known datacenter range
- Real user IP: `YOUR_EXIT_IP` (Russian residential)

## API Key Details
- **Key prefix:** `YOUR_API_KEY_PREFIX` (mainnet)
- **Created on:** mainnet (api.bybit.com)
- **Testnet key would need:** separate creation on api-testnet.bybit.com
- **401 on testnet:** expected — mainnet key doesn't work on testnet

## Account Info Retrieved
```json
{
    "accountType": "UNIFIED",
    "totalEquity": "0.00122000",
    "totalAvailableBalance": "0.00122000",
    "coin": [{"coin": "USDT", "equity": "0.00122000", "availableToWithdraw": "0.00122000"}]
}
```
- PnL: -59.98 USDT (historical losses)
- Balance: effectively empty (0.001 USDT)

## V5 API Signature Pattern
Headers required for authenticated requests:
```
X-BAPI-API-KEY: <api_key>
X-BAPI-SIGN: <hmac_sha256_signature>
X-BAPI-TIMESTAMP: <timestamp_ms>
X-BAPI-RECV-WINDOW: 5000
```

Signature string: `{timestamp}{api_key}{recv_window}{sorted_query_string}`
