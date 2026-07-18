# Telegram Gateway Crash Loop Pattern

## Signature

Gateway process exits repeatedly. `pgrep -f gateway` shows it's alive, but Telegram
doesn't respond to messages. The user asks "помер ?" ("is it dead?").

### Log evidence

**gateway_state.json** — lies about Telegram:
```json
{
  "platforms": {
    "telegram": {
      "state": "connected",
      "error_code": null,
      "error_message": null
    }
  }
}
```

**gateway-exit-diag.log** — real story (multiple cycles):
```
{"tag": "gateway.start", "pid": 25969}
{"tag": "asyncio.run.returned", "success": false}
{"tag": "gateway.exit_nonzero", "pid": 25969}
```

**gateway.log** — root cause:
```
WARNING gateway.platform_registry: Platform 'Telegram' requirements not met
  (pip install 'hermes-agent[telegram]')
ERROR gateway.run: Platform 'telegram' is registered but adapter creation
  failed (check dependencies and config)
WARNING gateway.run: No adapter available for telegram
```

Then systemd sends SIGTERM → gateway exits with code 1 (intentional) →
`Restart=on-failure` starts it again → loop.

## Why gateway_state says "connected" when it's not

The gateway records platform state optimistically during platform registration,
*before* adapter creation. If the adapter fails (missing dependency, bad config),
the state file isn't updated — it stays at the initial "connected" value from
platform setup. This is a known artifact of the state persistence order.

**Do NOT trust gateway_state.json for Telegram health.** Always verify with:
- `pgrep -af gateway` — is the process alive?
- `journalctl --user -u hermes-gatework --no-pager -n 20 | grep -i "telegram\|adapter\|requirements"` — adapter OK?
- `python3 -c "import importlib; m='hermes_plugins.platforms.telegram.adapter'; print('OK' if importlib.util.find_spec(m) else 'MISSING')"` — deps installed?

## Quick diagnostic (помер check)

```bash
# 1. Process alive?
pgrep -af gateway
# → PID /.../main.py gateway run  ← alive (or nothing → dead)

# 2. State file truth?
python3 -c "import json; d=json.load(open('$HOME/.hermes/gateway_state.json')); tg=d.get('platforms',{}).get('telegram',{}); print('state:', tg.get('state')); print('error:', tg.get('error_message'))"

# 3. Recent gateway log for adapter errors
tail -30 ~/.hermes/logs/gateway.log | grep -i "telegram\|requirements\|adapter"

# 4. Quick Telegram API test (sticky fallback)
TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)
curl -s --max-time 10 \
  --resolve "api.telegram.org:443:149.154.167.220" \
  "https://api.telegram.org/bot${TOKEN}/getMe"
# → {"ok":true,"result":{"id":...}}  ← bot API alive
# → curl: (28) Connection timed out   ← network dead
```

## Root cause: missing dependency

```bash
# Check if telegram plugin is importable
python3 -c "import hermes_plugins.platforms.telegram.adapter; print('OK')" 2>&1
# → ModuleNotFoundError → missing deps

# Fix
pip install 'hermes-agent[telegram]'
systemctl --user restart hermes-gateway
```

## Crash loop pattern details

| Variable | Typical value | Meaning |
|----------|---------------|---------|
| `asyncio.run.returned success` | `false` | Async loop returned abnormally |
| `gateway.exit_nonzero` | present | process exited with code != 0 |
| `SystemExit(0)` | present (same cycle) | Clean Python shutdown exits code 0 |
| `under_systemd` | `yes` | Managed by systemd user service |
| `Restart=on-failure` | configured | systemd restarts on every exit≠0 |

The paradox: `SystemExit(0)` in the Python traceback BUT `exit_nonzero` in the
gateway wrapper. This happens because:
1. `start_gateway()` raises `SystemExit(0)` to cleanly unwind the async loop
2. `run_gateway()` catches it and calls `sys.exit(1)` to signal systemd restart

So from Python's perspective: clean exit (0). From systemd's perspective:
non-zero (1). This is by design — the gateway exits on purpose but tells systemd
"not ready, retry me".

**When the user asks "помер ?"**, the answer is:
- If pgrep shows a PID: gateway process IS alive, but Telegram may not be functional
- Check gateway.log for adapter errors (missing deps most likely)
- gateway_state.json showing "connected" does NOT mean Telegram works
- Short answer: "нет, но телега не работает — не хватает hermes-agent[telegram]"
