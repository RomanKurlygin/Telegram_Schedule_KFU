import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import register_handlers
from config import TOKEN
from tasks.auto_sender import auto_sender
from storage.storage import load_auto_users

TOKEN = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def main():
    asyncio.create_task(auto_sender(bot, load_auto_users, "auto_users.json"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
