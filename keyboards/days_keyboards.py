from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def days_keyboard(group):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=d, callback_data=f"day_{group}_{d}") for d in ["Пн","Вт","Ср","Чт","Пт","Сб"]],
        [InlineKeyboardButton(text="📅 Вся неделя", callback_data=f"week_{group}")],
        [InlineKeyboardButton(text="⏰ Автоотправка", callback_data=f"auto_{group}"),
         InlineKeyboardButton(text="⛔ Стоп авто", callback_data=f"stopauto_{group}")],
        [InlineKeyboardButton(text="💾 Сохранить", callback_data=f"save_{group}"),
         InlineKeyboardButton(text="🔄 Обновить", callback_data=f"refresh_{group}")],

    ])