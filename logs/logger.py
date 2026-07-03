import logging


logging.basicConfig(
    filename="chat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_event(message):

    logging.info(message)