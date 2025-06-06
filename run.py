import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router


async def main():
    load_dotenv()
    bot = Bot(os.getenv("TG_BOT"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
