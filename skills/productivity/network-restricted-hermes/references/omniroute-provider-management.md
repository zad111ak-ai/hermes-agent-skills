# OmniRoute Provider Management

Managing AI provider connections, API keys, and proxy assignments in OmniRoute.

## Key Tables (SQLite at `~/.omniroute/storage.sqlite`)

### `provider_connections`
Each row = one provider connection (API key or OAuth):

| Column | Type | Purpose |
|--------|------|---------|
| `id` | TEXT PK | UUID |
| `provider` | TEXT | Provider slug (e.g., `openrouter`, `groq`, `anthropic`) |
| `auth_type` | TEXT | `apikey` or `oauth` |
| `test_status` | TEXT | `active`, `expired`, `banned`, `unavailable` |
| `api_key` | TEXT | The actual API key (stored plaintext) |
| `access_token` | TEXT | OAuth access token |
| `refresh_token` | TEXT | OAuth refresh token |
| `proxy_enabled` | INT | 1=proxy routing enabled |
| `is_active` | INT | 1=active, 0=disabled |
| `last_error` | TEXT | Last error message |
| `backoff_level` | INT | Exponential backoff count |
| `created_at` / `updated_at` | TEXT | Timestamps |

### `proxy_registry`
Registered proxy servers (currently unused in user's setup — table is empty):

| Column | Type | Purpose |
|--------|------|---------|
| `id` | TEXT PK | UUID |
| `name` | TEXT | Human name |
| `type` | TEXT | `socks5` or `http` |
| `host` | TEXT | Proxy host |
| `port` | INT | Proxy port |
| `username` / `password` | TEXT | Auth (if needed) |
| `status` | TEXT | `active`, `inactive` |
| `source` | TEXT | `manual` or auto-discovery |

### `proxy_assignments`
Links proxies to providers:

| Column | Type | Purpose |
|--------|------|---------|
| `proxy_id` | TEXT FK→proxy_registry | Proxy to use |
| `scope` | TEXT | `provider`, `combo`, `key` |
| `scope_id` | TEXT | Provider name (e.g., `openrouter`) |

### `api_keys`
Keys to access OmniRoute itself (not provider keys):

| Column | Type |
|--------|------|
| `id` | TEXT PK |
| `key` | TEXT (plaintext) |
| `name` | TEXT |
| `is_banned` | INT |
| `revoked_at` | TEXT |

## Adding a Provider API Key via SQLite

```bash
sqlite3 ~/.omniroute/storage.sqlite

# INSERT a new provider connection
INSERT INTO provider_connections (
  id, provider, auth_type, name, test_status, api_key,
  proxy_enabled, is_active, created_at, updated_at
) VALUES (
  hex(randomblob(16)), 'together', 'apikey', 'My Together Key',
  'active', 'your-api-key-here', 1, 1,
  datetime('now'), datetime('now')
);
```

## Updating an Existing Key

```bash
sqlite3 ~/.omniroute/storage.sqlite
UPDATE provider_connections SET api_key='new-key', test_status='active', updated_at=datetime('now')
WHERE provider='openai';
```

## Adding a SOCKS5 Proxy

```bash
sqlite3 ~/.omniroute/storage.sqlite

# Add proxy
INSERT INTO proxy_registry (id, name, type, host, port, status, source)
VALUES (hex(randomblob(16)), 'My SOCKS5', 'socks5', '127.0.0.1', 1080, 'active', 'manual');

# Assign to provider
INSERT INTO proxy_assignments (proxy_id, scope, scope_id)
VALUES ('<proxy-id-from-above>', 'provider', 'openrouter');
```

## REST API

OmniRoute provides a REST API (see `docs/openapi.yaml` in OmniRoute dist):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/providers` | GET | List all provider connections |
| `/api/settings/proxy` | GET | Get global proxy settings (PATCH returns 405, use SQLite instead) |
| `/api/settings/proxy/test` | POST | Test proxy connection |
| `/api/oauth/*` | POST | OAuth authorization flows |

**Note**: `PATCH /api/settings/proxy` returns 405 Method Not Allowed despite being documented. Direct SQLite write to `proxy_assignments` is the only reliable method to set a proxy for a provider.

## OmniRoute Proxy Configuration (SOCKS5)

If you have a working SOCKS5 proxy (e.g., tpws from `network-restricted-hermes`), add it to OmniRoute via SQLite:

```bash
python3 << 'EOF'
import sqlite3, uuid
conn = sqlite3.connect('/home/dima/.omniroute/storage.sqlite')

proxy_id = str(uuid.uuid4())
# Add proxy to registry
conn.execute("INSERT INTO proxy_registry (id, name, type, host, port, status, source) VALUES (?, ?, ?, ?, ?, 'active', 'manual')",
    (proxy_id, 'zapret-tpws', 'socks5', '127.0.0.1', 10987))
# Assign to all providers (scope_id=NULL = global)
conn.execute("INSERT INTO proxy_assignments (proxy_id, scope, scope_id) VALUES (?, 'provider', NULL)",
    (proxy_id,))
conn.commit()
conn.close()
print(f'Proxy {proxy_id} added — restart OmniRoute to apply')
EOF
```

After adding, restart OmniRoute with `HTTP_PROXY`/`HTTPS_PROXY` env vars:

```bash
export HTTP_PROXY=socks5://127.0.0.1:10987
export HTTPS_PROXY=socks5://127.0.0.1:10987
pkill -f 'next-server' 2>/dev/null
sleep 3
PORT=20128 node /path/to/omniroute/dist/server.js &
```

### Verify proxy is routing

Check call logs after the restart — look for the proxy IP in the outbound connection:

```bash
grep -r '"error":"\[502\]' ~/.omniroute/call_logs/$(date +%F)/ 2>/dev/null | head -3
# If 502 errors persist → proxy not routing or DPI still blocks
# If models start returning JSON → proxy works
```

## OmniRoute Restart (from inside Hermes session)

Kill and restart OmniRoute:

```bash
# Kill
pkill -f "next-server" 2>/dev/null

# Wait for port release
sleep 3

# Start with proxy env
HTTP_PROXY=socks5://127.0.0.1:10987 HTTPS_PROXY=socks5://127.0.0.1:10987 \
  nvm use 22 2>/dev/null && \
  PORT=20128 node /path/to/omniroute/dist/server.js > ~/.gateway.log 2>&1 &
```

To schedule a restart from inside a Hermes session (which can't exec `pkill` due to signal propagation), use a cron one-shot job:

```bash
hermes cron create \
  --schedule "$(date -d '+2 minute' +%Y-%m-%dT%H:%M:%S)" \
  --prompt "pkill -f 'next-server'; sleep 3; HTTP_PROXY=socks5://127.0.0.1:10987 HTTPS_PROXY=socks5://127.0.0.1:10987 PORT=20128 node /path/to/omniroute/dist/server.js &" \
  --name "restart-omniroute"
```
