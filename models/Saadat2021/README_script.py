from mdutils.mdutils import MdUtils  # noqa: E402
from glossary_utils.glossary import update_from_main_gloss, gloss_fromCSV, write_python_from_gloss, write_odes_from_model, extract_params_from_model
from pathlib import Path
import pandas as pd
from models import get_model

import os

###### Util Functions ######

def remove_math_mode(
    dic: dict,
    k: str,
    column_name: str = 'Abbreviation Here'
):
    s = dic[k][column_name]

    for i in range(dic[k][column_name].count('$')):
        s = s.replace('$', '')

    return s

def ode(
    first_var: str,
    second_var: str = 't'
):
    for i in [first_var, second_var]:
        if '$' in i:
            raise ValueError(f"Your given variable '{i}' has a '$' in it")

    return rf'\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}'

###### Model Infos ######

model_title = 'Saadat2021'
model_doi = 'https://doi.org/10.3389/fpls.2021.750580'

###### Glossaries ######

cite_dict = dict()

model_info = Path(__file__).parent / 'model_info'
python_written = model_info / 'python_written'
main_gloss = Path(__file__).parents[2] / 'Templates'

update_from_main_gloss(
    main_gloss_path=main_gloss / 'comp_glossary.csv',
    gloss_path=model_info / 'comps.csv',
    add_to_main=True,
    model_title=model_title
)

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / 'comps.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=python_written / 'comps.txt',
    gloss=comps_table,
    var_list_name='comps_table'
)

update_from_main_gloss(
    main_gloss_path=main_gloss / 'comp_glossary.csv',
    gloss_path=model_info / 'derived_comps.csv',
    add_to_main=True,
    model_title=model_title
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(
    path=model_info / 'derived_comps.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=python_written / 'derived_comps.txt',
    gloss=derived_comps_table,
    var_list_name='derived_comps_table'
)

update_from_main_gloss(
    main_gloss_path=main_gloss / 'rates_glossary.csv',
    gloss_path=model_info / 'rates.csv',
    add_to_main=True,
    model_title=model_title
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / 'rates.csv',
    omit_col='Glossary ID'
)

write_python_from_gloss(
    path_to_write=python_written / 'rates.txt',
    gloss=rates_table,
    var_list_name='rates_table'
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / 'params.csv',
    cite_dict=cite_dict
)

write_python_from_gloss(
    path_to_write= python_written / 'params.txt',
    gloss=params_table,
    var_list_name='params_table'
)

# extract_params_from_model(
#     model=get_model(),
#     path_to_write=model_info / 'test.csv'
# )

derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info / 'derived_params.csv')

write_python_from_gloss(
    path_to_write= python_written / 'derived_params.txt',
    gloss=derived_params_table,
    var_list_name='derived_params_table'
)

# write_odes_from_model(
#     path_to_write= python_written / 'odes.txt',
#     model=get_model(),
# )

###### Variables for ease of access ######

def remove_math(
    df,
    query_result,
    query_column = 'Paper Abbr.',
    answer_column = 'Common Abbr.'
):
    res = df[df[query_column] == query_result][answer_column].values[0]

    for i in range(df.loc[df[query_column] == query_result, answer_column].iloc[0].count('$')):
        res = res.replace('$', '')

    return res

# -- Compounds --

PQ = remove_math(comps_table, r'$\mathrm{PQ}_\mathrm{ox}$')
PC_ox = remove_math(comps_table, r'$\mathrm{PC}_\mathrm{ox}$')
Fd_ox = remove_math(comps_table, r'$\mathrm{Fd}_\mathrm{ox}$')
ATP_st = remove_math(comps_table, r'$\mathrm{ATP}$')
NADPH_st = remove_math(comps_table, r'$\mathrm{NADPH}$')
H_lu = remove_math(comps_table, r'$\mathrm{H}^+$')
LHC = remove_math(comps_table, r'$\mathrm{LHC}$')
psbS = remove_math(comps_table, r'$\mathrm{Psbs}$')
Vx = remove_math(comps_table, r'$\mathrm{Vx}$')
PGA = remove_math(comps_table, r'$\mathrm{PGA}$')
BPGA = remove_math(comps_table, r'$\mathrm{BPGA}$')
GAP = remove_math(comps_table, r'$\mathrm{GAP}$')
DHAP = remove_math(comps_table, r'$\mathrm{DHAP}$')
FBP = remove_math(comps_table, r'$\mathrm{FBP}$')
F6P = remove_math(comps_table, r'$\mathrm{F6P}$')
G6P = remove_math(comps_table, r'$\mathrm{G6P}$')
G1P = remove_math(comps_table, r'$\mathrm{G1P}$')
SBP = remove_math(comps_table, r'$\mathrm{SBP}$')
S7P = remove_math(comps_table, r'$\mathrm{S7P}$')
E4P = remove_math(comps_table, r'$\mathrm{E4P}$')
X5P = remove_math(comps_table, r'$\mathrm{X5P}$')
R5P = remove_math(comps_table, r'$\mathrm{R5P}$')
RUBP = remove_math(comps_table, r'$\mathrm{RUBP}$')
RU5P = remove_math(comps_table, r'$\mathrm{RU5P}$')
MDA = remove_math(comps_table, r'$\mathrm{MDA}$')
H2O2 = remove_math(comps_table, r'$\mathrm{H_2O_2}$')
DHA = remove_math(comps_table, r'$\mathrm{DHA}$')
GSSG = remove_math(comps_table, r'$\mathrm{GSSG}$')
Trx_ox = remove_math(comps_table, r'$\mathrm{Trx_{ox}}$')
E_CBB_inactive = remove_math(comps_table, r'$\mathrm{E}_\mathrm{inactive}$')

# -- Derived Compounds --

PQH_2 = remove_math(derived_comps_table, r'$\mathrm{PQH}_2$')
PC_red = remove_math(derived_comps_table, r'$\mathrm{PC}^-$')
Fd_red = remove_math(derived_comps_table, r'$\mathrm{Fd}^-$')
ADP_st = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
NADP = remove_math(derived_comps_table, r'$\mathrm{NADP}^+$')
Pi_st = remove_math(derived_comps_table, r'$\mathrm{P}_\mathrm{i}$')
IF_3P = remove_math(derived_comps_table, r'$\mathrm{N}$')
Zx = remove_math(derived_comps_table, r'$\mathrm{Zx}$')
PsbSP = remove_math(derived_comps_table, r'$\mathrm{PsbS^P}$')
psIIcross = remove_math(derived_comps_table, r'$\mathrm{PSII_{cross}}$')
B_0 = remove_math(derived_comps_table, r'$\mathrm{B_0}$')
B_1 = remove_math(derived_comps_table, r'$\mathrm{B_1}$')
B_2 = remove_math(derived_comps_table, r'$\mathrm{B_2}$')
B_3 = remove_math(derived_comps_table, r'$\mathrm{B_3}$')
Q = remove_math(derived_comps_table, r'$\mathrm{Q}$')
PSI_sta = remove_math(derived_comps_table, r'$\mathrm{PSII_{sta}}$')

# -- Rates --

v_PSII = remove_math(rates_table, r'$v_{\mathrm{PSII}}$')
v_b6f = remove_math(rates_table, r'$v_{\mathrm{b6f}}$')
v_FNR = remove_math(rates_table, r'$v_{\mathrm{FNR}}$')
v_FQR = remove_math(rates_table, r'$v_{\mathrm{FQR}}$')
v_ATPsynth = remove_math(rates_table, r'$v_{\mathrm{ATPsynthase}}$')
v_Leak = remove_math(rates_table, r'$v_{\mathrm{Leak}}$')
v_PQ = remove_math(rates_table, r'$v_{\mathrm{PTOX}}$')
v_NDH = remove_math(rates_table, r'$v_{\mathrm{NDH}}$')
v_Cyc = remove_math(rates_table, r'$v_{\mathrm{Cyc}}$')
v_St21 = remove_math(rates_table, r'$v_{\mathrm{St12}}$')
v_St12 = remove_math(rates_table, r'$v_{\mathrm{St21}}$')
v_Deepox = remove_math(rates_table, r'$v_{\mathrm{Deepox}}$')
v_Epox = remove_math(rates_table, r'$v_{\mathrm{Epox}}$')
v_PsbSP = remove_math(rates_table, r'$v_{\mathrm{LHCprotonation}}$')
v_psbSD = remove_math(rates_table, r'$v_{\mathrm{LHCdeprotonation}}$')
v_rubisco = remove_math(rates_table, r'$v_{\mathrm{RuBisCo}}$')
v_FBPase = remove_math(rates_table, r'$v_{\mathrm{FBPase}}$')
v_SBPase = remove_math(rates_table, r'$v_9$')
v_PRKase = remove_math(rates_table, r'$v_{13}$')
v_pga_ex = remove_math(rates_table, r'$v_{pga}$')
v_dhap_ex = remove_math(rates_table, r'$v_{DHAP}$')
v_gap_ex = remove_math(rates_table, r'$v_{gap}$')
v_starch = remove_math(rates_table, r'$v_{\mathrm{Starch}}$')
v_PGK1ase = remove_math(rates_table, r'$v_{\mathrm{PGA\_kinase}}$')
v_BPGAdehynase = remove_math(rates_table, r'$v_{\mathrm{BPGA\_dehydrogenase}}$')
v_TPIase = remove_math(rates_table, r'$v_{\mathrm{TPI}}$')
v_Aldolase_FBP = remove_math(rates_table, r'$v_{\mathrm{Aldolase}}$')
v_TKase_E4P = remove_math(rates_table, r'$v_{\mathrm{F6P\_ Transketolase}}$')
v_Aldolase_SBP = remove_math(rates_table, r'$v_{8}$')
v_TKase_R5P = remove_math(rates_table, r'$v_{10}$')
v_Rpiase = remove_math(rates_table, r'$v_{11}$')
v_RPEase = remove_math(rates_table, r'$v_{12}$')
v_PGIase = remove_math(rates_table, r'$v_{G6P\_ isomerase}$')
v_PGMase = remove_math(rates_table, r'$v_{\mathrm{Phosphoglucomutase}}$')
v_PSI = remove_math(rates_table, r'$v_{\mathrm{PSI}}$')
v_ATPcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ ATP}}$')
v_NADPHcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ NADPH}}$')
v_Fdred = remove_math(rates_table, r'$v_{\mathrm{Fd,\ red}}$')
v_FdTrReduc = remove_math(rates_table, r'$v_{\mathrm{FdTrReductase}}$')
v_MDAreduc = remove_math(rates_table, r'$v_{\mathrm{MDAreduct}}$')
v_GR = remove_math(rates_table, r'$v_{\mathrm{GR}}$')
v_RuBisCO = remove_math(rates_table, r'$v_{\mathrm{RuBisCO}}$')
v_APXase = remove_math(rates_table, r'$v_{\mathrm{Ascorbate}}$')
v_Mehler = remove_math(rates_table, r'$v_{\mathrm{Mehler}}$')
v_DHAR = remove_math(rates_table, r'$v_{\mathrm{DHAR}}$')
v_3ASC = remove_math(rates_table, r'$v_{\mathrm{3ASC}}$')
v_Eact = remove_math(rates_table, r'$v_{\mathrm{Eact}}$')
v_Einact = remove_math(rates_table, r'$v_{\mathrm{Einact}}$')

# -- Parameters --

convf = remove_math(params_table, r'$\mathrm{convf}$')
PSII_tot = remove_math(params_table, r'$\mathrm{PSII}^{\mathrm{tot}}$')
PSI_tot = remove_math(params_table, r'$\mathrm{PSI}^{\mathrm{tot}}$')
PQ_tot = remove_math(params_table, r'$\mathrm{PQ}^{\mathrm{tot}}$')
PC_tot = remove_math(params_table, r'$\mathrm{PC}^{\mathrm{tot}}$')
Fd_tot = remove_math(params_table, r'$\mathrm{Fd}^{\mathrm{tot}}$')
NADP_tot = remove_math(params_table, r'$\mathrm{NADP}^{\mathrm{tot}}$')
AP_tot = remove_math(params_table, r'$\mathrm{AP}^{\mathrm{tot}}$')
PsbS_tot = remove_math(params_table, r'$\mathrm{PsbS}^{\mathrm{tot}}$')
X_tot = remove_math(params_table, r'$\mathrm{X}^{\mathrm{tot}}$')
k_H = remove_math(params_table, r'$k_H$')
kH0 = remove_math(params_table, r'$k_{H_0}$')
k_F = remove_math(params_table, r'$k_F$')
k2 = remove_math(params_table, r'$k_2$')
k_Stt7 = remove_math(params_table, r'$k_\mathrm{Stt7}$')
k_Pph1 = remove_math(params_table, r'$k_\mathrm{Pph1}$')
KM_ST = remove_math(params_table, r'$K_{\mathrm{M}_\mathrm{ST}}$')
n_ST = remove_math(params_table, r'$n_\mathrm{ST}$')
sigma0_I = remove_math(params_table, r'$\sigma _\mathrm{I} ^0$')
sigma0_II = remove_math(params_table, r'$\sigma _\mathrm{II} ^0$')
k_ATPsynth = remove_math(params_table, r'$k_\mathrm{ATPsynthase}$')
Pi_mol = remove_math(params_table, r'$\mathrm{Pi}_\mathrm{mol}$')
DeltaG0_ATP = remove_math(params_table, r'$\Delta G_{0_{ATP}}$')
HPR = remove_math(params_table, r'$\mathrm{HPR}$')
pH_stroma = remove_math(params_table, r'$\mathrm{pH}_\mathrm{stroma}$')
k_Leak = remove_math(params_table, r'$k_\mathrm{leak}$')
b_H = remove_math(params_table, r'$b_\mathrm{H}$')
k_PQred = remove_math(params_table, r'$k_{\mathrm{PQ}_\mathrm{red}}$')
k_Cytb6f = remove_math(params_table, r'$k_\mathrm{Cytb6f}$')
k_PTOX = remove_math(params_table, r'$k_\mathrm{PTOX}$')
k_PCox = remove_math(params_table, r'$k_\mathrm{PCox}$')
k_Fdred = remove_math(params_table, r'$k_{\mathrm{Fd}_\mathrm{red}}$')
kcat_FNR = remove_math(params_table, r'$k_{\mathrm{cat}_\mathrm{FNR}}$')
k_cyc = remove_math(params_table, r'$k_\mathrm{cyc}$')
O2_ext = remove_math(params_table, r'$\mathrm{O}_2^\mathrm{ex}$')
k_NDH = remove_math(params_table, r'$k_\mathrm{NDH}$')
EFNR = remove_math(params_table, r'')
KM_FNR_F = remove_math(params_table, r'$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{F}}}$')
KM_FNR_N = remove_math(params_table, r'$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{N}}}$')
gamma_0 = remove_math(params_table, r'$\gamma_0$')
gamma_1 = remove_math(params_table, r'$\gamma_1$')
gamma_2 = remove_math(params_table, r'$\gamma_2$')
gamma_3 = remove_math(params_table, r'$\gamma_3$')
k_deprot = remove_math(params_table, r'$k_\mathrm{Deprotonation}$')
k_prot = remove_math(params_table, r'$k_\mathrm{Protonation}$')
K_pHSatLHC = remove_math(params_table, r'$K_\mathrm{pHSatLHC}$')
k_DV = remove_math(params_table, r'$k_\mathrm{DeepoxV}$')
k_EZ = remove_math(params_table, r'$k_\mathrm{EpoxZ}$')
K_pHSat = remove_math(params_table, r'$K_\mathrm{pHSat}$')
nh_x = remove_math(params_table, r'$\mathrm{k}_{\mathrm{Hill}_\mathrm{X}}$')
nh_PsbS = remove_math(params_table, r'$\mathrm{k}_{\mathrm{Hill}_\mathrm{L}}$')
K_ZSat = remove_math(params_table, r'$K_\mathrm{ZSat}$')
E0_QA = remove_math(params_table, r'$E^0\mathrm{(QA/QA^-)}$')
E0_PQ = remove_math(params_table, r'$E^0\mathrm{(PQ/PQH_2)}$')
E0_PC = remove_math(params_table, r'$E^0\mathrm{(PC/PC^-)}$')
E0_P700 = remove_math(params_table, r'$E^0\mathrm{(P_{700}^+/P_{700})}$')
E0_FA = remove_math(params_table, r'$E^0\mathrm{(FA/FA^-)}$')
E0_Fd = remove_math(params_table, r'$E^0\mathrm{(Fd/Fd^-)}$')
E0_NADP = remove_math(params_table, r'$E^0\mathrm{(NADP^+/NADPH)}$')
F = remove_math(params_table, r'$F$')
R = remove_math(params_table, r'$R$')
T = remove_math(params_table, r'$T$')
pfd = remove_math(params_table, r'$\mathrm{PFD}$')
Ton = remove_math(params_table, r'$t_{\mathrm{anoxia}}^\mathrm{on}$')
Toff = remove_math(params_table, r'$t_{\mathrm{anoxia}}^\mathrm{off}$')
ox = remove_math(params_table, r'$\mathrm{ox}$')
CO2 = remove_math(params_table, r'$\mathrm{CO}_2$')
P_tot = remove_math(params_table, r'$\mathrm{P}^{\mathrm{tot}}$')
Pext = remove_math(params_table, r'$\mathrm{P}_\mathrm{ext}$')
V_maxbase_rubisco = remove_math(params_table, r'$V_{1_{\mathrm{base}}}$')
V_maxbase_fbpase = remove_math(params_table, r'$V_{6_{\mathrm{base}}}$')
V_maxbase_sbpase = remove_math(params_table, r'$V_{9_{\mathrm{base}}}$')
V_maxbase_prkase = remove_math(params_table, r'$V_{13_{\mathrm{base}}}$')
V_maxbase_starch = remove_math(params_table, r'$V_{\mathrm{st}_{\mathrm{base}}}$')
Vmax_ex = remove_math(params_table, r'$V_{\mathrm{ex}}$')
K_PGK1ase = remove_math(params_table, r'$q_2$')
K_BPGAdehynase = remove_math(params_table, r'$q_3$')
K_TPIase = remove_math(params_table, r'$q_4$')
K_Aldolase_FBP = remove_math(params_table, r'$q_5$')
K_TKase_E4P = remove_math(params_table, r'$q_7$')
K_Aldolase_SBP = remove_math(params_table, r'$q_8$')
K_TKase_R5P = remove_math(params_table, r'$q_{10}$')
K_Rpiase = remove_math(params_table, r'$q_{11}$')
K_RPEase = remove_math(params_table, r'$q_{12}$')
K_PGIase = remove_math(params_table, r'$q_{14}$')
K_PGMase = remove_math(params_table, r'$q_{15}$')
Km_RuBisCO_RUBP = remove_math(params_table, r'$K_{\mathrm{m}1}$')
Km_RuBisCO_CO2 = remove_math(params_table, r'$K_{\mathrm{mCO2}}$')
Km_FBPase = remove_math(params_table, r'$K_{\mathrm{m}6}$')
Km_SBPase = remove_math(params_table, r'$K_{\mathrm{m}9}$')
Km_PRKase_RU5P = remove_math(params_table, r'$K_{\mathrm{m}131}$')
Km_PRKase_ATP = remove_math(params_table, r'$K_{\mathrm{m}132}$')
Km_Starch_G1P = remove_math(params_table, r'$K_{\mathrm{mst}1}$')
Km_Starch_ATP = remove_math(params_table, r'$K_{\mathrm{mst}2}$')
K_diss_PGA = remove_math(params_table, r'$K_{\mathrm{pga}}$')
K_diss_GAP = remove_math(params_table, r'$K_{\mathrm{gap}}$')
K_diss_DHAP = remove_math(params_table, r'$K_{\mathrm{dhap}}$')
K_diss_Pi = remove_math(params_table, r'$K_{\mathrm{pi}}$')
K_diss_Pext = remove_math(params_table, r'$K_{\mathrm{pxt}}$')
Ki_RuBisCO_PGA = remove_math(params_table, r'$K_{\mathrm{i}11}$')
Ki_RuBisCO_FBP = remove_math(params_table, r'$K_{\mathrm{i}12}$')
Ki_RuBisCO_SBP = remove_math(params_table, r'$K_{\mathrm{i}13}$')
Ki_RuBisCO_Pi = remove_math(params_table, r'$K_{\mathrm{i}14}$')
Ki_RuBisCO_NADPH = remove_math(params_table, r'$K_{\mathrm{i}15}$')
Ki_FBPase_F6P = remove_math(params_table, r'$K_{\mathrm{i}61}$')
Ki_FBPase_Pi = remove_math(params_table, r'$K_{\mathrm{i}62}$')
Ki_SBPase_Pi = remove_math(params_table, r'$K_{\mathrm{i}9}$')
Ki_PRKase_PGA = remove_math(params_table, r'$K_{\mathrm{i}131}$')
Ki_PRKase_RuBP = remove_math(params_table, r'$K_{\mathrm{i}132}$')
Ki_PRKase_Pi = remove_math(params_table, r'$K_{\mathrm{i}133}$')
Kiunc_PRKase_ADP = remove_math(params_table, r'$K_{\mathrm{i}134}$')
Kicom_PRKase_ADP = remove_math(params_table, r'$K_{\mathrm{i}135}$')
Ki_Starch_ADP = remove_math(params_table, r'$K_{\mathrm{ist}}$')
Kact_Starch_PGA = remove_math(params_table, r'$K_{\mathrm{ast1}}$')
Kact_Starch_F6P = remove_math(params_table, r'$K_{\mathrm{ast2}}$')
Kact_Starch_FBP = remove_math(params_table, r'$K_{\mathrm{ast3}}$')
k_fast = remove_math(params_table, r'$k$')
k_f1 = remove_math(params_table, r'$kf1$')
k_r1 = remove_math(params_table, r'$kr1$')
k_f2 = remove_math(params_table, r'$kf2$')
k_r2 = remove_math(params_table, r'$kr2$')
k_f3 = remove_math(params_table, r'$kf3$')
k_f4 = remove_math(params_table, r'$kf4$')
k_r4 = remove_math(params_table, r'$kr4$')
k_f5 = remove_math(params_table, r'$kf5$')
XT = remove_math(params_table, r'$XT$')
k_Mehler = remove_math(params_table, r'$k_{\mathrm{Mehler}}$')
kcat_GR = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{GR}}}$')
kcat_DHAR = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{DHAR}}}$')
k3 = remove_math(params_table, r'$k3$')
Km_NADPH = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{NADPH}}}$')
Km_GSSG = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{GSSG}}}$')
Km_DHA = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{DHA}}}$')
Km_GSH = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{GSH}}}$')
K_DHAR = remove_math(params_table, r'$K$')
GR_0 = remove_math(params_table, r'$\mathrm{GR}_0$')
DHAR_0 = remove_math(params_table, r'$\mathrm{DHAR}_0$')
Glutathion_total = remove_math(params_table, r'$\mathrm{Gluthation}_{\mathrm{total}}$')
Ascorbate_total = remove_math(params_table, r'$\mathrm{Ascorbate}_{\mathrm{total}}$')
kcat_MDAR = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{MDAR}}}$')
Km_MDAR_NADPH = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{MDAR-NADPH}}}$')
Km_MDAR_MDA = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{MDAR-MDA}}}$')
MDAR_0 = remove_math(params_table, r'$\mathrm{MDAR}_0$')
k_ex_atp = remove_math(params_table, r'$k_{\mathrm{ex}_{\mathrm{atp}}}$')
k_ex_nadph = remove_math(params_table, r'$k_{\mathrm{ex}_{\mathrm{nadph}}}$')
thioredoxin_tot = remove_math(params_table, r'$\mathrm{thioredoxin}_\mathrm{tot}$')
e_cbb_tot = remove_math(params_table, r'$e_{\mathrm{cbb}_\mathrm{tot}}$')
k_fd_tr_reductase = remove_math(params_table, r'$k_{\mathrm{fd}_{\mathrm{tr}_\mathrm{reductase}}}$')
k_e_cbb_activation = remove_math(params_table, r'$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{activation}}}$')
k_e_cbb_relaxation = remove_math(params_table, r'$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{relaxation}}}$')

# --- Derived Parameters ---

K_QAPQ = remove_math(derived_params_table, r'$K_\mathrm{eq, QAPQ}$')
K_ATPsynthase = remove_math(derived_params_table, r'$K_\mathrm{eq, ATPsynthase}$')
K_cytb6f = remove_math(derived_params_table, r'$K_\mathrm{eq, cytb6f}$')
H_st = remove_math(derived_params_table, r'$\mathrm{H}_\mathrm{st}$')
K_FAFd = remove_math(derived_params_table, r'$K_\mathrm{eq, FAFd}$')
K_PCP700 = remove_math(derived_params_table, r'$K_\mathrm{eq, PCP700}$')
K_FNR = remove_math(derived_params_table, r'$K_\mathrm{eq, FNR}$')

###### Making README File ######

mdFile = MdUtils(file_name=f'{os.path.dirname(__file__)}/README.md')

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

                     """)

mdFile.new_header(2, 'Installation')

mdFile.new_header(2, 'Summary')

mdFile.new_header(3, 'Compounds')

mdFile.new_header(4, 'Part of ODE system')

mdFile.new_table(columns = len(comps_table.columns), rows = len(comps_table_tolist), text = comps_table_list)

mdFile.new_paragraph(fr"""
<details>
<summary>ODE System</summary>

```math
   \begin{{align}}
      {ode(PQ)} &= -{v_PSII} + {v_PQ} - {v_NDH} + {v_b6f} - {v_Cyc} \\
      {ode(H_lu)} &= \frac{{1}}{b_H} \cdot \left(  2 \cdot {v_PSII} + 4 \cdot {v_b6f} - {v_Leak} - {HPR} \cdot {v_ATPsynth} \right) \\
      {ode(Fd_ox)} &= 2 \cdot {v_Cyc} + 2 \cdot {v_FNR} - {v_Fdred} + {v_FdTrReduc} \\
      {ode(PC_ox)} &= -2 \cdot {v_b6f} + {v_PSI} \\
      {ode(NADPH_st)} &= {convf} \cdot {v_FNR} - {v_BPGAdehynase} - {v_MDAreduc} - {v_GR} - {v_NADPHcons} \\
      {ode(LHC)} &= -{v_St21} + {v_St12} \\
      {ode(ATP_st)} &= {convf} \cdot {v_ATPsynth} - {v_PGK1ase} - {v_PRKase} - {v_starch} - {v_ATPcons} \\
      {ode(Vx)} &= -{v_Deepox} + {v_Epox} \\
      {ode(psbS)} &= -{v_PsbSP} + {v_psbSD} \\
      {ode(RUBP)} &= -{v_RuBisCO} + {v_PRKase} \\
      {ode(PGA)} &= 2 \cdot {v_RuBisCO} - {v_PGK1ase} - {v_pga_ex} \\
      {ode(BPGA)} &= {v_PGK1ase} - {v_BPGAdehynase} \\
      {ode(GAP)} &= {v_BPGAdehynase} - {v_TPIase} - {v_Aldolase_FBP} - {v_TKase_E4P} - {v_TKase_R5P} - {v_gap_ex} \\
      {ode(DHAP)} &= {v_TPIase} - {v_Aldolase_FBP} - {v_Aldolase_SBP} - {v_dhap_ex} \\
      {ode(FBP)} &= {v_Aldolase_FBP} - {v_FBPase} \\
      {ode(F6P)} &= {v_FBPase} - {v_TKase_E4P} - {v_PGIase} \\
      {ode(X5P)} &= {v_TKase_E4P} + {v_TKase_R5P} - {v_RPEase} \\
      {ode(E4P)} &= {v_TKase_E4P} - {v_Aldolase_SBP} \\
      {ode(SBP)} &= {v_Aldolase_SBP} - {v_SBPase} \\
      {ode(S7P)} &= {v_SBPase} - {v_TKase_R5P} \\
      {ode(R5P)} &= {v_TKase_R5P} - {v_Rpiase} \\
      {ode(RU5P)} &= {v_Rpiase} + {v_RPEase} - {v_PRKase} \\
      {ode(G6P)} &= {v_PGIase} - {v_PGMase} \\
      {ode(G1P)} &= {v_PGMase} - {v_starch} \\
      {ode(H2O2)} &= -{v_APXase} + 0.032 \cdot {v_Mehler} \\
      {ode(MDA)} &= 2 \cdot {v_APXase} - 2 \cdot {v_MDAreduc} - 2 \cdot {v_3ASC} \\
      {ode(GSSG)} &= -{v_GR} + {v_DHAR} \\
      {ode(DHA)} &= -{v_DHAR} + {v_3ASC} \\
      {ode(Trx_ox)} &= -{v_FdTrReduc} + 5 \cdot {v_Eact} \\
      {ode(E_CBB_inactive)} &= -5 \cdot {v_Eact} + 5 \cdot {v_Einact} \\
   \end{{align}}
```

</details>
                     """)

mdFile.new_header(4, 'Conserved quantities')

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
    \begin{{align}}
        {PQH_2} &= {PQ_tot} - {PQ} \\
        {PC_red} &= {PC_tot} - {PC_ox} \\
        {Fd_red} &= {Fd_tot} - {Fd_ox} \\
        {ADP_st} &= {AP_tot} - {ATP_st} \\
        {NADP} &= {NADP_tot} - {NADPH_st} \\
        {Pi_st} &= {P_tot} - \left({PGA} + 2 \cdot {BPGA} + {GAP} + {DHAP} + 2 \cdot {FBP} + {F6P} + {G6P} + {G1P} + 2 \cdot {SBP} + {S7P} + {E4P} + {X5P} + {R5P} + 2 \cdot {RUBP} + {RU5P} + {ATP_st} \right) \\
        {psIIcross} &= {sigma0_II} + (1 - {sigma0_II} - {sigma0_I}) \cdot {LHC} \\
        {Q} &= {gamma_0} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {psbS} + {gamma_1} \cdot \left( 1 - \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \right) \cdot {PsbSP} + {gamma_2} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {PsbSP} + {gamma_3} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}} \cdot {psbS} \\
        {PSI_sta} &= \frac{{{PSI_tot}}}{{1 + \frac{{(1 - {psIIcross}) \cdot {pfd}}}{{{k_Fdred} \cdot {Fd_ox}}} + \frac{{1 + {Fd_red}}}{{{K_FAFd} \cdot {Fd_ox}}} \cdot \left( \frac{{{PC_ox}}}{{{K_PCP700} \cdot {PC_red}}} + \frac{{(1 - {psIIcross}) \cdot {pfd}}}{{{k_PCox} \cdot {PC_red}}} \right)}}
    \end{{align}}
```

</details>

<details>
<summary> Quasi-steady state approximation used to calculate the rate of PSII </summary>

```math
    \begin{{align}}
        - \left( {psIIcross} \cdot {pfd} + \frac{{{k_PQred}}}{{{K_QAPQ}}} \cdot {PQH_2} \right) \cdot {B_0} + \left( {kH0} + {k_H} \cdot {Q} + {k_F} \right) \cdot {B_1} + {k_PQred} \cdot {PQ} \cdot {B_2} &= 0 \\
        {psIIcross} \cdot {pfd} \cdot {B_0} - \left( {kH0} + {k_H} \cdot {Q} + {k_F} + {k2} \right) \cdot {B_1} &= 0 \\
        {psIIcross} \cdot {pfd} \cdot {B_2} - \left( {kH0} + {k_H} \cdot {Q} + {k_F}\right) \cdot {B_3} &= 0 \\
        {B_0} + {B_1} + {B_2} + {B_3} &= {PSII_tot}
    \end{{align}}
```

</details>

                     """)

mdFile.new_header(3, 'Parameters')

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, 'Derived Parameters')

mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Equations of derived parameters</summary>

```math
    \begin{{align}}
        {K_QAPQ} = \mathrm{{exp}}\left( \frac{{-2 \cdot -{E0_QA} \cdot {F} + -2 \cdot {E0_PQ} \cdot {F} + 2 \cdot {pH_stroma} \cdot \ln 10 \cdot {R} \cdot {T}}}{{{R} \cdot {T}}}\right) \\
        {K_FAFd} = \mathrm{{exp}}\left( \frac{{{E0_FA} \cdot {F} - {E0_Fd} \cdot {F}}}{{{R} \cdot {T}}} \right) \\
        {K_PCP700} = \mathrm{{exp}}\left( \frac{{{E0_PC} \cdot {F} - {E0_P700} \cdot {F}}}{{{R} \cdot {T}}} \right) \\
        {K_QAPQ} = \mathrm{{exp}}\left( \frac{{-2 \cdot -{E0_Fd} \cdot {F} + -2 \cdot {E0_NADP} \cdot {F} + {pH_stroma} \cdot \ln 10 \cdot {R} \cdot {T}}}{{{R} \cdot {T}}}\right) \\
    \end{{align}}
```

</details>

                     """)

mdFile.new_header(3, 'Reaction Rates')

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

# mdFile.new_paragraph(fr"""

# <details>
# <summary>Rate equations</summary>

# ```math
#     \begin{{align}}
#         {v_PSII} &= 0.5 \cdot {k2} \cdot {B_1} \\
#         {v_PSI} &= \left( 1 - {psIIcross} \right) \cdot {pfd} \cdot {PSI_sta} \\
#         {v_b6f} &= \mathrm{{max}}\left( {k_Cytb6f} \cdot \frac{{{PQH_2} \cdot {PC_ox}^2 - \left( {PQ} \cdot {PC_red}^2 \right)}}{{{K_cytb6f}}}, - {k_Cytb6f} \right) \\
#         {v_FNR} &= {EFNR} \cdot {kcat_FNR} \cdot \frac{{\left(\frac{{{Fd_red}}}{{{KM_FNR_F}}}\right)^2 \cdot \frac{{{NADP}}}{{{convf} \cdot {KM_FNR_N}}} - \frac{{ \left( \frac{{{Fd_ox}}}{{{KM_FNR_F}}} \right)^2 \cdot \frac{{{NADPH_st}}}{{{convf} \cdot {KM_FNR_N}}} }}{{{K_FNR}}} }}{{\left( 1 + \frac{{{Fd_red}}}{{{KM_FNR_F}}} + \left(\frac{{{Fd_red}}}{{{KM_FNR_F}}}\right)^2 \right) \cdot \left( 1 + \frac{{{NADP}}}{{{convf} \cdot {KM_FNR_N}}} \right) + \left( 1 + \frac{{{Fd_ox}}}{{{KM_FNR_F}}} + \left(\frac{{{Fd_ox}}}{{{KM_FNR_F}}}\right)^2 \right) \cdot \left( 1 + \frac{{{NADPH_st}}}{{{convf} \cdot {KM_FNR_N}}} \right) - 1}} \\

#     \end{{align}}
# ```

# </details>

#                      """)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
   \begin{{align}}
       {vPS2} &=  0.5 {k2} \cdot {B1} \\
       {vPS1} &=  \left( 1 - {ps2cs} \right) {pfd} {A0} \\
       {vPTOX} &=  {PQred} \cdot {k_PTOX} \cdot \mathrm{{oxygen}} \left( {time}, {ox}, {O2_ext}, {k_NDH}, {Ton}, {Toff} \right)_{{0}} \\
       {vNDH} &=  \mathrm{{oxygen}} \left( {time}, {ox}, {O2_ext}, {k_NDH}, {Ton}, {Toff} \right)_{{1}} {PQ} \\
       {vB6f} &=  \mathrm{{np}}.\mathrm{{maximum}} \left( {k_Cytb6f} \cdot \left( {PQred} \cdot {PC}^{{2}} - \frac{{{PQ} \cdot {PCred}^{{2}}}}{{{Keq_B6f}}} \right), -{k_Cytb6f} \right) \\
       {vCyc} &=  {k_cyc} \cdot {Fdred}^{{2}} \cdot {PQ} \\
       {vFNR} &=  \frac{{{EFNR} \cdot {kcat_FNR} \cdot \left( \frac{{{Fdred}}}{{{KM_FNR_F}}} ^{{2}} \cdot \frac{{\frac{{{NADP}}}{{{convf}}}}}{{{KM_FNR_N}}}  - \frac{{\frac{{{Fd}}}{{{KM_FNR_F}}} ^{{2}} \cdot \frac{{\frac{{{NADPH}}}{{{convf}}}}}{{{KM_FNR_N}}} }}{{{Keq_FNR}}} \right)}}{{\left( 1 + \frac{{{Fdred}}}{{{KM_FNR_F}}}  + \frac{{{Fdred}}}{{{KM_FNR_F}}} ^{{2}} \right) \left( 1 + \frac{{\frac{{{NADP}}}{{{convf}}}}}{{{KM_FNR_N}}}  \right) + \left( 1 + \frac{{{Fd}}}{{{KM_FNR_F}}}  + \frac{{{Fd}}}{{{KM_FNR_F}}} ^{{2}} \right) \left( 1 + \frac{{\frac{{{NADPH}}}{{{convf}}}}}{{{KM_FNR_N}}}  \right) - 1}} \\
       {vLeak} &=  {k_Leak} \cdot \left( {H} - \mathrm{{calculate\_p{H}inv}} \left( \mathrm{{p{H}\_stroma}} \right) \right) \\
       {vSt12} &=  {k_Stt7} \cdot \frac{{1}}{{1 + \left( \frac{{\frac{{{PQ}}}{{{PQ_tot}}}}}{{{KM_ST}}} \right)^{{{n_ST}}}}}  \cdot {LHC} \\
       {vSt21} &=  {k_Pph1} \cdot {LHCp} \\
       {vATPsynthase} &=  {k_ATPsynth} \cdot \left( \frac{{{ADP}}}{{{convf}}} - \frac{{\frac{{{ATP}}}{{{convf}}}}}{{{Keq_ATPsynthase}}} \right) \\
       {vDeepox} &=  {k_DV} \cdot \frac{{{H}^{{\mathrm{{n{H}}}}}}}{{{H}^{{\mathrm{{n{H}}}}} + \left( \mathrm{{calculate\_p{H}inv}} \left( \mathrm{{K\_p{H}Sat}} \right) \right)^{{\mathrm{{n{H}}}}}}} {Vx} \\
       {vEpox} &=  {k_EZ} \cdot {Zx} \\
       {vLhcprotonation} &=  {k_prot} \cdot \frac{{{H}^{{\mathrm{{n{H}}}}}}}{{{H}^{{\mathrm{{n{H}}}}} + \left( \mathrm{{calculate\_p{H}inv}} \left( \mathrm{{K\_p{H}SatL{H}C}} \right) \right)^{{\mathrm{{n{H}}}}}}} {Psbs} \\
       {vLhcdeprotonation} &=  {k_deprot} \cdot {Psbsp} \\
       {vRuBisCO} &=  \frac{{{V1} \cdot {RUB{Pi}} \cdot {CO2}}}{{\left( {RUB{Pi}} + \mathrm{{Km\_RuBisCO\_RUB{Pi}}} \cdot \left( 1 + \frac{{{{Pi}GA}}}{{\mathrm{{Ki\_RuBisCO\_{Pi}GA}}}} + \frac{{{FB{Pi}}}}{{\mathrm{{Ki\_RuBisCO\_FB{Pi}}}}} + \frac{{{SB{Pi}}}}{{\mathrm{{Ki\_RuBisCO\_SB{Pi}}}}} + \frac{{{Pi}}}{{\mathrm{{Ki\_RuBisCO\_{Pi}i}}}} + \frac{{\mathrm{{NAD{Pi}H}}}}{{\mathrm{{Ki\_RuBisCO\_NAD{Pi}H}}}} \right) \right) \left( {CO2} + {Km_RuBisCO_CO2} \right)}} \\
       {vPGA_kinase} &=  {k_fast} \cdot \left( {ATP} \cdot {PGA} - \frac{{{BPGA} \cdot {ADP}}}{{{K_PGK1ase}}} \right) \\
       {vBPGA_dehydrogenase} &=  {k_fast} \cdot \left( {BPGA} \cdot {NADPH} \cdot {H_stroma} - \frac{{{GAP} \cdot {NADP} \cdot {Pi}}}{{{K_BPGAdehynase}}} \right) \\
       {vTPI} &=  {k_fast} \cdot \left( {GAP} - \frac{{{DHAP}}}{{{K_TPIase}}} \right) \\
       {vAldolase} &=  {k_fast} \cdot \left( {GAP} \cdot {DHAP} - \frac{{{FBP}}}{{{K_Aldolase_FBP}}} \right) \\
       {vFBPase} &=  \frac{{{V6} \cdot {FB{Pi}}}}{{{FB{Pi}} + \mathrm{{Km\_FB{Pi}ase}} \cdot \left( 1 + \frac{{{F6{Pi}}}}{{\mathrm{{Ki\_FB{Pi}ase\_F6{Pi}}}}} + \frac{{{Pi}}}{{\mathrm{{Ki\_FB{Pi}ase\_{Pi}i}}}} \right)}} \\
       {vF6P_Transketolase} &=  {k_fast} \cdot \left( {GAP} \cdot {F6P} - \frac{{{X5P} \cdot {E4P}}}{{{K_TKase_E4P}}} \right) \\
       {v8} &=  {k_fast} \cdot \left( {DHAP} \cdot {E4P} - \frac{{{SBP}}}{{{K_Aldolase_SBP}}} \right) \\
       {v9} &=  \frac{{{V9} \cdot {SBP}}}{{{SBP} + {Km_SBPase} \cdot \left( 1 + \frac{{{Pi}}}{{{Ki_SBPase_Pi}}} \right)}} \\
       {v10} &=  {k_fast} \cdot \left( {GAP} \cdot {S7P} - \frac{{{X5P} \cdot {R5P}}}{{{K_TKase_R5P}}} \right) \\
       {v11} &=  {k_fast} \cdot \left( {R5P} - \frac{{{RU5P}}}{{{K_Rpiase}}} \right) \\
       {v12} &=  {k_fast} \cdot \left( {X5P} - \frac{{{RU5P}}}{{{K_RPEase}}} \right) \\
       {v13} &=  \frac{{{V13} \cdot {RU5{Pi}} \cdot {AT{Pi}}}}{{\left( {RU5{Pi}} + \mathrm{{Km\_{Pi}RKase\_RU5{Pi}}} \cdot \left( 1 + \frac{{{{Pi}GA}}}{{\mathrm{{Ki\_{Pi}RKase\_{Pi}GA}}}} + \frac{{{RUB{Pi}}}}{{\mathrm{{Ki\_{Pi}RKase\_RuB{Pi}}}}} + \frac{{{Pi}}}{{\mathrm{{Ki\_{Pi}RKase\_{Pi}i}}}} \right) \right) \left( {AT{Pi}} \cdot \left( 1 + \frac{{\mathrm{{AD{Pi}}}}}{{\mathrm{{Kiunc\_{Pi}RKase\_AD{Pi}}}}} \right) + \mathrm{{Km\_{Pi}RKase\_AT{Pi}}} \cdot \left( 1 + \frac{{\mathrm{{AD{Pi}}}}}{{\mathrm{{Kicom\_{Pi}RKase\_AD{Pi}}}}} \right) \right)}} \\
       {vG6P_isomerase} &=  {k_fast} \cdot \left( {F6P} - \frac{{{G6P}}}{{{K_PGIase}}} \right) \\
       {vPhosphoglucomutase} &=  {k_fast} \cdot \left( {G6P} - \frac{{{G1P}}}{{{K_PGMase}}} \right) \\
       {vpga} &=  \frac{{{Vmax_ex} \cdot {PGA}}}{{{N} {K_diss_PGA}}} \\
       {vgap} &=  \frac{{{Vmax_ex} \cdot {GAP}}}{{{N} {K_diss_GAP}}} \\
       {vdhap} &=  \frac{{{Vmax_ex} \cdot {DHAP}}}{{{N} {K_diss_DHAP}}} \\
       {vStarch} &=  \frac{{{Vst} \cdot {G1{Pi}} \cdot {AT{Pi}}}}{{\left( {G1{Pi}} + \mathrm{{Km\_Starch\_G1{Pi}}} \right) \left( \left( 1 + \frac{{{AD{Pi}}}}{{\mathrm{{Ki\_Starch\_AD{Pi}}}}} \right) \left( {AT{Pi}} + \mathrm{{Km\_Starch\_AT{Pi}}} \right) + \frac{{\mathrm{{Km\_Starch\_AT{Pi}}} \cdot {Pi}}}{{\mathrm{{Kact\_Starch\_{Pi}GA}} \cdot \mathrm{{{Pi}GA}} + \mathrm{{Kact\_Starch\_F6{Pi}}} \cdot \mathrm{{F6{Pi}}} + \mathrm{{Kact\_Starch\_FB{Pi}}} \cdot \mathrm{{FB{Pi}}}}} \right)}} \\
       {vFdred} &=  {kFdred} \cdot {Fd} \cdot {A1} - \frac{{{kFdred}}}{{{Keq_FAFd}}} \cdot {Fdred} \cdot {A2} \\
       {vAscorbate} &=  \frac{{{ASC} {H2O2} \cdot {XT} }}{{{ASC} {H2O2} \cdot \left( \frac{{1}}{{{kf3}}} + \frac{{1}}{{{kf5}}} \right) + \frac{{{ASC}}}{{{kf1}}} + \frac{{{H2O2}}}{{{kf4}}} + \frac{{{H2O2} \cdot {kr4}}}{{{kf4} \cdot {kf5}}} + \frac{{{H2O2}}}{{{kf2}}} + \frac{{{H2O2} \cdot {kr2}}}{{{kf2} \cdot {kf3}}} + \frac{{{kr1}}}{{{kf1} \cdot {kf2}}} + \frac{{{kr1} \cdot {kr2}}}{{{kf1} \cdot {kf2} \cdot {kf3}}} }} \\
       {vMDAreduct} &=  \frac{{{kcatMDAR} \cdot {MDAR0} \cdot {NADPH} \cdot {MDA} }}{{{KmMDAR_NADPH} \cdot {MDA} + {KmMDAR_MDA} \cdot {NADPH} + {NADPH} \cdot {MDA} + {KmMDAR_NADPH} \cdot {KmMDAR_MDA} }} \\
       {vMehler} &=  {A1} \cdot {kMehler} \cdot {O2ext} \\
       {vGR} &=  \frac{{{kcat_GR} \cdot {GR0} \cdot {NADPH} \cdot {GSSG} }}{{{KmNADPH} \cdot {GSSG} + {KmGSSG} \cdot {NADPH} + {NADPH} \cdot {GSSG} + {KmNADPH} \cdot {KmGSSG} }} \\
       {vDHAR} &=  \frac{{{kcat_DHAR} \cdot {DHAR0} \cdot {DHA} \cdot {GSH} }}{{{K} + {{K}mDHA} \cdot {GSH} + \mathrm{{{K}mGSH}} \cdot {DHA} + {DHA} \cdot {GSH} }} \\
       {v3ASC} &=  {k3} \cdot {MDA}^{{2}} \\
       {vEX_ATP} &=  {k_ex_atp} \cdot {ATP} \\
       {vEX_NADPH} &=  {k_ex_nadph} \cdot {NADPH} \\
       {vFdTrReductase} &=  {k_fd_tr_reductase} \cdot {TR_ox} \cdot {Fdred} \\
       {vE_activation} &=  {k_e_cbb_activation} \cdot {E_inactive} \cdot {TR_red} \\
       {vE_inactivation} &=  {k_e_cbb_relaxation} \cdot {E_active} \\
   \end{{align}}
```

</details>

                     """)

mdFile.new_header(3, 'Tags')

# mdFile.write(rf'''

# ```mermaid
# flowchart LR;
#     H("$${H}$$") -->|"$${v_PSII}$$"| P("$${PQH_2}$$");
#     P -->|"$${v_PQ}$$"| H;
#     H -->|"$${v_ATPsynth}$$"| A("$${ATP}$$");
#     A -->|"$${v_ATPcons}$$"| empty:::hidden;
#     H -->|"$${v_Leak}$$"| empty1:::hidden;
#     PS("$${PsbS}$$") -->|"$${v_PsbSP}$$"| e1:::hidden;
#     Vx("$${Vx}$$") -->|"$${v_Xcyc}$$"| e2:::hidden;
#     e3:::hidden -->|"$${v_ATPact}$$"| ATP("$${ATPase}$$")


#     classDef hidden display: none;
# ```

#              ''')

mdFile.create_md_file()
