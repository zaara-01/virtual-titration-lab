"""
Tests for the pH engine.

These check the solver against pH values you can look up in any chemistry
textbook -- the key reference points of a titration curve. If a future change
breaks the chemistry, one of these will fail.
"""

import os
import sys

# makes engine/ importable
ENGINE = os.path.join(os.path.dirname(__file__), "..", "engine")
sys.path.insert(0, os.path.abspath(ENGINE))

from ph_calculations import titration_pH
from compounds import acids, bases

HCl = acids["HCl"]
AcOH = acids["CH3COOH"]
NaOH = bases["NaOH"]
NH3 = bases["NH3"]

V = 0.025   # 25 mL in the flask, in litres
TOL = 0.03  # pH tolerance for the comparisons


def close(got, expected):
    return abs(got - expected) < TOL


# strong acid + strong base

def test_strong_acid_alone():
    # 0.10 M HCl, no base added yet -> pH = -log10(0.10) = 1.00
    assert close(titration_pH(HCl, 0.10, V, NaOH, 0.10, 0.0), 1.00)


def test_strong_strong_equivalence_is_seven():
    # equal moles of strong acid and strong base -> neutral, exactly 7.00
    assert close(titration_pH(HCl, 0.10, V, NaOH, 0.10, 0.025), 7.00)


def test_strong_base_excess():
    # 50 mL 0.10 M NaOH into 25 mL 0.10 M HCl -> strongly basic
    assert close(titration_pH(HCl, 0.10, V, NaOH, 0.10, 0.050), 12.52)


# weak acid + strong base

def test_weak_acid_alone():
    # 0.10 M acetic acid by itself -> ~2.87
    assert close(titration_pH(AcOH, 0.10, V, NaOH, 0.10, 0.0), 2.87)


def test_weak_acid_half_equivalence_equals_pKa():
    # at half-equivalence pH == pKa == -log10(1.75e-5) == 4.76
    assert close(titration_pH(AcOH, 0.10, V, NaOH, 0.10, 0.0125), 4.76)


def test_weak_acid_equivalence_is_basic():
    # equivalence of a weak acid / strong base is basic
    assert close(titration_pH(AcOH, 0.10, V, NaOH, 0.10, 0.025), 8.73)


# weak base + strong acid

def test_weak_base_alone():
    # 0.10 M ammonia by itself -> ~11.13
    assert close(titration_pH(NH3, 0.10, V, HCl, 0.10, 0.0), 11.13)


def test_weak_base_half_equivalence():
    # at half-equivalence pH == 14 - pKb == 9.25
    assert close(titration_pH(NH3, 0.10, V, HCl, 0.10, 0.0125), 9.25)


def test_weak_base_equivalence_is_acidic():
    # equivalence of a weak base / strong acid is acidic
    assert close(titration_pH(NH3, 0.10, V, HCl, 0.10, 0.025), 5.27)


# Does the curve have any spikes or crashes?
def test_curve_is_smooth_through_equivalence():
    prev = None
    mL = 20.0
    while mL <= 30.0:
        pH = titration_pH(AcOH, 0.10, V, NaOH, 0.10, mL / 1000.0)
        if prev is not None:
            assert pH >= prev - TOL
            assert pH - prev < 2.0
        prev = pH
        mL += 0.1


if __name__ == "__main__":
    tests = [
            test_strong_acid_alone,
            test_strong_strong_equivalence_is_seven,
            test_strong_base_excess,
            test_weak_acid_alone,
            test_weak_acid_half_equivalence_equals_pKa,
            test_weak_acid_equivalence_is_basic,
            test_weak_base_alone,
            test_weak_base_half_equivalence,
            test_weak_base_equivalence_is_acidic,
            test_curve_is_smooth_through_equivalence,
        ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError:
            print(f"FAIL  {t.__name__}")
    print(f"\n{passed}/{len(tests)} passed")
