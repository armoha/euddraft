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

from .crypt import mix
from .mpqh import getMapHandleEPD


def keycalc(seedKey, fileCursor):
    if EUDIf()(Memory(0x6D0F14, Exactly, 0)):  # On game
        mpqEPD = getMapHandleEPD()
        mpqEPD += 0x130 // 4
        mpqHeaderEPD = f_epdread_epd(mpqEPD)
        DoActions([mpqEPD.AddNumber(1), mpqHeaderEPD.AddNumber(0x10 // 4)])
        blockTableEPD = f_epdread_epd(mpqEPD)
        # Basic check
        mpqHashTableOffset = f_dwread_epd(mpqHeaderEPD)
        DoActions([mpqEPD.AddNumber(1), mpqHeaderEPD.AddNumber(2)])
        hashTableEPD = f_epdread_epd(mpqEPD)
        mpqHashTableSize = f_dwread_epd(mpqHeaderEPD)
        mpqHeaderEPD += 1
        mpqBlockTableSize = f_dwread_epd(mpqHeaderEPD)
        DoActions(
            [
                mpqHashTableSize.AddNumber(-1),
                mpqBlockTableSize.AddNumber(-1),
                mpqHeaderEPD.AddNumber(-(0x1C // 4)),
            ]
        )

        # To find first real block index, seek scenario.chk.
        # Find scenario.chk in hash table
        chkHashA = 0xB701656E
        chkHashB = 0xFCFB1EED
        chkHashOffset = EUDVariable()
        chkHashEntryEPD = EUDVariable()
        chkHashOffset << (0xAFC8C05D & mpqHashTableSize)
        if EUDInfLoop()():
            chkHashEntryEPD << hashTableEPD + 4 * chkHashOffset
            EUDBreakIf(
                [
                    MemoryEPD(chkHashEntryEPD, Exactly, chkHashA),
                    MemoryEPD(chkHashEntryEPD + 1, Exactly, chkHashB),
                ]
            )
            chkHashOffset += 1
            chkHashOffset << (chkHashOffset & mpqHashTableSize)
        EUDEndInfLoop()

        chkHashEntryEPD += 3
        initialBlockIndex = f_dwread_epd(chkHashEntryEPD)
        blockTableOffsetDiv4 = initialBlockIndex * 4
        chkBlockEntryEPD = blockTableEPD + blockTableOffsetDiv4

    """if EUDElse()():  # On replay
        DoActions([
            [
                SetCurrentPlayer(pl),
                DisplayText("Freeze protection doesn't support replay mode"),
            ] for pl in range(8)
        ])
        if EUDInfLoop()():
            EUDDoEvents()
        EUDEndInfLoop()"""
    EUDEndIf()

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
        sample = f_dwread_epd(blockTableEPD + index)
        feedSample(sample, inplace)

    # 1. Feed mpq header
    if EUDLoopN()(8):
        feedSample(f_dwread_epd(mpqHeaderEPD))
        mpqHeaderEPD += 1
    EUDEndLoopN()

    for i in range(8):
        feedSampleByIndex(i, random.random() >= 0.5)

    # 2. Feed HET
    hashTableOffsetDiv4 = mpqHashTableOffset // 4
    DoActions(
        [
            chkBlockEntryEPD.AddNumber(2),
            initialBlockIndex.AddNumber(2),
            hashTableOffsetDiv4.AddNumber(3),
        ]
    )
    if EUDWhileNot()(mpqHashTableSize == -1):
        feedSampleByIndex(hashTableOffsetDiv4)
        DoActions([mpqHashTableSize.AddNumber(-1), hashTableOffsetDiv4.AddNumber(4)])
    EUDEndWhile()

    # 3. Feed BET
    # blockTableOffsetDiv4 = initialBlockIndex * 4
    if EUDWhile()(mpqBlockTableSize >= initialBlockIndex):
        feedSampleByIndex(blockTableOffsetDiv4)
        DoActions([initialBlockIndex.AddNumber(1), blockTableOffsetDiv4.AddNumber(4)])
    EUDEndWhile()

    # 4. Feed scenario.chk sectorOffsetTable
    chkSector_ = f_dwread_epd(chkBlockEntryEPD)
    chkSector_ += 4095
    chkSectorNum = chkSector_ // 4096
    i_ = EUDVariable(0)
    if EUDWhile()(i_ <= chkSectorNum):
        i_ += 8
        feedSampleByIndex(i_)
        i_ -= 5
    EUDEndWhile()

    # 5. Feed entire block table
    # For speed, we employ more simpler expression here instead of T function.
    SAMPLEN = 2048
    n = mpqBlockTableSize * 4
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
    seedKeySrc = blockTableEPD + n
    seedKey[0] = mix(seedKey[0], f_dwread_epd(seedKeySrc))
    seedKeySrc += 1
    seedKey[1] = mix(seedKey[1], f_dwread_epd(seedKeySrc))
    seedKeySrc += 1
    seedKey[2] = mix(seedKey[2], f_dwread_epd(seedKeySrc))
    seedKeySrc += 1
    seedKey[3] = mix(seedKey[3], f_dwread_epd(seedKeySrc))
