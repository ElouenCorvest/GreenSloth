from mxlpy import Model, Derived, InitialAssignment
import mxlbricks.names as n
import numpy as np
from mxlbricks.fns import moiety_1, mul, neg, value, neg_div, div, twice

def _light_per_L(par: float):
    return 0.84 * par / 0.7


def _driving_force_Cl(Cl_stroma: float, Cl_lumen: float, Dy: float):
    return 0.06 * np.log10(Cl_stroma / Cl_lumen) + Dy


def calc_PsbS_Protonation(pH_lumen: float, pKPsbS: float):
    return 1 / (10 ** (3 * (pH_lumen - pKPsbS)) + 1)


def calc_NPQ(Z, PsbS_H, max_NPQ):
    return 0.4 * max_NPQ * PsbS_H * Z + 0.5 * max_NPQ * PsbS_H + 0.1 * max_NPQ * Z


def calc_phi2(NPQ, QA):
    return 1 / (1 + (1 + NPQ) / (4.88 * QA))


def calc_h(pH):
    return 10 ** (-1 * pH)


def calc_pmf(Dy, pH_lumen, pH_stroma):
    return Dy + 0.06 * (pH_stroma - pH_lumen)


def calc_kCBB(PAR):
    return 60 * (PAR / (PAR + 250))


def _v_PSII_recombination(Dy, QAm, pH_lumen, k_recomb):  # correct
    delta_delta_g_recomb = Dy + 0.06 * (7.0 - pH_lumen)
    return k_recomb * QAm * 10 ** (delta_delta_g_recomb / 0.06)


def _v_PSII_charge_separations(antenna_size, light_per_L, Phi2):  # correct
    return antenna_size * light_per_L * Phi2


def _v_b6f(
    pH_lumen,
    PQH2,
    PQ,
    PC_ox,
    PC_red,
    pKreg,
    b6f_content,
    Em7_PC,
    Em7_PQH2,
    pmf,
    max_b6f,
):  # correct
    pHmod = 1 - (1 / (10 ** (pH_lumen - pKreg) + 1))
    b6f_deprot = pHmod * b6f_content

    Em_PC = Em7_PC
    Em_PQH2 = Em7_PQH2 - 0.06 * (pH_lumen - 7.0)

    Keq_b6f = 10 ** ((Em_PC - Em_PQH2 - pmf) / 0.06)
    k_b6f = b6f_deprot * max_b6f

    k_b6f_reverse = k_b6f / Keq_b6f
    f_PQH2 = PQH2 / (
        PQH2 + PQ
    )  # want to keep the rates in terms of fraction of PQHs, not total number
    f_PQ = 1 - f_PQH2
    return f_PQH2 * PC_ox * k_b6f - f_PQ * PC_red * k_b6f_reverse


def _v_NDH(Fd_red, PQ, Fd_ox, PQH2, pH_stroma, Em7_PQH2, Em_Fd, k_NDH, pmf):
    Em_PQH2 = Em7_PQH2 - 0.06 * (pH_stroma - 7.0)
    deltaEm = Em_PQH2 - Em_Fd
    Keq_NDH = 10 ** ((deltaEm - pmf * 2) / 0.06)
    k_NDH_reverse = k_NDH / Keq_NDH
    return k_NDH * Fd_red * PQ - k_NDH_reverse * Fd_ox * PQH2


def _v_PGR(Fd_red, PQ, PQH2, PGR_vmax):
    return PGR_vmax * (Fd_red**4 / (Fd_red**4 + 0.1**4)) * PQ / (PQ + PQH2)


def _v_PSI_charge_separation(Fd_ox, P700_red, PSI_antenna_size, light_per_L):
    return P700_red * light_per_L * PSI_antenna_size * Fd_ox


def _v_PQ_reduction_QA(QAm, PQ, kQA):
    return QAm * PQ * kQA


def _v_PQH2_oxidation_QA(PQH2, QA, kQA, Keq_QA_PQ):
    return PQH2 * QA * kQA / Keq_QA_PQ


def _v_PC_oxidation_P700(PC_red, P700_ox, k_PC_to_P700):
    return PC_red * k_PC_to_P700 * P700_ox


def _v_LEF(Fd_red, NADP_pool, k_Fd_to_NADP):
    return k_Fd_to_NADP * NADP_pool * Fd_red


def _v_Mehler(Fd_red, Fd_ox):
    return 4 * 0.000265 * Fd_red / (Fd_red + Fd_ox)


def _v_CBB_NADPH(NADPH_pool, NADP_pool, t, k_CBC):
    # print(f"{NADPH_pool=}, {NADP_pool=}, {t=}, {k_CBC=}")
    return (
        k_CBC
        * (1.0 - np.exp(-t / 600))
        * (np.log(NADPH_pool / NADP_pool) - np.log(1.25))
        / (np.log(3.5 / 1.25))
    )


def _v_KEA(QAm, pH_lumen, K_lumen, H_lumen, H_stroma, K_stroma, k_KEA):
    qL = 1 - QAm
    qL_act = qL**3 / (qL**3 + 0.15**3)
    pH_act = 1 / (10 ** (1 * (pH_lumen - 6.0)) + 1)
    f_KEA_act = qL_act * pH_act
    return k_KEA * (H_lumen * K_stroma - H_stroma * K_lumen) * f_KEA_act


def _v_K_channel(K_lumen, Dy, K_stroma, perm_K):
    K_deltaG = -0.06 * np.log10(K_stroma / K_lumen) + Dy
    return perm_K * K_deltaG * (K_lumen + K_stroma) / 2


def _v_VCCN1(Cl_lumen, Cl_stroma, driving_force_Cl, k_VCCN1):
    relative_Cl_flux = (
        332 * (driving_force_Cl**3)
        + 30.8 * (driving_force_Cl**2)
        + 3.6 * driving_force_Cl
    )
    return k_VCCN1 * relative_Cl_flux * (Cl_stroma + Cl_lumen) / 2


def _v_CLCE(Cl_lumen, Cl_stroma, H_lumen, H_stroma, driving_force_Cl, pmf, k_CLCE):
    return (
        k_CLCE
        * (driving_force_Cl * 2 + pmf)
        * (Cl_stroma + Cl_lumen)
        * (H_lumen + H_stroma)
        / 4
    )


def _v_leak(H_lumen, pmf, k_leak):
    return pmf * k_leak * H_lumen


def _v_pmf_protons_activity(t, pmf, n, ATP_synthase_max_turnover, light_per_L):
    x = t / 165
    actvt = 0.2 + 0.8 * (x**4 / (x**4 + 1))
    v_proton_active = 1 - (
        1 / (10 ** ((pmf - 0.132) * 1.5 / 0.06) + 1)
    )  # reduced ATP synthase
    v_proton_inert = 1 - (
        1 / (10 ** ((pmf - 0.204) * 1.5 / 0.06) + 1)
    )  # oxidized ATP synthase

    v_active = actvt * v_proton_active * n * ATP_synthase_max_turnover
    v_inert = (1 - actvt) * v_proton_inert * n * ATP_synthase_max_turnover

    v_proton_ATP = v_active + v_inert

    if light_per_L > 0:
        return v_proton_ATP
    else:
        return 0


def _v_ZE(Z, kZE):
    return Z * kZE


def _v_VDE(V, pH_lumen, VDE_Hill, pKvde, VDE_max_turnover_number):
    pHmod = 1 / (10 ** (VDE_Hill * (pH_lumen - pKvde)) + 1)
    return V * VDE_max_turnover_number * pHmod


def neg_2_div(x: float, y: float):
    return -2 * x / y


def neg_point_one_val(x: float):
    return -0.1 * x


def neg_point_two_val(x: float):
    return -0.2 * x


def neg_thrice(x: float):
    return x * -3


def moeity(total, x):
    return total - x

def _delta_pH_inVolts(delta_pH: float):
    return 0.06 * delta_pH

def potassium(compartment: str) -> str:
    return f"K_{compartment}"

def chloride(compartment: str) -> str:
    return f"Cl_{compartment}"

def get_li2021(
    str_lumen = "_lumen",
    str_stroma = "_stroma"
) -> Model:
    """Implementation of the Li2021 model ()
    
    """
    model = Model()
    model.add_variables({
        "QA_red": 0,
        n.pq_red(): 0,
        n.ph(str_lumen): 7.8,
        "Dy": 0,
        potassium(str_lumen): 0.1,
        n.pc_ox(): 0,
        "P700_ox": 0,
        n.zx(): 0,
        "singletO2": 0,
        n.fd_red(): 0,
        n.nadph(): 1.5,
        chloride(str_lumen): 0.04,
        chloride(str_stroma): 0.04
    })
    model.add_parameters({
        n.pfd(): 50,
        "k_recomb": 0.33,
        "triplet_yield": 0.45,
        "triplet_to_singletO2_yield": 1,
        "PSII_antenna_size": 0.5,
        "b6f_content": 0.433,
        "pKreg": 6.2,
        "Em7_PC": 0.37,
        "Em7_PQH2": 0.11,
        "max_b6f": 300,
        "pKPsbS": 6.2,
        "max_NPQ": 3,
        "pH_stroma": 7.8,
        "Em_Fd": -0.42,
        "k_NDH": 1000,
        "PGR_vmax": 0,
        "PSI_antenna_size": 0.5,
        "kQA": 1000,
        "Keq_QA_PQ": 200,
        "k_PC_to_P700": 5000,
        "k_Fd_to_NADP": 1000,
        potassium(str_stroma): 0.1,
        "k_KEA": 2500000,
        "perm_K": 150,
        "lumen_protons_per_turnover": 0.000587,
        "k_VCCN1": 12,
        "k_CLCE": 800000,
        "n": 14/3,
        "ATP_synthase_max_turnover": 200,
        "buffering_capacity": 0.014,
        "Volts_per_charge": 0.047,
        "kZE": 0.004,
        "VDE_Hill": 4,
        "pKvde": 5.65,
        "VDE_max_turnover_number": 0.08,
        "k_leak": 3e7,
        # Moeity
        "QA_total": 1,
        n.total_pq(): 7,
        "P700_total": 0.667,
        n.total_pc(): 2,
        n.total_ferredoxin(): 1,
        n.total_nadp(): 5,
        n.total_carotenoids(): 1,
    #     "k_CBC": InitialAssignment(    
    #     fn=calc_kCBB,
    #     args=[n.pfd()]
    # )
    })
    
    # NEW
    model.add_derived(
        "k_CBC",
        fn=calc_kCBB,
        args=[n.pfd()]
    )
    
    # Derived
    model.add_derived(
        "QA",
        fn=moiety_1,
        args=["QA_red", "QA_total"]
    )
    model.add_derived(
        "P700_red",
        fn=moiety_1,
        args=["P700_ox", "P700_total"]
    )
    model.add_derived(
        n.pq_ox(),
        fn=moiety_1,
        args=[n.pq_red(), n.total_pq()]
    )
    model.add_derived(
        n.pc_red(),
        fn=moiety_1,
        args=[n.pc_ox(), n.total_pc()]
    )
    model.add_derived(
        n.fd_ox(),
        fn=moiety_1,
        args=[n.fd_red(), n.total_ferredoxin()]
    )
    model.add_derived(
        n.nadp(),
        fn=moiety_1,
        args=[n.nadph(), n.total_nadp()]
    )
    model.add_derived(
        n.vx(),
        fn=moiety_1,
        args=[n.zx(), n.total_carotenoids()]
    )
    model.add_derived(
        "light_per_L",
        fn=_light_per_L,
        args=[n.pfd()]
    )
    model.add_derived(
        "driving_force_Cl",
        fn=_driving_force_Cl,
        args=[chloride(str_stroma), chloride(str_lumen), "Dy"]
    )
    model.add_derived(
        n.psbs_pr(),
        fn=calc_PsbS_Protonation,
        args=[n.ph(str_lumen), "pKPsbS"]
    )
    model.add_derived(
        "NPQ",
        fn=calc_NPQ,
        args=[n.zx(), n.psbs_pr(), "max_NPQ"]
    )
    model.add_derived(
        "Phi2",
        fn=calc_phi2,
        args=["NPQ", "QA"]
    )
    model.add_derived(
        n.h(str_lumen),
        fn=calc_h,
        args=[n.ph(str_lumen)]
    )
    model.add_derived(
        n.h(str_stroma),
        fn=calc_h,
        args=[n.ph(str_stroma)]
    )
    model.add_derived(
        "pmf",
        fn=calc_pmf,
        args=["Dy", n.ph(str_lumen), n.ph(str_stroma)]
    )
    model.add_derived(
        "kCBB",
        fn=calc_kCBB,
        args=[n.pfd()]
    )
    model.add_derived(
        "delta_pH",
        fn=moiety_1,
        args=[n.ph(str_lumen), n.ph(str_stroma)]
    )
    model.add_derived(
        "delta_pH_inVolts",
        fn=_delta_pH_inVolts,
        args=["delta_pH"]
    )
    
    # Reactions
    model.add_reaction(
        "v_PSII_recombination",
        fn=_v_PSII_recombination,
        args=["Dy", "QA_red", n.ph(str_lumen), "k_recomb"],
        stoichiometry={
            "singletO2": Derived(fn=mul, args=["triplet_yield", "triplet_to_singletO2_yield"]),
            "QA_red": -1,
            n.ph(str_lumen): Derived(fn=div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=neg, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_PSII_charge_separations",
        fn=_v_PSII_charge_separations,
        args=["PSII_antenna_size", "light_per_L", "Phi2"],
        stoichiometry={
            "QA_red": 1,
            n.ph(str_lumen): Derived(fn=neg_div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=value, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_PQ_reduction_QA",
        fn=_v_PQ_reduction_QA,
        args=["QA_red", n.pq_ox(), "kQA"],
        stoichiometry={
            "QA_red": -1,
            n.pq_red(): 0.5,
        }
    )
    model.add_reaction(
        "v_PQH2_oxidation_QA",
        fn=_v_PQH2_oxidation_QA,
        args=[n.pq_red(), "QA", "kQA", "Keq_QA_PQ"],
        stoichiometry={
            "QA_red": 1,
            n.pq_red(): -0.5,
        }
    )
    model.add_reaction(
        "v_b6f",
        fn=_v_b6f,
        args=[n.ph(str_lumen), n.pq_red(), n.pq_ox(), n.pc_ox(), n.pc_red(), "pKreg", "b6f_content", "Em7_PC", "Em7_PQH2", "pmf", "max_b6f"],
        stoichiometry={
            n.pq_red(): -0.5,
            n.pc_ox(): -1,
            n.ph(str_lumen): Derived(fn=neg_2_div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=value, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_NDH",
        fn=_v_NDH,
        args=[n.fd_red(), n.pq_ox(), n.fd_ox(), n.pq_red(), n.ph(str_stroma), "Em7_PQH2", "Em_Fd", "k_NDH", "pmf"],
        stoichiometry={
            n.pq_red(): 0.5,
            n.fd_red(): -1,
            n.ph(str_lumen): Derived(fn=neg_2_div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=twice, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_PGR",
        fn=_v_PGR,
        args=[n.fd_red(), n.pq_ox(), n.pq_red(), "PGR_vmax"],
        stoichiometry={
            n.pq_red(): 0.5,
            n.fd_red(): -1,
        }
    )
    model.add_reaction(
        "v_PSI_charge_separation",
        fn=_v_PSI_charge_separation,
        args=[n.fd_ox(), "P700_red", "PSI_antenna_size", "light_per_L"],
        stoichiometry={
            "P700_ox": 1,
            n.fd_red(): 1,
            "Dy": Derived(fn=value, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_PC_oxidation_P700",
        fn=_v_PC_oxidation_P700,
        args=[n.pc_red(), "P700_ox", "k_PC_to_P700"],
        stoichiometry={
            "P700_ox": -1,
            n.pc_ox(): 1
        }
    )
    model.add_reaction(
        "v_LEF",
        fn=_v_LEF,
        args=[n.fd_red(), n.nadp(), "k_Fd_to_NADP"],
        stoichiometry={
            n.fd_red(): -1,
            n.nadph(): 0.5
        }
    )
    model.add_reaction(
        "v_Mehler",
        fn=_v_Mehler,
        args=[n.fd_red(), n.fd_ox()],
        stoichiometry={
            n.fd_red(): -1,
        }
    )
    model.add_reaction(
        "v_CBB_NADPH",
        fn=_v_CBB_NADPH,
        args=[n.nadph(), n.nadp(), "time", "k_CBC"],
        stoichiometry={
            n.nadph(): -1,
        }
    )
    model.add_reaction(
        "v_KEA",
        fn=_v_KEA,
        args=["QA_red", n.ph(str_lumen), potassium(str_lumen), n.h(str_lumen), n.h(str_stroma), potassium(str_stroma), "k_KEA"],
        stoichiometry={
            potassium(str_lumen): Derived(fn=value, args=["lumen_protons_per_turnover"]),
            n.ph(str_lumen): Derived(fn=div, args=["lumen_protons_per_turnover", "buffering_capacity"])
        }
    )
    model.add_reaction(
        "v_K_channel",
        fn=_v_K_channel,
        args=[potassium(str_lumen), "Dy", potassium(str_stroma), "perm_K"],
        stoichiometry={
            potassium(str_lumen): Derived(fn=neg, args=["lumen_protons_per_turnover"]),
            "Dy": Derived(fn=neg, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_VCCN1",
        fn=_v_VCCN1,
        args=[chloride(str_lumen), chloride(str_stroma), "driving_force_Cl", "k_VCCN1"],
        stoichiometry={
            chloride(str_lumen): Derived(fn=value, args=["lumen_protons_per_turnover"]),
            chloride(str_stroma): Derived(fn=neg_point_one_val, args=["lumen_protons_per_turnover"]),
            "Dy": Derived(fn=neg, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_CLCE",
        fn=_v_CLCE,
        args=[chloride(str_lumen), chloride(str_stroma), n.h(str_lumen), n.h(str_stroma), "driving_force_Cl", "pmf", "k_CLCE"],
        stoichiometry={
            chloride(str_lumen): Derived(fn=twice, args=["lumen_protons_per_turnover"]),
            chloride(str_stroma): Derived(fn=neg_point_two_val, args=["lumen_protons_per_turnover"]),
            n.ph(str_lumen): Derived(fn=div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=neg_thrice, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_leak",
        fn=_v_leak,
        args=[n.h(str_lumen), "pmf", "k_leak"],
        stoichiometry={
            n.ph(str_lumen): Derived(fn=div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=neg, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_pmf_protons_activity",
        fn=_v_pmf_protons_activity,
        args=["time", "pmf", "n", "ATP_synthase_max_turnover", "light_per_L"],
        stoichiometry={
            n.ph(str_lumen): Derived(fn=div, args=["lumen_protons_per_turnover", "buffering_capacity"]),
            "Dy": Derived(fn=neg, args=["Volts_per_charge"])
        }
    )
    model.add_reaction(
        "v_ZE",
        fn=_v_ZE,
        args=[n.zx(), "kZE"],
        stoichiometry={
            n.zx(): -1
        }
    )
    model.add_reaction(
        n.violaxanthin_deepoxidase(),
        fn=_v_VDE,
        args=[n.vx(), n.ph(str_lumen), "VDE_Hill", "pKvde", "VDE_max_turnover_number"],
        stoichiometry={
            n.zx(): 1
        }
    )
    return model