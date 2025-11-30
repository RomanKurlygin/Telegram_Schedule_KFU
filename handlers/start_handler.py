from aiogram import Router, types
from aiogram.filters import Command
from storage.save_load import load_saved_schedule
from parsers.schedule_parser import get_schedule_cached
from keyboards.days_keyboards import days_keyboard

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Введите номер группы (например 09-515):")

@router.message()
async def get_group(msg: types.Message):
    group = msg.text.strip()
    saved = load_saved_schedule(group)
    if saved:
        get_schedule_cached(group)  # обновляем кэш
        await msg.answer(f"📁 Загружено сохранённое расписание для {group}\nВыберите день:",
                         reply_markup=days_keyboard(group))
        return
    await msg.answer("⏳ Получаю расписание...")
    schedule = get_schedule_cached(group)
    if not schedule:
        await msg.answer("❌ Расписание не найдено.")
        return
    await msg.answer(f"📅 Расписание для {group}\nВыберите день:", reply_markup=days_keyboard(group))
