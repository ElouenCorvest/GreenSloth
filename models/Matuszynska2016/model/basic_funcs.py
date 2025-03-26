def continous_subtraction(*args) -> float:
    if len(args) <= 1:
        raise ValueError("Not enough arguments given")
    else:
        v = args[0]
        for i in args[1:]:
            v -= i
        return v


def two_divided_value(x: float) -> float:
    return 2 / x


def four_divided_value(x: float) -> float:
    return 4 / x


def neg_fourteenthirds_divided_value(x: float) -> float:
    return -(14 / 3) / x


def neg_divided_value(x: float) -> float:
    return -1 / x
