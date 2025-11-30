from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("TOKEN")
SAVE_FILE = "saved_schedule.json"
AUTO_FILE = "auto_users.json"