import pytest
from parsers.schedule_parser import get_schedule
from storage.storage import save_schedule, load_saved_schedule
from bot.keyboards import days_keyboard
from aiogram.types import InlineKeyboardMarkup

# ===== Тест функции парсинга =====
def test_get_schedule():
    group = "09-515"
    schedule = get_schedule(group)
    assert schedule is not None, "Расписание не должно быть None"
    assert isinstance(schedule, dict), "Расписание должно быть словарем"
    for day in ["Пн","Вт","Ср","Чт","Пт","Сб"]:
        assert day in schedule, f"День {day} должен быть в расписании"

# ===== Тест функции сохранения и загрузки =====
def test_save_load_schedule(tmp_path):
    # tmp_path — временная директория, предоставляемая pytest
    save_file = tmp_path / "saved_schedule.json"

    # Используем monkeypatch, чтобы временно заменить путь файла
    from storage import storage
    original_file = storage.SAVE_FILE
    storage.SAVE_FILE = str(save_file)

    group = "09-515"
    data = {"Пн": ["Тестовая пара 1"], "Вт": [], "Ср": [], "Чт": [], "Пт": [], "Сб": []}
    save_schedule(group, data)
    loaded = load_saved_schedule(group)
    assert loaded == data, "Загруженные данные должны совпадать с сохранёнными"

    # Восстанавливаем оригинальный путь
    storage.SAVE_FILE = original_file

# ===== Тест функции клавиатуры =====
def test_days_keyboard():
    kb = days_keyboard("09-515")
    assert isinstance(kb, InlineKeyboardMarkup), "Должен возвращаться объект InlineKeyboardMarkup"
    # Проверяем, что кнопки существуют
    assert len(kb.inline_keyboard) > 0, "Кнопки должны быть не пустыми"
