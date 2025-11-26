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



@dp.message(Command("today"))
async def today_cmd(msg: types.Message):
    group = user_groups.get(msg.from_user.id)
    if not group:
        await msg.answer("Сначала отправьте номер группы")
        return
    schedule = get_schedule_kfu(group)
    await msg.answer("📅 Расписание на сегодня:\n" + schedule)

@dp.message(Command("tomorrow"))
async def tomorrow_cmd(msg: types.Message):
    group = user_groups.get(msg.from_user.id)
    if not group:
        await msg.answer("Сначала отправьте номер группы")
        return
    schedule = get_schedule_kfu(group)
    await msg.answer("📅 Расписание на завтра:\n" + schedule)


async def main():
    TEST_GROUP = "09-515"
    asyncio.create_task(daily_notification(bot, TEST_GROUP))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



