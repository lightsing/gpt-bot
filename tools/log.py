import logging

logger = logging.getLogger("tool")
logger.setLevel(logging.INFO)


def get_logger(suffix):
    return logger.getChild(suffix)
