from logging import Logger


def error_handler(func, logger: Logger):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.critical("Error encountered")
    return wrapper