from __future__ import annotations

from typing import Literal

import numpy as np


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
    
def value(x: float) -> float:
    return x

def neg_value(x: float) -> float:
    return -1 * x

def times_neg_fourteen_thirds(x: float) -> float:
    return x * (-14/3)

def two_times_value(x: float) -> float:
    return 2 * x

def three_times_value(x: float) -> float:
    return 3 * x

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