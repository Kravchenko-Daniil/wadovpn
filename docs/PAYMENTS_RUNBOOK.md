# Платежи в Wado VPN — операционный справочник

_Обновлено: 2026-04-19_

## Общая схема

```
Юзер в боте → «Купить подписку» → выбор тарифа
     ↓
bot/yookassa_api.py → POST https://api.yookassa.ru/v3/payments
     ↓
ЮKassa возвращает confirmation_url
     ↓
Юзер тапает «💳 Оплатить» → страница ЮKassa → оплата
     ↓
ЮKassa POST https://pay.wadovpn.online/yookassa/webhook
     ↓
nginx → 127.0.0.1:8081 (aiohttp в боте)
     ↓
bot/webhook.py: IP allowlist → GET /payments/{id} (перепроверка) → 
     → Marzban update_user (новый expire) → уведомление юзеру
```

## Точки отказа и как проверить

| Что проверить | Команда |
|---|---|
| DNS `pay.wadovpn.online` резолвится на 46.225.125.127 | `dig +short pay.wadovpn.online` |
| nginx отвечает на /health | `curl https://pay.wadovpn.online/health` → `ok` |
| Webhook-сервер внутри бота жив | `ssh my-hetzner "curl -s http://127.0.0.1:8081/health"` |
| Ключи ЮKassa валидны | `curl -u shop_id:secret https://api.yookassa.ru/v3/me` → 200 |
| Активен ли endpoint VDSka | `ssh my-vdska "docker logs \$(docker ps --filter name=marzban-node -q) --tail 5"` |
| Логи бота | `ssh my-hetzner "docker logs wado-bot-wado-bot-1 --tail 50"` |
| История вебхуков от ЮKassa | ЛК ЮKassa → Интеграция → HTTP-уведомления → История |

## Тарифы

Определены в `bot/config.py` → `PLANS`:

| Ключ | Цена | Месяцев |
|---|---|---|
| `1m` | 99 ₽ | 1 |
| `3m` | 249 ₽ | 3 |
| `6m` | 499 ₽ | 6 |
| `12m` | 899 ₽ | 12 |

Чтобы изменить цены — правишь `PLANS` и пересобираешь бот (`docker compose up -d --build`).

## ЮKassa: настройки в ЛК

- **Магазин:** shop_id `1329639`, статус `enabled`, не тестовый
- **API-ключ:** secret key (`live_...`), лежит в `/opt/wado-bot/.env` как `YOOKASSA_SECRET_KEY`
- **HTTP-уведомления (вебхуки):** `https://pay.wadovpn.online/yookassa/webhook`, события:
  - ✅ `payment.succeeded`
  - ✅ `payment.canceled`
  - ✅ `payment.waiting_for_capture` (на всякий)
  - ✅ `refund.succeeded`
  - ✅ `payment_method.active` (для будущих автоплатежей)

## Безопасность вебхука

В `bot/webhook.py` два уровня защиты:

1. **IP allowlist** — принимаем только с IP-диапазонов ЮKassa (`185.71.76.0/27`, `185.71.77.0/27`, `77.75.153.0/25`, `77.75.154.128/25`, `77.75.156.11`, `77.75.156.35`, `2a02:5180::/32`).
2. **Повторная верификация через GET /payments/{id}** — не доверяем payload как есть, обязательно перепроверяем статус через API ЮKassa с нашим secret key.

Если ЮKassa поменяет диапазон IP — добавь в `YOOKASSA_NETS` в `bot/webhook.py`. Актуальный список: https://yookassa.ru/developers/using-api/webhooks#ip

## Ротация ключей

### YOOKASSA_SECRET_KEY
ЛК ЮKassa → Интеграция → Ключи API → «Заменить». Новый ключ в `/opt/wado-bot/.env` → `docker compose up -d --force-recreate`.

### BOT_TOKEN
@BotFather → `/mybots` → @wadovpn_bot → API Token → Revoke. Новый токен в `.env` → пересоздать контейнер.

### MARZBAN_PASS
`marzban cli admin update --username admin` на мастере. Обновить `.env` → пересоздать.

**Важно:** `docker compose restart` **не перечитывает env_file** — нужен `up -d --force-recreate` или `down && up -d`.

## Чеки (НПД)

Сервис «Чеки для самозанятых» в ЮKassa закрыт с 29.12.2025 — чеки не бьются автоматически.

**Процесс** (после каждого `ADMIN_PAYMENT_NOTIFY`):
1. Открыть приложение «Мой налог»
2. «Новая продажа» → сумма из нотификации, плательщик «Физлицо», услуга «Подписка Wado VPN»
3. Чек сформируется и уйдёт в ФНС; пользователю отдельно отправлять не обязательно (email не собираем)

**Автоматизаторы на будущее** (когда объём вырастет): Консоль.Про, Точка-банк, Rocketwork — все они интегрируются с API «Мой налог».

## Частые проблемы

### «Не удалось создать платёж»

1. Проверь логи: `docker logs wado-bot-wado-bot-1 | grep -E 'yookassa|401|error'`
2. Если `401 invalid_credentials` — `.env` на сервере или в контейнере пустой. `docker exec wado-bot-wado-bot-1 python3 -c 'import os; print(bool(os.environ.get("YOOKASSA_SECRET_KEY")))'`. Если `False` — `docker compose up -d --force-recreate`.
3. Если ключи валидны — проверь `curl -u ...:... https://api.yookassa.ru/v3/me`. Если 200 — проблема в коде, не в ключах.

### Ссылка на оплату устарела

Ссылка ЮKassa живёт ~10 минут. У юзера в сообщении есть кнопка **«🔄 Новая ссылка»** — создаёт новый платёж и переписывает URL в том же сообщении. Старые pending платежи ЮKassa авто-отменит (webhook с `canceled` проигнорируется, если у юзера активная подписка).

### Не пришло уведомление об оплате

1. Посмотри историю вебхуков в ЛК ЮKassa (Интеграция → HTTP-уведомления → История). Должны быть 200 OK.
2. Если ЮKassa получает 403/500 — проблема в nginx или в боте. Смотри `/var/log/nginx/pay.error.log` и логи бота.
3. Если ЮKassa вообще не дошла — проверь DNS и сертификат (`curl -v https://pay.wadovpn.online/health`).

### Деньги пришли, подписка не продлилась

1. В БД: `ssh my-hetzner "sudo sqlite3 /opt/wado-bot/data/bot.db 'SELECT * FROM payments WHERE tg_id=...'"` — есть ли запись, какой статус.
2. Если запись есть со status=succeeded, но юзер не получил — проверь Marzban (`docker logs marzban-marzban-1`).
3. Если запись со status=pending — вебхук не дошёл, см. предыдущий пункт.
4. Ручное продление: `/grant <tg_id> <days>` от админа.

## Как протестить end-to-end после изменений

1. Ребилд: `ssh my-hetzner "cd /opt/wado-bot && docker compose up -d --build"`
2. `curl https://pay.wadovpn.online/health` → `ok`
3. В боте: «Купить подписку» → 99₽ → «💳 Оплатить» → оплата реальной картой (тестовых ключей нет, магазин live-only)
4. Ждёшь «✅ Оплата получена!» в чате
5. В Marzban-панели `admin.wadovpn.online` — видишь свежую подписку в `users`
6. Проверяешь в `/stats` от админа — счётчик `client` вырос
