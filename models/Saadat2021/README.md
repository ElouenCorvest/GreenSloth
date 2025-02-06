



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
