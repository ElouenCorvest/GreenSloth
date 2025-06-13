



# Li2021


[Li2021](https://doi.org/10.1038/s41477-021-00947-5)

                     
## Installation

## Summary

### Compounds

#### Part of ODE system

|Name|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Violaxanthin|$\mathrm{Vx}$|$\mathrm{Vx}$|C08614|Vx|
|Zeaxanthin concentration|$\mathrm{Zx}$|$\mathrm{Zx}$|C06098|Zx|
|Stromal ATP concentration|$\mathrm{ATP_{st}}$|$\mathrm{ATP}$|C00002|ATP_st|
|Stromal ADP concentration|$\mathrm{ADP_{st}}$|$\mathrm{ADP}$|C00008|ADP_st|
|Lumenal K+ concentration|$\mathrm{K}^{+}_{\mathrm{lu}}$|$\mathrm{K}^{+}_{\mathrm{lumen}}$|C00238|K_lu|
|Stromal K+ concentration|$\mathrm{K}^{+}_{\mathrm{st}}$|$\mathrm{K}^{+}_{\mathrm{stroma}}$|C00238|K_st|
|Lumenal Cl- concentration|$\mathrm{Cl}^{-}_{\mathrm{lu}}$|$\mathrm{Cl}^{-}_{\mathrm{lumen}}$|C00698|Cl_lu|
|Stromal Cl- concentration|$\mathrm{Cl}^{-}_{\mathrm{st}}$|$\mathrm{Cl}^{-}_{\mathrm{stroma}}$|C00698|Cl_st|
|Transthylakoid electric field|$\Delta \Psi _{\mathrm{thylakoid}}$|$\Delta \Psi$||Dpsi|
|Oxidised primary quinone of PSII|$\mathrm{Q_{A\|ox}}$|$\mathrm{Q_{A}}$||QA_ox|
|Reduced primary quinone of PSII|$\mathrm{Q_{A\|red}}$|$\mathrm{Q_{A}}^{-}$||QA_red|
|Plastoquinol|$\mathrm{PQH}_2$|$\mathrm{PQH_2}$|C16693|PQH_2|
|Plastoquinone|$\mathrm{PQ}$|$\mathrm{PQ}$|C02061|PQ|
|Reduced Plastocyanine|$\mathrm{PC}_\mathrm{red}$|$\mathrm{PC}$|C03025|PC_red|
|Oxidized Plastocyanine|$\mathrm{PC}_\mathrm{ox}$|$\mathrm{PC}^+$|C03162|PC_ox|
|Oxidized Ferrodoxin|$\mathrm{Fd}_\mathrm{ox}$|$\mathrm{Fd_{ox}}$|C00139|Fd_ox|
|Reduced Ferrodoxin|$\mathrm{Fd}_\mathrm{red}$|$\mathrm{Fd_{red}}$|C00138|Fd_red|
|Lumen pH|$\mathrm{pH}_\mathrm{lu}$|$\mathrm{pH_{lumen}}|C00080|pH_lu|
|Stromal NADPH concentration|$\mathrm{NADPH}_\mathrm{st}$|$\mathrm{NADPH}$|C00005|NADPH_st|
|Stromal NADP concentration|$\mathrm{NADP}_\mathrm{st}$|$\mathrm{NADP}^+$|C00006|NADP_st|
|Ground state of PSI (P700)|$\mathrm{Y_0}$|$\mathrm{P_{700}}$|M00163|Y0|
|Oxidised state of PSI (P700+)|$\mathrm{Y_2}$|$\mathrm{P_{700}}^+$|M00163|Y2|



<details>
<summary>ODE System</summary>

```math 
\frac{\mathrm{d}\mathrm{PC}_\mathrm{red}}{\mathrm{d}t} = v_{\mathrm{b6f}} - v_\mathrm{PSI|PCoxid}
```
```math 
\frac{\mathrm{d}\mathrm{PC}_\mathrm{ox}}{\mathrm{d}t} = - v_{\mathrm{b6f}} + v_\mathrm{PSI|PCoxid}
```
```math 
\frac{\mathrm{d}\mathrm{PQH}_2}{\mathrm{d}t} = - 0.5 \cdot v_{\mathrm{b6f}} + 0.5 \cdot v_{\mathrm{NDH}} + 0.5 \cdot v_\mathrm{PRG5} + 0.5 \cdot v_{\mathrm{PSII}}
```
```math 
\frac{\mathrm{d}\mathrm{PQ}}{\mathrm{d}t} = 0.5 \cdot v_{\mathrm{b6f}} - 0.5 \cdot v_{\mathrm{NDH}} - 0.5 \cdot v_\mathrm{PRG5} - 0.5 \cdot v_{\mathrm{PSII}}
```
```math 
\frac{\mathrm{d}\mathrm{pH}_\mathrm{lu}}{\mathrm{d}t} = \frac{ipt_\mathrm{lu}}{b_\mathrm{H}} \cdot \left( -2 \cdot v_{\mathrm{b6f}} - 2 \cdot v_{\mathrm{NDH}} + \frac{14}{3} \cdot v_{\mathrm{ATPsynthase}} + v_\mathrm{ClCe} + v_\mathrm{KEA3} - \mathrm{PSII_{ChSep}} + v_\mathrm{PSII|recomb} \right)
```
```math 
\frac{\mathrm{d}\Delta \Psi _{\mathrm{thylakoid}}}{\mathrm{d}t} = vpc \cdot \left( v_{\mathrm{b6f}} + 2 \cdot v_{\mathrm{NDH}} - \frac{14}{3} \cdot v_{\mathrm{ATPsynthase}} - v_\mathrm{ClCe} + \mathrm{PSII_{ChSep}} - v_\mathrm{PSII|recomb} - v_\mathrm{VCCN1} - v_\mathrm{VKC} + \mathrm{PSI_{ChSep}} \right)
```
```math 
\frac{\mathrm{d}\mathrm{Fd}_\mathrm{red}}{\mathrm{d}t} = - v_{\mathrm{NDH}} - v_\mathrm{PRG5} + \mathrm{PSI_{ChSep}} - v_{\mathrm{FNR}} - v_{\mathrm{Mehler}}
```
```math 
\frac{\mathrm{d}\mathrm{Fd}_\mathrm{ox}}{\mathrm{d}t} = v_{\mathrm{NDH}} + v_\mathrm{PRG5} - \mathrm{PSI_{ChSep}} + v_{\mathrm{FNR}} + v_{\mathrm{Mehler}}
```
```math 
\frac{\mathrm{d}\mathrm{Vx}}{\mathrm{d}t} = - v_{\mathrm{Deepox}}
```
```math 
\frac{\mathrm{d}\mathrm{Zx}}{\mathrm{d}t} = v_{\mathrm{Deepox}}
```
```math 
\frac{\mathrm{d}\mathrm{Cl}^{-}_{\mathrm{lu}}}{\mathrm{d}t} = 2 ipt_\mathrm{lu} \cdot v_\mathrm{ClCe} + ipt_\mathrm{lu} \cdot v_\mathrm{VCCN1}
```
```math 
\frac{\mathrm{d}\mathrm{Cl}^{-}_{\mathrm{st}}}{\mathrm{d}t} = - 2 ipt_\mathrm{st} \cdot v_\mathrm{ClCe} - 1 ipt_\mathrm{st} \cdot v_\mathrm{VCCN1}
```
```math 
\frac{\mathrm{d}\mathrm{K}^{+}_{\mathrm{lu}}}{\mathrm{d}t} = ipt_\mathrm{lu} \cdot v_\mathrm{KEA3} - 1 ipt_\mathrm{lu} \cdot v_\mathrm{VKC}
```
```math 
\frac{\mathrm{d}\mathrm{K}^{+}_{\mathrm{st}}}{\mathrm{d}t} = - 1 ipt_\mathrm{st} \cdot v_\mathrm{KEA3} + ipt_\mathrm{st} \cdot v_\mathrm{VKC}
```
```math 
\frac{\mathrm{d}\mathrm{Q_{A|red}}}{\mathrm{d}t} = - v_{\mathrm{PSII}} + \mathrm{PSII_{ChSep}} - v_\mathrm{PSII|recomb}
```
```math 
\frac{\mathrm{d}\mathrm{Q_{A|ox}}}{\mathrm{d}t} = v_{\mathrm{PSII}} - \mathrm{PSII_{ChSep}} + v_\mathrm{PSII|recomb}
```
```math 
\frac{\mathrm{d}\mathrm{Y_2}}{\mathrm{d}t} = - v_\mathrm{PSI|PCoxid} + \mathrm{PSI_{ChSep}}
```
```math 
\frac{\mathrm{d}\mathrm{Y_0}}{\mathrm{d}t} = v_\mathrm{PSI|PCoxid} - \mathrm{PSI_{ChSep}}
```
```math 
\frac{\mathrm{d}\mathrm{NADPH}_\mathrm{st}}{\mathrm{d}t} = 0.5 \cdot v_{\mathrm{FNR}} - 0.5 \cdot v_\mathrm{CBB}
```
```math 
\frac{\mathrm{d}\mathrm{NADP}_\mathrm{st}}{\mathrm{d}t} = - 0.5 \cdot v_{\mathrm{FNR}} + 0.5 \cdot v_\mathrm{CBB}
```

</details>
                     
#### Conserved quantities

|Name|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Lumenal Proton concentration|$\mathrm{H_{lu}}$|$H_{lumen}$|C00080|H_lu|
|The total proton motive force|$\mathrm{PMF}$|$pmf$||PMF|
|Concentration of protonated psbS protein|$\mathrm{psbS^P}$|$PsbS\_H$|K03542|PsbSP|
|Nonphotochemical quenching|$\mathrm{NPQ}$|$NPQ$||NPQ|
|Amount of protons going to ATPsynthase|$\mathrm{Prot_{ATPsynth}}$|$\mathrm{d\_protons\_to\_ATP}$||Prot_ATPsynth|
|Efficiency of PSII|$\Phi \mathrm{PSII}$|$\Phi \mathrm{PSII}$||PhiPSII|
|Number of $^1\mathrm{O_2}$|$^1\mathrm{O_2}$|$^1\mathrm{O_2}$|C00007|singO2|
|Stromal Proton concentration|$\mathrm{H_{st}}$|$H_{stroma}$|C00080|H_st|




<details>
<summary> Calculations </summary>

```math
\mathrm{H_{lu}} =  10^{-\mathrm{pH}_\mathrm{lu}}
```
```math
\mathrm{PMF} =  \Delta \Psi _{\mathrm{thylakoid}} + 0.06 \cdot \left( \mathrm{pH}_\mathrm{st} - \mathrm{pH}_\mathrm{lu} \right)
```
```math
\mathrm{psbS^P} =  \frac{1}{10^{3 \cdot \left( \mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a|PsbS}} \right)} + 1}
```
```math
\mathrm{NPQ} =  0.4 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{psbS^P} \cdot \mathrm{Zx} + 0.5 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{psbS^P} + 0.1 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{Zx}
```
```math
\mathrm{Prot_{ATPsynth}} =  \mathrm{Act_{ATPsynth}} \cdot \left( 1 - \frac{1}{10^{\frac{\left( \mathrm{PMF} - 0.132 \right) \cdot 1.5}{0.06}} + 1} \right) \mathrm{HPR} \cdot V_\mathrm{max|ATPsynth} + \left( 1 - \mathrm{Act_{ATPsynth}} \right) \left( 1 - \frac{1}{10^{\frac{\left( \mathrm{PMF} - 0.204 \right) \cdot 1.5}{0.06}} + 1} \right) \mathrm{HPR} \cdot V_\mathrm{max|ATPsynth}
```
```math
\Phi \mathrm{PSII} =  \frac{1}{1 + \frac{1 + \mathrm{NPQ}}{4.88 \cdot \mathrm{Q_{A|ox}}}}
```
```math
^1\mathrm{O_2} =  v_\mathrm{PSII|recomb} \cdot \Phi _{\mathrm{triplet}} \cdot \Phi _{\mathrm{^1O_2}}
```
```math
\mathrm{H_{st}} =  10^{-\mathrm{pH}_\mathrm{st}}
```

</details>

                     
### Parameters

|Short Description|Common Abbr.|Paper Abbr.|Value|Unit|Python Var|Reference|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Stromal concentration of orthophosphate|$\mathrm{P}_\mathrm{i,\ st}$|$\mathrm{P}_\mathrm{i}$|$1.5$|$\mathrm{mM}$|Pi_st||
|The maximum turnover rate for oxidation of PQH2 by the b6f complex at high pH|$V_\mathrm{max\|b6f}$|$V_{max}\left( \mathrm{b6f} \right)$|$300$|$\mathrm{s}^{-1}$|Vmax_b6f||
|Relative content of cytochrome b6f to PSII|$c_{\mathrm{b6f}}$|$\mathrm{cytochrome b_6f content}$|$0.433$|$\mathrm{PSII}^{-1}$|c_b6f||
|The regulatory pKa at which the cytochrome b6f complex is slowed by lumen pH|$\mathrm{pK_{a\|reg}}$|$\mathrm{pK_{reg}}$|$6.2$||pKa_reg||
|The midpoint potential of the plastocyanin couple at pH=7|$E_\mathrm{m\|PC\|pH7}$|$Em_\mathrm{PC\_pH7}$|$0.37$|$\mathrm{V}$|Em_PC_pH7||
|The midpoint potential of the PQ/PQH2 couple at pH=7|$E_\mathrm{m\|PQH2\|pH7}$|$Em_\mathrm{PQH2\_pH7}$|$0.11$|$\mathrm{V}$|Em_PQH2_pH7||
|The midpoint potential of ferredoxin|$E_\mathrm{m\|Fd}$|$Em_{Fd}$|$-0.42$|$\mathrm{V}$|Em_Fd||
|The rate constant for NDH|$k_\mathrm{NDH1}$|$k_\mathrm{{NDH}}$|$1000$|$\mathrm{s}^{-1}$|k_NDH1||
|The maximal turnover of the PGR5/PGRL1|$V_\mathrm{max\|PGR}$|$V_{max}\left( \mathrm{PGR} \right)$|$0$||Vmax_PGR||
|The maximal turnover of the fully protonated VDE enzyme|$V_\mathrm{max\|VDE}$|$V_{max}\left( \mathrm{VDE} \right)$|$0.08$|$\mathrm{s}^{-1}$|Vmax_VDE||
|The pKa for protonation and activation of VDE|$\mathrm{pK_{a\|VDE}}$|$\mathrm{pK_{VDE}}$|$5.65$||pKa_VDE||
|The Hill coefficient for protonation of VDE|$nh_\mathrm{VDE}$|$\mathrm{Hill_{VDE}}$|$4$||nh_VDE||
|The rate constant for ZE (zeaxanthin epoxidase)|$k_\mathrm{kEpoxZ}$|$k_\mathrm{ZE}|$0.004$|$\mathrm{s}^{-1}$|k_EZ||
|The pKa for protonation and activation of PsbS|$\mathrm{pK_{a\|PsbS}}$|$\mathrm{pK_{PsbS}}$|$6.2$||pKa_PsbS||
|Comparision of the H+/ATP ratios of ATP synthase|$\Delta _\mathrm{f} G^\circ_\mathrm{ATP}$|$\Delta G_{\mathrm{ATP}}$|$36$|$\mathrm{kJ}\ \mathrm{mol}^{-1}$|DeltaG0_ATP||
|Ratio of protons to ATP in ATP synthase|$\mathrm{HPR}$|$\mathrm{HPR}$|$\frac{14}{3}$||HPR||
|Normalized maximal rate of ATP synthase|$V_\mathrm{max\|ATPsynth}$|$V_\mathrm{max\|ATPsynth}$|$200$|$\mathrm{s}^{-1}$|Vmax_ATPsynth||
|Faraday constant|$F$|$F$|$96.485$|$\mathrm{kJ}$|F||
|Maximum NPQ|$\mathrm{NPQ_{max}}$|$NPQ_{max}$|$3$||NPQ_max||
|The average recombination rate for S2QA- and S3QA-|$k_\mathrm{recomb}$|$k_{recomb}$|$0.33$|$\mathrm{s}^{-1}$|k_recomb||
|The yield of triplets from each recombination event|$\Phi _{\mathrm{triplet}}$|$\Phi _{triplet}$|$0.45$||phi_triplet||
|The yield of 1O2 for each triplet formed|$\Phi _{\mathrm{^1O_2}}$|$\Phi _{O_2}^1$|$1$||phi_1O2||
|Photosynthetically active radiation|$\mathrm{PAR}$|$\mathrm{PAR}$|$10$|$\mathrm{photons\ m^{-2}}$|PAR||
|The maximum relative rate of PSII centers (0-1)|||$1$|$6 \times 10^{10} \mathrm{complexes}\ \mathrm{cm}^{-2}$|PSII_max||
|The relative antenna size of PSII|$\sigma _\mathrm{II} ^0$|$\mathrm{PSII_{antenna_size}}$|$0.5$||sigma0_II||
|The averate rate constant of oxidation of QA- by QB and PQ|$k_\mathrm{QA}$|$k_\mathrm{{QA}}$|$1000$|$\mathrm{s}^{-1}$|k_QA||
|Equilibrium constant of QA- by QB and PQ|$K_\mathrm{QA}$|$Keq_{QA \rightarrow PQ}$S|$200$||K_QA||
|The capcitance of the thylakoid expressed as V/charge/PSII|$vpc$|$\mathrm{Volts\_per\_charge}$|$0.047$|$\mathrm{V}$|vpc||
|The relative cross section of PSI antenna|$\sigma _\mathrm{I} ^0$|$\mathrm{PSI_{antenna_size}}$|$0.5$||sigma0_I||
|Lumenal concentration change of ion per turnover|$ipt_\mathrm{lu}$|$\mathrm{lumen\_protons\_per\_turnover}$|$0.000587$|$\mathrm{M}$|ipt_lu||
|The proton buffering capacity of the lumen in M/pH unit|$b_\mathrm{H}$|$\mathrm{Buffering\ capacity}$|$0.014$|$\mathrm{M}\ \left( \mathrm{pH\ unit} \right)^{-1}$|b_H||
|Stromal concentration change of ion per turnover|$ipt_\mathrm{st}$|$\mathrm{stroma\_protons\_per\_turnover}$|$5.87e-05$|$\mathrm{M}$|ipt_st||
|The relative permeability of the thylakoid to counterions|$\mathrm{P_{K^+}}$|$\mathrm{Perm_K}$|$150$|$\mathrm{s}^{-1}\ \mathrm{V}^{-1}$|P_K||
|The rate constant for VCCN1 moving Cl- from stroma to lumen|$k_\mathrm{VCCN1}$|$k_{VCCN1}$|$12$|$\mathrm{s}^{-1}\ \mathrm{M}^{-1}$|k_VCCN1||
|The rate constant for CLCE2 moving Cl- from lumen to stroma, driving by H+ gradient|$k_\mathrm{ClCe}$|$k_{CLCE}$|$80000$|$\mathrm{s}^{-1}\ \mathrm{M}^{-2}\ \mathrm{V}^{-1}$|k_ClCe||
|The rate constant for transfer of electrons from PC to P700+|$k_\mathrm{PC\|P700}$|$k_{PC\_to\_P700}$|$5000$|$\mathrm{M}$|k_PCtoP700||
|The rate constant for the KEA H+/H+ antiporter|$k_\mathrm{KEA3}$|$k_{KEA3}$|$2500000$|$\mathrm{s}^{-1}\ \mathrm{M}^{-2}$|k_KEA3||
|The second order rate constant for oxidation of Fd by NADP+|$k_\mathrm{Fd\|NADP}$|$k_\mathrm{Fd\_to\_NADP}$|$1000$||k_FdtoNADP||
|The rate constant for a simplified Calvin-Benson Cycle|$k_\mathrm{CBB}$|$k_{CBC}$|$60$|$\mathrm{s}^{-1}$|k_CBB||
|Rate constant of Proton leak|$k_\mathrm{Leak}$|$k_{leak}$|$30000000$|$\mathrm{s}^{-1}\ \mathrm{M}^{-1}\ \mathrm{V}^{-1}$|k_Leak||
|Stroma pH|$\mathrm{pH}_\mathrm{st}$|$\mathrm{pH_{stroma}}$|$7.8$||pH_st||

#### Derived Parameters

|Short Description|Common Abbr.|Paper Abbr.|Python Var|
| :---: | :---: | :---: | :---: |
|PAR photons per PSII|$ppPSII$|$\mathrm{light\_per\_L}$|ppPSII|
|Equilibrium constant of Cytochrome b6f|$K_\mathrm{b6f}$|$Keq_{b6f}$|K_b6f|
|Rate constant of Cytochrome b6f|$k_\mathrm{b6f}$|$k_{b6f}$|k_b6f|
|Equilibrium constant of NDH1|$K_\mathrm{NDH1}$|$Keq_{NDH}$|K_NDH1|
|ATPsynthase activity|$\mathrm{Act_{ATPsynth}}$|$\mathrm{ATP\_synthase\_actvt}$|Act_ATPsynth|
|Number of charge seperations in PSII per second|$\mathrm{PSII_{ChSep}}$|$PSII_{charge}$|PSII_ChSep|
|Rate of PSII recombination|$v_\mathrm{PSII\|recomb}$|$PSII_{recom}$|PSII_recomb|
|Driving force of Cl-|${\mathrm{Cl}^- _{\mathrm{df}}}$|$\mathrm{driving\_force\_Cl}$|Cl_df|




<details>
<summary>Equations of derived parameters</summary>

```math
ppPSII =  0.84 \cdot \frac{\mathrm{PAR}}{0.7}
```
```math
K_\mathrm{b6f} =  10^{\frac{E_\mathrm{m|PC|pH7} - \left( E_\mathrm{m|PQH2|pH7} - 0.06 \cdot \left( \mathrm{pH}_\mathrm{lu} - 7.0 \right) \right) - \mathrm{PMF}}{0.06}}
```
```math
k_\mathrm{b6f} =  \left( 1 - \frac{1}{10^{\mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a|reg}}} + 1} \right) c_{\mathrm{b6f}} \cdot V_\mathrm{max|b6f}
```
```math
K_\mathrm{NDH1} =  10^{\frac{E_\mathrm{m|PQH2|pH7} - 0.06 \cdot \left( \mathrm{pH}_\mathrm{st} - 7.0 \right) - E_\mathrm{m|Fd} - \mathrm{PMF} \cdot 2}{0.06}}
```
```math
\mathrm{Act_{ATPsynth}} =  0.2 + 0.8 \cdot \frac{\left( \frac{t}{165} \right)^{4}}{\left( \frac{t}{165} \right)^{4} + 1}
```
```math
\mathrm{PSII_{ChSep}} =  \sigma _\mathrm{II} ^0 \cdot ppPSII \cdot \Phi \mathrm{PSII}
```
```math
v_\mathrm{PSII|recomb} =  k_\mathrm{recomb} \cdot \mathrm{Q_{A|red}} \cdot 10^{\frac{\Delta \Psi _{\mathrm{thylakoid}} + 0.06 \cdot \left( 7.0 - \mathrm{pH}_\mathrm{lu} \right)}{0.06}}
```
```math
{\mathrm{Cl}^- _{\mathrm{df}}} =  0.06 \cdot \log_{10} \left( \frac{\mathrm{Cl}^{-}_{\mathrm{st}}}{\mathrm{Cl}^{-}_{\mathrm{lu}}} \right) + \Delta \Psi _{\mathrm{thylakoid}}
```

</details>

                     
### Reaction Rates

|Short Description|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Rate of the b6f complex|$v_{\mathrm{b6f}}$|$v_{b6f}$|R03817|v_b6f|
|Reduction of PQ pool by NADH reductase|$v_{\mathrm{NDH}}$|$v_{NDH}$||v_NDH|
|Rate of PRG5|$v_\mathrm{PRG5}$|$v_{PGR}$||v_PGR|
|De-epoxidation of violaxanthin|$v_{\mathrm{Deepox}}$|$v_{VDE}$|R10070|v_Deepox|
|Production of ATP by ATPsynthase|$v_{\mathrm{ATPsynthase}}$|$v_{ATPsynthase}$|R00086|v_ATPsynth|
|Rate of main voltage-gated chloride channel (VCCN1)|$v_\mathrm{VCCN1}$|$v_{VCCN1}$||v_VCCN1|
|Rate of ClCe|$v_\mathrm{ClCe}$|$v_{ClCe}$||v_ClCe|
|Rate of K+/H+ anitporter KEA3|$v_\mathrm{KEA3}$|$v_{KEA3}$||v_KEA3|
|Rate of voltage-gated K+ channel|$v_\mathrm{VKC}$|$v_{K\_channel}$||v_VKC|
|Number of charge seperations in PSII per second|$\mathrm{PSII_{ChSep}}$|$PSII_{charge}$||vPSII_ChSep|
|Rate of PSII recombination|$v_\mathrm{PSII\|recomb}$|$PSII_{recom}$||vPSII_recomb|
|Reduction of PQ due to PSII|$v_{\mathrm{PSII}}$|$v_{PSII}$|R09503|v_PSII|
|Number of charge seperations in PSII per second|$\mathrm{PSI_{ChSep}}$|$PSI_{charge}$||PSI_ChSep|
|Rate of PC oxidiation by PSI|$v_\mathrm{PSI\|PCoxid}$|$PSI_{PC\_oxidiation}$||v_PSI_PCoxid|
|Reaction mediated by FNR|$v_{\mathrm{FNR}}$|$v_{FNR}$|R01195|v_FNR|
|The rate for a simplified Calvin-Benson Cycle|$v_\mathrm{CBB}$|$v_{CBB}$||v_CBB|
|Mehler reaction lumping the reduction of O2 instead of Fd|$v_{\mathrm{Mehler}}$|$v_{Mehler}$||v_Mehler|




<details>
<summary>Rate equations</summary>

```math
v_{\mathrm{b6f}} =  \frac{\mathrm{PQH}_2}{\mathrm{PQH}_2 + \mathrm{PQ}} \cdot \mathrm{PC}_\mathrm{ox} \cdot k_\mathrm{b6f} - \left( 1 - \frac{\mathrm{PQH}_2}{\mathrm{PQH}_2 + \mathrm{PQ}} \right) \cdot \mathrm{PC}_\mathrm{red} \cdot \frac{k_\mathrm{b6f}}{K_\mathrm{b6f}}
```
```math
v_{\mathrm{NDH}} =  k_\mathrm{NDH1} \cdot \mathrm{Fd}_\mathrm{red} \cdot \mathrm{PQ} - \frac{k_\mathrm{NDH1}}{K_\mathrm{NDH1}} \cdot \mathrm{Fd}_\mathrm{ox} \cdot \mathrm{PQH}_2
```
```math
v_\mathrm{PRG5} =  \frac{V_\mathrm{max|PGR} \cdot \frac{\mathrm{Fd}_\mathrm{red}^{4}}{\mathrm{Fd}_\mathrm{red}^{4} + 0.1^{4}} \cdot \mathrm{PQ}}{\mathrm{PQ} + \mathrm{PQH}_2}
```
```math
v_{\mathrm{Deepox}} =  \mathrm{Vx} \cdot V_\mathrm{max|VDE} \frac{1}{10^{nh_\mathrm{VDE} \cdot \left( \mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a|VDE}} \right)} + 1} - \mathrm{Zx} \cdot k_\mathrm{kEpoxZ}
```
```math
v_{\mathrm{ATPsynthase}} = \left\{ 
  \begin{array}{ c l }
    \mathrm{Prot_{ATPsynth}} + \mathrm{PMF} \cdot k_\mathrm{Leak} \cdot \mathrm{H_{lu}} & \quad \textrm{if } ppPSII > 0 \\
    \mathrm{PMF} \cdot k_\mathrm{Leak} \cdot \mathrm{H_{lu}} & \quad \textrm{else}
  \end{array}
\right.
```
```math
v_\mathrm{VCCN1} =  \frac{k_\mathrm{VCCN1} \cdot \left( 332 \cdot {\mathrm{Cl}^- _{\mathrm{df}}}^{3} + 30.8 \cdot {\mathrm{Cl}^- _{\mathrm{df}}}^{2} + 3.6 \cdot {\mathrm{Cl}^- _{\mathrm{df}}} \right) \cdot \left( \mathrm{Cl}^{-}_{\mathrm{st}} + \mathrm{Cl}^{-}_{\mathrm{lu}} \right)}{2}
```
```math
v_\mathrm{ClCe} =  \frac{k_\mathrm{ClCe} \cdot \left( {\mathrm{Cl}^- _{\mathrm{df}}} \cdot 2 + \mathrm{PMF} \right) \cdot \left( \mathrm{Cl}^{-}_{\mathrm{st}} + \mathrm{Cl}^{-}_{\mathrm{lu}} \right) \cdot \left( \mathrm{H_{lu}} + \mathrm{H_{st}} \right)}{4}
```
```math
v_\mathrm{KEA3} =  k_\mathrm{KEA3} \cdot \left( \mathrm{H_{lu}} \cdot \mathrm{K}^{+}_{\mathrm{st}} - \mathrm{H_{st}} \cdot \mathrm{K}^{+}_{\mathrm{lu}} \right) \frac{\left( 1 - \mathrm{Q_{A|red}} \right)^{3}}{\left( 1 - \mathrm{Q_{A|red}} \right)^{3} + 0.15^{3}} \cdot \frac{1}{10^{\left( \mathrm{pH}_\mathrm{lu} - 6.0 \right)} + 1}
```
```math
v_\mathrm{VKC} =  \frac{\mathrm{P_{K^+}} \cdot \left( -0.06 \cdot \log_{10} \left( \frac{\mathrm{K}^{+}_{\mathrm{st}}}{\mathrm{K}^{+}_{\mathrm{lu}}} \right) + \Delta \Psi _{\mathrm{thylakoid}} \right) \cdot \left( \mathrm{K}^{+}_{\mathrm{lu}} + \mathrm{K}^{+}_{\mathrm{st}} \right)}{2}
```
```math
\mathrm{PSII_{ChSep}} =  \mathrm{PSII_{ChSep}}
```
```math
v_\mathrm{PSII|recomb} =  v_\mathrm{PSII|recomb}
```
```math
v_{\mathrm{PSII}} =  \mathrm{Q_{A|red}} \cdot \mathrm{PQ} \cdot k_\mathrm{QA} - \mathrm{PQH}_2 \cdot \mathrm{Q_{A|ox}} \cdot \frac{k_\mathrm{QA}}{K_\mathrm{QA}}
```
```math
\mathrm{PSI_{ChSep}} =  \mathrm{Y_0} \cdot ppPSII \cdot \sigma _\mathrm{I} ^0 \cdot \mathrm{Fd}_\mathrm{ox}
```
```math
v_\mathrm{PSI|PCoxid} =  \mathrm{PC}_\mathrm{red} \cdot k_\mathrm{PC|P700} \cdot \mathrm{Y_2}
```
```math
v_{\mathrm{FNR}} =  k_\mathrm{Fd|NADP} \cdot \mathrm{NADP}_\mathrm{st} \cdot \mathrm{Fd}_\mathrm{red}
```
```math
v_\mathrm{CBB} =  \frac{k_\mathrm{CBB} \cdot \left( 1 - \exp \left( \frac{-t}{600} \right) \right) \left( \ln \left( \frac{\mathrm{NADPH}_\mathrm{st}}{\mathrm{NADP}_\mathrm{st}} \right) - \ln 1.25 \right)}{\ln \left( \frac{3.5}{1.25} \right)}
```
```math
v_{\mathrm{Mehler}} =  \frac{4 \cdot 0.000265 \cdot \mathrm{Fd}_\mathrm{red}}{\mathrm{Fd}_\mathrm{red} + \mathrm{Fd}_\mathrm{ox}}
```

</details>

                     
### Figures
