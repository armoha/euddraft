# Test script for profiling.
# This requires Roulette map, eudtrglib map.

import os
import sys
import time

repoDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, repoDir)
os.chdir(os.path.join(repoDir, "..", "RandomAbilityCraft-HAJE", "eudplibdata"))
sys.path.insert(1, os.path.abspath("."))


import euddraft


def f():
    euddraft.applyEUDDraft("EUDEditor.edd")


if False:
    from tests import profile_tool

    profile_tool.profile(f, "../euddraft/profile.json")
else:
    start = time.time()
    f()
    print(f"\nFinished in {time.time() - start:.2f}s")
