import os
from dotenv import load_dotenv
from typing import List
from pathlib import Path

# ========================
# Load Environment File
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env.dev"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)


class Settings:

    # ========================
    # 🌍 Environment
    # ========================
    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # ========================
    # 🗄 Database
    # ========================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )

    # ========================
    # 🔐 JWT
    # ========================
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
    )

    # ========================
    # 🔑 Google OAuth
    # ========================
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")

    # ========================
    # 🌐 CORS
    # ========================
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "*"
    ).split(",")

    # ========================
    # Validate Critical Config
    # ========================
    def validate(self):
        if self.ENV == "prod" and not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is required in production.")


settings = Settings()
settings.validate()
