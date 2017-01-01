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
from .utils import (
    obfuscatedValueAssigner,
    writeAssigner,
)

from .crypt import mix2, mix


cryptKey = EUDVariable()
oJumper = []
oJumperSet = set()
tKeys = None


def clearOJumper():
    oJumper.clear()
    oJumperSet.clear()


RegisterCreatePayloadCallback(clearOJumper)


class OJumperBuffer(EUDObject):

    def __init__(self):
        super().__init__()

    def GetDataSize(self):
        return (len(oJumper) + 1) * 4

    def WritePayload(self, pbuf):
        for ra in oJumper:
            pbuf.WriteDword(EPD(ra + 4))

        pbuf.WriteDword(0)


class CallerProxy(ConstExpr):
    def __init__(self, ptr, jumper):
        super().__init__(self)
        self.ptr = ptr
        self.index = len(oJumper)
        self.jumper = jumper

    def Evaluate(self):
        # Calculate value
        if self not in oJumperSet:
            self.index = len(oJumper)
            oJumper.append(self.jumper)
            oJumperSet.add(self)

            keyIndex = self.index % 4

            # mix & apply
            tKeys[keyIndex] = mix2(tKeys[keyIndex], self.index)
            self.modv = tKeys[keyIndex]

        ptrV = Evaluate(self.ptr)
        ep_assert(ptrV.rlocmode == 4, "Invalid ptrV.rlocmode")
        ptrV.rlocmode = 0  # Force unrelocate

        return ptrV - self.modv


def ObfuscatedJump():
    oJumper = Forward()
    pdst = Forward()

    cProxy = CallerProxy(pdst, oJumper)
    oJumper << RawTrigger(
        nextptr=cProxy,
    )
    pdst << NextTrigger()


oJumperArray = OJumperBuffer()


def initOffsets(seedKey, destKeyVal, cryptKey):
    global tKeys

    # Generate key
    r = random.randint(0, 0xFFFFFFFF)
    rv = EUDVariable()
    writeAssigner(obfuscatedValueAssigner(rv, r))

    tKeys = [mix2(k, r) for k in destKeyVal]
    seedKeyArray = EUDArray(4)
    for i in range(4):
        seedKeyArray[i] = mix(seedKey[i], rv)

    # Table modifier
    kIndex = EUDVariable()
    oJumperIndex = EUDVariable()
    cryptKey2 = EUDVariable()
    cryptKey2 << cryptKey

    if EUDInfLoop()():
        jumperEPD = f_dwread_epd(EPD(oJumperArray) + oJumperIndex)
        EUDBreakIf(jumperEPD == 0)

        key = mix(seedKeyArray[kIndex], oJumperIndex)
        v = f_dwread_epd(jumperEPD)
        f_dwwrite_epd(jumperEPD, v + key + RlocInt(0, 4))
        seedKeyArray[kIndex] = key

        oJumperIndex += 1
        kIndex += 1
        Trigger(kIndex == 4, kIndex.SetNumber(0))
        cryptKey2 << cryptKey2 + 0x46b8622c
    EUDEndInfLoop()

    for i in range(4):
        seedKeyArray[i] = f_dwrand()


def decryptOffsets():
    # Table modifier
    oJumperPtr = EUDVariable()
    oJumperPtr << EPD(oJumperArray)
    cryptKey2 = EUDVariable()
    cryptKey2 << cryptKey

    if EUDInfLoop()():
        jumperEPD = f_dwread_epd(oJumperPtr)
        EUDBreakIf(jumperEPD == 0)

        v = f_dwread_epd(jumperEPD)
        f_dwwrite_epd(jumperEPD, (v ^ cryptKey2) + cryptKey)

        oJumperPtr += 1
        cryptKey2 << cryptKey2 + 0x46b8622c
    EUDEndInfLoop()


def encryptOffsets():

    # Table modifier
    oJumperPtr = EUDVariable()
    oJumperPtr << EPD(oJumperArray)
    cryptKeyInv = EUDVariable()
    cryptKeyInv << -cryptKey
    cryptKey2 = EUDVariable()
    cryptKey2 << cryptKey

    if EUDInfLoop()():
        jumperEPD = f_dwread_epd(oJumperPtr)
        EUDBreakIf(jumperEPD == 0)

        v = f_dwread_epd(jumperEPD)
        f_dwwrite_epd(jumperEPD, (v + cryptKeyInv) ^ cryptKey2)

        oJumperPtr += 1
        cryptKey2 << cryptKey2 + 0x46b8622c
    EUDEndInfLoop()
