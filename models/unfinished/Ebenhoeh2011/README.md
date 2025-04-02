



# Ebenhoeh2011


[here](https://doi.org/10.1016/j.biosystems.2010.10.011)
## Installation

## Summary

### Compounds

#### Part of ODE system

|Name|Paper Abbreviation|Abbreviation Here|Python Variable|
| :---: | :---: | :---: | :---: |
|Open state reaction centers|$\mathrm{A}_1$|$\mathrm{A}_1$|`A1`|
|Seperated charges state reaction centers|$\mathrm{A}_2$|$\mathrm{A}_2$|`A2`|
|Oxidised plastoquinone pool|$\mathrm{P}$|$\mathrm{PQ}_{\mathrm{ox}}$|`PQ_ox`|
|Proton concentration in the lumen|$\mathrm{H}$|$\mathrm{H}_{\mathrm{lu}}$|`H_lu`|
|Light harvesting complexes quencher in active state|$\mathrm{N}$|$\mathrm{N}$|`N`|
|Stromal ATP concentration|$\mathrm{T}$|$\mathrm{ATP}_{\mathrm{st}}$|`ATP_st`|




<details>
<summary>Open me for the ODE system!</summary>

$$    
    \begin{align}
        \frac{\mathrm{d}\mathrm{A}_1}{\mathrm{d}t} &= v_3 - v_1 \\
        \frac{\mathrm{d}\mathrm{A}_2}{\mathrm{d}t} &= v_1 - v_2 \\
        \frac{\mathrm{d}\mathrm{PQ}_{\mathrm{ox}}}{\mathrm{d}t} &= v_3 - v_4 \\
        \frac{\mathrm{d}\mathrm{H}_{\mathrm{lu}}}{\mathrm{d}t} &= b_{\mathrm{H}_{\mathrm{lu}}} \cdot \left( 2 \cdot v_2 + v_4 - \frac{14}{3} \cdot v_5 - v_8 \right) \\
        \frac{\mathrm{d}\mathrm{N}}{\mathrm{d}t} &= v_6 - v_7  \\
        \frac{\mathrm{d}\mathrm{ATP}_{\mathrm{st}}}{\mathrm{d}t} &= v_5 - v_9
    \end{align}
$$

</details>

                     
#### Conserved quantities

|Name|Paper Abbreviation|Abbreviation Here|Python Variable|
| :---: | :---: | :---: | :---: |
|Total amount of reaction centers|$\mathrm{D}$|$\mathrm{D}$|`D`|
|Total plastoquinone pool|$\mathrm{X}$|$\mathrm{PQ}_\mathrm{tot}$|`PQ_tot`|
|Total adenosine phosphate pool|$\mathrm{A}^{\mathrm{tot}}$|$\mathrm{AP}_\mathrm{tot}$|`AP_tot`|




<details>
<summary>Open me for the calculations of the conserved quantities!</summary>

$$    
    \begin{align}
        \mathrm{D} &= \mathrm{A}_1 + \mathrm{A}_2 + \mathrm{A}_3 \\
        \mathrm{PQ}_\mathrm{tot} &= \mathrm{PQ}_{\mathrm{ox}} + \mathrm{PQ}_{\mathrm{red}} \\
        \mathrm{AP}_\mathrm{tot} &= \mathrm{ADP}_{\mathrm{st}} + \mathrm{ATP}_{\mathrm{st}} \\
        1 &= \mathrm{N}^0 + \mathrm{N}
    \end{align}
$$

</details>

                     
#### Derived from conserved quantities

|Name|Paper Abbreviation|Abbreviation Here|Python Variable|
| :---: | :---: | :---: | :---: |
|Reduced state reaction centers|$\mathrm{A}_3$|$\mathrm{A}_3$|`A3`|
|Reduced plastoquinone pool|$\mathrm{Q}$|$\mathrm{PQ}_{\mathrm{red}}$|`PQ_red`|
|Stromal ADP concentration|$\mathrm{S}$|$\mathrm{ADP}_{\mathrm{st}}$|`ADP_st`|
|Light harvesting complexes quencher in inactive state|$\mathrm{N}^0$|$\mathrm{N}^0$|`N0`|

### Parameters

### Reaction Rates

|Short Description|Paper Abbreviation|Abbreviation Here|Python Variable|
| :---: | :---: | :---: | :---: |
|Light harvesting, excitation energy transfer and charge seperation of reaction centers|$v_1$|$v_1$|`v1`|
|Re-reduction of the reaction centers (electron donor) by oxygen evolving complex|$v_2$|$v_2$|`v2`|
|Re-oxidation of reaction centers by electron transfer to plastoquinone|$v_3$|$v_3$|`v3`|
|Re-oxidation of reduced plastoquinone by cytochrome b<sub>6</sub>f|$v_4$|$v_4$|`v4`|
|ATP synthesis rate by proton motive force|$v_5$|$v_5$|`v5`|
|Activation of quencher with pH-dependent rate|$v_6$|$v_6$|`v6`|
|Inactivation of quencher|$v_7$|$v_7$|`v7`|
|Passive leak of protons into stroma|$v_8$|$v_8$|`v8`|
|Combination and simplification of all ATP consuming processes|$v_9$|$v_9$|`v9`|




<details>
<summary>Open me for the rates!</summary>

$$    
    \begin{align}
        v_1 &= \mathrm{N}^0 \cdot k_1 \cdot \mathrm{A}_1 \\
        v_2 &= k_2 \cdot \mathrm{A}_2 \\
        v_3 &= k⁺_3 \cdot \mathrm{A}_3 \cdot \mathrm{PQ}_{\mathrm{ox}} - k⁻_3 \cdot \mathrm{A}_1 \cdot \mathrm{PQ}_{\mathrm{red}} \\
        v_4 &= k_4 \cdot \mathrm{PQ}_{\mathrm{red}} \\
        v_5 &= k_5 \cdot \left(\mathrm{AP}_\mathrm{tot} - \mathrm{ATP}_{\mathrm{st}} \cdot \left(1 + \frac{1}{K_{eq}(\mathrm{H}_{\mathrm{lu}})}\right)\right)  \\ \notag
        \mathrm{with} \ K_{\mathrm{eq}}(\mathrm{H}_{\mathrm{lu}}) &= \sqrt[RT]{e^{\Delta G^0 - \mathrm{ln}\ 10 \cdot \Delta \mathrm{pH} \cdot \frac{14}{3} \cdot RT}}\\
        v_6 &= k6 \cdot \mathrm{N}^0 \cdot \frac{\mathrm{H}_{\mathrm{lu}}^n}{\mathrm{H}_{\mathrm{lu}}^n \cdot K_{Q}^n} \\
        v_7 &= k7 \cdot \mathrm{N} \\
        v_8 &= k8 \cdot \left( \mathrm{H}_{\mathrm{lu}} - \mathrm{H}_{\mathrm{st}} \right) \\
        v_9 &= k9 \cdot \mathrm{ATP}_{\mathrm{st}}
    \end{align}
$$

</details>
                     