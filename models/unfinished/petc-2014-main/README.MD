# Model of the photosynthetic electron transport chain

## Model
This repository contains the mathematical model described in the paper published by [Ebenhoeh *et al.* 2014](http://dx.doi.org/10.1098/rstb.2013.0223), that has been originally developed in MATLAB. The model comprises a set of seven coupled ordinary differential equations and captures the temporal evolution of major protein complexes and key products of photosynthetic light reaction for model organism alga *Chlamydomonas reinhardtii*. The model has been written using [modelbase](https://github.com/QTB-HHU/modelbase) package.

## Setting up

- `pip install pre-commit`
- `pre-commit install`
- `pip install -r code/requirements.txt`

## Sample analysis
A sample analysis is given in the accompanying notebook. With the notebook you can perform various simulations, including PAM fluorescence experiments.


