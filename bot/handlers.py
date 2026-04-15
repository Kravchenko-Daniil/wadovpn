import logging
import secrets
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions

import db
import texts
import keyboards as kb
from marzban import MarzbanAPI
from yookassa_api import YooKassaAPI
from config import Config, PLANS

log = logging.getLogger(__name__)
router = Router()
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


# These are set from main.py at startup
marzban: MarzbanAPI = None
yookassa: YooKassaAPI = None
cfg: Config = None


def _marzban_username(tg_id: int) -> str:
    return f"wado_{tg_id}"


def _format_bytes(b: int) -> str:
    if b is None:
        return "0 MB"
    gb = b / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    return f"{b / (1024 ** 2):.0f} MB"


def _format_expires(iso: str | None) -> str:
    if not iso:
        return "бессрочно"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        return str(iso)


def _status_line(iso: str | None) -> str:
    if not iso:
        return "Подписка бессрочная"
    return f"Подписка активна до {_format_expires(iso)}"


def _is_unlimited(user: dict | None) -> bool:
    return bool(user and user.get("role") == "friend" and not user.get("expires_at"))


def _is_admin(tg_id: int) -> bool:
    return tg_id in cfg.admin_ids


def _status_text(status: str) -> str:
    return {
        "active": "Активна",
        "expired": "Истекла",
        "limited": "Лимит трафика",
        "disabled": "Отключена",
        "on_hold": "На паузе",
    }.get(status, status)


# /start
@router.message(Command("start"))
async def cmd_start(msg: Message, command: CommandObject):
    arg = (command.args or "").strip()
    if arg.startswith("inv_"):
        await _activate_invite(msg, arg[4:])
        return

    tg_id = msg.from_user.id
    tg_username = msg.from_user.username
    user = db.get_user(tg_id)
    if not _is_unlimited(user) and db.is_whitelisted(tg_username):
        has_active_paid = bool(
            user and user.get("expires_at")
            and user["expires_at"] > datetime.utcnow().isoformat()
        )
        if not has_active_paid:
            sub_url = await _grant_unlimited_friend(tg_id, tg_username)
            await msg.answer(
                texts.WHITELIST_ACTIVATED.format(sub_url=sub_url),
                parse_mode="Markdown",
                reply_markup=kb.trial_activated(),
                link_preview_options=NO_PREVIEW,
            )
            return

    if user and user["marzban_username"]:
        mz = await marzban.get_user(user["marzban_username"])
        if mz:
            status = mz["status"]
            if status in ("expired", "limited", "disabled"):
                trial_available = not bool(user.get("trial_used"))
                await msg.answer(
                    texts.WELCOME + "\n\n" + texts.SUB_EXPIRED,
                    parse_mode="Markdown",
                    reply_markup=kb.main_menu(has_sub=False, trial_available=trial_available),
                )
                return
            text = texts.WELCOME_BACK.format(
                status_line=_status_line(user["expires_at"]),
                used=_format_bytes(mz.get("used_traffic", 0)),
                limit=_format_bytes(mz.get("data_limit")),
            )
            await msg.answer(
                text, parse_mode="Markdown",
                reply_markup=kb.main_menu(has_sub=True, is_unlimited=_is_unlimited(user)),
            )
            return
    await msg.answer(texts.WELCOME, parse_mode="Markdown", reply_markup=kb.main_menu(has_sub=False))


# Trial
@router.callback_query(F.data == "trial")
async def on_trial(cq: CallbackQuery):
    tg_id = cq.from_user.id
    user = db.get_user(tg_id)

    if user and user["trial_used"]:
        await cq.answer(texts.TRIAL_ALREADY_USED, show_alert=True)
        return

    username = _marzban_username(tg_id)
    expires = datetime.utcnow() + timedelta(days=cfg.trial_days)
    expire_ts = int(expires.timestamp())

    try:
        mz = await marzban.create_user(username, expire_ts)
    except Exception as e:
        log.error("Failed to create trial user: %s", e)
        await cq.answer("Ошибка, попробуй позже.", show_alert=True)
        return

    db.create_user(
        tg_id=tg_id,
        username=cq.from_user.username,
        marzban_username=username,
        role="trial",
        expires_at=expires.isoformat(),
    )

    sub_url = mz.get("subscription_url", "")
    await cq.message.edit_text(
        texts.TRIAL_ACTIVATED.format(days=cfg.trial_days, sub_url=sub_url),
        parse_mode="Markdown",
        reply_markup=kb.trial_activated(),
        link_preview_options=NO_PREVIEW,
    )
    await cq.answer()


# My subscription
@router.callback_query(F.data == "my_sub")
async def on_my_sub(cq: CallbackQuery):
    user = db.get_user(cq.from_user.id)
    if not user or not user["marzban_username"]:
        trial_available = not bool(user and user.get("trial_used"))
        no_sub_text = texts.NO_SUB_WITH_TRIAL if trial_available else texts.NO_SUB
        await cq.message.edit_text(
            no_sub_text,
            reply_markup=kb.main_menu(has_sub=False, trial_available=trial_available),
        )
        await cq.answer()
        return

    mz = await marzban.get_user(user["marzban_username"])
    if not mz:
        trial_available = not bool(user.get("trial_used"))
        no_sub_text = texts.NO_SUB_WITH_TRIAL if trial_available else texts.NO_SUB
        await cq.message.edit_text(
            no_sub_text,
            reply_markup=kb.main_menu(has_sub=False, trial_available=trial_available),
        )
        await cq.answer()
        return

    status = mz["status"]
    if status in ("expired", "limited", "disabled"):
        await cq.message.edit_text(
            texts.SUB_EXPIRED, reply_markup=kb.sub_expired_kb()
        )
        await cq.answer()
        return

    text = texts.SUB_INFO.format(
        status_line=_status_line(user["expires_at"]),
        used=_format_bytes(mz.get("used_traffic", 0)),
        limit=_format_bytes(mz.get("data_limit")),
        sub_url=mz.get("subscription_url", ""),
    )
    await cq.message.edit_text(
        text, parse_mode="Markdown", reply_markup=kb.sub_info_kb(),
        link_preview_options=NO_PREVIEW,
    )
    await cq.answer()


# Install instructions
@router.callback_query(F.data == "install")
async def on_install(cq: CallbackQuery):
    await cq.message.edit_text(texts.INSTALL_CHOOSE, reply_markup=kb.platforms())
    await cq.answer()


@router.callback_query(F.data.startswith("install_"))
async def on_install_platform(cq: CallbackQuery):
    platform = cq.data.replace("install_", "")
    text = {
        "android": texts.INSTALL_ANDROID,
        "ios": texts.INSTALL_IOS,
        "windows": texts.INSTALL_WINDOWS,
        "macos": texts.INSTALL_MACOS,
    }.get(platform, "")
    await cq.message.edit_text(
        text, parse_mode="Markdown", reply_markup=kb.back_install(),
        link_preview_options=NO_PREVIEW,
    )
    await cq.answer()


# Help
@router.callback_query(F.data == "help")
async def on_help(cq: CallbackQuery):
    await cq.message.edit_text(
        texts.HELP_TEXT, parse_mode="Markdown", reply_markup=kb.help_kb()
    )
    await cq.answer()


# Back to main menu
@router.callback_query(F.data == "back_main")
async def on_back(cq: CallbackQuery):
    user = db.get_user(cq.from_user.id)
    if user and user["marzban_username"]:
        mz = await marzban.get_user(user["marzban_username"])
        if mz and mz["status"] not in ("expired", "limited", "disabled"):
            text = texts.WELCOME_BACK.format(
                status_line=_status_line(user["expires_at"]),
                used=_format_bytes(mz.get("used_traffic", 0)),
                limit=_format_bytes(mz.get("data_limit")),
            )
            await cq.message.edit_text(
                text, parse_mode="Markdown",
                reply_markup=kb.main_menu(has_sub=True, is_unlimited=_is_unlimited(user)),
            )
            await cq.answer()
            return
        # Sub exists but expired/limited/disabled
        trial_available = not bool(user.get("trial_used"))
        await cq.message.edit_text(
            texts.WELCOME, parse_mode="Markdown",
            reply_markup=kb.main_menu(has_sub=False, trial_available=trial_available),
        )
        await cq.answer()
        return
    await cq.message.edit_text(
        texts.WELCOME, parse_mode="Markdown", reply_markup=kb.main_menu(has_sub=False)
    )
    await cq.answer()


# Buy flow (YooKassa)
@router.callback_query(F.data == "buy")
async def on_buy(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    user = db.get_user(cq.from_user.id)
    text = texts.BUY_CHOOSE_DONATION if _is_unlimited(user) else texts.BUY_CHOOSE
    await cq.message.edit_text(
        text, parse_mode="Markdown", reply_markup=kb.buy_menu()
    )
    await cq.answer()


@router.callback_query(F.data.startswith("buy_"))
async def on_buy_plan(cq: CallbackQuery, state: FSMContext):
    plan_key = cq.data.replace("buy_", "")
    if plan_key not in PLANS:
        await cq.answer("Неизвестный тариф", show_alert=True)
        return
    await _create_and_send_payment(cq, plan_key, edit=False)


@router.callback_query(F.data.startswith("refresh_"))
async def on_refresh_payment(cq: CallbackQuery):
    plan_key = cq.data.replace("refresh_", "")
    if plan_key not in PLANS:
        await cq.answer("Неизвестный тариф", show_alert=True)
        return
    await _create_and_send_payment(cq, plan_key, edit=True)


async def _create_and_send_payment(cq: CallbackQuery, plan_key: str, edit: bool):
    plan = PLANS[plan_key]
    tg_id = cq.from_user.id
    try:
        payment = await yookassa.create_payment(tg_id, plan_key)
    except Exception as e:
        log.error("create_payment failed: %s", e)
        await cq.answer("Не удалось создать платёж. Попробуй позже.", show_alert=True)
        return

    payment_id = payment["id"]
    confirm_url = payment["confirmation"]["confirmation_url"]
    db.add_payment(
        tg_id=tg_id, amount=plan["price"], currency="RUB", method="yookassa",
        plan=plan_key, email="", external_id=payment_id,
    )

    text = texts.PAY_CREATED.format(label=plan["label"], price=plan["price"])
    markup = kb.pay_link(confirm_url, plan_key)
    if edit:
        await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=markup)
        await cq.answer("Ссылка обновлена")
    else:
        await cq.message.answer(text, parse_mode="Markdown", reply_markup=markup)
        await cq.answer()


# ── Admin commands ──────────────────────────────────────────────

@router.message(Command("grant"))
async def cmd_grant(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    parts = msg.text.split()
    if len(parts) < 3:
        await msg.answer(texts.GRANT_USAGE)
        return

    try:
        target_tg_id = int(parts[1])
        days = int(parts[2])
    except ValueError:
        await msg.answer(texts.GRANT_USAGE)
        return

    username = _marzban_username(target_tg_id)
    expires = datetime.utcnow() + timedelta(days=days)
    expire_ts = int(expires.timestamp())

    # Check if user already exists in Marzban
    existing = await marzban.get_user(username)
    if existing:
        mz = await marzban.update_user(username, expire=expire_ts, status="active")
    else:
        mz = await marzban.create_user(username, expire_ts)

    # Update local DB
    local = db.get_user(target_tg_id)
    if local:
        db.update_user(target_tg_id, role="friend", expires_at=expires.isoformat())
    else:
        db.create_user(
            tg_id=target_tg_id,
            username=None,
            marzban_username=username,
            role="friend",
            expires_at=expires.isoformat(),
        )

    sub_url = mz.get("subscription_url", "")
    await msg.answer(
        texts.GRANT_OK.format(username=username, days=days, sub_url=sub_url),
        parse_mode="Markdown",
        link_preview_options=NO_PREVIEW,
    )


@router.message(Command("block"))
async def cmd_block(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("Формат: /block <tg_id>")
        return

    try:
        target_tg_id = int(parts[1])
    except ValueError:
        await msg.answer("Формат: /block <tg_id>")
        return

    user = db.get_user(target_tg_id)
    if not user:
        await msg.answer(texts.BLOCK_NOT_FOUND.format(tg_id=target_tg_id))
        return

    username = user["marzban_username"]
    await marzban.update_user(username, status="disabled")
    db.update_user(target_tg_id, role="blocked")
    await msg.answer(texts.BLOCK_OK.format(username=username))


@router.message(Command("stats"))
async def cmd_stats(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    users = db.get_all_users()
    total = len(users)
    active = db.get_active_users_count()
    trial = sum(1 for u in users if u["role"] == "trial")
    friend = sum(1 for u in users if u["role"] == "friend")
    client = sum(1 for u in users if u["role"] == "client")

    await msg.answer(
        texts.STATS_TEXT.format(
            total=total, active=active, trial=trial, friend=friend, client=client
        ),
        parse_mode="Markdown",
    )


@router.message(Command("users"))
async def cmd_users(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    users = db.get_all_users()
    if not users:
        await msg.answer("Нет пользователей.")
        return

    lines = []
    for u in users[:20]:
        status = "expired" if (
            u["expires_at"] and u["expires_at"] < datetime.utcnow().isoformat()
        ) else "active"
        lines.append(
            f"`{u['tg_id']}` | {u['role']} | {status} | {_format_expires(u['expires_at'])}"
        )

    await msg.answer(
        "**Пользователи** (последние 20):\n\n" + "\n".join(lines),
        parse_mode="Markdown",
    )


# ── Invites ─────────────────────────────────────────────────────

@router.message(Command("invite"))
async def cmd_invite(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    parts = msg.text.split(maxsplit=2)
    max_uses = 1
    note = ""
    if len(parts) >= 2:
        try:
            max_uses = int(parts[1])
            if max_uses < 1:
                raise ValueError
        except ValueError:
            await msg.answer(texts.INVITE_USAGE, parse_mode="Markdown")
            return
    if len(parts) >= 3:
        note = parts[2]

    code = secrets.token_hex(4)
    db.create_invite(code=code, max_uses=max_uses, created_by=msg.from_user.id, note=note)

    me = await msg.bot.get_me()
    link = f"https://t.me/{me.username}?start=inv_{code}"
    await msg.answer(
        texts.INVITE_CREATED.format(max_uses=max_uses, link=link),
        parse_mode="Markdown",
        link_preview_options=NO_PREVIEW,
    )


@router.message(Command("invites"))
async def cmd_invites(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    invites = db.get_all_invites()
    if not invites:
        await msg.answer(texts.INVITES_EMPTY)
        return

    lines = []
    for inv in invites[:30]:
        note = f" — {inv['note']}" if inv.get("note") else ""
        lines.append(
            f"`{inv['code']}` | {inv['uses_count']}/{inv['max_uses']}{note}"
        )
    await msg.answer(
        texts.INVITES_HEADER + "\n".join(lines), parse_mode="Markdown"
    )


async def _grant_unlimited_friend(tg_id: int, tg_username: str | None) -> str:
    """Create or upgrade user to unlimited friend. Returns sub_url."""
    username = _marzban_username(tg_id)
    existing = await marzban.get_user(username)
    if existing:
        mz = await marzban.update_user(username, expire=0, status="active")
    else:
        mz = await marzban.create_user(username, 0)

    user = db.get_user(tg_id)
    if user:
        db.update_user(tg_id, role="friend", expires_at=None)
    else:
        db.create_user(
            tg_id=tg_id, username=tg_username,
            marzban_username=username, role="friend", expires_at=None,
        )
    return mz.get("subscription_url", "")


async def _activate_invite(msg: Message, code: str):
    tg_id = msg.from_user.id
    invite = db.get_invite(code)
    if not invite:
        await msg.answer(texts.INVITE_INVALID)
        return
    if invite["uses_count"] >= invite["max_uses"]:
        await msg.answer(texts.INVITE_EXHAUSTED)
        return

    user = db.get_user(tg_id)
    if user and user.get("expires_at"):
        try:
            if datetime.fromisoformat(user["expires_at"]) > datetime.utcnow():
                await msg.answer(texts.INVITE_ALREADY_HAS_SUB)
                return
        except ValueError:
            pass
    if _is_unlimited(user):
        await msg.answer(texts.INVITE_ALREADY_HAS_SUB)
        return

    sub_url = await _grant_unlimited_friend(tg_id, msg.from_user.username)
    db.increment_invite_use(code)

    await msg.answer(
        texts.INVITE_ACTIVATED.format(sub_url=sub_url),
        parse_mode="Markdown",
        reply_markup=kb.trial_activated(),
        link_preview_options=NO_PREVIEW,
    )


# ── Whitelist ───────────────────────────────────────────────────

@router.message(Command("whitelist"))
async def cmd_whitelist(msg: Message):
    if not _is_admin(msg.from_user.id):
        await msg.answer(texts.NOT_ADMIN)
        return

    parts = msg.text.split()
    if len(parts) == 1:
        rows = db.get_all_whitelist()
        if not rows:
            await msg.answer(texts.WHITELIST_EMPTY)
            return
        lines = [f"• `@{r['username']}`" for r in rows]
        await msg.answer(
            texts.WHITELIST_HEADER + "\n".join(lines), parse_mode="Markdown"
        )
        return

    if len(parts) < 3:
        await msg.answer(texts.WHITELIST_USAGE, parse_mode="Markdown")
        return

    action = parts[1].lower()
    usernames = [p.strip().lstrip("@").lower() for p in parts[2:] if p.strip().lstrip("@")]
    if not usernames or action not in ("add", "del"):
        await msg.answer(texts.WHITELIST_USAGE, parse_mode="Markdown")
        return

    added, existed, removed, not_found = [], [], [], []
    for u in usernames:
        if action == "add":
            (added if db.add_whitelist(u, msg.from_user.id) else existed).append(u)
        else:
            (removed if db.remove_whitelist(u) else not_found).append(u)

    lines = []
    if added:
        lines.append("✅ Добавлены: " + ", ".join(f"`@{u}`" for u in added))
    if existed:
        lines.append("ℹ️ Уже были: " + ", ".join(f"`@{u}`" for u in existed))
    if removed:
        lines.append("🗑 Удалены: " + ", ".join(f"`@{u}`" for u in removed))
    if not_found:
        lines.append("❓ Не найдены: " + ", ".join(f"`@{u}`" for u in not_found))
    await msg.answer("\n".join(lines), parse_mode="Markdown")
