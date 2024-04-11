from logging import Logger


def error_hendler(logger: Logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.critical("Error encountered")
                return None
        return wrapper
    return decorator