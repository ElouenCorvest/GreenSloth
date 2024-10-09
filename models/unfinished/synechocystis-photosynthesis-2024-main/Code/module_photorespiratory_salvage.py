import parameters

# CHANGE LOG
# 013 20.02.2022 | created lumped reaction replacing yokota model (includes parameter kPR and reaction vPR)
# 017 06.03.2023 | switched parameters to import from parameters.py

# Define parameter
p_list = ["kPR"]
p = {k: v for k, v in parameters.p.items() if k in p_list}

# Add reaction: lumped 2PG recycling
def vPR(PG, ATP, NADPH, NAD, kPR):
    """
    Calculate the rate of PG recycling
    """
    return kPR * PG * ATP * NADPH * NAD


# Define the overarching function adding the general ETC construct to a modelbase model
def add_photorespiratory_salvage(m, init_param=None):
    """
    Adds the lumped reaction recycling (2-phospho)glycolate from photorespiration:
    The standard stoichiometry assumes complete recycling via glycolate dahydrogenase and the glycerate pathway (via tartronic semialdehyde):

    2 PG + (NADPH + Ho) + 2 NAD + ATP --> (3PGA + CO2) + NADP + (2 NADH + 2 Ho) + ADP (+ Pi)
    """

    # If initial parameters are given, apply them
    if init_param is not None:
        p.update({k: v for k, v in init_param.items() if k in p_list})

    # Add the parameter
    m.add_parameters(p)

    # Add reaction: lumped 2PG recycling
    m.add_reaction(
        rate_name="vPRsalv",
        function=vPR,
        stoichiometry={
            "PG": -2,
            "ATP": -1,
            "NADPH": -1,
            "Ho": 1 / m.get_parameter("bHo"),
            "NADH": 2,
            "3PGA": 1,
            "CO2": 1,
        },
        modifiers=["NAD"],
        dynamic_variables=["PG", "ATP", "NADPH", "NAD"],
        parameters=["kPR"],
        reversible=False,
    )

    return m
