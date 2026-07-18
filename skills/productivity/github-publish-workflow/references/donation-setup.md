# Donation Setup (Создание донат-инфраструктуры)

См. также: `github-monetization-publish/references/donation-setup.md` и `github-monetization-publish/references/donation-infrastructure.md` (там canonical таблица с адресами).

## Краткая памятка

При создании нового репозитория **обязательно** добавить:

1. `.github/FUNDING.yml`:
   ```yaml
   github: zad111ak-ai
   custom: ["https://btc.com/bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j"]
   ```
   **Note:** `github:` enables the Sponsor button on the repo page. `custom:` adds a direct donation link. The Sponsor button only appears after manually enabling "Sponsors" in repo Settings → Features. Multiple custom links work but one is sufficient — the README has the full table with all wallets.

2. В README — таблицу кошельков (BTC, ETH, USDT/TON, TON, SOL)
3. Sponsor badge в шапку
4. Запушенное FUNDING.yml подхватится — кнопка Sponsor появляется после ручного включения в Settings → Features

## 🚨 Критично: Правильные Explorer'ы для бейджей

Каждый блокчейн использует СВОЙ обозреватель. Не перепутай, иначе бейдж ведёт в никуда:

| Актив | Explorer URL | Назначение |
|-------|-------------|------------|
| BTC | `https://blockchain.info/address/<addr>` | Bitcoin — НЕ solscan (solscan только для Solana) |
| ETH / ERC-20 | `https://etherscan.io/address/<addr>` | Ethereum |
| USDT (TON) | `https://tonviewer.com/<addr>` | TON network |
| TON | `https://tonviewer.com/<addr>` | TON network |
| SOL | `https://solscan.io/address/<addr>` | Solana |

**Прошлая ошибка (2026-07-12):** BTC бейдж вёл на solscan.io — это Solana explorer, биткоин там не показывается. Проверяй каждый explorer URL перед коммитом!

## Порядок верификации донатов

После обновления README с донатами — проверь:

1. Открой каждый explorer URL в браузере / `curl -o /dev/null -w "%{http_code}" <url>` — должен вернуть 200
2. Открой бейдж-ссылку на GitHub (render) — визуально проверь что иконка/название соответствует сети
3. Убедись что ETH вообще есть — часто забывается
4. Проверь что USDT адрес совпадает с сетью (USDT на TON ≠ USDT на Solana ≠ USDT на Ethereum)
