



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
\frac{\mathrm{d}\mathrm{PC}_\mathrm{red}}{\mathrm{d}t} = v_{\mathrm{b6f}} - v_\mathrm{PSI \vert PCoxid}
```
```math 
\frac{\mathrm{d}\mathrm{PC}_\mathrm{ox}}{\mathrm{d}t} = - v_{\mathrm{b6f}} + v_\mathrm{PSI \vert PCoxid}
```
```math 
\frac{\mathrm{d}\mathrm{PQH}_2}{\mathrm{d}t} = - 0.5 \cdot v_{\mathrm{b6f}} + 0.5 \cdot v_{\mathrm{NDH}} + 0.5 \cdot v_\mathrm{PRG5} + 0.5 \cdot v_{\mathrm{PSII}}
```
```math 
\frac{\mathrm{d}\mathrm{PQ}}{\mathrm{d}t} = 0.5 \cdot v_{\mathrm{b6f}} - 0.5 \cdot v_{\mathrm{NDH}} - 0.5 \cdot v_\mathrm{PRG5} - 0.5 \cdot v_{\mathrm{PSII}}
```
```math 
\frac{\mathrm{d}\mathrm{pH}_\mathrm{lu}}{\mathrm{d}t} = \frac{ipt_\mathrm{lu}}{b_\mathrm{H}} \cdot \left( -2 \cdot v_{\mathrm{b6f}} - 2 \cdot v_{\mathrm{NDH}} + \frac{14}{3} \cdot v_{\mathrm{ATPsynthase}} + v_\mathrm{ClCe} + v_\mathrm{KEA3} - \mathrm{PSII_{ChSep}} + v_\mathrm{PSII \vert recomb} \right)
```
```math 
\frac{\mathrm{d}\Delta \Psi _{\mathrm{thylakoid}}}{\mathrm{d}t} = vpc \cdot \left( v_{\mathrm{b6f}} + 2 \cdot v_{\mathrm{NDH}} - \frac{14}{3} \cdot v_{\mathrm{ATPsynthase}} - v_\mathrm{ClCe} + \mathrm{PSII_{ChSep}} - v_\mathrm{PSII \vert recomb} - v_\mathrm{VCCN1} - v_\mathrm{VKC} + \mathrm{PSI_{ChSep}} \right)
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
\frac{\mathrm{d}\mathrm{Q_{A \vert red}}}{\mathrm{d}t} = - v_{\mathrm{PSII}} + \mathrm{PSII_{ChSep}} - v_\mathrm{PSII \vert recomb}
```
```math 
\frac{\mathrm{d}\mathrm{Q_{A \vert ox}}}{\mathrm{d}t} = v_{\mathrm{PSII}} - \mathrm{PSII_{ChSep}} + v_\mathrm{PSII \vert recomb}
```
```math 
\frac{\mathrm{d}\mathrm{Y_2}}{\mathrm{d}t} = - v_\mathrm{PSI \vert PCoxid} + \mathrm{PSI_{ChSep}}
```
```math 
\frac{\mathrm{d}\mathrm{Y_0}}{\mathrm{d}t} = v_\mathrm{PSI \vert PCoxid} - \mathrm{PSI_{ChSep}}
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
\mathrm{psbS^P} =  \frac{1}{10^{3 \cdot \left( \mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a \vert PsbS}} \right)} + 1}
```
```math
\mathrm{NPQ} =  0.4 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{psbS^P} \cdot \mathrm{Zx} + 0.5 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{psbS^P} + 0.1 \cdot \mathrm{NPQ_{max}} \cdot \mathrm{Zx}
```
```math
\mathrm{Prot_{ATPsynth}} =  \mathrm{Act_{ATPsynth}} \cdot \left( 1 - \frac{1}{10^{\frac{\left( \mathrm{PMF} - 0.132 \right) \cdot 1.5}{0.06}} + 1} \right) \mathrm{HPR} \cdot V_\mathrm{max \vert ATPsynth} + \left( 1 - \mathrm{Act_{ATPsynth}} \right) \left( 1 - \frac{1}{10^{\frac{\left( \mathrm{PMF} - 0.204 \right) \cdot 1.5}{0.06}} + 1} \right) \mathrm{HPR} \cdot V_\mathrm{max \vert ATPsynth}
```
```math
\Phi \mathrm{PSII} =  \frac{1}{1 + \frac{1 + \mathrm{NPQ}}{4.88 \cdot \mathrm{Q_{A \vert ox}}}}
```
```math
^1\mathrm{O_2} =  v_\mathrm{PSII \vert recomb} \cdot \Phi _{\mathrm{triplet}} \cdot \Phi _{\mathrm{^1O_2}}
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
K_\mathrm{b6f} =  10^{\frac{E_\mathrm{m \vert PC \vert pH7} - \left( E_\mathrm{m \vert PQH2 \vert pH7} - 0.06 \cdot \left( \mathrm{pH}_\mathrm{lu} - 7.0 \right) \right) - \mathrm{PMF}}{0.06}}
```
```math
k_\mathrm{b6f} =  \left( 1 - \frac{1}{10^{\mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a \vert reg}}} + 1} \right) c_{\mathrm{b6f}} \cdot V_\mathrm{max \vert b6f}
```
```math
K_\mathrm{NDH1} =  10^{\frac{E_\mathrm{m \vert PQH2 \vert pH7} - 0.06 \cdot \left( \mathrm{pH}_\mathrm{st} - 7.0 \right) - E_\mathrm{m \vert Fd} - \mathrm{PMF} \cdot 2}{0.06}}
```
```math
\mathrm{Act_{ATPsynth}} =  0.2 + 0.8 \cdot \frac{\left( \frac{t}{165} \right)^{4}}{\left( \frac{t}{165} \right)^{4} + 1}
```
```math
\mathrm{PSII_{ChSep}} =  \sigma _\mathrm{II} ^0 \cdot ppPSII \cdot \Phi \mathrm{PSII}
```
```math
v_\mathrm{PSII \vert recomb} =  k_\mathrm{recomb} \cdot \mathrm{Q_{A \vert red}} \cdot 10^{\frac{\Delta \Psi _{\mathrm{thylakoid}} + 0.06 \cdot \left( 7.0 - \mathrm{pH}_\mathrm{lu} \right)}{0.06}}
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
v_\mathrm{PRG5} =  \frac{V_\mathrm{max \vert PGR} \cdot \frac{\mathrm{Fd}_\mathrm{red}^{4}}{\mathrm{Fd}_\mathrm{red}^{4} + 0.1^{4}} \cdot \mathrm{PQ}}{\mathrm{PQ} + \mathrm{PQH}_2}
```
```math
v_{\mathrm{Deepox}} =  \mathrm{Vx} \cdot V_\mathrm{max \vert VDE} \frac{1}{10^{nh_\mathrm{VDE} \cdot \left( \mathrm{pH}_\mathrm{lu} - \mathrm{pK_{a \vert VDE}} \right)} + 1} - \mathrm{Zx} \cdot k_\mathrm{kEpoxZ}
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
v_\mathrm{KEA3} =  k_\mathrm{KEA3} \cdot \left( \mathrm{H_{lu}} \cdot \mathrm{K}^{+}_{\mathrm{st}} - \mathrm{H_{st}} \cdot \mathrm{K}^{+}_{\mathrm{lu}} \right) \frac{\left( 1 - \mathrm{Q_{A \vert red}} \right)^{3}}{\left( 1 - \mathrm{Q_{A \vert red}} \right)^{3} + 0.15^{3}} \cdot \frac{1}{10^{\left( \mathrm{pH}_\mathrm{lu} - 6.0 \right)} + 1}
```
```math
v_\mathrm{VKC} =  \frac{\mathrm{P_{K^+}} \cdot \left( -0.06 \cdot \log_{10} \left( \frac{\mathrm{K}^{+}_{\mathrm{st}}}{\mathrm{K}^{+}_{\mathrm{lu}}} \right) + \Delta \Psi _{\mathrm{thylakoid}} \right) \cdot \left( \mathrm{K}^{+}_{\mathrm{lu}} + \mathrm{K}^{+}_{\mathrm{st}} \right)}{2}
```
```math
\mathrm{PSII_{ChSep}} =  \mathrm{PSII_{ChSep}}
```
```math
v_\mathrm{PSII \vert recomb} =  v_\mathrm{PSII \vert recomb}
```
```math
v_{\mathrm{PSII}} =  \mathrm{Q_{A \vert red}} \cdot \mathrm{PQ} \cdot k_\mathrm{QA} - \mathrm{PQH}_2 \cdot \mathrm{Q_{A \vert ox}} \cdot \frac{k_\mathrm{QA}}{K_\mathrm{QA}}
```
```math
\mathrm{PSI_{ChSep}} =  \mathrm{Y_0} \cdot ppPSII \cdot \sigma _\mathrm{I} ^0 \cdot \mathrm{Fd}_\mathrm{ox}
```
```math
v_\mathrm{PSI \vert PCoxid} =  \mathrm{PC}_\mathrm{red} \cdot k_\mathrm{PC \vert P700} \cdot \mathrm{Y_2}
```
```math
v_{\mathrm{FNR}} =  k_\mathrm{Fd \vert NADP} \cdot \mathrm{NADP}_\mathrm{st} \cdot \mathrm{Fd}_\mathrm{red}
```
```math
v_\mathrm{CBB} =  \frac{k_\mathrm{CBB} \cdot \left( 1 - \exp \left( \frac{-t}{600} \right) \right) \left( \ln \left( \frac{\mathrm{NADPH}_\mathrm{st}}{\mathrm{NADP}_\mathrm{st}} \right) - \ln 1.25 \right)}{\ln \left( \frac{3.5}{1.25} \right)}
```
```math
v_{\mathrm{Mehler}} =  \frac{4 \cdot 0.000265 \cdot \mathrm{Fd}_\mathrm{red}}{\mathrm{Fd}_\mathrm{red} + \mathrm{Fd}_\mathrm{ox}}
```

</details>

                     
### Figures

### Demonstrations



                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/li2021_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle using real Photosynthetic Photon Flux Density (PPFD) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal and is used to create a protocol for the light intensity PPFD over the course of the day, in a minute interval. The data used is filtered to only show a PPFD that equals or is higher than $40 \mathrm{µmol\ m^{−2}\ s^{−1}}$. This threshold is chosen as it has shown to allow most models to still simulate the photosynthetic machinery, while still being a decent representation of the actual daylight conditions. The simulation is run using the default parameters and initial conditions of each model, and the RuBisCO carboxylation rate (vRuBisCO), Adenosine Triphosphate (ATP) and Nicotinamide Adenine Dinucleotide Phosphate (NADPH) ratio, and fluorescence (F) results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

</details>



                     
<details>
<summary>FvCB Submodule</summary>
                     
<img style='float: center' src='figures/li2021_demon_fvcb.svg' alt='FvCB Submodule' width='600'/>

Comparison of modelled carbon assimilation (A) and RuBisCO carboxylation rate (vRuBisCO) against the Farquhar, von Caemmerer, and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025). To be able to simulate A, there are two mandatory quantities that need to be present in the model: carbon dioxide (CO2) concentration and vRuBisCO. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The simulation is then run until steady-state, or quasi-steady-state if not otherwise possible, for different intercellular CO2 concentration (Ci) partial pressure. The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model.

**Assumptions:**

- If no CO<sub>2</sub> concentration nor rate of rubisco carboxylation ($v_\mathrm{c}$) is present in the model, no comparison will be shown
- Infinite mesophyll conductance, therefore intercellular CO<sub>2</sub> partial pressure equals chloroplast partial pressure ($\mathrm{C_i} = \mathrm{C_c}$)
- If no $\mathrm{C_i}$ is present in the model, it will be added as a parameter assuming an initial value of CO<sub>2</sub> concentration divided by Henry's law constant for CO<sub>2</sub> ($H_\mathrm{s}^{cp}$)
- If no $H_\mathrm{s}^{cp}$ is present in the model, it will be added as a parameter with a value of $3.4 \times 10^{-4}\ \mathrm{mmol\ Pa^ {-1}}$ [[2]](https://doi.org/10.5194/acp-23-10901-2023)
- If no CO<sub>2</sub> compensation point in the absence of non-photorespiratory CO<sub>2</sub> release ($\Gamma ^*$) is present in the model, it will be added as a parameter with a value of $38.6\ \mathrm{\mu bar}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $R_\mathrm{light}$ is present in the model, it will be added as a parameter with a value of $1\ \mathrm{\mu mol\ m^{-2}\ s^{-1}}$ [[1]](https://doi.org/10.1101/2025.03.11.642611)
- If no $A$ is present in the model, it will be added as a derived variable following the FvCB equation [[1]](https://doi.org/10.1101/2025.03.11.642611): $v_\mathrm{c} \cdot \left(1 - \frac{\Gamma ^*}{C_i}\right) - R_\mathrm{light}$
- To be able to compare with original FvCB curves, the model needs to have $v_\mathrm{c}$ following the same units as the FvCB model ($\mathrm{\mu mol\ m^{-2}\ s^{-1}}$). The `mM_to_µmol_per_m2` can be used to convert from mM to $\mathrm{\mu mol\ m^{-2}}$ assuming a volume factor of $0.0112\ \mathrm{L\ m^{-2}}$ in the stroma [[3]](https://doi.org/10.1007/s11120-006-9109-1). If the given units are in mM, the conversion will be done automatically, by adding a derived parameter with the converted values.

**Notes:**

| Parameter                 | In Model          |
| -----------               | -----------       |
| $\mathrm{CO}_2$         | None          |
| $v_\mathrm{c}$          | None  |
| $\mathrm{C_i}$          | None          |
| $H_\mathrm{s}^{cp}$   | None              |
| $\Gamma ^*$               | None              |
| $R_\mathrm{light}$      | None        |
| $A$                       | None            |


</details>



                     
<details>
<summary>PAM Simulation</summary>
                     
<img style='float: center' src='figures/li2021_demon_pam.svg' alt='PAM Simulation' width='600'/>

Sample simulation of a common Pulse Amplitude Modulation (PAM) protocol to show fluctuations of fluorescence (F) and Non-Photochemical Quenching (NPQ) using saturating pulses. The simulation protocol is as follows: A dark adaptation period that simulates for 30 minutes at a dark light intensity ($40 \mathrm{µmol\ m^{−2}\ s^{−1}}$), then the actual protocol starts. The protocol consists of 22 periods with each being 2 minutes of length. That period consists of a specific light intensity of the respective type of period and ends with a saturating pulse with a length of 0.8 s and a light intensity of $3000 \mathrm{µmol\ m^{−2}\ s^{−1}}$. First, two dark periods with light intensity of $40 \mathrm{µmol\ m^{−2}\ s^{−1}}$, followed by ten light periods with light intensity of 1000 µmol m−2 s−1, then ten dark periods again. The simulation is run using the default parameters and initial conditions of each model.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{m}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{m}$.
- If $F_\mathrm{m}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{F_{\mathrm{m}\vert t=0} - F_{\mathrm{m} \vert t}}{F_{\mathrm{m} \vert t}}$

**Notes:**

</details>



                     
<details>
<summary>Photosynthesis MCA</summary>
                     
<img style='float: center' src='figures/li2021_demon_mca.svg' alt='Photosynthesis MCA' width='600'/>

A sample Metabolic Control Analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent  RuBisCO carboxylation rate (vRuBisCO), PSII rate (vPSII), PSI rate (vPSI), Cytb6f rate (vb6f) and ATP synthase rate (vATPSynth). The variables chosen should represent  carbon dioxide (CO2) concentration, Ribulose-1,5-bisphosphate (RuBP), oxidised plastoquinone (PQox), oxidised plastocyanin (PCox), denosine Triphosphate (ATP), and Nicotinamide Adenine Dinucleotide Phosphate (NADPH). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.01\%$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{p}^{x} = \frac{x_\mathrm{upper} - x_\mathrm{lower}}{2 \cdot \mathrm{disp} \cdot p}$, where $C_{p}^{x}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{disp}$ is the displacement value. $x_\mathrm{upper}$ and $x_\mathrm{lower}$ are the steady-state result of $x$ at either $+\mathrm{disp}$ and $-\mathrm{disp}$ respectively. It has to be noted that the (MCA) results can be very dependent on the other values of the parameters in the model, therefore the results shown here are only representative of the default parameter set of the model.

**Assumptions:**

- Steady-State needs to be achievable for the model to perform the MCA.
- The parameters for each coefficient, rates, and variables chosen need to be representative of the respective process.
- If a parameter, rate, or variable is not present in the model, the respective coefficient will be greyed out in the Heatmap.

**Notes:**

| Coefficient                   | In Model          |
| -----------                   | -----------       |
| $\mathrm{PSII}$             | None|
| $\mathrm{PSI}$              | None |
| $\mathrm{RuBisCO \vert C}$  | None |
| $\mathrm{cytb6f}$           | None              |
| $\mathrm{ATPsynthase}$      | None              |

| Flux                          | In Model          |
| -----------                   | -----------       |
| $\mathrm{PSII}$             | None |
| $\mathrm{PSI}$              | None |
| $\mathrm{RuBisCO \vert C}$  | None |
| $\mathrm{cytb6f}$           | None              |
| $\mathrm{ATPsynthase}$      | None              |

| Variable                  | In Model      |
| -----------               | -----------   |
| $\mathrm{CO_2}$         | None       |
| $\mathrm{RUBP}$         | None      |
| $\mathrm{PQ_{ox}}$    | None          |
| $\mathrm{PC_{ox}}$    | None          |
| $\mathrm{ATP}$          | None    |
| $\mathrm{NADPH}$        | None  |

</details>



                     
<details>
<summary>PAM Fitting</summary>
                     
<img style='float: center' src='figures/li2021_demon_fitting.svg' alt='PAM Fitting' width='600'/>

Sample fitting to experimental Non-Photochemical Quenching (NPQ) data. The NPQ data used is taken from experimental work published in von Bismarck (2022) and was acquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana (A. thaliana) plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 µs at a light intensity of $5000 \mathrm{µmol\ m^{−2}\ s^{−1}}$. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light ($903 \mathrm{µmol\ m^{−2}\ s^{−1}}$) for approximately 10 minutes, followed by a lower actinic light of ($90 \mathrm{µmol\ m^{−2}\ s^{−1}}$) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of $40 \mathrm{µmol\ m^{−2}\ s^{−1}}$ is used to avoid numerical issues. The fitting is performed using the lmfit package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help the fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parameters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{m}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{m}$.
- If $F_\mathrm{m}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{F_{\mathrm{m}\vert t=0} - F_{\mathrm{m} \vert t}}{F_{\mathrm{m} \vert t}}$

**Notes:**

</details>
