from eudplib import EUDFuncN
from eudplib.trigger import (
    triggerdef,
    branch
)
from .obfjump import ObfuscatedJump
import random


patchList = []


def issuePatcher(parent, attrname, ratio):
    oldcall = getattr(parent, attrname)

    def newcall(*args):
        if random.random() < ratio:
            ObfuscatedJump()
        return oldcall(*args)
    patchList.append((parent, attrname, oldcall, newcall))


issuePatcher(EUDFuncN, '__call__', 0.7)
issuePatcher(triggerdef, 'Trigger', 0.1)
issuePatcher(branch, 'EUDBranch', 0.2)


def obfpatch():
    for parent, attrname, oldcall, newcall in patchList:
        setattr(parent, attrname, newcall)


def obfunpatch():
    for parent, attrname, oldcall, newcall in patchList:
        setattr(parent, attrname, oldcall)
