# logger.py
import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message, level="info"):
    if level == "info":
        logging.info(message)
    else:
        logging.error(message)
