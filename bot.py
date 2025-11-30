import asyncio
from aiogram import Bot, Dispatcher, Router
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


