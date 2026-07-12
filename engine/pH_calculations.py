"""
The pH engine -- computes the pH at any point in an acid-base titration.

it uses a single charge-balance equation: a solution must be electrically neutral, 
so the positive ions must equal the negative ions. This is what keeps the result 
correct right at the equivalence point, where region-based formulas break down.

Handles strong/weak monoprotic acids and monohydroxy bases (weak species carry
a Ka/Kb; strong species are treated as fully ionized).
"""

import math
from compounds import Acid, Base, acids, bases

Kw = 1e-14

def charge_imbalance(h, Ca, Cb, Ka=None, Kb=None):
    OH = Kw / h

    if Ka is None:
        anion = Ca
    else:
        anion = Ca * Ka / (Ka + h)

    if Kb is None:
        base_cation = Cb
    else:
        Ka_conj = Kw / Kb
        base_cation = Cb * h / (h + Ka_conj)

    positives = base_cation + h
    negatives = anion + OH
    return positives - negatives

def solve_pH(Ca, Cb, Ka=None, Kb=None):
    lo_pH, hi_pH = 0.0, 14.0

    for _ in range(16):
        mid_pH = (lo_pH + hi_pH) / 2
        h = 10 ** (-mid_pH)

        if charge_imbalance(h, Ca, Cb, Ka, Kb) > 0:
            lo_pH = mid_pH
        else:
            hi_pH = mid_pH

    return (lo_pH + hi_pH) / 2

def titration_pH(flask_compound, flask_concentration, flask_volume, burette_compound, burette_concentration, burette_volume_added):
    total_volume = flask_volume + burette_volume_added
    

    Ka = None
    Kb = None

    if isinstance(flask_compound, Acid):
        Ka = flask_compound.Ka
        Ca = (flask_concentration * flask_volume) / total_volume
        Cb = (burette_concentration * burette_volume_added) / total_volume
    elif isinstance(flask_compound, Base):
        Kb = flask_compound.Kb
        Ca = (burette_concentration * burette_volume_added) / total_volume
        Cb = (flask_concentration * flask_volume) / total_volume

    if isinstance(burette_compound, Acid):
        Ka = burette_compound.Ka
    elif isinstance(burette_compound, Base):
        Kb = burette_compound.Kb

    return solve_pH(Ca, Cb, Ka, Kb)

