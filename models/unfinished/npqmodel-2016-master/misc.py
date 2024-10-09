#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
misc
"""

import numpy as np

def pH(H):
    return -np.log10(H*2.5e-4)

def pHinv(pH):
    return 4e3 * 10 ** -pH
