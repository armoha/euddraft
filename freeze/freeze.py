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
    mix2,
)

from .mpqh import getMapHandleEPD

from .obfjump import (
    initOffsets,
    encryptOffsets,
    decryptOffsets,
    ObfuscatedJump,
    cryptKey
)





g_seedKey = None



def unFreeze():
    global tKeys

    mpqEPD = getMapHandleEPD()

    mpqHeaderEPD = f_epdread_epd_safe(mpqEPD + (0x130 // 4))
    blockTableEPD = f_epdread_epd_safe(mpqEPD + (0x134 // 4)).makeR()
    hashTableEPD = f_epdread_epd_safe(mpqEPD + (0x138 // 4)).makeR()

    if EUDIf()(MemoryEPD(mpqHeaderEPD + (0x14 // 4), AtLeast, 1)):
        DoActions([
            [
                SetCurrentPlayer(i),
                DisplayExtText("freeze needs mpq post-protection.")
            ] for i in range(8)
        ])
        if EUDInfLoop()():
            EUDDoEvents()
        EUDEndInfLoop()
    EUDEndIf()

    # Basic check
    mpqArchiveSize = f_dwread_epd_safe(mpqHeaderEPD + (0x08 // 4))
    mpqHashTableOffset = f_dwread_epd_safe(mpqHeaderEPD + (0x10 // 4))
    mpqBlockTableOffset = f_dwread_epd_safe(mpqHeaderEPD + (0x14 // 4))
    mpqHashTableSize = f_dwread_epd_safe(mpqHeaderEPD + (0x18 // 4))
    mpqBlockTableSize = f_dwread_epd_safe(mpqHeaderEPD + (0x1C // 4))
    # EUDJumpIfNot(mpqBlockTableOffset == 0, hell1) - This should match
    # EUDJumpIfNot(mpqBlockTableSize == mpqArchiveSize // 16, hell2)
    zero = mpqBlockTableOffset

    # To find first real block index, seek scenario.chk.
    # Find scenario.chk in hash table
    chkHashA = 0xB701656E
    chkHashB = 0xFCFB1EED
    chkHashOffset = EUDVariable()
    chkHashEntryEPD = EUDVariable()
    chkHashOffset << (0xAFC8C05D & (mpqHashTableSize - 1))
    if EUDInfLoop()():
        chkHashEntryEPD << hashTableEPD + 4 * chkHashOffset
        EUDBreakIf([
            MemoryEPD(chkHashEntryEPD + 0, Exactly, chkHashA),
            MemoryEPD(chkHashEntryEPD + 1, Exactly, chkHashB)
        ])
        # I know this is slow, but too prevent any vulnerability, we will do
        # exactly the same operation as sc does for finding mpq.
        chkHashOffset << ((chkHashOffset + 1) & (mpqHashTableSize - 1))
    EUDEndInfLoop()

    initialBlockIndex = f_dwread_epd_safe(chkHashEntryEPD + 3) + zero
    chkBlockEntryEPD = blockTableEPD + initialBlockIndex * 4

    # OK. Map seems pretty good.

    ###########################################################################

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
    cryptKey << mix(cryptKey, zero)

    def feedSample(sample, inplace=True):
        nonlocal seedKey
        if inplace:
            seedKey[0] << mix(seedKey[0], sample)
            seedKey[1] << mix(seedKey[1], seedKey[0])
            seedKey[2] << mix(seedKey[2], seedKey[1])
            seedKey[3] << mix(seedKey[3], seedKey[2])
        else:
            seedKey[0] = mix(seedKey[0], sample).makeL()
            seedKey[1] = mix(seedKey[1], seedKey[0]).makeL()
            seedKey[2] = mix(seedKey[2], seedKey[1]).makeL()
            seedKey[3] = mix(seedKey[3], seedKey[2]).makeL()

    def feedSampleByIndex(index, inplace=True):
        sample = f_dwread_epd_safe(blockTableEPD + index)
        feedSample(sample, inplace)

    # 1. Feed mpq header
    for i in range(8):
        feedSample(f_dwread_epd_safe(mpqHeaderEPD + i))

    for i in range(8):
        feedSampleByIndex(i, random.random() >= 0.5)

    # 2. Feed HET
    hashTableOffsetDiv4 = mpqHashTableOffset // 4
    for i in EUDLoopRange(mpqHashTableSize):
        feedSampleByIndex(hashTableOffsetDiv4 + i * 4 + 3)

    # 3. Feed BET
    blockTableOffsetDiv4 = initialBlockIndex * 4
    for i in EUDLoopRange(mpqBlockTableSize - initialBlockIndex - 2):
        feedSampleByIndex(blockTableOffsetDiv4 + i * 4)

    # 4. Feed scenario.chk sectorOffsetTable
    chkSectorNum = (f_dwread_epd_safe(chkBlockEntryEPD + 2) + 4095) // 4096
    i_ = EUDVariable(0)
    if EUDWhile()(i_ <= chkSectorNum):
        feedSampleByIndex(8 + i_)
        i_ += 3
    EUDEndWhile()

    # 5. Feed entire mpq file
    # For speed, we employ more simpler expression here instead of T function.
    SAMPLEN = 2048
    n = mpqArchiveSize // 4 - 4
    for i in range(4):
        for j in EUDLoopRange(SAMPLEN // 4):
            sample = f_dwread_epd(blockTableEPD + fileCursor % n)
            seedKey[i] += seedKey[i] + seedKey[i] + sample
            fileCursor << mix(fileCursor, j)

    # 6. Final feedback
    if EUDLoopN()(64):
        seedKey[0] << mix(seedKey[0], seedKey[3])
        seedKey[1] << mix(seedKey[1], seedKey[0])
        seedKey[2] << mix(seedKey[2], seedKey[1])
    EUDEndLoopN()

    # Append block data
    seedKeySrc = blockTableEPD + (mpqBlockTableSize - 1) * 4
    seedKey[0] = mix(seedKey[0], f_dwread_epd(seedKeySrc + 0))
    seedKey[1] = mix(seedKey[1], f_dwread_epd(seedKeySrc + 1))
    seedKey[2] = mix(seedKey[2], f_dwread_epd(seedKeySrc + 2))
    seedKey[3] = mix(seedKey[3], f_dwread_epd(seedKeySrc + 3))

    # now seedKey should be equal to destKey.

    # Modify tables!
    initOffsets(seedKey, destKeyVal, cryptKey)

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

    encryptOffsets()


