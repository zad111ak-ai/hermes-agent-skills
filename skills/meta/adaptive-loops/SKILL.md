---
name: adaptive-loops
description: "Self-healing and self-learning loops for AI agents. Auto-recover from errors, remember what works."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Adaptive, Self-Healing, Learning, Error-Recovery, Automation]
    related_skills: [memory-guardian, skill-trigger-system]
---

# Adaptive Loops

Self-healing and self-learning system for AI agents. Automatically recovers from errors and remembers what works.

## Philosophy

> "The best agent is the one that learns from its mistakes without being told."

## Two Types of Loops

### 1. Self-Healing Loop
When a tool fails:
1. Detect error type (timeout, auth, rate limit, etc.)
2. Apply appropriate adapter (retry, rotate, proxy, etc.)
3. Retry with fix
4. Record result for future reference

### 2. Self-Learning Loop
After each task:
1. Record outcome (success/failure)
2. Note what worked/didn't work
3. Update trust scores for approaches
4. Apply successful patterns to future tasks

## Usage

### Pre-flight Check (before action)
```bash
# Check for known antipatterns
fact_store(action="reason", entities=["task_type", "past_error"])

# Check for known fixes
ls ~/.hermes/logs/adaptive/
```

### Post-action Capture (after result)
```bash
# Record success
cd ~/.hermes/learning_loop
python3 learning.py record coding "fixed proxy issue" true "groq/llama-3.1-8b-instant" "groq"

# Record failure
python3 learning.py record system_admin "config edit failed" false "auto/best-chat" "omniroute"
```

### Error-driven Adaptation
```python
# Automatic error handling
core.handle_error(tool="browser", error_type="timeout", msg="Connection reset", context={})
```

## Adaptation Strategies

| Error Type | Strategy | Example |
|------------|----------|---------|
| Timeout | Retry with backoff | `sleep 5 && retry` |
| Auth failure | Rotate credentials | Use different API key |
| Rate limit | Wait + retry | `sleep 60 && retry` |
| DPI block | Switch proxy | Hysteria2 → Tor |
| Model failure | Fallback model | auto/best-chat → groq |

## File Structure

```
~/.hermes/logs/adaptive/
├── browser_errors.jsonl
├── terminal_errors.jsonl
├── web_errors.jsonl
└── ...
```

## What NOT to Ask Dima

- "Can I record a fact?" → Just record it
- "Can I try an alternative?" → Just try it
- "Can I run handle_error?" → Just run it

## What TO Ask Dima

- Delete files/services
- Change systemd
- Install new software (pip install)
- Modify proxy/OmniRoute config
