# 🧠 Hermes Agent Skills — Коллекция скиллов для AI-агента / Skill Collection for AI Agents

**AI, который думает о своей эффективности.** / **AI that thinks about its own efficiency.**

<p align="center">
  <a href="#russian">🇷🇺 Русский</a> &nbsp;|&nbsp; <a href="#english">🇬🇧 English</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/zad111ak-ai/hermes-agent-skills?style=social)](https://github.com/zad111ak-ai/hermes-agent-skills)
[![GitHub contributors](https://img.shields.io/github/contributors/zad111ak-ai/hermes-agent-skills)](https://github.com/zad111ak-ai/hermes-agent-skills/graphs/contributors)

---

<a id="russian"></a>
## 🇷🇺 Русская версия

### 🎯 Философия

AI-агенты склонны к когнитивным искажениям: analysis paralysis, analysis paralysis, analysis paralysis... и они этого не осознают.

**Hermes Agent Skills** — это набор системных промптов, которые заставляют AI-агента думать о своей эффективности:

- 💰 **Экономить токены** — не тратить $5 на задачу за $0.01
- 🧠 **Помнить контекст** — не забывать что делал 5 минут назад
- 🔒 **Быть безопасным** — не ломать продакшн
- 📊 **Отслеживать расходы** — не просыпаться с нулём на балансе

### 📦 Скиллы

#### 🧠 Meta (мышление агента)

| Скилл | Описание | Экономия |
|-------|----------|----------|
| [memory-compactor](skills/meta/memory-compactor/) | Сжатие контекста — не тратить токены на старое | ~50% токенов |
| [post-mortem-analyzer](skills/meta/post-mortem-analyzer/) | Анализ ошибок — не повторять одни и те же баги | ~30% повторных ошибок |
| [reflexive-trigger-boost](skills/meta/reflexive-trigger-boost/) | Самоанализ триггеров — понимать когда активироваться | ~20% релевантности |
| [skill-trigger-system](skills/meta/skill-trigger-system/) | Умные триггеры — активировать скилл в нужный момент | ~40% пропущенных задач |
| [api-cost-tracker](skills/meta/api-cost-tracker/) | Трекер расходов на API в реальном времени | ~95% от сюрпризов с балансом |

#### ⚙️ Productivity (эффективность)

| Скилл | Описание | Экономия |
|-------|----------|----------|
| [agent-communication](skills/productivity/agent-communication/) | Межагентное общение — координация без хаоса | ~25% дублирования |
| [auto-qa-gates](skills/productivity/auto-qa-gates/) | Автоматический QA — проверка качества до деплоя | ~40% багов |
| [cost-aware-orchestrator](skills/productivity/cost-aware-orchestrator/) | Выбор дешёвой модели для простых задач | ~95% расходов |
| [decision-framework](skills/productivity/decision-framework/) | Структурированные решения — не теряться в вариантах | ~30% analysis paralysis |
| [reflection-qa](skills/productivity/reflection-qa/) | Рефлексия — проверка своих ответов | ~35% ошибок |
| [session-hygiene-plus](skills/productivity/session-hygiene-plus/) | Гигиена сессий — уборка контекста | ~87% токенов |
| [tool-proficiency-tracker](skills/productivity/tool-proficiency-tracker/) | Трекинг инструментов — знать что работает | ~20% лишних вызовов |
| [russia-hacks](skills/productivity/russia-hacks/) | Обход DPI из РФ: прокси, Hysteria 2, альтернативы | 🔓 Доступ к API |

#### 🔒 Security (безопасность)

| Скилл | Описание |
|-------|----------|
| [security-audit](skills/security/security-audit/) | Аудит безопасности перед деплоем |

#### 📝 Content (контент)

| Скилл | Описание |
|-------|----------|
| [content-pipeline](skills/content/content-pipeline/) | Пайплайн создания контента для Telegram |

### 🚀 Быстрый старт

```bash
# 1. Установи Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Клонируй и скопируй скиллы
git clone https://github.com/zad111ak-ai/hermes-agent-skills.git
cp -r hermes-agent-skills/skills/meta/* ~/.hermes/skills/
cp -r hermes-agent-skills/skills/productivity/* ~/.hermes/skills/

# 3. Проверь
hermes skills list
```

### 📚 Примеры

Смотри [examples/BEFORE_AFTER.md](examples/BEFORE_AFTER.md) — наглядные сравнения ДО и ПОСЛЕ.

### 🤝 Как внести вклад

Читай [CONTRIBUTING.md](CONTRIBUTING.md). Быстрый путь:
1. Скопируй [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
2. Напиши свой скилл
3. Отправь PR

### 📂 Структура

```
hermes-agent-skills/
├── README.md / CONTRIBUTING.md / SKILL_TEMPLATE.md
├── examples/BEFORE_AFTER.md
├── skills/{meta, productivity, security, content}/
└── LICENSE
```

---

<a id="english"></a>
## 🇬🇧 English Version

### 🎯 Philosophy

AI agents are prone to cognitive biases: analysis paralysis, analysis paralysis, analysis paralysis... and they don't even realize it.

**Hermes Agent Skills** is a set of system prompts that force AI agents to think about their own efficiency:

- 💰 **Save tokens** — don't spend $5 on a $0.01 task
- 🧠 **Remember context** — don't forget what you did 5 minutes ago
- 🔒 **Stay safe** — don't break production
- 📊 **Track costs** — don't wake up with a zero balance

### 📦 Skills

#### 🧠 Meta (Agent Cognition)

| Skill | Description | Savings |
|-------|-------------|---------|
| [memory-compactor](skills/meta/memory-compactor/) | Context compression — stop spending tokens on stale info | ~50% tokens |
| [post-mortem-analyzer](skills/meta/post-mortem-analyzer/) | Error analysis — stop repeating the same bugs | ~30% repeat errors |
| [reflexive-trigger-boost](skills/meta/reflexive-trigger-boost/) | Trigger self-analysis — understand when to activate | ~20% relevance |
| [skill-trigger-system](skills/meta/skill-trigger-system/) | Smart triggers — activate the right skill at the right time | ~40% missed tasks |
| [api-cost-tracker](skills/meta/api-cost-tracker/) | Real-time API cost tracker | ~95% balance surprises |

#### ⚙️ Productivity

| Skill | Description | Savings |
|-------|-------------|---------|
| [agent-communication](skills/productivity/agent-communication/) | Inter-agent communication — coordination without chaos | ~25% duplication |
| [auto-qa-gates](skills/productivity/auto-qa-gates/) | Automated QA — quality checks before deploy | ~40% bugs |
| [cost-aware-orchestrator](skills/productivity/cost-aware-orchestrator/) | Choose cheap models for simple tasks | ~95% costs |
| [decision-framework](skills/productivity/decision-framework/) | Structured decisions — stop getting lost in options | ~30% analysis paralysis |
| [reflection-qa](skills/productivity/reflection-qa/) | Reflection — verify your own answers | ~35% errors |
| [session-hygiene-plus](skills/productivity/session-hygiene-plus/) | Session hygiene — clean up context | ~87% tokens |
| [tool-proficiency-tracker](skills/productivity/tool-proficiency-tracker/) | Tool tracking — know what works | ~20% extra calls |
| [russia-hacks](skills/productivity/russia-hacks/) | DPI bypass from Russia: proxies, Hysteria 2, alternatives | 🔓 API access |

#### 🔒 Security

| Skill | Description |
|-------|-------------|
| [security-audit](skills/security/security-audit/) | Security audit before deployment |

#### 📝 Content

| Skill | Description |
|-------|-------------|
| [content-pipeline](skills/content/content-pipeline/) | Content creation pipeline for Telegram |

### 🚀 Quick Start

```bash
# 1. Install Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Clone and copy skills
git clone https://github.com/zad111ak-ai/hermes-agent-skills.git
cp -r hermes-agent-skills/skills/meta/* ~/.hermes/skills/
cp -r hermes-agent-skills/skills/productivity/* ~/.hermes/skills/

# 3. Verify
hermes skills list
```

### 📚 Examples

See [examples/BEFORE_AFTER.md](examples/BEFORE_AFTER.md) — side-by-side BEFORE/AFTER comparisons.

### 🤝 Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Quick path:
1. Copy [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
2. Write your skill
3. Submit a PR

---

## 💸 Support the Project / Поддержать проект

Если эти скиллы сэкономили вам токены и нервы — поддержите проект ☕️

| Сеть / Network | Адрес / Address |
|---|---|
| **BTC** | `bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j` |
| **ETH** | `0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3` |
| **USDT (TON)** | `UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP` |
| **SOL** | `99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK` |

---

## 📄 License / Лицензия

MIT License — use however you want. / Используй как хочешь.

## 🔗 Links / Ссылки

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — main framework / основной фреймворк
- [Hermes Docs](https://hermes-agent.nousresearch.com/docs) — documentation / документация
- [Issues](https://github.com/zad111ak-ai/hermes-agent-skills/issues) — bugs & ideas / баги и идеи
