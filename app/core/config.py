import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Constructure AI Email Assistant"
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    GOOGLE_CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET_FILE", "client_secret.json")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SESSION_SECRET = os.getenv("SESSION_SECRET", "super-secret-session-key-that-is-long-enough-for-sha256-algorithm")

settings = Settings()
