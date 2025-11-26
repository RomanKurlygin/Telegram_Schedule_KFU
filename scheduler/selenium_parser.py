from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_schedule_kfu(group_number: str) -> str:
    """
    Заходит на сайт КФУ, выбирает группу и получает расписание.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://kpfu.ru/studentu/ucheba/raspisanie"
        driver.get(url)

        # Ждём поле ввода группы
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
        )
        input_field.clear()
        input_field.send_keys(group_number)

        # Ждём кнопку поиска
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        search_button.click()

        # Ждём таблицу с расписанием
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )

        rows = table.find_elements(By.TAG_NAME, "tr")
        schedule_text = ""
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                line = " | ".join(col.text for col in cols)
                schedule_text += line + "\n"

        if not schedule_text:
            return "Расписание для этой группы не найдено."

        return schedule_text

    except (NoSuchElementException, ElementNotInteractableException):
        return "Не удалось получить расписание. Попробуйте позже."

    except Exception as e:
        return f"Ошибка при получении расписания: {e}"

    finally:
        driver.quit()
