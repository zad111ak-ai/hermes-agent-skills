# AWG Container Debug Session (July 2026)

Session findings from debugging `metaligh/amneziawg:latest` on WSL2 after container kept recreating and AWG handshake didn't establish.

## Key Discovery: `awg setconf` Rejects AWG Params

The `awg` binary in `metaligh/amneziawg:latest` is the **stock wireguard-tools v1.0.20210914** — it does NOT understand AmneziaWG-specific config keys:

```
Line unrecognized: `MTU=1400'
Configuration parsing error
```

Even after stripping MTU, Address, DNS:
```
Line unrecognized: `S3=47'
Configuration parsing error
```

**Only standard WireGuard keys work**: `PrivateKey`, `PublicKey`, `PresharedKey`, `EndPoint`, `AllowedIPs`, `PersistentKeepalive`, `ListenPort`.

## What DOES Work: `awg set` for Basic Config

```bash
# Set private key
awg set wg0 private-key /dev/stdin <<< "base64key=="

# Add peer (one-liner)
awg set wg0 peer +PeerPublicKey= \
  preshared-key /dev/stdin <<< "preshared==" \
  allowed-ips 149.154.160.0/20 \
  endpoint nl07awg.server.com:60137 \
  persistent-keepalive 25
```

## UAPI Socket Parameter Testing

`amneziawg-go` (PID 15) creates a UAPI socket at `/run/amneziawg/wg0.sock`. AWG params can be tested directly via this socket using Python:

```python
import socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(3)
s.connect("/run/amneziawg/wg0.sock")
s.sendall(b"set=1\n")
s.sendall(b"jc=9\n")
s.sendall(b"\n")
resp = s.recv(4096)  # expects "errno=0" or "errno=-22"
```

**Tested results (errno=0 = supported, errno=-22 = rejected):**

| Param | Format | Result | Notes |
|-------|--------|--------|-------|
| `jc` | `jc=9` | ✅ errno=0 | Junk packet count |
| `jmin` | `jmin=30` | ❌ errno=-22 | Needs different format or name |
| `jmax` | `jmax=90` | ✅ errno=0 | Max junk packets |
| `s1` | `s1=110` | ✅ errno=0 | Split position |
| `s2` | `s2=120` | ✅ errno=0 | Split position |
| `s3` | `s3=47` | ❌ errno=-22 | Rejected |
| `s4` | `s4=23` | ❌ errno=-22 | Rejected |
| `h1` | `h1=7291435` | ❌ errno=-22 | Rejected |
| `h2` | `h2=602843917` | ❌ errno=-22 | Rejected |
| `h3` | `h3=1249871566` | ❌ errno=-22 | Rejected |
| `h4` | `h4=1781926002` | ❌ errno=-22 | Rejected |
| `i1` | `i1=` (empty) | ❌ errno=-22 | Needs raw bytes, not hex |
| `i2` | `i2=` (empty) | ❌ errno=-22 | same |
| `i3` | `i3=` (empty) | ❌ errno=-22 | same |

The `amneziawg-go` version in `metaligh/amneziawg:latest` only supports partial AWG params. Some params (jmin, s3, s4, h1-4, i1-3) are not recognized. This means **full Amnezia obfuscation cannot be achieved with this image version** on WSL2.

## `amneziawg-go` False Kernel Detection on WSL2

When `amneziawg-go` starts, it detects the standard WireGuard kernel module and prints:

```
┌──────────────────────────────────────────────────────────────┐
│       Running amneziawg-go is not required because this      │
│       kernel has first class support for AmneziaWG.
└──────────────────────────────────────────────────────────────┘
```

This is **false** — WSL2's kernel only has standard WireGuard, not AmneziaWG. The `amneziawg-go` process exits early, leaving the kernel module in charge. All handshakes are plain WireGuard.

**Impact**: 148 B sent, 0 B received — server ignores the handshake because it expects AWG obfuscation.

## Alternative Image: `sub1g/amneziawg-socks5`

Discovered during debugging. This image has **built-in SOCKS5 proxy** using `gost`:

```dockerfile
# Entrypoint (simplified):
sed -i 's/^DNS\s*=.*/#&/' /etc/amnezia/amneziawg/awg0.conf
awg-quick up awg0
gost -L="socks5://:1080?udp=true"
```

**Usage:**
```bash
docker run -d \
  --name awg \
  --privileged \
  -v /path/to/awg0.conf:/etc/amnezia/amneziawg/awg0.conf:ro \
  -p 127.0.0.1:1080:1080/tcp \
  sub1g/amneziawg-socks5
```

Expects config at `/etc/amnezia/amneziawg/awg0.conf` (not `wg0.conf`). Uses `sed` to comment out DNS line before `awg-quick up`. Still has the same `awg setconf` limitation as the base image since it likely extends `metaligh/amneziawg:latest`.

## `/etc/hosts` DNS Bypass for Telegram

When ALL_PROXY is not an option (dead proxy, wrong port), add Telegram IPs to `/etc/hosts`:

```bash
echo "149.154.167.220 api.telegram.org" | sudo tee -a /etc/hosts
```

This bypasses DNS resolution and forces direct TCP to the IP. If DPI blocks the IP, this won't help — but if DNS was the only problem (DNS poisoning returning fake 8.6.112.x IPs), it works.

## Docker Bridge Routing (no proxy needed)

If the `awg` container has wg0 up with `AllowedIPs=149.154.160.0/20`, traffic from the WSL host can be routed through the Docker bridge directly:

```bash
# Find container IP
docker inspect awg --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
# → 172.17.0.2

# Add route for Telegram subnet through container
sudo ip route add 149.154.167.220 via 172.17.0.2 dev docker0
```

This works because the container's wg0 interface already has a route `149.154.160.0/20 dev wg0` — traffic arriving at the container via Docker bridge is forwarded out through wg0.

**Pitfall**: `ip route add` requires root (sudo). In WSL without a TTY, use `cmd.exe /c "wsl -u root -e ip route add ..."`.

**Pitfall**: The route may be overwritten by Docker/network manager. Check with `ip route get 149.154.167.220` before assuming it works.

## Container Recreation Loop

If the `awg` container keeps being recreated (every 60s or so), the culprit is usually:
1. `docker compose up -d` being run repeatedly (auto or manual) — recreates container from pristine image
2. `restart: unless-stopped` combined with health check failure — container exits and gets recreated
3. Systemd service managing the container

**Check**: `docker inspect awg --format '{{.Created}}'` — if the timestamp keeps changing, something is recreating it. Any changes made via `docker exec` (installing packages, modifying configs) will be **lost on every recreate**.

To make changes permanent, either:
- Modify the mounted config file on the host (survives recreates)
- Build a custom Docker image with changes baked in
- Fix the `docker-compose.yml` entrypoint correctly (use `|` literal block, not `>` folded scalar)

## Stale ALL_PROXY Diagnosis

The Hermes gateway inherits `ALL_PROXY`/`HTTPS_PROXY` from the shell environment. A stale proxy on a wrong port/address causes cryptic errors:

| Symptom | Likely Cause |
|---------|-------------|
| `ProtocolError('Malformed reply')` | ALL_PROXY points to a non-SOCKS service (e.g. HTTP server on SOCKS port) |
| `httpx.ReadError:` | ALL_PROXY connection reset or timeout |
| `ClientConnectorError: Network is unreachable` | ALL_PROXY points to a dead IP/port, DNS resolved to localhost |
| `ClientConnectorDNSError: Try again` | ALL_PROXY DNS resolution fails (socks5 vs socks5h distinction) |

**Debug:**
```bash
# What proxy vars are set?
env | grep -i proxy

# Is the proxy actually listening?
ss -tlnp | grep -E '1080|8080'

# Test direct (bypass proxy)
curl --noproxy '*' -s --max-time 5 https://api.telegram.org

# Test through proxy
curl -x socks5h://127.0.0.1:1080 -s --max-time 5 https://api.telegram.org
```

**Fix:**
```bash
unset ALL_PROXY HTTPS_PROXY HTTP_PROXY
systemctl --user restart hermes-gateway
```

To find the source of a persistent proxy env:
```bash
grep -rn '8080\|ALL_PROXY\|HTTPS_PROXY' /etc/environment ~/.bashrc ~/.profile /etc/profile.d/ ~/.pam_environment 2>/dev/null
```
