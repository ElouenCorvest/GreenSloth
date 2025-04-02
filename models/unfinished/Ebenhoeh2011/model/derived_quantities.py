import numpy as np
from modelbase2 import Model

from . import basic_funcs as bf


def N0_func(N: float) -> float:
    return 1 - N

def pH(H: float) -> float:
    return -np.log10(H * 2.5e-4)  # type: ignore

def rev_pH(pH: float) -> float:
    return (10 ** -pH) / 2.5e-4
    
def Keq_func(H_lu: float, DG0: float, H_st: float, RT: float, Pi: float) -> float:
    DG = DG0 - np.log(10) * (pH(H_st) - pH(H_lu)) * (14 / 3) * RT
    return Pi * np.exp(-DG / RT)  # type: ignore

def include_derived_quantities(m: Model) -> Model:
    m.add_derived(
        'RT',
        fn=bf.proportional,
        args=["R", "Temp"]
    )
    
    m.add_derived(
        'k1',
        fn=bf.proportional,
        args=["cPFD", "PFD"]
    )
    
    m.add_derived(
        'N0',
        fn=N0_func,
        args=['N'],
    )
    
    m.add_derived(
        'A3',
        fn=bf.continous_subtraction,
        args=['D', 'A1', 'A2'],
    )
    
    m.add_derived(
        'PQ_red',
        fn=bf.continous_subtraction,
        args=['PQ_tot', 'PQ_ox'],
    )
    
    m.add_derived(
        'ADP_st',
        fn=bf.continous_subtraction,
        args=['AP_tot', 'ATP_st'],
    )
    
    m.add_derived(
        'Keq',
        fn=Keq_func,
        args=['H_lu', 'DG0', 'H_st', 'RT', 'Pi'],
    )
    
    return m