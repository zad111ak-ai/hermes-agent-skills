# Crossfade (xfade) между кадрами в ffmpeg

## Когда нужно

При генерации слайд-шоу из N изображений (Pollinations, Pillow, и т.д.) в Pipeline v3. Вместо
резких стыков между кадрами — плавный fade-переход.

## Формула offset

```python
seg_frames = int(duration_per_frame * fps)  # длительность кадра в кадрах
fade_duration = min(30, seg_frames // 4)     # ~1с или 1/4 кадра
# offset для i-го перехода (i начинается с 1):
offset_frames = i * (seg_frames - fade_duration)
# В секундах для ffmpeg:
offset_seconds = offset_frames / fps
```

**Почему именно так:**

- Первый переход (i=1): fade начинается за `fade_duration` кадров до конца первого кадра
- Второй переход (i=2): учтено, что каждый предыдущий xfade «съедает» `fade_duration` кадров от общей длины
- Если использовать `i * seg_frames - fade_duration` (старая формула), офсет будет неверным
  для 2+ переходов — fade смещается вправо

## Цепочка фильтров

Исходные zoompan-кадры с метками `[z0]`, `[z1]`, ..., `[z{n-1}]`:

```
[z0][z1]xfade=transition=fade:duration=1.00:offset=5.17[f1];
[f1][z2]xfade=transition=fade:duration=1.00:offset=10.33[f2];
[f2][z3]xfade=transition=fade:duration=1.00:offset=15.50[vid]
```

- Промежуточные метки: `f1`, `f2`, ..., `f{n-2}`
- Последняя метка — `vid` (финальный видео-выход)
- Если всего 1 кадр — xfade не нужен, идёт `[z0]null[vid]`

## Включение в filter_complex

```python
# Сборка zoompan фильтров: [0:v]...zoompan...[z0]; [1:v]...zoompan...[z1]; ...
# Потом xfade цепочка:
if num_inputs >= 2:
    fade_duration = min(30, seg_frames // 4)
    prev = f"[z0]"
    for i in range(1, num_inputs):
        cur = f"[z{i}]"
        offset_frames = i * (seg_frames - fade_duration)
        new_label = f"f{i}" if i < num_inputs - 1 else "vid"
        filters.append(
            f"{prev}{cur}xfade=transition=fade:"
            f"duration={fade_duration/30:.2f}:"
            f"offset={offset_frames/30:.2f}[{new_label}]"
        )
        prev = f"[{new_label}]"
else:
    filters.append(f"[z0]null[vid]")
```

## Проверка синтаксиса

```bash
# Быстрая проверка, что xfade цепочка валидна:
ffmpeg -f lavfi -i color=c=black:s=1080x1920:d=3 \
       -f lavfi -i color=c=white:s=1080x1920:d=3 \
       -filter_complex "[0:v]format=yuv420p[z0];[1:v]format=yuv420p[z1];[z0][z1]xfade=transition=fade:duration=0.50:offset=2.50[vid]" \
       -map "[vid]" -frames:v 10 -y /dev/null 2>&1 | grep -c "Error"
# 0 = OK, 1+ = error
```

## Известные проблемы

- **xfade требует yuv420p на входе.** У zoompan уже стоит `format=yuv420p` — не убирать.
- **xfade НЕ РАБОТАЕТ с разными разрешениями.** Все [z{i}] входы должны быть одинакового размера (1080×1920).
- **При chained xfade** общая длина видео = `n * seg_frames/fps - (n-1) * fade_duration/fps`.
  Это нормально — «лишнее» аудио обрезается `-shortest` при монтаже.
- **xfade с `transition=fade`** — не единственный вариант. Есть `fadeblack`, `fadewhite`, `dissolve`, `pixelize`, `random` и десятки других. Для контента лучше всего `fade`.
