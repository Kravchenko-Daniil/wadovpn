import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import db
import handlers
import redirect
from config import load_config
from marzban import MarzbanAPI

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

    handlers.marzban = marzban_api
    handlers.cfg = cfg

    bot = Bot(
        token=cfg.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)

    redirect_runner = await redirect.start(cfg.redirect_host, cfg.redirect_port)

    try:
        await dp.start_polling(bot)
    finally:
        await redirect_runner.cleanup()
        await marzban_api.close()


if __name__ == "__main__":
    asyncio.run(main())
