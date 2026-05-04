
from mxlpy import Model
    
from .basic_funcs import (
    moiety_1,
)

def calc_PsbS_Protonation(pH_lumen: float, pKa_PsbS: float):
    return 1-(1 - (1 / (10 ** ((pH_lumen - pKa_PsbS)) + 1))) # checked

def calc_NPQ(Z, PsbS_H, NPQ_max):
    return NPQ_max * PsbS_H * Z # checked

def calc_phi2(NPQ, QA):
    return 1 / (1 + (1 + NPQ) / (4.88 * QA)) # checked

def DeltaGATP_to_volt(DeltaGATP):
    return 0.06*DeltaGATP/5.7

def ATPsynthase_driving_force(pmf, DeltaGATP, n):
    return pmf - (DeltaGATP/n)

def calc_h(pH):
    return 10 ** (-1 * pH) # checked

def calc_pmf(Dpsi, pH_lumen, pH_stroma, pmf_init):
    return Dpsi + 0.06 * (pH_stroma - pH_lumen) + pmf_init # checked


def _delta_pH_inVolts(delta_pH: float):
    return 0.06 * delta_pH

def include_derived_quantities(m: Model):


    m.add_derived(
        name="QA",
        fn=moiety_1,
        args=['QA_red', 'QA_total'],
    )

    m.add_derived(
        name="P700_red",
        fn=moiety_1,
        args=['P700_ox', 'P700_total'],
    )

    m.add_derived(
        name="PQ",
        fn=moiety_1,
        args=['PQH_2', 'PQ_tot'],
    )

    m.add_derived(
        name="PC_red",
        fn=moiety_1,
        args=['PC_ox', 'PC_tot'],
    )

    m.add_derived(
        name="Fd_ox",
        fn=moiety_1,
        args=['Fd_red', 'Fd_tot'],
    )

    m.add_derived(
        name="NADP_st",
        fn=moiety_1,
        args=['NADPH_st', 'NADP_tot'],
    )

    m.add_derived(
        name="Vx",
        fn=moiety_1,
        args=['Zx', 'Xanthophyll_tot'],
    )

    m.add_derived(
        name="DeltaGATP_V",
        fn=DeltaGATP_to_volt,
        args=['DeltaGATP'],
    )

    m.add_derived(
        name="PsbSP",
        fn=calc_PsbS_Protonation,
        args=['pH_lumen', 'pKa_PsbS'],
    )

    m.add_derived(
        name="NPQ",
        fn=calc_NPQ,
        args=['Zx', 'PsbSP', 'NPQ_max'],
    )

    m.add_derived(
        name="PhiPSII",
        fn=calc_phi2,
        args=['NPQ', 'QA'],
    )

    m.add_derived(
        name="H_lumen",
        fn=calc_h,
        args=['pH_lumen'],
    )

    m.add_derived(
        name="H_stroma",
        fn=calc_h,
        args=['pH_stroma'],
    )

    m.add_derived(
        name="pmf",
        fn=calc_pmf,
        args=['Dpsi', 'pH_lumen', 'pH_stroma', 'pmf_init'],
    )

    m.add_derived(
        name="delta_pH",
        fn=moiety_1,
        args=['pH_lumen', 'pH_stroma'],
    )

    m.add_derived(
        name="delta_pH_inVolts",
        fn=_delta_pH_inVolts,
        args=['delta_pH'],
    )

    m.add_derived(
        name='ATP_synthase_driving_force',
        fn=ATPsynthase_driving_force,
        args=['pmf', 'DeltaGATP_V', 'n'],
    )

    return m