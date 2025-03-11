from __future__ import annotations
from typing import Literal
import numpy as np


# Direct Values

def value(x: float) -> float:
    return x

def neg_value(x: float) -> float:
    return -1 * x

def two_value(x: float) -> float:
    return 2 * x

def neg_two_value(x: float) -> float:
    return -2 * x

def three_value(x: float) -> float:
    return 3 * x

def neg_three_value(x: float) -> float:
    return -3 * x

def four_value(x: float) -> float:
    return 4 * x

def neg_four_value(x: float) -> float:
    return -4 * x

def five_value(x: float) -> float:
    return 5 * x

def neg_five_value(x: float) -> float:
    return -5 * x

def fourteen_thirds_value(x: float) -> float:
    return 14/3 * x

def neg_fourteen_thirds_value(x: float) -> float:
    return -14/3 * x

# Fractioning

def divided_value(x: float) -> float:
    return 1 / x

def neg_divided_value(x: float) -> float:
    return -1 / x

def two_divided_value(x: float) -> float:
    return 2 / x

def neg_two_divided_value(x: float) -> float:
    return -2 / x

def three_divided_value(x: float) -> float:
    return 3 / x

def neg_three_divided_value(x: float) -> float:
    return -3 / x

def four_divided_value(x: float) -> float:
    return 4 / x

def neg_four_divided_value(x: float) -> float:
    return -4 / x

def value1_divided_value2(x: float, y: float) -> float:
    return x / y

def neg_value1_divided_value2(x: float, y: float) -> float:
    return - (x / y)

def two_value1_divided_value2(x: float, y: float) -> float:
    return 2 * x / y

def neg_two_value1_divided_value2(x: float, y: float) -> float:
    return -2 * x / y

def fourteenthirds_value1_divided_value2(x: float, y: float) -> float:
    return (14/3) * (x / y)

def neg_fourteenthirds_value1_divided_value2(x: float, y: float) -> float:
    return -(14/3) * (x / y)

# Advanced

def proportional(*args) -> float:
    if len(args) <= 1:
        raise ValueError("Not enough arguments given")
    else:
        v = args[0]
        for i in args[1:]:
            v *= i
        return v

def continous_subtraction(*args) -> float:
    if len(args) <= 1:
        raise ValueError("Not enough arguments given")
    else:
        v = args[0]
        for i in args[1:]:
            v -= i
        return v

def quadratic(
    a: float,
    b: float,
    c: float,
    option: Literal["max", "min", "both"]
) -> float:
    """
    This function will calculate the quadratic equation from the parts given respectively to this format:

    a x**2 + b x + c

    Args:
        a (float): Part of the quadratic equation
        b (float): Part of the quadratic equation
        c (float): Part of the quadratic equation
        option (Either 'max', 'min', or 'both'): Determines what type of output you wish to get, when your answer has two solutions. The max, min or both in a Tuple.

    Returns:
        float: _description_
    """
    d = b**2 - 4 * a * c
    conds = [d > 0, d == 0]

    r1 = np.select(
        conds,
        [
            (-b + np.sqrt(d)) / (2 * a),
            -b / (2 * a),
        ],
        None
    )
    r2 = np.select(
        conds,
        [
            (-b - np.sqrt(d)) / (2 * a),
            -b / (2 * a)
        ],
        None
    )

    if option == "max":
        x = np.select(
            [
                r1 > r2,
                r1 <= r2
            ],
            [
                r1,
                r2
            ]
        )
    elif option == "min":
        x = np.select(
            [
                r1 < r2,
                r1 >= r2
            ],
            [
                r1,
                r2
            ]
        )

    return x

def hill_kinetics(k, lig, nh, K_a):
    return k * ((lig ** nh) / (K_a ** nh + lig ** nh))

def rapid_eq_2_2(s1, s2, p1, p2, k, q):
    return k * (s1 * s2 - (p1 * p2 / q))

def rapid_eq_3_3(s1, s2, s3, p1, p2, p3, k, q):
    return k * (s1 * s2 * s3 - (p1 * p2 * p3 / q))

def rapid_eq_1_1(s1, p1, k, q):
    return k * (s1 - p1 / q)

def rapid_eq_2_1(s1, s2, p1, k, q):
    return k * (s1 * s2 - (p1 / q))
