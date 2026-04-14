WELCOME = (
    "**Wado VPN**\n\n"
    "Telegram, YouTube, ChatGPT, Instagram — "
    "всё работает без ограничений."
)

WELCOME_BACK = (
    "**Wado VPN**\n\n"
    "Подписка активна до {expires}\n"
    "Трафик: {used} / {limit}"
)

TRIAL_ALREADY_USED = "Пробный период уже использован."

TRIAL_ACTIVATED = (
    "✅ Пробный период — {days} дня\n\n"
    "Твоя ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируй и открой **Инструкция**."
)

SUB_INFO = (
    "Активна до {expires}\n"
    "Трафик: {used} / {limit}\n\n"
    "Ссылка:\n"
    "`{sub_url}`"
)

SUB_EXPIRED = "Подписка истекла."

INSTALL_CHOOSE = "Выбери платформу:"

INSTALL_ANDROID = (
    "**Android**\n\n"
    "1. Установи [v2rayNG](https://play.google.com/store/apps/details?id=com.v2ray.ang) "
    "или [Hiddify](https://play.google.com/store/apps/details?id=app.hiddify.com)\n"
    "2. Скопируй ссылку подписки (кнопка «Моя подписка»)\n"
    "3. В приложении нажми + → Импорт из буфера\n"
    "4. Нажми кнопку подключения"
)

INSTALL_IOS = (
    "**iOS**\n\n"
    "1. Установи [Streisand](https://apps.apple.com/app/streisand/id6450534064) "
    "или [Hiddify](https://apps.apple.com/app/hiddify-proxy-vpn/id6596777532)\n"
    "2. Скопируй ссылку подписки (кнопка «Моя подписка»)\n"
    "3. В приложении нажми + → Добавить из буфера\n"
    "4. Нажми кнопку подключения"
)

INSTALL_WINDOWS = (
    "**Windows**\n\n"
    "1. Скачай [Hiddify-Next](https://github.com/hiddify/hiddify-app/releases/latest)\n"
    "2. Установи и запусти\n"
    "3. Скопируй ссылку подписки (кнопка «Моя подписка»)\n"
    "4. Нажми + → Добавить из буфера\n"
    "5. Нажми кнопку подключения"
)

INSTALL_MACOS = (
    "**macOS**\n\n"
    "1. Скачай [Hiddify-Next](https://github.com/hiddify/hiddify-app/releases/latest) "
    "или [V2Box](https://apps.apple.com/app/v2box-v2ray-client/id6446814690)\n"
    "2. Скопируй ссылку подписки (кнопка «Моя подписка»)\n"
    "3. Добавь подписку из буфера\n"
    "4. Подключись"
)

NO_SUB = "У тебя пока нет подписки."

NO_SUB_WITH_TRIAL = (
    "У тебя пока нет подписки.\n"
    "Попробуй бесплатно — 3 дня!"
)

HELP_TEXT = (
    "**Не подключается?**\n"
    "Попробуй другое приложение.\n\n"
    "**Медленно?**\n"
    "Смени протокол в настройках.\n\n"
    "**Не помогло?**\n"
    "Напиши админу."
)

BUY_CHOOSE = "Выбери тариф:"

# Admin
GRANT_OK = "Доступ выдан: {username}\nСрок: {days} дней\nSub: `{sub_url}`"
GRANT_USAGE = "Формат: /grant <tg_id> <days>"
STATS_TEXT = (
    "**Статистика:**\n\n"
    "Всего юзеров: {total}\n"
    "Активных: {active}\n"
    "Trial: {trial}\n"
    "Friend: {friend}\n"
    "Client: {client}"
)
BLOCK_OK = "Пользователь {username} заблокирован."
BLOCK_NOT_FOUND = "Пользователь с tg_id={tg_id} не найден."
NOT_ADMIN = "Эта команда только для админа."
