from aiogram import Router, types
from aiogram.filters import Command
from storage.save_load import load_saved_schedule

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Введите номер группы (например 09-515):")

@router.message()
async def get_group(msg: types.Message):
    group = msg.text.strip()
    saved = load_saved_schedule(group)
