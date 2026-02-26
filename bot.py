import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

from database.db import init_db
from handlers import common, booking, admin
from services.reminders import start_scheduler

load_dotenv()

async def main() -> None:
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(booking.router)
    dp.include_router(admin.router)

    await init_db()
    await start_scheduler(bot)

    print("✅ Бот @Nails001_Manik_bot запущений українською мовою!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
