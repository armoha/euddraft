#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import random

from eudplib import *

from .crypt import mix, mix2
from .keycalc import keycalc
from .obfjump import ObfuscatedJump, cryptKey, encryptOffsets, initOffsets
from .obfpatch import obfpatch, obfunpatch
from .trigcrypt import decryptTrigger, encryptTriggers, obfuscateDT
from .trigutils import getExpectedTriggerCount, RestorePUPx, ObfuscatedAdd, SetMemoryC
from .utils import assignerMerge, obfuscatedValueAssigner, writeAssigner

# Basic mixer


g_seedKey = None


# Call patching


def unFreeze():
    global tKeys, cryptKey

    RestorePUPx()

    # Generate key
    keys = [random.randint(0, 0xFFFFFFFF) for _ in range(9)]
    seedKeyVal = keys[0:4]  # Used for checksumming
    destKeyVal = keys[4:8]  # Used for destinations
    fileCursorVal = keys[8]
    MPQAddFile("(keyfile)", b"".join(i2b4(k) for k in keys))

    triggerKeyVal = random.randint(0, 0xFFFFFFFF)
    triggerKey = EUDVariable()

    # Insert key to file.
    seedKey = [EUDVariable() for _ in seedKeyVal]
    fileCursor = EUDVariable()

    assigner = []
    for i, key in enumerate(seedKeyVal):
        assignerMerge(assigner, obfuscatedValueAssigner(seedKey[i], key))
    assignerMerge(assigner, obfuscatedValueAssigner(fileCursor, fileCursorVal))
    assignerMerge(assigner, obfuscatedValueAssigner(triggerKey, triggerKeyVal))
    writeAssigner(assigner)

    tempKey1 = mix(cryptKey, seedKey[0])
    tempKey2 = mix(tempKey1, seedKey[1])
    tempKey3 = mix(tempKey2, seedKey[2])
    tempKey4 = mix(tempKey3, seedKey[3])
    mix(tempKey4, 0, ret=cryptKey)

    cryptKeyVal = 0
    cryptKeyVal = mix2(cryptKeyVal, seedKeyVal[0])
    cryptKeyVal = mix2(cryptKeyVal, seedKeyVal[1])
    cryptKeyVal = mix2(cryptKeyVal, seedKeyVal[2])
    cryptKeyVal = mix2(cryptKeyVal, seedKeyVal[3])
    cryptKeyVal = mix2(cryptKeyVal, 0)

    # Calculate key using file data
    keycalc(seedKey, fileCursor)
    # now seedKey should be equal to destKey.

    # Modify tables!
    initOffsets(seedKey, destKeyVal, cryptKey)

    # Modify triggers
    desiredTriggerCount = EUDArray(getExpectedTriggerCount())
    encryptedTriggerCount = EUDArray(encryptTriggers(mix2(triggerKeyVal, cryptKeyVal)))
    tCount = EUDVariable()
    tInternalCount = EUDVariable()
    decryptedCount = EUDVariable()

    ObfuscatedJump()
    encryptTriggers(mix2(triggerKeyVal, cryptKeyVal))
    triggerKey = mix(triggerKey, cryptKey)

    def reset_seedkey1():
        random.shuffle(seedKey)
        key = seedKey.pop()
        return SetMemoryS(key.getValueAddr(), SetTo, 0)

    def reset_seedkey2():
        random.shuffle(seedKey)
        key = seedKey.pop()
        return SetMemoryC(key.getValueAddr(), SetTo, 0)

    for player in EUDLoopRange(8):
        tbegin = TrigTriggerBegin(player)
        if EUDIfNot()(tbegin == 0):
            tend = TrigTriggerEnd(player)
            acts = [
                reset_seedkey2(),
                reset_seedkey2(),
                SetMemoryC(tCount.getValueAddr(), SetTo, 0),
                SetMemoryC(tInternalCount.getValueAddr(), SetTo, 0),
                SetMemoryC(decryptedCount.getValueAddr(), SetTo, 0),
            ]
            random.shuffle(acts)
            DoActions(acts)
            for ptr, epd in EUDLoopList(tbegin, tend):
                ObfuscatedJump()
                offset = (8 + 320 + 2048) // 4
                decryptedCount += decryptTrigger(epd, triggerKey)
                ObfuscatedAdd(
                    epd, offset, [reset_seedkey2(), SetMemoryC(0x6509B0, SetTo, 0)]
                )
                propv = f_dwread_epd(epd)
                ObfuscatedAdd(
                    epd, -offset, [reset_seedkey2(), SetMemoryC(0x6509B0, SetTo, 0)]
                )
                if EUDIfNot()(propv == 8):
                    tCount += 1
                if EUDElse()():
                    tInternalCount += 1
                EUDEndIf()
            ObfuscatedJump()
            dst = EPD(desiredTriggerCount) + player
            cons = [MemoryEPD(dst, Exactly, tCount), tInternalCount == 217]
            random.shuffle(cons)
            Trigger(cons, cryptKey.AddNumber(1))
            cryptKey += decryptedCount - encryptedTriggerCount[player]
        EUDEndIf()

    # Reset key memory after usage
    # for i in range(4):
    #     seedKey[i].makeL().Assign(0)

    global g_seedKey
    g_seedKey = seedKey

    encryptOffsets()
