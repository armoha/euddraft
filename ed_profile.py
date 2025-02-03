# Test script for profiling.
# This requires Roulette map, eudtrglib map.

import os
import sys

sys.path.insert(1, os.path.abspath("."))
os.chdir(
    "C:/Users/armo/Documents/StarCraft/!Project/RandomAbilityCraft-HAJE/eudplibdata"
)
sys.path.insert(1, os.path.abspath("."))


import euddraft


def f():
    euddraft.applyEUDDraft("EUDEditor.edd")


if False:
    from tests import profile_tool

    profile_tool.profile(f, "../euddraft/profile.json")
else:
    f()
