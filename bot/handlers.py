import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions

import db
import texts
import keyboards as kb
from marzban import MarzbanAPI
from config import Config

log = logging.getLogger(__name__)
router = Router()
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)

# These are set from main.py at startup
marzban: MarzbanAPI = None
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
async def cmd_start(msg: Message):
    user = db.get_user(msg.from_user.id)
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
                expires=_format_expires(user["expires_at"]),
                used=_format_bytes(mz.get("used_traffic", 0)),
                limit=_format_bytes(mz.get("data_limit")),
            )
            await msg.answer(text, parse_mode="Markdown", reply_markup=kb.main_menu(has_sub=True))
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
        expires=_format_expires(user["expires_at"]),
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
                expires=_format_expires(user["expires_at"]),
                used=_format_bytes(mz.get("used_traffic", 0)),
                limit=_format_bytes(mz.get("data_limit")),
            )
            await cq.message.edit_text(
                text, parse_mode="Markdown", reply_markup=kb.main_menu(has_sub=True)
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


# Buy (placeholder — Stars payment will be added)
@router.callback_query(F.data == "buy")
async def on_buy(cq: CallbackQuery):
    await cq.message.edit_text(
        texts.BUY_CHOOSE, reply_markup=kb.buy_menu()
    )
    await cq.answer()


@router.callback_query(F.data.startswith("buy_"))
async def on_buy_plan(cq: CallbackQuery):
    await cq.answer("Оплата скоро будет доступна!", show_alert=True)


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
