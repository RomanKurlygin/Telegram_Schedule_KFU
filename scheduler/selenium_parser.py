from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_schedule_kfu(group_number: str) -> str:
    """
    Заходит на сайт КФУ, выбирает группу и получает расписание.
    """
    options = Options()
    options.add_argument('--headless')       # работа без окна
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # webdriver-manager сам скачает нужный ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://kpfu.ru/studentu/ucheba/raspisanie"
        driver.get(url)

        input_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        input_field.clear()
        input_field.send_keys(group_number)

        search_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
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