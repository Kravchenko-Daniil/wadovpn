from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu(
    has_sub: bool = False,
    trial_available: bool = True,
    is_unlimited: bool = False,
) -> InlineKeyboardMarkup:
    buttons = []
    if has_sub:
        buttons.append([InlineKeyboardButton(text="Моя подписка", callback_data="my_sub")])
    elif trial_available:
        buttons.append([InlineKeyboardButton(text="✨ Попробовать бесплатно", callback_data="trial")])
    if is_unlimited:
        buttons.append([InlineKeyboardButton(text="💝 Поддержать проект", callback_data="buy")])
    else:
        buttons.append([InlineKeyboardButton(text="Купить подписку", callback_data="buy")])
    buttons.append([
        InlineKeyboardButton(text="Инструкция", callback_data="install"),
        InlineKeyboardButton(text="Помощь", callback_data="help"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def platforms() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Android", callback_data="install_android"),
            InlineKeyboardButton(text="iOS", callback_data="install_ios"),
        ],
        [
            InlineKeyboardButton(text="Windows", callback_data="install_windows"),
            InlineKeyboardButton(text="macOS", callback_data="install_macos"),
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def help_kb(admin_username: str = "admin") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать админу", url=f"https://t.me/{admin_username}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def back_install() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="install")],
    ])


def sub_info_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Инструкция", callback_data="install"),
            InlineKeyboardButton(text="Назад", callback_data="back_main"),
        ],
    ])


def trial_activated() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Инструкция", callback_data="install")],
        [InlineKeyboardButton(text="← В меню", callback_data="back_main")],
    ])


def sub_expired_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить подписку", callback_data="buy")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def buy_menu() -> InlineKeyboardMarkup:
    from config import PLANS
    rows = []
    for key, plan in PLANS.items():
        rows.append([InlineKeyboardButton(
            text=f"{plan['label']} — {plan['price']} ₽",
            callback_data=f"buy_{key}",
        )])
    rows.append([InlineKeyboardButton(text="Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def pay_link(url: str, plan_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=url)],
        [InlineKeyboardButton(text="🔄 Новая ссылка", callback_data=f"refresh_{plan_key}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def cancel_email() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="back_main")],
    ])
