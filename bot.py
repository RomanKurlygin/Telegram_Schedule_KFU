import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher

user_groups = {}


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(

    )