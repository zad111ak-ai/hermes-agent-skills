#!/bin/sh
# AmneziaWG for Telegram DPI-bypass — без SOCKS5 (July 2026)
# OmniRoute проксирует AI API, AWG только для Telegram роутинга.
# See SKILL.md for full docs.
SKILL_DIR="${HOME}/.hermes/skills/autonomous-ai-agents/network-restricted-hermes"
WG_DIR="${HOME}/amneziawg"

docker rm -f awg 2>/dev/null

# 1) WG container
docker run -d --name awg \
  --cap-add=NET_ADMIN --cap-add=SYS_MODULE --device=/dev/net/tun \
  --sysctl net.ipv4.conf.all.src_valid_mark=1 --sysctl net.ipv4.ip_forward=1 \
  -v "${WG_DIR}/nether.conf:/etc/amnezia/amneziawg/wg0.conf:ro" \
  --entrypoint sh metaligh/amneziawg:latest \
  -c '
cp /etc/amnezia/amneziawg/wg0.conf /tmp/wg0.conf
# Удаляем AWG-специфичные параметры — awg setconf их не понимает
sed -i "/^[JSAHIJ]/d" /tmp/wg0.conf
sed -i "/^DNS/d" /tmp/wg0.conf
ln -sf /bin/true /usr/local/bin/resolvconf 2>/dev/null || true
awg-quick up /tmp/wg0.conf 2>&1 && echo "= WG_UP =" && sleep infinity
' > /dev/null 2>&1

sleep 6
if ! docker ps --filter name=awg --format '{{.Status}}' | grep -q Up; then
    echo "[awg] ❌ WG failed"; docker logs awg 2>&1 | tail -3; exit 1
fi
echo "[awg] ✅ WG up"

# 2) Force routing through wg0
docker exec awg sh -c '
  ip addr add 10.137.60.220/32 dev wg0 2>/dev/null
  ip link set wg0 up
  ip route del default via 172.17.0.1 dev eth0 2>/dev/null
  ip route add 172.17.0.0/16 dev eth0
  ip route add default dev wg0
  echo "nameserver 8.8.8.8" > /etc/resolv.conf
' > /dev/null 2>&1
echo "[awg] ✅ Routing via WG"

# 3) Add host route for Telegram (если ещё не добавлен)
ip route add 149.154.160.0/20 via 172.17.0.2 dev docker0 2>/dev/null || true
echo "[awg] ✅ Telegram route added"
