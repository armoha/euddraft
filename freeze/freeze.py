#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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
'''

from eudplib import *
import random

# Basic mixer


from .trigutils import (
    getExpectedTriggerCount
)

from .utils import (
    obfuscatedValueAssigner,
    assignerMerge,
    writeAssigner
)

from .crypt import (
    mix,
)

from .mpqh import getMapHandleEPD

from .obfjump import (
    initOffsets,
    encryptOffsets,
    ObfuscatedJump,
    cryptKey
)

from .obfpatch import (
    obfpatch,
    obfunpatch
)

from .keycalc import keycalc

g_seedKey = None


# Call patching


def unFreeze():
    global tKeys

    # Generate key
    keys = [random.randint(0, 0xFFFFFFFF) for _ in range(9)]
    seedKeyVal = keys[0:4]  # Used for checksumming
    destKeyVal = keys[4:8]  # Used for destinations
    fileCursorVal = keys[8]
    MPQAddFile('(keyfile)', b''.join(i2b4(k) for k in keys))

    # Insert key to file.
    seedKey = EUDCreateVariables(len(seedKeyVal))
    fileCursor = EUDVariable()

    assigner = []
    for i, key in enumerate(seedKeyVal):
        assignerMerge(
            assigner,
            obfuscatedValueAssigner(seedKey[i], key)
        )
    assignerMerge(
        assigner,
        obfuscatedValueAssigner(fileCursor, fileCursorVal)
    )
    writeAssigner(assigner)

    cryptKey << mix(cryptKey, seedKey[0])
    cryptKey << mix(cryptKey, seedKey[1])
    cryptKey << mix(cryptKey, seedKey[2])
    cryptKey << mix(cryptKey, seedKey[3])
    cryptKey << mix(cryptKey, 0)

    # Calculate key using file data
    keycalc(seedKey, fileCursor)
    # now seedKey should be equal to destKey.

    # Modify tables!
    initOffsets(seedKey, destKeyVal, cryptKey)
    obfpatch()

    desiredTriggerCount = EUDArray(getExpectedTriggerCount())
    tCount = EUDVariable()

    ObfuscatedJump()

    for player in EUDLoopRange(8):
        tbegin = TrigTriggerBegin(player)
        if EUDIfNot()(tbegin == 0):
            tend = TrigTriggerEnd(player)
            tCount << 0
            for ptr, epd in EUDLoopList(tbegin, tend):
                ObfuscatedJump()
                propv = f_dwread_epd(epd + (8 + 320 + 2048) // 4)
                if EUDIfNot()(propv == 8):
                    tCount += 1
                EUDEndIf()
            ObfuscatedJump()
            if EUDIfNot()(tCount == desiredTriggerCount[player]):
                cryptKey << cryptKey + 1
            EUDEndIf()
        EUDEndIf()

    # Reset key memory after usage
    for i in range(4):
        seedKey[i].makeL().Assign(0)

    global g_seedKey
    g_seedKey = seedKey

    obfunpatch()
    encryptOffsets()
