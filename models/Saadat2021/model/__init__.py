from modelbase2 import Model
from .derived_quantities import include_derived_quantities
from .rates import include_rates

__all__ = [
    'Saadat2021'
]

def Saadat2021() -> Model:
    m = Model()

    m.add_parameters(
        {
            'convf': 3.2e-3,     # [] Conversion factor of ATP and NADPH
            'PSII_tot': 2.5,     # [mmol (mol Chl)-1] PSII reaction centres
            'PSI_tot': 2.5,     # [mmol (mol Chl)-1] PSI reaction centres
            'PQ_tot': 17.5,     # [mmol (mol Chl)-1] Total plastoquinone pool
            'PC_tot': 4.0,     # [mmol (mol Chl)-1] Total plastocyanine pool
            'Fd_tot': 5.0,     # [mmol (mol Chl)-1] Total ferrodoxin pool
            'NADP_tot': 0.8,     # [mM] Total NADP pool
            'AP_tot': 2.55,     # [mM] Total adenosine phosphate pool
            'PsbS_tot': 1.0,     # [mmol (mol Chl)-1] Relative pool of PsbS
            'X_tot': 1.0,     # [mmol (mol Chl)-1] Relative pool of xanthophylls
            'k_H': 5e9,     # [s-1] Rate of non-radiative decay
            'kH0': 5e8,     # [s-1] Base rate of non-radiative decay
            'k_F': 6.25e8,     # [s-1] Rate of fluorescence
            'k2': 5e9,     # [s-1] Rate constant for photochemistry
            'k_Stt7': 0.0035,     # [s-1] Rate of phosphorylation of state transition from PSII to PSI
            'k_Pph1': 0.0013,     # [s-1] Rate of dephosphorylation of state transition from PSI to PSII
            'KM_ST': 0.2,     # [] Switch point (half-activity of Stt7) for 20% PQ oxidised
            'n_ST': 2.0,     # [] Hill coefficient of State transtion from PSII to PSI
            'sigma0_I': 0.37,     # [] Relative cross section of PSI-LHCl supercomplex
            'sigma0_II': 0.1,     # [] Relative cross section of PSII
            'k_ATPsynth': 20.0,     # [s-1] Rate constant of ATP synthase
            'Pi_mol': 0.01,     # [mmol (mol Chl)-1] Internal pool of phosphates, required to calculate ATP equilibrium
            'DeltaG0_ATP': 30.6,     # [kJ mol-1] Standard Gibbs free energy change of ATP formation
            'HPR': 14 / 3,     # [] Ratio of protons to ATP in ATP synthase
            'pH_stroma': 7.9,     # [] Stromal pH of a dark adapted state
            'k_Leak': 10.0,     # [s-1] Rate constant of proton leak
            'b_H': 100.0,     # [] Buffering protons constant of lumen
            'k_PQred': 250.0,     # [(mol Chl) mmol-1 s-1 ]
            'k_Cytb6f': 2.5,     # [(mol Chl)2  mmol-2 s-1 ]
            'k_PTOX': 0.01,     # [(mol Chl) mmol-1 s-1 ]
            'k_PCox': 2500.0,     # [(mol Chl) mmol-1 s-1 ]
            'k_Fdred': 2.5e5,     # [(mol Chl) mmol-1 s-1 ]
            'kcat_FNR': 500.0,     # [s-1] Catalytic constant of FNRase
            'k_cyc': 1.0,     # [s-1] Reaction rate constant of cyclic electron flow
            'O2_ext': 8.0,     # [mmol (mol Chl)-1] External oxygen pool, corresponds to 250μM.
            'k_NDH': 0.002,     # [s-1]
            'EFNR': 3.0,     # []
            'KM_FNR_F': 1.56,     # [mmol (mol Chl)-1]
            'KM_FNR_N': 0.22,     # [mmol (mol Chl)-1]
            'gamma_0': 0.1,     # [] Fitted quencher factor corresponding to base quenching not associated with protonation or zeaxanthin
            'gamma_1': 0.25,     # [] Fitted quencher factor corresponding to fast quenching due to protonation
            'gamma_2': 0.6,     # [] Fitted quencher factor corresponding to fastest possible quenching
            'gamma_3': 0.15,     # [] Fitted quencher factor corresponding to slow quenching of Zx present despite lack of protonation
            'k_deprot': 0.0096,     # [s-1] Rate of PsbS deprotonation
            'k_prot': 0.0096,     # [s-1] Rate of PsbS protonation
            'K_pHSatLHC': 5.8,     # [] pKa of PsbS activation, kept the same as for VDA
            'k_DV': 0.0024,     # [s-1] Rate constant of de-epoxidation of violaxanthin
            'k_EZ': 0.00024,     # [s-1] Rate constant of epoxidation of violaxanthin
            'K_pHSat': 5.8,     # [] Half-saturation pH for de-epoxidase activity, highest activity at pH 5.8
            'nh_x': 5,     # [] Hill-coefficient for de-epoxidase acitivity
            'nh_PsbS': 3.0,     # [] Hill-coefficient for PsbS protonation
            'K_ZSat': 0.12,     # [] Half-saturation constant (relative conc. of Zx) for quenching
            'E0_QA': -0.140,     # [V]
            'E0_PQ': 0.354,     # [V]
            'E0_PC': 0.380,     # [V]
            'E0_P700': 0.48,     # [V]
            'E0_FA': -0.55,     # [V]
            'E0_Fd': -0.43,     # [V]
            'E0_NADP': -0.113,     # [V]
            'F': 96.485,     # [kJ] Faraday constant
            'R': 0.0083,     # [J K-1 mol-1] Universal gas constant
            'T': 298.0,     # [K] Temperature
            'pfd': 100.0,     # [µmol m-2 s-1] Photon Flux Density
            'Ton': 0.0,     # [s] Time point with anoxia condition
            'Toff': 1800,     # [s] Time point without anoxia condition
            'ox': True,     # [] Conditional for constant oxygen supply
            'CO2': 0.2,     # [mM]
            'P_tot': 17.05,     # [mmol (mol Chl)-1] Total Phosphate pool
            'Pext': 0.5,     # [mM] External phosphate
            'V_maxbase_rubisco': 0.34 * 8,     # [mM s-1] Base $V_\mathrm{max}$ of RuBisCO
            'V_maxbase_fbpase': 1.6,     # [mM s-1] Base $V_\mathrm{max}$ of FBPase
            'V_maxbase_sbpase': 0.32,     # [mM s-1] Base $V_\mathrm{max}$ of SBPase
            'V_maxbase_prkase': 7.9992,     # [mM s-1] Base $V_\mathrm{max}$ of PRKase
            'V_maxbase_starch': 0.32,     # [mM s-1] Base $V_\mathrm{max}$ of Starch Synthase
            'Vmax_ex': 2.0,     # [mM s-1] $V_\mathrm{max}$ of Export
            'K_PGK1ase': 3.1e-4,     # [] Equilibrium constant of PGK1ase
            'K_BPGAdehynase': 1.6e7,     # [] Equilibrium constant of BPGA dehydrogenase
            'K_TPIase': 22.0,     # [] Equilibrium constant of TPIase
            'K_Aldolase_FBP': 7.1,     # [mM-1] Equilibrium constant of Aldolase of GAP and DHAP to FBP
            'K_TKase_E4P': 0.084,     # [] Equilibrium constant of TKase of GAP and F6P to X5P and E4P
            'K_Aldolase_SBP': 13.0,     # [mM-1] Equilibrium constant of Aldolase of E4P and DHAP to SBP
            'K_TKase_R5P': 0.85,     # [] Equilibrium constant of TKase of GAP and S7P to X5P and R5P
            'K_Rpiase': 0.4,     # [] Equilibrium constant of Rpiase
            'K_RPEase': 0.67,     # [] Equilibrium constant of RPEase
            'K_PGIase': 2.3,     # [] Equilibrium constant of PGIase
            'K_PGMase': 0.058,     # [] Equilibrium constant of PGMase
            'Km_RuBisCO_RUBP': 0.02,     # [mM] Michaelis Menten constant of RuBisCO for RUBP
            'Km_RuBisCO_CO2': 0.0107,     # [mM] Michaelis Menten constant of RuBisCO for CO2
            'Km_FBPase': 0.03,     # [mM] Michaelis Menten constant of FBPase
            'Km_SBPase': 0.013,     # [mM] Michaelis Menten constant of SBPase
            'Km_PRKase_RU5P': 0.05,     # [mM] Michaelis Menten constant of PRKase for RU5P
            'Km_PRKase_ATP': 0.05,     # [mM] Michaelis Menten constant of PRKase for ATP
            'Km_Starch_G1P': 0.08,     # [mM] Michaelis Menten constant of Starch production for G1P
            'Km_Starch_ATP': 0.08,     # [mM] Michaelis Menten constant of Starch production for ATP
            'K_diss_PGA': 0.25,     # [mM] Dissociation constant for the complex formed by phosphate translocator and PGA
            'K_diss_GAP': 0.075,     # [mM] Dissociation constant for the complex formed by phosphate translocator and GAP
            'K_diss_DHAP': 0.077,     # [mM] Dissociation constant for the complex formed by phosphate translocator and DHAP
            'K_diss_Pi': 0.63,     # [mM] Dissociation constant for the complex formed by phosphate translocator and Pi
            'K_diss_Pext': 0.74,     # [mM] Dissociation constant for the complex formed by phosphate translocator and external orthophosphate
            'Ki_RuBisCO_PGA': 0.04,     # [mM] Inhibition constant of RuBisCO by PGA
            'Ki_RuBisCO_FBP': 0.04,     # [mM] Inhibition constant of RuBisCO by FBP
            'Ki_RuBisCO_SBP': 0.075,     # [mM] Inhibition constant of RuBisCO by SBP
            'Ki_RuBisCO_Pi': 0.9,     # [mM] Inhibition constant of RuBisCO by Pi
            'Ki_RuBisCO_NADPH': 0.07,     # [mM] Inhibition constant of RuBisCO by NADPH
            'Ki_FBPase_F6P': 0.7,     # [mM] Inhibition constant of FBPase by F6P
            'Ki_FBPase_Pi': 12.0,     # [mM] Inhibition constant of FBPase by Pi
            'Ki_SBPase_Pi': 12.0,     # [mM] Inhibition constant of SBPase by Pi
            'Ki_PRKase_PGA': 2.0,     # [mM] Inhibition constant of Ru5P of PRKase by PGA
            'Ki_PRKase_RuBP': 0.7,     # [mM] Inhibition constant of Ru5P of PRKase by RuBP
            'Ki_PRKase_Pi': 4.0,     # [mM] Inhibition constant of Ru5P of PRKase by Pi
            'Kiunc_PRKase_ADP': 2.5,     # [mM] Uncompetitive inhibition constant of ATP of PRKase by ADP
            'Kicom_PRKase_ADP': 0.4,     # [mM] Competitive inhibition constant of ATP of PRKase by ADP
            'Ki_Starch_ADP': 10.0,     # [mM] Inhibition constant of ATP of Starch production by ADP
            'Kact_Starch_PGA': 0.1,     # [] Activation factor of Starch production by PGA
            'Kact_Starch_F6P': 0.02,     # [] Activation factor of Starch production by F6P
            'Kact_Starch_FBP': 0.02,     # [] Activation factor of Starch production by FBP
            'k_fast': 8e8,     # [mM] Arbituary fast rate constant
            'k_f1': 10000.0,     # []
            'k_r1': 220.0,     # []
            'k_f2': 10000.0,     # []
            'k_r2': 4000.0,     # []
            'k_f3': 2510.0,     # []
            'k_f4': 10000.0,     # []
            'k_r4': 4000.0,     # []
            'k_f5': 2510.0,     # []
            'XT': 0.07,     # [] Concentration of ascorbate peroxidase
            'k_Mehler': 1.0,     # [mM-1 s-1] Estimated rate constant for summarized hydrogen peroxide production
            'kcat_GR': 595,     # [s-1] Turnover rate of gluthation reductase
            'kcat_DHAR': 142,     # [s-1] Turnover rate of dehydroascorbate reductase
            'k3': 500.0,     # [mM-1 s-1] Rate constant for the spontaneous disproportion of MDA
            'Km_NADPH': 3e-3,     # [mM] Michaelis Menten constant of NADPH
            'Km_GSSG': 0.2,     # [mM] Michaelis Menten constant of oxidized gluthation
            'Km_DHA': 70e-3,     # [mM] Michaelis Menten constant of dehydroascorbate
            'Km_GSH': 2.5,     # [mM] Michaelis Menten constant of reduced gluthation
            'K_DHAR': 0.5,     # [mM2] Dissociation constant of dehydroascorbate reductase
            'GR_0': 1.4e-3,     # [mM] Concentration of gluthatione reductase
            'DHAR_0': 1.7e-3,     # [mM] Concentration of dehydroascorbate reductase
            'Glutathion_total': 10,     # [mM] Total concentration of reduced and oxidized glutathione
            'Ascorbate_total': 10,     # [mM] Total concentration of reduced and oxidized ascorbate
            'kcat_MDAR': 300.0,     # [s-1] Turnover rate of monodehydroascorbate reductase
            'Km_MDAR_NADPH': 23e-3,     # [mM] Michaelis-menten constant of monodehydroascorbate for the conversion to NADPH
            'Km_MDAR_MDA': 1.4e-3,     # [mM] Michaelis-menten constant of monodehydroascorbate for the conversion to MDA
            'MDAR_0': 2e-3,     # [mM] Concentration of monodehydroascorbate reductase
            'k_ex_atp': 0.2,     # [s-1] General consumption rate of ATP
            'k_ex_nadph': 0.2,     # [s-1] General consumption rate of NADPH
            'thioredoxin_tot': 1,     # [] Relative total concentration of thioredoxin
            'e_cbb_tot': 6,     # [mM] Estimated maximal concentration of CBB enzymes
            'k_fd_tr_reductase': 1,     # [s-1] Rate constant of ferrodoxin thioredoxin reductase
            'k_e_cbb_activation': 1,     # [] Rate constant of CBB activation
            'k_e_cbb_relaxation': 0.1,     # [s-1] Rate constant of CBB relaxation
        }
    )

    m.add_variables(
        {
            "PQ": 11.027139850905353,
            "PC_ox": 1.8895071932002812,
            "Fd_ox": 3.8690237263896705,
            "ATP_st": 1.620195002854852,
            "NADPH_st": 0.4882103700673736,
            "H_lu": 0.0022147075094596015,
            "LHC": 0.8023074419510501,
            "psbS": 0.9607146039898598,
            "Vx": 0.950783616933656,
            "PGA": 0.9913970817549008,
            "BPGA": 0.0005355311557548053,
            "GAP": 0.0062630116252017295,
            "DHAP": 0.13778623933075737,
            "FBP": 0.006126990841013743,
            "F6P": 0.31166103888161867,
            "G6P": 0.7168203893211117,
            "G1P": 0.041575582577936025,
            "SBP": 0.01311315151803723,
            "S7P": 0.15782894767619207,
            "E4P": 0.00732079113061801,
            "X5P": 0.022396849486562384,
            "R5P": 0.03751472214765548,
            "RUBP": 0.13153657267999222,
            "RU5P": 0.015005888732707041,
            "MDA": 5.85270097771621e-06,
            "H2O2": 3.4273920330125316e-06,
            "DHA": 8.513863740903352e-09,
            "GSSG": 4.137406632226743e-09,
            "TR_ox": 0.9,
            "E_CBB_inactive": 4.7368421052631575,
        }
    )

    m = include_derived_quantities(m)
    m = include_rates(m)

    return m

m = Saadat2021()
