from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

def get_schedule_kfu(group_number: str, day: str = "today") -> str:
    """
    Получает расписание КФУ для указанной группы и дня.
    day: "today", "tomorrow" или "week"
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://kpfu.ru/studentu/ucheba/raspisanie")


        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        input_field.clear()
        input_field.send_keys(group_number)


        search_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", search_button)


        table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")


        schedule_text = ""
        today_date = datetime.now().date()
        tomorrow_date = today_date + timedelta(days=1)

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if not cols:
                continue


            date_str = cols[0].text.strip()
            try:
                lesson_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            except ValueError:
                lesson_date = None  # пропускаем строки без даты

            line = " | ".join(col.text for col in cols)

            if day == "today" and lesson_date == today_date:
                schedule_text += line + "\n"
            elif day == "tomorrow" and lesson_date == tomorrow_date:
                schedule_text += line + "\n"
            elif day == "week":
                schedule_text += line + "\n"

        if not schedule_text:
            schedule_text = "Расписание для этой группы не найдено."

        return schedule_text

    except TimeoutException:
        return "Не удалось загрузить расписание. Попробуйте позже."
    except NoSuchElementException:
        return "Не удалось найти расписание на сайте КФУ."
    except Exception as e:
        return f"Ошибка при получении расписания: {e}"
    finally:
        driver.quit()
