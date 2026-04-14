WELCOME = (
    "Привет! Я бот Wado VPN.\n\n"
    "Быстрый и надёжный VPN для обхода блокировок. "
    "YouTube, ChatGPT, Instagram, Discord — всё работает.\n\n"
    "Выбери действие:"
)

WELCOME_BACK = (
    "С возвратом! Твоя подписка: {status}\n"
    "Действует до: {expires}\n\n"
    "Трафик: {used} / {limit}"
)

TRIAL_ALREADY_USED = "Ты уже использовал пробный период."

TRIAL_ACTIVATED = (
    "Пробный период активирован на {days} дней!\n\n"
    "Твоя ссылка подписки:\n"
    "`{sub_url}`\n\n"
    "Нажми на ссылку чтобы скопировать.\n"
    "Затем открой «Инструкция» и выбери свою платформу."
)

SUB_INFO = (
    "Твоя подписка:\n\n"
    "Статус: {status}\n"
    "Действует до: {expires}\n"
    "Трафик: {used} / {limit}\n\n"
    "Ссылка подписки:\n"
    "`{sub_url}`"
)

SUB_EXPIRED = "Твоя подписка истекла. Продли, чтобы продолжить пользоваться VPN."

INSTALL_CHOOSE = (
    "Выбери свою платформу, чтобы увидеть "
    "какое приложение установить и как подключиться:"
)

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

NO_SUB = "У тебя пока нет подписки.\nНажми «Купить подписку» чтобы начать."

NO_SUB_WITH_TRIAL = (
    "У тебя пока нет подписки.\n"
    "Нажми «Пробный период» чтобы попробовать бесплатно "
    "или «Купить подписку»."
)

HELP_TEXT = (
    "**Часто задаваемые вопросы:**\n\n"
    "**Не подключается?**\n"
    "Попробуй другой сервер в списке или другое приложение.\n\n"
    "**Медленно работает?**\n"
    "Переключись на другой протокол в приложении.\n\n"
    "**Нужна помощь?**\n"
    "Напиши админу: нажми кнопку ниже."
)

BUY_CHOOSE = (
    "Выбери тариф:\n\n"
    "Оплата через Telegram Stars.\n"
    "Чем больше срок — тем выгоднее."
)

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
