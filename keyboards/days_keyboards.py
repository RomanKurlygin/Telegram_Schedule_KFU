from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def days_keyboard(group):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=d, callback_data=f"day_{group}_{d}") for d in ["Пн","Вт","Ср","Чт","Пт","Сб"]],

    ])