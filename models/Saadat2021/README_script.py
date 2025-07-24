from pathlib import Path

from mdutils.mdutils import MdUtils  # noqa: E402

from GreenSlothUtils import gloss_fromCSV, remove_math

###### Util Functions ######


def ode(first_var: str, second_var: str = "t") -> str:
    for i in [first_var, second_var]:
        if "$" in i:
            msg = f"Your given variable '{i}' has a '$' in it"
            raise ValueError(msg)

    return rf"\frac{{\mathrm{{d}}{first_var}}}{{\mathrm{{d}}{second_var}}}"


###### Model Infos ######

model_title = "Saadat2021"
model_doi = "ENTER HERE"

###### Glossaries ######

cite_dict = {}

model_info = Path(__file__).parent / "model_info"
python_written = model_info / "python_written"

comps_table, comps_table_tolist, comps_table_list = gloss_fromCSV(
    path=model_info / "comps.csv", omit_col="Glossary ID"
)

derived_comps_table, derived_comps_table_tolist, derived_comps_table_list = (
    gloss_fromCSV(path=model_info / "derived_comps.csv", omit_col="Glossary ID")
)

rates_table, rates_table_tolist, rates_table_list = gloss_fromCSV(
    path=model_info / "rates.csv", omit_col="Glossary ID"
)

params_table, params_table_tolist, params_table_list = gloss_fromCSV(
    path=model_info / "params.csv", cite_dict=cite_dict
)

derived_params_table, derived_params_table_tolist, derived_params_table_list = (
    gloss_fromCSV(model_info / "derived_params.csv")
)

###### Variables for ease of access ######

# -- Compounds --

PGA = remove_math(comps_table, r"$\mathrm{PGA}$")
BPGA = remove_math(comps_table, r"$\mathrm{BPGA}$")
GAP = remove_math(comps_table, r"$\mathrm{GAP}$")
DHAP = remove_math(comps_table, r"$\mathrm{DHAP}$")
FBP = remove_math(comps_table, r"$\mathrm{FBP}$")
F6P = remove_math(comps_table, r"$\mathrm{F6P}$")
G6P = remove_math(comps_table, r"$\mathrm{G6P}$")
G1P = remove_math(comps_table, r"$\mathrm{G1P}$")
SBP = remove_math(comps_table, r"$\mathrm{SBP}$")
S7P = remove_math(comps_table, r"$\mathrm{S7P}$")
E4P = remove_math(comps_table, r"$\mathrm{E4P}$")
X5P = remove_math(comps_table, r"$\mathrm{X5P}$")
R5P = remove_math(comps_table, r"$\mathrm{R5P}$")
RUBP = remove_math(comps_table, r"$\mathrm{RUBP}$")
RU5P = remove_math(comps_table, r"$\mathrm{RU5P}$")
ATP_st = remove_math(comps_table, r"$\mathrm{ATP}$")
Fd_ox = remove_math(comps_table, r"$\mathrm{Fd}_\mathrm{ox}$")
H_lumen = remove_math(comps_table, r"$\mathrm{H}^+$")
LHC = remove_math(comps_table, r"$\mathrm{LHC}$")
NADPH_st = remove_math(comps_table, r"$\mathrm{NADPH}$")
PC_ox = remove_math(comps_table, r"$\mathrm{PC}_\mathrm{ox}$")
PQ = remove_math(comps_table, r"$\mathrm{PQ}_\mathrm{ox}$")
psbS = remove_math(comps_table, r"$\mathrm{Psbs}$")
Vx = remove_math(comps_table, r"$\mathrm{Vx}$")
MDA = remove_math(comps_table, r"$\mathrm{MDA}$")
H2O2 = remove_math(comps_table, r"$\mathrm{H_2O_2}$")
DHA = remove_math(comps_table, r"$\mathrm{DHA}$")
GSSG = remove_math(comps_table, r"$\mathrm{GSSG}$")
TRX_ox = remove_math(comps_table, r"$\mathrm{Trx_{ox}}$")
E_CBB_inactive = remove_math(comps_table, r"$\mathrm{E}_\mathrm{inactive}$")

# -- Derived Compounds --

pH_lumen = remove_math(derived_comps_table, r"$\mathrm{pH}_\mathrm{lumen}$")
Zx = remove_math(derived_comps_table, r"$\mathrm{Zx}$")
Fd_red = remove_math(derived_comps_table, r"$\mathrm{Fd}^-$")
PC_red = remove_math(derived_comps_table, r"$\mathrm{PC}^-$")
PsbSP = remove_math(derived_comps_table, r"$\mathrm{PsbS^P}$")
LHCp = remove_math(derived_comps_table, r"$\mathrm{LHCp}$")
Q = remove_math(derived_comps_table, r"$\mathrm{Q}$")
PQH_2 = remove_math(derived_comps_table, r"$\mathrm{PQH}_2$")
psIIcross = remove_math(derived_comps_table, r"$\mathrm{PSII_{cross}}$")
TRX_red = remove_math(derived_comps_table, r"$\mathrm{Trx_{red}}$")
E_CBB_active = remove_math(derived_comps_table, r"$\mathrm{E}_\mathrm{cbb,\ inactive}$")
NADP_st = remove_math(derived_comps_table, r"$\mathrm{NADP}^+$")
ADP_st = remove_math(derived_comps_table, r"$\mathrm{ADP}$")
Pi_st = remove_math(derived_comps_table, r"$\mathrm{P}_\mathrm{i}$")
ASC = remove_math(derived_comps_table, r"$\mathrm{ASC}$")
GSH = remove_math(derived_comps_table, r"$\mathrm{GSH}$")
IF_3P = remove_math(derived_comps_table, r"$\mathrm{N}$")
B0 = remove_math(derived_comps_table, r"$\mathrm{B_0}$")
B1 = remove_math(derived_comps_table, r"$\mathrm{B_1}$")
B2 = remove_math(derived_comps_table, r"$\mathrm{B_2}$")
B3 = remove_math(derived_comps_table, r"$\mathrm{B_3}$")
Y0 = remove_math(derived_comps_table, r"$\mathrm{Y_0}$")
Y1 = remove_math(derived_comps_table, r"$\mathrm{Y_1}$")
Y2 = remove_math(derived_comps_table, r"$\mathrm{Y_2}$")
Fluo = remove_math(derived_comps_table, r"$\mathrm{Fluo}$")

# -- Rates --

v_Einact = remove_math(rates_table, r"$v_{\mathrm{Einact}}$")
v_Eact = remove_math(rates_table, r"$v_{\mathrm{Eact}}$")
v_3ASC = remove_math(rates_table, r"$v_{\mathrm{3ASC}}$")
v_DHAR = remove_math(rates_table, r"$v_{\mathrm{DHAR}}$")
v_Mehler = remove_math(rates_table, r"$v_{\mathrm{Mehler}}$")
v_APXase = remove_math(rates_table, r"$v_{\mathrm{Ascorbate}}$")
v_GR = remove_math(rates_table, r"$v_{\mathrm{GR}}$")
v_MDAreduct = remove_math(rates_table, r"$v_{\mathrm{MDAreduct}}$")
v_FdTrReduc = remove_math(rates_table, r"$v_{\mathrm{FdTrReductase}}$")
v_Fdred = remove_math(rates_table, r"$v_{\mathrm{Fd,\ red}}$")
v_NADPHcons = remove_math(rates_table, r"$v_{\mathrm{EX\_ NADPH}}$")
v_PSI = remove_math(rates_table, r"$v_{\mathrm{PSI}}$")
v_PGMase = remove_math(rates_table, r"$v_{\mathrm{Phosphoglucomutase}}$")
v_PGIase = remove_math(rates_table, r"$v_{G6P\_ isomerase}$")
v_RPEase = remove_math(rates_table, r"$v_{12}$")
v_Rpiase = remove_math(rates_table, r"$v_{11}$")
v_TKase_R5P = remove_math(rates_table, r"$v_{10}$")
v_Aldolase_SBP = remove_math(rates_table, r"$v_{8}$")
v_TKase_E4P = remove_math(rates_table, r"$v_{\mathrm{F6P\_ Transketolase}}$")
v_Aldolase_FBP = remove_math(rates_table, r"$v_{\mathrm{Aldolase}}$")
v_TPIase = remove_math(rates_table, r"$v_{\mathrm{TPI}}$")
v_BPGAdehynase = remove_math(rates_table, r"$v_{\mathrm{BPGA\_dehydrogenase}}$")
v_PGK1ase = remove_math(rates_table, r"$v_{\mathrm{PGA\_kinase}}$")
v_starch = remove_math(rates_table, r"$v_{\mathrm{Starch}}$")
v_gap_ex = remove_math(rates_table, r"$v_{gap}$")
v_dhap_ex = remove_math(rates_table, r"$v_{DHAP}$")
v_pga_ex = remove_math(rates_table, r"$v_{pga}$")
v_PRKase = remove_math(rates_table, r"$v_{13}$")
v_SBPase = remove_math(rates_table, r"$v_9$")
v_FBPase = remove_math(rates_table, r"$v_{\mathrm{FBPase}}$")
v_RuBisCO_c = remove_math(rates_table, r"$v_{\mathrm{RuBisCo}}$")
v_PsbSD = remove_math(rates_table, r"$v_{\mathrm{LHCdeprotonation}}$")
v_Epox = remove_math(rates_table, r"$v_{\mathrm{Epox}}$")
v_Deepox = remove_math(rates_table, r"$v_{\mathrm{Deepox}}$")
v_St12 = remove_math(rates_table, r"$v_{\mathrm{St21}}$")
v_St21 = remove_math(rates_table, r"$v_{\mathrm{St12}}$")
v_Cyc = remove_math(rates_table, r"$v_{\mathrm{Cyc}}$")
v_NDH = remove_math(rates_table, r"$v_{\mathrm{NDH}}$")
v_FNR = remove_math(rates_table, r"$v_{\mathrm{FNR}}$")
v_b6f = remove_math(rates_table, r"$v_{\mathrm{b6f}}$")
v_PsbSP = remove_math(rates_table, r"$v_{\mathrm{LHCprotonation}}$")
v_ATPcons = remove_math(rates_table, r"$v_{\mathrm{EX\_ ATP}}$")
v_Leak = remove_math(rates_table, r"$v_{\mathrm{Leak}}$")
v_ATPsynth = remove_math(rates_table, r"$v_{\mathrm{ATPsynthase}}$")
v_PQ = remove_math(rates_table, r"$v_{\mathrm{PTOX}}$")
v_PSII = remove_math(rates_table, r"$v_{\mathrm{PSII}}$")

# -- Parameters --

PPFD = remove_math(params_table, r"$\mathrm{PFD}$")
CO2 = remove_math(params_table, r"$\mathrm{CO}_2$")
O2_lumen = remove_math(params_table, r"$\mathrm{O}_2^\mathrm{ex}$")
pH_stroma = remove_math(params_table, r"$\mathrm{pH}_\mathrm{stroma}$")
H_stroma = remove_math(params_table, r"$\mathrm{H}_\mathrm{stroma}$")
bH = remove_math(params_table, r"$b_\mathrm{H}$")
F = remove_math(params_table, r"$F$")
E0_PC = remove_math(params_table, r"$E^0\mathrm{(PC/PC^-)}$")
E0_P700 = remove_math(params_table, r"$E^0\mathrm{(P_{700}^+/P_{700})}$")
E0_FA = remove_math(params_table, r"$E^0\mathrm{(FA/FA^-)}$")
E0_Fd = remove_math(params_table, r"$E^0\mathrm{(Fd/Fd^-)}$")
E0_NADP = remove_math(params_table, r"$E^0\mathrm{(NADP^+/NADPH)}$")
convf = remove_math(params_table, r"$\mathrm{convf}$")
R = remove_math(params_table, r"$R$")
T = remove_math(params_table, r"$T$")
Carotenoids_tot = remove_math(params_table, r"$\mathrm{X}^{\mathrm{tot}}$")
Fd_tot = remove_math(params_table, r"$\mathrm{Fd}^{\mathrm{tot}}$")
PC_tot = remove_math(params_table, r"$\mathrm{PC}^{\mathrm{tot}}$")
PSBS_tot = remove_math(params_table, r"$\mathrm{PsbS}^{\mathrm{tot}}$")
LHC_tot = remove_math(params_table, r"")
gamma0 = remove_math(params_table, r"$\gamma_0$")
gamma1 = remove_math(params_table, r"$\gamma_1$")
gamma2 = remove_math(params_table, r"$\gamma_2$")
gamma3 = remove_math(params_table, r"$\gamma_3$")
kZSat = remove_math(params_table, r"$K_\mathrm{ZSat}$")
E0_QA = remove_math(params_table, r"$E^0\mathrm{(QA/QA^-)}$")
E0_PQ = remove_math(params_table, r"$E^0\mathrm{(PQ/PQH_2)}$")
PQ_tot = remove_math(params_table, r"$\mathrm{PQ}^{\mathrm{tot}}$")
staticAntII = remove_math(params_table, r"$\sigma _\mathrm{II} ^0$")
staticAntI = remove_math(params_table, r"$\sigma _\mathrm{I} ^0$")
Thioredoxin_tot = remove_math(params_table, r"$\mathrm{thioredoxin}_\mathrm{tot}$")
E_total = remove_math(params_table, r"$e_{\mathrm{cbb}_\mathrm{tot}}$")
NADP_tot = remove_math(params_table, r"$\mathrm{NADP}^{\mathrm{tot}}$")
AP_tot = remove_math(params_table, r"$\mathrm{AP}^{\mathrm{tot}}$")
Pi_tot = remove_math(params_table, r"$\mathrm{P}^{\mathrm{tot}}$")
kf_v_FdTrReduc = remove_math(
    params_table, r"$k_{\mathrm{fd}_{\mathrm{tr}_\mathrm{reductase}}}$"
)
kf_v_Eact = remove_math(
    params_table, r"$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{activation}}}$"
)
kf_v_Einact = remove_math(
    params_table, r"$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{relaxation}}}$"
)
ASC_tot = remove_math(params_table, r"$\mathrm{Ascorbate}_{\mathrm{total}}$")
Glutathion_tot = remove_math(params_table, r"$\mathrm{Gluthation}_{\mathrm{total}}$")
kf_v_ATPsynth = remove_math(params_table, r"$k_\mathrm{ATPsynthase}$")
HPR = remove_math(params_table, r"$\mathrm{HPR}$")
Pi_mol = remove_math(params_table, r"$\mathrm{Pi}_\mathrm{mol}$")
DeltaG0_ATP = remove_math(params_table, r"$\Delta G_{0_{ATP}}$")
kcat_v_b6f = remove_math(params_table, r"$k_\mathrm{Cytb6f}$")
kh_v_PsbSP = remove_math(params_table, r"$\mathrm{k}_{\mathrm{Hill}_\mathrm{L}}$")
kf_v_PsbSP = remove_math(params_table, r"$k_\mathrm{Protonation}$")
ksat_v_PsbSP = remove_math(params_table, r"$K_\mathrm{pHSatLHC}$")
kf_v_PsbSD = remove_math(params_table, r"$k_\mathrm{Deprotonation}$")
kf_v_Cyc = remove_math(params_table, r"$k_\mathrm{cyc}$")
kf_v_Deepox = remove_math(params_table, r"$k_\mathrm{DeepoxV}$")
kh_v_Deepox = remove_math(params_table, r"$\mathrm{k}_{\mathrm{Hill}_\mathrm{X}}$")
ksat_v_Deepox = remove_math(params_table, r"$K_\mathrm{pHSat}$")
kf_v_Epox = remove_math(params_table, r"$k_\mathrm{EpoxZ}$")
km_v_FNR_Fd_red = remove_math(
    params_table, r"$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{F}}}$"
)
km_v_FNR_NADP_st = remove_math(
    params_table, r"$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{N}}}$"
)
Enz0_v_FNR = remove_math(params_table, r"$\mathrm{EFNR}$")
kcat_v_FNR = remove_math(params_table, r"$k_{\mathrm{cat}_\mathrm{FNR}}$")
kf_v_NDH = remove_math(params_table, r"$k_\mathrm{NDH}$")
PSII_total = remove_math(params_table, r"$\mathrm{PSII}^{\mathrm{tot}}$")
PSI_total = remove_math(params_table, r"$\mathrm{PSI}^{\mathrm{tot}}$")
kH0 = remove_math(params_table, r"$k_{H_0}$")
kPQred = remove_math(params_table, r"$k_{\mathrm{PQ}_\mathrm{red}}$")
kPCox = remove_math(params_table, r"$k_\mathrm{PCox}$")
kFdred = remove_math(params_table, r"$k_{\mathrm{Fd}_\mathrm{red}}$")
k2 = remove_math(params_table, r"$k_2$")
kH = remove_math(params_table, r"$k_H$")
kF = remove_math(params_table, r"$k_F$")
kMehler = remove_math(params_table, r"$k_{\mathrm{Mehler}}$")
Enz0_v_Fdred = remove_math(params_table, r"")
kcat_v_Fdred = remove_math(params_table, r"")
kf_v_Leak = remove_math(params_table, r"$k_\mathrm{leak}$")
kPTOX = remove_math(params_table, r"$k_\mathrm{PTOX}$")
kStt7 = remove_math(params_table, r"$k_\mathrm{Stt7}$")
km_v_St12 = remove_math(params_table, r"$K_{\mathrm{M}_\mathrm{ST}}$")
n_ST = remove_math(params_table, r"$n_\mathrm{ST}$")
kPph1 = remove_math(params_table, r"$k_\mathrm{Pph1}$")
Enz0_rubisco = remove_math(params_table, r"")
kcat_v_RuBisCO_c = remove_math(params_table, r"$V_{1_{\mathrm{base}}}$")
km_v_RuBisCO_c_RUBP = remove_math(params_table, r"$K_{\mathrm{m}1}$")
km_v_RuBisCO_c_CO2 = remove_math(params_table, r"$K_{\mathrm{mCO2}}$")
ki_v_RuBisCO_c_PGA = remove_math(params_table, r"$K_{\mathrm{i}11}$")
ki_v_RuBisCO_c_FBP = remove_math(params_table, r"$K_{\mathrm{i}12}$")
ki_v_RuBisCO_c_SBP = remove_math(params_table, r"$K_{\mathrm{i}13}$")
ki_v_RuBisCO_c_Pi_st = remove_math(params_table, r"$K_{\mathrm{i}14}$")
ki_v_RuBisCO_c_NADPH_st = remove_math(params_table, r"$K_{\mathrm{i}15}$")
kre_v_PGK1ase = remove_math(params_table, r"$k$")
keq_v_PGK1ase = remove_math(params_table, r"$q_2$")
kre_v_BPGAdehynase = remove_math(params_table, r"$k$")
keq_v_BPGAdehynase = remove_math(params_table, r"$q_3$")
kre_v_TPIase = remove_math(params_table, r"$k$")
keq_v_TPIase = remove_math(params_table, r"$q_4$")
kre_v_Aldolase_FBP = remove_math(params_table, r"$k$")
keq_v_Aldolase_FBP = remove_math(params_table, r"$q_5$")
kre_v_Aldolase_SBP = remove_math(params_table, r"$k$")
keq_v_Aldolase_SBP = remove_math(params_table, r"$q_8$")
Enz0_v_FBPase = remove_math(params_table, r"")
kcat_v_FBPase = remove_math(params_table, r"$V_{6_{\mathrm{base}}}$")
km_v_FBPase_s = remove_math(params_table, r"$K_{\mathrm{m}6}$")
ki_v_FBPase_F6P = remove_math(params_table, r"$K_{\mathrm{i}61}$")
ki_v_FBPase_Pi_st = remove_math(params_table, r"$K_{\mathrm{i}62}$")
kre_v_TKase_E4P = remove_math(params_table, r"$k$")
keq_v_TKase_E4P = remove_math(params_table, r"$q_7$")
kre_v_TKase_R5P = remove_math(params_table, r"$k$")
keq_v_TKase_R5P = remove_math(params_table, r"$q_{10}$")
Enz0_v_SBPase = remove_math(params_table, r"")
kcat_v_SBPase = remove_math(params_table, r"$V_{9_{\mathrm{base}}}$")
km_v_SBPase_s = remove_math(params_table, r"$K_{\mathrm{m}9}$")
ki_v_SBPase_Pi_st = remove_math(params_table, r"$K_{\mathrm{i}9}$")
kre_v_Rpiase = remove_math(params_table, r"$k$")
keq_v_Rpiase = remove_math(params_table, r"$q_{11}$")
kre_v_RPEase = remove_math(params_table, r"$k$")
keq_v_RPEase = remove_math(params_table, r"$q_{12}$")
Enz0_v_PRKase = remove_math(params_table, r"")
kcat_v_PRKase = remove_math(params_table, r"$V_{13_{\mathrm{base}}}$")
km_v_PRKase_RU5P = remove_math(params_table, r"$K_{\mathrm{m}131}$")
km_v_PRKase_ATP_st = remove_math(params_table, r"$K_{\mathrm{m}132}$")
ki_v_PRKase_PGA = remove_math(params_table, r"$K_{\mathrm{i}131}$")
ki_v_PRKase_RUBP = remove_math(params_table, r"$K_{\mathrm{i}132}$")
ki_v_PRKase_Pi_st = remove_math(params_table, r"$K_{\mathrm{i}133}$")
ki_v_PRKase_4 = remove_math(params_table, r"$K_{\mathrm{i}134}$")
ki_v_PRKase_5 = remove_math(params_table, r"$K_{\mathrm{i}135}$")
kre_v_PGIase = remove_math(params_table, r"$k$")
keq_v_PGIase = remove_math(params_table, r"$q_{14}$")
kre_v_PGMase = remove_math(params_table, r"$k$")
keq_v_PGMase = remove_math(params_table, r"$q_{15}$")
Pi_ext = remove_math(params_table, r"$\mathrm{P}_\mathrm{ext}$")
km_v_pga_ex = remove_math(params_table, r"$K_{\mathrm{pga}}$")
km_v_gap_ex = remove_math(params_table, r"$K_{\mathrm{gap}}$")
km_v_dhap_ex = remove_math(params_table, r"$K_{\mathrm{dhap}}$")
km_N_translocator_Pi_ext = remove_math(params_table, r"$K_{\mathrm{pxt}}$")
km_N_translocator_Pi_st = remove_math(params_table, r"$K_{\mathrm{pi}}$")
kcat_N_translocator = remove_math(params_table, r"$V_{\mathrm{ex}}$")
Enz0_N_translocator = remove_math(params_table, r"")
Enz0_v_starch = remove_math(params_table, r"")
km_v_starch_G1P = remove_math(params_table, r"$K_{\mathrm{mst}1}$")
km_v_starch_ATP_st = remove_math(params_table, r"$K_{\mathrm{mst}2}$")
ki_v_starch = remove_math(params_table, r"$K_{\mathrm{ist}}$")
ki_v_starch_PGA = remove_math(params_table, r"$K_{\mathrm{ast1}}$")
ki_v_starch_F6P = remove_math(params_table, r"$K_{\mathrm{ast2}}$")
ki_v_starch_FBP = remove_math(params_table, r"$K_{\mathrm{ast3}}$")
kcat_v_starch = remove_math(params_table, r"$V_{\mathrm{st}_{\mathrm{base}}}$")
kf_v_3ASC = remove_math(params_table, r"$k3$")
Enz0_v_MDAreduct = remove_math(params_table, r"$\mathrm{MDAR}_0$")
kcat_v_MDAreduct = remove_math(params_table, r"$k_{\mathrm{cat}_{\mathrm{MDAR}}}$")
km_v_MDAreduct_NADPH_st = remove_math(
    params_table, r"$K_{\mathrm{m}_{\mathrm{MDAR-NADPH}}}$"
)
km_v_MDAreduct_MDA = remove_math(params_table, r"$K_{\mathrm{m}_{\mathrm{MDAR-MDA}}}$")
kf1 = remove_math(params_table, r"$kf1$")
kr1 = remove_math(params_table, r"$kr1$")
kf2 = remove_math(params_table, r"$kf2$")
kr2 = remove_math(params_table, r"$kr2$")
kf3 = remove_math(params_table, r"$kf3$")
kf4 = remove_math(params_table, r"$kf4$")
kr4 = remove_math(params_table, r"$kr4$")
kf5 = remove_math(params_table, r"$kf5$")
XT = remove_math(params_table, r"$XT$")
Enz0_v_GR = remove_math(params_table, r"$\mathrm{GR}_0$")
kcat_v_GR = remove_math(params_table, r"$k_{\mathrm{cat}_{\mathrm{GR}}}$")
km_v_GR_NADPH_st = remove_math(params_table, r"$K_{\mathrm{m}_{\mathrm{NADPH}}}$")
km_v_GR_GSSG = remove_math(params_table, r"$K_{\mathrm{m}_{\mathrm{GSSG}}}$")
km_v_DHAR_DHA = remove_math(params_table, r"$K_{\mathrm{m}_{\mathrm{DHA}}}$")
km_v_DHAR_GSH = remove_math(params_table, r"$K_{\mathrm{m}_{\mathrm{GSH}}}$")
K = remove_math(params_table, r"$K$")
Enz0_v_DHAR = remove_math(params_table, r"$\mathrm{DHAR}_0$")
kcat_v_DHAR = remove_math(params_table, r"$k_{\mathrm{cat}_{\mathrm{DHAR}}}$")
kf_v_ATPcons = remove_math(params_table, r"$k_{\mathrm{ex}_{\mathrm{atp}}}$")
kf_v_NADPHcons = remove_math(params_table, r"$k_{\mathrm{ex}_{\mathrm{nadph}}}$")

# --- Derived Parameters ---

RT = remove_math(derived_params_table, r"$RT$")
dG_pH = remove_math(derived_params_table, r"")
keq_PQH_2 = remove_math(derived_params_table, r"$K_\mathrm{eq, QAPQ}$")
keq_v_FNR = remove_math(derived_params_table, r"$K_\mathrm{eq, FNR}$")
vmax_v_FNR = remove_math(derived_params_table, r"")
keq_PCP700 = remove_math(derived_params_table, r"$K_\mathrm{eq, PCP700}$")
keq_v_Fdred = remove_math(derived_params_table, r"$K_\mathrm{eq, FAFd}$")
vmax_v_Fdred = remove_math(derived_params_table, r"")
vmax_v_pga_ex = remove_math(derived_params_table, r"")
vmax_v_MDAreduct = remove_math(derived_params_table, r"")
vmax_v_GR = remove_math(derived_params_table, r"")
vmax_v_DHAR = remove_math(derived_params_table, r"")
keq_v_ATPsynth = remove_math(derived_params_table, r"$K_\mathrm{eq, ATPsynthase}$")
keq_v_b6f = remove_math(derived_params_table, r"$K_\mathrm{eq, cytb6f}$")
E0_rubisco_active = remove_math(derived_params_table, r"")
vmax_v_RuBisCO_c = remove_math(derived_params_table, r"$V_1$")
E0_v_FBPase_active = remove_math(derived_params_table, r"")
vmax_v_FBPase = remove_math(derived_params_table, r"$V_6$")
E0_v_SBPase_active = remove_math(derived_params_table, r"")
vmax_v_SBPase = remove_math(derived_params_table, r"$V_9$")
E0_v_PRKase_active = remove_math(derived_params_table, r"")
vmax_v_PRKase = remove_math(derived_params_table, r"$V_13$")
E0_v_starch_active = remove_math(derived_params_table, r"")
vmax_v_starch = remove_math(derived_params_table, r"$V_\mathrm{st}$")

###### Making README File ######

mdFile = MdUtils(file_name=f"{Path(__file__).parents[0]}/README.md")  # noqa: N816

mdFile.new_header(1, model_title)

mdFile.new_paragraph(f"""[{model_title}]({model_doi})

                     """)

mdFile.new_header(2, "Installation")

mdFile.new_header(2, "Summary")

mdFile.new_header(3, "Compounds")

mdFile.new_header(4, "Part of ODE system")

mdFile.new_table(
    columns=len(comps_table.columns),
    rows=len(comps_table_tolist),
    text=comps_table_list,
)

mdFile.new_paragraph(rf"""
<details>
<summary>ODE System</summary>

```math
{ode(PQ)} = -1.0 \cdot {v_PSII} + 1.0 \cdot {v_PQ} - 1.0 \cdot {v_NDH} + 1.0 \cdot {v_b6f} - 1.0 \cdot {v_Cyc}
```
```math
{ode(H_lumen)} = \frac{{1}}{{{bH}}} \cdot \left( 2 \cdot {v_PSII} + 4 \cdot {v_b6f} - {HPR} \cdot {v_ATPsynth} - {v_Leak} \right)
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
{ode(PGA)} = -1.0 \cdot {v_PGK1ase} - 1.0 \cdot {v_pga_ex} + 2.0 \cdot {v_RuBisCO_c}
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
{ode(RUBP)} = 1.0 \cdot {v_PRKase} - 1.0 \cdot {v_RuBisCO_c}
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

mdFile.new_header(4, "Conserved quantities")

mdFile.new_table(
    columns=len(derived_comps_table.columns),
    rows=len(derived_comps_table_tolist),
    text=derived_comps_table_list,
)

mdFile.new_paragraph(rf"""

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
{Zx} = {Carotenoids_tot} - {Vx}
```
```math
{PsbSP} = {PSBS_tot} - {psbS}
```
```math
{psIIcross} =  {staticAntII} + \left( 1 - {staticAntII} - {staticAntI} \right) \cdot {LHC}
```
```math
{Q} =  {gamma0} \cdot {Vx} \cdot {psbS} + {gamma1} \cdot {Vx} \cdot {PsbSP} + {gamma2} \cdot \frac{{{Zx}}}{{{Zx} + {kZSat}}}  \cdot {PsbSP} + {gamma3} \cdot \frac{{{Zx}}}{{{Zx} + {kZSat}}}  \cdot {psbS}
```
```math
Fluo =  \frac{{{psIIcross} \cdot {kF} \cdot {B0}}}{{{kF} + {k2} + {kH} \cdot {Q}}} + \frac{{{psIIcross} \cdot {kF} \cdot {B2}}}{{{kF} + {kH} \cdot {Q}}}
```
```math
{pH_lumen} =  \frac{{-\log \left( {H_lumen} \cdot 0.00025 \right)}}{{\log 10}}
```
```math
{Pi_st} =  {Pi_tot} - \left( {PGA} + 2 \cdot {BPGA} + {GAP} + {DHAP} + 2 \cdot {FBP} + {F6P} + {G6P} + {G1P} + 2 \cdot {SBP} + {S7P} + {E4P} + {X5P} + {R5P} + 2 \cdot {RUBP} + {RU5P} + {ATP_st} \right)
```
```math
{TRX_red} = {Thioredoxin_tot} - {TRX_ox}
```
```math
{E_CBB_active} = {E_total} - {E_CBB_inactive}
```
```math
{ASC} = {ASC_tot} - {MDA} - {DHA}
```
```math
{GSH} =  {Glutathion_tot} - 2 \cdot {GSSG}
```

</details>

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

                     """)

mdFile.new_header(3, "Parameters")

mdFile.new_table(
    columns=len(params_table.columns),
    rows=len(params_table_tolist),
    text=params_table_list,
)

mdFile.new_header(4, "Derived Parameters")

mdFile.new_table(
    columns=len(derived_params_table.columns),
    rows=len(derived_params_table_tolist),
    text=derived_params_table_list,
)

mdFile.new_paragraph(rf"""

<details>
<summary>Equations of derived parameters</summary>

```math
{keq_PQH_2} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_QA} \cdot {F} + -2 \cdot {E0_PQ} \cdot {F} + 2 \cdot {pH_stroma} \ln 10 \cdot {R} \cdot {T} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{keq_v_Fdred} =  \exp \left( \frac{{-\left( -\left( -{E0_FA} \cdot {F} \right) + -{E0_Fd} \cdot {F} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{keq_PCP700} =  \exp \left( \frac{{-\left( -\left( -{E0_PC} \cdot {F} \right) + -{E0_P700} \cdot {F} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{keq_v_FNR} =  \exp \left( \frac{{-\left( -2 \cdot -{E0_Fd} \cdot {F} + -2 \cdot {E0_NADP} \cdot {F} + \ln 10 \cdot {R} \cdot {T} \cdot {pH_stroma} \right)}}{{{R} \cdot {T}}} \right)
```
```math
{keq_v_ATPsynth} =  {Pi_mol} \cdot \exp \left( \frac{{- \left( {DeltaG0_ATP} - \left( \ln(10) \cdot {R} \cdot {T} \right) \cdot {HPR} \cdot \left( {pH_stroma} - {pH_lumen} \right) \right)}}{{{R} \cdot {T}}} \right)
```
```math
{keq_v_b6f} =  \exp \left( \frac{{-\left( -\left( -2 \cdot {F} \cdot {E0_PQ} + 2 \cdot \ln 10 \cdot {R} {T} \cdot {pH_lumen} \right) + 2 \cdot -{F} \cdot {E0_PC} + 2 \ln 10 \cdot {R} \cdot {T} \cdot \left( {pH_stroma} - {pH_lumen} \right) \right)}}{{{R} \cdot {T}}} \right)
```
```math
{vmax_v_RuBisCO_c} = {E_CBB_active} \cdot {kcat_v_RuBisCO_c}
```
```math
{vmax_v_FBPase} = {E_CBB_active} \cdot {kcat_v_FBPase}
```
```math
{vmax_v_SBPase} = {E_CBB_active} \cdot {kcat_v_SBPase}
```
```math
{vmax_v_PRKase} = {E_CBB_active} \cdot {kcat_v_PRKase}
```
```math
{vmax_v_starch} = {E_CBB_active} \cdot {kcat_v_starch}
```
</details>

                     """)

mdFile.new_header(3, "Reaction Rates")

mdFile.new_table(
    columns=len(rates_table.columns),
    rows=len(rates_table_tolist),
    text=rates_table_list,
)

mdFile.new_paragraph(rf"""

<details>
<summary>Rate equations</summary>

```math
{v_PSII} =  0.5 \cdot {B1} \cdot {k2}
```
```math
{v_PQ} =  {PQH_2} \cdot {kPTOX} \cdot \left\{{ \begin{{array}}{{cl}}
{O2_lumen} & : \ ox\ \mathrm{{is \ True\ \lor}}\ time < Ton \lor time > Toff  \\
0 &
\end{{array}} \right.
```
```math
{v_NDH} = {PQ} \cdot  \left\{{ \begin{{array}}{{cl}}
{kf_v_NDH} & : \ ox\ \mathrm{{is \ True\ \lor}}\ \left( time > Ton \land time < Toff \right)  \\
0 &
\end{{array}} \right.
```
```math
{v_b6f} =  \mathrm{{max}} \left( {kcat_v_b6f} \cdot \left( {PQH_2} \cdot {PC_ox}^{{2}} - \frac{{{PQ} \cdot {PC_red}^{{2}}}}{{{keq_v_b6f}}} \right), -{kcat_v_b6f} \right)
```
```math
{v_Cyc} =  {kf_v_Cyc} \cdot {Fd_red}^{{2}} \cdot {PQ}
```
```math
{v_FNR} =  \frac{{{Enz0_v_FNR} \cdot {kcat_v_FNR} \cdot \left( \left( \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \cdot \frac{{{NADP_st}}}{{{convf} \cdot {km_v_FNR_NADP_st}}} - \frac{{\left( \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \cdot \frac{{{NADPH_st}}}{{{convf} \cdot {km_v_FNR_NADP_st}}}}}{{{keq_v_FNR}}} \right)}}{{\left( 1 + \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} + \left( \frac{{{Fd_red}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \right) \left( 1 + \frac{{{NADP_st}}}{{{convf} \cdot {km_v_FNR_NADP_st}}} \right) + \left( 1 + \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} + \left( \frac{{{Fd_ox}}}{{{km_v_FNR_Fd_red}}} \right)^{{2}} \right) \cdot \left( 1 + \frac{{{NADPH_st}}}{{{convf} \cdot {km_v_FNR_NADP_st}}} \right) - 1}}
```
```math
{v_Leak} =  {kf_v_Leak} \cdot \left( {H_lumen} - 4 \times 10^3 \cdot 10^{{{pH_stroma}}} \right)
```
```math
{v_St21} =  {kStt7} \cdot \frac{{1}}{{1 + \left( \frac{{{PQ}}}{{{PQ_tot} \cdot {km_v_St12}}} \right)^{{{n_ST}}}}} \cdot {LHC}
```
```math
{v_St12} = {LHCp} \cdot {kPph1}
```
```math
{v_ATPsynth} =  {kf_v_ATPsynth} \cdot \left( \frac{{{ADP_st}}}{{{convf}}} - \frac{{{ATP_st}}}{{{convf} \cdot {keq_v_ATPsynth}}} \right)
```
```math
{v_Deepox} =  {kf_v_Deepox} \cdot \frac{{{H_lumen} ^{kh_v_Deepox}}}{{\left(4 \times 10^3 \cdot 10^{{{ksat_v_Deepox}}}\right)^{kh_v_Deepox} + {H_lumen} ^{kh_v_Deepox}}} \cdot {Vx}
```
```math
{v_Epox} = {Zx} \cdot {kf_v_Epox}
```
```math
{v_PsbSP} =  {kf_v_PsbSP} \cdot \frac{{{H_lumen} ^{kh_v_PsbSP}}}{{\left(4 \times 10^3 \cdot 10^{{{ksat_v_PsbSP}}}\right)^{kh_v_PsbSP} + {H_lumen} ^{kh_v_PsbSP}}} \cdot {psbS}
```
```math
{v_PsbSD} = {kf_v_PsbSD} \cdot {PsbSP}
```
```math
{v_PGK1ase} =  {kre_v_PGK1ase} \cdot \left( {ATP_st} \cdot {PGA} - \frac{{{BPGA} \cdot {ADP_st}}}{{{keq_v_PGK1ase}}} \right)
```
```math
{v_BPGAdehynase} =  {kre_v_BPGAdehynase} \cdot \left( {BPGA} \cdot {NADPH_st} \cdot {H_stroma} - \frac{{{GAP} \cdot {NADP_st} \cdot {Pi_st}}}{{{keq_v_BPGAdehynase}}} \right)
```
```math
{v_TPIase} =  {kre_v_TPIase} \cdot \left( {GAP} - \frac{{{DHAP}}}{{{keq_v_TPIase}}} \right)
```
```math
{v_Aldolase_FBP} =  {kre_v_Aldolase_FBP} \cdot \left( {GAP} \cdot {DHAP} - \frac{{{FBP}}}{{{keq_v_Aldolase_FBP}}} \right)
```
```math
{v_TKase_E4P} =  {kre_v_TKase_E4P} \cdot \left( {GAP} \cdot {F6P} - \frac{{{X5P} \cdot {E4P}}}{{{keq_v_TKase_E4P}}} \right)
```
```math
{v_Aldolase_SBP} =  {kre_v_Aldolase_SBP} \cdot \left( {DHAP} \cdot {E4P} - \frac{{{SBP}}}{{{keq_v_Aldolase_SBP}}} \right)
```
```math
{v_TKase_R5P} =  {kre_v_TKase_R5P} \cdot \left( {GAP} \cdot {S7P} - \frac{{{X5P} \cdot {R5P}}}{{{keq_v_TKase_R5P}}} \right)
```
```math
{v_Rpiase} =  {kre_v_Rpiase} \cdot \left( {R5P} - \frac{{{RU5P}}}{{{keq_v_Rpiase}}} \right)
```
```math
{v_RPEase} =  {kre_v_RPEase} \cdot \left( {X5P} - \frac{{{RU5P}}}{{{keq_v_RPEase}}} \right)
```
```math
{v_PGIase} =  {kre_v_PGIase} \cdot \left( {F6P} - \frac{{{G6P}}}{{{keq_v_PGIase}}} \right)
```
```math
{v_PGMase} =  {kre_v_PGMase} \cdot \left( {G6P} - \frac{{{G1P}}}{{{keq_v_PGMase}}} \right)
```
```math
{v_pga_ex} =  \frac{{{kcat_N_translocator} \cdot {PGA}}}{{{IF_3P} \cdot {km_v_pga_ex}}}
```
```math
{v_gap_ex} =  \frac{{{kcat_N_translocator} \cdot {GAP}}}{{{IF_3P} \cdot {km_v_gap_ex}}}
```
```math
{v_dhap_ex} =  \frac{{{kcat_N_translocator} \cdot {DHAP}}}{{{IF_3P} \cdot {km_v_dhap_ex}}}
```
```math
{v_RuBisCO_c} =  \frac{{{vmax_v_RuBisCO_c} \cdot {RUBP} \cdot {CO2}}}{{\left( {RUBP} + {km_v_RuBisCO_c_RUBP} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_RuBisCO_c_PGA}}} + \frac{{{FBP}}}{{{ki_v_RuBisCO_c_FBP}}} + \frac{{{SBP}}}{{{ki_v_RuBisCO_c_SBP}}} + \frac{{{Pi_st}}}{{{ki_v_RuBisCO_c_Pi_st}}} + \frac{{{NADPH_st}}}{{{ki_v_RuBisCO_c_NADPH_st}}} \right) \right) \left( {CO2} + {km_v_RuBisCO_c_CO2} \right)}}
```
```math
{v_FBPase} =  \frac{{{vmax_v_FBPase} \cdot {FBP}}}{{{FBP} + {km_v_FBPase_s} \cdot \left( 1 + \frac{{{F6P}}}{{{ki_v_FBPase_F6P}}} + \frac{{{Pi_st}}}{{{ki_v_FBPase_Pi_st}}} \right)}}
```
```math
{v_SBPase} =  \frac{{{vmax_v_SBPase} \cdot {SBP}}}{{{SBP} + {km_v_SBPase_s} \cdot \left( 1 + \frac{{{Pi_st}}}{{{ki_v_SBPase_Pi_st}}} \right)}}
```
```math
{v_PRKase} =  \frac{{{vmax_v_PRKase} \cdot {RU5P} \cdot {ATP_st}}}{{\left( {RU5P} + {km_v_PRKase_RU5P} \cdot \left( 1 + \frac{{{PGA}}}{{{ki_v_PRKase_PGA}}} + \frac{{{RUBP}}}{{{ki_v_PRKase_RUBP}}} + \frac{{{Pi_st}}}{{{ki_v_PRKase_Pi_st}}} \right) \right) \left( {ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_PRKase_4}}} \right) + {km_v_PRKase_ATP_st} \cdot \left( 1 + \frac{{{ADP_st}}}{{{ki_v_PRKase_5}}} \right) \right)}}
```
```math
{v_starch} =  \frac{{{vmax_v_starch} \cdot {G1P} \cdot {ATP_st}}}{{\left( {G1P} + {km_v_starch_G1P} \right) \left( \left( 1 + \frac{{{ADP_st}}}{{{ki_v_starch}}} \right) \left( {ATP_st} + {km_v_starch_ATP_st} \right) + \frac{{{km_v_starch_ATP_st} \cdot {Pi_st}}}{{{ki_v_starch_PGA} \cdot {PGA} + {ki_v_starch_F6P} \cdot {F6P} + {ki_v_starch_FBP} \cdot {FBP}}} \right)}}
```
```math
{v_FdTrReduc} = {TRX_ox} \cdot {Fd_red} \cdot {kf_v_FdTrReduc}
```
```math
{v_Eact} = {E_CBB_inactive} \cdot {TRX_red} \cdot {kf_v_Eact}
```
```math
{v_Einact} = {E_CBB_active} \cdot {kf_v_Einact}
```
```math
{v_PSI} =  \left( 1 - {psIIcross} \right) \cdot {PPFD} \cdot {Y0}
```
```math
{v_Fdred} =  {kFdred} \cdot {Fd_ox} \cdot {Y1} - \frac{{{kFdred}}}{{{keq_v_Fdred}}} \cdot {Fd_red} \cdot {Y2}
```
```math
{v_APXase} =  \frac{{{ASC} \cdot {H2O2} \cdot {XT}}}{{{ASC} \cdot {H2O2} \cdot \left( \frac{{1}}{{{kf3}}} + \frac{{1}}{{{kf5}}} \right) + \frac{{{ASC}}}{{{kf1}}} + \frac{{{H2O2}}}{{{kf4}}} + \frac{{{H2O2} \cdot {kr4}}}{{{kf4} \cdot {kf5}}} + \frac{{{H2O2}}}{{{kf2}}} + \frac{{{H2O2} \cdot {kr2}}}{{{kf2} \cdot {kf3}}} + \frac{{{kr1}}}{{{kf1} \cdot {kf2}}} + \frac{{{kr1} \cdot {kr2}}}{{{kf1} \cdot {kf2} \cdot {kf3}}}}}
```
```math
{v_MDAreduct} =  \frac{{{kcat_v_MDAreduct} \cdot {Enz0_v_MDAreduct} \cdot {NADPH_st} \cdot {MDA}}}{{{km_v_MDAreduct_NADPH_st} \cdot {MDA} + {km_v_MDAreduct_MDA} \cdot {NADPH_st} + {NADPH_st} \cdot {MDA} + {km_v_MDAreduct_NADPH_st} \cdot {km_v_MDAreduct_MDA}}}
```
```math
{v_Mehler} = {Y1} \cdot {O2_lumen} \cdot {kMehler}
```
```math
{v_GR} =  \frac{{{kcat_v_GR} \cdot {Enz0_v_GR} \cdot {NADPH_st} \cdot {GSSG}}}{{{km_v_GR_NADPH_st} \cdot {GSSG} + {km_v_GR_GSSG} \cdot {NADPH_st} + {NADPH_st} \cdot {GSSG} + {km_v_GR_NADPH_st} \cdot {km_v_GR_GSSG}}}
```
```math
{v_DHAR} =  \frac{{{kcat_v_DHAR} \cdot {Enz0_v_DHAR} \cdot {DHA} \cdot {GSH}}}{{{km_v_DHAR_DHA} + {km_v_DHAR_DHA} \cdot {GSH} + {km_v_DHAR_GSH} \cdot {DHA} + {DHA} \cdot {GSH}}}
```
```math
{v_3ASC} =  {kf_v_3ASC} \cdot {MDA}^{{2}}
```
```math
{v_ATPcons} = {ATP_st} \cdot {kf_v_ATPcons}
```
```math
{v_NADPHcons} = {NADPH_st} \cdot {kf_v_NADPHcons}
```

</details>

                     """)

mdFile.new_header(3, "Figures")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 2</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig2.svg'>



</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 3</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig3.svg'>



</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 4</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig4.svg'>



</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 5</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig5.svg'>



</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 6</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig6.svg'>



</details>
""")

mdFile.new_paragraph(r"""
                     
<details>
<summary>Figure 7</summary>
                     
<img style='display: block; margin: 0 auto' src='paper_figures/Saadat2021_fig7.svg'>



</details>
""")

mdFile.create_md_file()
