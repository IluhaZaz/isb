from logging import Logger


def error_hendler(func, logger: Logger):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.critical("Error encountered")
            return None
    return wrapper