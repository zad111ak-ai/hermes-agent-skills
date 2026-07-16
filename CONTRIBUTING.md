# 🤝 Как внести свой вклад

**Hermes Agent Skills** — open-source проект. Мы рады любому вкладу: новый скилл, исправление бага, улучшение документации.

---

## 📋 Что можно сделать

### 1. 💡 Предложить новый скилл
Если ты придумал скилл, который делает AI-агента умнее — напиши его!

### 2. 🐛 Исправить баг
Нашёл ошибку в существующем скилле? Исправь и отправь PR.

### 3. 📖 Улучшить документацию
Добавить примеры, исправить опечатки, перевести на другой язык.

### 4. 💬 Поделиться опытом
Расскажи в Issues/Discussions как используешь скиллы.

---

## 🛠 Как создать свой скилл

### Шаг 1: Скопируй шаблон
```bash
cp -r skills/meta/post-mortem-analyzer skills/my-new-skill
```

### Шаг 2: Отредактируй SKILL.md
Используй структуру из [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md).

### Шаг 3: Проверь
```bash
# Установи локально
cp -r skills/my-new-skill ~/.hermes/skills/

# Проверь что Hermes видит скилл
hermes skills list
```

### Шаг 4: Отправь PR
```bash
git checkout -b my-new-skill
git add skills/my-new-skill/
git commit -m "feat: добавил скилл my-new-skill"
git push origin my-new-skill
```

---

## 📏 Требования к скиллу

### Обязательно:
- ✅ Файл `SKILL.md` с YAML-фронтматом
- ✅ Описание на русском языке
- ✅ Теги вфронтмате
- ✅ Конкретные примеры (не абстракции)
- ✅ Правила "что делать" и "что НЕ делать"

### Желательно:
- 📊 Метрики ("экономит X% токенов")
- 🔧 Конкретные команды/код
- 📸 Скриншоты/примеры ДО/ПОСЛЕ
- 🧪 Тест-кейсы

### Запрещено:
- ❌ Реклама платных сервисов
- ❌ Захардкоженные ключи/API
- ❌ Опасные команды без предупреждений

---

## 🏷 Теги

Используй теги из списка:
```
memory, compression, meta, cost, optimization, security, 
quality, qa, communication, triggers, content, russia, 
proxy, bypass, api, tracking, budget
```

---

## 📝 Формат коммитов

```
feat: добавил скилл my-new-skill
fix: исправил триггер в session-hygiene-plus
docs: обновил README
refactor: оптимизировал cost-aware-orchestrator
```

---

## ❓ Вопросы?

Открой [Issue](https://github.com/zad111ak-ai/hermes-agent-skills/issues) — ответим!
