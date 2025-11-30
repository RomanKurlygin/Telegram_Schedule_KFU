from aiogram import Router
from aiogram import types
from storage.save_load import load_auto_users, save_auto_users
from parsers.schedule_parser import get_schedule_cached

router = Router()

@router.callback_query(lambda c: c.data.startswith("auto_"))
async def auto_btn(call: types.CallbackQuery):
    _, group = call.data.split("_")
    users = load_auto_users()
    if not isinstance(users, list):
        users = []  # на случай битого файла
    # проверка, есть ли уже пользователь
    if any(isinstance(u, dict) and u.get("user_id")==call.from_user.id for u in users):
        await call.answer("⏰ Автоотправка уже включена!", show_alert=True)
        return
    users.append({"user_id": call.from_user.id, "group": group, "morning":"07:00", "evening":"20:00"})
    save_auto_users(users)
    await call.answer("⏰ Автоотправка включена!", show_alert=True)


@router.callback_query(lambda c: c.data.startswith("stopauto_"))
async def stop_auto(call):
    users = load_auto_users()
    new_users = [u for u in users if u["user_id"] != call.from_user.id]
    save_auto_users(new_users)
    await call.answer("⛔ Автоотправка отключена!", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("save_"))
async def save_btn(call):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    save_auto_users(schedule)  # можно заменить на save_schedule из save_load.py
    await call.answer("📁 Расписание сохранено!", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("refresh_"))
async def refresh_btn(call):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    await call.message.edit_text(f"📅 Обновлённое расписание для {group}\nВыберите день:")
