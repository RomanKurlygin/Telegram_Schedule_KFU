from aiogram import Router
from parsers.schedule_parser import get_schedule_cached
from keyboards.days_keyboard import days_keyboard

router = Router()

@router.callback_query(lambda c: c.data.startswith("day_"))
async def show_day(call):
    _, group, day = call.data.split("_")
    schedule = get_schedule_cached(group)
    lessons = schedule.get(day, [])
    text = f"📌 {day}\n\n" + ("\n\n".join(lessons) if lessons else "Нет занятий.")
    await call.message.edit_text(text, reply_markup=days_keyboard(group))
