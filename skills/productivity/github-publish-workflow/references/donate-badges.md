---
title: Donate Badges
version: 1.0.0
audience: Developers monetizing open-source tools
tags:
  - donate
  - shields.io
  - crypto
  - monetization
  - badges
---

## Donate Badges

### Shields.io Badges for Cryptocurrencies

```markdown
[![BTC](https://img.shields.io/badge/BTC-bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j?logo=bitcoin)](https://blockchain.info/address/bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j)
[![ETH](https://img.shields.io/badge/ETH-0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3?logo=ethereum)](https://etherscan.io/address/0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3)
[![TON](https://img.shields.io/badge/TON-UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP?logo=ton)](https://tonviewer.com/UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP)
[![SOL](https://img.shields.io/badge/SOL-99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK?logo=solana)](https://solscan.io/address/99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK)
```

### Ko-fi Badge (accepts cards/PayPal/crypto)

```markdown
[![Ko-fi](https://img.shields.io/badge/support-Ko--fi-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/username)
```

### Block Explorer URLs

| Currency | Block Explorer | Example URL |
|---|---|---|
| BTC | blockchain.info | `https://blockchain.info/address/<addr>` |
| ETH | etherscan.io | `https://etherscan.io/address/<addr>` |
| USDT (TON) | tonviewer.com | `https://tonviewer.com/<addr>` |
| TON | tonviewer.com | `https://tonviewer.com/<addr>` |
| SOL | solscan.io | `https://solscan.io/address/<addr>` |

### Verification Checklist

1. **BTC:** `curl -s "https://blockchain.info/address/bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j" | grep "address"`
2. **ETH:** `curl -s "https://etherscan.io/address/0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3" | grep "Ethereum"`
3. **TON:** `curl -s "https://tonviewer.com/UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP" | grep "TON"`
4. **SOL:** `curl -s "https://solscan.io/address/99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK" | grep "Solana"`

### Pitfalls
- **BTC on Solscan:** BTC addresses do NOT work on solscan.io — always use blockchain.info
- **ETH on Tonviewer:** ETH addresses do NOT work on tonviewer.com — always use etherscan.io
- **URL encoding:** Always encode addresses in URLs (e.g., `+` → `%2B`)
- **Logo:** Always use the correct logo (bitcoin, ethereum, ton, solana)

### References
- [GitHub Publish Workflow](../SKILL.md) — full publish cycle