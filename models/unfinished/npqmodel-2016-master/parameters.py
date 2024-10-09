#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameter class of the qE model presented in Matuszynska et al. 2016 and the 
doctoral thesis "Mathematicla model of light acclimation mechanisms 
in higher plants and green algae" Matuszynska 2016
"""

pars = {
            
    #Pool sizes 
    'PSIItot': 2.5,         # PSII reaction centres
    'PQtot': 20,            # PQ + PQH2
    'APtot': 50,            # total adenosine phosphate pool (ATP + ADP)
    'PsbStot': 1,           # LHCII normalized 
    'Xtot': 1,              # toal xanthophylls
    'O2ex': 8,              # external oxygen
    'Pi': 0.01,             # internal pool of phosphates
            
    #Rate constants and key parameters
    'kCytb6f': 0.104, 
    'kActATPase': 0.01,
    'kDeactATPase': 0.002,
    'kATPsynthase': 20.,
    'kATPconsumption': 10.,
    'kPQred': 250.,
    'kH': 5e9,
    'kF': 6.25e8,
    'kP': 5e9,
    'kPTOX': 0.01,
    'pHstroma': 7.8,
    'kleak': 1000,
    'bH': 100,
    'HPR': 14./3.,
            
    #Parameter associated with xanthophyll cycle
    'kDeepoxV': 0.0024,
    'kEpoxZ': 0.00024,
    'KphSatZ': 5.8,
    'nHX': 5.,
    'Kzsat': 0.12,
            
    #Parameter associated with PsbS protonation
    'nHL': 3,
    'kDeprot': 0.0096,
    'kProt': 0.0096,
    'KphSatLHC': 5.8,
            
    #Fitted quencher contribution factors
    'gamma0': 0.1,
    'gamma1': 0.25,
    'gamma2': 0.6,
    'gamma3': 0.15,
            
    #Physical constants
    'F': 96.485,
    'R': 8.3e-3, #J in KJ
    'T': 298,
            
    #Standard potentials
    'E0QAQAm': -0.140,
    'E0PQPQH2': 0.354,
    'E0PCPCm': 0.380,
    'DG0ATP': 30.6,
            
    #PFD
    'PFD': 100

            }
    
    

