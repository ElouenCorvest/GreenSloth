



# Bellasio2019

## Summary


The [Bellasio2019](https://doi.org/10.1007/s11120-018-0601-1) model is a generalized C<sub>3</sub> leaf-photosynthesis model, that includes simplified representations of the light and dark reactions and a stomatal behaviour submodule. A lot of its implementation is based on past work by the same author and is mainly inspired by the common Farquhar-von Caemmerer-Berry model. The light reactions are modified from Yin et al. (2004) and include the potential rate sof ATP and NADPH production based on light intensity.

                     
## Installation



All the files needed to run this model are located in [model](./model) folder. To use this model you only need to copy this folder and write the following to import the model in your Python script:

```python
from model import Bellasio2019
```

The packages required to run this model can either be installed by using the `pixi` environment located inside the [pyproject.toml](../pyproject.toml) file or by just installing the `mxlpy` package and all its dependencies.
                     
### Compounds

#### Part of ODE system

|Name|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Carbon Dioxide|$\left[\mathrm{CO_2}\right]$|$\left[\mathrm{CO_2}\right]$|C00011|CO2|
|Bicarbonate|$\left[\mathrm{HCO_3^-}\right]$|$\left[\mathrm{HCO_3^-}\right]$||HCO3|
|Ribulose 1,5-bisphosphate|$\mathrm{RUBP}$|$\left[\mathrm{RuBP}\right]$|C01182|RUBP|
|3-phosphoglyceric acid|$\mathrm{PGA}$|$\left[\mathrm{PGA}\right]$|C00197|PGA|
|Dihydroxyacetone phosphate|$\mathrm{DHAP}$|$\left[\mathrm{DHAP}\right]$|C00111|DHAP|
|Stromal ATP concentration|$\mathrm{ATP_{st}}$|$\left[\mathrm{ATP}\right]$|C00002|ATP_st|
|Stromal NADPH concentration|$\mathrm{NADPH}_\mathrm{st}$|$\left[\mathrm{NADPH}\right]$|C00005|NADPH_st|
|Ribulose 5-phosphate|$\mathrm{RU5P}$|$\left[\mathrm{RuP}\right]$|C00199|RU5P|
|RuBisCO activation state|$R_{\mathrm{act}}$|$R_{\mathrm{act}}$|EC 4.1.1.39|Ract|
|Total NADPH production|$J_\mathrm{NADPH}$|$J_\mathrm{NADPH}$||J_NADPH|
|Total ATP production|$J_\mathrm{ATP}$|$J_\mathrm{ATP}$||J_ATP|
|Intercellular $\mathrm{CO_2}$ concentration|$C_\mathrm{i}$|$C_\mathrm{i}$||Ci|
|Stomatal conductance of water vapour to the atmosphere|$g_\mathrm{S}$|$g_\mathrm{S}$||gs|



<details>
<summary>ODE System</summary>

```math 
\frac{\mathrm{d}R_{\mathrm{act}}}{\mathrm{d}t} = v_{R_\mathrm{act}}
```
```math 
\frac{\mathrm{d}J_\mathrm{NADPH}}{\mathrm{d}t} = v_{J_\mathrm{NADPH}}
```
```math 
\frac{\mathrm{d}J_\mathrm{ATP}}{\mathrm{d}t} = v_{J_\mathrm{ATP}}
```
```math 
\frac{\mathrm{d}g_\mathrm{S}}{\mathrm{d}t} = v_{g_\mathrm{S}}
```
```math 
\frac{\mathrm{d}\left[\mathrm{CO_2}\right]}{\mathrm{d}t} = \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Carboxylase}} + \frac{0.5}{V_\mathrm{M}} \cdot v_{\mathrm{GDC}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{CAase}} + \frac{1.0}{V_\mathrm{M}} \cdot R_\mathrm{light} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{CO_{2 \vert diss}}}
```
```math 
\frac{\mathrm{d}\mathrm{RUBP}}{\mathrm{d}t} = \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Carboxylase}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Oxy}} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PRKase}}
```
```math 
\frac{\mathrm{d}\mathrm{PGA}}{\mathrm{d}t} = \frac{2.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Carboxylase}} + \frac{0.5}{V_\mathrm{M}} \cdot v_{\mathrm{GDC}} - \left( \frac{1}{3} \right) \frac{1}{V_\mathrm{M}} \cdot R_\mathrm{light} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Oxy}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PGAreduc}}
```
```math 
\frac{\mathrm{d}\mathrm{ATP_{st}}}{\mathrm{d}t} = \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Oxy}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PRKase}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PGAreduc}} + \frac{-0.5}{V_\mathrm{M}} \cdot v_{\mathrm{carbsyn}} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{ATPsynthase}}
```
```math 
\frac{\mathrm{d}\mathrm{NADPH}_\mathrm{st}}{\mathrm{d}t} = \frac{-0.5}{V_\mathrm{M}} \cdot v_{\mathrm{RuBisCO \vert Oxy}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PGAreduc}} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{FNR}}
```
```math 
\frac{\mathrm{d}\mathrm{DHAP}}{\mathrm{d}t} = - \left( \frac{5}{3} \right) \frac{1}{V_\mathrm{M}} \cdot v_{\mathrm{PRKase}} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PGAreduc}} + \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{carbsyn}}
```
```math 
\frac{\mathrm{d}\mathrm{RU5P}}{\mathrm{d}t} = \frac{-1.0}{V_\mathrm{M}} \cdot v_{\mathrm{PRKase}} + \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{rpp}}
```
```math 
\frac{\mathrm{d}\left[\mathrm{HCO_3^-}\right]}{\mathrm{d}t} = \frac{1.0}{V_\mathrm{M}} \cdot v_{\mathrm{CAase}}
```
```math 
\frac{\mathrm{d}C_\mathrm{i}}{\mathrm{d}t} = - v_{\mathrm{CO_{2 \vert diss}}} + v_{\mathrm{CO_{2 \vert stomdiff}}}
```

</details>
                     
#### Conserved quantities

|Name|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Stromal ADP concentration|$\mathrm{ADP_{st}}$|$\mathrm{ADP}$|C00008|ADP_st|
|Stromal NADP concentration|$\mathrm{NADP}_\mathrm{st}$|$\mathrm{NADP}$|C00006|NADP_st|
|Stromal concentration of orthophosphate|$\mathrm{P}_\mathrm{i,\ st}$|$\mathrm{P_i}$|C00009|Pi_st|
|Efficiency of PSII|$\Phi \mathrm{PSII}$|$Y\mathrm{(II)}$||PhiPSII|
|$\mathrm{CO}_2$ assimilation|$A$|$A$||A|
|Oxygen Concentration|$\mathrm{O_2}$|$O_2$||O2|




<details>
<summary> Calculations </summary>

```math
\mathrm{ADP_{st}} =  AP_\mathrm{Tot} - \mathrm{ATP_{st}}
```
```math
\mathrm{NADP}_\mathrm{st} =  \mathrm{NAD_{Tot}} - \mathrm{NADPH}_\mathrm{st}
```
```math
\mathrm{P}_\mathrm{i,\ st} =  \mathrm{P_i} - \mathrm{PGA} - \mathrm{DHAP} - \mathrm{RU5P} - 2 \mathrm{RUBP} - \mathrm{ATP_{st}}
```
```math
\Phi \mathrm{PSII} =  \Phi (\mathrm{II})_0 \cdot \frac{v_{\mathrm{ATPsynthase}}}{J_\mathrm{ATP}} \frac{v_{\mathrm{FNR}}}{J_\mathrm{NADPH}} \cdot \left( 1 - \mathrm{max} \left( 0, \mathrm{non\_rect\_hyperbole} \left( \mathrm{PPFD}, \alpha_\mathrm{PPFD \vert \Phi (\mathrm{II})}, V_\mathrm{0 \vert PPFD \vert \Phi (\mathrm{II})}, \theta_\mathrm{PPFD \vert \Phi (\mathrm{II})} \right) \right) \right)
```
```math
A =  v_{\mathrm{RuBisCO \vert Carboxylase}} - 0.5 v_{\mathrm{RuBisCO \vert Oxy}} - R_\mathrm{light}
```
```math
\mathrm{O_2} =  \frac{p(\mathrm{O_2})}{K_\mathrm{h \vert O_2}}
```

</details>

                     
### Parameters

|Short Description|Common Abbr.|Paper Abbr.|Value|Unit|Python Var|Reference|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|Total adenylates|$AP_\mathrm{Tot}$|$A_\mathrm{Tot}$|$1.5$|$\mathrm{mM}$|AP_tot|Wang et al. 2014|
|Total inorganic phosphorus|$\mathrm{P_i}$|$[P_\mathrm{i}]$|$15$|$\mathrm{mM}$|Pi_tot|Lilley et al. 1977|
|$\mathrm{O_2}$ partial pressure (gas)|$p(\mathrm{O_2})$|$\mathrm{p\ O_2}$|$210000$|$\mathrm{\mu bar}$|p_o2||
|$\mathrm{O_2}$ volatility|$K_\mathrm{h\|O_2}$|$K_\mathrm{h}\ \mathrm{O_2}$|$833300$|$\mathrm{\mu bar mM^{-1}}$|Kh_o2|Warneck and Williams 2012|
|Mesophyll volume per $\mathrm{m^2}$ of leaf|$V_\mathrm{M}$|Volume M|$0.03$|$\mathrm{dm^3\ m^{-2}}$|V_m||
|Incident radiation|$\mathrm{PPFD}$|$I_\mathrm{inc}$|$1500$|$\mathrm{\mu\ mol\ m^{-2}\ s^{-1}}$|PPFD||
|Respiration in the light|$R_\mathrm{light}$|$R_\mathrm{LIGHT}$|$0.001$|$\mathrm{\mu\ mol\ m^{-2}\ s^{-1}}$|RLight||
|Lumped energy conversion coefficient|$s_\mathrm{ener}$|$s$|$0.43$|$\mathrm{electrons\ quanta^{-1}}$|s|Bellasio et al. 2016|
|Yield of PSII extrapolate under zero PPFD|$\Phi (\mathrm{II})_0$|$Y(II)_\mathrm{LL}$|$0.72$||PhiPSII_LL|Bellasio et al. 2016|
|Yield of PSI extrapolate under zero PPFD|$\Phi (\mathrm{I})_0$|$Y(I)_\mathrm{LL}$|$1$|$\mathrm{electrons\ quanta^{-1}}$|PhiPSI_LL|Yin et al. 2004|
|Initial slope of PPFD hyperbola in regard of $\Phi (\mathrm{II})$|$\alpha_\mathrm{PPFD\|\Phi (\mathrm{II})}$|$\alpha_{Y(II)}$|$0.00125$||alpha_ppfd_PhiPSII||
|Y-intercept of PPFD hyperbola in regard of $\Phi (\mathrm{II})$|$V_\mathrm{0\|PPFD\|\Phi (\mathrm{II})}$|$V_{0Y(II)}$|$-0.8$||V0_ppfd_PhiPSII||
|Curvature of PPFD hyperbola in regard of $\Phi (\mathrm{II})$|$\theta_\mathrm{PPFD\|\Phi (\mathrm{II})}$|$\theta_{Y(II)}$|$0.7$||theta_ppfd_PhiPSII||
|Fraction of electron flow used by nitrate assimilation|$f_\mathrm{PseudocycNR}$|$f_\mathrm{PSEUDO\ NR}$|$0.01$||f_pseudocycNR||
|Fraction of electron flow through the Q-cycle|$f_\mathrm{Q}$|$f_\mathrm{Q}$|$1$||fq|Yin et al. 2004|
|Fraction of electron flow through the NDH complex|$f_\mathrm{NDH}$|$f_\mathrm{NDH}$|$0$||f_ndh|Yamori and Shikanai 2016|
|Number of protons per ATP|$h$|$h$|$4$|$\mathrm{protons ATP^{-1}}$|h|Yin and Struik 2012|
|Atmospheric $\mathrm{CO_2}$ concentration|$C_\mathrm{a}$|$C_\mathrm{a}$|$400$|$\mathrm{\mu bar}$|Ca||
|Initial slope of PPFD hyperbola in regard of RuBisCO|$\alpha_\mathrm{PPFD\|RuBisCO}$|$\alpha_\mathrm{V}$|$0.0018$||alpha_ppfd_rub||
|Y-intercept of PPFD hyperbola in regard of RuBisCO|$V_\mathrm{0\|PPFD\|RuBisCO}$|$V_{0}$|$0.16$||V0_ppfd_rub||
|Curvature of PPFD hyperbola in regard of RuBisCO|$\theta_\mathrm{PPFD\|RuBisCO}$|$\theta_\mathrm{V}$|$0.95$||theta_ppfd_rub||
|Initial slope of $\mathrm{CO_2}$ hyperbola in regard of RuBisCO|$\alpha_\mathrm{CO_2\|RuBisCO}$|$\alpha_\mathrm{C}$|$400$||alpha_co2||
|Y-intercept of $\mathrm{CO_2}$ hyperbola in regard of RuBisCO|$V_\mathrm{0\|CO_2\|RuBisCO}$|$V_{0C}$|$-0.2$||V0_co2||
|Curvature of $\mathrm{CO_2}$ hyperbola in regard of RuBisCO|$\theta_\mathrm{CO_2\|RuBisCO}$|$\theta_\mathrm{C}$|$0.98$||theta_co2||
|Time constant for RuBisCO induction|$\tau_{\mathrm{i}\|R_\mathrm{act}}$|$\tau_\mathrm{i}$|$360$|$\mathrm{s}$|tau_i|Seemann et al. 1988|
|Time constant for RuBisCO deactivation|$\tau_{\mathrm{d}\|R_\mathrm{act}}$|$\tau_\mathrm{d}$|$1200$|$\mathrm{s}$|tau_d|Seemann et al. 1988|
|Michealis-Menten constant for $\mathrm{CO_2}$ in RuBisCO carboxylase|$K_\mathrm{m\|RuBisCO\|CO_2}$|$K_\mathrm{C}$|$0.014$|$\mathrm{mM}$|km_v_RuBisCO_c_CO2|von Caemmerer 2000|
|Michealis-Menten constant for RUBP in RuBisCO carboxylase|$K_\mathrm{m\|RuBisCO\|RUBP}$|$K_\mathrm{m}\ \mathrm{RuBP}$|$0.02$|$\mathrm{mM}$|km_v_RuBisCO_c_RUBP|Zhu et al. 2007|
|Michealis-Menten constant for $\mathrm{O_2}$ in RuBisCO carboxylase|$K_\mathrm{m\|RuBisCO\|O_2}$|$K_\mathrm{O}$|$0.222$|$\mathrm{mM}$|km_v_RuBisCO_c_O2|Zhu et al. 2007|
|Inhibition constant for PGA in RuBisCO carboxylase|$K_\mathrm{i\|RuBisCO\|PGA}$|$K_\mathrm{i}\ \mathrm{PGA}$|$2.52$|$\mathrm{mM}$|ki_v_RuBisCO_c_PGA|Zhu et al. 2007|
|Inhibition constant for NADP in RuBisCO carboxylase|$K_\mathrm{i\|RuBisCO\|NADP}$|$K_\mathrm{i}\ \mathrm{NADP}$|$0.21$|$\mathrm{mM}$|ki_v_RuBisCO_c_NADP_st|Zhu et al. 2007|
|Inhibition constant for ADP in RuBisCO carboxylase|$K_\mathrm{i\|RuBisCO\|ADP}$|$K_\mathrm{i}\ \mathrm{ADP}$|$0.2$|$\mathrm{mM}$|ki_v_RuBisCO_c_ADP_st|Zhu et al. 2007|
|Inhibition constant for Pi in RuBisCO carboxylase|$K_\mathrm{i\|RuBisCO\|ADP}$|$K_\mathrm{i}\ \mathrm{P_i}$|$3.6$|$\mathrm{mM}$|ki_v_RuBisCO_c_Pi_st|Zhu et al. 2007|
|Maximum rate of RuBisCO carboxylation|$V_\mathrm{max\|RuBisCO}$|$V_\mathrm{cmax}$|$0.2$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_RuBisCO_c||
|Turnover per S1L1|$k_\mathrm{cat\|RuBisCO}$|Cat n°|$4.7$|$\mathrm{s^{-1}}$|kcat_v_RuBisCO_c|Zhu et al. 2007|
|Specificity in the gas phase|$S_\mathrm{C\|O}$|$S_\mathrm{C/O}$|$2200$||S_co_gas|Bellasio et al. 2016|
|Maximum rate of PRKase|$V_\mathrm{max\|PRKase}$|$V_\mathrm{max}\ \mathrm{RuP_{Phosp}}$|$1.17$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_PRKase|Zhu et al. 2007|
|Equilibirum constant in PRKase|$K_\mathrm{eq\|PRKase}$|$K_\mathrm{e}\ \mathrm{RuP_{Phosp}}$|$6846$|$\mathrm{mM}$|keq_v_PRKase|Zhu et al. 2007|
|Michealis-Menten constant for ATP in PRKase|$K_\mathrm{m\|PRKase\|ATP}$|$K_\mathrm{m}\ \mathrm{ATP}$|$0.625$|$\mathrm{mM}$|km_v_PRKase_ATP_st|Zhu et al. 2007|
|Inhibition constant for ADP in PRKase|$K_\mathrm{i\|PRKase\|ADP}$|$K_\mathrm{i}\ \mathrm{ADP}$|$0.1$|$\mathrm{mM}$|ki_v_PRKase_ADP_st|Zhu et al. 2007|
|Michealis-Menten constant for RU5P in PRKase|$K_\mathrm{m\|PRKase\|RU5P}$|$K_\mathrm{m}\ \mathrm{RuP}$|$0.034$|$\mathrm{mM}$|km_v_PRKase_RU5P|Gardemann et al. 1983|
|Inhibition constant for PGA in PRKase|$K_\mathrm{i\|PRKase\|PGA}$|$K_\mathrm{i}\ \mathrm{PGA}$|$2$|$\mathrm{mM}$|ki_v_PRKase_PGA|Zhu et al. 2007|
|Inhibition constant for RUBP in PRKase|$K_\mathrm{i\|PRKase\|RUBP}$|$K_\mathrm{i}\ \mathrm{RuBP}$|$0.7$|$\mathrm{mM}$|ki_v_PRKase_RUBP|Zhu et al. 2007|
|Inhibition constant for Pi in PRKase|$K_\mathrm{i\|PRKase\|Pi}$|$K_\mathrm{i}\ \mathrm{P_i}$|$4$|$\mathrm{mM}$|ki_v_PRKase_Pi_st|Zhu et al. 2007|
|Maximum rate of PGA reduction|$V_\mathrm{max\|PGAreduc}$|$V_\mathrm{max}\ \mathrm{PR}$|$0.4$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_pgareduction||
|Michealis-Menten constant for ATP in PGA reduction|$K_\mathrm{m\|PGAreduc\|ATP}$|$K_\mathrm{m}\ \mathrm{ATP}$|$0.3$|$\mathrm{mM}$|km_v_pgareduction_ATP_st|Zhu et al. 2007|
|Michealis-Menten constant for PGA in PGA reduction|$K_\mathrm{m\|PGAreduc\|PGA}$|$K_\mathrm{m}\ \mathrm{PGA}$|$10$|$\mathrm{mM}$|km_v_pgareduction_PGA||
|Michealis-Menten constant for NADPH in PGA reduction|$K_\mathrm{m\|PGAreduc\|NADPH}$|$K_\mathrm{m}\ \mathrm{NADPH}$|$0.05$|$\mathrm{mM}$|km_v_pgareduction_NADPH_st|Zhu et al. 2007|
|Inhibition constant for ADP in PGA reduction|$K_\mathrm{i\|PGAreduc\|ADP}$|$K_\mathrm{i}\ \mathrm{ADP}$|$0.89$|$\mathrm{mM}$|ki_v_pgareduction_ADP_st||
|Maximum rate of Carbohydrate Synthesis|$V_\mathrm{max\|carbsyn}$|$V_\mathrm{max}\ \mathrm{CA}$|$0.2235$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_carbohydrate_synthesis|Zhu et al. 2007|
|Equilibirum constant in Carbohydrate Synthesis|$K_\mathrm{eq\|carbsyn}$|$K_\mathrm{e}\ \mathrm{CA}$|$0.8$||keq_v_carbohydrate_synthesis|Zhu et al. 2007|
|Michealis-Menten constant for DHAP in Carbohydrate Synthesis|$K_\mathrm{m\|carbsyn\|DHAP}$|$K_\mathrm{m}\ \mathrm{DHAP}$|$22$|$\mathrm{mM}$|km_v_carbohydrate_synthesis_DHAP|Zhu et al. 2007|
|Inhibition constant for ADP in Carbohydrate Synthesis|$K_\mathrm{i\|carbsyn\|ADP}$|$K_\mathrm{i}\ \mathrm{ADP}$|$1$|$\mathrm{mM}$|ki_v_carbohydrate_synthesis_ADP_st|Zhu et al. 2007|
|Maximum rate of reductive pentose phosphate pathway|$V_\mathrm{max\|rpp}$|$V_\mathrm{max}\ \mathrm{RPP}$|$0.0585$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_rpp|Zhu et al. 2007|
|Equilibirum constant in reductive pentose phosphate pathway|$K_\mathrm{eq\|rpp}$|$K_\mathrm{e}\ \mathrm{RPP}$|$0.06$||keq_v_rpp||
|Michealis-Menten constant for DHAP in reductive pentose phosphate pathway|$K_\mathrm{m\|rpp\|DHAP}$|$K_\mathrm{m}\ \mathrm{DHAP}$|$0.5$|$\mathrm{mM}$|km_v_rpp_DHAP||
|Concentration of Protons|$H^+$|$[H^+]$|$5.012e-05$|$\mathrm{mM}$|H||
|Maximum rate of carbonic anhydrase|$V_\mathrm{max\|CAase}$|$V_\mathrm{max}\ \mathrm{CA}$|$200$|$\mathrm{mmol\ m^{-2}\ s^{-1}}$|vmax_v_co2_hydration|Zhu et al. 2007|
|Equilibirum constant in carbonic anhydrase|$K_\mathrm{eq\|CAase}$|$K_\mathrm{e}\ \mathrm{CA}$|$0.00056$||keq_v_co2_hydration|Zhu et al. 2007|
|Michealis-Menten constant for $\mathrm{CO_2}$ in carbonic anhydrase|$K_\mathrm{m\|CAase\|CO_2}$|$K_\mathrm{m}\ \mathrm{CO_2}$|$2.8$|$\mathrm{mM}$|km_v_co2_hydration_CO2|Zhu et al. 2007|
|Michealis-Menten constant for $\mathrm{HCO_3}$ in carbonic anhydrase|$K_\mathrm{m\|CAase\|HCO_3}$|$K_\mathrm{m}\ \mathrm{HCO_3}$|$34$|$\mathrm{mM}$|km_v_co2_hydration_HCO3|Zhu et al. 2007|
|Equilibirum constant in FNRase|$K_\mathrm{eq\|FNRase}$|$K_\mathrm{e}\ \mathrm{NADPH}$|$502$||keq_v_FNR|Santamarina et al. 2002|
|Michealis-Menten constant for NADP in FNRase|$K_\mathrm{m\|FNRase\|NADP}$|$K_\mathrm{m}\ \mathrm{NADP}$|$0.0072$|$\mathrm{mM}$|km_v_FNR_NADP_st|Santamarina et al. 2002|
|Michealis-Menten constant for NADPH in FNRase|$K_\mathrm{m\|FNRase\|NADPH}$|$K_\mathrm{m}\ \mathrm{NADPH}$|$0.036$|$\mathrm{mM}$|km_v_FNR_NADPH_st|Santamarina et al. 2002|
|Time constant for induction of FNRase|$K_\mathrm{J\|FNRase\|NADPH}$|$K_\mathrm{J}\ \mathrm{NADPH}$|$200$|$\mathrm{s}$|Kj_NADPH|Bellasio et al. 2017|
|Equilibirum constant in ATPsynthase|$K_\mathrm{eq\|ATPsynthase}$|$K_\mathrm{e}$|$5734$||keq_v_ATPsynth|Santamarina et al. 2002|
|Michealis-Menten constant for ADP in ATPsynthase|$K_\mathrm{m\|ATPsynthase\|ADP}$|$K_\mathrm{m}\ \mathrm{ADP}$|$0.014$|$\mathrm{mM}$|km_v_ATPsynth_ADP_st|Santamarina et al. 2002|
|Michealis-Menten constant for Pi in ATPsynthase|$K_\mathrm{m\|ATPsynthase\|Pi}$|$K_\mathrm{m}\ \mathrm{P_i}$|$0.3$|$\mathrm{mM}$|km_v_ATPsynth_Pi_st|Santamarina et al. 2002|
|Michealis-Menten constant for ATP in ATPsynthase|$K_\mathrm{m\|ATPsynthase\|ATP}$|$K_\mathrm{m}\ \mathrm{ATP}$|$0.3$|$\mathrm{mM}$|km_v_ATPsynth_ATP_st|Santamarina et al. 2002|
|Time constant for induction of ATPsynthase|$K_\mathrm{J\|ATPsynthase\|ATP}$|$K_\mathrm{J}\ \mathrm{ATP}$|$200$|$\mathrm{s}$|Kj_ATP|Bellasio et al. 2017|
|Mesophyll conductance to $\mathrm{CO_2}$|$g_\mathrm{M}$|$g_\mathrm{M}$|$0.5$|$\mathrm{mol\ m^{-2}\ s^{-1}}$|gm|Flexas et al. 2008|
|$\mathrm{CO_2}$ volatility|$K_\mathrm{h\|CO_2}$|$K_\mathrm{h}\ \mathrm{CO_2}$|$30303.0303030303$|$\mathrm{\mu bar mM^{-1}}$|Kh_co2|van der Heijden et al. 2015|
|Time constant for decrease in $g_\mathrm{S}$|$K_{\mathrm{d}\|g_\mathrm{S}}$|$K_\mathrm{d}$|$150$|$\mathrm{s}$|Kd|McAusland et al. 2016|
|Time constant for increase in $g_\mathrm{S}$|$K_{\mathrm{i}\|g_\mathrm{S}}$|$K_\mathrm{i}$|$900$|$\mathrm{s}$|Ki|McAusland et al. 2016|
|Value of $\tau$ in the dark|$\tau_0$|$\tau_0$|$-0.1$|$\mathrm{mM}$|tau0||
|Turgor to conductance factor|$\chi \beta$|$\chi \beta$|$0.5$|$\mathrm{mol air MPa^{-1}}$|chi_beta||
|Soil water potential|$\Phi_\mathrm{soil}$|$\Phi_\mathrm{soil}$|$0$|$\mathrm{MPa}$|phi||
|Epidermal osmotic pressure|$\pi _\mathrm{e}$|$\pi _\mathrm{e}$|$1.2$|$\mathrm{MPa}$|pi_e|Bellasio et al. 2017|
|Root to leaf hydraulic conductance|$K_\mathrm{h}$|$K_\mathrm{h}$|$12$|$\mathrm{mmol\ water\ m^{-2}\ s^{-1}\ Mpa^{-1}}$|Kh|Bellasio et al. 2017|
|Leaf-to-boundary layer $\mathrm{H_2O}$ mole fraction gradient|$D_\mathrm{S}$|$D_\mathrm{S}$|$10$||Ds||
|Basal stomatal conductance|$g_\mathrm{s0}$|$g_\mathrm{s0}$|$0.01$|$\mathrm{mol\ m^{-2}\ s^{-1}}$|gs0|Buckley et al. 2003|
|Total NAD|$\mathrm{NAD_{Tot}}$|$NAD_\mathrm{Tot}$|$0.5$|$\mathrm{mM}$|NADP_tot|Wang et al. 2014|

#### Derived Parameters

|Short Description|Common Abbr.|Paper Abbr.|Python Var|
| :---: | :---: | :---: | :---: |
|Total concentration of RuBisCO catalytic sites|$E_\mathrm{RuBisCO\|Total}$|$E_\mathrm{T}$|Et|
|Light absorbed by PSII when $f_\mathrm{Cyc} = 0$|$I_\mathrm{2\|0}$|$I_\mathrm{2,0}$|I2_0|
|Light absorbed by PSI when $f_\mathrm{Cyc} = 0$|$I_\mathrm{1\|0}$|$I_\mathrm{1,0}$|I1_0|
|Michealis-Menten constant for RuBP in RuBisCO carboxylation|$K_{\mathrm{m\|RuBisCO\|RuBP}}^\prime$|$K_{\mathrm{m\ RuBP}}^\prime$|km_v_RuBisCO_c_RUBP_extra|
|Function that relatives RuBP concentration to concentration of RuBisCO active sites|$f\left(\mathrm{RUBP}\right)$|$f\left(\mathrm{RuBP}\right)$|f_rubp|
|Steady state value of the RuBisCO activation state ($R_\mathrm{act}$)|$R_\mathrm{act\|steady}$|$R_\mathrm{act\ eq}$|Ract_eq|
|Quantity that reduces PSI when the cyclic electron flow is engaged|$\chi$|$\chi$|chi|
|Light absorbed by PSI|$I_1$|$I_1$|I1|
|Proportion of electron flow at PSI which follows CEF|$f_\mathrm{Cyc}$|$f_\mathrm{Cyc}$|f_cyc|
|Light absorbed by PSII|$I_2$|$I_2$|I2|
|Electron flow through PSII|$J_2$|$J_2$|J2|
|Electron flow through PSI|$J_1$|$J_1$|J1|
|Fraction of $J_1$ used by alternative electron sinks|$f_\mathrm{Pseudocyc}$|$f_\mathrm{Pseudocyc}$|f_pseudocyc|
|Steady state value of the total NADPH production|$J_\mathrm{NADPH\|steady}$|$J_\mathrm{NADPH}$|J_NADPH_steady|
|Steady state value of the total ATP production|$J_\mathrm{ATP\|steady}$|$J_\mathrm{ATP}$|J_ATP_steady|
|Steady state value of the stomatal conductance of water vapour to the atmosphere|$g_\mathrm{S\|steady}$|$g_\mathrm{S}$|gs_steady|




<details>
<summary>Equations of derived parameters</summary>

```math
E_\mathrm{RuBisCO \vert Total} =  \frac{\frac{V_\mathrm{max \vert RuBisCO}}{k_\mathrm{cat \vert RuBisCO}}}{V_\mathrm{M}}
```
```math
I_\mathrm{2 \vert 0} =  \mathrm{PPFD} \cdot s_\mathrm{ener}
```
```math
I_\mathrm{1 \vert 0} =  \frac{I_\mathrm{2 \vert 0} \cdot \Phi (\mathrm{II})_0}{\Phi (\mathrm{I})_0}
```
```math
K_{\mathrm{m \vert RuBisCO \vert RuBP}}^\prime =  K_\mathrm{m \vert RuBisCO \vert RUBP} \cdot \left( 1 + \frac{\mathrm{PGA}}{K_\mathrm{i \vert RuBisCO \vert PGA}} + \frac{\mathrm{NADP}_\mathrm{st}}{K_\mathrm{i \vert RuBisCO \vert NADP}} + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} + \frac{\mathrm{P}_\mathrm{i,\ st}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right)
```
```math
f\left(\mathrm{RUBP}\right) =  \frac{E_\mathrm{RuBisCO \vert Total} + K_{\mathrm{m \vert RuBisCO \vert RuBP}}^\prime + \mathrm{RUBP} - \sqrt{ \left( E_\mathrm{RuBisCO \vert Total} + K_{\mathrm{m \vert RuBisCO \vert RuBP}}^\prime + \mathrm{RUBP} \right)^{2} - 4 \mathrm{RUBP} \cdot E_\mathrm{RuBisCO \vert Total} }}{2 E_\mathrm{RuBisCO \vert Total}}
```
```math
R_\mathrm{act \vert steady} =  \mathrm{non\_rect\_hyperbole} \left( \mathrm{PPFD}, \alpha_\mathrm{PPFD \vert RuBisCO}, V_\mathrm{0 \vert PPFD \vert RuBisCO}, \theta_\mathrm{PPFD \vert RuBisCO} \right) \cdot \mathrm{non\_rect\_hyperbole} \left( \left[\mathrm{CO_2}\right], \alpha_\mathrm{CO_2 \vert RuBisCO}, V_\mathrm{0 \vert CO_2 \vert RuBisCO}, \theta_\mathrm{CO_2 \vert RuBisCO} \right)
```
```math
\chi =  \frac{f_\mathrm{Cyc}}{1 + f_\mathrm{Cyc} + \Phi (\mathrm{II})_0}
```
```math
I_1 =  \left( 1 + \chi \right) I_\mathrm{1 \vert 0}
```
```math
f_\mathrm{Cyc} =  \mathrm{max} \left( 0, -1 + 15^{\frac{v_{\mathrm{ATPsynthase}}}{J_\mathrm{ATP}} - \frac{v_{\mathrm{FNR}}}{J_\mathrm{NADPH}}} \right)
```
```math
I_2 =  \left( \frac{1}{\Phi (\mathrm{II})_0} - \chi \right) I_\mathrm{2 \vert 0} \cdot \Phi (\mathrm{II})_0
```
```math
J_2 =  I_2 \cdot \Phi \mathrm{PSII}
```
```math
J_1 =  \frac{J_2}{1} - f_\mathrm{Cyc}
```
```math
f_\mathrm{Pseudocyc} =  f_\mathrm{PseudocycNR} + 4 \mathrm{O_2} \cdot \left( 1 - \frac{v_{\mathrm{FNR}}}{J_\mathrm{NADPH}} \right)
```
```math
J_\mathrm{NADPH \vert steady} =  \frac{\frac{J_1 \cdot \left( 1 - f_\mathrm{Cyc} - f_\mathrm{Pseudocyc} \right)}{2}}{1000}
```
```math
J_\mathrm{ATP \vert steady} =  \frac{\frac{J_2 + \left( 1 - f_\mathrm{Q} \right) J_1 + 2 f_\mathrm{Q} \cdot J_1 + 2 f_\mathrm{Cyc} \cdot f_\mathrm{NDH} \cdot J_1}{h}}{1000}
```
```math
g_\mathrm{S \vert steady} =  \mathrm{max} \left( g_\mathrm{s0}, \frac{\chi \beta \cdot \left( \tau_0 + f\left(\mathrm{RUBP}\right) \right) \left( \Phi_\mathrm{soil} + \pi _\mathrm{e} \right)}{1 + \chi \beta \cdot \left( \tau_0 + f\left(\mathrm{RUBP}\right) \right) \frac{1}{K_\mathrm{h}} \cdot D_\mathrm{S}} \right)
```

</details>

                     
### Reaction Rates

|Short Description|Common Abbr.|Paper Abbr.|KEGG ID|Python Var|
| :---: | :---: | :---: | :---: | :---: |
|Rate of RuBisCO activation|$v_{R_\mathrm{act}}$|$R_{\mathrm{act}\ t+\mathrm{d}t}$||Ract_rate|
|Rate of the total ATP production|$v_{J_\mathrm{NADPH}}$|$J_{\mathrm{NADPH}\ t+\mathrm{d}t}$||v_J_NADPH|
|Rate of total ATP production|$v_{J_\mathrm{ATP}}$|$J_{\mathrm{ATP}\ t+\mathrm{d}t}$||v_J_ATP|
|Rate of the stomatal conductance of water vapour to the atmosphere|$v_{g_\mathrm{S}}$|$g_{\mathrm{S}\ t+\mathrm{d}t}$||v_gs|
|Rate of RuBisCo Carboxylase|$v_{\mathrm{RuBisCO\|Carboxylase}}$|$V_C$|R00024|v_RuBisCO_c|
|Rate of RuBisCO Oxygenase|$v_{\mathrm{RuBisCO\|Oxy}}$|$V_O$|R03140|rubisco_oxygenase|
|Rate of glycine decarboxylase|$v_{\mathrm{GDC}}$|$\mathrm{GDC}$|R03425|glycine_decarboxylase|
|Rate of PRKase|$v_{\mathrm{PRKase}}$|$\mathrm{RuP_{Phosp}}$|R01523|v_PRKase|
|Combined rate of PGK1ase (R01523) and GAPDHase (R01603|$v_{\mathrm{PGAreduc}}$|$\mathrm{PR}$||v_pgareduction|
|Simplified rate of Carbohydrate Synthesis|$v_{\mathrm{carbsyn}}$|$\mathrm{CS}$||v_carbohydrate_synthesis|
|Simplified reductive pentose phosphate pathway|$v_{\mathrm{rpp}}$|$\mathrm{RPP}$||v_rpp|
|Rate of carbonic anhydrase|$v_{\mathrm{CAase}}$|$\mathrm{CA}$||v_co2_hydration|
|Respiration in the light|$R_\mathrm{light}$|$R_\mathrm{LIGHT}$||v_RLight|
|Reaction mediated by FNR|$v_{\mathrm{FNR}}$|$v_\mathrm{NADPH}$|R01195|v_FNR|
|Production of ATP by ATPsynthase|$v_{\mathrm{ATPsynthase}}$|$v_\mathrm{ATP}$|R00086|v_ATPsynth|
|Rate of $\mathrm{CO_2}$ dissolution in aqueous media within the leaf|$v_{\mathrm{CO_{2\|diss}}}$|$\mathrm{CO_2 dissolution}$||CO2_dissolution|
|Rate of $\mathrm{CO_2}$ stomatal diffusion|$v_{\mathrm{CO_{2\|stomdiff}}}$|$\mathrm{CO_2 stomatal diffusion}$||CO2_stomatal_diffusion|




<details>
<summary>Rate equations</summary>

```math
v_{R_\mathrm{act}} = \left\{ \begin{array}{cl} \frac{R_\mathrm{act \vert steady} - R_{\mathrm{act}}}{\tau_{\mathrm{d} \vert R_\mathrm{act}}} & : \ R_{\mathrm{act}} \geq R_\mathrm{act \vert steady} \\ \frac{R_\mathrm{act \vert steady} - R_{\mathrm{act}}}{\tau_{\mathrm{i} \vert R_\mathrm{act}}} & : \ R_{\mathrm{act}} < R_\mathrm{act \vert steady} \end{array} \right.
```
```math
v_{J_\mathrm{NADPH}} = \left\{ \begin{array}{cl} \frac{J_\mathrm{NADPH \vert steady} - J_\mathrm{NADPH}}{0.1 \cdot K_\mathrm{J \vert FNRase \vert NADPH}} & : \ J_\mathrm{NADPH} \geq J_\mathrm{NADPH \vert steady} \\ \frac{J_\mathrm{NADPH \vert steady} - J_\mathrm{NADPH}}{K_\mathrm{J \vert FNRase \vert NADPH}} & : \ J_\mathrm{NADPH} < J_\mathrm{NADPH \vert steady} \end{array} \right.
```
```math
v_{J_\mathrm{NADPH}} = \left\{ \begin{array}{cl} \frac{J_\mathrm{ATP \vert steady} - J_\mathrm{ATP}}{0.1 \cdot K_\mathrm{J \vert ATPsynthase \vert ATP}} & : \ J_\mathrm{ATP} \geq J_\mathrm{ATP \vert steady} \\ \frac{J_\mathrm{ATP \vert steady} - J_\mathrm{ATP}}{K_\mathrm{J \vert ATPsynthase \vert ATP}} & : \ J_\mathrm{ATP} < J_\mathrm{NADPH \vert steady} \end{array} \right.
```
```math
v_{g_\mathrm{S}} = \left\{ \begin{array}{cl} \frac{g_\mathrm{S \vert steady} - g_\mathrm{S}}{K_{\mathrm{d} \vert g_\mathrm{S}}} & : \ g_\mathrm{S} \geq g_\mathrm{S \vert steady} \\ \frac{g_\mathrm{S \vert steady} - g_\mathrm{S}}{K_{\mathrm{i} \vert g_\mathrm{S}}} & : \ g_\mathrm{S} < g_\mathrm{S \vert steady} \end{array} \right.
```
```math
v_{\mathrm{RuBisCO \vert Carboxylase}} =  \frac{V_\mathrm{max \vert RuBisCO} \cdot R_{\mathrm{act}} \cdot f\left(\mathrm{RUBP}\right) \cdot \mathrm{RUBP} \cdot \left[\mathrm{CO_2}\right]}{\left( K_\mathrm{m \vert RuBisCO \vert CO_2} \cdot \left( 1 + \frac{\mathrm{O_2}}{K_\mathrm{m \vert RuBisCO \vert O_2}} \right) + \left[\mathrm{CO_2}\right] \right) \left( K_{\mathrm{m \vert RuBisCO \vert RuBP}}^\prime + \mathrm{RUBP} \right)}
```
```math
v_{\mathrm{RuBisCO \vert Oxy}} =  \frac{v_{\mathrm{RuBisCO \vert Carboxylase}} \cdot 2 \frac{1}{2 \frac{S_\mathrm{C \vert O}}{K_\mathrm{h \vert O_2}} \cdot K_\mathrm{h \vert CO_2}} \cdot \mathrm{O_2}}{\left[\mathrm{CO_2}\right]}
```
```math
v_{\mathrm{GDC}} =  v_{\mathrm{RuBisCO \vert Oxy}}
```
```math
v_{\mathrm{PRKase}} =  \frac{V_\mathrm{max \vert PRKase} \cdot \left( \mathrm{ATP_{st}} \cdot \mathrm{RU5P} - \frac{\mathrm{ADP_{st}} \cdot \mathrm{RUBP}}{K_\mathrm{eq \vert PRKase}} \right)}{\left( \mathrm{ATP_{st}} + K_\mathrm{m \vert PRKase \vert ATP} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right) \right) \left( \mathrm{RU5P} + K_\mathrm{m \vert PRKase \vert RU5P} \cdot \left( 1 + \frac{\mathrm{PGA}}{K_\mathrm{i \vert RuBisCO \vert PGA}} + \frac{\mathrm{RUBP}}{K_\mathrm{i \vert PRKase \vert RUBP}} + \frac{\mathrm{P}_\mathrm{i,\ st}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right) \right)}
```
```math
v_{\mathrm{PGAreduc}} =  \frac{V_\mathrm{max \vert PGAreduc} \cdot \mathrm{ATP_{st}} \cdot \mathrm{PGA} \cdot \mathrm{NADPH}_\mathrm{st}}{\left( \mathrm{PGA} + K_\mathrm{m \vert PGAreduc \vert PGA} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right) \right) \left( \mathrm{ATP_{st}} + K_\mathrm{m \vert PRKase \vert ATP} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right) \right) \left( \mathrm{NADPH}_\mathrm{st} + K_\mathrm{m \vert PGAreduc \vert NADPH} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right) \right)}
```
```math
v_{\mathrm{carbsyn}} =  \frac{V_\mathrm{max \vert carbsyn} \cdot \left( \mathrm{DHAP} - 0.4 \right) \left( 1 - \frac{\left| v_{\mathrm{PGAreduc}} \right| \cdot \mathrm{P}_\mathrm{i,\ st}}{K_\mathrm{eq \vert carbsyn}} \right)}{\mathrm{DHAP} + K_\mathrm{m \vert carbsyn \vert DHAP} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{i \vert RuBisCO \vert ADP}} \right)}
```
```math
v_{\mathrm{rpp}} =  \frac{V_\mathrm{max \vert rpp} \cdot \left( \mathrm{DHAP} - \frac{\mathrm{RU5P}}{K_\mathrm{eq \vert rpp}} \right)}{\mathrm{DHAP} + K_\mathrm{m \vert carbsyn \vert DHAP}}
```
```math
v_{\mathrm{CAase}} =  \frac{V_\mathrm{max \vert carbsyn} \cdot \left( \left[\mathrm{CO_2}\right] - \frac{\left[\mathrm{HCO_3^-}\right] \cdot H^+}{K_\mathrm{eq \vert carbsyn}} \right)}{K_\mathrm{m \vert CAase \vert CO_2} \cdot \left( 1 + \frac{\left[\mathrm{CO_2}\right]}{K_\mathrm{m \vert CAase \vert CO_2}} + \frac{\left[\mathrm{HCO_3^-}\right]}{K_\mathrm{m \vert CAase \vert HCO_3}} \right)}
```
```math
R_\mathrm{light} =  R_\mathrm{light}
```
```math
v_{\mathrm{FNR}} =  \frac{J_\mathrm{NADPH} \cdot \left( \mathrm{NADP}_\mathrm{st} - \frac{\mathrm{NADPH}_\mathrm{st}}{K_\mathrm{eq \vert FNRase}} \right)}{K_\mathrm{m \vert FNRase \vert NADP} \cdot \left( 1 + \frac{\mathrm{NADP}_\mathrm{st}}{K_\mathrm{m \vert FNRase \vert NADP}} + \frac{\mathrm{NADPH}_\mathrm{st}}{K_\mathrm{m \vert PGAreduc \vert NADPH}} \right)}
```
```math
v_{\mathrm{ATPsynthase}} =  \frac{J_\mathrm{ATP} \cdot \left( \mathrm{ADP_{st}} \cdot \mathrm{P}_\mathrm{i,\ st} - \frac{\mathrm{ATP_{st}}}{K_\mathrm{eq \vert ATPsynthase}} \right)}{K_\mathrm{m \vert ATPsynthase \vert ADP} \cdot K_\mathrm{m \vert ATPsynthase \vert Pi} \cdot \left( 1 + \frac{\mathrm{ADP_{st}}}{K_\mathrm{m \vert ATPsynthase \vert ADP}} + \frac{\mathrm{ATP_{st}}}{K_\mathrm{m \vert PRKase \vert ATP}} + \frac{\mathrm{P}_\mathrm{i,\ st}}{K_\mathrm{m \vert ATPsynthase \vert Pi}} + \frac{\mathrm{ADP_{st}} \cdot \mathrm{P}_\mathrm{i,\ st}}{K_\mathrm{m \vert ATPsynthase \vert ADP} \cdot K_\mathrm{m \vert ATPsynthase \vert Pi}} \right)}
```
```math
v_{\mathrm{CO_{2 \vert diss}}} =  \frac{g_\mathrm{M} \cdot \left( C_\mathrm{i} - \left[\mathrm{CO_2}\right] \cdot K_\mathrm{h \vert CO_2} \right)}{1000}
```
```math
v_{\mathrm{CO_{2 \vert stomdiff}}} =  \frac{g_\mathrm{S} \cdot \left( C_\mathrm{a} - C_\mathrm{i} \right)}{1000}
```

</details>

                     
### Figures



                     
<details>
<summary>Figure 3</summary>
                     
<img style='float: center' src='figures/bellasio2019_fig3.svg' alt='Figure 3' width='600'/>

Simulated $A$-$\mathrm{PPFD}$ (left) and  $A$-$C_\mathrm{a}$ (right) response curves under two different oxygen partial pressures ($\mathrm{O_2}$ = 210000, orange, and = 20000, blue). The simulation was run to a quasi steady-state (1800 s) at each value of $C_\mathrm{a}$ or $\mathrm{PPFD}$. The $C_\mathrm{a}$ response curve was simulated at a $\mathrm{PPFD}$ of 1500 µmol m⁻² s⁻¹, while the $\mathrm{PPFD}$ response curve was simulated at a $C_\mathrm{a}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top row shows the assimilation rate $A$, the middle row the stomatal conductance ($g_\mathrm{S}$), and the bottom row the $\mathrm{NADPH}_\mathrm{st}$ production rate $v_{\mathrm{FNR}}$.

The recreation of this figure was done effortlessly with only a few issues. The original figure does not specify how long the simulations were run; therefore, it was assumed to follow the length of simulation detailed in Figure 4. Additionally, the original figure shows an $A$-$C_\mathrm{i}$ response curve on the right; it could be inferred that they either meant $A$-$C_\mathrm{a}$ or assumed $C_\mathrm{i}$ to be equal to $C_\mathrm{a}$. In this recreation, $A$-$C_\mathrm{a}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>



                     
<details>
<summary>Figure 4</summary>
                     
<img style='float: center' src='figures/bellasio2019_fig4.svg' alt='Figure 4' width='600'/>

Simulated $A$-$\mathrm{PPFD}$ (left) and  $A$-$C_\mathrm{a}$ (right) response curves under two different oxygen partial pressures ($p(\mathrm{O_2}) = 210000 \mathrm{\mu bar}$, orange, and $p(\mathrm{O_2}) = 20000 \mathrm{\mu bar}$, blue). The simulation was run to a quasi steady-state (1800 s) at each value of $C_\mathrm{a}$ or $\mathrm{PPFD}$. The $C_\mathrm{a}$ response curve was simulated at a $\mathrm{PPFD}$ of 1500 µmol m⁻² s⁻¹, while the $\mathrm{PPFD}$ response curve was simulated at a $C_\mathrm{a}$ of 400 µmol mol⁻¹. Other parameters and initial conditions were not changed from the default values used in the model. The top and middle row show the concentrations of $\mathrm{RUBP}$ and $\mathrm{PGA}$, respectively. These concentrations were given in µmol m⁻² by multiplying their volumetric concentrations by the chloroplast volume per leaf area (V_\mathrm{M}). The bottom row shows the relative RuBisCO activity by multiplying $R_{\mathrm{act}}$ and $f\left(\mathrm{RUBP}\right)$.


The recreation of this figure was done effortlessly with only a few issues. The original figure shows an $A$-$C_\mathrm{i}$ response curve on the right; it could be inferred that they either meant $A$-$C_\mathrm{a}$ or assumed $C_\mathrm{i}$ to be equal to $C_\mathrm{a}$. In this recreation, $A$-$C_\mathrm{a}$ was chosen. This causes issues with the x-axis values in the right plots; however, since the lines still follow the same trend, the recreation remains valid.
</details>



                     
<details>
<summary>Figure 5</summary>
                     
<img style='float: center' src='figures/bellasio2019_fig5.svg' alt='Figure 5' width='600'/>

Response curves to a transition from low to high light (left) and from high to low light (right). The low light intensity was 50 µmol m⁻² s⁻¹, while the high light intensity was 1500 µmol m⁻² s⁻¹. Acclimation was simulated for 400s at the respective light intensities before switching to the other light intensity. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: $C_\mathrm{a} = 350 \mathrm{\mu mol\ mol^{-1}}$, $V_\mathrm{max \vert RuBisCO} = 0.18 \mathrm{mmol\ m^{-2}\ s^{-1}}$, $\chi \beta = 0.8 \mathrm{mol\ air\ MPa^{-1}}$, $\tau_0 = -0.12$, $K_{\mathrm{i} \vert g_\mathrm{S}} = 3600 \mathrm{s}$, and $K_{\mathrm{d} \vert g_\mathrm{S}} = 1200 \mathrm{s}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate $A$ and the rate of \mathrm{ATP_{st}} and \mathrm{NADPH}_\mathrm{st} synthesis ($v_{\mathrm{ATPsynthase}}$ and $v_{\mathrm{FNR}}$ respectively). The middle shows row the stomatal conductance ($g_\mathrm{S}$), the RuBisCO activation state ($R_{\mathrm{act}}), and $f\left(\mathrm{RUBP}\right)$. Lastly, the bottom row shows the ratio of $\mathrm{ATP_{st}}$ and $\mathrm{NADPH}_\mathrm{st}$ to their respective totals.

The recreation of this figure was only partly achieved. Both upper rows show trends very similar to the original figure; however, the right plots show a gradual but stark decrease in the recreation, whereas in the original figure, it is a sudden drop immediately after the light switch. The other four plots show distinct differences in values and trends, especially in the concentrations of $\mathrm{P}_\mathrm{i,\ st}$ and $\mathrm{PGA}$, as well as in the ratio of $\mathrm{NADPH}_\mathrm{st}$. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results. Even though the recreation is not perfect, it still captures the same information as the original figure; this recreation is still valid.

</details>



                     
<details>
<summary>Figure 5</summary>
                     
<img style='float: center' src='figures/bellasio2019_fig5.svg' alt='Figure 5' width='600'/>

Response curves to a transition from low to high light (left) and from high to low light (right). The low light intensity was 50 µmol m⁻² s⁻¹, while the high light intensity was 1500 µmol m⁻² s⁻¹. Acclimation was simulated for $1000 \mathrms_\mathrm{ener}$ at the respective light intensities before switching to the other light intensity. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: $C_\mathrm{a} = 350 \mathrm{\mu mol\ mol^{-1}}$, $V_\mathrm{max \vert RuBisCO} = 0.18 \mathrm{mmol\ m^{-2}\ s^{-1}}$, $\chi \beta = 0.8 \mathrm{mol\ air\ MPa^{-1}}$, $\tau_0 = -0.12$, $K_{\mathrm{i} \vert g_\mathrm{S}} = 3600 \mathrm{s}$, and $K_{\mathrm{d} \vert g_\mathrm{S}} = 1200 \mathrm{s}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate $A$ and the rate of \mathrm{ATP_{st}} and \mathrm{NADPH}_\mathrm{st} synthesis ($v_{\mathrm{ATPsynthase}}$ and $v_{\mathrm{FNR}}$ respectively). The middle shows row the stomatal conductance ($g_\mathrm{S}$), the RuBisCO activation state ($R_{\mathrm{act}}), and $f\left(\mathrm{RUBP}\right)$. Lastly, the bottom row shows the ratio of $\mathrm{ATP_{st}}$ and $\mathrm{NADPH}_\mathrm{st}$ to their respective totals.

The recreation of this figure was only partly achieved. Both upper rows show trends very similar to the original figure; however, the right plots show a gradual but stark decrease in the recreation, whereas in the original figure, it is a sudden drop immediately after the light switch. The other four plots show distinct differences in values and trends, especially in the concentrations of $\mathrm{P}_\mathrm{i,\ st}$ and $\mathrm{PGA}$, as well as in the ratio of $\mathrm{NADPH}_\mathrm{st}$. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results. Furthermore, true steady-state can not be achieved with the recreated version of the model, and so the shortest duration that shows least of change at the end is used. Even though the recreation is not perfect, it still captures the same information as the original figure and therefore is still deemed valid.

</details>



                     
<details>
<summary>Figure 6</summary>
                     
<img style='float: center' src='paper_figures/bellasio2019_fig6.svg' alt='Figure 6' width='600'/>

Response curves to a transition from low to high atmospheric $\mathrm{CO_2}$ concentration $C_\mathrm{a}$ (left) and from high to low atmospheric $C_\mathrm{a}$ (right). The low concentration was 350 µmol mol⁻¹, while the high concentration was 1500 µmol mol⁻¹. Acclimation was simulated for $100000\ \mathrm{s}$ at the respective concentration before switching to the other concentration. This switch is the zero point on the x-axis. The parameters of the model were changed better to reflect the experimental conditions of a measurement cuvette therefore the following parameters were changed: $\mathrm{PPFD} = 1500 \mathrm{\mu mol\ m^{-2}\ s^{-1}}$, $V_\mathrm{max \vert RuBisCO} = 0.18 \mathrm{mmol\ m^{-2}\ s^{-1}}$, $\chi \beta = 0.8 \mathrm{mol\ air\ MPa^{-1}}$, $\tau_0 = -0.12$, $K_{\mathrm{i} \vert g_\mathrm{S}} = 3600 \mathrm{s}$, and $K_{\mathrm{d} \vert g_\mathrm{S}} = 1200 \mathrm{s}$. All other parameters were not changed from the default values used in the model. The top row shows the assimilation rate $A$ and the rate of \mathrm{ATP_{st}} and \mathrm{NADPH}_\mathrm{st} synthesis ($v_{\mathrm{ATPsynthase}}$ and $v_{\mathrm{FNR}}$ respectively). The middle shows row the stomatal conductance ($g_\mathrm{S}$), the RuBisCO activation state ($R_{\mathrm{act}}$), and $f\left(\mathrm{RUBP}\right)$. Lastly, the bottom row shows the ratio of $\mathrm{ATP_{st}}$ and $\mathrm{NADPH}_\mathrm{st}$ to their respective totals.

The recreation of this figure could be achieved. While the acclimation follows the trends and approximate values of the original figure, there are vast differences in the phase after acclimation. In the recreation, the values remain relatively steady after the switch. In contrast, in the original figure, there is a gradual increase or decrease after the switch. The cause of these discrepancies could not be determined; however, it is speculated that some parameter values or initial conditions were not accurately represented in the original caption, or that the use of different numerical solvers could have affected the results.

</details>



                     
<details>
<summary>Figure 7</summary>
                     
<img style='float: center' src='figures/bellasio2019_fig7.svg' alt='Figure 7' width='600'/>

Response to a transition from ambient ($p(\mathrm{O_2}) = 210000 \mathrm{\mu bar}$) to low oxygen partial pressure ($p(\mathrm{O_2}) = 20000 \mathrm{\mu bar}$). The simulation uses the default parameter values, except for $C_\mathrm{a} = 200 \mathrm{\mu mol\ mol^{-1}}$ and $\mathrm{PPFD} = 300 \mathrm{\mu mol\ m^{-2}\ s^{-1}}$. Ambient oxygen was simulated until steady-state was reached. From the zero point on the x-axis only $250\ \mathrm{s_\mathrm{ener}}$ of the atmospheric pressure is shown, then the simulation is run at low pressure for the rest of the plot. The switch point is also indicated by the two different bars at the top of the figure. The two shown lines are the assimilation rate $A$ (green solid) and the efficiency of PSII $\Phi \mathrm{PSII}$ (grey dotted).

</details>

### Demonstrations



                     
<details>
<summary>Day Simulation</summary>
                     
<img style='float: center' src='figures/bellasio2019_demon_daysimulation.svg' alt='Day Simulation' width='600'/>

Sample simulation of a day cycle (06:00 to 20:00) using real Photosynthetically active radiation (PAR) data from Kansas, USA on June 19, 2023. The data was obtained from the National Ecological Observatory Network (NEON) data portal ([https://doi.org/10.48443/vzfh-7675])(https://doi.org/10.48443/vzfh-7675) and is used to create a protocol for the light intensity ($\mathrm{PPFD}$) over the course of the day, in a minute interval. The simulation is run using the default parameters and initial conditions of the model, and the RuBisCO carboxylation rate ($v_{\mathrm{RuBisCO \vert Carboxylase}}$), $\mathrm{ATP_{st}}$ and $\mathrm{NADPH}_\mathrm{st}$ ratio, and Flourescence results is plotted over the course of the day, if possible. The results do not represent actual plant behavior, but show the capabilities of the model to simulate complex and more realistic light protocols.

**Notes:**

As this model does not contain a representation of Flourescence output, this can not be shown. However, both the RuBisCO carboxylation rate and ATP and NADPH ratio follow the trend of the light intensity over the course of the day.

</details>



                     
<details>
<summary>FvCB Submodule</summary>
                     
<img style='float: center' src='figures/bellasio2019_demon_fvcb.svg' alt='FvCB Submodule' width='600'/>

Comparison of modelled carbon assimilation ($A$) and carboxylation rate ($v_\mathrm{c}$) against the Farquhar, von Caemmerer and Berry (FvCB) model. The FvCB model is calculated using the min-W approach as described by Lochoki and McGrath (2025) [[1]](https://doi.org/10.1101/2025.03.11.642611). To be able to simulate carbon assimilation, there are two mandatory parameters that need to be present in the model: CO2 concentration and $v_\mathrm{c}$. If one of these parameters is missing, the FvCB model will still be shown, but no comparison with the model will be possible. Other parameters that are required to calculate the FvCB model will be added as parameters with default values if they are not present in the model. The simulation is then run until steady-state, or quasi-steady-state if not otherwise possible, for different intercellular CO<sub>2</sub> partial pressure ($\mathrm{C_i}$). The carbon assimilation shown does not represent actual values but rather a theoretical curve to compare the kinetic model to the popular FvCB model.

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
| $\mathrm{CO}_2$         | $\left[\mathrm{CO_2}\right]$           |
| $v_\mathrm{c}$          | $v_{\mathrm{RuBisCO \vert Carboxylase}}$ but unit conversion to $\mathrm{\mu mol\ m^{-2}\ s^{-1}}$  |
| $\mathrm{C_i}$          | $C_\mathrm{i}$ but calculated through $C_\mathrm{a}$          |
| $H_\mathrm{s}^{cp}$   | None              |
| $\Gamma ^*$               | None              |
| $R_\mathrm{light}$      | $R_\mathrm{light}$        |
| $A$                       | $A$ but unit conversion to $\mathrm{\mu mol\ m^{-2}\ s^{-1}}$            |

To be able to create this figure, three things had to be added to the model: $C_\mathrm{i}_\mathrm{new}$ as a parameter to use it as input that calculates $C_\mathrm{a}$, and $A$ and  $v_{\mathrm{RuBisCO \vert Carboxylase}}$ converted in $\mathrm{\mu mol\ m^{-2}\ s^{-1}}$. As the model does not always reach true steady-state, a quasi-steady-state is used where the model is simulated to $1800\ \mathrm{s}$ if not otherwise possible. The recreated figure shows the same trends as the original FvCB model, especially follwing the Rubisco-limited and light-limited regimes. Some discrepancies can be seen in lower $C_\mathrm{i}$ values and in the general shape of the curve; however, the recreation is still valid.

</details>



                     
<details>
<summary>PAM Simulation</summary>
                     
<img style='float: center' src='figures/bellasio2019_demon_pam.svg' alt='PAM Simulation' width='600'/>

Sample simulation of a common PAM protocol to show fluctuations of Flourescence and NPQ using saturating pulses. The simulation protocol is as follows: A dark adaptation period that simulates for 30 minutes at a dark light intensity (40 µmol m⁻² s⁻¹), then the actual protocol starts. The protocol consists of 22 periods with each being 2 minutes of length. That period consists of a specific light intensity of the respective type of period and ends with a saturating pulse with a length of 0.8 s and a light intensity of 3000 µmol m⁻² s⁻¹. First two dark periods with light intensity of 40 µmol m⁻² s⁻¹, followed by ten light periods with light intensity of 1000 µmol m⁻² s⁻¹, then ten dark periods again. The simulation is run using the default parameters and initial conditions of the model.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{m}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{m}$.
- If $F_\mathrm{m}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{F_{\mathrm{m}\vert t=0} - F_{\mathrm{m} \vert t}}{F_{\mathrm{m} \vert t}}$

**Notes:**

As this model does not contain a representation of Flourescence or NPQ output, this can not be shown.

</details>



                     
<details>
<summary>Photosynthesis MCA</summary>
                     
<img style='float: center' src='figures/bellasio2019_demon_mca.svg' alt='Photosynthesis MCA' width='600'/>

A sample metabolic control analysis (MCA) of typical photosynthesis variables and fluxes. A control coefficient analysis is to be performed, therefore each parameter represents a single coefficient of the photosynthesis rate. The rates chosen should represent RuBisCO carboxylation rate ($v_\mathrm{RuBisCO \vert C}$), rate of photosystem II ($v_\mathrm{PSII}$), rate of photosystem I ($v_\mathrm{PSI}$), rate of cytochrome b<sub>6</sub>f ($v_\mathrm{cytb6f}$) and rate of ATP synthesis ($v_\mathrm{ATPsynthase}$). The variables chosen should represent CO<sub>2</sub> concentration ($\mathrm{CO_2}$), Ribulose-1,5-bisphosphate concentration ($\mathrm{RUBP}$), oxidised Plastoquinone ($\mathrm{PQ_{ox}}$), oxidised Plastocyanin ($\mathrm{PC_{ox}}$), adenosine triphosphate concentration ($\mathrm{ATP}$), and nicotinamide adenine dinucleotide phosphate concentration ($\mathrm{NADPH}$). For each parameter to be scanned, the model is simulated to steady-state, with a displacement of $\pm 0.0001$ of each respective parameter. The control coefficients are then calculated for each variable and flux by the following formula: $C_{p}^{x} = \frac{x_\mathrm{upper} - x_\mathrm{lower}}{2 \cdot \mathrm{disp} \cdot p}$, where $C_{p}^{x}$ is the control coefficient of parameter $p$ on variable or flux $x$, and $\mathrm{disp}$ is the displacement value. $x_\mathrm{upper}$ and $x_\mathrm{lower}$ are the steady-state result of $x$ at either $+\mathrm{disp}$ and $-\mathrm{disp}$ respectively.

**Assumptions:**

- Steady-State needs to be achievable for the model to perform the MCA.
- The parameters for each coefficient, rates, and variables chosen need to be representative of the respective process.
- If a parameter, rate, or variable is not present in the model, the respective coefficient will be greyed out in the Heatmap.

**Notes:**

| Coefficient                   | In Model          |
| -----------                   | -----------       |
| $\mathrm{PSII}$             | $\mathrm{PPFD}$ |
| $\mathrm{PSI}$              | None |
| $\mathrm{RuBisCO \vert C}$  | $k_\mathrm{cat \vert RuBisCO}$ |
| $\mathrm{cytb6f}$           | None              |
| $\mathrm{ATPsynthase}$      | None              |

| Flux                          | In Model          |
| -----------                   | -----------       |
| $\mathrm{PSII}$             | None |
| $\mathrm{PSI}$              | None |
| $\mathrm{RuBisCO \vert C}$  | $v_{\mathrm{RuBisCO \vert Carboxylase}}$ |
| $\mathrm{cytb6f}$           | None              |
| $\mathrm{ATPsynthase}$      | $v_{\mathrm{ATPsynthase}}$              |

| Variable                  | In Model      |
| -----------               | -----------   |
| $\mathrm{CO_2}$         | $\left[\mathrm{CO_2}\right]$       |
| $\mathrm{RUBP}$         | $\mathrm{RUBP}$      |
| $\mathrm{PQ_{ox}}$    | None          |
| $\mathrm{PC_{ox}}$    | None          |
| $\mathrm{ATP}$          | $\mathrm{ATP_{st}}$    |
| $\mathrm{NADPH}$        | $\mathrm{NADPH}_\mathrm{st}$  |

</details>



                     
<details>
<summary>PAM Fitting</summary>
                     
<img style='float: center' src='figures/bellasio2019_demon_fitting.svg' alt='PAM Fitting' width='600'/>

Sample fitting to experimental NPQ data. The NPQ data used is taken from experimental work published in ([https://doi.org/10.1111/nph.18534](https://doi.org/10.1111/nph.18534)) and was aquired using Maxi Imaging-PAM (Walz, Germany) using Col-0 Arabidopsis thaliana plants. It is assumed that the experiment follows the default PAM protocol of the machine, as no other experimental protocol has been given. Therefore, the protocol of each simulation follows the data given, where the length of one saturating pulse is set to 720 ms at a light intensity of 5000 µmol m⁻² s⁻¹. The light protocol consists of a dark adaptation period of 30 minutes to acclimate the simulation conditions. Then the actual protocol starts with a longer phase of high actinic light (903 µmol m⁻² s⁻¹) for approximately 10 minutes, followed by a lower actinic light of (90 µmol m⁻² s⁻¹) for 10 minutes, and then 5 minutes of a dark period. During each phase, saturating pulses are given approximately every 60 seconds. As the experimental data also provides exact time points for each pulse, these were taken as reference for the protocol and not the general time intervals. In the experimental work, the dark period consists of actual darkness, whereas in the simulation a low light intensity of 40 µmol m⁻² s⁻¹ is used to avoid numerical issues. The fitting is performed using the `lmfit`package in Python with the leastsquare method. On top of that, a standard scaling towards the experimental data is done, to keep the fitting results in the same order of magnitude. To help fitting converge, weights are applied to the data points, which are defined as the reciprocal of the standard deviation. These settings set are not to be taken as set in stone, as fitting is a highly experimental process and differing settings might be required depending on the model and data used. These settings are a basic starting point for fitting data to a model. The hardest and most impactful decision while fitting is the choice of parameters to fit. There are many ways to find which parmaters may be most impactful to fit, such as sensitivity analysis or metabolic control analysis. However, either way experimenting with different parameter sets is always required to find the best fitting practice, which differs for each model and also data to fit to.

**Assumptions:**

- If no Flourescence and NPQ output is present in the model, it can not be shown in the results.
- If Flourescence is present, $F_\mathrm{m}$ is found by using the protocol used in the simulation to find each saturating pulse. A period between each pulse is taken and the maximum Flourescence value during the pulse is taken as $F_\mathrm{m}$.
- If $F_\mathrm{m}$ is found and NPQ is not present, NPQ is calculated using the formula: $NPQ_t = \frac{F_{\mathrm{m}\vert t=0} - F_{\mathrm{m} \vert t}}{F_{\mathrm{m} \vert t}}$

**Notes:**

As this model does not contain a representation of Flourescence or NPQ output, the model cannot be fitted to the data.

</details>
