from modelbase2 import Model, Derived
import numpy as np
from .basic_funcs import proportional, two_divided_value, four_divided_value, value, neg_one_divided_value, neg_value1_divided_value2, hill_kinetics, rapid_eq_2_2, rapid_eq_3_3, rapid_eq_1_1, rapid_eq_2_1

def v_PSII(B1, k2):
    return 0.5 * B1 * k2

def v_PSI(psIIcross, pfd, Y0):
    return (1 - psIIcross) * pfd * Y0

def _oxygen(time, ox, O2_ext, k_NDH, Ton, Toff):
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if ox:
        """by default we assume constant oxygen supply"""
        return O2_ext, k_NDH
    else:
        if time < Ton or time > Toff:
            return O2_ext, 0
        else:
            return 0, k_NDH

def oxygen(time, ox, O2_ext, k_NDH, Ton, Toff):
    """return oxygen and NDH concentration as a function of time
    used to simulate anoxia conditions as in the paper"""
    if isinstance(time, (int, float)):
        return np.array(_oxygen(time, ox, O2_ext, k_NDH, Ton, Toff))
    else:

        return np.array([_oxygen(time, ox, O2_ext, k_NDH, Ton, Toff) for time, ox, O2_ext, k_NDH, Ton, Toff in zip(time, ox, O2_ext, k_NDH, Ton, Toff)]).T

def v_PQ(PQH_2, time, k_PTOX, ox, O2_ext, k_NDH, Ton, Toff):
    """calculates reaction rate of PTOX"""
    return PQH_2 * k_PTOX * oxygen(time, ox, O2_ext, k_NDH, Ton, Toff)[0]

def v_NDH(PQ, time, ox, O2_ext, k_NDH, Ton, Toff):
    """
    calculates reaction rate of PQ reduction under absence of oxygen
    can be mediated by NADH reductase NDH
    """
    return  PQ * oxygen(time, ox, O2_ext, k_NDH, Ton, Toff)[1]

def v_b6f(PC_ox, PQ, PQH_2, PC_red, K_cytb6f, k_Cytb6f):
    """calculates reaction rate of cytb6f"""
    return np.maximum(k_Cytb6f * (PQH_2 * PC_ox ** 2 - (PQ * PC_red ** 2) / K_cytb6f), -k_Cytb6f)

def v_Cyc(PQ, Fd_red, k_cyc):
    """
    calculates reaction rate of cyclic electron flow
    considered as practically irreversible
    """
    return k_cyc * ((Fd_red ** 2) * PQ)

def v_FNR(Fd_ox, Fd_red, NADPH_st, NADP_st, KM_FNR_F, KM_FNR_N, EFNR, kcat_FNR, K_FNR, convf):
    """
    Reaction rate mediated by the Ferredoxin—NADP(+) reductase (FNR)
    Kinetic: convenience kinetics Liebermeister and Klipp, 2006
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [F], [Fdred] in mmol/mol Chl/s
    [NADPH] in mM
    """
    fdred = Fd_red / KM_FNR_F
    fdox = Fd_ox / KM_FNR_F
    nadph = NADPH_st / (convf * KM_FNR_N)   # NADPH requires conversion to mmol/mol of chlorophyll
    nadp = NADP_st / (convf * KM_FNR_N)  # NADP requires conversion to mmol/mol of chlorophyll
    return (
        EFNR
        * kcat_FNR
        * ((fdred ** 2) * nadp - ((fdox ** 2) * nadph) / K_FNR)
        / ((1 + fdred + fdred ** 2) * (1 + nadp) + (1 + fdox + fdox ** 2) * (1 + nadph) - 1)
    )

def calculate_pHinv(x):
    return 4e3 * 10 ** (-x)

def v_Leak(H_lu, k_Leak, pH_stroma):
    """
    rate of leak of protons through the membrane
    """
    return k_Leak * (H_lu - calculate_pHinv(pH_stroma))

def v_St21(LHC, PQ, k_Stt7, PQ_tot, KM_ST, n_ST):
    """
    reaction rate of state transitions from PSII to PSI
    Ant depending on module used corresponds to non-phosphorylated antennae
    or antennae associated with PSII
    """
    kKin = k_Stt7 * (1 / (1 + (PQ / (PQ_tot * KM_ST) ) ** n_ST))
    return kKin * LHC

def v_ATPsynth(ATP_st, ADP_st, K_ATPsynth, k_ATPsynth, convf):
    """
    Reaction rate of ATP production
    Kinetic: simple mass action with PH dependant equilibrium
    Compartment: lumenal side of the thylakoid membrane
    Units:
    Reaction rate: mmol/mol Chl/s
    [ATP], [ADP] in mM
    """
    return k_ATPsynth * (ADP_st / convf - ATP_st / (convf * K_ATPsynth))

def v_Deepox(Vx, H_lu, nh_x, k_DV, K_pHSat):
    """
    activity of xantophyll cycle: de-epoxidation of violaxanthin, modelled by Hill kinetics
    """
    return hill_kinetics(k_DV, H_lu, nh_x, calculate_pHinv(K_pHSat)) * Vx

def v_PsbSP(psbS, H_lu, nh_PsbS, k_prot, K_pHSatLHC):
    """
    activity of PsbS protein protonation: protonation modelled by Hill kinetics
    """
    return hill_kinetics(k_prot, H_lu, nh_PsbS, calculate_pHinv(K_pHSatLHC)) * psbS

def v_RuBisCO(RUBP, PGA, FBP, SBP, Pi_st, NADPH_st, Vmax_rubisco, CO2, Km_RuBisCO_RUBP, Ki_RuBisCO_PGA, Ki_RuBisCO_FBP, Ki_RuBisCO_SBP, Ki_RuBisCO_Pi, Ki_RuBisCO_NADPH, Km_RuBisCO_CO2):
    return (Vmax_rubisco * RUBP * CO2) / (
        (RUBP + Km_RuBisCO_RUBP * (1 + (PGA / Ki_RuBisCO_PGA) + (FBP / Ki_RuBisCO_FBP) + (SBP / Ki_RuBisCO_SBP) + (Pi_st / Ki_RuBisCO_Pi) + (NADPH_st / Ki_RuBisCO_NADPH)))
        * (CO2 + Km_RuBisCO_CO2)
    )

def v_FBPase(FBP, F6P, Pi_st, Vmax_fbpase, Km_FBPase, Ki_FBPase_F6P, Ki_FBPase_Pi):
    return (Vmax_fbpase * FBP) / (FBP + Km_FBPase * (1 + (F6P / Ki_FBPase_F6P) + (Pi_st / Ki_FBPase_Pi)))

def v_SBPase(SBP, Pi_st, Vmax_sbpase, Km_SBPase, Ki_SBPase_Pi):
    return (Vmax_sbpase * SBP) / (SBP + Km_SBPase * (1 + (Pi_st / Ki_SBPase_Pi)))

def v_PRKase(RU5P, ATP_st, RUBP, PGA, Pi_st, ADP_st, Vmax_prkase, Km_PRKase_RU5P, Ki_PRKase_PGA, Ki_PRKase_RuBP, Ki_PRKase_Pi, Kiunc_PRKase_ADP, Km_PRKase_ATP, Kicom_PRKase_ADP):
    return (Vmax_prkase * RU5P * ATP_st) / (
        (RU5P + Km_PRKase_RU5P * (1 + (PGA / Ki_PRKase_PGA) + (RUBP / Ki_PRKase_RuBP) + (Pi_st / Ki_PRKase_Pi)))
        * (ATP_st * (1 + (ADP_st / Kiunc_PRKase_ADP)) + Km_PRKase_ATP * (1 + (ADP_st / Kicom_PRKase_ADP)))
    )

def triose_export(S, IF_3P, Vmax_ex, K_diss_PGA):
    return (Vmax_ex * S) / (IF_3P * K_diss_PGA)

def v_starch(G1P, ATP_st, ADP_st, Pi_st, PGA, F6P, FBP, Vmax_starch, Km_Starch_G1P, Ki_Starch_ADP, Km_Starch_ATP, Kact_Starch_PGA, Kact_Starch_F6P, Kact_Starch_FBP):
    """G1P -> Gn-1 ; Starch production"""
    return (Vmax_starch * G1P * ATP_st) / (
        (G1P + Km_Starch_G1P)
        * ((1 + (ADP_st / Ki_Starch_ADP)) * (ATP_st + Km_Starch_ATP) + ((Km_Starch_ATP * Pi_st) / (Kact_Starch_PGA * PGA + Kact_Starch_F6P * F6P + Kact_Starch_FBP * FBP)))
    )

def v_Fdred(Fd_ox, Fd_red, Y1, Y2, k_Fdred, K_FAFd):
    """rate of the redcution of Fd by the activity of PSI
    used to be equall to the rate of PSI but now
    alternative electron pathway from Fd allows for the production of ROS
    hence this rate has to be separate
    """
    return k_Fdred * Fd_ox * Y1 - k_Fdred / K_FAFd * Fd_red * Y2

def v_APXase(ASC, H2O2, k_f1, k_r1, k_f2, k_r2, k_f3, k_f4, k_r4, k_f5, XT):
    """lumped reaction of ascorbate peroxidase
    the cycle stretched to a linear chain with
    two steps producing the MDA
    two steps releasing ASC
    and one step producing hydrogen peroxide"""
    nom = ASC * H2O2 * XT
    denom = (
        ASC * H2O2 * (1 / k_f3 + 1 / k_f5)
        + ASC / k_f1
        + H2O2 / k_f4
        + H2O2 * k_r4 / (k_f4 * k_f5)
        + H2O2 / k_f2
        + H2O2 * k_r2 / (k_f2 * k_f3)
        + k_r1 / (k_f1 * k_f2)
        + k_r1 * k_r2 / (k_f1 * k_f2 * k_f3)
    )
    return nom / denom

def v_MDAreduct(NADPH_st, MDA, kcat_MDAR, Km_MDAR_NADPH, Km_MDAR_MDA, MDAR_0):
    """Compare Valero et al. 2016"""
    nom = kcat_MDAR * MDAR_0 * NADPH_st * MDA
    denom = Km_MDAR_NADPH * MDA + Km_MDAR_MDA * NADPH_st + NADPH_st * MDA + Km_MDAR_NADPH * Km_MDAR_MDA
    return nom / denom

def v_GR(NADPH_st, GSSG, kcat_GR, GR_0, Km_NADPH, Km_GSSG):
    nom = kcat_GR * GR_0 * NADPH_st * GSSG
    denom = Km_NADPH * GSSG + Km_GSSG * NADPH_st + NADPH_st * GSSG + Km_NADPH * Km_GSSG
    return nom / denom

def v_DHAR(DHA, GSH, kcat_DHAR, DHAR_0, Km_DHA, K_DHAR, Km_GSH):
    nom = kcat_DHAR * DHAR_0 * DHA * GSH
    denom = K_DHAR + Km_DHA * GSH + Km_GSH * DHA + DHA * GSH
    return nom / denom

def v_3ASC(MDA, k3):
    return k3 * MDA ** 2

def include_rates(
    m: Model
):

    # ------------------------------------
    # Matuszynska Module
    # ------------------------------------

    m.add_reaction(
        name='v_PSII',
        fn=v_PSII,
        args=['B1', 'k2'],
        stoichiometry={"PQ": -1, "H_lu": Derived(two_divided_value, ['b_H'])}
    )

    m.add_reaction(
        name='v_PQ',
        fn=v_PQ,
        args=['PQH_2', 'time', 'k_PTOX', 'ox', 'O2_ext', 'k_NDH', 'Ton', 'Toff'],
        stoichiometry={"PQ": 1}
    )

    m.add_reaction(
        name='v_NDH',
        fn=v_NDH,
        args=['PQ', 'time', 'ox', 'O2_ext', 'k_NDH', 'Ton', 'Toff'],
        stoichiometry={"PQ": -1}
    )

    m.add_reaction(
        name='v_b6f',
        fn=v_b6f,
        args=['PC_ox', 'PQ', 'PQH_2', 'PC_red', 'K_cytb6f', 'k_Cytb6f'],
        stoichiometry={"PC_ox": -2, "PQ": 1, "H_lu": Derived(four_divided_value, ['b_H'])},
    )

    m.add_reaction(
        name='v_Cyc',
        fn=v_Cyc,
        args=['PQ', 'Fd_red', 'k_cyc'],
        stoichiometry={"PQ": -1, "Fd_ox": 2},
    )

    m.add_reaction(
        name='v_FNR',
        fn=v_FNR,
        args=['Fd_ox', 'Fd_red', 'NADPH_st', 'NADP_st', 'KM_FNR_F', 'KM_FNR_N', 'EFNR', 'kcat_FNR', 'K_FNR', 'convf'],
        stoichiometry={"Fd_ox": 2, "NADPH_st": Derived(value, ['convf'])},
    )

    m.add_reaction(
        name='v_Leak',
        fn=v_Leak,
        args=['H_lu', 'k_Leak', 'pH_stroma'],
        stoichiometry={"H_lu": Derived(neg_one_divided_value, ['b_H'])},
    )

    m.add_reaction(
        name='v_St21',
        fn=v_St21,
        args=['LHC', 'PQ', 'k_Stt7', 'PQ_tot', 'KM_ST', 'n_ST'],
        stoichiometry={"LHC": -1},
    )

    m.add_reaction(
        name='v_St12',
        fn=proportional,
        args=['LHCp', 'k_Pph1'],
        stoichiometry={"LHC": 1},
    )

    m.add_reaction(
        name='v_ATPsynth',
        fn=v_ATPsynth,
        args=['ATP_st', 'ADP_st', 'K_ATPsynth', 'k_ATPsynth', 'convf'],
        stoichiometry={
            "H_lu": Derived(neg_value1_divided_value2, ['HPR', 'b_H']),
            "ATP_st": Derived(value, ['convf']),
        },
    )

    m.add_reaction(
        name="v_Deepox",
        fn=v_Deepox,
        args=['Vx', 'H_lu', 'nh_x', 'k_DV', 'K_pHSat'],
        stoichiometry={"Vx": -1}
    )

    m.add_reaction(
        name="v_Epox",
        fn=proportional,
        args=['Zx', 'k_EZ'],
        stoichiometry={"Vx": 1},
    )

    m.add_reaction(
        name="v_PsbSP",
        fn=v_PsbSP,
        args=['psbS', 'H_lu', 'nh_PsbS', 'k_prot', 'K_pHSatLHC'],
        stoichiometry={"psbS": -1},
    )

    m.add_reaction(
        name="v_PsbSD",
        fn=proportional,
        args=['k_deprot', 'PsbSP'],
        stoichiometry={"psbS": 1},
    )

    m.add_reaction(
        name="v_PGK1ase",
        fn=rapid_eq_2_2,
        args=['ATP_st', 'PGA', 'BPGA', 'ADP_st', 'k_fast', 'K_PGK1ase'],
        stoichiometry={"ATP_st": -1, "PGA": -1, "BPGA": 1},
    )

    m.add_reaction(
        name="v_BPGAdehynase",
        fn=rapid_eq_3_3,
        args=["BPGA", "NADPH_st", "H_st", "GAP", "NADP_st", "Pi_st", "k_fast", "K_BPGAdehynase"],
        stoichiometry={"BPGA": -1, "NADPH_st": -1, "GAP": 1},
    )

    m.add_reaction(
        name="v_TPIase",
        fn=rapid_eq_1_1,
        args=['GAP', 'DHAP', 'k_fast', 'K_TPIase'],
        stoichiometry={"GAP": -1, "DHAP": 1}
    )

    m.add_reaction(
        name="v_Aldolase_FBP",
        fn=rapid_eq_2_1,
        args=['GAP', 'DHAP', 'FBP', 'k_fast', 'K_Aldolase_FBP'],
        stoichiometry={"GAP": -1, "DHAP": -1, "FBP": 1},
    )

    m.add_reaction(
        name="v_TKase_E4P",
        fn=rapid_eq_2_2,
        args=['GAP', 'F6P', 'X5P', 'E4P', 'k_fast', 'K_TKase_E4P'],
        stoichiometry={"GAP": -1, "F6P": -1, "X5P": 1, "E4P": 1},
    )

    m.add_reaction(
        name="v_Aldolase_SBP",
        fn=rapid_eq_2_1,
        args=['DHAP', 'E4P', 'SBP', 'k_fast', 'K_Aldolase_SBP'],
        stoichiometry={"DHAP": -1, "E4P": -1, "SBP": 1},
    )

    m.add_reaction(
        name="v_TKase_R5P",
        fn=rapid_eq_2_2,
        args=['GAP', 'S7P', 'X5P', 'R5P', 'k_fast', 'K_TKase_R5P'],
        stoichiometry={"GAP": -1, "S7P": -1, "X5P": 1, "R5P": 1},
    )

    m.add_reaction(
        name="v_Rpiase",
        fn=rapid_eq_1_1,
        args=['R5P', 'RU5P', 'k_fast', 'K_Rpiase'],
        stoichiometry={"R5P": -1, "RU5P": 1},
    )

    m.add_reaction(
        name="v_RPEase",
        fn=rapid_eq_1_1,
        args=['X5P', 'RU5P', 'k_fast', 'K_RPEase'],
        stoichiometry={"X5P": -1, "RU5P": 1},
    )

    m.add_reaction(
        name="v_PGIase",
        fn=rapid_eq_1_1,
        args=['F6P', 'G6P', 'k_fast', 'K_PGIase'],
        stoichiometry={"F6P": -1, "G6P": 1},
    )

    m.add_reaction(
        name="v_PGMase",
        fn=rapid_eq_1_1,
        args=['G6P', 'G1P', 'k_fast', 'K_PGMase'],
        stoichiometry={"G6P": -1, "G1P": 1},
    )

    m.add_reaction(
        name="v_pga_ex",
        fn=triose_export,
        args=['PGA', 'IF_3P', 'Vmax_ex', 'K_diss_PGA'],
        stoichiometry={"PGA": -1},
    )

    m.add_reaction(
        name="v_gap_ex",
        fn=triose_export,
        args=['GAP', 'IF_3P', 'Vmax_ex', 'K_diss_GAP'],
        stoichiometry={"GAP": -1},
    )

    m.add_reaction(
        name="v_dhap_ex",
        fn=triose_export,
        args=['DHAP', 'IF_3P', 'Vmax_ex', 'K_diss_DHAP'],
        stoichiometry={"DHAP": -1},
    )

    # ------------------------------------
    # Thioredoxin Module
    # ------------------------------------

    m.add_reaction(
        name="v_RuBisCO",
        fn=v_RuBisCO,
        args=['RUBP', 'PGA', 'FBP', 'SBP', 'Pi_st', 'NADPH_st', 'Vmax_rubisco', 'CO2', 'Km_RuBisCO_RUBP', 'Ki_RuBisCO_PGA', 'Ki_RuBisCO_FBP', 'Ki_RuBisCO_SBP', 'Ki_RuBisCO_Pi', 'Ki_RuBisCO_NADPH', 'Km_RuBisCO_CO2'],
        stoichiometry={"RUBP": -1, "PGA": 2},
    )

    m.add_reaction(
        name="v_FBPase",
        fn=v_FBPase,
        args=['FBP', 'F6P', 'Pi_st', 'Vmax_fbpase', 'Km_FBPase', 'Ki_FBPase_F6P', 'Ki_FBPase_Pi'],
        stoichiometry={"FBP": -1, "F6P": 1},
    )

    m.add_reaction(
        name="v_SBPase",
        fn=v_SBPase,
        args=['SBP', 'Pi_st', 'Vmax_sbpase', 'Km_SBPase', 'Ki_SBPase_Pi'],
        stoichiometry={"SBP": -1, "S7P": 1},
    )

    m.add_reaction(
        name="v_PRKase",
        fn=v_PRKase,
        args=['RU5P', 'ATP_st', 'RUBP', 'PGA', 'Pi_st', 'ADP_st', 'Vmax_prkase', 'Km_PRKase_RU5P', 'Ki_PRKase_PGA', 'Ki_PRKase_RuBP', 'Ki_PRKase_Pi', 'Kiunc_PRKase_ADP', 'Km_PRKase_ATP', 'Kicom_PRKase_ADP'],
        stoichiometry={"RU5P": -1, "ATP_st": -1, "RUBP": 1},
    )

    m.add_reaction(
        name="v_starch",
        fn=v_starch,
        args=['G1P', 'ATP_st', 'ADP_st', 'Pi_st', 'PGA', 'F6P', 'FBP', 'Vmax_starch', 'Km_Starch_G1P', 'Ki_Starch_ADP', 'Km_Starch_ATP', 'Kact_Starch_PGA', 'Kact_Starch_F6P', 'Kact_Starch_FBP'],
        stoichiometry={"G1P": -1, "ATP_st": -1},
    )

    m.add_reaction(
        name="v_FdTrReduc",
        fn=proportional,
        args=['TRX_ox', 'Fd_red', 'k_fd_tr_reductase'],
        stoichiometry={"TRX_ox": -1, "Fd_ox": 1},
    )

    m.add_reaction(
        name="v_Eact",
        fn=proportional,
        args=['E_CBB_inactive', 'TRX_red', 'k_e_cbb_activation'],
        stoichiometry={"E_CBB_inactive": -5, "TRX_ox": 5},
    )

    m.add_reaction(
        name="v_Einact",
        fn=proportional,
        args=['E_CBB_active', 'k_e_cbb_relaxation'],
        stoichiometry={"E_CBB_inactive": 5},
    )

    # ------------------------------------
    # Mehler Module
    # ------------------------------------

    m.add_reaction(
        name='v_PSI',
        fn=v_PSI,
        args=['psIIcross', 'pfd', 'Y0'],
        stoichiometry={"PC_ox": 1}
    )

    m.add_reaction(
        name="v_Fdred",
        fn=v_Fdred,
        args=['Fd_ox', 'Fd_red', 'Y1', 'Y2', 'k_Fdred', 'K_FAFd'],
        stoichiometry={"Fd_ox": -1}
    )

    m.add_reaction(
        name="v_APXase",
        fn=v_APXase,
        args=['ASC', 'H2O2', 'k_f1', 'k_r1', 'k_f2', 'k_r2', 'k_f3', 'k_f4', 'k_r4', 'k_f5', 'XT'],
        stoichiometry={"H2O2": -1, "MDA": 2},
    )

    m.add_reaction(
        name="v_MDAreduct",
        fn=v_MDAreduct,
        args=['NADPH_st', 'MDA', 'kcat_MDAR', 'Km_MDAR_NADPH', 'Km_MDAR_MDA', 'MDAR_0'],
        stoichiometry={"NADPH_st": -1, "MDA": -2},
    )

    m.add_reaction(
        name="v_Mehler",
        fn=proportional,
        args=['Y1', 'O2_ext', 'k_Mehler'],
        stoichiometry={"H2O2": Derived(value, ['convf'])},  # required to convert as rates of PSI are expressed in mmol/mol Chl
    )

    m.add_reaction(
        name="v_GR",
        fn=v_GR,
        args=['NADPH_st', 'GSSG', 'kcat_GR', 'GR_0', 'Km_NADPH', 'Km_GSSG'],
        stoichiometry={"NADPH_st": -1, "GSSG": -1},
    )

    m.add_reaction(
        name="v_DHAR",
        fn=v_DHAR,
        args=['DHA', 'GSH', 'kcat_DHAR', 'DHAR_0', 'Km_DHA', 'K_DHAR', 'Km_GSH'],
        stoichiometry={"DHA": -1, "GSSG": 1},
    )

    m.add_reaction(
        name="v_3ASC",
        fn=v_3ASC,
        args=['MDA', 'k3'],
        stoichiometry={"MDA": -2, "DHA": 1},
    )

    # ------------------------------------
    # Consumption Module
    # ------------------------------------

    m.add_reaction(
        name="v_ATPcons",
        fn=proportional,
        args=['ATP_st', 'k_ex_atp'],
        stoichiometry={"ATP_st": -1},
    )

    m.add_reaction(
        name="v_NADPHcons",
        fn=proportional,
        args=['NADPH_st', 'k_ex_nadph'],
        stoichiometry={"NADPH_st": -1},
    )

    return m
