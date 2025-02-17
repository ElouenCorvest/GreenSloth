



# Saadat2021


[Saadat2021](https://doi.org/10.3389/fpls.2021.750580)


## Installation

## Summary

### Compounds

#### Part of ODE system

|Name|Common Abbr.|Paper Abbr.|MetaCyc ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Plastoquinone|$\mathrm{PQ}$|$\mathrm{PQ}_\mathrm{ox}$|PLASTOQUINONE|PQ|
|Oxidized Plastocyanine|$\mathrm{PC}_\mathrm{ox}$|$\mathrm{PC}_\mathrm{ox}$|C03162|PC_ox|
|Oxidized Ferrodoxin|$\mathrm{Fd}_\mathrm{ox}$|$\mathrm{Fd}_\mathrm{ox}$|C00139|Fd_ox|
|Stromal ATP concentration|$\mathrm{ATP_{st}}$|$\mathrm{ATP}$|ATP|ATP_st|
|Stromal NADPH concentration|$\mathrm{NADPH}_\mathrm{st}$|$\mathrm{NADPH}$|NADPH|NADPH_st|
|Lumenal Proton concentration|$\mathrm{H_{lu}}$|$\mathrm{H}^+$|PROTON|H_lu|
|Phosphorylated fraction of light harvesting complexes|$\mathrm{LHC}$|$\mathrm{LHC}$||LHC|
|Concentration of psbS protein|$\mathrm{psbS}$|$\mathrm{Psbs}$|AT1G44575|psbS|
|Violaxanthin|$\mathrm{Vx}$|$\mathrm{Vx}$|CPD1F-133|Vx|
|3-phosphoglyceric acid|$\mathrm{PGA}$|$\mathrm{PGA}$|G3P|PGA|
|2,3-biphosphoglyceric acid|$\mathrm{BPGA}$|$\mathrm{BPGA}$|23-DIPHOSPHOGLYCERATE|BPGA|
|Glyceraldehyde 3-phosphate|$\mathrm{GAP}$|$\mathrm{GAP}$|GAP|GAP|
|Dihydroxyacetone phosphate|$\mathrm{DHAP}$|$\mathrm{DHAP}$|DIHYDROXY-ACETONE-PHOSPHATE|DHAP|
|Fructose 1,6-bisphosphate|$\mathrm{FBP}$|$\mathrm{FBP}$|FRUCTOSE-16-DIPHOSPHATE|FBP|
|Fructose 6-phosphate|$\mathrm{F6P}$|$\mathrm{F6P}$|FRUCTOSE-6P|F6P|
|Glucose 6-phosphate|$\mathrm{G6P}$|$\mathrm{G6P}$|ALPHA-GLC-6-P|G6P|
|Glucose 1-phosphate|$\mathrm{G1P}$|$\mathrm{G1P}$|GLC-1-P|G1P|
|Sedoheptulose 1,7-bisphosphate|$\mathrm{SBP}$|$\mathrm{SBP}$|D-SEDOHEPTULOSE-1-7-P2|SBP|
|Sedoheptulose 7-phosphate|$\mathrm{S7P}$|$\mathrm{S7P}$|D-SEDOHEPTULOSE-7-P|S7P|
|Erythrose 4-phosphate|$\mathrm{E4P}$|$\mathrm{E4P}$|ERYTHROSE-4P|E4P|
|Xylulose 5-phosphate|$\mathrm{X5P}$|$\mathrm{X5P}$|XYLULOSE-5-PHOSPHATE|X5P|
|Ribose 5-phosphate|$\mathrm{R5P}$|$\mathrm{R5P}$|CPD-15318|R5P|
|Ribulose 1,5-bisphosphate|$\mathrm{RUBP}$|$\mathrm{RUBP}$|D-RIBULOSE-15-P2|RUBP|
|Ribulose 5-phosphate|$\mathrm{RU5P}$|$\mathrm{RU5P}$|RIBULOSE-5P|RU5P|
|Monodehydroascorbate radicals|$\mathrm{MDA}$|$\mathrm{MDA}$|CPD-318|MDA|
|Hydrogen Peroxide|$\mathrm{H_2O_2}$|$\mathrm{H_2O_2}$|HYDROGEN-PEROXIDE|H2O2|
|Dehydroacorbate|$\mathrm{DHA}$|$\mathrm{DHA}$|L-DEHYDRO-ASCORBATE|DHA|
|Glutathione disulfide|$\mathrm{GSSG}$|$\mathrm{GSSG}$|OXIDIZED-GLUTATHIONE|GSSG|
|Oxidised thioredoxin|$\mathrm{Trx_{ox}}$|$\mathrm{Trx_{ox}}$|2142833|Trx_ox|
|Inactive CBB proteins|$\mathrm{E}_\mathrm{CBB,\ inact}$|$\mathrm{E}_\mathrm{inactive}$||E_CBB_inactive|



<details>
<summary>ODE System</summary>

```math
   \begin{align}
      \frac{\mathrm{d}\mathrm{PQ}}{\mathrm{d}t} &= -v_{\mathrm{PSII}} + v_{\mathrm{PQ}_{\mathrm{ox}}} - v_{\mathrm{NDH}} + v_{\mathrm{b6f}} - v_{\mathrm{Cyc}} \\
      \frac{\mathrm{d}\mathrm{H_{lu}}}{\mathrm{d}t} &= 0.02 \cdot v_{\mathrm{PSII}} + 0.04 \cdot v_{\mathrm{b6f}} - 0.0v_{\mathrm{Leak}} - 0.04666666666666667 \cdot v_{\mathrm{ATPsynthase}} \\
      \frac{\mathrm{d}\mathrm{Fd}_\mathrm{ox}}{\mathrm{d}t} &= 2 \cdot v_{\mathrm{Cyc}} + 2 \cdot v_{\mathrm{FNR}} - v_{\mathrm{Fd}_{\mathrm{red}}} + v_{\mathrm{FdTrReductase}} \\
      \frac{\mathrm{d}\mathrm{PC}_\mathrm{ox}}{\mathrm{d}t} &= -2 \cdot v_{\mathrm{b6f}} + v_{\mathrm{PSI}} \\
      \frac{\mathrm{d}\mathrm{NADPH}_\mathrm{st}}{\mathrm{d}t} &= 0.032 \cdot v_{\mathrm{FNR}} - v_{\mathrm{BPGAdehynase}} - v_{\mathrm{MDAreduct}} - v_{\mathrm{GR}} - v_{\mathrm{NADPH}_\mathrm{consumption}} \\
      \frac{\mathrm{d}\mathrm{LHC}}{\mathrm{d}t} &= -v_{\mathrm{St21}} + v_{\mathrm{St12}} \\
      \frac{\mathrm{d}\mathrm{ATP_{st}}}{\mathrm{d}t} &= 0.032 \cdot v_{\mathrm{ATPsynthase}} - v_{\mathrm{PGK1ase}} - v_{\mathrm{PRKase}} - v_{\mathrm{Starch}} - v_{\mathrm{ATP}_{\mathrm{consumption}}} \\
      \frac{\mathrm{d}\mathrm{Vx}}{\mathrm{d}t} &= -v_{\mathrm{Deepox}} + v_{\mathrm{Epox}} \\
      \frac{\mathrm{d}\mathrm{psbS}}{\mathrm{d}t} &= -v_{\mathrm{Psbs^P}} + v_{\mathrm{Psbs^D}} \\
      \frac{\mathrm{d}\mathrm{RUBP}}{\mathrm{d}t} &= -v_{\mathrm{RuBisCO}} + v_{\mathrm{PRKase}} \\
      \frac{\mathrm{d}\mathrm{PGA}}{\mathrm{d}t} &= 2 \cdot v_{\mathrm{RuBisCO}} - v_{\mathrm{PGK1ase}} - v_{\mathrm{PGA,\ ex}} \\
      \frac{\mathrm{d}\mathrm{BPGA}}{\mathrm{d}t} &= v_{\mathrm{PGK1ase}} - v_{\mathrm{BPGAdehynase}} \\
      \frac{\mathrm{d}\mathrm{GAP}}{\mathrm{d}t} &= v_{\mathrm{BPGAdehynase}} - v_{\mathrm{TPIase}} - v_{\mathrm{Aldolase_{FBP}}} - v_{\mathrm{TKase_E4P}} - v_{\mathrm{TKase_R5P}} - v_{\mathrm{GAP,\ ex}} \\
      \frac{\mathrm{d}\mathrm{DHAP}}{\mathrm{d}t} &= v_{\mathrm{TPIase}} - v_{\mathrm{Aldolase_{FBP}}} - v_{\mathrm{Aldolase_{SBP}}} - v_{\mathrm{DHAP,\ ex}} \\
      \frac{\mathrm{d}\mathrm{FBP}}{\mathrm{d}t} &= v_{\mathrm{Aldolase_{FBP}}} - v_{\mathrm{FBPase}} \\
      \frac{\mathrm{d}\mathrm{F6P}}{\mathrm{d}t} &= v_{\mathrm{FBPase}} - v_{\mathrm{TKase_E4P}} - v_{\mathrm{PGIase}} \\
      \frac{\mathrm{d}\mathrm{X5P}}{\mathrm{d}t} &= v_{\mathrm{TKase_E4P}} + v_{\mathrm{TKase_R5P}} - v_{\mathrm{RPEase}} \\
      \frac{\mathrm{d}\mathrm{E4P}}{\mathrm{d}t} &= v_{\mathrm{TKase_E4P}} - v_{\mathrm{Aldolase_{SBP}}} \\
      \frac{\mathrm{d}\mathrm{SBP}}{\mathrm{d}t} &= v_{\mathrm{Aldolase_{SBP}}} - v_{\mathrm{SBPase}} \\
      \frac{\mathrm{d}\mathrm{S7P}}{\mathrm{d}t} &= v_{\mathrm{SBPase}} - v_{\mathrm{TKase_R5P}} \\
      \frac{\mathrm{d}\mathrm{R5P}}{\mathrm{d}t} &= v_{\mathrm{TKase_R5P}} - v_{\mathrm{Rpiase}} \\
      \frac{\mathrm{d}\mathrm{RU5P}}{\mathrm{d}t} &= v_{\mathrm{Rpiase}} + v_{\mathrm{RPEase}} - v_{\mathrm{PRKase}} \\
      \frac{\mathrm{d}\mathrm{G6P}}{\mathrm{d}t} &= v_{\mathrm{PGIase}} - v_{\mathrm{PGMase}} \\
      \frac{\mathrm{d}\mathrm{G1P}}{\mathrm{d}t} &= v_{\mathrm{PGMase}} - v_{\mathrm{Starch}} \\
      \frac{\mathrm{d}\mathrm{H_2O_2}}{\mathrm{d}t} &= -v_{\mathrm{APXase}} + 0.032 \cdot v_{\mathrm{Mehler}} \\
      \frac{\mathrm{d}\mathrm{MDA}}{\mathrm{d}t} &= 2 \cdot v_{\mathrm{APXase}} - 2 \cdot v_{\mathrm{MDAreduct}} - 2 \cdot v_{\mathrm{3ASC}} \\
      \frac{\mathrm{d}\mathrm{GSSG}}{\mathrm{d}t} &= -v_{\mathrm{GR}} + v_{\mathrm{DHAR}} \\
      \frac{\mathrm{d}\mathrm{DHA}}{\mathrm{d}t} &= -v_{\mathrm{DHAR}} + v_{\mathrm{3ASC}} \\
      \frac{\mathrm{d}\mathrm{Trx_{ox}}}{\mathrm{d}t} &= -v_{\mathrm{FdTrReductase}} + 5 \cdot v_{\mathrm{Eact}} \\
      \frac{\mathrm{d}\mathrm{E}_\mathrm{CBB,\ inact}}{\mathrm{d}t} &= -5 \cdot v_{\mathrm{Eact}} + 5 \cdot v_{\mathrm{Einact}} \\
   \end{align}
```

</details>

#### Conserved quantities

### Parameters

|Short Description|Common Abbr.|Paper Abbr.|Value|Unit|MetaCyc ID|Python Var|Reference|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
||||$0.032$|||convf||
|PSII reaction centres|$\mathrm{PSII}^{\mathrm{tot}}$|$\mathrm{PSII}^{\mathrm{tot}}$|$2.5$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||PSII_tot|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
|PSI reaction centres|$\mathrm{PSI}^{\mathrm{tot}}$|$\mathrm{PSI}^{\mathrm{tot}}$|$2.5$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||PSI_tot|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
|Total plastoquinone pool|$\mathrm{PQ}^{\mathrm{tot}}$|$\mathrm{PQ}^{\mathrm{tot}}$|$17.5$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||PQ_tot|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
|Total plastocyanine pool|$\mathrm{PC}^{\mathrm{tot}}$|$\mathrm{PC}^{\mathrm{tot}}$|$4.0$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||PC_tot|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
|Total ferrodoxin pool|$\mathrm{Fd}^{\mathrm{tot}}$|$\mathrm{Fd}^{\mathrm{tot}}$|$5.0$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||Fd_tot||
||||$2.5$|||Ctot||
|Total NADP pool|$\mathrm{NADP}^{\mathrm{tot}}$|$\mathrm{NADP}^{\mathrm{tot}}$|$0.8$|$\mathrm{mM}$||NADP_tot|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Total adenosine phosphate pool|$\mathrm{AP}^{\mathrm{tot}}$|$\mathrm{AP}^{\mathrm{tot}}$|$2.55$|$\mathrm{mM}$||AP_tot|[[3]](Increased from Bionumbers)|
|Relative pool of PsbS|$\mathrm{PsbS}^{\mathrm{tot}}$|$\mathrm{PsbS}^{\mathrm{tot}}$|$1.0$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||PsbS_tot|[[4]](https://doi.org/10.1016/j.bbabio.2016.09.003)|
|Relative pool of xanthophylls|$\mathrm{X}^{\mathrm{tot}}$|$\mathrm{X}^{\mathrm{tot}}$|$1.0$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||X_tot|[[4]](https://doi.org/10.1016/j.bbabio.2016.09.003)|
|Rate of non-radiative decay|$k_H$|$k_H$|$5 \times 10^9$|$s^{-1}$||k_H|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$500000000.0$|||kH0||
|Rate of fluorescence|$k_F$|$k_F$|$6.25 \times 10^8$|$s^{-1}$||k_F||
||||$5000000000.0$|||k1||
||||$10000000000.0$|||k1rev||
||||$5000000000.0$|||k2||
||||$100$|||kdeg||
||||$0.000555$|||krep||
||||$0.0035$|||kStt7||
||||$0.0013$|||kPph1||
|Switch point (half-activity of Stt7) for 20% PQ oxidised|$K_{\mathrm{M}_\mathrm{ST}}$|$K_{\mathrm{M}_\mathrm{ST}}$|$0.2$|||KM_ST|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$2.0$|||n_ST||
||||$0.37$|||staticAntI||
||||$0.1$|||staticAntII||
||||$1.0$|||prob_attach||
||||$0.05$|||kActATPase||
||||$0.002$|||kDeactATPase||
||$k_\mathrm{ATPsynth}$|$k_\mathrm{ATPsynthase}$|$20.0$|$s^{-1}$||kATPsynth|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$10.0$|||kATPcons||
||||$0.5$|||ATPcyt||
|Internal pool of phosphates, required to calculate ATP equilibrium|$\mathrm{Pi}_{\mathrm{mol}$|$\mathrm{Pi}_{\mathrm{mol}$|$0.01$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||Pi_mol||
||||$30.6$|||DeltaG0_ATP||
|Ratio of protons to ATP in ATP synthase|||$\frac{14}{3}$|||HPR|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$15.0$|||kNADPHcons||
||||$0.5$|||NADPHcyt||
|Stromal pH of a dark adapted state|$\mathrm{pH}_\mathrm{stroma}$|$\mathrm{pH}_\mathrm{stroma}$|$7.9$|||pH_stroma||
||$k_\mathrm{Leak}$|$k_\mathrm{leak}$|$10.0$|$s^{-1}$||k_Leak||
||$b_\mathrm{H}$|$b_\mathrm{H}$|$100.0$|||b_H|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_{\mathrm{PQ}_\mathrm{red}}$|$k_{\mathrm{PQ}_\mathrm{red}}$|$250.0$|$\mathrm{mmol}^{-1} \left(\mathrm{mol\ Chl}\right)\  s^{-1}$||k_PQred|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_\mathrm{Cytb6f}$|$k_\mathrm{Cytb6f}$|$2.5$|$\mathrm{mmol^{-2}(mol\ Chl)^2\,s^{-1}}}$||k_Cytb6f|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_\mathrm{PTOX}$|$k_\mathrm{PTOX}$|$0.01$|$\mathrm{mmol^{-1}(mol\ Chl)\,s^{-1}}$||k_PTOX|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_\mathrm{PCox}$|$k_\mathrm{PCox}$|$2500.0$|$\mathrm{mmol^{-1}(mol\ Chl)\,s^{-1}}$||k_PCox|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_{\mathrm{Fd}_\mathrm{red}}$|$k_{\mathrm{Fd}_\mathrm{red}}$|$2.5 \times 10^5$|$\mathrm{mmol^{-1}(mol\ Chl)\,s^{-1}}$||k_Fdred|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$500.0$|||kcatFNR||
||||$1.0$|||kcyc||
|External oxygen pool, corresponds to 250μM.|$\mathrm{O}_{2_\mathrm{ext}}$|$\mathrm{O}_2^\mathrm{ex}$|$8.0$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||O2_ext|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$k_\mathrm{NDH}$|$k_\mathrm{NDH}$|$0.002$|$s^{-1}$||k_NDH|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$0.05$|||kNh||
||||$0.004$|||kNr||
||||$5.0$|||nH||
||||$3.0$|||EFNR||
||$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{F}}}$|$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{F}}}$|$1.56$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||KM_FNR_F|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{N}}}$|$K_{\mathrm{M}_{\mathrm{FNR}_\mathrm{N}}}$|$0.22$|$\mathrm{mmol} \left(\mathrm{mol\ Chl}\right)^{-1}$||KM_FNR_N|[[1]](https://doi.org/10.1098/rstb.2013.0223)|
||||$0.1$|||gamma0||
||||$0.25$|||gamma1||
||||$0.6$|||gamma2||
||||$0.15$|||gamma3||
||||$0.0096$|||kDeprotonation||
||||$0.0096$|||kProtonationL||
||||$5.8$|||kphSatLHC||
||||$0.0024$|||kDeepoxV||
||||$0.00024$|||kEpoxZ||
||||$5.8$|||kphSat||
||||$5.0$|||kHillX||
||||$3.0$|||kHillL||
||||$0.12$|||kZSat||
||||$-0.14$|||E0_QA||
||||$0.354$|||E0_PQ||
||||$0.35$|||E0_cytf||
||||$0.38$|||E0_PC||
||||$0.48$|||E0_P700||
||||$-0.55$|||E0_FA||
||||$-0.43$|||E0_Fd||
||||$-0.113$|||E0_NADP||
||||$96.485$|||F||
||||$0.0083$|||R||
||||$298.0$|||T||
||||$100.0$|||pfd||
||||$0.0$|||Ton||
||||$1800$|||Toff||
||||$120$|||dT||
||||$True$|||ox||
||||$0.5$|||CN||
||$\mathrm{CO}_2$|$\mathrm{CO}_2$|$0.2$|$\mathrm{mM}$||CO2|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
||||$17.05$|||Cp||
||||$0.5$|||Ca||
||||$7.6$|||pHmedium||
|External phosphate|$\mathrm{P}_\mathrm{ext}$|$\mathrm{P}_\mathrm{ext}$|$0.5$|$\mathrm{mM}$||Pext|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Base $V_\mathrm{max}$ of RuBisCO|$V_{\mathrm{max,\ base}_{\mathrm{RuBisCO}}}$|$V_{1_{\mathrm{base}}}$|$0.34 \cdot 8$|$\mathrm{mM}\ s^{-1}$||V_maxbase_rubisco||
|Base $V_\mathrm{max}$ of FBPase|$V_{\mathrm{max,\ base}_{\mathrm{FBPase}}}$|$V_{6_{\mathrm{base}}}$|$1.6$|$\mathrm{mM}\ s^{-1}$||V_maxbase_fbpase||
|Base $V_\mathrm{max}$ of SBPase|$V_{\mathrm{max,\ base}_{\mathrm{SBPase}}}$|$V_{9_{\mathrm{base}}}$|$0.32$|$\mathrm{mM}\ s^{-1}$||V_maxbase_sbpase||
|Base $V_\mathrm{max}$ of PRKase|$V_{\mathrm{max,\ base}_{\mathrm{PRKase}}}$|$V_{13_{\mathrm{base}}}$|$7.9992$|$\mathrm{mM}\ s^{-1}$||V_maxbase_prkase||
|Base $V_\mathrm{max}$ of Starch Synthase|$V_{\mathrm{max,\ base}_{\mathrm{Starch}}}$|$V_{\mathrm{st}_{\mathrm{base}}}$|$0.32$|$\mathrm{mM}\ s^{-1}$||V_maxbase_starch||
|$V_\mathrm{max}$ of Export|$V_{\mathrm{max}_{\mathrm{ex}}}$|$V_{\mathrm{ex}}$|$2.0$|$\mathrm{mM}\ s^{-1}$||Vmax_ex||
|Equilibrium constant of PGK1ase|$K_\mathrm{PGK1ase}$|$q_2$|$3.1 \times 10^{-4}$|||K_PGK1ase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of BPGA dehydrogenase|$K_\mathrm{BPGAdehynase}$|$q_3$|$1.6 \times 10^{7}$|||K_BPGAdehynase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of TPIase|$K_\mathrm{TPIase}$|$q_4$|$22.0$|||K_TPIase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of Aldolase of GAP and DHAP to FBP|$K_\mathrm{Aldolase_{FBP}}$|$q_5$|$7.1$|$\mathrm{mM}^{-1}$||K_Aldolase_FBP|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of TKase of GAP and F6P to X5P and E4P|$K_\mathrm{TKase_{E4P}}$|$q_7$|$0.084$|||K_TKase_E4P|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of Aldolase of E4P and DHAP to SBP|$K_\mathrm{Aldolase_{SBP}}$|$q_8$|$13.0$|$\mathrm{mM}^{-1}$||K_Aldolase_SBP|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of TKase of GAP and S7P to X5P and R5P|$K_\mathrm{TKase_{R5P}}$|$q_10$|$0.85$|||K_TKase_R5P|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of Rpiase|$K_\mathrm{Rpiase}$|$q_11$|$0.4$|||K_Rpiase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of RPEase|$K_\mathrm{RPEase}$|$q_12$|$0.67$|||K_RPEase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of PGIase|$K_\mathrm{PGIase}$|$q_14$|$2.3$|||K_PGIase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Equilibrium constant of PGMase|$K_\mathrm{PGMase}$|$q_15$|$0.058$|||K_PGMase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Michaelis Menten constant of RuBisCO for RUBP|$K_{\mathrm{m}_{\mathrm{RuBisCO}_\mathrm{RUBP}}}$|$K_{\mathrm{m}1}$|$0.02$|$\mathrm{mM}$||Km_RuBisCO_RUBP|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Michaelis Menten constant of RuBisCO for CO2|$K_{\mathrm{m}_{\mathrm{RuBisCO}_\mathrm{CO_2}}}$|$K_{\mathrm{mCO2}}$|$0.0107$|$\mathrm{mM}$||Km_RuBisCO_CO2|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Michaelis Menten constant of FBPase|$K_{\mathrm{m}_{\mathrm{FBPase}}}$|$K_{\mathrm{m}6}$|$0.03$|$\mathrm{mM}$||Km_FBPase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
|Michaelis Menten constant of SBPase|$K_{\mathrm{m}_{\mathrm{SBPase}}}$|$K_{\mathrm{m}9}$|$0.013$|$\mathrm{mM}$||Km_SBPase|[[2]](https://doi.org/10.1111/j.1432-1033.1988.tb14242.x)|
||||$0.05$|||Km131||
||||$0.05$|||Km132||
||||$0.014$|||Km161||
||||$0.3$|||Km162||
||||$0.08$|||Kmst1||
||||$0.08$|||Kmst2||
||||$0.19$|||Kmnadph||
||||$0.25$|||Kpga||
||||$0.075$|||Kgap||
||||$0.077$|||Kdhap||
||||$0.63$|||Kpi||
||||$0.74$|||Kpxt||
||||$0.04$|||Ki11||
||||$0.04$|||Ki12||
||||$0.075$|||Ki13||
||||$0.9$|||Ki14||
||||$0.07$|||Ki15||
||||$0.7$|||Ki61||
||||$12.0$|||Ki62||
||||$12.0$|||Ki9||
||||$2.0$|||Ki131||
||||$0.7$|||Ki132||
||||$4.0$|||Ki133||
||||$2.5$|||Ki134||
||||$0.4$|||Ki135||
||||$10.0$|||Kist||
||||$0.1$|||Kast1||
||||$0.02$|||Kast2||
||||$0.02$|||Kast3||
||||$800000000.0$|||k||
|Estimated|$kf_1$|$kf1$|$10000.0$|||k_f1||
||$kr_1$|$kr1$|$220.0$|||k_r1|[[5]](BRENDA database)|
|Estimated|$kf_2$|$kf2$|$10000.0$|||k_f2||
||$kr_2$|$kr2$|$4000.0$|||k_r2|[[5]](BRENDA database)|
||$kf_3$|$kf3$|$2510.0$|||k_f3|[[5]](BRENDA database)|
|Estimated|$kf_4$|$kf4$|$10000.0$|||k_f4||
||$kr_4$|$kr4$|$4000.0$|||k_r4|[[5]](BRENDA database)|
||$kf_5$|$kf5$|$2510.0$|||k_f5|[[5]](BRENDA database)|
|Concentration of ascorbate peroxidase|$XT$|$XT$|$0.07$|||XT|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Estimated rate constant for summarized hydrogen peroxide production|$k_{\mathrm{Mehler}}$|$k_{\mathrm{Mehler}}$|$1.0$|$\mathrm{mM}^{-1}\ \mathrm{s}^{-1}$||k_Mehler||
|Turnover rate of gluthation reductase|$k_{\mathrm{cat}_{\mathrm{GR}}}$|$k_{\mathrm{cat}_{\mathrm{GR}}}$|$595$|$\mathrm{s}^{-1}$||kcat_GR|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Turnover rate of dehydroascorbate reductase|$k_{\mathrm{cat}_{\mathrm{DHAR}}}$|$k_{\mathrm{cat}_{\mathrm{DHAR}}}$|$142$|$\mathrm{s}^{-1}$||kcat_DHAR|[[6]](https://doi.org/10.1104/pp.108.133223)|
||||$12000.0$|||k1APX||
||||$50000.0$|||k2APX||
||||$2100.0$|||k3APX||
||||$699.9999999999999$|||k4APX||
||||$0.01$|||k5APX||
|Rate constant for the spontaneous disproportion of MDA|$k_3$|$k3$|$500.0$|$\mathrm{mM}^{-1}\ \mathrm{s}^{-1}$||k3|[[6]](https://doi.org/10.1104/pp.108.133223)|
||||$100.0$|||k4||
||||$200.0$|||k5||
||||$200.0$|||k6||
||||$699.9999999999999$|||k7||
||||$0.002$|||k8||
|Michaelis Menten constant of NADPH|$K_{\mathrm{m}_{\mathrm{NADPH}}}$|$K_{\mathrm{m}_{\mathrm{NADPH}}}$|$3 \times 10^{-3}$|$\mathrm{mM}$||Km_NADPH|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Michaelis Menten constant of oxidized gluthation|$K_{\mathrm{m}_{\mathrm{GSSG}}}$|$K_{\mathrm{m}_{\mathrm{GSSG}}}$|$0.2$|$\mathrm{mM}$||Km_GSSG|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Michaelis Menten constant of dehydroascorbate|$K_{\mathrm{m}_{\mathrm{DHA}}}$|$K_{\mathrm{m}_{\mathrm{DHA}}}$|$70 \times 10^{-3}$|$\mathrm{mM}$||Km_DHA|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Michaelis Menten constant of reduced gluthation|$K_{\mathrm{m}_{\mathrm{GSH}}}$|$K_{\mathrm{m}_{\mathrm{GSH}}}$|$2.5$|$\mathrm{mM}$||Km_GSH|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Dissociation constant of dehydroascorbate reductase|$K_{\mathrm{DHAR}}$|$K$|$0.5$|$\mathrm{mM}^2$||K_DHAR|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Concentration of gluthatione reductase|$\mathrm{GR}_0$|$\mathrm{GR}_0$|$1.4 \times 10^{-3}$|$\mathrm{mM}$||GR_0|[[6]](https://doi.org/10.1104/pp.108.133223)|
|Concentration of dehydroascorbate reductase|$\mathrm{DHAR}_0$|$\mathrm{DHAR}_0$|$1.7 \times 10^{-3}$|$\mathrm{mM}$||DHAR_0|[[6]](https://doi.org/10.1104/pp.108.133223)|
||||$0.07$|||APX0||
|Total concentration of reduced and oxidized glutathione|$\mathrm{Gluthation}^{\mathrm{tot}}$|$\mathrm{Gluthation}_{\mathrm{total}}$|$10$|$\mathrm{mM}$||Glutathion_total||
|Total concentration of reduced and oxidized ascorbate|$\mathrm{Ascorbate}^{\mathrm{tot}}$|$\mathrm{Ascorbate}_{\mathrm{total}}$|$10$|$\mathrm{mM}$||Ascorbate_total||
|Turnover rate of monodehydroascorbate reductase|$k_{\mathrm{cat}_{\mathrm{MDAR}}}$|$k_{\mathrm{cat}_{\mathrm{MDAR}}}$|$300.0$|$\mathrm{s}^{-1}$||kcat_MDAR|[[7]](https://doi.org/10.1186/s12918-015-0239-y)|
|Michaelis-menten constant of monodehydroascorbate for the conversion to NADPH|$K_{\mathrm{m}_{\mathrm{MDAR-NADPH}}}$|$K_{\mathrm{m}_{\mathrm{MDAR-NADPH}}}$|$23 \times 10^{-3}$|$\mathrm{mM}$||Km_MDAR_NADPH|[[7]](https://doi.org/10.1186/s12918-015-0239-y)|
|Michaelis-menten constant of monodehydroascorbate for the conversion to MDA|$K_{\mathrm{m}_{\mathrm{MDAR-MDA}}}$|$K_{\mathrm{m}_{\mathrm{MDAR-MDA}}}$|$1.4 \times 10^{-3}$|$\mathrm{mM}$||Km_MDAR_MDA|[[7]](https://doi.org/10.1186/s12918-015-0239-y)|
|Concentration of monodehydroascorbate reductase|$\mathrm{MDAR}_0$|$\mathrm{MDAR}_0$|$2 \times 10^{-3}$|$\mathrm{mM}$||MDAR_0|[[7]](https://doi.org/10.1186/s12918-015-0239-y)|
|General consumption rate of ATP|$k_{\mathrm{ex}_{\mathrm{ATP}}}$|$k_{\mathrm{ex}_{\mathrm{atp}}}$|$0.2$|$\mathrm{s}^{-1}$||k_ex_atp|[[8]](Estimated)|
|General consumption rate of NADPH|$k_{\mathrm{ex}_{\mathrm{NADPH}}}$|$k_{\mathrm{ex}_{\mathrm{nadph}}}$|$0.2$|$\mathrm{s}^{-1}$||k_ex_nadph|[[8]](Estimated)|
|Relative total concentration of thioredoxin|$\mathrm{Thioredoxin}^{\mathrm{tot}}$|$\mathrm{thioredoxin}_\mathrm{tot}$|$1$|||thioredoxin_tot||
|Estimated maximal concentration of CBB enzymes|$\mathrm{Enz}_{\mathrm{cbb}_\mathrm{tot}}$|$e_{\mathrm{cbb}_\mathrm{tot}}$|$6$|$\mathrm{mM}$||e_cbb_tot||
|Rate constant of ferrodoxin thioredoxin reductase|$k_{\mathrm{fd}_{\mathrm{tr}_\mathrm{reductase}}}$|$k_{\mathrm{fd}_{\mathrm{tr}_\mathrm{reductase}}}$|$1$|$\mathrm{s}^{-1}$||k_fd_tr_reductase|[[8]](Estimated)|
|Rate constant of CBB activation|$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{activation}}}$|$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{activation}}}$|$1$|||k_e_cbb_activation|[[8]](Estimated)|
|Rate constant of CBB relaxation|$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{relaxation}}}$|$k_{\mathrm{e}_{\mathrm{cbb}_\mathrm{relaxation}}}$|$0.1$|$\mathrm{s}^{-1}$||k_e_cbb_relaxation|[[8]](Estimated)|

#### Derived Parameters

### Reaction Rates

|Short Description|Common Abbr.|Paper Abbr.|MetaCyc ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Reduction of PQ due to PSII|$v_{\mathrm{PSII}}$|$v_{\mathrm{PSII}}$||v_PSII|
|Rate of the b6f complex|$v_{\mathrm{b6f}}$|$v_{\mathrm{b6f}}$||v_b6f|
|Reaction mediated by FNR|$v_{\mathrm{FNR}}$|$v_{\mathrm{FNR}}$||v_FNR|
|Ferredoxin-plastoquinone reductase|$v_{\mathrm{FQR}}$|$v_{\mathrm{FQR}}$||v_FQR|
|Production of ATP by ATPsynthase|$v_{\mathrm{ATPsynthase}}$|$v_{\mathrm{ATPsynthase}}$||v_ATPsynth|
|Transmembrane Proton Leak|$v_{\mathrm{Leak}}$|$v_{\mathrm{Leak}}$||v_Leak|
|Oxidation of the PQ pool through cytochrome and PTOX|$v_{\mathrm{PQ}_{\mathrm{ox}}}$|$v_{\mathrm{PTOX}}$||v_PQ|
|Reduction of PQ pool by NADH reductase|$v_{\mathrm{NDH}}$|$v_{\mathrm{NDH}}$||v_NDH|
|Cyclic electron flow|$v_{\mathrm{Cyc}}$|$v_{\mathrm{Cyc}}$||v_Cyc|
|State transitions from PSII to PSI|$v_{\mathrm{St21}}$|$v_{\mathrm{St12}}$||v_St21|
|State transitions from PSI to PSII|$v_{\mathrm{St12}}$|$v_{\mathrm{St21}}$||v_St12|
|De-epoxidation of violaxanthin|$v_{\mathrm{Deepox}}$|$v_{\mathrm{Deepox}}$||v_Deepox|
|Epoxidation of violaxanthin|$v_{\mathrm{Epox}}$|$v_{\mathrm{Epox}}$||v_Epox|
|Protonation of psbS protein|$v_{\mathrm{Psbs^P}}$|$v_{\mathrm{LHCprotonation}}$||v_PsbSP|
|Deprotonation of psbS protein|$v_{\mathrm{Psbs^D}}$|$v_{\mathrm{LHCdeprotonation}}$||v_psbSD|
|Rate of RuBisCo|$v_{\mathrm{RuBisCo}}$|$v_{\mathrm{RuBisCo}}$||v_rubisco|
|Rate of FBPase|$v_{\mathrm{FBPase}}$|$v_{\mathrm{FBPase}}$||v_FBPase|
|Rate of SBPase|$v_{\mathrm{SBPase}}$|$v_9$||v_SBPase|
|Rate of PRKase|$v_{\mathrm{PRKase}}$|$v_{13}$||v_PRKase|
|Export of PGA|$v_{\mathrm{PGA,\ ex}}$|$v_{pga}$||v_pga_ex|
|Export of DHAP|$v_{\mathrm{DHAP,\ ex}}$|$v_{DHAP}$||v_dhap_ex|
|Export of GAP|$v_{\mathrm{GAP,\ ex}}$|$v_{gap}$||v_gap_ex|
|Starch production|$v_{\mathrm{Starch}}$|$v_{\mathrm{Starch}}$||v_starch|
|Rate of PGK1ase|$v_{\mathrm{PGK1ase}}$|$v_{\mathrm{PGA\_kinase}}$||v_PGK1ase|
|Rate of BPGA dehydrogenase|$v_{\mathrm{BPGAdehynase}}$|$v_{\mathrm{BPGA\_dehydrogenase}}$||v_BPGAdehynase|
|Rate of TPIase|$v_{\mathrm{TPIase}}$|$v_{\mathrm{TPI}}$||v_TPIase|
|Rate of Aldolase of GAP and DHAP to FBP|$v_{\mathrm{Aldolase_{FBP}}}$|$v_{\mathrm{Aldolase}}$||v_Aldolase_FBP|
|Rate of TKase of GAP and F6P to X5P and E4P|$v_{\mathrm{TKase_E4P}}$|$v_{\mathrm{F6P\_ Transketolase}}$|EC 2.2.1.1|v_TKase_E4P|
|Rate of Aldolase of E4P and DHAP to SBP|$v_{\mathrm{Aldolase_{SBP}}}$|$v_{8}$||v_Aldolase_SBP|
|Rate of TKase of GAP and S7P to X5P and R5P|$v_{\mathrm{TKase_R5P}}$|$v_{10}$|EC 2.2.1.1|v_TKase_R5P|
|Rate of Rpiase|$v_{\mathrm{Rpiase}}$|$v_{11}$|EC 5.3.1.6|v_Rpiase|
|Rate of RPEase|$v_{\mathrm{RPEase}}$|$v_{12}$|EC 5.1.3.1|v_RPEase|
|Rate of PGIase|$v_{\mathrm{PGIase}}$|$v_{G6P\_ isomerase}$|AT4G24620|v_PGIase|
|Rate of PGMase|$v_{\mathrm{PGMase}}$|$v_{\mathrm{Phosphoglucomutase}}$|AT5G51820|v_PGMase|
||$v_{\mathrm{PSI}}$|$v_{\mathrm{PSI}}$||v_PSI|
|ATP consuming reaction|$v_{\mathrm{ATP}_{\mathrm{consumption}}}$|$v_{\mathrm{EX\_ ATP}}$||v_ATPcons|
|Consumption of NADPH|$v_{\mathrm{NADPH}_\mathrm{consumption}}$|$v_{\mathrm{EX\_ NADPH}}$||v_NADPHcons|
|Rate of reduction of Fd by the activity of PSI|$v_{\mathrm{Fd}_{\mathrm{red}}}$|$v_{\mathrm{Fd,\ red}}$||v_Fdred|
||$v_{\mathrm{FdTrReductase}}$|$v_{\mathrm{FdTrReductase}}$||v_FdTrReduc|
||$v_{\mathrm{MDAreduct}}$|$v_{\mathrm{MDAreduct}}$||v_MDAreduc|
||$v_{\mathrm{GR}}$|$v_{\mathrm{GR}}$||v_GR|
||$v_{\mathrm{RuBisCO}}$|$v_{\mathrm{RuBisCO}}$||v_RuBisCO|
|Rate of APXase|$v_{\mathrm{APXase}}$|$v_{\mathrm{Ascorbate}}$||v_APXase|
|Mehler reaction lumping the reduction of O2 instead of Fd|$v_{\mathrm{Mehler}}$|$v_{\mathrm{Mehler}}$||v_Mehler|
||$v_{\mathrm{DHAR}}$|$v_{\mathrm{DHAR}}$||v_DHAR|
||$v_{\mathrm{3ASC}}$|$v_{\mathrm{3ASC}}$||v_3ASC|
|Enzyme Activation|$v_{\mathrm{Eact}}$|$v_{\mathrm{Eact}}$||v_Eact|
|Enzyme inactivation|$v_{\mathrm{Einact}}$|$v_{\mathrm{Einact}}$||v_Einact|

### Tags
