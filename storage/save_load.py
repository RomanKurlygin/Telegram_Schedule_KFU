import json, os
from config import SAVE_FILE, AUTO_FILE

def save_schedule(group, data):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding="utf-8") as f:
            file_data = json.load(f)
    else:
        file_data = {}
    file_data[group] = data
    with open(SAVE_FILE, 'w', encoding="utf-8") as f:
        json.dump(file_data, f, ensure_ascii=False, indent=4)

