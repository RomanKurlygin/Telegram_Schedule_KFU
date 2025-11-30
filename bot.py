import asyncio
from aiogram import Bot, Dispatcher, Router
from config import TOKEN
from handlers import start_handler, day_handler, week_handler, stats_handler, auto_handler
from tasks.auto_sender import auto_sender

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Подключаем роутеры из файлов
router.include_router(start_handler.router)
router.include_router(day_handler.router)
router.include_router(week_handler.router)
router.include_router(stats_handler.router)
router.include_router(auto_handler.router)

async def main():
    asyncio.create_task(auto_sender(bot))  # запускаем автоотправку
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
