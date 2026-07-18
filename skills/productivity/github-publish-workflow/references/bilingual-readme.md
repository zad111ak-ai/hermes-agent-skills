---
title: Bilingual README Template
version: 1.0.0
audience: Developers publishing bilingual open-source projects
tags: readme, bilingual, russian, english, template
---

## Bilingual README Pattern

All public repos use Russian + English READMEs. Russian is primary (first section).

### Language Switcher (top of file, before badges)

```html
<p align="center">
  <a href="#russian">🇷🇺 Русский</a> &nbsp;|&nbsp; <a href="#english">🇬🇧 English</a>
</p>
```

### Anchor IDs

Each language section starts with an anchor:
```html
<a id="russian"></a>
## 🇷🇺 О проекте
...

<a id="english"></a>
## 🇬🇧 About
...
```

### Badge Row (after switcher, before first section)

```markdown
[![GitHub Stars](https://img.shields.io/github/stars/OWNER/REPO?style=social)](https://github.com/OWNER/REPO)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
```

### Donations Section (bilingual, at the bottom)

Two formats — use the simpler table for small projects, shields.io badges for larger ones:

**Table format (compact):**
```markdown
## Donations / Донаты

| Валюта / Currency | Адрес / Address |
|---|---|
| **BTC** | `bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j` |
| **ETH** | `0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3` |
| **USDT (TON)** | `UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP` |
| **SOL** | `99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK` |
```

**Badge format (visual):**
```markdown
## 💖 Donate / Донаты

[![BTC](https://img.shields.io/badge/BTC-bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j?logo=bitcoin)](https://blockchain.info/address/bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j)
[![ETH](https://img.shields.io/badge/ETH-0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3?logo=ethereum)](https://etherscan.io/address/0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3)
[![TON](https://img.shields.io/badge/TON-UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP?logo=ton)](https://tonviewer.com/UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP)
[![SOL](https://img.shields.io/badge/SOL-99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK?logo=solana)](https://solscan.io/address/99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK)
```

### Full Addresses (copy-paste safe)

| Currency | Address | Explorer URL |
|---|---|---|
| BTC | `bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j` | blockchain.info |
| ETH | `0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3` | etherscan.io |
| USDT (TON) | `UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP` | tonviewer.com |
| SOL | `99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK` | solscan.io |

**NEVER truncate addresses.** Previous sessions had truncated addresses like `bc1q...` or `0x...` — this is always wrong.

### Pitfalls

1. **Never truncate addresses** — always use the full crypto address
2. **Russian section MUST come first** — it's the primary audience
3. **Both sections must cover the same content** — don't skip features in one language
4. **Anchor IDs must be unique** — `#russian` and `#english` are the standard
5. **Language switcher goes BEFORE badges** — so users see it immediately
6. **Commit language changes separately** from feature changes — easier to review
