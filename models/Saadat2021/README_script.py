from mdutils.mdutils import MdUtils  # noqa: E402
from pathlib import Path
from greensloth_utils import remove_math, gloss_fromCSV

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

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / 'comps.csv',
    omit_col='Glossary ID'
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(
    path=model_info / 'derived_comps.csv',
    omit_col='Glossary ID'
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / 'rates.csv',
    omit_col='Glossary ID'
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / 'params.csv',
    cite_dict=cite_dict
)

derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info / 'derived_params.csv')

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
TRX_ox = remove_math(comps_table, r'$\mathrm{Trx_{ox}}$')
E_CBB_inactive = remove_math(comps_table, r'$\mathrm{E}_\mathrm{inactive}$')

# -- Derived Compounds --

PQH_2 = remove_math(derived_comps_table, r'$\mathrm{PQH}_2$')
PC_red = remove_math(derived_comps_table, r'$\mathrm{PC}^-$')
Fd_red = remove_math(derived_comps_table, r'$\mathrm{Fd}^-$')
ADP_st = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
NADP_st = remove_math(derived_comps_table, r'$\mathrm{NADP}^+$')
LHCp = remove_math(derived_comps_table, r'$\mathrm{LHCp}$')
Zx = remove_math(derived_comps_table, r'$\mathrm{Zx}$')
PsbSP = remove_math(derived_comps_table, r'$\mathrm{PsbS^P}$')
psIIcross = remove_math(derived_comps_table, r'$\mathrm{PSII_{cross}}$')
Q = remove_math(derived_comps_table, r'$\mathrm{Q}$')
B0 = remove_math(derived_comps_table, r'$\mathrm{B_0}$')
B1 = remove_math(derived_comps_table, r'$\mathrm{B_1}$')
B2 = remove_math(derived_comps_table, r'$\mathrm{B_2}$')
B3 = remove_math(derived_comps_table, r'$\mathrm{B_3}$')
pH_lu = remove_math(derived_comps_table, r'$\mathrm{pH}_\mathrm{lumen}$')
Pi_st = remove_math(derived_comps_table, r'$\mathrm{P}_\mathrm{i}$')
IF_3P = remove_math(derived_comps_table, r'$\mathrm{N}$')
TRX_red = remove_math(derived_comps_table, r'$\mathrm{Trx_{red}}$')
E_CBB_active = remove_math(derived_comps_table, r'$\mathrm{E}_\mathrm{cbb,\ inactive}$')
ASC = remove_math(derived_comps_table, r'$\mathrm{ASC}$')
GSH = remove_math(derived_comps_table, r'$\mathrm{GSH}$')
Y0 = remove_math(derived_comps_table, r'$\mathrm{Y_0}$')
Y1 = remove_math(derived_comps_table, r'$\mathrm{Y_1}$')
Y2 = remove_math(derived_comps_table, r'$\mathrm{Y_2}$')
Fluo = remove_math(derived_comps_table, r'$\mathrm{Fluo}$')

# -- Rates --

v_PSII = remove_math(rates_table, r'$v_{\mathrm{PSII}}$')
v_PQ = remove_math(rates_table, r'$v_{\mathrm{PTOX}}$')
v_NDH = remove_math(rates_table, r'$v_{\mathrm{NDH}}$')
v_b6f = remove_math(rates_table, r'$v_{\mathrm{b6f}}$')
v_Cyc = remove_math(rates_table, r'$v_{\mathrm{Cyc}}$')
v_FNR = remove_math(rates_table, r'$v_{\mathrm{FNR}}$')
v_Leak = remove_math(rates_table, r'$v_{\mathrm{Leak}}$')
v_St21 = remove_math(rates_table, r'$v_{\mathrm{St12}}$')
v_St12 = remove_math(rates_table, r'$v_{\mathrm{St21}}$')
v_ATPsynth = remove_math(rates_table, r'$v_{\mathrm{ATPsynthase}}$')
v_Deepox = remove_math(rates_table, r'$v_{\mathrm{Deepox}}$')
v_Epox = remove_math(rates_table, r'$v_{\mathrm{Epox}}$')
v_PsbSP = remove_math(rates_table, r'$v_{\mathrm{LHCprotonation}}$')
v_PsbSD = remove_math(rates_table, r'$v_{\mathrm{LHCdeprotonation}}$')
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
v_pga_ex = remove_math(rates_table, r'$v_{pga}$')
v_gap_ex = remove_math(rates_table, r'$v_{gap}$')
v_dhap_ex = remove_math(rates_table, r'$v_{DHAP}$')
v_RuBisCO = remove_math(rates_table, r'$v_{\mathrm{RuBisCo}}$')
v_FBPase = remove_math(rates_table, r'$v_{\mathrm{FBPase}}$')
v_SBPase = remove_math(rates_table, r'$v_9$')
v_PRKase = remove_math(rates_table, r'$v_{13}$')
v_starch = remove_math(rates_table, r'$v_{\mathrm{Starch}}$')
v_FdTrReduc = remove_math(rates_table, r'$v_{\mathrm{FdTrReductase}}$')
v_Eact = remove_math(rates_table, r'$v_{\mathrm{Eact}}$')
v_Einact = remove_math(rates_table, r'$v_{\mathrm{Einact}}$')
v_PSI = remove_math(rates_table, r'$v_{\mathrm{PSI}}$')
v_Fdred = remove_math(rates_table, r'$v_{\mathrm{Fd,\ red}}$')
v_APXase = remove_math(rates_table, r'$v_{\mathrm{Ascorbate}}$')
v_MDAreduct = remove_math(rates_table, r'$v_{\mathrm{MDAreduct}}$')
v_Mehler = remove_math(rates_table, r'$v_{\mathrm{Mehler}}$')
v_GR = remove_math(rates_table, r'$v_{\mathrm{GR}}$')
v_DHAR = remove_math(rates_table, r'$v_{\mathrm{DHAR}}$')
v_3ASC = remove_math(rates_table, r'$v_{\mathrm{3ASC}}$')
v_ATPcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ ATP}}$')
v_NADPHcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ NADPH}}$')

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
EFNR = remove_math(params_table, r'$\mathrm{EFNR}$')
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
time = 't'

# --- Derived Parameters ---

H_st = remove_math(derived_params_table, r'$\mathrm{H}_\mathrm{st}$')
K_QAPQ = remove_math(derived_params_table, r'$K_\mathrm{eq, QAPQ}$')
K_FAFd = remove_math(derived_params_table, r'$K_\mathrm{eq, FAFd}$')
K_PCP700 = remove_math(derived_params_table, r'$K_\mathrm{eq, PCP700}$')
K_FNR = remove_math(derived_params_table, r'$K_\mathrm{eq, FNR}$')
K_ATPsynth = remove_math(derived_params_table, r'$K_\mathrm{eq, ATPsynthase}$')
K_cytb6f = remove_math(derived_params_table, r'$K_\mathrm{eq, cytb6f}$')
Vmax_rubisco = remove_math(derived_params_table, r'$V_1$')
Vmax_fbpase = remove_math(derived_params_table, r'$V_6$')
Vmax_sbpase = remove_math(derived_params_table, r'$V_9$')
Vmax_prkase = remove_math(derived_params_table, r'$V_13$')
Vmax_starch = remove_math(derived_params_table, r'$V_\mathrm{st}$')

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
{ode(PQ)} = -1.0 \cdot {v_PSII} + 1.0 \cdot {v_PQ} - 1.0 \cdot {v_NDH} + 1.0 \cdot {v_b6f} - 1.0 \cdot {v_Cyc}
```
```math
{ode(H_lu)} = \frac{{1}}{{{b_H}}} \cdot \left( 2 \cdot {v_PSII} + 4 \cdot {v_b6f} - {HPR} \cdot {v_ATPsynth} - {v_Leak} \right)
```
```math
{ode(PC_ox)} = -2.0 \cdot {v_b6f} + 1.0 \cdot {v_PSI}
```
```math
{ode(Fd_ox)} = 2.0 \cdot {v_Cyc} + 2.0 \cdot {v_FNR} + 1.0 \cdot {v_FdTrReduc} - 1.0 \cdot {v_Fdred}
```
```math
{ode(NADPH_st)} = {convf} \cdot {v_FNR} - 1.0 \cdot {v_BPGAdehynase} - 1.0 \cdot {v_MDAreduct} - 1.0 \cdot {v_GR} - 1.0 \cdot {v_NADPHcons}
```
```math
{ode(LHC)} = -1.0 \cdot {v_St21} + 1.0 \cdot {v_St12}
```
```math
{ode(ATP_st)} = {convf} \cdot {v_ATPsynth} - 1.0 \cdot {v_PGK1ase} - 1.0 \cdot {v_PRKase} - 1.0 \cdot {v_starch} - 1.0 \cdot {v_ATPcons}
```
```math
{ode(Vx)} = -1.0 \cdot {v_Deepox} + 1.0 \cdot {v_Epox}
```
```math
{ode(psbS)} = -1.0 \cdot {v_PsbSP} + 1.0 \cdot {v_PsbSD}
```
```math
{ode(PGA)} = -1.0 \cdot {v_PGK1ase} - 1.0 \cdot {v_pga_ex} + 2.0 \cdot {v_RuBisCO}
```
```math
{ode(BPGA)} = -1.0 \cdot {v_BPGAdehynase} + 1.0 \cdot {v_PGK1ase}
```
```math
{ode(GAP)} = 1.0 \cdot {v_BPGAdehynase} - 1.0 \cdot {v_TPIase} - 1.0 \cdot {v_Aldolase_FBP} - 1.0 \cdot {v_TKase_E4P} - 1.0 \cdot {v_TKase_R5P} - 1.0 \cdot {v_gap_ex}
```
```math
{ode(DHAP)} = 1.0 \cdot {v_TPIase} - 1.0 \cdot {v_Aldolase_FBP} - 1.0 \cdot {v_Aldolase_SBP} - 1.0 \cdot {v_dhap_ex}
```
```math
{ode(FBP)} = 1.0 \cdot {v_Aldolase_FBP} - 1.0 \cdot {v_FBPase}
```
```math
{ode(F6P)} = -1.0 \cdot {v_TKase_E4P} + 1.0 \cdot {v_FBPase} - 1.0 \cdot {v_PGIase}
```
```math
{ode(X5P)} = 1.0 \cdot {v_TKase_E4P} + 1.0 \cdot {v_TKase_R5P} - 1.0 \cdot {v_RPEase}
```
```math
{ode(E4P)} = 1.0 \cdot {v_TKase_E4P} - 1.0 \cdot {v_Aldolase_SBP}
```
```math
{ode(SBP)} = 1.0 \cdot {v_Aldolase_SBP} - 1.0 \cdot {v_SBPase}
```
```math
{ode(S7P)} = -1.0 \cdot {v_TKase_R5P} + 1.0 \cdot {v_SBPase}
```
```math
{ode(R5P)} = 1.0 \cdot {v_TKase_R5P} - 1.0 \cdot {v_Rpiase}
```
```math
{ode(RU5P)} = -1.0 \cdot {v_PRKase} + 1.0 \cdot {v_RPEase} + 1.0 \cdot {v_Rpiase}
```
```math
{ode(G6P)} = 1.0 \cdot {v_PGIase} - 1.0 \cdot {v_PGMase}
```
```math
{ode(G1P)} = -1.0 \cdot {v_starch} + 1.0 \cdot {v_PGMase}
```
```math
{ode(RUBP)} = 1.0 \cdot {v_PRKase} - 1.0 \cdot {v_RuBisCO}
```
```math
{ode(TRX_ox)} = -1.0 \cdot {v_FdTrReduc} + 5.0 \cdot {v_Eact}
```
```math
{ode(E_CBB_inactive)} = -5.0 \cdot {v_Eact} + 5.0 \cdot {v_Einact}
```
```math
{ode(H2O2)} = -1.0 \cdot {v_APXase} + {convf} \cdot {v_Mehler}
```
```math
{ode(MDA)} = -2.0 \cdot {v_MDAreduct} + 2.0 \cdot {v_APXase} - 2.0 \cdot {v_3ASC}
```
```math
{ode(GSSG)} = -1.0 \cdot {v_GR} + 1.0 \cdot {v_DHAR}
```
```math
{ode(DHA)} = 1.0 \cdot {v_3ASC} - 1.0 \cdot {v_DHAR}
```

</details>
                     """)

mdFile.new_header(4, 'Conserved quantities')

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
{PQH_2} = {PQ_tot} - {PQ}
```
```math
{PC_red} = {PC_tot} - {PC_ox}
```
```math
{Fd_red} = {Fd_tot} - {Fd_ox}
```
```math
{ADP_st} = {AP_tot} - {ATP_st}
```
```math
{NADP_st} = {NADP_tot} - {NADPH_st}
```
```math
{LHCp} =  1 - {LHC}
```
```math
{Zx} = {X_tot} - {Vx}
```
```math
{PsbSP} = {PsbS_tot} - {psbS}
```
```math
{psIIcross} =  {sigma0_II} + \left( 1 - {sigma0_II} - {sigma0_I} \right) \cdot {LHC}
```
```math
{Q} =  {gamma_0} \cdot {Vx} \cdot {psbS} + {gamma_1} \cdot {Vx} \cdot {PsbSP} + {gamma_2} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}}  \cdot {PsbSP} + {gamma_3} \cdot \frac{{{Zx}}}{{{Zx} + {K_ZSat}}}  \cdot {psbS}
```
```math
{Fluo} =  \frac{{{psIIcross} \cdot {k_F} \cdot {B0}}}{{{k_F} + {k2} + {k_H} \cdot {Q}}} + \frac{{{psIIcross} \cdot {k_F} \cdot {B2}}}{{{k_F} + {k_H} \cdot {Q}}}
```
```math
{pH_lu} =  \frac{{-\log \left( {H_lu} \cdot 0.00025 \right)}}{{\log 10}}
```
```math
{Pi_st} =  {P_tot} - \left( {PGA} + 2 \cdot {BPGA} + {GAP} + {DHAP} + 2 \cdot {FBP} + {F6P} + {G6P} + {G1P} + 2 \cdot {SBP} + {S7P} + {E4P} + {X5P} + {R5P} + 2 \cdot {RUBP} + {RU5P} + {ATP_st} \right)
```
```math
{TRX_red} = {thioredoxin_tot} - {TRX_ox}
```
```math
{E_CBB_active} = {e_cbb_tot} - {E_CBB_inactive}
```
```math
{ASC} = {Ascorbate_total} - {MDA} - {DHA}
```
```math
{GSH} =  {Glutathion_total} - 2 \cdot {GSSG}
```

</details>

<details>
<summary> Quasi-steady state approximation used to calculate the rate of PSII </summary>

```math
\begin{{align}}
\left( - \left( {psIIcross} \cdot {pfd}  \right) - \left({k_PQred} \cdot \frac{{{PQH_2}}}{{{K_QAPQ}}} \right) \right) \cdot {B0} + \left( {kH0} + {k_H} \cdot {Q} + {k_F} \right) \cdot {B1} + {k_PQred} \cdot {PQ} \cdot {B2} &= 0 \\
{psIIcross} \cdot {pfd} \cdot {B0} - \left( {kH0} + {k_H} \cdot {Q} + {k_F} + {k2} \right) \cdot {B1} &= 0 \\
{psIIcross} \cdot {pfd} \cdot {B2} - \left( {kH0} + {k_H} \cdot {Q} + {k_F} \right) \cdot {B3} &= 0 \\
{B0} + {B1} + {B2} + {B3} &= {PSII_tot}
\end{{align}}
```

</details>

<details>
<summary> Quasi-steady state approximation used to calculate the rate of PSI </summary>

```math
\begin{{align}}
- \left( \left( 1 - {psIIcross} \right) \cdot {pfd} + \left( \frac{{{k_PCox}}}{{{K_PCP700}}} \right) \cdot {PC_ox} \right) \cdot {Y0} + {k_PCox} \cdot {PC_red} \cdot {Y2} &= 0 \\
\left( 1 - {psIIcross} \right) \cdot {pfd} \cdot {Y0} - \left( {k_Fdred} \cdot {Fd_ox} + {O2_ext} \cdot {k_Mehler} \right) \cdot {Y1} + \frac{{{k_Fdred}}}{{{K_FAFd}}} \cdot {Fd_red} \cdot {Y2}  &= 0 \\
{Y0} + {Y1} + {Y2} &= {PSI_tot}
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
{H_st} =  1000.0 \cdot 10.0^{{-{pH_stroma}}}
```
```math
{K_QAPQ} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_QA} \cdot {F} + -2 \cdot {E0_PQ} \cdot {F} + 2 \cdot {pH_stroma} \ln 10 \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_FAFd} =  \exp \left( \frac{{-\left( -\left( -{E0_FA} \cdot {F} \right) + -{E0_Fd} \cdot {F} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_PCP700} =  \exp \left( \frac{{-\left( -\left( -{E0_PC} \cdot {F} \right) + -{E0_P700} \cdot {F} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_FNR} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_Fd} \cdot {F} + -2 \cdot {E0_NADP} \cdot {F} + \ln 10 \cdot {R} \cdot {T} \cdot {pH_stroma} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_ATPsynth} =  {Pi_mol} \cdot \exp \left( \frac{{- \left( {DeltaG0_ATP} - \left( \ln(10) \cdot {R} \cdot {T} \right) \cdot {HPR} \cdot \left( {pH_stroma} - {pH_lu} \right) \right)}}{{{R} \cdot {T}}} \right)
```
```math
{K_cytb6f} =  \exp \left( \frac{{-\left( -\left( -2 \cdot {F} \cdot {E0_PQ} + 2 \cdot \ln 10 \cdot {R} {T} \cdot {pH_lu} \right) + 2 \cdot -{F} \cdot {E0_PC} + 2 \ln 10 \cdot {R} \cdot {T} \cdot \left( {pH_stroma} - {pH_lu} \right) \right)}}{{{R} \cdot {T}}} \right)
```
```math
{Vmax_rubisco} = {E_CBB_active} \cdot {V_maxbase_rubisco}
```
```math
{Vmax_fbpase} = {E_CBB_active} \cdot {V_maxbase_fbpase}
```
```math
{Vmax_sbpase} = {E_CBB_active} \cdot {V_maxbase_sbpase}
```
```math
{Vmax_prkase} = {E_CBB_active} \cdot {V_maxbase_prkase}
```
```math
{Vmax_starch} = {E_CBB_active} \cdot {V_maxbase_starch}
```
</details>

                     """)

mdFile.new_header(3, 'Reaction Rates')

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
{v_PSII} =  0.5 \cdot {B1} \cdot {k2}
```
```math
{v_PQ} =  {PQH_2} \cdot {k_PTOX} \cdot \left\{{ \begin{{array}}{{cl}}
{O2_ext} & : \ {ox}\ \mathrm{{is \ True\ \lor}}\ {time} < {Ton} \lor {time} > {Toff}  \\
0 &
\end{{array}} \right.
```
```math
{v_NDH} = {PQ} \cdot  \left\{{ \begin{{array}}{{cl}}
{k_NDH} & : \ {ox}\ \mathrm{{is \ True\ \lor}}\ \left( {time} > {Ton} \land {time} < {Toff} \right)  \\
0 &
\end{{array}} \right.
```
```math
{v_b6f} =  \mathrm{{max}} \left( {k_Cytb6f} \cdot \left( {PQH_2} \cdot {PC_ox}^{{2}} - \frac{{{PQ} \cdot {PC_red}^{{2}}}}{{{K_cytb6f}}} \right), -{k_Cytb6f} \right)
```
```math
{v_Cyc} =  {k_cyc} \cdot {Fd_red}^{{2}} \cdot {PQ}
```
```math
{v_FNR} =  \frac{{{EFNR} \cdot {kcat_FNR} \cdot \left( \left( \frac{{{Fd_red}}}{{{KM_FNR_F}}} \right)^{{2}} \cdot \frac{{{NADP_st}}}{{{convf} \cdot {KM_FNR_N}}} - \frac{{\left( \frac{{{Fd_ox}}}{{{KM_FNR_F}}} \right)^{{2}} \cdot \frac{{{NADPH_st}}}{{{convf} \cdot {KM_FNR_N}}}}}{{{K_FNR}}} \right)}}{{\left( 1 + \frac{{{Fd_red}}}{{{KM_FNR_F}}} + \left( \frac{{{Fd_red}}}{{{KM_FNR_F}}} \right)^{{2}} \right) \left( 1 + \frac{{{NADP_st}}}{{{convf} \cdot {KM_FNR_N}}} \right) + \left( 1 + \frac{{{Fd_ox}}}{{{KM_FNR_F}}} + \left( \frac{{{Fd_ox}}}{{{KM_FNR_F}}} \right)^{{2}} \right) \cdot \left( 1 + \frac{{{NADPH_st}}}{{{convf} \cdot {KM_FNR_N}}} \right) - 1}}
```
```math
{v_Leak} =  {k_Leak} \cdot \left( {H_lu} - 4 \times 10^3 \cdot 10^{{{pH_stroma}}} \right)
```
```math
{v_St21} =  {k_Stt7} \cdot \frac{{1}}{{1 + \left( \frac{{{PQ}}}{{{PQ_tot} \cdot {KM_ST}}} \right)^{{{n_ST}}}}} \cdot {LHC}
```
```math
{v_St12} = {LHCp} \cdot {k_Pph1}
```
```math
{v_ATPsynth} =  {k_ATPsynth} \cdot \left( \frac{{{ADP_st}}}{{{convf}}} - \frac{{{ATP_st}}}{{{convf} \cdot {K_ATPsynth}}} \right)
```
```math
{v_Deepox} =  {k_DV} \cdot \frac{{{H_lu} ^{nh_x}}}{{\left(4 \times 10^3 \cdot 10^{{{K_pHSat}}}\right)^{nh_x} + {H_lu} ^{nh_x}}} \cdot {Vx}
```
```math
{v_Epox} = {Zx} \cdot {k_EZ}
```
```math
{v_PsbSP} =  {k_prot} \cdot \frac{{{H_lu} ^{nh_PsbS}}}{{\left(4 \times 10^3 \cdot 10^{{{K_pHSatLHC}}}\right)^{nh_PsbS} + {H_lu} ^{nh_PsbS}}} \cdot {psbS}
```
```math
{v_PsbSD} = {k_deprot} \cdot {PsbSP}
```
```math
{v_PGK1ase} =  {k_fast} \cdot \left( {ATP_st} \cdot {PGA} - \frac{{{BPGA} \cdot {ADP_st}}}{{{K_PGK1ase}}} \right)
```
```math
{v_BPGAdehynase} =  {k_fast} \cdot \left( {BPGA} \cdot {NADPH_st} \cdot {H_st} - \frac{{{GAP} \cdot {NADP_st} \cdot {Pi_st}}}{{{K_BPGAdehynase}}} \right)
```
```math
{v_TPIase} =  {k_fast} \cdot \left( {GAP} - \frac{{{DHAP}}}{{{K_TPIase}}} \right)
```
```math
{v_Aldolase_FBP} =  {k_fast} \cdot \left( {GAP} \cdot {DHAP} - \frac{{{FBP}}}{{{K_Aldolase_FBP}}} \right)
```
```math
{v_TKase_E4P} =  {k_fast} \cdot \left( {GAP} \cdot {F6P} - \frac{{{X5P} \cdot {E4P}}}{{{K_TKase_E4P}}} \right)
```
```math
{v_Aldolase_SBP} =  {k_fast} \cdot \left( {DHAP} \cdot {E4P} - \frac{{{SBP}}}{{{K_Aldolase_SBP}}} \right)
```
```math
{v_TKase_R5P} =  {k_fast} \cdot \left( {GAP} \cdot {S7P} - \frac{{{X5P} \cdot {R5P}}}{{{K_TKase_R5P}}} \right)
```
```math
{v_Rpiase} =  {k_fast} \cdot \left( {R5P} - \frac{{{RU5P}}}{{{K_Rpiase}}} \right)
```
```math
{v_RPEase} =  {k_fast} \cdot \left( {X5P} - \frac{{{RU5P}}}{{{K_RPEase}}} \right)
```
```math
{v_PGIase} =  {k_fast} \cdot \left( {F6P} - \frac{{{G6P}}}{{{K_PGIase}}} \right)
```
```math
{v_PGMase} =  {k_fast} \cdot \left( {G6P} - \frac{{{G1P}}}{{{K_PGMase}}} \right)
```
```math
{v_pga_ex} =  \frac{{{Vmax_ex} \cdot {PGA}}}{{{IF_3P} \cdot {K_diss_PGA}}}
```
```math
{v_gap_ex} =  \frac{{{Vmax_ex} \cdot {GAP}}}{{{IF_3P} \cdot {K_diss_GAP}}}
```
```math
{v_dhap_ex} =  \frac{{{Vmax_ex} \cdot {DHAP}}}{{{IF_3P} \cdot {K_diss_DHAP}}}
```
```math
{v_RuBisCO} =  \frac{{{Vmax_rubisco} \cdot {RUBP} \cdot {CO2}}}{{\left( {RUBP} + {Km_RuBisCO_RUBP} \cdot \left( 1 + \frac{{{PGA}}}{{{Ki_RuBisCO_PGA}}} + \frac{{{FBP}}}{{{Ki_RuBisCO_FBP}}} + \frac{{{SBP}}}{{{Ki_RuBisCO_SBP}}} + \frac{{{Pi_st}}}{{{Ki_RuBisCO_Pi}}} + \frac{{{NADPH_st}}}{{{Ki_RuBisCO_NADPH}}} \right) \right) \left( {CO2} + {Km_RuBisCO_CO2} \right)}}
```
```math
{v_FBPase} =  \frac{{{Vmax_fbpase} \cdot {FBP}}}{{{FBP} + {Km_FBPase} \cdot \left( 1 + \frac{{{F6P}}}{{{Ki_FBPase_F6P}}} + \frac{{{Pi_st}}}{{{Ki_FBPase_Pi}}} \right)}}
```
```math
{v_SBPase} =  \frac{{{Vmax_sbpase} \cdot {SBP}}}{{{SBP} + {Km_SBPase} \cdot \left( 1 + \frac{{{Pi_st}}}{{{Ki_SBPase_Pi}}} \right)}}
```
```math
{v_PRKase} =  \frac{{{Vmax_prkase} \cdot {RU5P} \cdot {ATP_st}}}{{\left( {RU5P} + {Km_PRKase_RU5P} \cdot \left( 1 + \frac{{{PGA}}}{{{Ki_PRKase_PGA}}} + \frac{{{RUBP}}}{{{Ki_PRKase_RuBP}}} + \frac{{{Pi_st}}}{{{Ki_PRKase_Pi}}} \right) \right) \left( {ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{Kiunc_PRKase_ADP}}} \right) + {Km_PRKase_ATP} \cdot \left( 1 + \frac{{{ADP_st}}}{{{Kicom_PRKase_ADP}}} \right) \right)}}
```
```math
{v_starch} =  \frac{{{Vmax_starch} \cdot {G1P} \cdot {ATP_st}}}{{\left( {G1P} + {Km_Starch_G1P} \right) \left( \left( 1 + \frac{{{ADP_st}}}{{{Ki_Starch_ADP}}} \right) \left( {ATP_st} + {Km_Starch_ATP} \right) + \frac{{{Km_Starch_ATP} \cdot {Pi_st}}}{{{Kact_Starch_PGA} \cdot {PGA} + {Kact_Starch_F6P} \cdot {F6P} + {Kact_Starch_FBP} \cdot {FBP}}} \right)}}
```
```math
{v_FdTrReduc} = {TRX_ox} \cdot {Fd_red} \cdot {k_fd_tr_reductase}
```
```math
{v_Eact} = {E_CBB_inactive} \cdot {TRX_red} \cdot {k_e_cbb_activation}
```
```math
{v_Einact} = {E_CBB_active} \cdot {k_e_cbb_relaxation}
```
```math
{v_PSI} =  \left( 1 - {psIIcross} \right) \cdot {pfd} \cdot {Y0}
```
```math
{v_Fdred} =  {k_Fdred} \cdot {Fd_ox} \cdot {Y1} - \frac{{{k_Fdred}}}{{{K_FAFd}}} \cdot {Fd_red} \cdot {Y2}
```
```math
{v_APXase} =  \frac{{{ASC} \cdot {H2O2} \cdot {XT}}}{{{ASC} \cdot {H2O2} \cdot \left( \frac{{1}}{{{k_f3}}} + \frac{{1}}{{{k_f5}}} \right) + \frac{{{ASC}}}{{{k_f1}}} + \frac{{{H2O2}}}{{{k_f4}}} + \frac{{{H2O2} \cdot {k_r4}}}{{{k_f4} \cdot {k_f5}}} + \frac{{{H2O2}}}{{{k_f2}}} + \frac{{{H2O2} \cdot {k_r2}}}{{{k_f2} \cdot {k_f3}}} + \frac{{{k_r1}}}{{{k_f1} \cdot {k_f2}}} + \frac{{{k_r1} \cdot {k_r2}}}{{{k_f1} \cdot {k_f2} \cdot {k_f3}}}}}
```
```math
{v_MDAreduct} =  \frac{{{kcat_MDAR} \cdot {MDAR_0} \cdot {NADPH_st} \cdot {MDA}}}{{{Km_MDAR_NADPH} \cdot {MDA} + {Km_MDAR_MDA} \cdot {NADPH_st} + {NADPH_st} \cdot {MDA} + {Km_MDAR_NADPH} \cdot {Km_MDAR_MDA}}}
```
```math
{v_Mehler} = {Y1} \cdot {O2_ext} \cdot {k_Mehler}
```
```math
{v_GR} =  \frac{{{kcat_GR} \cdot {GR_0} \cdot {NADPH_st} \cdot {GSSG}}}{{{Km_NADPH} \cdot {GSSG} + {Km_GSSG} \cdot {NADPH_st} + {NADPH_st} \cdot {GSSG} + {Km_NADPH} \cdot {Km_GSSG}}}
```
```math
{v_DHAR} =  \frac{{{kcat_DHAR} \cdot {DHAR_0} \cdot {DHA} \cdot {GSH}}}{{{K_DHAR} + {Km_DHA} \cdot {GSH} + {Km_GSH} \cdot {DHA} + {DHA} \cdot {GSH}}}
```
```math
{v_3ASC} =  {k3} \cdot {MDA}^{{2}}
```
```math
{v_ATPcons} = {ATP_st} \cdot {k_ex_atp}
```
```math
{v_NADPHcons} = {NADPH_st} \cdot {k_ex_nadph}
```

</details>

                     """)

mdFile.new_header(3, "Figures")

mdFile.new_paragraph(rf"""
                     
<details>
<summary></summary>
                     
<img style='float: center' src=''>

</details>
""")

mdFile.create_md_file()
