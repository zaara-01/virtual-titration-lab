class Acid:
    def __init__(self, name, formula, strength, molar_mass, Ka=None):
        self.name = name
        self.formula = formula
        self.strength = strength
        self.molar_mass = molar_mass
        self.Ka = Ka

class Base:
    def __init__(self, name, formula, strength, molar_mass, Kb=None):
        self.name = name
        self.formula = formula
        self.strength = strength
        self.molar_mass = molar_mass
        self.Kb = Kb

acids = {}
acids["HCl"] = Acid("Hydrochloric acid", "HCl", "strong", 36.5)
acids["H2SO4"] = Acid("Sulfuric acid", "H2SO4", "strong", 98.1)
acids["HNO3"] = Acid("Nitric acid", "HNO3", "strong", 63.0)
acids["CH3COOH"] = Acid("Ethanoic acid", "CH3COOH", "weak", 60.0, 1.74e-5)

bases = {}
bases["NaOH"] = Base("Sodium hydroxide", "NaOH", "strong", 40.0)
bases["KOH"] = Base("Potassium hydroxide", "KOH", "strong", 56.1)
bases["NH3"] = Base("Ammonia", "NH3", "weak", 17.0, 1.77e-5)

