from pathlib import Path

from mdutils.mdutils import MdUtils  # noqa: E402

from GreenSlothUtils import gloss_fromCSV, remove_math

###### Util Functions ######

def ode(
    first_var: str,
    second_var: str = "t"
) -> str:
    for i in [first_var, second_var]:
        if "$" in i:
            msg = f"Your given variable '{i}' has a '$' in it"
            raise ValueError(msg)

    return rf"\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}"

###### Model Infos ######

model_title = "Saadat2021"
model_doi = "https://doi.org/10.3389/fpls.2021.750580"

###### Glossaries ######

cite_dict = {}

model_info = Path(__file__).parent / "model_info"
python_written = model_info / "python_written"

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / "comps.csv",
    omit_col="Glossary ID"
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = gloss_fromCSV(
    path=model_info / "derived_comps.csv",
    omit_col="Glossary ID"
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / "rates.csv",
    omit_col="Glossary ID"
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / "params.csv",
    cite_dict=cite_dict
)

derived_params_table, derived_params_table_tolist, derived_params_table_list = gloss_fromCSV(model_info / "derived_params.csv")

###### Variables for ease of access ######

# -- Compounds --

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
ATP_st = remove_math(comps_table, r'$\mathrm{ATP}$')
Fd_ox = remove_math(comps_table, r'$\mathrm{Fd}_\mathrm{ox}$')
H_lumen = remove_math(comps_table, r'$\mathrm{H}^+$')
LHC = remove_math(comps_table, r'$\mathrm{LHC}$')
NADPH_st = remove_math(comps_table, r'$\mathrm{NADPH}$')
PC_ox = remove_math(comps_table, r'$\mathrm{PC}_\mathrm{ox}$')
PQ = remove_math(comps_table, r'$\mathrm{PQ}_\mathrm{ox}$')
psbS = remove_math(comps_table, r'$\mathrm{Psbs}$')
Vx = remove_math(comps_table, r'$\mathrm{Vx}$')
MDA = remove_math(comps_table, r'$\mathrm{MDA}$')
H2O2 = remove_math(comps_table, r'$\mathrm{H_2O_2}$')
DHA = remove_math(comps_table, r'$\mathrm{DHA}$')
GSSG = remove_math(comps_table, r'$\mathrm{GSSG}$')
TRX_ox = remove_math(comps_table, r'$\mathrm{Trx_{ox}}$')
E_CBB_inactive = remove_math(comps_table, r'$\mathrm{E}_\mathrm{inactive}$')

# -- Derived Compounds --

pH_lumen = remove_math(derived_comps_table, r'$\mathrm{pH}_\mathrm{lumen}$')
Zx = remove_math(derived_comps_table, r'$\mathrm{Zx}$')
Fd_red = remove_math(derived_comps_table, r'$\mathrm{Fd}^-$')
PC_red = remove_math(derived_comps_table, r'$\mathrm{PC}^-$')
PsbSP = remove_math(derived_comps_table, r'$\mathrm{PsbS^P}$')
LHCp = remove_math(derived_comps_table, r'$\mathrm{LHCp}$')
Q = remove_math(derived_comps_table, r'$\mathrm{Q}$')
PQH_2 = remove_math(derived_comps_table, r'$\mathrm{PQH}_2$')
psIIcross = remove_math(derived_comps_table, r'$\mathrm{PSII_{cross}}$')
TRX_red = remove_math(derived_comps_table, r'$\mathrm{Trx_{red}}$')
E_CBB_active = remove_math(derived_comps_table, r'$\mathrm{E}_\mathrm{cbb,\ inactive}$')
NADP_st = remove_math(derived_comps_table, r'$\mathrm{NADP}^+$')
ADP_st = remove_math(derived_comps_table, r'$\mathrm{ADP}$')
Pi_st = remove_math(derived_comps_table, r'$\mathrm{P}_\mathrm{i}$')
ASC = remove_math(derived_comps_table, r'$\mathrm{ASC}$')
GSH = remove_math(derived_comps_table, r'$\mathrm{GSH}$')
IF_3P = remove_math(derived_comps_table, r'$\mathrm{N}$')
B0 = remove_math(derived_comps_table, r'$\mathrm{B_0}$')
B1 = remove_math(derived_comps_table, r'$\mathrm{B_1}$')
B2 = remove_math(derived_comps_table, r'$\mathrm{B_2}$')
B3 = remove_math(derived_comps_table, r'$\mathrm{B_3}$')
Y0 = remove_math(derived_comps_table, r'$\mathrm{Y_0}$')
Y1 = remove_math(derived_comps_table, r'$\mathrm{Y_1}$')
Y2 = remove_math(derived_comps_table, r'$\mathrm{Y_2}$')
Fluo = remove_math(derived_comps_table, r'$\mathrm{Fluo}$')

# -- Rates --

v_Einact = remove_math(rates_table, r'$v_{\mathrm{Einact}}$')
v_Eact = remove_math(rates_table, r'$v_{\mathrm{Eact}}$')
v_3ASC = remove_math(rates_table, r'$v_{\mathrm{3ASC}}$')
v_DHAR = remove_math(rates_table, r'$v_{\mathrm{DHAR}}$')
v_Mehler = remove_math(rates_table, r'$v_{\mathrm{Mehler}}$')
v_APXase = remove_math(rates_table, r'$v_{\mathrm{Ascorbate}}$')
v_GR = remove_math(rates_table, r'$v_{\mathrm{GR}}$')
v_MDAreduct = remove_math(rates_table, r'$v_{\mathrm{MDAreduct}}$')
v_FdTrReduc = remove_math(rates_table, r'$v_{\mathrm{FdTrReductase}}$')
v_Fdred = remove_math(rates_table, r'$v_{\mathrm{Fd,\ red}}$')
v_NADPHcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ NADPH}}$')
v_PSI = remove_math(rates_table, r'$v_{\mathrm{PSI}}$')
v_PGMase = remove_math(rates_table, r'$v_{\mathrm{Phosphoglucomutase}}$')
v_PGIase = remove_math(rates_table, r'$v_{G6P\_ isomerase}$')
v_RPEase = remove_math(rates_table, r'$v_{12}$')
v_Rpiase = remove_math(rates_table, r'$v_{11}$')
v_TKase_R5P = remove_math(rates_table, r'$v_{10}$')
v_Aldolase_SBP = remove_math(rates_table, r'$v_{8}$')
v_TKase_E4P = remove_math(rates_table, r'$v_{\mathrm{F6P\_ Transketolase}}$')
v_Aldolase_FBP = remove_math(rates_table, r'$v_{\mathrm{Aldolase}}$')
v_TPIase = remove_math(rates_table, r'$v_{\mathrm{TPI}}$')
v_BPGAdehynase = remove_math(rates_table, r'$v_{\mathrm{BPGA\_dehydrogenase}}$')
v_PGK1ase = remove_math(rates_table, r'$v_{\mathrm{PGA\_kinase}}$')
v_starch = remove_math(rates_table, r'$v_{\mathrm{Starch}}$')
v_gap_ex = remove_math(rates_table, r'$v_{gap}$')
v_dhap_ex = remove_math(rates_table, r'$v_{DHAP}$')
v_pga_ex = remove_math(rates_table, r'$v_{pga}$')
v_PRKase = remove_math(rates_table, r'$v_{13}$')
v_SBPase = remove_math(rates_table, r'$v_9$')
v_FBPase = remove_math(rates_table, r'$v_{\mathrm{FBPase}}$')
v_RuBisCO_c = remove_math(rates_table, r'$v_{\mathrm{RuBisCo}}$')
v_PsbSD = remove_math(rates_table, r'$v_{\mathrm{LHCdeprotonation}}$')
v_Epox = remove_math(rates_table, r'$v_{\mathrm{Epox}}$')
v_Deepox = remove_math(rates_table, r'$v_{\mathrm{Deepox}}$')
v_St12 = remove_math(rates_table, r'$v_{\mathrm{St21}}$')
v_St21 = remove_math(rates_table, r'$v_{\mathrm{St12}}$')
v_Cyc = remove_math(rates_table, r'$v_{\mathrm{Cyc}}$')
v_NDH = remove_math(rates_table, r'$v_{\mathrm{NDH}}$')
v_FNR = remove_math(rates_table, r'$v_{\mathrm{FNR}}$')
v_b6f = remove_math(rates_table, r'$v_{\mathrm{b6f}}$')
v_PsbSP = remove_math(rates_table, r'$v_{\mathrm{LHCprotonation}}$')
v_ATPcons = remove_math(rates_table, r'$v_{\mathrm{EX\_ ATP}}$')
v_Leak = remove_math(rates_table, r'$v_{\mathrm{Leak}}$')
v_ATPsynth = remove_math(rates_table, r'$v_{\mathrm{ATPsynthase}}$')
v_PQ = remove_math(rates_table, r'$v_{\mathrm{PTOX}}$')
v_PSII = remove_math(rates_table, r'$v_{\mathrm{PSII}}$')

# -- Parameters --

PPFD = remove_math(params_table, r'$\mathrm{PFD}$')
CO2 = remove_math(params_table, r'$\mathrm{CO}_2$')
O2_lumen = remove_math(params_table, r'$\mathrm{O}_2^\mathrm{ex}$')
pH_stroma = remove_math(params_table, r'$\mathrm{pH}_\mathrm{stroma}$')
H_stroma = remove_math(params_table, r'$\mathrm{H}_\mathrm{stroma}$')
bH = remove_math(params_table, r'$b_\mathrm{H}$')
F = remove_math(params_table, r'$F$')
E0_PC = remove_math(params_table, r'$E^0\mathrm{(PC/PC^-)}$')
E0_P700 = remove_math(params_table, r'$E^0\mathrm{(P_{700}^+/P_{700})}$')
E0_FA = remove_math(params_table, r'$E^0\mathrm{(FA/FA^-)}$')
E0_Fd = remove_math(params_table, r'$E^0\mathrm{(Fd/Fd^-)}$')
E0_NADP = remove_math(params_table, r'$E^0\mathrm{(NADP^+/NADPH)}$')
convf = remove_math(params_table, r'$\mathrm{convf}$')
R = remove_math(params_table, r'$R$')
T = remove_math(params_table, r'$T$')
Carotenoids_tot = remove_math(params_table, r'$\mathrm{X}^{\mathrm{tot}}$')
Fd_tot = remove_math(params_table, r'$\mathrm{Fd}^{\mathrm{tot}}$')
PC_tot = remove_math(params_table, r'$\mathrm{PC}^{\mathrm{tot}}$')
PSBS_tot = remove_math(params_table, r'$\mathrm{PsbS}^{\mathrm{tot}}$')
LHC_tot = remove_math(params_table, r'')
gamma0 = remove_math(params_table, r'$\gamma_0$')
gamma1 = remove_math(params_table, r'$\gamma_1$')
gamma2 = remove_math(params_table, r'$\gamma_2$')
gamma3 = remove_math(params_table, r'$\gamma_3$')
kZSat = remove_math(params_table, r'$K_\mathrm{ZSat}$')
E0_QA = remove_math(params_table, r'$E^0\mathrm{(QA/QA^-)}$')
E0_PQ = remove_math(params_table, r'$E^0\mathrm{(PQ/PQH_2)}$')
PQ_tot = remove_math(params_table, r'$\mathrm{PQ}^{\mathrm{tot}}$')
staticAntII = remove_math(params_table, r'$\sigma _\mathrm{II} ^0$')
staticAntI = remove_math(params_table, r'$\sigma _\mathrm{I} ^0$')
Thioredoxin_tot = remove_math(params_table, r'$\mathrm{thioredoxin}_\mathrm{tot}$')
E_total = remove_math(params_table, r'$e_{\mathrm{cbb}_\mathrm{tot}}$')
NADP_tot = remove_math(params_table, r'$\mathrm{NADP}^{\mathrm{tot}}$')
AP_tot = remove_math(params_table, r'$\mathrm{AP}^{\mathrm{tot}}$')
Pi_tot = remove_math(params_table, r'$\mathrm{P}^{\mathrm{tot}}$')
kf_v_FdTrReduc = remove_math(params_table, r'$k_{\mathrm{fd}_{\mathrm{tr}_\mathrm{reductase}}}$')
kf_v_Eact = remove_math(params_table, r'$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{activation}}}$')
kf_v_Einact = remove_math(params_table, r'$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{relaxation}}}$')
ASC_tot = remove_math(params_table, r'$\mathrm{Ascorbate}_{\mathrm{total}}$')
Glutathion_tot = remove_math(params_table, r'$\mathrm{Gluthation}_{\mathrm{total}}$')
kf_v_ATPsynth = remove_math(params_table, r'$k_\mathrm{ATPsynthase}$')
HPR = remove_math(params_table, r'$\mathrm{HPR}$')
Pi_mol = remove_math(params_table, r'$\mathrm{Pi}_\mathrm{mol}$')
DeltaG0_ATP = remove_math(params_table, r'$\Delta G_{0_{ATP}}$')
kcat_v_b6f = remove_math(params_table, r'$k_\mathrm{Cytb6f}$')
kh_v_PsbSP = remove_math(params_table, r'$\mathrm{k}_{\mathrm{Hill}_\mathrm{L}}$')
kf_v_PsbSP = remove_math(params_table, r'$k_\mathrm{Protonation}$')
ksat_v_PsbSP = remove_math(params_table, r'$K_\mathrm{pHSatLHC}$')
kf_v_PsbSD = remove_math(params_table, r'$k_\mathrm{Deprotonation}$')
kf_v_Cyc = remove_math(params_table, r'$k_\mathrm{cyc}$')
kf_v_Deepox = remove_math(params_table, r'$k_\mathrm{DeepoxV}$')
kh_v_Deepox = remove_math(params_table, r'$\mathrm{k}_{\mathrm{Hill}_\mathrm{X}}$')
ksat_v_Deepox = remove_math(params_table, r'$K_\mathrm{pHSat}$')
kf_v_Epox = remove_math(params_table, r'$k_\mathrm{EpoxZ}$')
km_v_FNR_Fd_red = remove_math(params_table, r'$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{F}}}$')
km_v_FNR_NADP_st = remove_math(params_table, r'$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{N}}}$')
Enz0_v_FNR = remove_math(params_table, r'$\mathrm{EFNR}$')
kcat_v_FNR = remove_math(params_table, r'$k_{\mathrm{cat}_\mathrm{FNR}}$')
kf_v_NDH = remove_math(params_table, r'$k_\mathrm{NDH}$')
PSII_total = remove_math(params_table, r'$\mathrm{PSII}^{\mathrm{tot}}$')
PSI_total = remove_math(params_table, r'$\mathrm{PSI}^{\mathrm{tot}}$')
kH0 = remove_math(params_table, r'$k_{H_0}$')
kPQred = remove_math(params_table, r'$k_{\mathrm{PQ}_\mathrm{red}}$')
kPCox = remove_math(params_table, r'$k_\mathrm{PCox}$')
kFdred = remove_math(params_table, r'$k_{\mathrm{Fd}_\mathrm{red}}$')
k2 = remove_math(params_table, r'$k_2$')
kH = remove_math(params_table, r'$k_H$')
kF = remove_math(params_table, r'$k_F$')
kMehler = remove_math(params_table, r'$k_{\mathrm{Mehler}}$')
Enz0_v_Fdred = remove_math(params_table, r'$\mathrm{E_{Fdred}}$')
kcat_v_Fdred = remove_math(params_table, r'$k_{\mathrm{cat}_\mathrm{Fdred}}$')
kf_v_Leak = remove_math(params_table, r'$k_\mathrm{leak}$')
kPTOX = remove_math(params_table, r'$k_\mathrm{PTOX}$')
kStt7 = remove_math(params_table, r'$k_\mathrm{Stt7}$')
km_v_St12 = remove_math(params_table, r'$K_{\mathrm{M}_\mathrm{ST}}$')
n_ST = remove_math(params_table, r'$n_\mathrm{ST}$')
kPph1 = remove_math(params_table, r'$k_\mathrm{Pph1}$')
Enz0_rubisco = remove_math(params_table, r'$\mathrm{E_{Rubisco}}$')
kcat_v_RuBisCO_c = remove_math(params_table, r'$V_{1_{\mathrm{base}}}$')
km_v_RuBisCO_c_RUBP = remove_math(params_table, r'$K_{\mathrm{m}1}$')
km_v_RuBisCO_c_CO2 = remove_math(params_table, r'$K_{\mathrm{mCO2}}$')
ki_v_RuBisCO_c_PGA = remove_math(params_table, r'$K_{\mathrm{i}11}$')
ki_v_RuBisCO_c_FBP = remove_math(params_table, r'$K_{\mathrm{i}12}$')
ki_v_RuBisCO_c_SBP = remove_math(params_table, r'$K_{\mathrm{i}13}$')
ki_v_RuBisCO_c_Pi_st = remove_math(params_table, r'$K_{\mathrm{i}14}$')
ki_v_RuBisCO_c_NADPH_st = remove_math(params_table, r'$K_{\mathrm{i}15}$')
kre_v_PGK1ase = remove_math(params_table, r'$k$')
keq_v_PGK1ase = remove_math(params_table, r'$q_2$')
kre_v_BPGAdehynase = remove_math(params_table, r'$k$')
keq_v_BPGAdehynase = remove_math(params_table, r'$q_3$')
kre_v_TPIase = remove_math(params_table, r'$k$')
keq_v_TPIase = remove_math(params_table, r'$q_4$')
kre_v_Aldolase_FBP = remove_math(params_table, r'$k$')
keq_v_Aldolase_FBP = remove_math(params_table, r'$q_5$')
kre_v_Aldolase_SBP = remove_math(params_table, r'$k$')
keq_v_Aldolase_SBP = remove_math(params_table, r'$q_8$')
Enz0_v_FBPase = remove_math(params_table, r'')
kcat_v_FBPase = remove_math(params_table, r'$V_{6_{\mathrm{base}}}$')
km_v_FBPase_s = remove_math(params_table, r'$K_{\mathrm{m}6}$')
ki_v_FBPase_F6P = remove_math(params_table, r'$K_{\mathrm{i}61}$')
ki_v_FBPase_Pi_st = remove_math(params_table, r'$K_{\mathrm{i}62}$')
kre_v_TKase_E4P = remove_math(params_table, r'$k$')
keq_v_TKase_E4P = remove_math(params_table, r'$q_7$')
kre_v_TKase_R5P = remove_math(params_table, r'$k$')
keq_v_TKase_R5P = remove_math(params_table, r'$q_{10}$')
Enz0_v_SBPase = remove_math(params_table, r'')
kcat_v_SBPase = remove_math(params_table, r'$V_{9_{\mathrm{base}}}$')
km_v_SBPase_s = remove_math(params_table, r'$K_{\mathrm{m}9}$')
ki_v_SBPase_Pi_st = remove_math(params_table, r'$K_{\mathrm{i}9}$')
kre_v_Rpiase = remove_math(params_table, r'$k$')
keq_v_Rpiase = remove_math(params_table, r'$q_{11}$')
kre_v_RPEase = remove_math(params_table, r'$k$')
keq_v_RPEase = remove_math(params_table, r'$q_{12}$')
Enz0_v_PRKase = remove_math(params_table, r'')
kcat_v_PRKase = remove_math(params_table, r'$V_{13_{\mathrm{base}}}$')
km_v_PRKase_RU5P = remove_math(params_table, r'$K_{\mathrm{m}131}$')
km_v_PRKase_ATP_st = remove_math(params_table, r'$K_{\mathrm{m}132}$')
ki_v_PRKase_PGA = remove_math(params_table, r'$K_{\mathrm{i}131}$')
ki_v_PRKase_RUBP = remove_math(params_table, r'$K_{\mathrm{i}132}$')
ki_v_PRKase_Pi_st = remove_math(params_table, r'$K_{\mathrm{i}133}$')
ki_v_PRKase_4 = remove_math(params_table, r'$K_{\mathrm{i}134}$')
ki_v_PRKase_5 = remove_math(params_table, r'$K_{\mathrm{i}135}$')
kre_v_PGIase = remove_math(params_table, r'$k$')
keq_v_PGIase = remove_math(params_table, r'$q_{14}$')
kre_v_PGMase = remove_math(params_table, r'$k$')
keq_v_PGMase = remove_math(params_table, r'$q_{15}$')
Pi_ext = remove_math(params_table, r'$\mathrm{P}_\mathrm{ext}$')
km_v_pga_ex = remove_math(params_table, r'$K_{\mathrm{pga}}$')
km_v_gap_ex = remove_math(params_table, r'$K_{\mathrm{gap}}$')
km_v_dhap_ex = remove_math(params_table, r'$K_{\mathrm{dhap}}$')
km_IF_3P_Pi_ext = remove_math(params_table, r'$K_{\mathrm{pxt}}$')
km_IF_3P_Pi_st = remove_math(params_table, r'$K_{\mathrm{pi}}$')
kcat_IF_3P = remove_math(params_table, r'$V_{\mathrm{ex}}$')
Enz0_IF_3P = remove_math(params_table, r'')
Enz0_v_starch = remove_math(params_table, r'')
km_v_starch_G1P = remove_math(params_table, r'$K_{\mathrm{mst}1}$')
km_v_starch_ATP_st = remove_math(params_table, r'$K_{\mathrm{mst}2}$')
ki_v_starch = remove_math(params_table, r'$K_{\mathrm{ist}}$')
ki_v_starch_PGA = remove_math(params_table, r'$K_{\mathrm{ast1}}$')
ki_v_starch_F6P = remove_math(params_table, r'$K_{\mathrm{ast2}}$')
ki_v_starch_FBP = remove_math(params_table, r'$K_{\mathrm{ast3}}$')
kcat_v_starch = remove_math(params_table, r'$V_{\mathrm{st}_{\mathrm{base}}}$')
kf_v_3ASC = remove_math(params_table, r'$k3$')
Enz0_v_MDAreduct = remove_math(params_table, r'$\mathrm{MDAR}_0$')
kcat_v_MDAreduct = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{MDAR}}}$')
km_v_MDAreduct_NADPH_st = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{MDAR-NADPH}}}$')
km_v_MDAreduct_MDA = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{MDAR-MDA}}}$')
kf1 = remove_math(params_table, r'$kf1$')
kr1 = remove_math(params_table, r'$kr1$')
kf2 = remove_math(params_table, r'$kf2$')
kr2 = remove_math(params_table, r'$kr2$')
kf3 = remove_math(params_table, r'$kf3$')
kf4 = remove_math(params_table, r'$kf4$')
kr4 = remove_math(params_table, r'$kr4$')
kf5 = remove_math(params_table, r'$kf5$')
XT = remove_math(params_table, r'$XT$')
Enz0_v_GR = remove_math(params_table, r'$\mathrm{GR}_0$')
kcat_v_GR = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{GR}}}$')
km_v_GR_NADPH_st = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{NADPH}}}$')
km_v_GR_GSSG = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{GSSG}}}$')
km_v_DHAR_DHA = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{DHA}}}$')
km_v_DHAR_GSH = remove_math(params_table, r'$K_{\mathrm{m}_{\mathrm{GSH}}}$')
K = remove_math(params_table, r'$K$')
Enz0_v_DHAR = remove_math(params_table, r'$\mathrm{DHAR}_0$')
kcat_v_DHAR = remove_math(params_table, r'$k_{\mathrm{cat}_{\mathrm{DHAR}}}$')
kf_v_ATPcons = remove_math(params_table, r'$k_{\mathrm{ex}_{\mathrm{atp}}}$')
kf_v_NADPHcons = remove_math(params_table, r'$k_{\mathrm{ex}_{\mathrm{nadph}}}$')

# --- Derived Parameters ---

RT = remove_math(derived_params_table, r'$RT$')
dG_pH = remove_math(derived_params_table, r'$\Delta G _\mathrm{pH}$')
keq_PQH_2 = remove_math(derived_params_table, r'$K_\mathrm{eq, QAPQ}$')
keq_v_FNR = remove_math(derived_params_table, r'$K_\mathrm{eq, FNR}$')
vmax_v_FNR = remove_math(derived_params_table, r'$V_{FNR}$')
keq_PCP700 = remove_math(derived_params_table, r'$K_\mathrm{eq, PCP700}$')
keq_v_Fdred = remove_math(derived_params_table, r'$K_\mathrm{eq, FAFd}$')
vmax_v_Fdred = remove_math(derived_params_table, r'$V_{Fdred}$')
vmax_v_pga_ex = remove_math(derived_params_table, r'$V_{pga\_ex}$')
vmax_v_MDAreduct = remove_math(derived_params_table, r'$V_{mdared}$')
vmax_v_GR = remove_math(derived_params_table, r'$V_{GR}$')
vmax_v_DHAR = remove_math(derived_params_table, r'$V_{DHAR}$')
keq_v_ATPsynth = remove_math(derived_params_table, r'$K_\mathrm{eq, ATPsynthase}$')
keq_v_b6f = remove_math(derived_params_table, r'$K_\mathrm{eq, cytb6f}$')
Enz0_rubisco_active = remove_math(derived_params_table, r'$Enz_{rubisco}$')
vmax_v_RuBisCO_c = remove_math(derived_params_table, r'$V_1$')
Enz0_v_FBPase_active = remove_math(derived_params_table, r'$Enz_{fbpase}$')
vmax_v_FBPase = remove_math(derived_params_table, r'$V_6$')
Enz0_v_SBPase_active = remove_math(derived_params_table, r'$Enz_{sbpase}$')
vmax_v_SBPase = remove_math(derived_params_table, r'$V_9$')
Enz0_v_PRKase_active = remove_math(derived_params_table, r'$Enz_{prkase}$')
vmax_v_PRKase = remove_math(derived_params_table, r'$V_13$')
Enz0_v_starch_active = remove_math(derived_params_table, r'$Enz_{starch}$')
vmax_v_starch = remove_math(derived_params_table, r'$V_\mathrm{st}$')

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""The [{model_title}]({model_doi}) model builds upon previous models, particularly the Matuszynska2019 model, by incorporating and modifying various reactions and aspects of photosynthesis. Overall, the model can be divided into three modules: the ascorbate-glutathione cycle, the Calvin-Benson-Bassham (CBB) cycle and thioredoxin reductase-regulated reactions, and the photosynthetic electron transport chain (PETC).
                     
The model is primarily used to investigate the electron flows around PSI and their relevance to photosynthetic efficiency. Several different analyses have been conducted to validate the model in both steady-state and dynamic environment conditions. The most interesting is the direct comparison of a knockout mutant of the protein PGR5. This protein is known to catalyse the reduction of plastoquinone by ferredoxin. The results of this comparison align with experimental values, which are, however, not presented in the publication but are referenced. Additionally, it is noted that the results should not be interpreted as accurate quantitative data, but rather as a proof of concept for the model.

Overall, the model has one advantage over other photosynthesis models, as it also highlights the importance of other electron flows, not just the PETC. Additionally, not only are the authors open about the model's flaws, but they are also insistent on making their code and analyses available on GitHub. Therefore, this model serves as a good stepping stone for more complex models that aim to incorporate aspects of photosynthesis, which are often simplified in other models.
                     """)

mdFile.new_header(2, "Installation")

mdFile.new_paragraph(f"""
All the files needed to run this model are located in [model](./model) folder. To use this model you only need to copy this folder and write the following to import the model in your Python script:

```python
from model import {model_title}
```

The packages required to run this model can either be installed by using the `pixi` environment located inside the [pyproject.toml](../pyproject.toml) file or by just installing the `mxlpy` package and all its dependencies.
                     """)

mdFile.new_header(3, "Compounds")

mdFile.new_header(4, "Part of ODE system")

mdFile.new_table(columns = len(comps_table.columns), rows = len(comps_table_tolist), text = comps_table_list)

mdFile.new_paragraph(fr"""
<details>
<summary>ODE System</summary>

```math 
{ode(TRX_ox)} = - {v_FdTrReduc} + 5 \cdot {v_Eact}
```
```math 
{ode(Fd_ox)} = {v_FdTrReduc} + 2 \cdot {v_Cyc} + 2 \cdot {v_FNR} - {v_Fdred}
```
```math 
{ode(E_CBB_inactive)} = - 5 \cdot {v_Eact} + 5 \cdot {v_Einact}
```
```math 
{ode(H_lumen)} = \frac{{-{HPR}}}{{{bH}}} \cdot {v_ATPsynth} + \frac{{4.0}}{{{bH}}} \cdot {v_b6f} + \frac{{2.0}}{{{bH}}} \cdot {v_PSII} + \frac{{-1.0}}{{{bH}}} \cdot {v_Leak}
```
```math 
{ode(ATP_st)} = {convf} \cdot {v_ATPsynth} - 1.0 \cdot {v_PGK1ase} - 1.0 \cdot {v_PRKase} - 1.0 \cdot {v_starch} - {v_ATPcons}
```
```math 
{ode(PC_ox)} = - 2 \cdot {v_b6f} + {v_PSI}
```
```math 
{ode(PQ)} = - {v_Cyc} + {v_b6f} - {v_PSII} - {v_NDH} + {v_PQ}
```
```math 
{ode(psbS)} = - {v_PsbSP} + {v_PsbSD}
```
```math 
{ode(Vx)} = - {v_Deepox} + {v_Epox}
```
```math 
{ode(NADPH_st)} = {convf} \cdot {v_FNR} - 1.0 \cdot {v_BPGAdehynase} - {v_MDAreduct} - {v_GR} - {v_NADPHcons}
```
```math 
{ode(H2O2)} = {convf} \cdot {v_Mehler} - {v_APXase}
```
```math 
{ode(LHC)} = - {v_St12} + {v_St21}
```
```math 
{ode(RUBP)} = 1.0 \cdot {v_PRKase} - 1.0 \cdot {v_RuBisCO_c}
```
```math 
{ode(PGA)} = - 1.0 \cdot {v_PGK1ase} + 2.0 \cdot {v_RuBisCO_c} - {v_pga_ex}
```
```math 
{ode(BPGA)} = 1.0 \cdot {v_PGK1ase} - 1.0 \cdot {v_BPGAdehynase}
```
```math 
{ode(GAP)} = 1.0 \cdot {v_BPGAdehynase} - {v_TPIase} - {v_Aldolase_FBP} - {v_TKase_E4P} - {v_TKase_R5P} - {v_gap_ex}
```
```math 
{ode(DHAP)} = {v_TPIase} - {v_Aldolase_FBP} - {v_Aldolase_SBP} - {v_dhap_ex}
```
```math 
{ode(FBP)} = {v_Aldolase_FBP} - {v_FBPase}
```
```math 
{ode(E4P)} = {v_TKase_E4P} - {v_Aldolase_SBP}
```
```math 
{ode(SBP)} = {v_Aldolase_SBP} - {v_SBPase}
```
```math 
{ode(F6P)} = - {v_TKase_E4P} + {v_FBPase} - {v_PGIase}
```
```math 
{ode(X5P)} = {v_TKase_E4P} + {v_TKase_R5P} - {v_RPEase}
```
```math 
{ode(S7P)} = - {v_TKase_R5P} + {v_SBPase}
```
```math 
{ode(R5P)} = {v_TKase_R5P} - {v_Rpiase}
```
```math 
{ode(RU5P)} = - 1.0 \cdot {v_PRKase} + {v_RPEase} + {v_Rpiase}
```
```math 
{ode(G6P)} = {v_PGIase} - {v_PGMase}
```
```math 
{ode(G1P)} = - 1.0 \cdot {v_starch} + {v_PGMase}
```
```math 
{ode(MDA)} = - 2 \cdot {v_MDAreduct} + 2 \cdot {v_APXase} - 2 \cdot {v_3ASC}
```
```math 
{ode(DHA)} = {v_3ASC} - {v_DHAR}
```
```math 
{ode(GSSG)} = - {v_GR} + {v_DHAR}
```

</details>
                     """)

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(columns = len(derived_comps_table.columns), rows = len(derived_comps_table_tolist), text = derived_comps_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary> Calculations </summary>

```math
{pH_lumen} =  -\log_{{10}} \left( {H_lumen} \cdot 0.00025 \right)
```
```math
{Zx} =  {Carotenoids_tot} - {Vx}
```
```math
{Fd_red} =  {Fd_tot} - {Fd_ox}
```
```math
{PC_red} =  {PC_tot} - {PC_ox}
```
```math
{PsbSP} =  {PSBS_tot} - {psbS}
```
```math
{LHCp} =  {LHC_tot} - {LHC}
```
```math
{Q} =  {gamma0} \cdot {Vx} \cdot {psbS} + {gamma1} \cdot {Vx} \cdot {PsbSP} + {gamma2} \cdot \frac{{{Zx}}}{{{Zx} + {kZSat}}} \cdot {PsbSP} + {gamma3} \cdot \frac{{{Zx}}}{{{Zx} + {kZSat}}} \cdot {psbS}
```
```math
{PQH_2} =  {PQ_tot} - {PQ}
```
```math
{psIIcross} =  {staticAntII} + \left( 1 - {staticAntII} - {staticAntI} \right) {LHC}
```
```math
{TRX_red} =  {Thioredoxin_tot} - {TRX_ox}
```
```math
{E_CBB_active} =  {E_total} - {E_CBB_inactive}
```
```math
{NADP_st} =  {NADP_tot} - {NADPH_st}
```
```math
{ADP_st} =  {AP_tot} - {ATP_st}
```
```math
{Pi_st} =  {Pi_tot} - \left( {PGA} + 2 {BPGA} + {GAP} + {DHAP} + 2 {FBP} + {F6P} + {G6P} + {G1P} + 2 {SBP} + {S7P} + {E4P} + {X5P} + {R5P} + 2 {RUBP} + {RU5P} + {ATP_st} \right)
```
```math
{ASC} =  {ASC_tot} - {MDA} - {DHA}
```
```math
{GSH} =  {Glutathion_tot} - 2 {GSSG}
```
```math
{IF_3P} =  1 + \left( 1 + \frac{{{km_IF_3P_Pi_ext}}}{{{Pi_ext}}} \right) \left( \frac{{{Pi_st}}}{{{km_IF_3P_Pi_st}}} + \frac{{{PGA}}}{{{km_v_pga_ex}}} + \frac{{{GAP}}}{{{km_v_gap_ex}}} + \frac{{{DHAP}}}{{{km_v_dhap_ex}}} \right)
```
```math
{Fluo} =  \frac{{{psIIcross} \cdot {kF} \cdot {B0}}}{{{kF} + {k2} + {kH} \cdot {Q}}} + \frac{{{psIIcross} \cdot {kF} \cdot {B2}}}{{{kF} + {kH} \cdot {Q}}}
```

<details>
<summary> Quasi-steady state approximation used to calculate the rate of PSII </summary>

```math
\begin{{align}}
\left( - \left( {psIIcross} \cdot {PPFD}  \right) - \left({kPQred} \cdot \frac{{{PQH_2}}}{{{keq_PQH_2}}} \right) \right) \cdot {B0} + \left( {kH0} + {kH} \cdot {Q} + {kF} \right) \cdot {B1} + {kPQred} \cdot {PQ} \cdot {B2} &= 0 \\
{psIIcross} \cdot {PPFD} \cdot {B0} - \left( {kH0} + {kH} \cdot {Q} + {kF} + {k2} \right) \cdot {B1} &= 0 \\
{psIIcross} \cdot {PPFD} \cdot {B2} - \left( {kH0} + {kH} \cdot {Q} + {kF} \right) \cdot {B3} &= 0 \\
{B0} + {B1} + {B2} + {B3} &= {PSII_total}
\end{{align}}
```

</details>

<details>
<summary> Quasi-steady state approximation used to calculate the rate of PSI </summary>

```math
\begin{{align}}
- \left( \left( 1 - {psIIcross} \right) \cdot {PPFD} + \left( \frac{{{kPCox}}}{{{keq_PCP700}}} \right) \cdot {PC_ox} \right) \cdot {Y0} + {kPCox} \cdot {PC_red} \cdot {Y2} &= 0 \\
\left( 1 - {psIIcross} \right) \cdot {PPFD} \cdot {Y0} - \left( {kFdred} \cdot {Fd_ox} + {O2_lumen} \cdot {kMehler} \right) \cdot {Y1} + \frac{{{kFdred}}}{{{keq_v_Fdred}}} \cdot {Fd_red} \cdot {Y2}  &= 0 \\
{Y0} + {Y1} + {Y2} &= {PSI_total}
\end{{align}}
```

</details>

</details>

                     """)

mdFile.new_header(3, "Parameters")

mdFile.new_table(columns = len(params_table.columns), rows = len(params_table_tolist), text = params_table_list)

mdFile.new_header(4, "Derived Parameters")

mdFile.new_table(columns = len(derived_params_table.columns), rows = len(derived_params_table_tolist), text = derived_params_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Equations of derived parameters</summary>

```math
{RT} =  {T} \cdot {R}
```
```math
{dG_pH} =  \log 10 \cdo{T} {R} {T}
```
```math
{keq_PQH_2} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_QA} {F} + -2 {E0_PQ} {F} + 2 {pH_stroma} \cdot {dG_pH} \right)}}{{{RT}}} \right)
```
```math
{keq_v_FNR} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_Fd} {F} + -2 {E0_NADP} {F} + {dG_pH} \cdot {pH_stroma} \right)}}{{{RT}}} \right)
```
```math
{vmax_v_FNR} =  {Enz0_v_FNR} \cdot {kcat_v_FNR}
```
```math
{keq_PCP700} =  \exp \left( \frac{{-\left( -{E0_PC} {F} + -{E0_P700} {F} \right)}}{{{RT}}} \right)
```
```math
{keq_v_Fdred} =  \exp \left( \frac{{-\left( -{E0_FA} {F} + -{E0_Fd} {F} \right)}}{{{RT}}} \right)
```
```math
{vmax_v_Fdred} =  {Enz0_v_Fdred} \cdot {kcat_v_Fdred}
```
```math
{vmax_v_pga_ex} =  {Enz0_IF_3P} \cdot {kcat_IF_3P}
```
```math
{vmax_v_MDAreduct} =  {Enz0_v_MDAreduct} \cdot {kcat_v_MDAreduct}
```
```math
{vmax_v_GR} =  {Enz0_v_GR} \cdot {kcat_v_GR}
```
```math
{vmax_v_DHAR} =  {Enz0_v_DHAR} \cdot {kcat_v_DHAR}
```
```math
{keq_v_ATPsynth} =  {Pi_mol} \cdot \exp \left( \frac{{-\left( {DeltaG0_ATP} - {dG_pH} \cdot {HPR} \cdot \left( {pH_stroma} - {pH_lumen} \right) \right)}}{{{RT}}} \right)
```
```math
{keq_v_b6f} =  \mathrm{{cast}} \left( \mathrm{{float}}, \exp \left( \frac{{-\left( -\left( -2 {F} \cdot {E0_PQ} + 2 {dG_pH} \cdot {pH_lumen} \right) + 2 \cdot -{F} \cdot {E0_PC} + 2 {dG_pH} \cdot \left( {pH_stroma} - {pH_lumen} \right) \right)}}{{{RT}}} \right) \right)
```
```math
{Enz0_rubisco_active} =  {Enz0_rubisco} {E_CBB_active}
```
```math
{vmax_v_RuBisCO_c} =  {Enz0_rubisco_active} \cdot {kcat_v_RuBisCO_c}
```
```math
{Enz0_v_FBPase_active} =  {Enz0_v_FBPase} {E_CBB_active}
```
```math
{vmax_v_FBPase} =  {Enz0_v_FBPase_active} \cdot {kcat_v_FBPase}
```
```math
{Enz0_v_SBPase_active} =  {Enz0_v_SBPase} {E_CBB_active}
```
```math
{vmax_v_SBPase} =  {Enz0_v_SBPase_active} \cdot {kcat_v_SBPase}
```
```math
{Enz0_v_PRKase_active} =  {Enz0_v_PRKase} {E_CBB_active}
```
```math
{vmax_v_PRKase} =  {Enz0_v_PRKase_active} \cdot {kcat_v_PRKase}
```
```math
{Enz0_v_starch_active} =  {Enz0_v_starch} {E_CBB_active}
```
```math
{vmax_v_starch} =  {Enz0_v_starch_active} \cdot {kcat_v_starch}
```

</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(columns = len(rates_table.columns), rows = len(rates_table_tolist), text = rates_table_list)

mdFile.new_paragraph(fr"""

<details>
<summary>Rate equations</summary>

```math
{v_Einact} =  {kf_v_Einact} \cdot {E_CBB_active}
```
```math
{v_Eact} =  {kf_v_Eact} \cdot {E_CBB_inactive} \cdot {TRX_red}
```
```math
{v_3ASC} =  {kf_v_3ASC} \cdot {MDA}^{{2}}
```
```math
{v_DHAR} =  \frac{{{vmax_v_DHAR} \cdot {DHA} \cdot {GSH}}}{{{K} + {km_v_DHAR_DHA} \cdot {GSH} + {km_v_DHAR_GSH} \cdot {DHA} + {DHA} \cdot {GSH}}}
```
```math
{v_Mehler} =  {kMehler} \cdot {Y1} \cdot {O2_lumen}
```
```math
{v_APXase} =  \frac{{{ASC} {H2O2} \cdot {XT}}}{{{ASC} {H2O2} \cdot \left( \frac{{1}}{{{kf3}}} + \frac{{1}}{{{kf5}}} \right) + \frac{{{ASC}}}{{{kf1}}} + \frac{{{H2O2}}}{{{kf4}}} + \frac{{{H2O2} \cdot {kr4}}}{{{kf4} \cdot {kf5}}} + \frac{{{H2O2}}}{{{kf2}}} + \frac{{{H2O2} \cdot {kr2}}}{{{kf2} \cdot {kf3}}} + \frac{{{kr1}}}{{{kf1} \cdot {kf2}}} + \frac{{{kr1} \cdot {kr2}}}{{{kf1} \cdot {kf2} \cdot {kf3}}}}}
```
```math
{v_GR} =  \frac{{{vmax_v_GR} \cdot {NADPH_st} \cdot {GSSG}}}{{{km_v_GR_NADPH_st} \cdot {GSSG} + {km_v_GR_GSSG} \cdot {NADPH_st} + {NADPH_st} \cdot {GSSG} + {km_v_GR_NADPH_st} \cdot {km_v_GR_GSSG}}}
```
```math
{v_MDAreduct} =  \frac{{{vmax_v_MDAreduct} \cdot {NADPH_st} \cdot {MDA}}}{{{km_v_MDAreduct_NADPH_st} \cdot {MDA} + {km_v_MDAreduct_MDA} \cdot {NADPH_st} + {NADPH_st} \cdot {MDA} + {km_v_MDAreduct_NADPH_st} \cdot {km_v_MDAreduct_MDA}}}
```
```math
{v_FdTrReduc} =  {kf_v_FdTrReduc} \cdot {TRX_ox} \cdot {Fd_red}
```
```math
{v_Fdred} =  {vmax_v_Fdred} \cdot {Fd_ox} \cdot {Y1} - \frac{{{vmax_v_Fdred}}}{{{keq_v_Fdred}}} \cdot {Fd_red} \cdot {Y2}
```
```math
{v_NADPHcons} =  {kf_v_NADPHcons} \cdot {NADPH_st}
```
```math
{v_PSI} =  \left( 1 - \m{Y0}thrm{{ps2cs}} \right) \m{Y0}thrm{{pfd}} {Y0}
```
```math
{v_PGMase} =  {kre_v_PGMase} \cdot \left( {G6P} - \frac{{{G1P}}}{{{keq_v_PGMase}}} \right)
```
```math
{v_PGIase} =  {kre_v_PGIase} \cdot \left( {F6P} - \frac{{{G6P}}}{{{keq_v_PGIase}}} \right)
```
```math
{v_RPEase} =  {kre_v_RPEase} \cdot \left( {X5P} - \frac{{{RU5P}}}{{{keq_v_RPEase}}} \right)
```
```math
{v_Rpiase} =  {kre_v_Rpiase} \cdot \left( {R5P} - \frac{{{RU5P}}}{{{keq_v_Rpiase}}} \right)
```
```math
{v_TKase_R5P} =  {kre_v_TKase_R5P} \cdot \left( {GAP} \cdot {S7P} - \frac{{{R5P} \cdot {X5P}}}{{{keq_v_TKase_R5P}}} \right)
```
```math
{v_Aldolase_SBP} =  {kre_v_Aldolase_SBP} \cdot \left( {DHAP} \cdot {E4P} - \frac{{{SBP}}}{{{keq_v_Aldolase_SBP}}} \right)
```
```math
{v_TKase_E4P} =  {kre_v_TKase_E4P} \cdot \left( {GAP} \cdot {F6P} - \frac{{{E4P} \cdot {X5P}}}{{{keq_v_TKase_E4P}}} \right)
```
```math
{v_Aldolase_FBP} =  {kre_v_Aldolase_FBP} \cdot \left( {GAP} \cdot {DHAP} - \frac{{{FBP}}}{{{keq_v_Aldolase_FBP}}} \right)
```
```math
{v_TPIase} =  {kre_v_TPIase} \cdot \left( {GAP} - \frac{{{DHAP}}}{{{keq_v_TPIase}}} \right)
```
```math
{v_BPGAdehynase} =  {kre_v_BPGAdehynase} \cdot \left( {BPGA} \cdot {NADPH_st} \cdot {H_stroma} - \frac{{{GAP} \cdot {NADP_st} \cdot {Pi_st}}}{{{keq_v_BPGAdehynase}}} \right)
```
```math
{v_PGK1ase} =  {kre_v_PGK1ase} \cdot \left( {PGA} \cdot {ATP_st} - \frac{{{BPGA} \cdot {ADP_st}}}{{{keq_v_PGK1ase}}} \right)
```
```math
{v_starch} =  \frac{{{vmax_v_starch} \cdot {G1P} \cdot {ATP_st}}}{{\left( {G1P} + {km_v_starch_G1P} \right) \left( \left( 1 + \frac{{{ADP_st}}}{{{ki_v_starch}}} \right) \left( {ATP_st} + {km_v_starch_ATP_st} \right) + \frac{{{km_v_starch_ATP_st} \cdot {Pi_st}}}{{{ki_v_starch_PGA} \cdot {PGA} + {ki_v_starch_F6P} \cdot {F6P} + {ki_v_starch_FBP} \cdot {FBP}}} \right)}}
```
```math
{v_gap_ex} =  \frac{{{vmax_v_pga_ex} \cdot {GAP}}}{{{IF_3P} \cdot {km_v_gap_ex}}}
```
```math
{v_dhap_ex} =  \frac{{{vmax_v_pga_ex} \cdot {DHAP}}}{{{IF_3P} \cdot {km_v_dhap_ex}}}
```
```math
{v_pga_ex} =  \frac{{{vmax_v_pga_ex} \cdot {PGA}}}{{{IF_3P} \cdot {km_v_pga_ex}}}
```
```math
{v_PRKase} =  \frac{{{vmax_v_PRKase} \cdot {RU5P} \cdot {ATP_st}}}{{\left( {RU5P} + {km_v_PRKase_RU5P} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_PRKase_PGA}}} + \frac{{{RUBP}}}{{{ki_v_PRKase_RUBP}}} + \frac{{{Pi_st}}}{{{ki_v_PRKase_Pi_st}}} \right) \right) \left( {ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_PRKase_4}}} \right) + {km_v_PRKase_ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_PRKase_5}}} \right) \right)}}
```
```math
{v_SBPase} =  \frac{{{vmax_v_SBPase} \cdot {SBP}}}{{{SBP} + {km_v_SBPase_s} \cdot \left( 1 + \frac{{{Pi_st}}}{{\mathrm{{k{Pi_st}}}}} \r{Pi_st}ght)}}
```
```math
{v_FBPase} =  \frac{{{vmax_v_FBPase} \cdot {FBP}}}{{{FBP} + {km_v_FBPase_s} \cdot \left( 1 + \frac{{{F6P}}}{{{ki_v_FBPase_F6P}}} + \frac{{{Pi_st}}}{{{ki_v_FBPase_Pi_st}}} \right)}}
```
```math
{v_RuBisCO_c} =  \frac{{{vmax_v_RuBisCO_c} \cdot {RUBP} \cdot {CO2}}}{{\left( {RUBP} + {km_v_RuBisCO_c_RUBP} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_RuBisCO_c_PGA}}} + \frac{{{FBP}}}{{{ki_v_RuBisCO_c_FBP}}} + \frac{{{SBP}}}{{{ki_v_RuBisCO_c_SBP}}} + \frac{{{Pi_st}}}{{{ki_v_RuBisCO_c_Pi_st}}} + \frac{{{NADPH_st}}}{{{ki_v_RuBisCO_c_NADPH_st}}} \right) \right) \left( {CO2} + {km_v_RuBisCO_c_CO2} \right)}}
```
```math
{v_PsbSD} =  {kf_v_PsbSD} \cdot {PsbSP}
```
```math
{v_Epox} =  {kf_v_Epox} \cdot {Zx}
```
```math
{v_Deepox} =  {kf_v_Deepox} \cdot \frac{{{H_lumen}^{{\mathrm{{n{H_lumen}}}}}}}{{{H_lumen}^{{\mathrm{{n{H_lumen}}}}} + \left( \mathrm{{protons\_stroma}} \left( {ksat_v_Deepox} \right) \right)^{{\mathrm{{n{H_lumen}}}}}}} {Vx}
```
```math
{v_St12} =  {kStt7} \cdot \frac{{1}}{{1 + \left( \frac{{\frac{{{PQ}}}{{{PQ_tot}}}}}{{{km_v_St12}}} \right)^{{{n_ST}}}}} {LHC}
```
```math
{v_St21} =  {kPph1} \cdot {LHCp}
```
```math
{v_Cyc} =  {kf_v_Cyc} \cdot {Fd_red}^{{2}} \cdot {PQ}
```
```math
{v_NDH} =  {kf_v_NDH} \cdot {PQ}
```
```math
{v_FNR} =  \frac{{{vmax_v_FNR} \cdot \left( \left( \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \frac{{\frac{{{NADP_st}}}{{{convf}}}}}{{{km_v_FNR_NADP_st}}} - \frac{{\left( \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \frac{{\frac{{{NADPH_st}}}{{{convf}}}}}{{{km_v_FNR_NADP_st}}}}}{{{keq_v_FNR}}} \right)}}{{\left( 1 + \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} + \left( \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \right) \left( 1 + \frac{{\frac{{{NADP_st}}}{{{convf}}}}}{{{km_v_FNR_NADP_st}}} \right) + \left( 1 + \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} + \left( \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \right) \left( 1 + \frac{{\frac{{{NADPH_st}}}{{{convf}}}}}{{{km_v_FNR_NADP_st}}} \right) - 1}}
```
```math
{v_b6f} =  \mathrm{{cast}} \left( \mathrm{{float}}, \mathrm{{np}}.\mathrm{{maximum}} \left( {kcat_v_b6f} \cdot \left( {PQH_2} \cdot {PC_ox}^{{2}} - \frac{{{PQ} \cdot {PC_red}^{{2}}}}{{{keq_v_b6f}}} \right), -{kcat_v_b6f} \right) \right)
```
```math
{v_PsbSP} =  \mat{H_lumen}rm{{k\_fwd}} \cdot \frac{{{H_lumen}^{{\mat{H_lumen}rm{{n{H_lumen}}}}}}}{{{H_lumen}^{{\mat{H_lumen}rm{{n{H_lumen}}}}} + \left( \mat{H_lumen}rm{{protons\_stroma}} \left( \mat{H_lumen}rm{{k\_p{H_lumen}\_sat}} \rig{H_lumen}t) \rig{H_lumen}t)^{{\mat{H_lumen}rm{{n{H_lumen}}}}}}} {psbS}
```
```math
{v_ATPcons} =  {kf_v_ATPcons} \cdot {ATP_st}
```
```math
{v_Leak} =  {kf_v_Leak} \cdot \left( {H_lumen} - \mathrm{{protons\_stroma}} \left( {pH_stroma} \right) \right)
```
```math
{v_ATPsynth} =  {kf_v_ATPsynth} \cdot \left( \frac{{{ADP_st}}}{{{convf}}} - \frac{{\frac{{{ATP_st}}}{{{convf}}}}}{{{keq_v_ATPsynth}}} \right)
```
```math
{v_PQ} =  {kPTOX} \cdot {PQH_2} \cdot {O2_lumen}
```
```math
{v_PSII} =  0.5 {k2} \cdot {B1}
```

</details>

                     """)

mdFile.new_header(3, "Figures")

mdFile.new_paragraph("""You can find the recreation of the figures from the original publication below. Due to differing copyright reasons the original figures cannot be included in this README file. Instead, the comparision has to be made using the original publication.""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 2</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/{model_title.lower()}_fig2.svg'>

The generic Pulse Amplitude Modulation (PAM) protocol starts with a 4 min dark period with a saturating pulse at the 2 min mark. At the end of the dark period, another saturating pulse indicates the start of an actinic light period that goes on for 10 min, with saturating pulses every 2 min. Then another dark period of 18 min starts, again with a saturating pulse at the start and at each 2 min mark. The light intensity used for the actinic light period is $1000 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$, while the dark periods are $40 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. Each saturating pulse was simulated for 0.8 s at a light intensity of $5000 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. The simulation is run using the default parameters and initial conditions of the model, except for the reaction rate constant of cyclic electron flow (kcyc) (= 0) to match an organism with no cyclic electron flow. The values of light intensity were inputted directly to the Photosynthetic Photon Flux Density (PPFD) parameter of the model. The results shown are the fluorescence (F) which was normalized to the maximum value of that series (red), and the Non-Photochemical Quenching (NPQ) (black), which was calculated by using the F and maximal fluorescence (Fm).

This figure could successfully be recreated.
</details>
""")

mdFile.new_paragraph(fr"""
                     
<details>
<summary>Figure 3</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/{model_title.lower()}_fig3.svg'>

The model was simulated to steady-state under different Photosynthetic Photon Flux Density (PPFD) values, ranging from $50 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ to $1500 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$. The results are separated in two different plots, differentiating between photosynthetic electron fluxes and the energy and redox status. The left side shows the PSI rate (vPSI) (blue), the Linear Electron Flow (LEF) (orange, and calculated by doubling the PSII rate (vPSII)), the rate of the cyclic electron flow (vcyc) (green), the mehler reaction lumping the reduction of O2 instead of Fd (vmehler) (red and dashed), and the oxidation of the PQ pool through cytochrome and PTOX (vPQox ) (red and dotted). On the right side the ratios of Adenosine Triphosphate (ATP) (blue), Nicotinamide Adenine Dinucleotide Phosphate (NADPH) (orange), reduced ferredoxin (Fdred) (green), reduced plastoquinone (PQred) (red), and reduced plastocyanin (PCred) (purple) to their total pools are shown. Additionally the concentration of hydrogen peroxide (H2O2) (red, dashed) is also plotted. The simulation is run using the default parameters and initial conditions of the model, while changing only the Photosynthetic Photon Flux Density (PPFD) to the desired value for each simulation.

This figure could successfully be recreated.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 4</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/{model_title.lower()}_fig4.svg'>

The model was simulated to steady-state under different reaction rate constant of cyclic electron flow (kcyc) values representing log2-fold changes ranging from negative three to three. The results are separated in two different plots, differentiating between photosynthetic electron fluxes and the energy and redox status. The top plot shows the PSI rate (vPSI) (blue), the Linear Electron Flow (LEF) (orange, and calculated by doubling the PSII rate (vPSII)), the rate of the cyclic electron flow (vcyc) (green), and the concentration of hydrogen peroxide (H2O2) (red). In the bottom plot the ratios of Adenosine Triphosphate (ATP) (blue), Nicotinamide Adenine Dinucleotide Phosphate (NADPH) (orange), reduced ferredoxin (Fdred) (green), reduced plastoquinone (PQred) (red), and reduced plastocyanin (PCred) (purple) to their total pools are shown. The simulation is run at a Photosynthetic Photon Flux Density (PPFD) of $1000 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$, otherwise using the default parameters and initial conditions of the model, while changing only the kcyc to the desired value for each simulation. Due to issues of singular ranges of kcyc not being able to be simulated to steady-state, only a few values could actually be plotted, to bee seen by the jaggedness of the lines.

This figure shows the correct trends, but the parameter range, where limit cycle oscillations of the reaction rate constant of cyclic electron flow (kcyc) parameter were observed, could not be recreated. This issue made it therefore impossible to fully recreate the figure, which is why the lines in the recreation are much more jagged than in the publication.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/{model_title.lower()}_fig5.svg'>

A simple fluctuating light protocol was used to simulate a wildtype (black) and a knockout mutant (red) of the model. The protocol undergoes a total of 10 periods, each of them lasting 1 min. The light intensities of the periods alternate between light and dark, using a light intensity of $600 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ and $40 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$, respectively. The wildtype simulation was run using the default parameters and initial conditions of the model, while the knockout mutant was simulated by setting the reaction rate constant of cyclic electron flow (kcyc) to zero. Each light intensity was inputted into the Photosynthetic Photon Flux Density (PPFD) parameter of the models. The results shown are the ratio of reduced ferredoxin (Fdred) to its total pool on the left, and the RuBisCO carboxylation rate (vRuBisCO) on the right.

This figure could successfully be recreated.

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Figure 6</summary>
                     
<img style='display: block; margin: 0 auto' src='figures/{model_title.lower()}_fig6.svg'>

A Metabolic Control Analysis (MCA) was done to the model under two different light intensities, $100 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ (top) and $1000 \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ (bottom). The results of the fluxes can be found on the left, while on the right are the variables. The parameters that were used for the MCA are the control coefficients of the fluxes with the same names. The following were used, given from left to right on the x-axis of each heatmap: total PSII reaction centers (PSIItot), total PSI (PSItot), rate constant of the cytochrome b6f complex reaction (kCytb6f), reaction rate constant of cyclic electron flow (kcyc), estimated rate constant for summarized hydrogen peroxide production (kMehler), catalytic rate constant of RuBisCO for carboxylation (kRuBisCO), catalytic rate constant of FBPase (kFBPase), catalytic rate constant of SBPase (kSBPase), turnover rate of monodehydroascorbate reductase (kMDAR), and turnover rate of dehydroascorbate reductase (kDHAR). These parameters were displaced by ±1%. The simulations were otherwise done using the default parameters and initial conditions of the model, while changing only the Photosynthetic Photon Flux Density (PPFD) to the desired value for each simulation.

This figure could successfully be recreated.

</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 7</summary>
                     
The seventh figure of the publication includes the same parameter range as the fourth figure, therefore the same issue is observed in the recreation. However in this case, the recreation could not be completed at all, as the specific range of the rate constant of the cyclic electron flow parameter where these oscillations are found is not well documented.

</details>
""")

mdFile.new_header(3, "Demonstrations")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle using real Photosynthetic Photon Flux Density (PPFD) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal and is used to create a protocol for the light intensity PPFD over the course of the day, in a minute interval. The data used is filtered to only show a PPFD that equals or is higher than $40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$. This threshold is chosen as it has shown to allow most models to still simulate the photosynthetic machinery, while still being a decent representation of the actual daylight conditions. The simulation is run using the default parameters and initial conditions of each model, and the RuBisCO carboxylation rate (vRuBisCO), Adenosine Triphosphate (ATP) and Nicotinamide Adenine Dinucleotide Phosphate (NADPH) ratio, and fluorescence (F) results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>FvCB Submodule</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_fvcb.svg' alt='FvCB Submodule' width='600'/>

Comparison of modelled carbon assimilation (A) and RuBisCO carboxylation rate (vRuBisCO) against the Farquhar, von Caemmerer, and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025). To be able to simulate A, there are two mandatory quantities that need to be present in the model: carbon dioxide (CO2) concentration and vRuBisCO. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The simulation is then run until steady-state, or quasi-steady-state if not otherwise possible, for different intercellular CO2 concentration (Ci) partial pressure. The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model.

**Assumptions:**

- If no CO<sub>2</sub> concentration nor rate of rubisco carboxylation ($v_\mathrm{{c}}$) is present in the model, no comparison will be shown
- Infinite mesophyll conductance, therefore intercellular CO<sub>2</sub> partial pressure equals chloroplast partial pressure ($\mathrm{{C_i}} = \mathrm{{C_c}}$)
- If no $\mathrm{{C_i}}$ is present in the model, it will be added as a parameter assuming an initial value of CO<sub>2</sub> concentration divided by Henry's law constant for CO<sub>2</sub> ($H_\mathrm{{s}}^{{cp}}$)
- If no $H_\mathrm{{s}}^{{cp}}$ is present in the model, it will be added as a parameter with a value of $3.4 \times 10^{{-4}}\ \mathrm{{mmol\ Pa^ {{-1}}}}$ [[2]](https://doi.org/10.5194/acp-23-10901-2023)
- If no CO<sub>2</sub> compensation point in the absence of non-photorespiratory CO<sub>2</sub> release ($\Gamma ^*$) is present in the model, it will be added as a parameter with a value of $38.6\ \mathrm{{\mu bar}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $R_\mathrm{{light}}$ is present in the model, it will be added as a parameter with a value of $1\ \mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $A$ is present in the model, it will be added as a derived variable following the FvCB equation [[1]](https://doi.org/10.1101/2025.03.11.642611): $v_\mathrm{{c}} \cdot \left(1 - \frac{{\Gamma ^*}}{{C_i}}\right) - R_\mathrm{{light}}$
- To be able to compare with original FvCB curves, the model needs to have $v_\mathrm{{c}}$ following the same units as the FvCB model ($\mathrm{{\mu mol\ m^{{-2}}\ s^{{-1}}}}$). The `mM_to_µmol_per_m2` can be used to convert from mM to $\mathrm{{\mu mol\ m^{{-2}}}}$ assuming a volume factor of $0.0112\ \mathrm{{L\ m^{{-2}}}}$ in the stroma [[3]](https://doi.org/10.1007/s11120-006-9109-1). If the given units are in mM, the conversion will be done automatically, by adding a derived parameter with the converted values.

**Notes:**

| Parameter                 | In Model          |
| -----------               | -----------       |
| $\mathrm{{CO}}_2$         | {CO2}          |
| $v_\mathrm{{c}}$          | {v_RuBisCO_c}  |
| $\mathrm{{C_i}}$          | None          |
| $H_\mathrm{{s}}^{{cp}}$   | None              |
| $\Gamma ^*$               | None              |
| $R_\mathrm{{light}}$      | None        |
| $A$                       | None            |


</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>PAM Simulation</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_pam.svg' alt='PAM Simulation' width='600'/>

A sample Metabolic Control Analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent  RuBisCO carboxylation rate (vRuBisCO), PSII rate (vPSII), PSI rate (vPSI), Cytb6f rate (vb6f) and ATP synthase rate (vATPSynth). The variables chosen should represent  carbon dioxide (CO2) concentration, Ribulose-1,5-bisphosphate (RuBP), oxidised plastoquinone (PQox), oxidised plastocyanin (PCox), denosine Triphosphate (ATP), and Nicotinamide Adenine Dinucleotide Phosphate (NADPH). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.01\%$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{{p}}^{{x}} = \frac{{x_\mathrm{{upper}} - x_\mathrm{{lower}}}}{{2 \cdot \mathrm{{disp}} \cdot p}}$, where $C_{{p}}^{{x}}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{{disp}}$ is the displacement value. $x_\mathrm{{upper}}$ and $x_\mathrm{{lower}}$ are the steady-state result of $x$ at either $+\mathrm{{disp}}$ and $-\mathrm{{disp}}$ respectively. It has to be noted that the (MCA) results can be very dependent on the other values of the parameters in the model, therefore the results shown here are only representative of the default parameter set of the model.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{{m}}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{{m}}$.
- If $F_\mathrm{{m}}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{{F_{{\mathrm{{m}}\vert t=0}} - F_{{\mathrm{{m}} \vert t}}}}{{F_{{\mathrm{{m}} \vert t}}}}$

**Notes:**

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>Photosynthesis MCA</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_mca.svg' alt='Photosynthesis MCA' width='600'/>

Sample fitting to experimental Non-Photochemical Quenching (NPQ) data. The NPQ data used is taken from experimental work published in von Bismarck (2022) and was acquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana (A. thaliana) plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 µs at a light intensity of $5000 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light ($903 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$) for approximately 10 minutes, followed by a lower actinic light of ($90 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of $40 \mathrm{{µmol\ m^{{−2}}\ s^{{−1}}}}$ is used to avoid numerical issues. The fitting is performed using the lmfit package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help the fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parameters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- Steady-State needs to be achievable for the model to perform the MCA.
- The parameters for each coefficient, rates, and variables chosen need to be representative of the respective process.
- If a parameter, rate, or variable is not present in the model, the respective coefficient will be greyed out in the Heatmap.

**Notes:**

| Coefficient                   | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | {k2}|
| $\mathrm{{PSI}}$              | None |
| $\mathrm{{RuBisCO \vert C}}$  | {kcat_v_RuBisCO_c} |
| $\mathrm{{cytb6f}}$           | {kcat_v_b6f}              |
| $\mathrm{{ATPsynthase}}$      | {kf_v_ATPsynth}              |

| Flux                          | In Model          |
| -----------                   | -----------       |
| $\mathrm{{PSII}}$             | {v_PSII} |
| $\mathrm{{PSI}}$              | {v_PSI} |
| $\mathrm{{RuBisCO \vert C}}$  | {v_RuBisCO_c} |
| $\mathrm{{cytb6f}}$           | {v_b6f}              |
| $\mathrm{{ATPsynthase}}$      | {v_ATPsynth}              |

| Variable                  | In Model      |
| -----------               | -----------   |
| $\mathrm{{CO_2}}$         | {CO2}       |
| $\mathrm{{RUBP}}$         | {RUBP}      |
| $\mathrm{{PQ_{{ox}}}}$    | {PQ}          |
| $\mathrm{{PC_{{ox}}}}$    | {PC_ox}          |
| $\mathrm{{ATP}}$          | {ATP_st}    |
| $\mathrm{{NADPH}}$        | {NADPH_st}  |

</details>
""")

mdFile.new_paragraph(rf"""
                     
<details>
<summary>PAM Fitting</summary>
                     
<img style='float: center' src='figures/{model_title.lower()}_demon_fitting.svg' alt='PAM Fitting' width='600'/>

Sample fitting to experimental NPQ data. The NPQ data used is taken from experimental work published in ([https://doi.org/10.1111/nph.18534](https://doi.org/10.1111/nph.18534)) and was aquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 ms at a light intensity of 5000 µmol m⁻² s⁻¹. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light (903 µmol m⁻² s⁻¹) for approximately 10 minutes, followed by a lower actinic light of (90 µmol m⁻² s⁻¹) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of 40 µmol m⁻² s⁻¹ is used to avoid numerical issues. The fitting is performed using the `lmfit`package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parmaters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{{m}}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{{m}}$.
- If $F_\mathrm{{m}}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{{F_{{\mathrm{{m}}\vert t=0}} - F_{{\mathrm{{m}} \vert t}}}}{{F_{{\mathrm{{m}} \vert t}}}}$

**Notes:**

{ksat_v_Deepox}, {gamma0}, and {ksat_v_PsbSP} were fitted.

</details>
""")

mdFile.create_md_file()
