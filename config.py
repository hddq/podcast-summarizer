import os
from dotenv import load_dotenv

load_dotenv()

GPODDER_BASE_URL = os.getenv("GPODDER_BASE_URL", "").rstrip("/")
GPODDER_USERNAME = os.getenv("GPODDER_USERNAME")
GPODDER_PASSWORD = os.getenv("GPODDER_PASSWORD")
SINCE_TIMESTAMP = int(os.getenv("SINCE_TIMESTAMP", "0"))
DOWNLOAD_DIR = "downloads"
TRANSCRIPT_DIR = "transcripts"
MODELS_DIR = "models"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Whisper settings
WHISPER_ROOT = "/app/whisper.cpp"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
# The expected path for the model file
WHISPER_MODEL_PATH = os.path.join(MODELS_DIR, f"ggml-{WHISPER_MODEL}.bin")

AUTH = (GPODDER_USERNAME, GPODDER_PASSWORD)
