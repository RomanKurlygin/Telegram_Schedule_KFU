from aiogram import Router, types, Dispatcher
from aiogram.filters import Command

from bot.keyboards import days_keyboard
from parsers.schedule_parser import get_schedule_cached
from storage.storage import save_schedule, load_saved_schedule, load_auto_users, save_auto_users

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Введите номер группы (например 09-515):")

@router.message()
async def get_group(msg: types.Message):
    group = msg.text.strip()
    saved = load_saved_schedule(group)
    if saved:
        get_schedule_cached(group)  # закэшируем сохранённое
        await msg.answer(f"📁 Загружено сохранённое расписание для {group}\nВыберите день:", reply_markup=days_keyboard(group))
        return
    await msg.answer("⏳ Получаю расписание...")
    schedule = get_schedule_cached(group)
    if not schedule:
        await msg.answer("❌ Расписание не найдено.")
        return
    await msg.answer(f"📅 Расписание для {group}\nВыберите день:", reply_markup=days_keyboard(group))

@router.callback_query(lambda c: c.data.startswith("day_"))
async def show_day(call: types.CallbackQuery):
    _, group, day = call.data.split("_")
    schedule = get_schedule_cached(group)
    lessons = schedule.get(day, [])
    text = f"📌 {day}\n\n" + ("\n\n".join(lessons) if lessons else "Нет занятий.")
    await call.message.edit_text(text, reply_markup=days_keyboard(group))

@router.callback_query(lambda c: c.data.startswith("week_"))
async def show_week(call: types.CallbackQuery):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    text = f"📅 Расписание на всю неделю ({group}):\n\n"
    for day, lessons in schedule.items():
        text += f"🔷 {day}\n" + ("\n".join(lessons) if lessons else "Нет занятий") + "\n\n"
    await call.message.edit_text(text, reply_markup=days_keyboard(group))

@router.callback_query(lambda c: c.data.startswith("stats_"))
async def show_stats(call: types.CallbackQuery):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    if not schedule:
        await call.answer("❌ Расписание не найдено!", show_alert=True)
        return

    import matplotlib.pyplot as plt
    import io
    from aiogram.types import BufferedInputFile

    day_counts = {day: len(lessons) for day, lessons in schedule.items()}
    plt.figure(figsize=(8,4))
    days = list(day_counts.keys())
    counts = list(day_counts.values())
    plt.bar(days, counts, color='skyblue')
    plt.title(f"Количество пар по дням - {group}")
    plt.xlabel("День недели")
    plt.ylabel("Количество пар")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    photo = BufferedInputFile(buf.read(), filename="stats.png")
    await call.message.answer_photo(photo=photo, caption=f"📊 Статистика для группы {group}")

@router.callback_query(lambda c: c.data.startswith("auto_"))
async def auto_btn(call: types.CallbackQuery):
    _, group = call.data.split("_")
    users = load_auto_users()
    if any(u["user_id"]==call.from_user.id for u in users):
        await call.answer("⏰ Автоотправка уже включена!", show_alert=True)
        return
    users.append({"user_id": call.from_user.id, "group": group, "morning":"07:00", "evening":"20:00"})
    save_auto_users(users)
    await call.answer("⏰ Автоотправка включена!", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("stopauto_"))
async def stop_auto(call: types.CallbackQuery):
    users = load_auto_users()
    new_users = [u for u in users if u["user_id"] != call.from_user.id]
    save_auto_users(new_users)
    await call.answer("⛔ Автоотправка отключена!", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("save_"))
async def save_btn(call: types.CallbackQuery):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    save_schedule(group, schedule)
    await call.answer("📁 Расписание сохранено!", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("refresh_"))
async def refresh_btn(call: types.CallbackQuery):
    _, group = call.data.split("_")
    schedule_cache = get_schedule_cached.__globals__['schedule_cache']
    schedule_cache.pop(group, None)
    schedule = get_schedule_cached(group)
    if not schedule:
        await call.message.edit_text("❌ Не удалось обновить.")
        return
    await call.message.edit_text(f"📅 Обновлённое расписание для {group}\nВыберите день:", reply_markup=days_keyboard(group))

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
