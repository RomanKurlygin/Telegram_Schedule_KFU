from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime

URL = "https://kpfu.ru/studentu/ucheba/raspisanie"

def get_schedule_kfu(group: str, mode="today"):
    """
    mode: 'today', 'tomorrow', 'week'
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)

        # вводим номер группы
        input_group = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "p_group_name"))
        )
        input_group.clear()
        input_group.send_keys(group)
        input_group.send_keys(Keys.ENTER)  # триггер JS autocomplete

        # вызываем JS функцию submit_group()
        driver.execute_script("submit_group();")

        # ждём, пока таблица появится
        table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )

        # собираем строки
        rows = table.find_elements(By.TAG_NAME, "tr")
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
        schedule_text = ""

        for row in rows[1:]:  # пропускаем заголовок
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells:
                continue
            time_cell = cells[0].text.strip()
            day_cells = cells[1:]

            for i, cell in enumerate(day_cells):
                text = cell.text.strip()
                if text:
                    schedule_text += f"{days[i]} {time_cell}: {text}\n"

        # фильтр по today/tomorrow
        if mode in ["today", "tomorrow"]:
            weekday = datetime.datetime.today().weekday()  # 0-Пн ... 6-Вс
            if mode == "tomorrow":
                weekday = (weekday + 1) % 7  # Пн-Сб-Сб/Вс
            filtered_lines = []
            for line in schedule_text.split("\n"):
                if line.startswith(days[weekday % 6]):  # только Пн-Сб
                    filtered_lines.append(line)
            schedule_text = "\n".join(filtered_lines) if filtered_lines else "Нет занятий."

        if not schedule_text:
            schedule_text = "Нет занятий."

        return schedule_text

    except Exception as e:
        return f"Ошибка при получении расписания: {str(e)}"

    finally:
        driver.quit()
