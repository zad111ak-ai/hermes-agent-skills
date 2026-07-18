# Fiat → Crypto On-Ramp (Russia, 2026)

## Methods (ranked by cost)

### 1. Bybit P2P (cheapest, needs KYC)
- Bybit P2P works from RF through Hysteria2 proxy
- Bank card (T-Bank, Alfa, etc.) → USDT TRC20
- Fee: 0–1% (varies by merchant)
- Time: 5–15 min
- **Requires:** verified Bybit account (passport)
- **Flow:** Bybit → P2P → Buy → Select USDT/RUB → Choose merchant → Pay → USDT credited
- **Payment methods on Bybit P2P:** Bank card (T-Bank, Alfa) ✅, SBP ✅, YuMoney uncertain (depends on seller), Qiwi ❌

### 2. Telegram Bots (fast, no KYC)
- @CryptoBot (accepts T-Bank/Alfa transfers)
- Fee: 2–5%
- Time: 2–5 min
- **Flow:** /start → Buy → Select amount → Pay transfer → USDT received

### 3. BestChange Aggregator (bestchange.ru)
- Compares rates across 200+ exchangers
- Filter: Bank card → USDT TRC20
- Fee: 1–3% (depends on exchanger)
- Time: 5–30 min
- **Flow:** bestchange.ru → Select direction → Pick exchanger → Go to site → Buy

### 4. SBP (fast transfers)
- Some exchangers accept SBP
- Fee: 2–4%
- Time: 5–15 min
- Search: bestchange.ru → Filter "SBP"

## Bank Loyalty Ranking (2026)

| Bank | Loyalty | Notes |
|------|---------|-------|
| T-Bank (ex-Tinkoff) | 🟡 Moderate | Blocks some exchangers, passes P2P |
| Alfa-Bank | 🟡 Moderate | Modern, sometimes passes |
| Gazprombank | 🟡 Moderate | Was crypto-friendly |
| Rosbank | 🟡 Moderate | Less strict |
| Sberbank | 🔴 Strict | Often blocks crypto transfers |
| VTB | 🔴 Strict | Operation control |
| Pochta Bank | 🔴 Strict | Conservative |

**Key factors for blocks:** amount >50,000 RUB, frequent transfers to exchangers, suspicious counterparties.

**Avoid block:** max 30,000 RUB per transfer, no more than 2-3x/week, use P2P not direct transfers.

## ❌ Does NOT Work (2026)
- **Qiwi:** DEAD — license revoked Feb 2024, wallet blocked, cannot use
- Direct card → Bybit (blocked by banks)
- Binance (blocked in RF)
- Coinbase (not available from RF)
- Most Western exchanges (sanctioned)

## ⚠️ Bank Policy Changes
Banks change crypto policies every 1–3 months. What works today may not work tomorrow. Monitor and have fallback methods.

## Recommended for $20
**Bybit P2P** is cheapest. After USDT received:
1. Move from P2P wallet to Trading wallet (Bybit → Assets → Transfer)
2. Buy BTC/ETH/SOL on spot market
3. Start freqtrade with `dry_run: false` + API keys

**At $20**, banks won't notice the amount — use any bank.
