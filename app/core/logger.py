from loguru import logger
import sys
import os

os.makedirs("data/logs", exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format=(
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "{message}"
    )
)

logger.add(
    "data/logs/parser.log",
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    level="INFO"
)

app_logger = logger