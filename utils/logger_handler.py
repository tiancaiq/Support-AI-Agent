from datetime import datetime
import logging
import os
import sys

from utils.path_tool import get_abs_path

LOG_ROOT = get_abs_path("logs")
#make dir
os.makedirs(LOG_ROOT, exist_ok=True)

#log config
DEFAULT_LOGGING_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s -%(filename)s:%(lineno)d - %(message)s'
)

def get_logger(
        name: str ="agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)


    # avoiding add muti handler
    if logger.handlers:
        return logger
    # handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOGGING_FORMAT)

    logger.addHandler(console_handler)

    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOGGING_FORMAT)
    logger.addHandler(file_handler)

    return logger

# logger shortcut
logger = get_logger()

if __name__ == '__main__':
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.debug("debug")