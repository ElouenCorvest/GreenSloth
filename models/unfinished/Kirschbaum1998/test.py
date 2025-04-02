import matplotlib
import numpy as np

def nrh(
    theta,
    Vmax,
    alpha,
    Vmin,
    I
):
    if theta == 0:
        v = Vmax * ((alpha * I *(1 - Vmin))/(alpha * I + 1 - Vmin) + Vmin)
    else:
        top = alpha * I + Vmax - np.sqrt((alpha * I + Vmax)**2 - 4 * alpha * I * Vmax * theta)
        bottom = 2 * theta
        v = top/bottom

    return v

x = nrh(
    0.866,
    Vmax=71.5,
    alpha=0.0088,
    Vmin=13.6,
    I=100
)

print(x)
