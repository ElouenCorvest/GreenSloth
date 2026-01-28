def rapid_equilibrium_1s_1p(
    s1: float,
    p1: float,
    k_re: float,
    q: float,
) -> float:
    return k_re * (s1 - p1 / q)


def michaelis_menten_1s_1i(
    s: float,
    i: float,
    vmax: float,
    km: float,
    ki: float,
) -> float:
    return vmax * s / (s + km * (1 + i / ki))


def moiety_2(x1: float, x2: float, total: float) -> float:
    return total - x1 - x2


def protons_stroma(ph: float) -> float:
    return 4000.0 * 10 ** (-ph)


def rapid_equilibrium_2s_1p(
    s1: float,
    s2: float,
    p1: float,
    k_re: float,
    q: float,
) -> float:
    return k_re * (s1 * s2 - p1 / q)


def mass_action_1s(s1: float, k_fwd: float) -> float:
    return k_fwd * s1


def michaelis_menten_1s_2i(
    s: float,
    i1: float,
    i2: float,
    vmax: float,
    km: float,
    ki1: float,
    ki2: float,
) -> float:
    return vmax * s / (s + km * (1 + i1 / ki1 + i2 / ki2))


def neg_div(x: float, y: float) -> float:
    return -x / y


def value(x: float) -> float:
    return x


def rapid_equilibrium_2s_2p(
    s1: float,
    s2: float,
    p1: float,
    p2: float,
    k_re: float,
    q: float,
) -> float:
    return k_re * (s1 * s2 - p1 * p2 / q)


def mass_action_2s(s1: float, s2: float, k_fwd: float) -> float:
    return k_fwd * s1 * s2


def mul(x: float, y: float) -> float:
    """Calculate the product of two values.

    Parameters
    ----------
    x
        First factor
    y
        Second factor

    Returns
    -------
    Float
        Product of x and y (x * y)

    Examples
    --------
    >>> mul(2.0, 3.0)
    6.0
    >>> mul(0.5, 4.0)
    2.0

    """
    return x * y


def moiety_1(concentration: float, total: float) -> float:
    return total - concentration


def div(x: float, y: float) -> float:
    return x / y


def rapid_equilibrium_3s_3p(
    s1: float,
    s2: float,
    s3: float,
    p1: float,
    p2: float,
    p3: float,
    k_re: float,
    q: float,
) -> float:
    return k_re * (s1 * s2 * s3 - p1 * p2 * p3 / q)
