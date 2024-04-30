import math


def check_if_num(price) -> bool:
    try:
        float(price)
        return True
    except ValueError as valerr:
        raise valerr


def non_empty_string(price) -> bool:
    if len(price) != 0:
        return True
    return False


def check_valid(price) -> bool:
    if check_if_num(price) and non_empty_string(price) is True:
        return True
    return False
