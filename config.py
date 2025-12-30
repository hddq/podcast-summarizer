import os
from dotenv import load_dotenv

load_dotenv()

GPODDER_BASE_URL = os.getenv("GPODDER_BASE_URL", "").rstrip("/")
GPODDER_USERNAME = os.getenv("GPODDER_USERNAME")
GPODDER_PASSWORD = os.getenv("GPODDER_PASSWORD")
SINCE_TIMESTAMP = int(os.getenv("SINCE_TIMESTAMP", "0"))
DOWNLOAD_DIR = "data/downloads"
TRANSCRIPT_DIR = "data/transcripts"
SUMMARY_DIR = "data/summaries"
PROMPT_FILE = "prompt.md"
MODELS_DIR = "data/models"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower() # gemini or ollama
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Whisper settings
WHISPER_ROOT = "/app/whisper.cpp"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
# The expected path for the model file
WHISPER_MODEL_PATH = os.path.join(MODELS_DIR, f"ggml-{WHISPER_MODEL}.bin")
WHISPER_BIN = os.getenv("WHISPER_BIN", os.path.join(WHISPER_ROOT, "build/bin/whisper-cli"))

AUTH = (GPODDER_USERNAME, GPODDER_PASSWORD)
