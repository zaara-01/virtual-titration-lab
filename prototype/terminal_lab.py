"""
Virtual Titration Lab -- text-based prototype interface.

A terminal version of the game, used to work out the exact interaction flow
before building the graphical UI.

This is a scratch prototype for figuring out the logic and screen flow -- not
the final interface. The real GUI will reuse the same game.py underneath.
"""

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from game import TitrationGame, acids, bases, indicators, cm3
import random

def choose_mode():
    mode = input("Choose a mode (challenge/sandbox): ").strip().lower()
    return mode if mode in ["challenge", "sandbox"] else choose_mode()

def setup_challenge():
    flask_type = random.choice(["acid", "base"])
    if flask_type == "acid":
        flask_compound = random.choice(list(acids.values()))
    else:
        flask_compound = random.choice(list(bases.values()))

    burette_type = "base" if flask_type == "acid" else "acid"
    table = acids if burette_type == "acid" else bases
    
    if flask_compound.strength == "weak":
        options = [c for c in table.values() if c.strength == "strong"] 
        # because a weak acids/base can only be titrated with strong acid/base
    else:
        options = list(table.values())  

    print(f"\nThere is 25 cm^3 of {flask_compound.name} with an unknown concentration in a conical flask.", end=" ")
    print(f"Your job is to calculate its concentration by titrating it with 0.1 mol/dm^3 of {burette_type}.")
    print(f"This is the list of {burette_type}s you can use:")
    for i, compound in enumerate(options, start=1):
        print(f" {i}. {compound.name}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            burette_compound = options[choice - 1]
            acid = flask_compound if flask_type == "acid" else burette_compound
            base = burette_compound if flask_type == "acid" else flask_compound
            break
        except (ValueError, IndexError):
            print("Please enter a valid number from the list.")

    indicator_options = list(indicators.values())    

    if acid.strength == "strong" and base.strength == "strong":
        equivalence = "neutral, around pH 7"
    elif acid.strength == "weak" and base.strength == "strong":
        equivalence = "basic, above pH 7"
    else:
        equivalence = "acidic, below pH 7"

    print(f"\nYou have a {acid.strength} acid ({acid.name}) and a {base.strength} base ({base.name})", end=" ")
    print(f"so the equivalence point will be {equivalence}.")
    print("Pick an indicator whose colour change lines up with that pH:\n")

    for i, ind in enumerate(indicator_options, start=1):
        low = ind.pKa - 1
        high = ind.pKa + 1
        print(f" {i}. {ind.name}  (pKa {ind.pKa}, changes ~pH {low:.1f}-{high:.1f})")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            indicator = indicator_options[choice - 1]
            break
        except (ValueError, IndexError):
            print("Please enter a valid number from the list.")

    game = TitrationGame("challenge", flask_compound, burette_compound, indicator)
    return game


def setup_sandbox():
    pass

    #in progress