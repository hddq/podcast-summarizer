import os
from dotenv import load_dotenv

load_dotenv()

GPODDER_BASE_URL = os.getenv("GPODDER_BASE_URL", "").rstrip("/")
GPODDER_USERNAME = os.getenv("GPODDER_USERNAME")
GPODDER_PASSWORD = os.getenv("GPODDER_PASSWORD")
SINCE_TIMESTAMP = int(os.getenv("SINCE_TIMESTAMP", "0"))
DOWNLOAD_DIR = "downloads"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

AUTH = (GPODDER_USERNAME, GPODDER_PASSWORD)
