import ipaddress
import logging
from datetime import datetime, timedelta

from aiohttp import web
from aiogram import Bot

import db
import texts
from config import Config, PLANS
from marzban import MarzbanAPI
from yookassa_api import YooKassaAPI

log = logging.getLogger(__name__)

# https://yookassa.ru/developers/using-api/webhooks#ip
YOOKASSA_NETS = [
    ipaddress.ip_network("185.71.76.0/27"),
    ipaddress.ip_network("185.71.77.0/27"),
    ipaddress.ip_network("77.75.153.0/25"),
    ipaddress.ip_network("77.75.154.128/25"),
    ipaddress.ip_network("77.75.156.11/32"),
    ipaddress.ip_network("77.75.156.35/32"),
    ipaddress.ip_network("2a02:5180::/32"),
]


def _marzban_username(tg_id: int) -> str:
    return f"wado_{tg_id}"


def _ip_allowed(remote: str) -> bool:
    try:
        ip = ipaddress.ip_address(remote)
    except ValueError:
        return False
    return any(ip in net for net in YOOKASSA_NETS)


async def _handle_succeeded(
    payment: dict, bot: Bot, marzban: MarzbanAPI, cfg: Config
):
    metadata = payment.get("metadata") or {}
    tg_id = int(metadata.get("tg_id", 0))
    plan_key = metadata.get("plan")
    if not tg_id or plan_key not in PLANS:
        log.warning("payment.succeeded missing metadata: %s", payment.get("id"))
        return

    plan = PLANS[plan_key]
    months = plan["months"]
    username = _marzban_username(tg_id)
    user = db.get_user(tg_id)

    # Friends with unlimited access donating → just thank them, don't touch sub
    is_donation = bool(
        user and user.get("role") == "friend" and not user.get("expires_at")
    )

    if is_donation:
        try:
            await bot.send_message(tg_id, texts.PAY_OK_DONATION, parse_mode="Markdown")
        except Exception as e:
            log.warning("Failed to notify donor %s: %s", tg_id, e)
        await _notify_admins(
            bot=bot, cfg=cfg, payment=payment, plan=plan, tg_id=tg_id,
            new_expires=None, is_donation=True,
        )
        return

    # Extend from current expires_at if still active, else from now
    now = datetime.utcnow()
    base = now
    if user and user.get("expires_at"):
        try:
            cur = datetime.fromisoformat(user["expires_at"])
            if cur > now:
                base = cur
        except ValueError:
            pass
    new_expires = base + timedelta(days=30 * months)
    expire_ts = int(new_expires.timestamp())

    existing = await marzban.get_user(username)
    if existing:
        mz = await marzban.update_user(username, expire=expire_ts, status="active")
    else:
        mz = await marzban.create_user(username, expire_ts)

    if user:
        db.update_user(tg_id, role="client", expires_at=new_expires.isoformat())
    else:
        db.create_user(
            tg_id=tg_id, username=None, marzban_username=username,
            role="client", expires_at=new_expires.isoformat(),
        )

    sub_url = mz.get("subscription_url", "")
    try:
        await bot.send_message(
            tg_id,
            texts.PAY_OK.format(
                months=months,
                expires=new_expires.strftime("%d.%m.%Y"),
                sub_url=sub_url,
            ),
            parse_mode="Markdown",
        )
    except Exception as e:
        log.warning("Failed to notify user %s: %s", tg_id, e)

    await _notify_admins(
        bot=bot, cfg=cfg, payment=payment, plan=plan, tg_id=tg_id,
        new_expires=new_expires,
    )


async def _notify_admins(
    bot: Bot, cfg: Config, payment: dict, plan: dict, tg_id: int,
    new_expires: datetime | None, is_donation: bool = False,
):
    if not cfg.admin_ids:
        return

    amount_obj = payment.get("amount") or {}
    amount = amount_obj.get("value", str(plan["price"]))

    tg_username = None
    try:
        chat = await bot.get_chat(tg_id)
        tg_username = chat.username
    except Exception:
        pass
    user_link = f"@{tg_username}" if tg_username else f"[профиль](tg://user?id={tg_id})"

    if is_donation:
        text = texts.ADMIN_DONATION_NOTIFY.format(
            amount=amount,
            user_link=user_link,
            tg_id=tg_id,
            payment_id=payment.get("id", "?"),
        )
    else:
        text = texts.ADMIN_PAYMENT_NOTIFY.format(
            amount=amount,
            label=plan["label"],
            months=plan["months"],
            user_link=user_link,
            tg_id=tg_id,
            expires=new_expires.strftime("%d.%m.%Y"),
            payment_id=payment.get("id", "?"),
        )
    for admin_id in cfg.admin_ids:
        try:
            await bot.send_message(admin_id, text, parse_mode="Markdown")
        except Exception as e:
            log.warning("Failed to notify admin %s: %s", admin_id, e)


async def _handle_canceled(payment: dict, bot: Bot):
    metadata = payment.get("metadata") or {}
    tg_id = int(metadata.get("tg_id", 0))
    if not tg_id:
        return

    # Пользователь мог создать несколько pending платежей (жал «Новая ссылка»)
    # и оплатить один — остальные ЮKassa позже авто-отменит. Не беспокоим
    # юзера, если у него сейчас активная подписка.
    user = db.get_user(tg_id)
    if user and user.get("expires_at"):
        try:
            if datetime.fromisoformat(user["expires_at"]) > datetime.utcnow():
                log.info("skip canceled notify for %s (active sub)", tg_id)
                return
        except ValueError:
            pass

    try:
        await bot.send_message(tg_id, texts.PAY_CANCELED)
    except Exception as e:
        log.warning("Failed to notify canceled %s: %s", tg_id, e)


def build_app(
    bot: Bot, marzban: MarzbanAPI, yookassa: YooKassaAPI, cfg: Config
) -> web.Application:
    async def health(request: web.Request) -> web.Response:
        return web.Response(text="ok")

    async def on_webhook(request: web.Request) -> web.Response:
        remote = request.headers.get("X-Forwarded-For", request.remote or "")
        remote = remote.split(",")[0].strip()
        if not _ip_allowed(remote):
            log.warning("webhook from disallowed ip: %s", remote)
            return web.Response(status=403)

        try:
            data = await request.json()
        except Exception:
            return web.Response(status=400)

        event = data.get("event")
        obj = data.get("object") or {}
        payment_id = obj.get("id")
        log.info("YooKassa webhook: %s id=%s status=%s", event, payment_id, obj.get("status"))

        # Re-fetch the payment to avoid trusting the payload blindly
        if payment_id and event in ("payment.succeeded", "payment.canceled"):
            try:
                verified = await yookassa.get_payment(payment_id)
            except Exception as e:
                log.error("verify payment failed: %s", e)
                return web.Response(status=500)
            obj = verified

        if event == "payment.succeeded" and obj.get("status") == "succeeded":
            db.update_payment_by_external(payment_id, "succeeded")
            await _handle_succeeded(obj, bot, marzban, cfg)
        elif event == "payment.canceled":
            db.update_payment_by_external(payment_id, "canceled")
            await _handle_canceled(obj, bot)

        return web.Response(text="ok")

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post("/yookassa/webhook", on_webhook)
    return app


async def start_webhook(cfg: Config, bot: Bot, marzban: MarzbanAPI, yookassa: YooKassaAPI):
    app = build_app(bot, marzban, yookassa, cfg)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, cfg.webhook_host, cfg.webhook_port)
    await site.start()
    log.info("Webhook server listening on %s:%s", cfg.webhook_host, cfg.webhook_port)
    return runner
