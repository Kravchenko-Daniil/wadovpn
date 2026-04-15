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

ASK_EMAIL = (
    "Введи email для отправки чека:\n\n"
    "_Чек придёт от ФНС на указанный адрес — это обязательно по закону (54-ФЗ)._"
)

EMAIL_INVALID = "Это не похоже на email. Попробуй ещё раз:"

PAY_CREATED = (
    "**Тариф:** {label}\n"
    "**Сумма:** {price} ₽\n\n"
    "Нажми **«💳 Оплатить»**. Ссылка живёт ~10 минут — "
    "если закрыл окно, нажми **«🔄 Новая ссылка»**.\n\n"
    "После оплаты подписка активируется автоматически."
)

PAY_OK = (
    "✅ **Оплата получена!**\n\n"
    "Подписка продлена на {months} мес.\n"
    "Активна до **{expires}**\n\n"
    "Твоя ссылка:\n`{sub_url}`"
)

PAY_CANCELED = (
    "❌ Оплата не прошла.\n"
    "Попробуй ещё раз или напиши в поддержку."
)

# Admin
GRANT_OK = "Доступ выдан: {username}\nСрок: {days} дней\nSub: `{sub_url}`"
GRANT_USAGE = "Формат: /grant <tg_id> <days>"

INVITE_CREATED = (
    "🎁 Инвайт создан\n\n"
    "Бессрочный доступ, активаций: {max_uses}\n\n"
    "Ссылка для друга:\n"
    "`{link}`\n\n"
    "Просто перешли её — человек жмёт, бот сам всё настроит."
)
INVITE_USAGE = (
    "Формат: /invite [max_uses] [note]\n\n"
    "Примеры:\n"
    "`/invite` — на одного человека\n"
    "`/invite 5` — на 5 человек\n"
    "`/invite 1 мама` — с подписью"
)
INVITE_ACTIVATED = (
    "🎉 Тебе открыли доступ!\n\n"
    "Подписка бессрочная.\n\n"
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

ADMIN_PAYMENT_NOTIFY = (
    "💰 **Новая оплата**\n\n"
    "Сумма: **{amount} ₽**\n"
    "План: {label} ({months} мес.)\n"
    "Юзер: {user_link} (`{tg_id}`)\n"
    "Активна до: **{expires}**\n"
    "Payment ID: `{payment_id}`\n\n"
    "👉 Пробей чек в «Мой налог»"
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
