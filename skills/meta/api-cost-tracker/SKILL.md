---
name: api-cost-tracker
description: "Трекер расходов на API в реальном времени. Логирование каждого вызова, подсчёт стоимости, алерты при превышении лимита. Чтобы не проснуться с пустым балансом."
tags: ["cost", "tracking", "budget", "monitoring", "api"]
---

# API Cost Tracker — Трекер расходов на API

Активировать: при каждой задаче, которая делает API-вызовы (LLM, парсинг, генерация).

**Цель:** Знать сколько тратишь. Не проснуться с $0 на балансе.

---

## Зачем

AI-агенты сжигают токены молча. Ты не замечаешь как 100K токенов пролетают за одну задачу. Через неделю — сюрприз: баланс на нуле.

---

## Текущая ценовая карта (2025)

| Провайдер | Модель | Вход | Выход | 100K токенов |
|-----------|--------|------|-------|--------------|
| Groq | Llama 3.1 8B | 0.05$ | 0.08$ | **0.013$** |
| OpenRouter | Gemini 2.5 Flash | 0.15$ | 0.60$ | **0.075$** |
| OpenRouter | Claude Sonnet 4 | 3.00$ | 15.00$ | **1.80$** |
| DeepSeek | DeepSeek V3 | 0.14$ | 0.28$ | **0.042$** |
| GLM-4 | Zhipu AI | 0.07¥ | 0.07¥ | **0.007¥** |

---

## Логирование

```python
import time
from dataclasses import dataclass

@dataclass
class APICall:
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    timestamp: float

class CostTracker:
    def __init__(self, budget_limit: float = 10.0):
        self.calls = []
        self.budget_limit = budget_limit
        self.total_cost = 0.0
    
    def log_call(self, provider, model, input_tokens, output_tokens, cost):
        call = APICall(provider, model, input_tokens, output_tokens, cost, time.time())
        self.calls.append(call)
        self.total_cost += cost
        
        if self.total_cost > self.budget_limit:
            print(f"🚨 БЮДЖЕТ ПРЕВЫШЕН: ${self.total_cost:.2f} / ${self.budget_limit:.2f}")
    
    def today_summary(self):
        today = time.time() - 86400
        today_calls = [c for c in self.calls if c.timestamp > today]
        total = sum(c.cost for c in today_calls)
        return f"Сегодня: {len(today_calls)} вызовов, ${total:.4f}"
```

---

## Алерты

```bash
# Проверь баланс перед задачей
grep -i "balance\|credit\|remaining" ~/.provider_status

# Установи лимит в .env
BUDGET_DAILY_LIMIT=5.00
BUDGET_MONTHLY_LIMIT=50.00
```

---

## Правила

1. **ВСЕГДА** логируй каждый API-вызов
2. **ПРОВЕРЯЙ** баланс перед дорогими задачами
3. **ИСПОЛЬЗУЙ** дешёвые модели для простых задач (Groq, DeepSeek)
4. **ДЕЛАГАЙ** на дешёвые модели когда возможно
5. **СОХРАНЯЙ** логи — потом можно проанализировать расходы
