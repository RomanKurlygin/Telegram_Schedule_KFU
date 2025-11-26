import asyncio
from datetime import datetime
from config import CHAT_ID
from scheduler.selenium_parser import get_schedule_kfu
from aiogram import Bot

async def daily_notification(bot: Bot, group_number: str):
    """
    Автопостинг расписания:
    - 08:00 — расписание на сегодня
    - 20:00 — расписание на завтра
    """
    while True:
        now = datetime.now()
        time_str = now.strftime("%H:%M")

        if time_str == "08:00":
            schedule = get_schedule_kfu(group_number)
            await bot.send_message(CHAT_ID, "Доброе утро! 🌞\n" + schedule)

        if time_str == "20:00":
            schedule = get_schedule_kfu(group_number)
            await bot.send_message(CHAT_ID, "Вечерняя рассылка 🌙\n" + schedule)

        await asyncio.sleep(60)
