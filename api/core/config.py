import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")


if not SECRET_KEY:
    raise RuntimeError("AUTH_SECRET_KEY must be configured")
