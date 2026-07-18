# Telegram DPI Bypass — Session Notes

## Environment
- WSL2, Ubuntu 26.04, kernel 6.18.33.2-microsoft-standard-WSL2
- Hermes Gateway as systemd user service
- OmniRoute on localhost:20128 (AI gateway, not messaging)

## Problem
`api.telegram.org` resolves to IPs blocked by DPI (TCP SYN to port 443 times out, ICMP ping works).
Root cause: Deep Packet Inspection drops TLS handshake to Telegram IPs, not DNS poisoning.

## Working IPs Found
| IP | Status |
|---|---|
| `149.154.167.220` | WORKING — in `_SEED_FALLBACK_IPS` already |
| `149.154.166.110` | BLOCKED — returned by DoH auto-discovery |
| `91.108.56.100` | BLOCKED |

## Architecture of TelegramFallbackTransport
Location: `plugins/platforms/telegram/telegram_network.py`

1. `discover_fallback_ips()` queries Google + Cloudflare DoH for A records of `api.telegram.org`
2. If DoH returns IPs, **those** are used as fallback (even if they're also blocked)
3. If DoH yields nothing, falls back to `_SEED_FALLBACK_IPS = ["149.154.167.220"]`
4. The transport: first tries primary DNS (blocked → timeout), then tries each fallback IP
5. `_rewrite_request_for_ip()` changes URL host to IP but keeps `host` header and `sni_hostname` as `api.telegram.org` — same as `curl --resolve`
6. First successful fallback becomes `sticky_ip` — subsequent requests try it first

## Why DoH discovery was the problem
DoH from inside WSL also goes through the DPI-filtered connection. Google/Cloudflare DoH returned `149.154.166.110` (also blocked), which was used as the only fallback. The seed IP `149.154.167.220` was never reached because DoH "succeeded".

## Fix
Setting `fallback_ips` in config skips DoH entirely:
```
hermes config set gateway.platforms.telegram.extra.fallback_ips "149.154.167.220"
```

## Key Code References
- `_SEED_FALLBACK_IPS` line 43 of `telegram_network.py`
- `TelegramFallbackTransport.handle_async_request()` — fallback retry loop with sticky IP
- `_rewrite_request_for_ip()` — preserves host/SNI during IP rewrite
- `_fallback_ips()` in `adapter.py` — reads from `config.extra.get("fallback_ips")`
- `resolve_proxy_url("TELEGRAM_PROXY")` — proxy env var resolution
- `custom_base_url = self.config.extra.get("base_url")` — alternative: point bot at a custom API URL

## OmniRoute Combo Auto-Promote Connection

When the Hermes gateway uses an OmniRoute `auto/*` combo model (e.g. `auto/coding:reliable`), model failures cascade into Telegram unresponsiveness:

**The chain of failure:**
1. OmniRoute selected a provider from the virtual combo (e.g. `opencode/big-pickle`)
2. Provider returned an empty stream → OmniRoute treated it as "successful" (no finish_reason)
3. OmniRoute didn't try the next model in the combo → returned empty to Hermes
4. Hermes gateway got an empty response → couldn't generate reply → user got no answer
5. From the user's perspective: "Telegram disconnected"

**Root cause:** `comboAutoPromoteEnabled: false` in OmniRoute settings (default). The self-healing manager only excludes providers with score < 0.2. An "empty stream" doesn't lower the provider's health score — it keeps getting selected.

**Fix:** Enable auto-promote via Dashboard (Settings → Combo → Auto-promote) or direct SQLite write:
```bash
# Using OmniRoute's node_modules better-sqlite3 (nvm use 22 first):
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22
node -e "
const Database = require(process.env.NVM_BIN.replace('/bin','') + '/lib/node_modules/omniroute/node_modules/better-sqlite3');
const db = new Database('/home/dima/.omniroute/storage.sqlite', { readonly: false });
db.prepare(\"INSERT OR REPLACE INTO key_value (namespace, key, value) VALUES ('settings', ?, ?)\").run('comboAutoPromoteEnabled', JSON.stringify(true));
db.close();
"
```

**Verify:**
```bash
curl -s http://localhost:20128/api/settings | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('comboAutoPromoteEnabled'))"
# Should print: True
```

## custom_providers base_url Pitfall

The Hermes config.yaml stores `custom_providers`. If you point Hermes at OmniRoute, the base_url must be correct:

**Wrong:**
```yaml
custom_providers:
  - name: OmniRoute (localhost:20128)
    base_url: https://polza.ai/api/v1     # ← WRONG! This is a different service
    api_key: ''
    model: deepseek/deepseek-v4-flash
```

**Correct:**
```yaml
custom_providers:
  - name: OmniRoute (localhost:20128)
    base_url: http://localhost:20128/v1     # ← OmniRoute server URL
    api_key: no-key-required                # ← non-empty placeholder
    model: deepseek/deepseek-v4-flash
```

Symptoms of wrong base_url:
- Gateway logs show `HTTP 401: Неверные учётные данные авторизации`
- `agent.auxiliary_client: resolve_provider_client: named custom provider '...' has no resolvable api_key`
- Gateway starts, Telegram connects, but no messages get responses
- If model.provider references a custom provider with the wrong base_url, ALL requests fail

Fix both URL and api_key:
```bash
hermes config set custom_providers.0.base_url "http://localhost:20128/v1"
hermes config set custom_providers.0.api_key "no-key-required"
systemctl --user restart hermes-gateway
```

## Database Schema

Settings table structure in `~/.omniroute/storage.sqlite`:
- `key_value` — generic KV store, key storage for all settings
  - `namespace='settings'` — system settings (comboAutoPromoteEnabled, etc.)
  - `namespace='compression'` — compression pipeline config
  - `namespace='databaseSettings'` — audit/log toggles

Tables (sample from v3.8.39): ~180 tables including `combos`, `combo_targets`, `api_keys`, `provider_connections`, `proxy_registry`, `quota_pools`, `key_groups`, `session_account_affinity`, `webhook_deliveries`, etc.
- `comboAutoPromoteEnabled` in OmniRoute settings (`src/lib/db/settings.ts`) — when false, auto/combo won't failover on "empty stream" errors. Fix: set via SQLite (`namespace='settings'`, key=`comboAutoPromoteEnabled`, value=`true`) or toggle in dashboard (Settings → Combo)

## awg (AmneziaWG) Build Notes
- `amneziawg-go` builds from source with Go 1.23+ (no special deps beyond `git` and `go`)
- Docker registry pull from docker.io was also blocked — used direct git clone + Go build
- Build command: `cd /tmp && git clone --depth 1 https://github.com/amnezia-vpn/amneziawg-go.git && cd amneziawg-go && CGO_ENABLED=0 go build -o awg .`
- Binary is ~4.9MB statically linked
- Running awg says "kernel has first class support for AmneziaWG" — but WSL2 Microsoft kernel DOES NOT actually have it. The message is misleading.
- WSL root for installation: `cmd.exe /c "wsl -u root -e cp /tmp/amneziawg-go/awg /usr/local/bin/awg"`
- Can't install Go locally without root? Use Docker build: `docker run --rm -v /tmp/out:/out golang:1.23 bash -c 'git clone ... && CGO_ENABLED=0 go build -o /out/awg .'` (if Docker Hub is reachable)
