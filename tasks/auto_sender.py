import asyncio, time
from storage.save_load import load_auto_users
from parsers.schedule_parser import get_schedule_cached
from aiogram import Bot
from config import TOKEN

bot = Bot(token=TOKEN)

async def auto_sender(bot):
    while True:
        now = time.localtime()
        current_time = f"{now.tm_hour:02d}:{now.tm_min:02d}"
        users = load_auto_users()
        for u in users:
            schedule = get_schedule_cached(u["group"])
            if current_time == u.get("morning"):
                day = ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"][now.tm_wday]
                lessons = schedule.get(day, [])
                text = f"⏰ Расписание на сегодня ({day}):\n\n" + ("\n\n".join(lessons) if lessons else "Нет занятий")
                await bot.send_message(u["user_id"], text)
            if current_time == u.get("evening"):
                tomorrow = (now.tm_wday + 1) % 7
                day = ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"][tomorrow]
                lessons = schedule.get(day, [])
                text = f"🌙 Расписание на завтра ({day}):\n\n" + ("\n\n".join(lessons) if lessons else "Нет занятий")
                await bot.send_message(u["user_id"], text)
        await asyncio.sleep(60)
