def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return type_of_output(result)

        return wrapper

    return decorator


# 3
@type_converter(str)
def return_int():
    return 5


# result = return_int()
# print(result)
# print(type(result))


# 4 string to int
@type_converter(int)
def return_string():
    return "not a number"


if __name__ == "__main__":

    y = return_int()
    print(type(y).__name__)  # This should print "str"
    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  # This is what should happen
