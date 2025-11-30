import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

schedule_cache = {}

def get_schedule(group: str):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://kpfu.ru/studentu/ucheba/raspisanie")

    input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "p_group_name")))
    input_box.clear()
    input_box.send_keys(group)
    driver.execute_script("submit_group();")

    print_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@onclick,'window.open')]"))
    )
    print_url = print_button.get_attribute("onclick").split("'")[1]
    driver.get(print_url)
    time.sleep(1)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return None
    rows = table.find_all("tr")

    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
    schedule_dict = {day: [] for day in days}

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue
        time_slot = cols[0].get_text(strip=True)
        for day, col in zip(days, cols[1:]):
            content = col.get_text("\n", strip=True)
            if content:
                lines = content.split("\n")
                subject = lines[0]
                details = "\n".join(lines[1:])
                formatted = f"⏰ {time_slot}\n📘 {subject}"
                if details:
                    formatted += f"\n🏫 {details}"
                schedule_dict[day].append(formatted)
    return schedule_dict

def get_schedule_cached(group):
    if group in schedule_cache:
        return schedule_cache[group]
    schedule = get_schedule(group)
    if schedule:
        schedule_cache[group] = schedule
    return schedule
