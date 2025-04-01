import logging
import os
import sys

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from src import config, database, routers
from src.middlewares import UserMiddleware

i18n = I18n(path="locales", default_locale="en", domain="messages")

dp = Dispatcher()
dp.include_routers(*[getattr(routers, router_name) for router_name in routers.__all__])

dp.message.middleware(ChatActionMiddleware())
dp.message.middleware(UserMiddleware())
dp.message.middleware(SimpleI18nMiddleware(i18n))
dp.callback_query.middleware(ChatActionMiddleware())
dp.callback_query.middleware(UserMiddleware())
dp.callback_query.middleware(SimpleI18nMiddleware(i18n))


@dp.startup()
async def on_startup() -> None:
    await database.init_db()


@dp.shutdown()
async def on_shutdown() -> None:
    await database.close_db()
    logging.shutdown()


async def main() -> None:
    if not config.BOT_TOKEN:
        raise EnvironmentError("Missing environment variable: CORE_BOT_TOKEN")

    os.makedirs("data", exist_ok=True)

    proxy_url = os.getenv("CORE_PROXY")
    if proxy_url:
        logging.info(f"Using proxy: {proxy_url}")

    bot = Bot(
        token=config.BOT_TOKEN,
        session=AiohttpSession(proxy=proxy_url or None),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)s] <%(filename)s:%(funcName)s:%(lineno)d> - %(message)s",
    )
    uvloop.run(main(), debug=config.DEBUG)
