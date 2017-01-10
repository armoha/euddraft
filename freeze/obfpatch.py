from eudplib import EUDFuncN
from eudplib import trigger
from eudplib import ctrlstru
from .obfjump import ObfuscatedJump
import random
from math import sqrt

patchList = []


def issuePatcher(parent, attrname, ratio):
    oldcall = getattr(parent, attrname)

    maxcalln = 1000 * sqrt(ratio)
    calln = 0

    def oldcall2(*args, **kwargs):
        pass

    def newcall(*args, **kwargs):
        nonlocal calln
        ratio2 = ratio * (maxcalln - calln) / maxcalln
        if random.random() < ratio2:
            ObfuscatedJump()
        calln += 1
        return oldcall(*args, **kwargs)
    patchList.append((parent, attrname, oldcall, newcall))


issuePatcher(EUDFuncN, '__call__', 0.7)
issuePatcher(trigger, 'Trigger', 0.05)
issuePatcher(trigger, 'EUDBranch', 0.03)
issuePatcher(ctrlstru, 'EUDSwitch', 0.8)  # for TRIG encryption


def obfpatch():
    for parent, attrname, oldcall, newcall in patchList:
        setattr(parent, attrname, newcall)


def obfunpatch():
    for parent, attrname, oldcall, newcall in patchList:
        setattr(parent, attrname, oldcall)
