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
from .mpqh import getMapHandleEPD
from .crypt import mix
import random


def keycalc(seedKey, fileCursor):
    chkHandle, chkHandleEPD = f_dwepdread_epd_safe(EPD(0x6D0F24))

    mpqHeaderEPD = EUDVariable()
    blockTableEPD = EUDVariable()

    mpqArchiveSize = EUDVariable()
    mpqHashTableOffset = EUDVariable()
    mpqHashTableSize = EUDVariable()
    mpqBlockTableSize = EUDVariable()

    initialBlockIndex = EUDVariable()
    chkBlockEntryEPD = EUDVariable()

    if EUDIf()(Memory(0x6D0F14, Exactly, 0)):  # On game
        mpqEPD = getMapHandleEPD()
        mpqHeaderEPD << f_epdread_epd_safe(mpqEPD + (0x130 // 4))
        blockTableEPD << f_epdread_epd_safe(mpqEPD + (0x134 // 4))
        hashTableEPD = f_epdread_epd_safe(mpqEPD + (0x138 // 4))

        # Basic check
        mpqArchiveSize << f_dwread_epd_safe(mpqHeaderEPD + (0x08 // 4))
        mpqHashTableOffset << f_dwread_epd_safe(mpqHeaderEPD + (0x10 // 4))
        mpqHashTableSize << f_dwread_epd_safe(mpqHeaderEPD + (0x18 // 4))
        mpqBlockTableSize << f_dwread_epd_safe(mpqHeaderEPD + (0x1C // 4))
        # EUDJumpIfNot(mpqBlockTableOffset == 0, hell1) - This should match
        # EUDJumpIfNot(mpqBlockTableSize == mpqArchiveSize // 16, hell2)

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
            chkHashOffset << ((chkHashOffset + 1) & (mpqHashTableSize - 1))
        EUDEndInfLoop()

        initialBlockIndex << f_dwread_epd_safe(chkHashEntryEPD + 3)
        chkBlockEntryEPD << blockTableEPD + initialBlockIndex * 4

    if EUDElse()():  # On replay
        chkBlockSize = f_dwread_epd(chkHandleEPD - 4)

        mpqHeaderEPD << chkHandleEPD
        blockTableEPD << chkHandleEPD

        mpqArchiveSize << chkBlockSize
        mpqHashTableOffset << 0
        mpqHashTableSize << 0
        mpqBlockTableSize << chkBlockSize // 16

        initialBlockIndex << mpqBlockTableSize - 32
        chkBlockEntryEPD << EPD(Db(bytes(16)))

    EUDEndIf()

    DoActions(SetDeaths(0, SetTo, 5678, 0))

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
