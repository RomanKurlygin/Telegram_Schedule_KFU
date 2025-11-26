import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from auto_post import daily_notification
from config import TOKEN
from scheduler.selenium_parser import get_schedule_kfu

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message(lambda msg: not msg.text.startswith("/"))
async def set_group(msg: types.Message):
    group_number = msg.text.strip()

    if len(group_number) < 3 or " " in group_number:
        await msg.answer("Отправьте корректный номер группы, например: 09-515")
        return

    user_groups[msg.from_user.id] = group_number
    await msg.answer(
        f"Группа {group_number} сохранена ✅\nТеперь используйте команды /today, /tomorrow, /week"
    )

async def send_schedule(msg: types.Message, day: str):
    group = user_groups.get(msg.from_user.id)
    if not group:
        await msg.answer("Сначала отправьте номер группы")
        return

    await msg.answer("⏳ Получаем расписание, подождите...")
    schedule = get_schedule_kfu(group, day)
    if day == "today":
        header = "📅 Расписание на сегодня:\n"
    elif day == "tomorrow":
        header = "📅 Расписание на завтра:\n"
    else:
        header = "📅 Расписание на неделю:\n"

    await msg.answer(header + schedule)


@dp.message(Command("today"))
async def today_cmd(msg: types.Message):
    await send_schedule(msg, "today")

@dp.message(Command("tomorrow"))
async def tomorrow_cmd(msg: types.Message):
    await send_schedule(msg, "tomorrow")

@dp.message(Command("week"))
async def week_cmd(msg: types.Message):
    await send_schedule(msg, "week")




async def main():

    TEST_GROUP = "09-515"
    asyncio.create_task(daily_notification(bot, TEST_GROUP))


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
