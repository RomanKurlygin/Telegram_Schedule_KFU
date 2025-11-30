from aiogram import Router
from parsers.schedule_parser import get_schedule_cached
from keyboards.days_keyboards import days_keyboard

router = Router()

@router.callback_query(lambda c: c.data.startswith("week_"))
async def show_week(call):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    text = f"📅 Расписание на всю неделю ({group}):\n\n"
    for day, lessons in schedule.items():
        text += f"🔷 {day}\n" + ("\n".join(lessons) if lessons else "Нет занятий") + "\n\n"
    await call.message.edit_text(text, reply_markup=days_keyboard(group))
