"""
Virtual Titration Lab -- game logic layer.

A TitrationGame object represents one titration session in progress. 
it drips titrant in drop by drop, tracks the pH and the indicator's colour at every
step, records the curve, and handles the two game modes:

  --> Challenge -- the flask holds an acid or base of a hidden, randomly chosen
    concentration. The player titrates, records concordant titres, and submits
    a calculated concentration to be marked.
  --> Sandbox   -- the compounds, indicator, and concentrations are all chosen
    and visible; the full pH curve is captured as you drip.
"""

import os
import sys
import random

# make the engine importable
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine")
sys.path.insert(0, os.path.abspath(ENGINE))

from compounds import acids, bases
from indicators import indicators
from ph_calculations import titration_pH

# game constants

flask_volume = 0.025 # 25 cm^3 in the conical flask
drop_volume = 0.00005 # ~0.05 cm^3 per drop
max_volume = 0.050 # 50 cm^3 burette capacity
standard_conc = 0.100 # the known burette concentration (mol/dm^3)
concordance = 0.20 # titres within 0.20 cm^3 are concordant
answer_tolerance = 0.03 # answer accepted within 3% of the truth


def cm3(dm3):
    return dm3 * 1000.0


class TitrationGame:
    def __init__(self, mode, flask_compound, burette_compound, indicator,
                 flask_conc=None, burette_conc=standard_conc):

        self.mode = mode # "challenge" or "sandbox"
        self.flask_compound = flask_compound
        self.burette_compound = burette_compound
        self.indicator = indicator
        self.burette_conc = burette_conc

        if mode == "challenge":
            self.flask_conc = round(random.uniform(0.05, 0.15), 3)
        else:
            self.flask_conc = flask_conc

        self.volume_added = 0.0
        self.burette_level = max_volume
        self.history = [] # list of (volume_cm3, pH) points for graph

        # challenge-only
        self.titres = [] # recorded titres, in cm^3
        self.mean_titre = None # cm^3, set once two runs are concordant
        self.phase = "dripping" # dripping -> titre_logged -> concordant -> checked

    def current_pH(self):
        return titration_pH(
            self.flask_compound, self.flask_conc, flask_volume,
            self.burette_compound, self.burette_conc, self.volume_added,
        )

    def current_color(self):
        return self.indicator.color_at_pH(self.current_pH())

    def add_drop(self):
        # deliver one drop from the burette
        # increases self.volume_added by drop_volume (without going past max_volume)
        # appends the new point (cm3(self.volume_added), self.current_pH()) to self.history so a graph can be drawn later
      
        if self.burette_level <= 0.0:
            return
        self.volume_added += drop_volume
        self.burette_level -= drop_volume
        self.history.append((cm3(self.volume_added), self.current_pH()))

    def log_titre(self):
        # appends the current volume_added (in cm^3) to self.titres
        # checks if the new titre is concordant with any previous titres and if so then calculates the mean titre
        self.titres.append(cm3(self.volume_added))
        for titre in self.titres[:-1]:
            if round(abs(titre - self.titres[-1]), 2) <= concordance:
                self.mean_titre = round((titre + self.titres[-1]) / 2, 2)
                self.phase = "concordant"
                return
        self.phase = "titre_logged"

    def refill(self):
        self.burette_level = max_volume

    def next_run(self):
        # start a fresh flask for another titration run
        self.volume_added = 0.0
        self.burette_level = max_volume
        self.history = []
        self.phase = "dripping"

    def check_answer(self, guess):
        # Compare the student's concentration guess to the hidden truth.
        truth = self.flask_conc
        correct = abs(guess - truth) <= answer_tolerance * truth
        self.phase = "checked"
        return correct
