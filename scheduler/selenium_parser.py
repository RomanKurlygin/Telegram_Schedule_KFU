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