import os
import sys
import random
import tkinter as tk
from tkinter import ttk

# make the engine/ package importable
ENGINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine")
sys.path.insert(0, os.path.abspath(ENGINE))

from compounds import acids, bases
from indicators import indicators
from ph_calculations import titration_pH



