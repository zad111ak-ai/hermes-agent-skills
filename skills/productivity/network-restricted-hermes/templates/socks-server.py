#!/usr/bin/env python3
"""
⚠️ DEPRECATED (July 2026) — SOCKS5 больше не нужен.
OmniRoute проксирует AI API, Telegram идёт через AWG роут.

Оставлен как reference на случай возврата к старой архитектуре.
"""
"""SOCKS5 server for AmneziaWG tunnel - all traffic through WG via pre-resolved host IPs."""
import socketserver, struct, sys, socket, threading

# Хардкод реальных IP провайдеров (обход DPI блокировки DNS)
HOSTS = {
    "api.groq.com": "172.64.149.20",
    "openrouter.ai": "172.64.154.20",
    "api.together.xyz": "172.64.150.10",
    "api.perplexity.ai": "104.18.0.121",
    "api.novita.ai": "104.18.0.121",
    "api.telegram.org": "149.154.167.220",
}
