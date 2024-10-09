# Model parameters
# Exported on 04.03.2024 - 08:57

import pandas as pd

p = { # Module parameters
    'PSIItot': 0.830, # [mmol mol(Chl)^-1] total concentration of photosystem II complexes (Zavrel2023)
    'PSItot': 3.270, # [mmol mol(Chl)^-1] total concentration of photosystem I complexes (Zavrel2023)
    'Q_tot': 13.000, # [mmol mol(Chl)^-1] total PHOTOACTIVE PQ concentration (Khorobrykh2020)
    'PC_tot': 1.571, # [mmol mol(Chl)^-1] total concentration of plastocyanin (PC_ox + PC_red) (Zavrel2019)
    'Fd_tot': 3.597, # [mmol mol(Chl)^-1] total concentration of ferredoxin (Fd_ox + Fd_red) (Moal2012)
    'NADP_tot': 26.805, # [mmol mol(Chl)^-1] total concentration of NADP species (NADP + NADPH) (Kauny2014)
    'NAD_tot': 11.169, # [mmol mol(Chl)^-1] total concentration of NAD species (NAD + NADH) (Tanaka2021)
    'AP_tot': 430.143, # [mmol mol(Chl)^-1] total concentration of adenosine species (ADP + ATP) (Doello2018)
    'O2ext': 55.402, # [mmol mol(Chl)^-1] concentration of oxygen in the surrounding medium (Kihara2014)
    'CO2ext': 3.103, # [mmol mol(Chl)^-1] saturated concentration of CO2 in 25 °C water with ~10 ‰ Cl^- ions (Li1971)
    'F': 96.485, # [C mmol^-1] Faraday's constant (Richardson2019)
    'R': 8.300e-03, # [J K^-1 mmol^-1] ideal gas constant (Richardson2019)
    'T': 298.150, # [K] temperature (set)
    'bHi': 100.000, # [unitless] buffering constant of the thylakoid lumen (estimated)
    'bHo': 1.111e+03, # [unitless] buffering constant of the cytoplasm, assumed to be 1/f_V_lumen times larger (estimated)
    'cf_lumen': 4.613e-05, # [mol(Chl) ml^-1] conversion factor for [mmol mol(Chl)^-1] -> [mol l^-1] for the thylakoid lumen (derived)
    'cf_cytoplasm': 4.562e-06, # [mol(Chl) ml^-1] conversion factor for [mmol mol(Chl)^-1] -> [mol l^-1] for the cytoplasm (derived)
    # 'fCin': 100.000, # [unitless] ratio of intracellular to external CO2 concentration with activity of the CCM (Hagemann2021)
    'E0_QA': -0.140, # [V] standard electrode potential of the reduction of PS2 plastoquinone A (Lewis2022)
    'E0_PQ': 0.533, # [V] standard electrode potential of the reduction of free plastoquinone (Lewis2022)
    'E0_PC': 0.350, # [V] standard electrode potential of the reduction of free plastocyanin (Lewis2022)
    'E0_P700': 0.410, # [V] standard electrode potential of the reduction of the oxidised PS1 reaction center (Lewis2022)
    'E0_FA': -0.580, # [V] standard electrode potential of the reduction of PS1 iron-sulfur cluster A (Lewis2022)
    'E0_Fd': -0.410, # [V] standard electrode potential of the reduction of free ferredoxin (Lewis2022)
    'E0_NADP': -0.113, # [V] standard electrode potential of the reduction of NADP to NADPH (Falkowski2007)
    'E0_succinate/fumarate': 0.443, # [V] standard electrode potential of the reduction of fumarate to succinate (Falkowski2007)
    'kH0': 5.000e+08, # [s^-1] rate constant of (unregulated) excitation quenching by heat (Ebenhoh2014)
    'kHst': 1.000e+09, # [s^-1] rate constant of state transition regulated excitation quenching by heat (guess)
    'kF': 6.250e+08, # [s^-1] rate constant of excitation quenching by fluorescence (Ebenhoh2014)
    'k2': 2.500e+09, # [s^-1] rate constant of excitation quenching by photochemistry (Ebenhoh2014,Bernat2009)
    'kPQred': 250.000, # [mol(Chl) mmol^-1 s^-1] rate constant of PQ reduction via PS2 (Matuszynska2019)
    # 'kQuench': 2.500e-05, # [mol(Chl) mmol^-1 s^-1] rate constant of PS2 quenching by Q_red (manually fitted)
    # 'kUnquench': 1.250e-03, # [mol(Chl) mmol^-1 s^-1] rate constant of PS2 unquenching by Q_ox (manually fitted)
    # 'kATPconsumption': 0.300, # [s^-1] rate constant of ATP consumption by processes other than the CBB (guess)
    # 'kNADHconsumption': 10.000, # [s^-1] rate constant of NADH consumption by processes other than NDH (guess)
    'kFlvactivation': 0.500, # [s^-1] rate constant of Flv activation by reduced Fd (manually fitted)
    'kFlvdeactivation': 0.100, # [s^-1] rate constant of Flv deactivation by oxidised Fd (manually fitted)
    # 'kCBBactivation': 5.000e-02, # [s^-1] rate constant of CBB activation by reduced Fd (manually fitted)
    'kCBBdeactivation': 2.500e-03, # [s^-1] rate constant of CBB deactivation by oxidised Fd (manually fitted)
    'kPCox': 2.500e+03, # [mol(Chl) mmol^-1 s^-1] rate constant of PC oxidation via PS1 (Matuszynska2019)
    'kFdred': 2.500e+05, # [mol(Chl) mmol^-1 s^-1] rate constant of Fd reduction via PS1 (Matuszynska2019)
    # 'k_F1': 1.000, # [s^-1] rate constant of excitation quenching via fluorescence (guess)
    'k_ox1': 0.211, # [mol(Chl)^2 mmol^-2 s^-1] rate constant of oxygen reduction via bd-type (Cyd) terminal oxidases (Ermakova2016)
    # 'k_Q': 1.755e+03, # [mol(Chl) mmol^-1 s^-1] rate constant of PC reduction by the cytochrome b6f complex (Setif2020)
    'k_NDH': 3.136, # [mol(Chl) mmol^-1 s^-1] rate constant of PQ reduction by NDH-2 (Cooley2001)
    'k_SDH': 0.430, # [mol(Chl) mmol^-1 s^-1] rate constant of PQ reduction by SDH (Cooley2001)
    'k_O2': 35.935, # [mol(Chl)^2 mmol^-2 s^-1] rate constant of Fd oxidation by Flv 1/3 (Ermakova2016)
    'k_FN_fwd': 3.730, # [mol(Chl) mmol^-1 s^-1] rate constant of NADP reduction by FNR (Kauny2014)
    'k_FN_rev': 53.364, # [mol(Chl)^3 mmol^-3 s^-1] rate constant of reverse flux through FNR in darkness (Kauny2014)
    # 'k_pass': 1.000e-02, # [mmol mol(Chl)^-1 s^-1] rate constant of protons leaking across the thylakoid membrane per delta pH (guess)
    'k_NQ': 100.000, # [mol(Chl) mmol^-1 s^-1] rate constant of PQ reduction by NDH (Theune2021)
    # 'k_aa': 1.156, # [mol(Chl)^2 mmol^-2 s^-1] rate constant of oxygen reduction via aa3-type (COX) terminal oxidases (Ermakova2016)
    'kRespiration': 3.506e-06, # [mol(Chl)^3 mmol^-3 s^-1] rate constant of 3PGA oxidation and fumarate reduction by glycolysis and the TCA cycle (Ermakova2016)
    'kO2out': 4.025e+03, # [s^-1] rate constant of oxygen diffusion out of the cell (Kihara2014)
    'kCCM': 4.025e+03, # [s^-1] rate constant of CO2 diffusion into the cell, assumed to be identical to kO2out (guess)
    # 'fluo_influence': {'PS2': 1.000, 'PS1': 1.000, 'PBS': 1.250}, # [unitless] factors multiplied to the calculated fluorescence (no effect at 1) (manually fitted)
    'PBS_free': 9.000e-02, # [unitless] fraction of unbound PBS (Zavrel2023)
    'PBS_PS1': 0.390, # [unitless] fraction of PBS bound to PSI (Zavrel2023)
    'PBS_PS2': 0.510, # [unitless] fraction of PBS bound to PSII (Zavrel2023)
    'pigment_content': pd.Series({'chla': 1.000, 'beta_carotene': 0.176, 'allophycocyanin': 1.118, 'phycocyanin': 6.765}), # [mg(Pigment) mg(Chla)^-1] relative pigment concentrations in a synechocystis cell (Zavrel2023)
    # 'lcf': 0.500, # [excitations photons^-1] light conversion factor (manually fitted)
    # 'kATPsynth': 10.000, # [s^-1] rate constant of ATP synthesis (fit to supply CBB)
    'Pi_mol': 1.000e-02, # [mmol mol(Chl)^-1] molar conccentration of phosphate (Matuszynska2019)
    'DeltaG0_ATP': 30.600, # [kJ mol^-1] energy of ATP formation (Matuszynska2019)
    'HPR': 4.667, # [unitless] number of protons (14) passing through the ATP synthase per ATP (3) synthesized (Pogoryelov2007)
    'vOxy_max': 16.059, # [mmol mol(Chl)^-1 s^-1] approximate Rubisco oxygenation rate (Savir2010)
    'KMATP': 24.088, # [mmol mol(Chl)^-1] order of magnitude of the michaelis constant for ATP consumption in the CBB cycle (Wadano1998,Tsukamoto2013)
    'KMNADPH': 18.066, # [mmol mol(Chl)^-1] approxiate michaelis constant for NADPH consumption in the CBB cycle (Koksharova1998)
    'KMCO2': 72.264, # [mmol mol(Chl)^-1] order of magnitude of the michaelis constant for CO2 consumption by cyanobacterial Rubisco (Savir2010)
    'KIO2': 240.880, # [mmol mol(Chl)^-1] order of magnitude of the michaelis inhibition constant of O2 for CO2 consumption by cyanobacterial Rubisco, assumed equal to KMO2 (Savir2010)
    'KMO2': 240.880, # [mmol mol(Chl)^-1] order of magnitude of the michaelis constant for O2 consumption by cyanobacterial Rubisco (Savir2010)
    'KICO2': 72.264, # [mmol l^-1] order of magnitude of the michaelis inhibition constant of CO2 for O2 consumption by cyanobacterial Rubisco, assumed equal to KMCO2 (Savir2010)
    # 'KMPGA': 0.100, # [mmol mol(Chl)^-1] arbitrary michaelis constant limiting oxygenation reactions for low 3PGA (guess)
    'vCBB_max': 51.301, # [mmol mol(Chl)^-1 s^-1] approximate maximal rate of the Calvin Benson Bassham cycle (Zavrel2017)
    'kPR': 1.523e-06, # [mol(Chl)^4 mmol^-4 s^-1] rate constant of (2-phospho)glycolate recycling into 3PGA (Huege2011)
    'fCin': 1032.3825198828176,
    'k_F1': 1.0144691550897802,
    'k_Q': 1789.6877149900638,
    'k_pass': 0.0103757688087645,
    'k_aa': 1.0726342220286855,
    'fluo_influence': {
        'PS2': 1.0871604554468057,
        'PS1': 1.0580747331180056,
        'PBS': 1.2652931291892002
    },
    'lcf': 0.4852970468572075,
    'KMPGA': 0.108119035344566,
    'kATPsynth': 10.508685365751944,
    'kATPconsumption': 0.3007216562727887,
    'kNADHconsumption': 10.774127129643528,
    'kUnquench': 0.1084895168082126,
    'KMUnquench': 0.2057753667172297,
    'kQuench': 0.0021298894016293,
    'KHillFdred': 39.138885950985646,
    'nHillFdred': 3.803733201004677,
    'kCBBactivation': 0.0368469911771887,
    'KMFdred': 0.2867372651572032,
    'kOCPactivation': 9.119349718302952e-05,
    'kOCPdeactivation': 0.0013779872861697,
    'OCPmax': 0.2894610142573665,
    'vNQ_max': 47.52413111835536,
    'KMNQ_Qox': 1.225188500783819,
    'KMNQ_Fdred': 1.3324893590389415
}

pu = { # Update-module parameters
    'cChl': 4.151e-03, # [mol l^-1] total molar concentration of chlorophyll (derived)
    'CO2ext_pp': 5.000e-02, # [atm] CO2 partial pressure in 5% CO2 enriched air used for bubbeling (set)
    # 'KHillFdred': 39.062, # [mmol^nHillFdred mol(Chl)^-nHillFdred] Flv binding constant of Fd_red in Hill kinetics, assuming half activity around 2.5 mmol mol(Chl)^-1 (guess)
    # 'nHillFdred': 4.000, # [unitless] Hill constant of Fd_red binding to Flv, assuming stong cooperative binding (see Brown2019) (guess)
    'S': 35.000, # [unitless] salinity within a cell (MojicaPrieto2002)
    'k_O2': 12.926, # [mol(Chl)^2 mmol^-2 s^-1] rate constant of Fd oxidation by Flv 1/3 (Ermakova2016)
    # 'fCin': 1000.000, # [unitless] ratio of intracellular to external CO2 partial pressure with activity of the CCM (Hagemann2021,Benschop2003)
    # 'kOCPactivation': 9.600e-05, # [s^-1 (umol(Photons) m^-2 s^-1)^-1] rate constant of OCP activation by absorbed light (manually fitted)
    # 'kOCPdeactivation': 1.350e-03, # [s^-1] rate constant of OCP deactivation by thermal processes (manually fitted)
    # 'OCPmax': 0.280, # [unitless] maximal fraction of PBS quenched by OCP (Tian2011)
    # 'kUnquench': 0.100, # [s^-1] rate constant of internal PS2 unquenching (manually fitted)
    # 'KMUnquench': 0.200, # [mmol mol(Chl)^-1] binding constant of PS2 unquenching inhibition by Q_red (manually fitted)
    # 'kQuench': 2.000e-03, # [mmol^-1 mol(Chl)^-1 s^-1] rate constant of PS2 quenching by Q_red (manually fitted)
    # 'kCBBactivation': 3.466e-02, # [s^-1] rate constant of CBB activation by reduced ferredoxin (Nikkanen2020)
    # 'KMFdred': 0.300, # [mmol mol(Chl)^-1] Michaelis constant of CBB activation by reduced ferredoxin (Schuurmans2014)
    'KHillFdred_CBB': 1.000e-04, # [mmol^nHillFdred_CBB mol(Chl)^-nHillFdred_CBB] Apparent dissociation constant of reduced ferredoxin for CBB activation (Schuurmans2014)
    'nHillFdred_CBB': 4.000, # [unitless] Hill coefficient of CBB activation by reduced ferredoxin (guess)
    # 'vNQ_max': 50.000, # [mmol mol(Chl)^-1 s^-1] maximal rate of NDH-1 ()
    # 'KMNQ_Qox': 1.300, # [mmol mol(Chl)^-1] Michaelis constant for Q_ox reduction by NDH-1 (guess)
    # 'KMNQ_Fdred': 1.439, # [mmol mol(Chl)^-1] Michaelis constant for Fd_red oxidation by NDH-1 (guess)
    'fCin': 1032.3825198828176,
    'k_F1': 1.0144691550897802,
    'k_Q': 1789.6877149900638,
    'k_pass': 0.0103757688087645,
    'k_aa': 1.0726342220286855,
    'fluo_influence': {
        'PS2': 1.0871604554468057,
        'PS1': 1.0580747331180056,
        'PBS': 1.2652931291892002
    },
    'lcf': 0.4852970468572075,
    'KMPGA': 0.108119035344566,
    'kATPsynth': 10.508685365751944,
    'kATPconsumption': 0.3007216562727887,
    'kNADHconsumption': 10.774127129643528,
    'kUnquench': 0.1084895168082126,
    'KMUnquench': 0.2057753667172297,
    'kQuench': 0.0021298894016293,
    'KHillFdred': 39.138885950985646,
    'nHillFdred': 3.803733201004677,
    'kCBBactivation': 0.0368469911771887,
    'KMFdred': 0.2867372651572032,
    'kOCPactivation': 9.119349718302952e-05,
    'kOCPdeactivation': 0.0013779872861697,
    'OCPmax': 0.2894610142573665,
    'vNQ_max': 47.52413111835536,
    'KMNQ_Qox': 1.225188500783819,
    'KMNQ_Fdred': 1.3324893590389415
}

y0 = { # Module initial concentrations
    'PSII': 0.415, # [mmol mol(Chl)^-1] initial concentration of unquenched PSII (guessed from ca. 50% reduced plastoquinone) (guess)
    'O2': 55.402, # [mmol mol(Chl)^-1] concentration of oxygen in the cell (Kihara2014)
    'PC_ox': 0.157, # [mmol mol(Chl)^-1] initial concentration of oxidised plastocyanin (aerobic) (Schreiber2017)
    'Fd_ox': 3.237, # [mmol mol(Chl)^-1] initial concentration of oxidised ferredoxin (aerobic) (Schreiber2017)
    'NADPH': 20.104, # [mmol mol(Chl)^-1] initial concentration of NADPH (Cooley2001)
    'NADH': 3.574, # [mmol mol(Chl)^-1] initial concentration of NADH (Tanaka2021)
    'ATP': 172.057, # [mmol mol(Chl)^-1] initial concentration of ATP (Doello2018)
    'PG': 0.894, # [mmol mol(Chl)^-1] initial concentration of (2-phospho) glycolate (Huege2011)
    'succinate': 2.000, # [mmol mol(Chl)^-1] initial concentration of succinate (guess)
    'fumarate': 2.000, # [mmol mol(Chl)^-1] initial concentration of fumarate (guess)
    'GA': 0.500, # [mmol mol(Chl)^-1] initial concentration of glycerate (guess)
    '3PGA': 2.000e+03, # [mmol mol(Chl)^-1] initial concentration of 3-phospho glycerate (including all other sugars) (guess)
    'CO2': 310.253, # [mmol mol(Chl)^-1] concentration of CO2 in the cell increased by activity of the CCM (estimated)
    'Flva': 0.000e+00, # [unitless] fraction of Fd-activated Flv enzyme (guess)
    'CBBa': 0.000e+00, # [unitless] fraction of Fd-activated, lumped enzymes of the CBB (guess)
    'Hi': 0.217, # [mmol mol(Chl)^-1] initial concentration of lumenal protons in 10^4 uE cm^-1 s^-1 light (Belkin1987)
    'Ho': 6.932e-03, # [mmol mol(Chl)^-1] initial concentration of cytoplasmic protons in 10^4 uE cm^-1 s^-1 light (Belkin1987)
    'Q_ox': 7.202, # [mmol mol(Chl)^-1] concentration of oxidised, PHOTOACTIVE plastoquinone in 40 umol m^-2 s^-1 irradiation (Khorobrykh2020)
}

y0u = { # Update-module initial concentrations
    'CO2': 3.103, # [mmol mol(Chl)^-1] concentration of CO2 in the cell without activity of the CCM (estimated)
    'OCP': 0.000e+00, # [unitless] initial activity of OCP (guess)
}