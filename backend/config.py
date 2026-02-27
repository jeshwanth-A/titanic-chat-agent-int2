import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
DATA_PATH = BASE_DIR / "data" / "titanic.csv"
FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = int(os.getenv("PORT", "8000"))
BACKEND_URL = f"http://localhost:{FASTAPI_PORT}"
