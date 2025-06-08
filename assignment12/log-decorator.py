import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):

        call_func = func(*args, **kwargs)

        log_message = (
            f"\nfunction: {func.__name__}"
            f"\npositional parameters: {args if args else 'none'}"
            f"\nkeyword parameters: {kwargs if kwargs else 'none'}"
            f"\nreturn: {call_func}"
            "\n"
        )

        logger.log(logging.INFO, log_message)

        # return from original function call
        return call_func

    return wrapper


# 3
@logger_decorator
def print_hw():
    print("Hello World!")


# 4
@logger_decorator
def return_true(*args):
    return True


# 5
@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator


if __name__ == "__main__":
    # 3
    print_hw()

    # 4
    return_true()
    return_true(1)
    return_true(1, 2, 3)

    # 5
    decorator = return_decorator(a=1, b=2)

    @decorator
    def return_decorator(x):
        return x * 2

    return_decorator(5)
