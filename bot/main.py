import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import db
import handlers
from config import load_config
from marzban import MarzbanAPI
from yookassa_api import YooKassaAPI
from webhook import start_webhook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


async def main():
    cfg = load_config()
    log.info("Starting Wado VPN bot...")

    db.init_db()

    marzban_api = MarzbanAPI(cfg)
    yookassa_api = YooKassaAPI(cfg)

    handlers.marzban = marzban_api
    handlers.yookassa = yookassa_api
    handlers.cfg = cfg

    bot = Bot(
        token=cfg.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)

    webhook_runner = await start_webhook(cfg, bot, marzban_api, yookassa_api)

    try:
        await dp.start_polling(bot)
    finally:
        await webhook_runner.cleanup()
        await marzban_api.close()
        await yookassa_api.close()


if __name__ == "__main__":
    asyncio.run(main())
