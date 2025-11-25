from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROMEDRIVER_PATH

def get_schedule_kfu():
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

        search = driver.find_element(By.CSS_SELECTOR, "input[type=text]")