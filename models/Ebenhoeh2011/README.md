# Ebenhoeh2011

[here](https://doi.org/10.1016/j.biosystems.2010.10.011)

## Installation

## Summary

$$
\aone
$$

### Compounds

|                         Name                        | Paper Abbreviation |       Abbrivation Here       | Python Variable |
|:---------------------------------------------------:|:------------------:|:----------------------------:|:---------------:|
|             Open state reaction centers             |   $\mathrm{A}_1$   | --                           |       `A1`      |
|       Seperated charges state rection centers       |   $\mathrm{A}_2$   | --                           |       `A2`      |
|             Oxidised plastoquinone pool             |    $\mathrm{P}$    |  $\mathrm{PQ}_{\mathrm{ox}}$ |     `PQ_ox`     |
|          Proton concentration in the lumen          |    $\mathrm{H}$    | $\mathrm{H}_{\mathrm{lu}}$   |      `H_lu`     |
| Light harvesting complexes quencher in active state |    $\mathrm{N}$    | --                           |       `N`       |
|              Stromal ATP concentration              |    $\mathrm{T}$    | $\mathrm{ATP}_{\mathrm{st}}$ |     `ATP_st`    |

### Reaction Rates

|                                    Short Description                                   | Abreviation in Paper | Abreviation here | Python Variable |
|:--------------------------------------------------------------------------------------:|:--------------------:|:----------------:|:---------------:|
| Light harvesting, excitation energy transfer and charge seperation of reaction centers | $v_1$                | --               | `v1`            |
| Re-reduction of the reaction centers (electron donor) by oxygen evolving complex       | $v_2$                | --               | `v2`            |
| Re-oxidation of reaction centers by electron transfer to plastoquinone                 | $v_3$                | --               | `v3`            |
| Re-oxidation of reduced plastoquinone by cytochrome b<sub>6</sub>f                     | $v_4$                | --               | `v4`            |
| ATP synthesis rate by proton motive force                                              | $v_5$                | --               | `v5`            |
| Activation of quencher with pH-dependent rate                                          | $v_6$                | --               | `v6`            |
| Inactivation of quencher                                                               | $v_7$                | --               | `v7`            |
| Passive leak of protons into stroma                                                    | $v_8$                | --               | `v8`            |
| Combination and simplification of all ATP consuming processes                          | $v_9$                | --               | `v9`            |

<details>
<summary>Open me for the rates!</summary>

$$
\newcommand{\atwo}{\mathrm{A}_2}
\newcommand{\pq}{\mathrm{PQ}_{\mathrm{ox}}}\\
\newcommand{\proton}{\mathrm{H}_{\mathrm{lu}}}\\
\newcommand{\quencher}{\mathrm{N}}\\
\newcommand{\ATP}{\mathrm{ATP}_{\mathrm{st}}}\\

\begin{align}
v_1 &= (1 - \quencher) \cdot k_1 \cdot \aone \\
v_2 &= k_2 \cdot \atwo \\
v_3 &= k⁺_3 \cdot (\mathrm{D} - \aone - \atwo) \cdot \pq - k⁻_3 \cdot \aone \cdot (\mathrm{X} - \pq) \\
v_4 &= k_4 \cdot (\mathrm{X} - \pq)\\
v_5 &= k_5 \cdot \left(\mathrm{A}^{\mathrm{tot}} - \ATP \cdot \left(1 + \frac{1}{K_{eq}(\proton)}\right)\right) \mathrm{with} \\
K_{\mathrm{eq}}(\proton) = 
\end{align}
$$

$$
\pq
$$

</details>

### Parameters
