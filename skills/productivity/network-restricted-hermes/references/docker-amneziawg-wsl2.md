# AmneziaWG + SOCKS5 in Docker on WSL2

Refactored architecture (June 2026) — SOCKS5 code lives in `templates/socks-server.py` with an IP hardcode dict for DNS-poisoning bypass. The `scripts/start-awg.sh` script mounts that file as a volume so both containers share it.

## Architecture

```
Hermes (WSL) → socks5h://127.0.0.1:1080 → SOCKS5 (python:3.12-slim)
  → --network=container:awg → wg0 tunnel → AI Provider API
```

Two containers share network stack (via `--network=container:awg`):
- **awg**: `metaligh/amneziawg` — `awg-quick up wg0`, creates AmneziaWG tunnel
- **awg-socks**: `python:3.12-slim` — runs `templates/socks-server.py` from mounted volume

## Key Files

| File | Purpose |
|------|---------|
| `templates/socks-server.py` | SOCKS5 server. Hardcoded provider IPs in HOSTS dict bypass DPI-poisoned DNS. Pure stdlib, no deps. |
| `scripts/start-awg.sh` | One-shot launcher: rm old containers → create WG → create SOCKS5 → fix routing → verify |
| `~/.bashrc` (end) | If-absent autostart: OmniRoute first, then `scripts/start-awg.sh &` in background |

## Autostart (.bashrc snippet)

```bash
# ~/.bashrc — разместить ПОСЛЕ nvm init
AWG_SKILL="$HOME/.hermes/skills/autonomous-ai-agents/network-restricted-hermes"

# OmniRoute (if not running)
if ! curl -s --max-time 3 http://localhost:20128/v1/models > /dev/null 2>&1; then
    nvm use 22 > /dev/null 2>&1
    nohup node /home/dima/.nvm/versions/node/v22.23.1/lib/node_modules/omniroute/dist/server.js > ~/.omniroute.log 2>&1 &
    sleep 3
    echo "✅ OmniRoute запущен"
    bash "$AWG_SKILL/scripts/start-awg.sh" > /dev/null 2>&1 &
fi

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q awg-socks; then
    export ALL_PROXY=socks5h://127.0.0.1:1080
fi
```

## Setup Steps (one-time)

```bash
# 1) docker registry mirrors (required — Docker Hub is also DPI-blocked)
cmd.exe /c "wsl -u root -e sh -c 'mkdir -p /etc/docker && cat > /etc/docker/daemon.json'" </tmp/daemon.json
cmd.exe /c "wsl -u root -e systemctl reload docker"

# 2) Pull images (through mirrors)
docker pull metaligh/amneziawg:latest
docker pull python:3.12-slim

# 3) Place AmneziaWG config
cp /path/to/nether.conf ~/amneziawg/nether.conf

# 4) First launch
bash "$AWG_SKILL/scripts/start-awg.sh"
```

## DNS Poisoning Trap

DNS (UDP 53) bypasses the WG tunnel even inside containers. The `HOSTS` dict in 
`socks-server.py` hardcodes real provider IPs so the SOCKS5 proxy never resolves 
blocked domains through the poisoned resolver.

Known real IPs (current as of June 2026):
- `api.groq.com` → `172.64.149.20`
- `openrouter.ai` → `172.64.154.20`
- `api.together.xyz` → `172.64.150.10`
- `api.perplexity.ai` → `104.18.0.121`
- `api.novita.ai` → `104.18.0.121`

To verify/update:
```bash
docker exec awg sh -c 'curl -s "https://dns.google/resolve?name=DOMAIN&type=A" -H "accept: application/dns-json"'
```

Edit `templates/socks-server.py` with new IPs, then re-run `scripts/start-awg.sh`.

## Verification

```bash
# Check VPN IP
curl -x socks5h://127.0.0.1:1080 -s --max-time 15 https://ifconfig.me
# → must show VPN IP (e.g. YOUR_VPN_IP), NOT host IP

# Check DPI-blocked provider
curl -x socks5h://127.0.0.1:1080 -s --max-time 15 \
  -o /dev/null -w "%{http_code}" https://openrouter.ai/api/v1/models
# → 200 (not 000)

# Check Groq (with real API key)
curl -x socks5h://127.0.0.1:1080 -s --max-time 15 \
  -o /dev/null -w "HTTP: %{http_code} (%{time_total}s)" \
  https://api.groq.com/openai/v1/models -H "Authorization: Bearer $KEY"
# → 403 (auth, not timeout)
```

## Port Mismatch Trap

The `.bashrc` may set `ALL_PROXY=socks5h://127.0.0.1:8080` but the skill's docker-compose and `start-awg.sh` both serve SOCKS5 on **port 1080**. This means `ALL_PROXY` points to a dead port — all traffic through it silently fails.

**When debugging**: always check what port the SOCKS5 container actually listens on vs what `ALL_PROXY` says:

```bash
ss -tlnp | grep -E '1080|8080'
env | grep -i ALL_PROXY
```

If they don't match, update `.bashrc` to use `1080` (or change the docker setup to use `8080`).

## Empty Config Trap

The docker-compose mounts `./wg0-minimal.conf` as the WG config. If this file is **empty (0 bytes)**, `amneziawg-go` starts with no config — no handshake, no error, just silence.

The `scripts/start-awg.sh` mounts a DIFFERENT file: `nether.conf`. So the script may work while docker-compose silently fails.

**Diagnostic**:
```bash
ls -la ~/amneziawg/wg0-minimal.conf
cat ~/amneziawg/wg0-minimal.conf | wc -c
# If 0 → file is empty → tunnel never connects
```

**Fix**: delete `wg0-minimal.conf` and replace with the real config, or change `docker-compose.yml` to mount `nether.conf` instead.

## Pitfalls

- **ALWAYS `docker rm -f` before creating fresh containers.** `docker restart` preserves stale WG kernel state — handshake is lost immediately. The script does `rm -f` on every run.
- **WireGuard loses handshake on ANY restart.** Ephemeral kernel state. Kill and recreate, never restart.
- **`ALL_PROXY=socks5h://127.0.0.1:1080` — the `h` is critical.** `socks5h` resolves DNS through the proxy (inside WG). `socks5` resolves locally (DPI-poisoned). Without the `h`, all traffic hits fake IPs and immediately resets. This is the #1 source of "proxy isn't working" bugs.
- **Docker pull from registry is DPI-blocked.** Pre-configure mirrors first.
- **Routing fix required after `awg-quick up`.** `awg-quick up wg0` creates the tunnel but does NOT change the default route. Without `ip route del default via 172.17.0.1 dev eth0 && ip route add default dev wg0`, all traffic from the SOCKS5 container goes through Docker bridge (eth0 → WSL host), bypassing WG entirely.
- **Config must be at `/etc/amnezia/amneziawg/wg0.conf`.** Not `/etc/wireguard/`.
- **`--device=/dev/net/tun` required** for userspace TUN.
- **apt-get inside WG container fails** after routing is forced through wg0 (no internet on default route from inside the WG container to APT mirrors). That's why SOCKS5 uses a separate `python:3.12-slim` container with pre-installed Python.
- **DNS poisoning via HOSTS dict** — without hardcoded IPs in `templates/socks-server.py`, the SOCKS5 proxy resolves domains through the container's resolver, which uses the host's DNS (DPI-poisoned). The `HOSTS` dict intercepts lookups at the application level, bypassing the poisoned resolver entirely.
- **OmniRoute proxy config via SQLite has a cache issue.** Even after deleting old proxy entries and creating new ones, OmniRoute may still attempt connections to the old proxy IP/port (e.g., `127.0.0.1:10987`). Full `pkill -f 'node.*omniroute'` + restart is required, and even that may not clear the in-memory cache. The `ALL_PROXY` env var approach is more reliable.
- **`--device=/dev/net/tun` required** for userspace TUN.
- **apt-get inside WG container fails** after routing is forced through wg0. That's why SOCKS5 uses a separate `python:3.12-slim` container with pre-installed Python.

## `amneziawg-go` False Kernel Detection

The `amneziawg-go` binary in `metaligh/amneziawg` falsely detects kernel AmneziaWG support on WSL2 because the standard WireGuard kernel module is loaded. It prints:

```
┌──────────────────────────────────────────────────────────────┐
│       Running amneziawg-go is not required because this      │
│       kernel has first class support for AmneziaWG.          │
└──────────────────────────────────────────────────────────────┘
```

Then exits immediately without creating the TUN. The standard WireGuard kernel module handles the interface instead — sending plain WireGuard handshakes, NOT Amnezia-obfuscated ones. All handshakes show `148 B sent, 0 B received` if the server requires AWG obfuscation.

**Fix**: Strip AWG params before `awg-quick up` (the bunker approach). See SKILL.md section "AmneziaWG Params — The Stripping Problem" for details.

## `awg setconf` Rejects AWG Config Lines

The `awg`/`wg setconf` command inside the container is the standard WireGuard tool, NOT an AmneziaWG-patched version. It rejects lines like:

```
Line unrecognized: `S3=47'
```

This causes `awg-quick up` to fail if the config file contains AWG params. Configs from AmneziaWG VPN providers always include these lines. The fix is to strip them with sed before applying (see start-awg.sh for the exact sed pattern).