# 🧠 Hermes Agent Skills — Коллекция скиллов для AI-агента

**AI, который думает о своей эффективности.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 Философия

AI-агенты склонны к когнитивным искажениям:.analysis paralysis, analysis paralysis, analysis paralysis... и они этого не осознают.

**Hermes Agent Skills** — это набор системных промптов, которые заставляют AI-агента думать о своей эффективности:

- 💰 **Экономить токены** — не тратить $5 на задачу за $0.01
- 🧠 **Помнить контекст** — не забывать что делал 5 минут назад
- 🔒 **Быть безопасным** — не ломать продакшн
- 📊 **Отслеживать расходы** — не просыпаться с нулём на балансе

---

## 📦 Скиллы

### 🧠 Meta (мышление агента)

| Скилл | Описание | Экономия |
|-------|----------|----------|
| [memory-compactor](skills/meta/memory-compactor/) | Сжатие контекста — не тратить токены на старое | ~50% токенов |
| [post-mortem-analyzer](skills/meta/post-mortem-analyzer/) | Анализ ошибок — не повторять одни и те же баги | ~30% повторных ошибок |
| [reflexive-trigger-boost](skills/meta/reflexive-trigger-boost/) | Самоанализ триггеров — понимать когда активироваться | ~20% релевантности |
| [skill-trigger-system](skills/meta/skill-trigger-system/) | Умные триггеры — активировать скилл в нужный момент | ~40% пропущенных задач |
| [api-cost-tracker](skills/meta/api-cost-tracker/) | Трекер расходов на API в реальном времени | ~95% от сюрпризов с балансом |

### ⚙️ Productivity (эффективность)

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

### 🔒 Security (безопасность)

| Скилл | Описание |
|-------|----------|
| [security-audit](skills/security/security-audit/) | Аудит безопасности перед деплоем |

### 📝 Content (контент)

| Скилл | Описание |
|-------|----------|
| [content-pipeline](skills/content/content-pipeline/) | Пайплайн создания контента для Telegram |

---

## 🚀 Быстрый старт

### 1. Установи Hermes Agent
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### 2. Скопируй скиллы
```bash
# Клонируй репозиторий
git clone https://github.com/zad111ak-ai/hermes-agent-skills.git

# Скопируй нужные скиллы
cp -r hermes-agent-skills/skills/meta/* ~/.hermes/skills/
cp -r hermes-agent-skills/skills/productivity/* ~/.hermes/skills/
```

### 3. Проверь
```bash
hermes skills list
```

---

## 📚 Примеры

Смотри [examples/BEFORE_AFTER.md](examples/BEFORE_AFTER.md) — наглядные сравнения ДО и ПОСЛЕ применения скиллов.

---

## 🤝 Как внести вклад

Читай [CONTRIBUTING.md](CONTRIBUTING.md) — там пошаговый гайд.

### Быстрый путь:
1. Скопируй [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
2. Напиши свой скилл
3. Отправь PR

---

## 📂 Структура

```
hermes-agent-skills/
├── README.md                    # Этот файл
├── CONTRIBUTING.md              # Гайд для контрибьюторов
├── SKILL_TEMPLATE.md            # Шаблон скилла
├── examples/
│   └── BEFORE_AFTER.md          # Примеры ДО/ПОСЛЕ
├── skills/
│   ├── meta/                    # Мышление агента
│   ├── productivity/            # Эффективность
│   ├── security/                # Безопасность
│   └── content/                 # Контент
└── LICENSE                      # MIT
```

---

## 💸 Поддержать проект

Проект развивается силами энтузиастов. Если скиллы сэкономили вам токены и нервы, вы можете поддержать развитие репозитория ☕️

### Криптовалюта

| Сеть | Адрес |
|------|-------|
| **BTC** | `bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j` |
| **ETH** | `0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3` |
| **USDT (TON)** | `UQAoI2i8P9sQpBCm4nKXvLkNf8dGmVxYzJ7B3sT9wR2eK5p` |
| **SOL** | `99EtqBVmPxzYrzLv8fDgKfBpZcVwKqVxJ7B3sT9wR2eK` |

### Другие способы

| Платформа | Ссылка |
|-----------|--------|
| **Boosty** | [boosty.to/josephpost](https://boosty.to/josephpost) |
| **GitHub Sponsors** | [github.com/sponsors/zad111ak-ai](https://github.com/sponsors/zad111ak-ai) |

---

## 📄 Лицензия

MIT License — используй как хочешь.

---

## 🔗 Ссылки

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — основной фреймворк
- [Hermes Docs](https://hermes-agent.nousresearch.com/docs) — документация
- [Issues](https://github.com/zad111ak-ai/hermes-agent-skills/issues) — баги и идеи
