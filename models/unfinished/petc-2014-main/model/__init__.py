from __future__ import annotations

from . import rates as r
from .rates import calculate_pHinv
from modelbase.ode import Model

__all__ = [
    "calculate_pHinv",
    "get_model",
]


def _add_derived_parameters(m: Model) -> Model:
    m.add_derived_parameter(
        parameter_name="RT",
        function=r.proportional,
        parameters=["R", "T"],
    )

    m.add_derived_parameter(
        parameter_name="dG_pH",
        function=r.dG_pH,
        parameters=["R", "T"],
    )

    m.add_derived_parameter(
        parameter_name="Hstroma",
        function=r.Hstroma,
        parameters=["pHstroma"],
    )

    m.add_derived_parameter(
        parameter_name="kProtonation",
        function=r.kProtonation,
        parameters=["Hstroma"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_PQred",
        function=r.keq_PQred,
        parameters=["E0_QA", "F", "E0_PQ", "pHstroma", "dG_pH", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_cyc",
        function=r.Keq_cyc,
        parameters=["E0_Fd", "F", "E0_PQ", "pHstroma", "dG_pH", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_FAFd",
        function=r.Keq_FAFd,
        parameters=["E0_FA", "F", "E0_Fd", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_PCP700",
        function=r.Keq_PCP700,
        parameters=["E0_PC", "F", "E0_P700", "RT"],
    )

    m.add_derived_parameter(
        parameter_name="Keq_FNR",
        function=r.Keq_FNR,
        parameters=["E0_Fd", "F", "E0_NADP", "pHstroma", "dG_pH", "RT"],
    )
    return m


def _add_algebraic_modules(m: Model) -> Model:
    m.add_algebraic_module_from_args(
        module_name="pq_alm",
        function=r.pqmoiety,
        derived_compounds=["PQred"],
        args=["PQ", "PQtot"],
    )

    m.add_algebraic_module_from_args(
        module_name="pc_alm",
        function=r.pcmoiety,
        derived_compounds=["PCred"],
        args=["PC", "PCtot"],
    )

    m.add_algebraic_module_from_args(
        module_name="fd_alm",
        function=r.fdmoiety,
        derived_compounds=["Fdred"],
        args=["Fd", "Fdtot"],
    )

    m.add_algebraic_module_from_args(
        module_name="adp_alm",
        function=r.adpmoiety,
        derived_compounds=["ADP"],
        args=["ATP", "APtot"],
    )

    m.add_algebraic_module_from_args(
        module_name="nadp_alm",
        function=r.nadpmoiety,
        derived_compounds=["NADP"],
        args=["NADPH", "NADPtot"],
    )

    m.add_algebraic_module_from_args(
        module_name="lhc_alm",
        function=r.lhcmoiety,
        derived_compounds=["LHCp"],
        args=["LHC"],
    )

    m.add_algebraic_module_from_args(
        module_name="ps2crosssection",
        function=r.ps2crosssection,
        derived_compounds=["ps2cs"],
        args=["LHC", "staticAntII", "staticAntI"],
    )

    m.add_algebraic_module_from_args(
        module_name="ps2states",
        function=r.ps2states,
        derived_compounds=["B0", "B1", "B2", "B3"],
        args=[
            "PQ",
            "PQred",
            "ps2cs",
            "PSIItot",
            "k2",
            "kF",
            "kH",
            "kH0",
            "Keq_PQred",
            "kPQred",
            "pfd",
        ],
    )

    m.add_algebraic_module_from_args(
        module_name="ps1states",
        function=r.ps1states,
        derived_compounds=["A1"],
        args=[
            "PC",
            "PCred",
            "Fd",
            "Fdred",
            "LHC",
            "ps2cs",
            "PSItot",
            "kFdred",
            "Keq_FAFd",
            "Keq_PCP700",
            "kPCox",
            "pfd",
        ],
    )

    m.add_algebraic_module_from_args(
        module_name="fluorescence",
        function=r.fluorescence,
        derived_compounds=["Fluo"],
        args=["B0", "B2", "ps2cs", "k2", "kF", "kH", "kH0"],
    )

    m.add_algebraic_module_from_args(
        module_name="calculate_pH",
        function=r.calculate_pH,
        derived_compounds=["pH"],
        args=["H"],
    )
    return m


def _add_reactions(m: Model) -> Model:
    # FIXME
    m.add_reaction_from_args(
        rate_name="vPS2",
        function=r.vPS2,
        stoichiometry={"PQ": -1, "H": 2 / m.get_parameter("bH")},
        args=["B1", "k2"],
    )

    m.add_reaction_from_args(
        rate_name="vPS1",
        function=r.vPS1,
        stoichiometry={"Fd": -1, "PC": 1},
        args=["A1", "ps2cs", "pfd"],
    )

    m.add_reaction_from_args(
        rate_name="vPTOX",
        function=r.vPTOX,
        stoichiometry={"PQ": 1},
        args=["PQred", "time", "kPTOX", "ox", "O2ext", "kNDH", "Ton", "Toff"],
    )

    m.add_reaction_from_args(
        rate_name="vNDH",
        function=r.vNDH,
        stoichiometry={"PQ": -1},
        args=["PQ", "time", "ox", "O2ext", "kNDH", "Ton", "Toff"],
    )

    m.add_reaction_from_args(
        rate_name="vB6f",
        function=r.vB6f,
        stoichiometry={"PC": -2, "PQ": 1, "H": 4 / 100},  # FIXME: bH?
        args=[
            "PC",
            "PQ",
            "H",
            "PQred",
            "PCred",
            "pH",
            "kCytb6f",
            "F",
            "E0_PQ",
            "E0_PC",
            "pHstroma",
            "RT",
            "dG_pH",
        ],
    )

    m.add_reaction_from_args(
        rate_name="vCyc",
        function=r.vCyc,
        stoichiometry={"PQ": -1, "Fd": 2},
        args=["PQ", "Fdred", "kcyc"],
    )

    m.add_reaction_from_args(
        rate_name="vFNR",
        function=r.vFNR,
        stoichiometry={"Fd": 2, "NADPH": 1},
        args=[
            "Fd",
            "Fdred",
            "NADPH",
            "NADP",
            "KM_FNR_F",
            "KM_FNR_N",
            "EFNR",
            "kcatFNR",
            "Keq_FNR",
        ],
    )

    # FIXME: use derived stoichiometry
    m.add_reaction_from_args(
        rate_name="vLeak",
        function=r.vLeak,
        stoichiometry={"H": -1 / m.get_parameter("bH")},
        args=["H", "kLeak", "pHstroma"],
    )

    m.add_reaction_from_args(
        rate_name="vSt12",
        function=r.vSt12,
        stoichiometry={"LHC": -1},
        args=["LHC", "PQ", "kStt7", "PQtot", "KM_ST", "n_ST"],
    )

    m.add_reaction_from_args(
        rate_name="vSt21",
        function=r.vSt21,
        stoichiometry={"LHC": 1},
        args=["LHCp", "kPph1"],
    )

    # FIXME: use derived stoichiometry
    m.add_reaction_from_args(
        rate_name="vATPsynthase",
        function=r.vATPsynthase,
        stoichiometry={"ATP": 1, "H": -m.get_parameter("HPR") / m.get_parameter("bH")},
        args=[
            "ATP",
            "ADP",
            "pH",
            "kATPsynth",
            "DeltaG0_ATP",
            "dG_pH",
            "HPR",
            "pHstroma",
            "Pi_mol",
            "RT",
        ],
    )

    m.add_reaction_from_args(
        rate_name="vATPconsumption",
        function=r.vATPconsumption,
        stoichiometry={"ATP": -1},
        args=["ATP", "kATPcons"],
    )

    m.add_reaction_from_args(
        rate_name="vNADPHconsumption",
        function=r.vNADPHconsumption,
        stoichiometry={"NADPH": -1},
        args=["NADPH", "kNADPHcons"],
    )
    return m


def get_model() -> Model:
    m = Model()
    m.add_compounds(
        [
            "PQ",  # oxidised plastoquinone
            "PC",  # oxidised plastocyan
            "Fd",  # oxidised ferrodoxin
            "ATP",  # stromal concentration of ATP
            "NADPH",  # stromal concentration of NADPH
            "H",  # lumenal protons
            "LHC",  # non-phosphorylated LHC
        ]
    )

    m.add_parameters(
        {
            "PSIItot": 2.5,  # [mmol/molChl] total concentration of PSII
            "PSItot": 2.5,
            "PQtot": 17.5,  # [mmol/molChl]
            "PCtot": 4.0,  # Bohme1987 but other sources give different values - seems to depend greatly on organism and conditions
            "Fdtot": 5.0,  # Bohme1987
            "Ctot": 2.5,  # source unclear (Schoettler says 0.4...?, but plausible to assume that complexes (PSII,PSI,b6f) have approx. same abundance)
            "NADPtot": 25.0,  # estimate from ~ 0.8 mM, Heineke1991
            "APtot": 60.0,  # [mmol/molChl] Bionumbers ~2.55mM (=81mmol/molChl) (FIXME: Soma had 50)
            # parameters associated with photosystem II
            "kH": 0.0,
            "kH0": 5e8,  # base quenching" after calculation with Giovanni
            "kF": 6.25e7,  # 6.25e7 fluorescence 16ns
            "k1": 5e9,  # excitation of Pheo / charge separation 200ps
            "k1rev": 1e10,
            "k2": 5e9,
            # parameters associated with photosystem I
            "kStt7": 0.0035,  # [s-1] fitted to the FM dynamics
            "kPph1": 0.0013,  # [s-1] fitted to the FM dynamics
            "KM_ST": 0.2,  # Switch point (half-activity of Stt7) for 20% PQ oxidised (80% reduced)
            "n_ST": 2.0,  # Hill coefficient of 4 -> 1/(2.5^4)~1/40 activity at PQox=PQred
            "staticAntI": 0.2,  # corresponds to PSI - LHCI supercomplex, when chlorophyll decreases more relative fixed antennae
            "staticAntII": 0.0,  # corresponds to PSII core
            # ATP and NADPH parameters
            "kATPsynth": 20.0,  # taken from MATLAB
            "kATPcons": 10.0,  # taken from MATLAB
            "ATPcyt": 0.5,  # only relative levels are relevant (normalised to 1) to set equilibrium
            "Pi_mol": 0.01,
            "DeltaG0_ATP": 30.6,  # 30.6kJ/mol / RT
            "HPR": 14.0 / 3.0,  # Vollmar et al. 2009 (after Zhu et al. 2013)
            "kNADPHcons": 15.0,  # taken from MATLAB
            "NADPHcyt": 0.5,  # only relatice levels
            # global conversion factor of PFD to excitation rate
            # "cPFD": 4. # [m^2/mmol PSII]
            # pH and protons
            "pHstroma": 7.8,
            "kLeak": 0.010,  # [1/s] leakage rate -- inconsistency with Kathrine
            "bH": 100.0,  # proton buffer: ratio total / free protons
            # rate constants
            "kPQred": 250.0,  # [1/(s*(mmol/molChl))]
            "kCytb6f": 2.5,  # a rough estimate: transfer PQ->cytf should be ~10ms
            "kPTOX": 0.01,  # ~ 5 electrons / seconds. This gives a bit more (~20)
            "kPCox": 2500.0,  # a rough estimate: half life of PC->P700 should be ~0.2ms
            "kFdred": 2.5e5,  # a rough estimate: half life of PC->P700 should be ~2micro-s
            "kcatFNR": 500.0,  # Carrillo2003 (kcat~500 1/s)
            "kcyc": 1.0,
            "O2ext": 8.0,  # corresponds to 250 microM cor to 20%
            "kNDH": 0.002,  # re-introduce e- into PQ pool. Only positive for anaerobic (reducing) condition
            "kNh": 0.05,
            "kNr": 0.004,
            "NPQsw": 5.8,
            "nH": 5.0,
            "EFNR": 3.0,  # Bohme1987
            "KM_FNR_F": 1.56,  # corresponds to 0.05 mM (Aliverti1990)
            "KM_FNR_N": 0.22,  # corresponds to 0.007 mM (Shin1971 Aliverti2004)
            # standard redox potentials (at pH=0) in V
            "E0_QA": -0.140,
            "E0_PQ": 0.354,
            "E0_cytf": 0.350,
            "E0_PC": 0.380,
            "E0_P700": 0.480,
            "E0_FA": -0.550,
            "E0_Fd": -0.430,
            "E0_NADP": -0.113,
            # physical constants
            "F": 96.485,  # Faraday constant
            "R": 8.3e-3,  # universal gas constant
            "T": 298.0,  # Temperature in K - for now assumed to be constant at 25 C
            # light
            "pfd": 100.0,
            "Ton": 500.0,
            "Toff": 1800,
            "dT": 120,
            "ox": True,
        }
    )

    m = _add_derived_parameters(m)
    m = _add_algebraic_modules(m)
    m = _add_reactions(m)

    return m
