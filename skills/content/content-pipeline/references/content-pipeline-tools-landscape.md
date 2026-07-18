# Content Pipeline Tools & Self-Improving Loop

Результаты исследования GitHub landscape (2026-07) — что существует, что подходит под наш стек, как построить self-improving цикл.

## Top GitHub Repos (сравнение)

| Репозиторий | ⭐ | Язык | Наш стек? | Self-improving? |
|---|---|---|---|---|
| **IgorShadurin/app.yumcut.com** | 715 | TypeScript | ❌ (Next.js, не Python) | ❌ |
| **ChaitanyaEswarRajeshJakki/gemini-youtube-automation** | 298 | Python | ⚠️ (moviepy, Gemini; нет Pollinations) | ❌ |
| **YoussefBechara/AI-Automated-Short-Video-Generator-Editor-Uploader-For-Views** | 21 | Python | ⚠️ (LLM → TTS → видео → upload, но нет crossfade/zoompan) | ❌ |
| **indiser/ViralContent-Factory** | 12 | Python | ✅ (edge-tts, moviepy, LLM) Reddit → TikTok | ❌ |
| **vovuhuydeveloper/agent-content-kit** | 9 | Python | ⚠️ (multi-agent, Telegram, Playwright) | ❌ |
| **obendaoud/faceless-video-pipeline** | 0 | Python | ✅✅ (Claude + Flux + Edge-TTS + FFmpeg) | ❌ |
| **chimu15/ai-content-evaluator-loop** | 0 | n8n | ❌ (n8n workflow) | ✅ (LLM-as-a-judge) |

### Лучший по стеку: obendaoud/faceless-video-pipeline
- Claude + Flux + Edge-TTS + FFmpeg — почти наш стек
- 0 звёзд, новый, но архитектурно близок
- README на французском/английском
- Ссылка: https://github.com/obendaoud/faceless-video-pipeline

### Самый зрелый: gemini-youtube-automation (298⭐)
- Полностью автономный: Idea → Script → Visuals → Upload
- Python + moviepy + Gemini
- Есть CI/CD (GitHub Actions) для ежедневного запуска
- Ссылка: https://github.com/ChaitanyaEswarRajeshJakki/gemini-youtube-automation

## Self-Improving Loop — Методология

Готового self-improving пайплайна на GitHub нет. Концепция только emerging. Вот как построить:

### 1. LLM-as-a-Judge (как chimu15/ai-content-evaluator-loop)
```
После генерации → LLM оценивает:
- Качество 0-10 по критериям: визуал, субтитры, синхронизация, вовлечение
- Записывает метрики в БД (SQLite/tracker.json)
- Если score < 7 → корректирует промпты и перезапускает
- Если score >= 7 → публикует
```

### 2. A/B тестирование контента
```
- Генерировать 2-3 варианта скрипта/промпта
- Публиковать лучший по LLM-judge
- Со временем LLM запоминает что работает → промпты эволюционируют
```

### 3. Feedback loop from analytics
```
- После публикации: собирать views/retention/engagement
- Сравнивать с историческими данными
- Анализировать что сработало (тема, стиль, длина)
- Корректировать pipeline params для следующего цикла
```

### 4. Простая реализация (наш стек)
```python
# В конце pipeline.py:
def self_improve(metrics: dict, history_path="~/content_output/quality_history.json"):
    """Записывает метрики и корректирует параметры для следующего запуска"""
    history = json.load(open(history_path)) if os.path.exists(history_path) else []
    history.append(metrics)
    
    # LLM-as-a-judge оценивает качество
    score = llm_judge(f"Оцени видео от 0-10: {metrics}")  # через OmniRoute
    
    # Если плохо — корректируем промпты
    if score < 7:
        prompt_corrections = llm_advice(f"Что улучшить: {metrics}")
        save_corrections(prompt_corrections)  # влияет на следующий запуск
    
    json.dump(history[-50:], open(history_path, "w"))  # храним 50 последних
```

### Ключевые выводы
1. **Готового решения нет** — надо строить самому поверх нашего pipeline.py
2. **LLM-as-a-judge** — самый доступный подход (OmniRoute 680+ моделей)
3. **Content-pipeline у нас уже лучше многих** — Ken Burns + crossfade + Pollinations + edge-tts + whisper — это feature-rich решение
4. **Приоритет апгрейда** — добавить self-improving loop (оценка → запись → корректировка)

## Как искать новые инструменты
```bash
# Через Hysteria HTTP прокси:
curl -s --proxy http://127.0.0.1:1082 \
  "https://api.github.com/search/repositories?q=faceless+video+shorts+pipeline&sort=stars&per_page=5" \
  -H "Accept: application/vnd.github+json" | python3 -m json.tool

# Для self-improving специфично:
curl -s --proxy http://127.0.0.1:1082 \
  "https://api.github.com/search/repositories?q=ai+content+evaluator+loop+quality+judge&sort=stars&per_page=5" \
  -H "Accept: application/vnd.github+json" | python3 -m json.tool
```

Прокси: HTTP `127.0.0.1:1082` или SOCKS5 `127.0.0.1:1081` (SOCKS5 требует `--proxy socks5h://` для DNS через прокси).
