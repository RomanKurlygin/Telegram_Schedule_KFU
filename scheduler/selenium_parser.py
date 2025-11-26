from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROMEDRIVER_PATH

def get_schedule_kfu(group_number:str) -> str:
    """
    Заходит на сайт КФУ, выбирает группу и получает расписание.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://kpfu.ru/studentu/ucheba/raspisanie"
        driver.get(url)

        input_field = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
        input_field.clear()
        input_field.send_keys(group_number)

        search_button = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
        search_button.click()

        driver.implicitly_wait(5)

        table = driver.find_element(By.CSS_SELECTOR, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        schedule_text = ""
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                line = " | ".join(col.text for col in cols)
                schedule_text += line + "\n"

        if not schedule_text:
            schedule_text = "Расписание для этой группы не найдено."

        return schedule_text

    except Exception as e:
        return f"Ошибка при получении расписания: {e}"

    finally:
        driver.quit()