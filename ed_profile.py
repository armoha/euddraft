# Test script for profiling.
# This requires Roulette map, eudtrglib map.

import os
import sys

sys.path.insert(1, os.path.abspath("."))
os.chdir("../Roulette")
sys.path.insert(1, os.path.abspath("."))
sys.path.insert(1, os.path.abspath("../eudtrglib"))


import euddraft


def f():
    euddraft.applyEUDDraft("main.edd")


if False:
    from tests import profile_tool
    profile_tool.profile(f, '../euddraft/profile.json')
else:
    f()

os.chdir("../euddraft")
