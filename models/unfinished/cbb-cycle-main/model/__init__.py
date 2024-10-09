from .modules import ADP, N, P_i
from .rates import (
    rapid_equilibrium_1_1,
    rapid_equilibrium_2_1,
    rapid_equilibrium_2_2,
    v1,
    v3,
    v6,
    v9,
    v13,
    v16,
    v_out,
    vStarchProduction,
)
from modelbase.ode import Model

parameters = {
    "Vmax_1": 2.72,  # [mM/s], Pettersson 1988
    "Vmax_6": 1.6,  # [mM/s], Pettersson 1988
    "Vmax_9": 0.32,  # [mM/s], Pettersson 1988
    "Vmax_13": 8.0,  # [mM/s], Pettersson 1988
    "Vmax_16": 2.8,  # [mM/s], Pettersson 1988
    "Vmax_starch": 0.32,  # [mM/s], Pettersson 1988
    "Vmax_efflux": 2.0,  # [mM/s], Pettersson 1988
    "Km_1": 0.02,  # [mM], Pettersson 1988
    "Km_6": 0.03,  # [mM], Pettersson 1988
    "Km_9": 0.013,  # [mM], Pettersson 1988
    "Km_13_1": 0.05,  # [mM], Pettersson 1988
    "Km_13_2": 0.05,  # [mM], Pettersson 1988
    "Km_16_1": 0.014,  # [mM], Pettersson 1988
    "Km_16_2": 0.3,  # [mM], Pettersson 1988
    "Km_starch_1": 0.08,  # [mM], Pettersson 1988
    "Km_starch_2": 0.08,  # [mM], Pettersson 1988
    "K_pga": 0.25,  # [mM], Pettersson 1988
    "K_gap": 0.075,  # [mM], Pettersson 1988
    "K_dhap": 0.077,  # [mM], Pettersson 1988
    "K_pi": 0.63,  # [mM], Pettersson 1988
    "K_pxt": 0.74,  # [mM], Pettersson 1988
    "Ki_1_1": 0.04,  # [mM], Pettersson 1988
    "Ki_1_2": 0.04,  # [mM], Pettersson 1988
    "Ki_1_3": 0.075,  # [mM], Pettersson 1988
    "Ki_1_4": 0.9,  # [mM], Pettersson 1988
    "Ki_1_5": 0.07,  # [mM], Pettersson 1988
    "Ki_6_1": 0.7,  # [mM], Pettersson 1988
    "Ki_6_2": 12.0,  # [mM], Pettersson 1988
    "Ki_9": 12.0,  # [mM], Pettersson 1988
    "Ki_13_1": 2.0,  # [mM], Pettersson 1988
    "Ki_13_2": 0.7,  # [mM], Pettersson 1988
    "Ki_13_3": 4.0,  # [mM], Pettersson 1988
    "Ki_13_4": 2.5,  # [mM], Pettersson 1988
    "Ki_13_5": 0.4,  # [mM], Pettersson 1988
    "Ki_starch": 10.0,  # [mM], Pettersson 1988
    "Ka_starch_1": 0.1,  # [mM], Pettersson 1988
    "Ka_starch_2": 0.02,  # [mM], Pettersson 1988
    "Ka_starch_3": 0.02,  # [mM], Pettersson 1988
    "k_rapid_eq": 800000000.0,  # Rapid Equilibrium speed
    "q2": 0.00031,  # [], Pettersson 1988
    "q3": 16000000.0,  # [], Pettersson 1988
    "q4": 22.0,  # [], Pettersson 1988
    "q5": 7.1,  # [1/mM]], Pettersson 1988
    "q7": 0.084,  # [], Pettersson 1988
    "q8": 13.0,  # [1/mM]], Pettersson 1988
    "q10": 0.85,  # [], Pettersson 1988
    "q11": 0.4,  # [], Pettersson 1988
    "q12": 0.67,  # [], Pettersson 1988
    "q14": 2.3,  # [], Pettersson 1988
    "q15": 0.058,  # [], Pettersson 1988
    "CO2": 0.2,  # [mM], Pettersson 1988
    "Phosphate_total": 15.0,  # [mM], Pettersson 1988
    "AP_total": 0.5,  # [mM], Pettersson 1988
    "N_total": 0.5,  # [mM], Pettersson 1988
    "Phosphate_pool_ext": 0.5,  # [mM], Pettersson 1988
    "pH_medium": 7.6,  # [], Pettersson 1988
    "pH_stroma": 7.9,  # [], Pettersson 1988
    "proton_pool_stroma": 1.2589254117941661e-05,  # [mM], Pettersson 1988
    "NADPH_pool": 0.21,  # [mM], Pettersson 1988
    "NADP_pool": 0.29,  # [mM], Pettersson 1988
}


def get_model() -> Model:
    model = Model(parameters=parameters)
    model.add_compounds(
        [
            "PGA",
            "BPGA",
            "GAP",
            "DHAP",
            "FBP",
            "F6P",
            "G6P",
            "G1P",
            "SBP",
            "S7P",
            "E4P",
            "X5P",
            "R5P",
            "RUBP",
            "RU5P",
            "ATP",
        ]
    )

    model.add_algebraic_module(
        module_name="ADP_mod",
        function=ADP,
        compounds=["ATP"],
        derived_compounds=["ADP"],
        parameters=["AP_total"],
    )

    model.add_algebraic_module(
        module_name="Pi_mod",
        function=P_i,
        compounds=[
            "PGA",
            "BPGA",
            "GAP",
            "DHAP",
            "FBP",
            "F6P",
            "G6P",
            "G1P",
            "SBP",
            "S7P",
            "E4P",
            "X5P",
            "R5P",
            "RUBP",
            "RU5P",
            "ATP",
        ],
        derived_compounds=["Phosphate_pool"],
        parameters=["Phosphate_total"],
    )

    model.add_algebraic_module(
        module_name="N_mod",
        function=N,
        compounds=["Phosphate_pool", "PGA", "GAP", "DHAP"],
        derived_compounds=["N_pool"],
        parameters=[
            "K_pxt",
            "Phosphate_pool_ext",
            "K_pi",
            "K_pga",
            "K_gap",
            "K_dhap",
        ],
    )

    model.add_reaction(
        rate_name="v1",
        function=v1,
        stoichiometry={"RUBP": -1, "PGA": 2},
        modifiers=["PGA", "FBP", "SBP", "Phosphate_pool"],
        parameters=[
            "Vmax_1",
            "Km_1",
            "Ki_1_1",
            "Ki_1_2",
            "Ki_1_3",
            "Ki_1_4",
            "Ki_1_5",
            "NADPH_pool",
        ],
    )
    model.add_reaction(
        rate_name="v2",
        function=rapid_equilibrium_2_2,
        stoichiometry={"PGA": -1, "ATP": -1, "BPGA": 1},
        modifiers=["ADP"],
        parameters=["k_rapid_eq", "q2"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v3",
        function=v3,
        stoichiometry={"BPGA": -1, "GAP": 1},
        modifiers=["Phosphate_pool"],
        parameters=[
            "proton_pool_stroma",
            "NADPH_pool",
            "NADP_pool",
            "k_rapid_eq",
            "q3",
        ],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v4",
        function=rapid_equilibrium_1_1,
        stoichiometry={"GAP": -1, "DHAP": 1},
        parameters=["k_rapid_eq", "q4"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v5",
        function=rapid_equilibrium_2_1,
        stoichiometry={"GAP": -1, "DHAP": -1, "FBP": 1},
        parameters=["k_rapid_eq", "q5"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v6",
        function=v6,
        stoichiometry={"FBP": -1, "F6P": 1},
        modifiers=["F6P", "Phosphate_pool"],
        parameters=["Vmax_6", "Km_6", "Ki_6_1", "Ki_6_2"],
    )
    model.add_reaction(
        rate_name="v7",
        function=rapid_equilibrium_2_2,
        stoichiometry={"GAP": -1, "F6P": -1, "E4P": 1, "X5P": 1},
        parameters=["k_rapid_eq", "q7"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v8",
        function=rapid_equilibrium_2_1,
        stoichiometry={"DHAP": -1, "E4P": -1, "SBP": 1},
        parameters=["k_rapid_eq", "q8"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v9",
        function=v9,
        stoichiometry={"SBP": -1, "S7P": 1},
        modifiers=["Phosphate_pool"],
        parameters=["Vmax_9", "Km_9", "Ki_9"],
    )
    model.add_reaction(
        rate_name="v10",
        function=rapid_equilibrium_2_2,
        stoichiometry={"GAP": -1, "S7P": -1, "X5P": 1, "R5P": 1},
        parameters=["k_rapid_eq", "q10"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v11",
        function=rapid_equilibrium_1_1,
        stoichiometry={"R5P": -1, "RU5P": 1},
        parameters=["k_rapid_eq", "q11"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v12",
        function=rapid_equilibrium_1_1,
        stoichiometry={"X5P": -1, "RU5P": 1},
        parameters=["k_rapid_eq", "q12"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v13",
        function=v13,
        stoichiometry={"RU5P": -1, "ATP": -1, "RUBP": 1},
        modifiers=["Phosphate_pool", "PGA", "RUBP", "ADP"],
        parameters=[
            "Vmax_13",
            "Km_13_1",
            "Km_13_2",
            "Ki_13_1",
            "Ki_13_2",
            "Ki_13_3",
            "Ki_13_4",
            "Ki_13_5",
        ],
    )
    model.add_reaction(
        rate_name="v14",
        function=rapid_equilibrium_1_1,
        stoichiometry={"F6P": -1, "G6P": 1},
        parameters=["k_rapid_eq", "q14"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v15",
        function=rapid_equilibrium_1_1,
        stoichiometry={"G6P": -1, "G1P": 1},
        parameters=["k_rapid_eq", "q15"],
        reversible=True,
    )
    model.add_reaction(
        rate_name="v16",
        function=v16,
        stoichiometry={"ATP": 1},
        modifiers=["ADP", "Phosphate_pool"],
        parameters=["Vmax_16", "Km_16_1", "Km_16_2"],
    )
    model.add_reaction(
        rate_name="vPGA_out",
        function=v_out,
        stoichiometry={"PGA": -1},
        modifiers=["N_pool"],
        parameters=["Vmax_efflux", "K_pga"],
    )
    model.add_reaction(
        rate_name="vGAP_out",
        function=v_out,
        stoichiometry={"GAP": -1},
        modifiers=["N_pool"],
        parameters=["Vmax_efflux", "K_gap"],
    )
    model.add_reaction(
        rate_name="vDHAP_out",
        function=v_out,
        stoichiometry={"DHAP": -1},
        modifiers=["N_pool"],
        parameters=["Vmax_efflux", "K_dhap"],
    )
    model.add_reaction(
        rate_name="vSt",
        function=vStarchProduction,
        stoichiometry={"G1P": -1, "ATP": -1},
        modifiers=["ADP", "Phosphate_pool", "PGA", "F6P", "FBP"],
        parameters=[
            "Vmax_starch",
            "Km_starch_1",
            "Km_starch_2",
            "Ki_starch",
            "Ka_starch_1",
            "Ka_starch_2",
            "Ka_starch_3",
        ],
    )
    return model
