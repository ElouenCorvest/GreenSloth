#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qE model presented in Matuszynska et al. 2016 and in the
doctoral thesis "Mathematicla model of light acclimation mechanisms
in higher plants and green algae" Matuszynska 2016
"""

import numpy as np
from modelbase.ode import Model, Simulator

#with git submodule COMMENT WHEN RUNNING PYTHON FILE
from .parameters import pars
from .misc import pH, pHinv

#Without git submodule UNCOMMENT WHEN RUNNING PYTHON FILE
# from parameters import pars
# from misc import pH, pHinv


#%%

# define the basic model
M16model = Model(pars)

# add compounds
M16model.add_compounds([
    "P", # reduced Plastoquinone
    "H", # luminal Protons
    "E", # ATPactivity
    "A", # ATP
    "Pr", # fraction of non-protonated PsbS
    "V" # fraction of Violaxanthin
    ])


##############################################################################
# Derived Parameters
##############################################################################


# add derived parameters
M16model.add_derived_parameter(
    parameter_name="RT", function=lambda r, t: r * t, parameters=["R", "T"])

def _KeqQAPQ(F, E0QAQAm, E0PQPQH2, pHstroma, RT):
    DG1 =  -F*E0QAQAm
    DG2 = -2*F*E0PQPQH2 + 2*pHstroma * np.log(10) * RT
    DG0 = -2*DG1 + DG2
    Keq = np.exp(-DG0/RT)
    return Keq

M16model.add_derived_parameter(
    parameter_name = "KeqQAPQ", function=_KeqQAPQ, parameters=["F", "E0QAQAm", "E0PQPQH2", "pHstroma", "RT"])


##############################################################################
# Auxiliary functions
##############################################################################

def PSII(P, Q, light, PQtot, kPQred, KeqQAPQ, kH, kF, kP, PSIItot):

    Bs = []
    #light = np.ones(len(P)) * light
    Pox = PQtot - P
    b0 = (light + kPQred*P/KeqQAPQ)
    b1 = (kH * Q + kF)
    b2 = kH * Q + kF + kP

    for Pox,b0,b1,b2 in zip(Pox,b0,b1,b2):
        A = np.array([
        [-b0,        b1,         kPQred*Pox,                0], #B0
        [light,     -b2,         0,                         0], #B1
        [0,          0,          light,                   -b1], #B3
        [1,          1,          1,                         1]
        ])

        b = np.array([0,0,0,PSIItot])
        B0,B1,B2,B3 = np.linalg.solve(A,b)
        Bs.append([B0, B1, B2, B3])
    return np.array(Bs).T


def Keqcytb6f(H, F, E0PQPQH2, RT, E0PCPCm, pHstroma):
     DG1 = -2*F*E0PQPQH2 + 2 * RT * np.log(10) * pH(H)
     DG2 = -F*E0PCPCm
     DG3 = RT*np.log(10)*(pHstroma - pH(H))
     DG = -DG1 + 2*DG2 + 2*DG3
     Keq = np.exp(-DG/RT)
     return Keq


def KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi):
    DG = DG0ATP - np.log(10) * (pHstroma-pH(H)) * (14/3)  * RT
    Keq = Pi * np.exp(-DG/RT)
    return Keq



###############################################################################
# Conserved quantities
###############################################################################

def pqmoiety(P, PQtot):
    return [PQtot - P]

def atpmoiety(A, APtot):
    return [APtot - APtot]

def psbsmoiety(Pr, PsbStot):
    return [Pr - PsbStot]

def xcycmoiety(V, Xtot):
    return [Xtot - V]

###############################################################################
# RATE EQUATIONS
###############################################################################

def vPSII(B1, light, PQtot, kPQred, KeqQAPQ, kH, kF, kP, PSIItot):
    v = kP * 0.5 * B1
    return v



def vPQox(P, H, light, kCytb6f, kPTOX, O2ex, PQtot, F, E0PQPQH2, RT, E0PCPCm, pHstroma):
    kPFD = kCytb6f * light
    kPTOX = kPTOX * O2ex
    Keq = Keqcytb6f(H, F, E0PQPQH2, RT, E0PCPCm, pHstroma)
    a1 = kPFD * Keq/ (Keq + 1)
    a2 = kPFD/(Keq + 1)
    v = (a1 + kPTOX) * P - a2 * (PQtot - P)
    return v


def vATPsynthase(A, H, E, kATPsynthase, DG0ATP, pHstroma, RT, Pi, APtot):
    v = E * kATPsynthase * (APtot - A - A/KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi))
    return v


def vATPactivity(E, light,  kActATPase,  kDeactATPase):
    switch = light > 0
    v = kActATPase * switch * (1 - E) - kDeactATPase * (1-switch) * E
    return v


def vLeak(H, kleak, pHstroma):
    v = kleak * (H - pHinv(pHstroma))
    return v


def vATPcons(A, kATPconsumption):
    v = kATPconsumption * A
    return v


def vXcyc(V, H, nHX, KphSatZ, kDeepoxV, kEpoxZ, Xtot):
    a = H**nHX / (H**nHX + pHinv(KphSatZ)**nHX)
    v = kDeepoxV * a * V - kEpoxZ * (Xtot - V)
    return v


def vPsbSP(Pr, H, nHL, KphSatLHC, kProt, kDeprot, PsbStot):
    a = H**nHL / (H**nHL + pHinv(KphSatLHC)**nHL)
    v = kProt * a * Pr - kDeprot * (PsbStot - Pr)
    return v


def Quencher(Pr, V, Xtot, PsbStot, Kzsat, gamma0, gamma1, gamma2, gamma3):
    Z = Xtot - V
    P = PsbStot - Pr
    Zs = Z/(Z +  Kzsat)

    Q = gamma0 * (1-Zs) * Pr \
    + gamma1 * (1-Zs) * P \
    + gamma2 * Zs * P \
    + gamma3 * Zs * Pr
    return Q


def Fluorescence(P, Q, B0, B2, light, PQtot, kPQred, KeqQAPQ, kH, kF, kP, PSIItot):
    Fluo =  kF/(kH*Q+kF+kP) * B0 + kF/(kH*Q+kF) * B2
    return Fluo

#%%

##############################################################################
# Add algebraic modules
#############################################################################

M16model.add_algebraic_module(
    module_name = "P_am",
    function = pqmoiety,
    compounds = ["P"],
    derived_compounds = ["Pox"],
    parameters = ["PQtot"])


M16model.add_algebraic_module(
    module_name = "A_am",
    function = atpmoiety,
    compounds = ["A"],
    derived_compounds = ["ADP"],
    parameters = ["APtot"])


M16model.add_algebraic_module(
    module_name = "PsbS_am",
    function = psbsmoiety,
    compounds = ["Pr"],
    derived_compounds = ["Pnr"],
    parameters = ["PsbStot"])


M16model.add_algebraic_module(
    module_name = "X_am",
    function = xcycmoiety,
    compounds = ["V"],
    derived_compounds = ["Z"],
    parameters = ["Xtot"])


M16model.add_algebraic_module(
    module_name = "Quencher",
    function = Quencher,
    compounds = ["Pr", "V"],
    derived_compounds = ["Q"],
    parameters = ["Xtot", "PsbStot", "Kzsat",
                  "gamma0", "gamma1", "gamma2",
                  "gamma3"])


M16model.add_algebraic_module(
    module_name = 'PSIIstates',
    function = PSII,
    compounds = ["P", "Q"],
    derived_compounds = ["B0", "B1", "B2", "B3"],
    parameters = ["PFD", "PQtot", "kPQred",
                  "KeqQAPQ", "kH", "kF", "kP", "PSIItot"])


M16model.add_algebraic_module(
    module_name = "Fluorescence",
    function = Fluorescence,
    compounds = ["P", "Q", "B0", "B2"],
    derived_compounds = ["Fluo"],
    parameters = ['PFD', 'PQtot', 'kPQred', 'KeqQAPQ',
                  'kH', 'kF', 'kP', 'PSIItot'])

M16model.add_algebraic_module(
    module_name = "L",
    function = lambda X, PFD: PFD ,
    compounds = ["P"],
    derived_compounds = ["L"],
    parameters = ['PFD'])


###############################################################################
# Add rates to model
###############################################################################

M16model.add_reaction(
        rate_name = "vPSII",
        function = vPSII,
        dynamic_variables=["B1"],
        stoichiometry = {"P":1,"H":2/pars["bH"]},
        parameters = ["PFD","PQtot","kPQred", "KeqQAPQ",
                      "kH", "kF", "kP", "PSIItot"])


M16model.add_reaction(
        rate_name = "vPQox",
        function = vPQox,
        dynamic_variables = ['P','H'],
        stoichiometry = {"P":-1,"H":4/pars["bH"]},
        parameters = ["PFD", "kCytb6f", "kPTOX", "O2ex",
                          "PQtot", "F", "E0PQPQH2", "RT", "E0PCPCm",
                          "pHstroma"])


M16model.add_reaction(
        rate_name = "vATPsynthase",
        function = vATPsynthase,
        dynamic_variables = ["A","H","E"],
        stoichiometry = {"A":1, "H": (-14/3)/pars["bH"]},
        parameters = ["kATPsynthase", "DG0ATP", "pHstroma",
                      "RT", "Pi", "APtot"])


M16model.add_reaction(
        rate_name = "vATPactivity",
        function = vATPactivity,
        dynamic_variables = ["E"],
        stoichiometry = {"E":1},
        parameters = ["PFD",  "kActATPase",  "kDeactATPase"])


M16model.add_reaction(
        rate_name = "vLeak",
        function  = vLeak,
        stoichiometry = {"H": -1/pars["bH"]},
        parameters = ["kleak", "pHstroma"])


M16model.add_reaction(
        rate_name = "vATPcons",
        function = vATPcons,
        stoichiometry = {"A":-1},
        parameters = ["kATPconsumption"])


M16model.add_reaction(
        rate_name = "vXcyc",
        function = vXcyc,
        dynamic_variables = ['V','H'],
        stoichiometry = {"V": -1},
        parameters = ["nHX", "KphSatZ", "kDeepoxV",
                      "kEpoxZ", "Xtot"])


M16model.add_reaction(
        rate_name = "vPsbSP",
        function = vPsbSP,
        dynamic_variables = ["Pr", "H"],
        stoichiometry = {"Pr":-1},
        parameters = ["nHL", "KphSatLHC", "kProt",
                      "kDeprot", "PsbStot"])
#%%
if __name__ == "__main__":

    import matplotlib.pyplot as plt

    y0d =  {"P": 0, "H": 6.339572769844456e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}

    #Function for PAM experiment
    def changingLight(model, y0d, lights, interval):
        s = Simulator(model)
        s.initialise(y0d)
        dt = 0
        for i in range(len(interval)):
            s.update_parameter('PFD', lights[i])
            dt += interval[i]
            s.simulate(dt, **{"rtol":1e-16,"atol":1e-6, "maxnef": 20, "maxncf":10})
        return s


    ##########################################################################
    # REPRODUCE FIGURE 4 MATUSZYNSKA 4
    ##########################################################################

    tprot = np.array([  1.        ,   0.8       ,  27.86666667,   0.8       ,
        29.86666667,   0.8       ,  49.53333333,   0.8       ,
        70.2       ,   0.8       ,  91.2       ,   0.8       ,
        110.86666667,   0.8       , 131.2       ,   0.8       ,
        151.53333333,   0.8       , 172.53333333,   0.8       ,
        29.2       ,   0.8       ,  49.2       ,   0.8       ,
        69.53333333,   0.8       ,  89.2       ,   0.8       ,
        109.53333333,   0.8       , 570.53333333,   0.8       ,
        29.2       ,   0.8       ,  29.86666667,   0.8       ,
        49.86666667,   0.8       ,  70.53333333,   0.8       ,
        90.53333333,   0.8       , 110.86666667,   0.8       ])

    ProtPFDs = np.array([   0.   , 5000.   ,    0.   , 5000.   ,  220.003, 5000.   ,
        220.003, 5000.   ,  220.003, 5000.   ,  220.003, 5000.   ,
        220.003, 5000.   ,  220.003, 5000.   ,  220.003, 5000.   ,
        220.003, 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,  220.003, 5000.   ,
        220.003, 5000.   ,  220.003, 5000.   ,  220.003, 5000.   ,
        220.003, 5000.   ])



    PAM1 = changingLight(M16model, y0d, ProtPFDs, tprot)
    F = PAM1.get_variable('Fluo')
    plt.plot(PAM1.get_time()/60, F/max(F))
    plt.xlabel('Time [min]')
    plt.ylabel('Fluorescence')
    plt.show()


    tprot = np.array([   1.        ,    0.8       ,   28.2       ,    0.8       ,
         29.53333333,    0.8       ,   49.53333333,    0.8       ,
         69.86666667,    0.8       ,   89.53333333,    0.8       ,
        109.53333333,    0.8       ,  130.53333333,    0.8       ,
        149.86666667,    0.8       ,  169.86666667,    0.8       ,
         29.53333333,    0.8       ,   49.2       ,    0.8       ,
         69.86666667,    0.8       ,   89.53333333,    0.8       ,
        109.53333333,    0.8       , 1490.53333333,    0.8       ,
         29.2       ,    0.8       ,   29.53333333,    0.8       ,
         49.86666667,    0.8       ,   69.2       ,    0.8       ,
         90.2       ,    0.8       ,  109.2       ,    0.8       ])

    ProtPFDs = np.array([   0.   , 5000.   ,    0.   , 5000.   ,  320.007, 5000.   ,
        320.007, 5000.   ,  320.007, 5000.   ,  320.007, 5000.   ,
        320.007, 5000.   ,  320.007, 5000.   ,  320.007, 5000.   ,
        320.007, 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,  320.007, 5000.   ,
        320.007, 5000.   ,  320.007, 5000.   ,  320.007, 5000.   ,
        320.007, 5000.   ])

    PAM2 = changingLight(M16model, y0d, ProtPFDs, tprot)
    F = PAM2.get_variable('Fluo')
    plt.plot(PAM2.get_time()/60, F/max(F))
    plt.xlabel('Time [min]')
    plt.ylabel('Fluorescence')
    plt.show()



    tprot = np.array([   1.        ,    0.8       ,   27.86666667,    0.8       ,
         29.53333333,    0.8       ,   49.86666667,    0.8       ,
         69.2       ,    0.8       ,   90.2       ,    0.8       ,
        109.86666667,    0.8       ,  129.86666667,    0.8       ,
        150.86666667,    0.8       ,  170.86666667,    0.8       ,
         29.2       ,    0.8       ,   49.2       ,    0.8       ,
         69.53333333,    0.8       ,   89.86666667,    0.8       ,
        109.2       ,    0.8       , 3270.53333333,    0.8       ,
         29.53333333,    0.8       ,   29.53333333,    0.8       ,
         49.53333333,    0.8       ,   69.86666667,    0.8       ,
         89.2       ,    0.8       ,  110.2       ,    0.8       ])

    ProtPFDs = np.array([   0.   , 5000.   ,    0.   , 5000.   ,  900.003, 5000.   ,
        900.003, 5000.   ,  900.003, 5000.   ,  900.003, 5000.   ,
        900.003, 5000.   ,  900.003, 5000.   ,  900.003, 5000.   ,
        900.003, 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,    0.   , 5000.   ,
          0.   , 5000.   ,    0.   , 5000.   ,  900.003, 5000.   ,
        900.003, 5000.   ,  900.003, 5000.   ,  900.003, 5000.   ,
        900.003, 5000.   ])

    PAM3 = changingLight(M16model, y0d, ProtPFDs, tprot)
    F = PAM3.get_variable('Fluo')
    plt.plot(PAM3.get_time()/60, F/max(F))
    plt.xlabel('Time [min]')
    plt.ylabel('Fluorescence')
    plt.show()
