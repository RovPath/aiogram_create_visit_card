import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.create_handlers import router as create_router
from app.handlers.edit_handlers import router as edit_router


async def main():
    load_dotenv()
    bot = Bot(os.getenv("TG_BOT"))
    dp = Dispatcher()
    dp.include_routers(create_router, edit_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
