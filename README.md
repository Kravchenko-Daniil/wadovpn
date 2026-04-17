# wadovpn

Subscription-based VPN service for friends and paying customers in Russia — distributed through a Telegram bot. No custom client apps; users install standard ones (Hiddify, Streisand, v2rayNG, Amnezia) and get a rotating subscription URL from the bot.

## Stack

- **Bot:** Python · [aiogram](https://github.com/aiogram/aiogram) · aiohttp (webhook server) · SQLite
- **VPN backend:** [Marzban](https://github.com/Gozargah/Marzban) (Xray) — VLESS Reality + Shadowsocks-2022
- **Payments:** YooKassa (RUB) with signed webhook verification
- **Infra:** Docker + docker-compose · nginx (SSL via Let's Encrypt) · multi-node Hetzner / Aeza

## How it works

```
Telegram user
     ↓  /start
aiogram bot (Python)
     ↓  creates / renews user in Marzban via HTTP API
     ↓  returns a multi-protocol subscription link (self-rotating)
User's VPN client auto-picks a working config.

Payment flow:
  user taps "Buy subscription"
    → bot creates YooKassa payment → returns confirmation_url
    → user pays on YooKassa page
    → YooKassa → HTTPS webhook → nginx → bot
    → bot re-verifies payment, extends user in Marzban, notifies user
```

**Why a subscription URL instead of a static config?** It lets the backend rotate/fix configs without user action — critical against DPI (ТСПУ) and iOS client changes. One sub-link serves 4–5 protocols (Reality on different ports with different SNI, gRPC+TLS, Shadowsocks-2022, AmneziaWG); the client auto-switches to whichever works.

## Repo layout

- `bot/`
  - `main.py` · `handlers.py` · `keyboards.py` · `texts.py` — UI & user flow
  - `marzban.py` — Marzban HTTP client (create/renew/revoke users)
  - `yookassa_api.py` — YooKassa payment creation + verification
  - `webhook.py` — aiohttp webhook with IP allowlist
  - `db.py` — SQLite (users, subscriptions, payments)
  - `config.py` — env-based config
  - `Dockerfile` · `docker-compose.yml`
- `deploy/nginx/` — production nginx config (SSL + proxy to bot webhook)
- `docs/TZ.md` — full product spec (Russian)

## Run locally

```bash
cp bot/.env.example bot/.env    # fill BOT_TOKEN, YOOKASSA_SHOP_ID, MARZBAN_URL, ...
cd bot
docker compose up -d
```

## Status

Active — MVP shipped April 2026, running in production for early users.
