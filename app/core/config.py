from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    HEADLESS = os.getenv("HEADLESS", "False") == "True"

    MAX_PAGES = int(os.getenv("MAX_PAGES", 5))
    MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", 10))

    MIN_PAGE_DELAY = int(os.getenv("MIN_PAGE_DELAY", 2))
    MAX_PAGE_DELAY = int(os.getenv("MAX_PAGE_DELAY", 6))

    MIN_MESSAGE_DELAY = int(os.getenv("MIN_MESSAGE_DELAY", 5))
    MAX_MESSAGE_DELAY = int(os.getenv("MAX_MESSAGE_DELAY", 15))

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///data/db.sqlite"
    )

    PROFILE_PATH = os.getenv(
        "PROFILE_PATH",
        "data/session/profile"
    )

    EXPORT_PATH = os.getenv(
        "EXPORT_PATH",
        "data/exports"
    )


config = Config()