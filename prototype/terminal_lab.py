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


def choice(table):
    while True:
        try:
            choice = int(input("\nEnter the number of your choice: "))
            return table[choice-1]
        except:
            print("Please enter a valid number.")


def ask_concentration(prompt):
    while True:
        try:
            conc = float(input(prompt))
            if conc > 0:
                return conc
            print("Concentration must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


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
    
    burette_compound = choice(options)
    acid = flask_compound if flask_type == "acid" else burette_compound
    base = burette_compound if flask_type == "acid" else flask_compound

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

    indicator = choice(indicator_options)

    game = TitrationGame("challenge", flask_compound, burette_compound, indicator)
    return game


def setup_sandbox():
    print("\nYou are in sandbox mode. You can choose any acid, base, and indicator.")
    print("\nFirst, choose what type of solution is in the conical flask:")
    print(" 1. Acid")
    print(" 2. Base")
    
    type_list = ['acid', 'base']
    flask_type = choice(type_list)
    
    flask_table = acids if flask_type == "acid" else bases
    burette_type = "base" if flask_type == "acid" else "acid"
    burette_table = bases if flask_type == "acid" else acids

    print(f"\nHere is a list of {flask_type}s:")
    for i, substance in enumerate(flask_table, start=1):
        print(f"{i}. {substance}")
    
    flask_compound = choice(list(flask_table.values()))
    flask_conc = ask_concentration(f"\nEnter the concentration of {flask_compound.name} (mol/dm^3): ")

    if flask_compound.strength == "weak":
        burette_options = [c for c in burette_table.values() if c.strength == "strong"]
        # a weak acid/base can only be titrated with a strong one
    else:
        burette_options = list(burette_table.values())

    print(f"\nHere is a list of {burette_type}s:")
    for i, compound in enumerate(burette_options, start=1):
        print(f"{i}. {compound.name}")

    burette_compound = choice(burette_options)
    burette_conc = ask_concentration(f"\nEnter the concentration of {burette_compound.name} (mol/dm^3): ")

    acid = flask_compound if flask_type == "acid" else burette_compound
    base = flask_compound if flask_type == "base" else burette_compound

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

    indicator = choice(indicator_options)

    game = TitrationGame("sandbox", flask_compound, burette_compound, indicator, flask_conc=flask_conc, burette_conc=burette_conc)    
    return game


def swatch(hex_color, width=4):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"\033[48;2;{r};{g};{b}m{' ' * width}\033[0m"


def show_state(game):
    ml = cm3(game.volume_added)
    burette = cm3(game.burette_level)
    print(f"\nAdded: {ml:5.2f} cm^3   Burette: {burette:5.2f} cm^3   "
          f"pH: {game.current_pH():5.2f}   {swatch(game.current_color())}")
    

def add_many(game, n):
    for i in range(n):
        game.add_drop()


def play_sandbox(game):
    print("\nSandbox: drip and watch the pH and colour change.")
    print("Commands:  [enter]=1 drop   f=add 1 cm^3   c=coarse (5 cm^3)   "
          "r=refill   q=quit")
    
    while True:
        show_state(game)
        cmd = input("> ").strip().lower()
        if cmd == "":
            game.add_drop()
        elif cmd == "f":
            add_many(game, 20) # 20 drops = ~1 cm^3
        elif cmd == "c":
            add_many(game, 100) # ~5 cm^3
        elif cmd == "r":
            game.refill()
        elif cmd == "q":
            break

    print(f"\nDone. {len(game.history)} points recorded for the curve.")


def play_challenge(game):
    print("\nChallenge: find the flask's hidden concentration.")
    print("Titrate, log at least two concordant titres (within 0.20 cm^3), then submit.")
    print("Commands:  [enter]=1 drop   f=add 1 cm^3   c=coarse (5 cm^3)   t=log titre   n=next run   r=refill   s=submit   q=quit")

    while True:
        show_state(game)
        cmd = input("> ").strip().lower()

        if cmd == "":
            game.add_drop()
        elif cmd == "f":
            add_many(game, 20)
        elif cmd == "c":
            add_many(game, 100)
        elif cmd == "r":
            game.refill()
        elif cmd == "t":
            game.log_titre()
            print("\nRecorded titres (cm^3):", [f"{t:.2f}" for t in game.titres])
            if game.phase == "concordant":
                print(f"Concordant! Mean titre = {game.mean_titre:.2f} cm^3.")
                print("Calculate the concentration and submit with 's'.")
            else:
                print("Logged. Press 'n' to start another run and get a concordant pair.")
        elif cmd == "n":
            game.next_run()
            print("\nFresh flask, burette refilled. Start dripping again.")
        elif cmd == "s":
            if game.mean_titre is None:
                print("\nYou need two concordant titres before submitting.")
                continue
            try:
                guess = float(input("Your calculated concentration (mol/dm^3): "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            correct = game.check_answer(guess)
            truth = game.flask_conc
            if correct:
                print(f"\nCorrect! True concentration was {truth:.3f} mol/dm^3.")
            else:
                print(f"\nNot quite. You said {guess:.3f}; "
                      f"true value was {truth:.3f} mol/dm^3.")
            break
        elif cmd == "q":
            break


def main():
    mode = choose_mode()
    if mode == "challenge":
        game = setup_challenge()
        play_challenge(game)
    else:
        game = setup_sandbox()
        play_sandbox(game)


main()