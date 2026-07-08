
"""
This module models acid-base indicators and computes the colour one shows at a given pH.
Each indicator is treated as a weak acid with a known pKa value, and the colour is determined by the ratio of the acid and base forms at the given pH.
color_at_pH(pH) returns a hex color code representing the colour of the indicator at the specified pH so the colour shifts gradually through the transition.
"""

def blend_hex_colors(color1, color2, ratio):
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    r1 = int(color1[0:2], 16)
    g1 = int(color1[2:4], 16)
    b1 = int(color1[4:6], 16)
    r2 = int(color2[0:2], 16)
    g2 = int(color2[2:4], 16)
    b2 = int(color2[4:6], 16)
    
    r = round(r1 + (r2 - r1) * ratio)
    g = round(g1 + (g2 - g1) * ratio)
    b = round(b1 + (b2 - b1) * ratio)

    return f"#{r:02X}{g:02X}{b:02X}"
       

class Indicator:
    def __init__(self, name, pKa, acid_color, base_color):
        self.name = name
        self.pKa = pKa
        self.acid_color = acid_color
        self.base_color = base_color
    
    def color_at_pH(self, pH):
        ratio = 10 ** (pH - self.pKa)
        fraction = ratio / (1 + ratio) # Here, fraction represents the proportion of the base form of the indicator at the given pH.
        return blend_hex_colors(self.acid_color, self.base_color, fraction)

indicators = {}
indicators["Methyl Orange"] = Indicator("Methyl Orange", 3.7, "#FF0000", "#FFFF00")
indicators["Bromophenol Blue"] = Indicator("Bromophenol Blue", 4.0, "#FFFF00", "#0000FF")
indicators["Bromocresol Green"] = Indicator("Bromocresol Green", 4.7, "#FFFF00", "#0000FF")
indicators["Methyl Red"] = Indicator("Methyl Red", 5.1, "#FF0000", "#FFFF00")
indicators["Litmus"] = Indicator("Litmus", 6.5, "#FF0000", "#0000FF")
indicators["Bromothymol Blue"] = Indicator("Bromothymol Blue", 7.0, "#FFFF00", "#0000FF")
indicators["Phenolphthalein"] = Indicator("Phenolphthalein", 9.3, "#FFFFFF", "#FF00FF")

