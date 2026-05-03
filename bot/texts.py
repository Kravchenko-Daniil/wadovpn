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
    "Ваша ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируйте и откройте **Инструкция**."
)

SUB_INFO = (
    "{status_line}\n"
    "Трафик: {used} / {limit}\n\n"
    "Ссылка:\n"
    "`{sub_url}`"
)

SUB_EXPIRED = "Подписка истекла. Можно бесплатно продлить кнопкой ниже 👇"

INSTALL_CHOOSE = "Выберите платформу:"

INSTALL_ANDROID = (
    "<b>Android</b>\n\n"
    "1. Установите <a href=\"https://play.google.com/store/apps/details?id=com.v2ray.ang\">v2rayNG</a> "
    "или <a href=\"https://play.google.com/store/apps/details?id=app.hiddify.com\">Hiddify</a>\n"
    "2. Откройте <a href=\"https://t.me/wadovpn_bot?start=mysub\">Мою подписку</a> и скопируйте ссылку\n"
    "3. В приложении нажмите + → Импорт из буфера\n"
    "4. Нажмите кнопку подключения"
)

INSTALL_IOS = (
    "<b>iOS</b>\n\n"
    "Все три приложения работают в российском App Store:\n"
    "• <a href=\"https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973\">Happ Proxy Utility Plus</a> — бесплатно, рекомендую\n"
    "• <a href=\"https://apps.apple.com/ru/app/karing/id6472431552\">Karing</a> — бесплатно, запасной вариант\n"
    "• <a href=\"https://apps.apple.com/ru/app/shadowrocket/id932747118\">Shadowrocket</a> — 249 ₽, для тех, кто хочет надёжнее\n\n"
    "1. Установите любое из них\n"
    "2. Откройте <a href=\"https://t.me/wadovpn_bot?start=mysub\">Мою подписку</a> и скопируйте ссылку\n"
    "3. В приложении нажмите + → Добавить из буфера\n"
    "4. Нажмите кнопку подключения"
)

INSTALL_WINDOWS = (
    "<b>Windows</b>\n\n"
    "1. Скачайте <a href=\"https://github.com/hiddify/hiddify-app/releases/latest\">Hiddify-Next</a>\n"
    "2. Установите и запустите\n"
    "3. Откройте <a href=\"https://t.me/wadovpn_bot?start=mysub\">Мою подписку</a> и скопируйте ссылку\n"
    "4. Нажмите + → Добавить из буфера\n"
    "5. Нажмите кнопку подключения"
)

INSTALL_MACOS = (
    "<b>macOS</b>\n\n"
    "1. Скачайте <a href=\"https://github.com/hiddify/hiddify-app/releases/latest\">Hiddify-Next</a> "
    "или <a href=\"https://apps.apple.com/app/v2box-v2ray-client/id6446814690\">V2Box</a>\n"
    "2. Откройте <a href=\"https://t.me/wadovpn_bot?start=mysub\">Мою подписку</a> и скопируйте ссылку\n"
    "3. Добавьте подписку из буфера\n"
    "4. Подключитесь"
)

NO_SUB = (
    "У вас пока нет подписки.\n"
    "Нажмите «🎁 Получить доступ бесплатно» — выдам без оплаты."
)

NO_SUB_WITH_TRIAL = (
    "У вас пока нет подписки.\n"
    "Можно начать с триала на 3 дня или сразу взять доступ бесплатно."
)

HELP_TEXT = (
    "**Не подключается?**\n"
    "Попробуйте другое приложение.\n\n"
    "**Медленно?**\n"
    "Смените протокол в настройках.\n\n"
    "**Не помогло?**\n"
    "Напишите админу."
)

BUY_CHOOSE = (
    "🎁 **Доступ бесплатно**\n\n"
    "Выберите, на сколько включить — оплата не нужна, ничего списывать не будем."
)

SUB_ACTIVATED = (
    "✅ **Доступ открыт!**\n\n"
    "Подписка на {months} мес.\n"
    "Активна до **{expires}**\n\n"
    "Ваша ссылка:\n`{sub_url}`"
)

ALREADY_UNLIMITED = (
    "💝 **У вас уже бессрочный доступ.**\n\n"
    "Дополнительная подписка не нужна."
)

BUY_CHOOSE_DONATION = (
    "💝 **У вас бессрочный доступ.**\n\n"
    "Доп. подписка не нужна — выбирайте тариф, только если хочется тыкнуть."
)

# Admin
GRANT_OK = "Доступ выдан: {username}\nСрок: {days} дней\nSub: `{sub_url}`"
GRANT_USAGE = "Формат: /grant <tg_id> <days>"

INVITE_CREATED = (
    "🎁 Инвайт создан\n\n"
    "Бессрочный доступ для одного человека.\n\n"
    "Ссылка:\n"
    "`{link}`\n\n"
    "Перешлите её — человек жмёт, бот сам всё настроит."
)
INVITE_USAGE = (
    "Формат: /invite [подпись]\n\n"
    "Создаёт бессрочный инвайт на одного человека.\n"
    "Примеры:\n"
    "`/invite`\n"
    "`/invite мама`"
)
INVITE_ACTIVATED = (
    "🎉 Вам открыли доступ!\n\n"
    "Подписка бессрочная.\n\n"
    "Ваша ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируйте и откройте **Инструкция**."
)
TRIAL_CREATED = (
    "🎟 Триал-инвайт создан\n\n"
    "Доступ на {days} дней для одного человека.\n\n"
    "Ссылка:\n"
    "`{link}`\n\n"
    "Перешлите её — человек жмёт, бот сам всё настроит."
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
    "🎉 Вам открыли доступ на {days} дней!\n\n"
    "{status_line}.\n\n"
    "Ваша ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируйте и откройте **Инструкция**."
)
INVITE_INVALID = "Инвайт не найден или уже использован."
INVITE_EXHAUSTED = "У этого инвайта закончились активации."
INVITE_ALREADY_HAS_SUB = (
    "У вас уже есть активная подписка — инвайт не нужен 🙂"
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
    "🎁 Здравствуйте! Вы в списке друзей — даю вам бессрочный доступ.\n\n"
    "Ваша ссылка:\n"
    "`{sub_url}`\n\n"
    "Скопируйте и откройте **Инструкция**."
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
