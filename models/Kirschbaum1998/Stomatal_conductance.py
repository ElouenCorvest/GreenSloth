from modelbase2 import Model, Simulator, make_protocol
import numpy as np
from typing import Literal
import matplotlib.pyplot as plt
from labellines import labelLines

def rate_func(
    A: float,
    B: float,
    tau: float
):
    return (A - B) / tau

def v1(
    Seq,
    S,
    tau_i,
    tau_d
):
    return (
        np.select(
            [Seq > S],
            [
                rate_func(Seq, S, tau_i)
            ],
            rate_func(Seq, S, tau_d)
        )
    )

def proportional(*args) -> float:
    if len(args) <= 1:
        raise ValueError("Not enough arguments given")
    else:
        v = args[0]
        for i in args[1:]:
            v *= i
        return v

def quadratic_min(
    a: float,
    b: float,
    c: float,
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

def quad_b_func(
    Smin,
    alpha,
    I
):
    return -(1 + Smin + alpha * I)

def quad_c_func(
    Smin,
    alpha,
    I
):
    return Smin + alpha * I

def get_model():
    return (
        Model()
        .add_parameters({
            'tau_i': 0.37, #Time constant for an increase in value of S [min]
            'tau_d': 7, #Time constant for a decrease in value of S [min]
            'tau_pi': 13, #Time constant for change in value of pi [min]
            'tau_w': 15, #Time constant for change in water content [min]
            'alpha': 0.0088, #Slope of Svar at zero I [m2 s (µmol quanta)-1]
            'Smin': 0.192, #Extrapolated minimum value of Seq in darkness []
            'theta': 0.866, #Measure of the curvature []
            'gs_high': 71.5, #Maximum leaf conductance [mmol m-2 s-1]
            'I': 10, #Irradiance [µmol quanta m-2 s-1]
        })
        .add_variables({
            'S': 0.1, #Initial biochemical signal in the guard cells
            'pi': 0.1, #Guard cell osmotic potential
            'w': 0.1, #Guard cell water content
        })
        .add_derived(
            'gs',
            fn=proportional,
            args=['w', 'gs_high']
        )
        .add_derived(
            'quad_b',
            fn=quad_b_func,
            args=['Smin', 'alpha', 'I']
        )
        .add_derived(
            'quad_c',
            fn=quad_c_func,
            args=['Smin', 'alpha', 'I']
        )
        .add_derived(
            'Seq',
            fn=quadratic_min,
            args=['theta', 'quad_b', 'quad_c']
        )
        .add_reaction(
            "v1",
            fn=v1,
            args=['Seq', 'S', 'tau_i', 'tau_d'],
            stoichiometry={'S': 1}
        )
        .add_reaction(
            "v2",
            fn=rate_func,
            args=['S', 'pi', 'tau_pi'],
            stoichiometry={'pi': 1}
        )
        .add_reaction(
            "v3",
            fn=rate_func,
            args=['pi', 'w', 'tau_w'],
            stoichiometry={'w': 1}
        )
    )

def figure_4():

    fig, ax = plt.subplots()

    light_fleck = 5

    protocol = make_protocol(
        [
            (light_fleck, {'I': 500}),
            (90 - light_fleck, {'I': 10})
        ]
    )

    concs, fluxes = (
        Simulator(get_model())
        .simulate_over_protocol(protocol, time_points_per_step=100)
        .get_full_concs_and_fluxes()
    )

    ax.plot(concs.index, concs['gs'])
    ax.set_xlim(-15, 90)
    ax.set_ylim(0, 50)
    ax.set_xlabel('Time [minutes]')
    ax.set_ylabel('gs [mmol m-2 s-1]')



def figure_6():

    fig, axs = plt.subplots(1, 2, sharey=True)

    light_fleck = 5

    protocol = make_protocol(
        [
            (light_fleck, {'I': 500}),
            (90 - light_fleck, {'I': 10})
        ]
    )

    concs, fluxes = (
        Simulator(get_model())
        .simulate_over_protocol(protocol, time_points_per_step=100)
        .get_full_concs_and_fluxes()
    )

    for comp in concs.columns:
        axs[0].plot(concs.index, concs[comp], label = comp)

    axs[0].annotate("", xy=(0, 1.1), xytext=(0, 1),
            arrowprops=dict(arrowstyle="->"))

    axs[0].annotate("", xy=(0, 1.1), xytext=(0, 1), arrowprops=dict(arrowstyle="->"))
    axs[0].annotate("", xy=(light_fleck, 1), xytext=(light_fleck, 1.1), arrowprops=dict(arrowstyle="->"))

    light_fleck = 15/60

    protocol = make_protocol(
        [
            (light_fleck, {'I': 500}),
            (90 - light_fleck, {'I': 10})
        ]
    )

    concs, fluxes = (
        Simulator(get_model())
        .simulate_over_protocol(protocol, time_points_per_step=100)
        .get_full_concs_and_fluxes()
    )

    for comp in concs.columns:
        axs[1].plot(concs.index, concs[comp], label = comp)

    for ax in axs:
        ax.set_xlim(-15, 90)
        ax.set_xticks([0, 30, 60, 90])
        ax.set_xticks([15, 45, 75], minor = True)
        ax.set_xlabel('Time [minutes]')
        labelLines(ax.get_lines(), zorder=2.5)

    axs[1].annotate("", xy=(0, 1.1), xytext=(0, 1), arrowprops=dict(arrowstyle="->"))
    axs[1].annotate("", xy=(light_fleck, 1), xytext=(light_fleck, 1.1), arrowprops=dict(arrowstyle="->"))

    axs[0].set_ylim(0.0, 1.2)
    axs[0].set_ylabel('Relative Response')

figure_4()

plt.show()
