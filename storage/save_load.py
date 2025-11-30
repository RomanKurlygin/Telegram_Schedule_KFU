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

def load_saved_schedule(group):
        if not os.path.exists(SAVE_FILE):
            return None
        with open(SAVE_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
        return data.get(group)

def load_auto_users():
        if not os.path.exists(AUTO_FILE):
            return []
        with open(AUTO_FILE, 'r', encoding="utf-8") as f:
            return json.load(f)

def save_auto_users(users):
        with open(AUTO_FILE, 'w', encoding="utf-8") as f:
            json.dump(users, f, indent=4)


