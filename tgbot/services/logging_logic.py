import os

import logging
from logging.handlers import RotatingFileHandler
import betterlogging as bl


logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


def register_logger():
    """
    Настройка логгера.

    :return: None
    """
    log_format = (
        "%(filename)s [LINE:%(lineno)d] #%(levelname)-6s [%(asctime)s]  %(message)s"
    )
    date_format = "%d.%m.%Y %H:%M:%S"

    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        level=log_level,
    )
    logger = logging.getLogger()

    logger.setLevel(log_level)

    log_file_path = os.path.join("logs", "bot.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5
    )  # Максимальный размер файла 10 МБ, хранится 5 файлов
    file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    logger.addHandler(file_handler)

    logger.info("Starting bot")
