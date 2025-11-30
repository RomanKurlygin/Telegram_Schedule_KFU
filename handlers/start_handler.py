from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Введите номер группы (например 09-515):")