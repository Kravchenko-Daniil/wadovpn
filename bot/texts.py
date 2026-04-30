WELCOME = (
    "**Wado VPN**\n\n"
    "Telegram, YouTube, ChatGPT, Instagram — "
    "всё работает без ограничений."
)

WELCOME_BACK = (
    "**Wado VPN**\n\n"
    "{status_line}\n"
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
    "{status_line}\n"
    "Трафик: {used} / {limit}\n\n"
    "Ссылка:\n"
    "`{sub_url}`"
)

SUB_EXPIRED = "Подписка истекла. Можно бесплатно продлить кнопкой ниже 👇"

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

NO_SUB = (
    "У тебя пока нет подписки.\n"
    "Жми «🎁 Получить доступ бесплатно» — выдам без оплаты."
)

NO_SUB_WITH_TRIAL = (
    "У тебя пока нет подписки.\n"
    "Можно начать с триала на 3 дня или сразу взять доступ бесплатно."
)

HELP_TEXT = (
    "**Не подключается?**\n"
    "Попробуй другое приложение.\n\n"
    "**Медленно?**\n"
    "Смени протокол в настройках.\n\n"
    "**Не помогло?**\n"
    "Напиши админу."
)

BUY_CHOOSE = (
    "🎁 **Доступ бесплатно**\n\n"
    "Выбери, на сколько включить — оплата не нужна, ничего списывать не будет."
)

SUB_ACTIVATED = (
    "✅ **Доступ открыт!**\n\n"
    "Подписка на {months} мес.\n"
    "Активна до **{expires}**\n\n"
    "Твоя ссылка:\n`{sub_url}`"
)

ALREADY_UNLIMITED = (
    "💝 **У тебя уже бессрочный доступ.**\n\n"
    "Дополнительная подписка не нужна."
)

BUY_CHOOSE_DONATION = (
    "💝 **У тебя бессрочный доступ.**\n\n"
    "Доп. подписка не нужна — выбирай тариф только если хочется тыкнуть."
)

# Admin
GRANT_OK = "Доступ выдан: {username}\nСрок: {days} дней\nSub: `{sub_url}`"
GRANT_USAGE = "Формат: /grant <tg_id> <days>"

INVITE_CREATED = (
    "🎁 Инвайт создан\n\n"
    "Бессрочный доступ для одного человека.\n\n"
    "Ссылка:\n"
    "`{link}`\n\n"
    "Перешли её — человек жмёт, бот сам всё настроит."
)
INVITE_USAGE = (
    "Формат: /invite [подпись]\n\n"
    "Создаёт бессрочный инвайт на одного человека.\n"
    "Примеры:\n"
    "`/invite`\n"
    "`/invite мама`"
)
INVITE_ACTIVATED = (
    "🎉 Тебе открыли доступ!\n\n"
    "Подписка бессрочная.\n\n"
    "Твоя ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируй и открой **Инструкция**."
)
TRIAL_CREATED = (
    "🎟 Триал-инвайт создан\n\n"
    "Доступ на {days} дней для одного человека.\n\n"
    "Ссылка:\n"
    "`{link}`\n\n"
    "Перешли её — человек жмёт, бот сам всё настроит."
)
TRIAL_INVITE_USAGE = (
    "Формат: /trial [дни] [подпись]\n\n"
    "Создаёт инвайт с доступом на N дней (по умолчанию 30).\n"
    "Примеры:\n"
    "`/trial` — 30 дней\n"
    "`/trial 7` — 7 дней\n"
    "`/trial 14 друг` — 14 дней с подписью"
)
INVITE_ACTIVATED_TRIAL = (
    "🎉 Тебе открыли доступ на {days} дней!\n\n"
    "{status_line}.\n\n"
    "Твоя ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируй и открой **Инструкция**."
)
INVITE_INVALID = "Инвайт не найден или уже использован."
INVITE_EXHAUSTED = "У этого инвайта закончились активации."
INVITE_ALREADY_HAS_SUB = (
    "У тебя уже есть активная подписка — инвайт не нужен 🙂"
)
INVITES_EMPTY = "Нет активных инвайтов."
INVITES_HEADER = "**Инвайты:**\n\n"

WHITELIST_USAGE = (
    "Формат:\n"
    "`/whitelist add @user1 @user2 ...` — добавить (можно пачкой)\n"
    "`/whitelist del @user1 @user2 ...` — удалить\n"
    "`/whitelist` — список"
)
WHITELIST_ADDED = "✅ `@{username}` добавлен в whitelist. При первом `/start` получит бессрочный доступ."
WHITELIST_EXISTS = "`@{username}` уже в whitelist."
WHITELIST_REMOVED = "🗑 `@{username}` удалён из whitelist."
WHITELIST_NOT_FOUND = "`@{username}` не найден в whitelist."
WHITELIST_EMPTY = "Whitelist пуст."
WHITELIST_HEADER = "**Whitelist:**\n\n"

WHITELIST_ACTIVATED = (
    "🎁 Привет! Ты в списке друзей — даю тебе бессрочный доступ.\n\n"
    "Твоя ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируй и открой **Инструкция**."
)

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
