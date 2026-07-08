# virtual-titration-lab

An interactive titration simulator built on **real acid–base chemistry**.
You choose an acid, a base, and an indicator, and the engine computes the 
pH at every drop the way it actually behaves in the flask.

> **Status: early / work in progress.** Right now this is just the chemistry
> engine — the pH-calculation core and its supporting data (compounds and
> indicators). The interactive simulation and UI are still to come.

## What works today

- **pH engine** (`engine/pH_calculations.py`) — computes the pH at any point in
  a titration for the three cases that matter in practice:
  - strong acid + strong base
  - weak acid + strong base
  - weak base + strong acid
- **Compound data** (`engine/compounds.py`) — a small library of common acids
  and bases with their strengths and dissociation constants.
- **Indicators** (`engine/indicators.py`) — models an indicator's colour as a
  continuous blend between its acid and base colours, based on pH.
- **Tests** (`tests/test_ph.py`) — the engine is checked against known textbook
  pH values.

## Still to come

- Dripping the titrant in and drawing the live pH curve
- Live indicator colour change in a flask
- An interactive front end
- Adapting the chemistry for polyprotic acids/bases

## How the chemistry works

Most simple titration simulators stitch together separate formulas for the
different regions of the curve (before, at, and after the equivalence point).
That approach is fragile: it divides by near-zero quantities right where the
curve is steepest, producing a non-physical spike at the endpoint.

This engine takes a single, unified approach instead.

### One equation: charge balance

A solution has to be electrically neutral — the positive charges must exactly
equal the negative charges:

```
  positive ions  =  negative ions
```

Every ion concentration can be written in terms of one unknown, `h = [H⁺]`:

- `[OH⁻] = Kw / h`  (water's self-ionization, `Kw = 1e-14`)
- a **strong** acid or base is fully ionized, so its ion is just a constant
- a **weak** acid contributes `[A⁻] = C · Ka / (Ka + h)`
- a **weak** base contributes `[BH⁺] = C · h / (h + Ka′)`, where `Ka′ = Kw / Kb`

So for, say, a weak acid being titrated with a strong base (Na⁺ spectator), the
balance is:

```
  Na⁺  +  H⁺   =   OH⁻  +  A⁻

  Cb  +  h   =   Kw/h  +  Ca·Ka/(Ka + h)
```

The `Kw/h` term is present *everywhere* on the curve — including right at the
equivalence point, which is exactly where it matters most. That's what keeps the
result correct across the whole titration with no special cases.

### Solving it: binary search

There's no need to rearrange that equation by hand. Since the charge imbalance
changes sign as `h` moves, we find the answer by **binary search on the pH
scale** (0–14): guess a pH, check whether there's too much positive or negative
charge, and halve the range accordingly. About 16 halvings pin the pH down far
below any precision you'd ever display.

The same "do the charges balance here?" question is asked at every point on the
curve, so the buffer region, the equivalence point, and the excess region all
fall out of one method.

### It matches the textbook

| Titration | Point | pH |
|---|---|---|
| 0.10 M HCl vs 0.10 M NaOH | equivalence | **7.00** (neutral) |
| 0.10 M CH₃COOH vs 0.10 M NaOH | half-equivalence | **4.76** (= pKa) |
| 0.10 M CH₃COOH vs 0.10 M NaOH | equivalence | **8.73** (basic salt) |
| 0.10 M NH₃ vs 0.10 M HCl | half-equivalence | **9.25** (= 14 − pKb) |
| 0.10 M NH₃ vs 0.10 M HCl | equivalence | **5.27** (acidic salt) |

## Running it

Requires only Python 3 (standard library — nothing to install).

```bash
# run the tests
python3 tests/test_ph.py     # or: pytest

# use the engine
cd engine
python3 -c "
from pH_calculations import titration_pH
from compounds import acids, bases
# 12.5 mL of 0.1 M NaOH into 25 mL of 0.1 M acetic acid:
print(titration_pH(acids['CH3COOH'], 0.1, 0.025, bases['NaOH'], 0.1, 0.0125))
"
```

Volumes are in **dm^3** and concentrations in **mol/dm^3**.

## License

See [LICENSE](LICENSE).
