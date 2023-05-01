from loguru import logger

def get_logger():
    logger.remove()
    LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    logger.add("logger.log", format=LOG_FORMAT)
    return logger
