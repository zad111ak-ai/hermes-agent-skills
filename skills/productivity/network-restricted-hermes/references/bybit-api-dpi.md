# Bybit API — DPI & Proxy Blocking Patterns (July 2026)

## Akamai CDN IP-Reputation Blocking

Bybit API (`api2.bybit.com`) sits behind **Akamai CDN**, which blocks requests from datacenter/cloud IPs. This is NOT standard DPI (TCP reset) — it's HTTP-level Access Denied.

### Symptoms
```
curl through Hysteria 2 HTTP proxy (127.0.0.1:1082) to api2.bybit.com:
→ "Access Denied" (HTTP 403)
→ Reference: 18.458a1402.1784326980.2ea90b1a (Akamai error)
→ errors.edgesuite.net/18.458a1402...
```

### What works vs what doesn't
| Target | Via Hysteria 2 proxy | Via direct | Diagnosis |
|--------|---------------------|------------|-----------|
| `httpbin.org/ip` | ✅ 200 | ❌ DPI | Proxy works |
| `google.com` | ✅ 200 | ❌ DPI | Proxy works |
| `api2.bybit.com` | ❌ 403 Access Denied | ❌ DPI | **Akamai blocks proxy IP** |

### Why
Akamai maintains IP reputation databases. Datacenter IPs (including VPN/proxy exit IPs) are flagged as non-residential. Bybit's Akamai config rejects all traffic from flagged IPs at the CDN edge — before the request even reaches Bybit's servers.

### Solutions
1. **Residential proxy** — IP from real ISP customer, not datacenter. Cost: $1-5/мес. Providers: Bright Data, Smartproxy, IPRoyal.
2. **Mobile proxy** — IP from cellular carrier. Even harder for Akamai to block.
3. **Bybit mobile app** — No API needed, trade directly from phone.
4. **Bybit P2P** — Trade without API access.

### What won't work
- Any datacenter proxy (Hysteria, WireGuard, SOCKS5 on VPS)
- AmneziaWG tunnel (exit IP is still datacenter)
- tpws/DPI bypass tools (this is not DPI, it's IP reputation)

## OAuth Callback — WSL2 ↔ Windows Boundary

Bybit OAuth flow redirects to `127.0.0.1:9876/callback`. This fails in WSL2 because:
- OAuth server runs in WSL2 (listens on `127.0.0.1:9876`)
- User's browser runs on Windows
- WSL2 and Windows are in different network namespaces
- Windows browser cannot reach WSL2's `127.0.0.1:9876`

### Workaround
Create API key manually through Bybit UI (web or app):
1. Go to Bybit → Profile → API Management
2. Create new API key
3. Enter public IP for IP binding: `YOUR_EXIT_IP` (Hysteria 2 exit IP)
4. Save API Key + Secret Key
5. Provide both to Hermes

### IP Binding Caveat
The IP `YOUR_EXIT_IP` is the Hysteria 2 exit server's IP. If Hysteria 2 goes down or the exit server changes, the API key stops working. Consider this for production use.

## Testnet API — Works Through Proxy ✅

**Key discovery (July 2026):** While `api2.bybit.com` (mainnet) is blocked by Akamai, the **testnet** endpoints are accessible through the Hysteria 2 HTTP proxy.

### Working Endpoint Matrix

| Endpoint | Via Hysteria 2 proxy (1082) | Direct | Notes |
|----------|---------------------------|--------|-------|
| `api-testnet.bybit.com` | ✅ 200 — `{"retCode":0,"retMsg":"OK"}` | ❌ DPI | **Use this** |
| `api2.bybit.com` | ❌ 403 Akamai | ❌ DPI | Mainnet blocked |
| `api2-testnet.bybit.com` | ❌ 404 nginx | ❌ DPI | Wrong domain |
| `api.bybit.com` | ⚠️ Not tested | ❌ DPI | — |

**Always use `api-testnet.bybit.com`** for testnet API calls. The `api2-testnet` domain does NOT work.

### V5 API Signature Format

Bybit V5 uses HMAC-SHA256. The sign string format:

```
sign_string = timestamp_ms + api_key + recv_window + query_string
```

Where `query_string` is the URL query parameters **sorted alphabetically** and concatenated as `key=value&key=value`.

#### Example: Wallet Balance (GET)

```bash
export BYBIT_API_KEY="YOUR_KEY"
export BYBIT_API_SECRET="YOUR_SECRET"
export BYBIT_ENV="testnet"

# Timestamp in milliseconds
TIMESTAMP=$(($(date +%s) * 1000))

# Query string (sorted alphabetically)
QUERY="accountType=UNIFIED"

# Sign string: timestamp + apiKey + recv_window + query
SIGN_STRING="${TIMESTAMP}${BYBIT_API_KEY}5000${QUERY}"

# HMAC-SHA256 signature
SIGNATURE=$(echo -n "$SIGN_STRING" | openssl dgst -sha256 -hmac "$BYBIT_API_SECRET" | awk '{print $2}')

# Request
curl -s -x http://127.0.0.1:1082 \
  "https://api-testnet.bybit.com/v5/account/wallet-balance?accountType=UNIFIED" \
  -H "X-BAPI-API-KEY: $BYBIT_API_KEY" \
  -H "X-BAPI-SIGN: $SIGNATURE" \
  -H "X-BAPI-TIMESTAMP: $TIMESTAMP" \
  -H "X-BAPI-RECV-WINDOW: 5000" \
  -H "Content-Type: application/json"
```

#### Required Headers

| Header | Value | Notes |
|--------|-------|-------|
| `X-BAPI-API-KEY` | Your API key | From Bybit UI |
| `X-BAPI-SIGN` | HMAC-SHA256 signature | See formula above |
| `X-BAPI-TIMESTAMP` | Current time in **milliseconds** | Must be within recv_window |
| `X-BAPI-RECV-WINDOW` | `5000` (recommended) | Max allowed: 5000ms |

#### Common Pitfalls

- **Timestamp must be milliseconds** — `date +%s` gives seconds, multiply by 1000
- **401 Unauthorized** usually means: wrong signature format, timestamp expired, or key created for wrong environment (mainnet key used on testnet)
- **The API key environment must match the endpoint** — a mainnet key won't work on testnet, and vice versa
- **IP binding** — if the API key has an IP binding, the request must come from that IP. Through Hysteria 2 proxy, the exit IP is what Bybit sees

### Environment Variables

```bash
export BYBIT_API_KEY="your_key_here"
export BYBIT_API_SECRET="your_secret_here"
export BYBIT_ENV="testnet"          # or "mainnet"
export BYBIT_API_URL="https://api-testnet.bybit.com"  # testnet
# export BYBIT_API_URL="https://api2.bybit.com"       # mainnet (blocked from RF)
```

## Related Patterns
- Standard DPI (TCP reset) → see main skill body (ECONNRESET pattern)
- DNS spoofing → see main skill body (8.6.112.x / 8.47.69.x)
- Cloudflare CDN blocking → see main skill body (OpenRouter/Together/Groq)
- **Akamai CDN IP-reputation** → this document (Bybit-specific)
