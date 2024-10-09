from __future__ import annotations

import numpy as np


def value(x: float) -> float:
    return x


def neg(x: float) -> float:
    return -x


def proportional(x: float, y: float) -> float:
    return x * y


def times_two(x: float) -> float:
    return x * 2


def times_minus_fourteen_thirds(x: float) -> float:
    return -x * 14 / 3


def k1(PFD: float, cPFD: float) -> float:
    return cPFD * PFD


def Keq(H: float, DG0: float, Hst: float, RT: float, Pi: float) -> float:
    DG = DG0 - np.log(10) * (pH(Hst) - pH(H)) * (14 / 3) * RT
    return Pi * np.exp(-DG / RT)  # type: ignore


def v1(N: float, A1: float, PFD: float, cPFD: float) -> float:
    return (1 - N) * k1(PFD, cPFD) * A1


def v2(A2: float, k2: float) -> float:
    return k2 * A2


def v3(
    A1: float, A2: float, P: float, D: float, X: float, k3p: float, k3m: float
) -> float:  # P seems to be reduce and Q oxidized ?
    A3 = D - A1 - A2
    Q = X - P
    return k3p * A3 * Q - k3m * A1 * P


def v4(P: float, k4: float) -> float:
    return k4 * P


def v5(
    T: float, H: float, A: float, k5: float, DG0: float, Hst: float, RT: float, Pi: float
) -> float:
    return k5 * (A - T * (1 + 1 / Keq(H, DG0, Hst, RT, Pi)))


def v6(N: float, H: float, k6: float, n: float, KQ: float) -> float:
    return k6 * (1 - N) * ((H**n) / (H**n + KQ**n))  # type: ignore


def v7(N: float, k7: float) -> float:
    return k7 * N


def v8(H: float, Hst: float, k8: float) -> float:
    return k8 * (H - Hst)


def v9(T: float, k9: float) -> float:
    return k9 * T


def pH(H: float) -> float:
    return -np.log10(H * 2.5e-4)  # type: ignore
