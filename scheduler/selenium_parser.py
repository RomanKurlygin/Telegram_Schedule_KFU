from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)

        # вводим номер группы
        input_group = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "p_group_name"))
        )
        input_group.clear()
        input_group.send_keys(group)

        # нажимаем "Показать расписание"
        show_button = driver.find_element(By.CSS_SELECTOR, "div[onclick='submit_group();']")
        show_button.click()

        # ждём таблицу
        table = WebDriverWait(driver, 10).until(
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
                weekday = (weekday + 1) % 6  # только Пн-Сб
            filtered_lines = []
            for line in schedule_text.split("\n"):
                if line.startswith(days[weekday]):
                    filtered_lines.append(line)
            schedule_text = "\n".join(filtered_lines) if filtered_lines else "Нет занятий."

        if not schedule_text:
            schedule_text = "Нет занятий."

        return schedule_text

    except Exception as e:
        return f"Ошибка при получении расписания: {str(e)}"

    finally:
        driver.quit()
