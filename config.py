from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
