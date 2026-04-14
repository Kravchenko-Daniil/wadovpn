from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu(has_sub: bool = False, trial_available: bool = True) -> InlineKeyboardMarkup:
    buttons = []
    if has_sub:
        buttons.append([InlineKeyboardButton(text="Моя подписка", callback_data="my_sub")])
    elif trial_available:
        buttons.append([InlineKeyboardButton(text="Пробный период (3 дня)", callback_data="trial")])
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


def sub_expired_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить подписку", callback_data="buy")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])


def buy_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц — 150 Stars", callback_data="buy_1m")],
        [InlineKeyboardButton(text="3 месяца — 400 Stars", callback_data="buy_3m")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")],
    ])
