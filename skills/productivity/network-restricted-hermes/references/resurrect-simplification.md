# Resurrect Script Simplification (July 2026)

## Problem

`resurrect.sh` (cron, every minute) was in a death loop:
- Checked SOCKS5 on port 1080 → SOCKS5 container `awg-socks` never started (`python:3.12-slim` crashed) → FAIL
- Checked OpenRouter/Telegram through SOCKS5 → both returned `000` → "FULL MELTDOWN"
- Hard reboot: `sudo reboot` → machine reboots → resurrect runs at boot → same loop
- 20+ reboots in 20 minutes

## Root Cause

**SOCKS5 was unnecessary** in the current architecture:
- OmniRoute (localhost:20128) handles all AI API proxying
- Telegram works through direct `ip route 149.154.167.220 via docker0` (AWG container routing)
- SOCKS5 was legacy from before OmniRoute existed

## Changes Made

| Section | Before | After |
|---------|--------|-------|
| AWG check | `awg_up && socks_up` — checked port 1080 | `awg_up` only — no SOCKS5 check |
| AWG restart | `docker rm -f awg awg-socks` + `pkill haproxy` | `docker rm -f awg` only |
| HAProxy | Full section: start haproxy config, check port 8080 | Commented out (not needed) |
| Health check | 5 external curls through SOCKS5 → reboot if all fail | 1 local curl to `localhost:20128` + `systemctl is-active hermes-gateway` |
| send_tg_notify | `curl -x socks5h://127.0.0.1:1080` | `curl` without proxy (uses TG route via docker0) |
| Reboot | `sudo reboot` on meltdown | Removed entirely — max restart AWG |

## Current resurrect.sh Health Check Logic

```bash
# 1. Check OmniRoute
OR_LOCAL=$(curl -s -m 5 http://localhost:20128/v1/models -o /dev/null -w "%{http_code}")
# 2. Check gateway
GW=$(systemctl --user is-active hermes-gateway 2>/dev/null || echo "inactive")

# If OmniRoute dead → restart omniroute → if still dead → restart AWG
# If gateway dead → systemctl restart hermes-gateway
# NEVER reboots
```

## Verification

```bash
tail -f ~/resurrect.log | grep -v "FULL MELTDOWN\|reboot"
# Expected log:
# 📊 Health: OmniRoute=200 Gateway=active
```
