import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from core.config import settings


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        self.baseFilename = get_log_filename()
        super().doRollover()


def get_log_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(settings.LOGS_PATH, f"log_{today}.log")


def init_logger():
    os.makedirs(settings.LOGS_PATH, exist_ok=True)

    log_handler = CustomTimedRotatingFileHandler(
        get_log_filename(), when="midnight", interval=1, encoding="utf-8"
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(message)s",
        datefmt="%H:%M:%S",
    )
    log_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Основные логгеры FastAPI / Uvicorn
    log_names = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "httpx",
    ]  # можешь добавить свое

    for name in log_names:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)
        logger.propagate = False  # важно: иначе будут дубли в root
