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
        "Привет! Я бот с расписанием занятий КФУ 🎓\n\n"
        "Отправь мне номер группы, и я пришлю расписание.\n"
        "Команды:\n"
        "/today — расписание на сегодня\n"
        "/tomorrow — расписание на завтра\n"
        "/week — расписание на неделю"
    )

@dp.message()
async def set_group(msg: types.Message):
    group_number = msg.text.strip()
    user_groups[msg.from_user.id] = group_number
    await msg.answer(f"Группа {group_number} сохранена ✅\nТеперь используйте команды /today, /tomorrow, /week")