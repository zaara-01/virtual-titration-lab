import math
from compounds import acids, bases

Kw = 1e-14

def pH(substance, concentration):
    if isinstance(substance, Acid):
        if substance.strength == "strong":
            return -1 * (math.log10(concentration))
        else:
            return -1 * (math.log10(math.sqrt(substance.Ka * concentration)))
    elif isinstance(substance, Base):
        if substance.strength == "strong":
            return 14 + (math.log10(concentration))
        else:
            return 14 + (math.log10(math.sqrt(substance.Kb * concentration)))
    else:
        return None

def strong_strong_pH(acid_concentration, base_concentration, acid_volume, base_volume):
    acid_moles = acid_concentration * acid_volume
    base_moles = base_concentration * base_volume
    total_volume = acid_volume + base_volume

    if acid_moles > base_moles:
        excess_moles = acid_moles - base_moles
        H_concentration = excess_moles / total_volume
        return -math.log10(H_concentration)

    elif base_moles > acid_moles:
        excess_moles = base_moles - acid_moles
        OH_concentration = excess_moles / total_volume
        return 14 + math.log10(OH_concentration)

    else:
        return 7.0


def weak_acid_strong_base_pH(Ka, acid_concentration, acid_volume, base_concentration, base_volume):
    acid_moles = acid_concentration * acid_volume
    base_moles = base_concentration * base_volume
    total_volume = acid_volume + base_volume

    pKa = -math.log10(Ka)

    #henderson-hasslebach equation
    if acid_moles > base_moles:
        acid_moles_remaining = acid_moles - base_moles
        conjugate_base_moles = base_moles
        return pKa + math.log10(conjugate_base_moles / acid_moles_remaining)

    #strong base in excess
    elif base_moles > acid_moles:
        excess_base_moles = base_moles - acid_moles
        OH_concentration = excess_base_moles / total_volume
        return 14 + math.log10(OH_concentration)
    
    #equivalence point (pH will be basic)
    else:
        conjugate_base_concentration = acid_moles / total_volume
        Kb = Kw / Ka
        OH_concentration = math.sqrt(Kb * conjugate_base_concentration)
        return 14 + math.log10(OH_concentration)

def strong_acid_weak_base_pH(acid_concentration, acid_volume, Kb, base_concentration, base_volume):
    acid_moles = acid_concentration * acid_volume
    base_moles = base_concentration * base_volume
    total_volume = acid_volume + base_volume

    pKb = -math.log10(Kb)
    
    #henderson-hasslebach equation
    if base_moles > acid_moles:
        base_moles_remaining = base_moles - acid_moles
        conjugate_acid_moles = acid_moles
        return 14 - (pKb + math.log10(conjugate_acid_moles / base_moles_remaining))

    #strong acid in excess
    elif acid_moles > base_moles:
        excess_acid_moles = acid_moles - base_moles
        H_concentration = excess_acid_moles / total_volume
        return -math.log10(H_concentration)
    
    #equivalence point (pH will be acidic)
    else:
        conjugate_acid_concentration = base_moles / total_volume
        Ka = Kw / Kb
        H_concentration = math.sqrt(Ka * conjugate_acid_concentration)
        return -math.log10(H_concentration)

def weak_acid_weak_base_pH(Ka, acid_concentration, acid_volume, Kb, base_concentration, base_volume):
    acid_moles = acid_concentration * acid_volume
    base_moles = base_concentration * base_volume
    total_volume = acid_volume + base_volume

    pKa = -math.log10(Ka)
    pKb = -math.log10(Kb)

    if acid_moles > base_moles:
        acid_moles_remaining = acid_moles - base_moles
        conjugate_base_moles = base_moles
        return pKa + math.log10(conjugate_base_moles / acid_moles_remaining)
    
    elif base_moles > acid_moles:
        base_moles_remaining = base_moles - acid_moles
        conjugate_acid_moles = acid_moles
        return 14 - (pKb + math.log10(conjugate_acid_moles / base_moles_remaining))
    
    else:
        return 7.0 + 0.5 * (pKa - pKb)

def new_pH(flask_compound, flask_concentration, flask_volume,
           burette_compound, burette_concentration, burette_volume_added):

    if burette_volume_added == 0:
        return pH(flask_compound, flask_concentration)

    if isinstance(flask_compound, Acid) and isinstance(burette_compound, Base):
        acid = flask_compound
        acid_concentration = flask_concentration
        acid_volume = flask_volume

        base = burette_compound
        base_concentration = burette_concentration
        base_volume = burette_volume_added

    elif isinstance(flask_compound, Base) and isinstance(burette_compound, Acid):
        acid = burette_compound
        acid_concentration = burette_concentration
        acid_volume = burette_volume_added

        base = flask_compound
        base_concentration = flask_concentration
        base_volume = flask_volume

    else:
        raise ValueError("You need one acid and one base.")

    
    if acid.strength == "strong" and base.strength == "strong":
        return strong_strong_pH(acid_concentration, base_concentration, acid_volume, base_volume)
    elif acid.strength == "strong" and base.strength == "weak":
        return strong_acid_weak_base_pH(acid_concentration, acid_volume, base.Kb, base_concentration, base_volume)
    elif acid.strength == "weak" and base.strength == "strong":
        return weak_acid_strong_base_pH(acid.Ka, acid_concentration, acid_volume, base_concentration, base_volume)
    elif acid.strength == "weak" and base.strength == "weak":
        return weak_acid_weak_base_pH(acid.Ka, acid_concentration, acid_volume, base.Kb, base_concentration, base_volume)
    else:
        return None
    

        