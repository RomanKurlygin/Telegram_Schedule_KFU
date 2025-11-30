from aiogram import Router
from aiogram.types import BufferedInputFile
from parsers.schedule_parser import get_schedule_cached
import matplotlib.pyplot as plt
import io
from aiogram import Bot
from config import TOKEN

bot = Bot(token=TOKEN)
router = Router()

@router.callback_query(lambda c: c.data.startswith("stats_"))
async def show_stats(call):
    _, group = call.data.split("_")
    schedule = get_schedule_cached(group)
    if not schedule:
        await call.answer("❌ Расписание не найдено!", show_alert=True)
        return
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
    buf.seek(0)
    plt.close()
    photo = BufferedInputFile(buf.read(), filename="stats.png")
    await bot.send_photo(call.from_user.id, photo=photo, caption=f"📊 Статистика для группы {group}")
