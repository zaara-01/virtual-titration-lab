"""
Charge-balance + binary-search titration demo.

Nothing here imports from engine/ -- it's a sandbox so you can run it,
poke at it, and see WHY the method works.

ONE charge_imbalance() function now covers all three real titration cases:
    - strong acid + strong base
    - weak acid   + strong base
    - weak base   + strong acid
You pick the case just by which constants (Ka / Kb) you supply.

Run it with:  python3 test.py
"""

import math

Kw = 1e-14  # water: [H+][OH-] = 1e-14 at 25 C


# ---------------------------------------------------------------------------
# STEP 1: "Do the charges balance at this guess of h = [H+]?"
#
# Every ion is one of two kinds:
#   - STRONG (fully ionized)  -> its concentration is a flat constant
#   - WEAK   (partly ionized) -> its concentration is an h-dependent fraction
#
# So we hand this function whichever constants apply:
#   Ka given  -> the acid is weak     |  Ka = None -> strong acid
#   Kb given  -> the base is weak     |  Kb = None -> strong base
#
# positives = negatives  when the charges balance.
#   f > 0 -> too much positive charge -> guessed h too BIG
#   f < 0 -> guessed h too SMALL
# ---------------------------------------------------------------------------
def charge_imbalance(h, Ca, Cb, Ka=None, Kb=None):
    OH = Kw / h

    # anion from the acid
    if Ka is None:                       # strong acid: fully ionized
        anion = Ca                       #   [Cl-] = all of it
    else:                                # weak acid: only a fraction ionizes
        anion = Ca * Ka / (Ka + h)       #   [A-]

    # cation from the base
    if Kb is None:                       # strong base: spectator cation
        base_cation = Cb                 #   [Na+] = all of it
    else:                                # weak base: only a fraction protonates
        Ka_conj = Kw / Kb                #   conjugate-acid constant Ka'
        base_cation = Cb * h / (h + Ka_conj)   # [BH+]

    positives = base_cation + h          # base cation + [H+]
    negatives = anion + OH               # acid anion + [OH-]
    return positives - negatives


# ---------------------------------------------------------------------------
# STEP 2: Binary search for the h (really, the pH) where charges balance.
# 16 halvings pins pH far below any precision you'd ever display.
# ---------------------------------------------------------------------------
def solve_pH(Ca, Cb, Ka=None, Kb=None):
    lo_pH, hi_pH = 0.0, 14.0

    for _ in range(16):
        mid_pH = (lo_pH + hi_pH) / 2
        h = 10 ** (-mid_pH)              # convert the pH guess back to [H+]

        if charge_imbalance(h, Ca, Cb, Ka, Kb) > 0:
            lo_pH = mid_pH               # too much positive charge -> go higher pH
        else:
            hi_pH = mid_pH

    return (lo_pH + hi_pH) / 2


# ---------------------------------------------------------------------------
# STEP 3: Turn "how much acid / how much base is in the flask right now"
# into formal concentrations, then solve. Works no matter which one is the
# titrant -- you just vary whichever volume is being added.
# Volumes in LITRES.
# ---------------------------------------------------------------------------
def titration_pH(acid_conc, acid_vol, base_conc, base_vol, Ka=None, Kb=None):
    total_vol = acid_vol + base_vol
    Ca = (acid_conc * acid_vol) / total_vol    # total acid, ionized or not
    Cb = (base_conc * base_vol) / total_vol    # total base added
    return solve_pH(Ca, Cb, Ka, Kb)


# ---------------------------------------------------------------------------
# DEMOS: same solver, three different titrations.
# ---------------------------------------------------------------------------
titrant_mL = [0, 5, 10, 12.5, 20, 24, 24.9, 25, 25.1, 30, 40, 50]


def print_curve(title, compute_pH):
    print(f"\n{title}")
    print(" titrant (mL) |  pH")
    print("--------------+------")
    for mL in titrant_mL:
        print(f"   {mL:6.1f}     | {compute_pH(mL):6.2f}")


# 1) STRONG ACID + STRONG BASE
#    Flask: 25 mL 0.10 M HCl.  Burette: 0.10 M NaOH.
#    No Ka, no Kb -> both strong. Equivalence should land on exactly 7.00.
print_curve(
    "STRONG ACID + STRONG BASE  (0.10 M HCl  vs  0.10 M NaOH)",
    lambda mL: titration_pH(0.10, 0.025, 0.10, mL / 1000.0),
)

# 2) WEAK ACID + STRONG BASE
#    Flask: 25 mL 0.10 M acetic acid (Ka=1.74e-5).  Burette: 0.10 M NaOH.
#    Half-equiv (12.5 mL) -> pH == pKa ~ 4.76.  Equivalence ~ 8.7 (basic).
print_curve(
    "WEAK ACID + STRONG BASE  (0.10 M CH3COOH  vs  0.10 M NaOH)",
    lambda mL: titration_pH(0.10, 0.025, 0.10, mL / 1000.0, Ka=1.74e-5),
)

# 3) WEAK BASE + STRONG ACID
#    Flask: 25 mL 0.10 M ammonia (Kb=1.77e-5).  Burette: 0.10 M HCl.
#    Here the ACID volume is the one that varies (it's the titrant).
#    Equivalence ~ 5.3 (acidic salt).
print_curve(
    "WEAK BASE + STRONG ACID  (0.10 M NH3  vs  0.10 M HCl)",
    lambda mL: titration_pH(0.10, mL / 1000.0, 0.10, 0.025, Kb=1.77e-5),
)
