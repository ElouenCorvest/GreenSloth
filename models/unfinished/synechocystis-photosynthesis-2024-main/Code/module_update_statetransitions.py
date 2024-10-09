from modelbase.ode import ratefunctions as rf
import parameters

# CHANGE LOG
# 017 28.02.2023 | moved state transition hill update to module_update_statetransitions
#     06.03.2023 | switched parameters to import from parameters.py


def vPSIIunquench(PSIIq, Q_red, kUnquench, KMUnquench):
    nUnquench=1
    return kUnquench * PSIIq * (1 - rf.hill(Q_red, 1, KMUnquench, nUnquench))


def update_statetransitions_hill(m, y0, init_param=None, verbose=True):
    if verbose:
        print("updating state transitions to hill")

    m.remove_parameters(["kQuench", "kUnquench"])

    p_list = [
        "kUnquench",
        "KMUnquench",
        # "nUnquench",
        "kQuench",
        # "const",
    ]
    p = {k: v for k, v in parameters.pu.items() if k in p_list}

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    m.add_parameters(p)

    m.add_reaction_from_args(
        rate_name="vPSIIunquench",
        function=vPSIIunquench,
        stoichiometry={"PSII": 1},
        args=["PSIIq", "Q_red", "kUnquench", "KMUnquench"],
    )

    m.update_reaction_from_args(
        rate_name="vPSIIquench",
        function=rf.mass_action_2,
        stoichiometry={"PSII": -1},
        args=["PSII", "Q_red", "kQuench"],
    )

    return m, y0
