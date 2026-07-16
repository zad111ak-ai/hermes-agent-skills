---
name: security-audit
description: "Аудит безопасности кода перед деплоем: проверка секретов, SQL injection, path traversal, зависимостей. Не дай агенту уронить продакшн."
tags: ["security", "audit", "code-review", "production"]
---

# Security Audit — Аудит безопасности

Активировать: перед деплоем любого кода, который работает с данными/сетью.

**Цель:** Не выпустить код с дырами в безопасности.

---

## Зачем

AI-агенты пишут быстро. Слишком быстро. Они забывают экранировать SQL, хардкодят ключи, пропускают path traversal. Один забытый `os.path.join(user_input, ...)` — и у тебя RCE.

---

## Чек-лист аудита

### 1. 🔑 Секреты и ключи
```bash
# Найти захардкоженные ключи
grep -rn "api_key\|token\|secret\|password" --include="*.py" .
grep -rn "sk-\|ghp_\|gho_" --include="*.py" .
```

**Правила:**
- ❌ НИКОГДА не хардкодь ключи в коде
- ✅ ВСЕГДА используй `.env` + `os.getenv()`
- ✅ ВСЕГДА добавляй `.env` в `.gitignore`

### 2. 🗄 SQL Injection
```python
# ❌ ПЛОХО — string formatting
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ ХОРОШО — параметризованный запрос
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

**Правила:**
- ✅ ВСЕГДА используй параметризованные запросы
- ❌ НИКОГДА не используй f-строки/format() для SQL
- ✅ Используй ORM когда возможно (SQLAlchemy, Tortoise)

### 3. 📁 Path Traversal
```python
# ❌ ПЛОХО — пользователь управляет путём
file_path = os.path.join(upload_dir, user_filename)

# ✅ ХОРОШО — валидация и нормализация
safe_name = os.path.basename(user_filename)
file_path = os.path.join(upload_dir, safe_name)
if not os.path.abspath(file_path).startswith(os.path.abspath(upload_dir)):
    raise ValueError("Path traversal detected")
```

**Правила:**
- ✅ ВСЕГДА используй `os.path.basename()` для имён файлов
- ✅ ПРОВЕРЯЙ что путь внутри разрешённой директории
- ❌ НИКОГДА не доверяй пользовательский ввод для путей

### 4. 🌐 SSRF (Server-Side Request Forgery)
```python
# ❌ ПЛОХО — URL от пользователя
requests.get(user_url)

# ✅ ХОРОШО — whitelist и валидация
ALLOWED_HOSTS = ["api.example.com", "cdn.example.com"]
parsed = urlparse(user_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("Host not allowed")
```

### 5. 📦 Зависимости
```bash
# Проверь на известные уязвимости
pip-audit
safety check
```

**Правила:**
- ✅ Регулярно обновляй зависимости
- ✅ Используй `pip-audit` перед деплоем
- ❌ Не ставь пакеты без проверки репутации

---

## Формат отчёта

```
🔒 Security Audit Report
━━━━━━━━━━━━━━━━━━━━━━
✅ Секреты: не найдены
✅ SQL Injection: параметризованные запросы
⚠️ Path Traversal: найдена potential проблема в utils/file_handler.py:42
✅ Зависимости: 0 known vulnerabilities

Общий статус: ✅ PASS (с рекомендациями)
```
