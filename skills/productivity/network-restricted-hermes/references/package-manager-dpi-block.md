# Package Manager DPI Blocking

## Diagnosis (July 2026)

In this environment, ALL external HTTPS registries are DPI-blocked, not just AI providers:

| Registry | Blocked? | Code | Notes |
|----------|----------|------|-------|
| `pypi.org` | ❌ | 000 | pip install impossible |
| `files.pythonhosted.org` | ❌ | 000 | Python package downloads |
| `registry.npmjs.org` | ❌ | 000 | npm install impossible |
| `cdn.jsdelivr.net` | ❌ | 000 | CDN package delivery |
| `unpkg.com` | ❌ | 000 | CDN package delivery |
| `github.com` | ❌ | FAIL | git clone, API, releases |
| `api.telegram.org` | ❌ | 000 (direct) | But works via AWG route |

**Even OmniRoute (localhost:20128) returns 000** for external registries — it doesn't proxy them.

## What Works

- **Local registries** — `localhost:20128` (OmniRoute), `localhost:*` (any local service)
- **Telegram** — via `ip route 149.154.167.220 via docker0` (AWG container routing)
- **Docker images** — via registry mirrors (`mirror.gcr.io`, `docker.m.daocloud.io`, etc.)
- **OC/OpenCode** — proprietary tunnel bypasses DPI

## Workarounds

### 1. Offline wheels

```bash
# On non-blocked machine:
pip download <package> -d /tmp/wheels/ && tar czf wheels.tar.gz /tmp/wheels/
# On blocked machine:
tar xzf wheels.tar.gz && pip install --no-index --find-links=/tmp/wheels/ <package>
```

### 2. SOCKS5 through tunnel

If AWG container had a working SOCKS5 daemon:
```bash
pip install --proxy socks5://127.0.0.1:1080 <package>
npm config set proxy socks5://127.0.0.1:1080
```
**Caveat**: `awg-socks` container never worked — port 1080 is mapped but nothing listens.

### 3. Check what's pre-installed

```bash
python3 -c "import <module>" 2>&1 && echo "EXISTS" || echo "MISSING"
pip3 list | grep <package>
```

## Current State

No external registries accessible. Need offline wheels, working proxy, or Docker with pre-pulled images.
