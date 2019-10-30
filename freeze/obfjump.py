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
from .utils import obfuscatedValueAssigner, writeAssigner
from .trigutils import ObfuscatedAdd, SetMemoryC

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
        return RlocInt(ptrV.offset - self.modv, 0)


def ObfuscatedJump():
    oJumper = Forward()
    pdst = Forward()
    r = random.randint(0, 0xFFFFFFFF)

    cProxy = CallerProxy(pdst - r, oJumper)
    oJumper << RawTrigger(nextptr=cProxy, actions=SetMemoryC(oJumper + 4, Add, r))
    pdst << RawTrigger(actions=SetMemoryC(oJumper + 4, Add, -r))


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
        f_dwadd_epd(jumperEPD, key + RlocInt(0, 4))
        seedKeyArray[kIndex] = key

        obfus = random.randint(0, 0xFFFFFFFF)
        ObfuscatedAdd(
            cryptKey2, obfus, [kIndex.AddNumber(1), oJumperIndex.AddNumber(1)]
        )
        Trigger(kIndex == 4, kIndex.SetNumber(0))
        ObfuscatedAdd(cryptKey2, 0x46B8622C - obfus, SetMemoryC(0x6509B0, SetTo, 0))
    EUDEndInfLoop()

    for i in range(4):
        seedKeyArray[i] = f_dwrand()


def decryptOffsets():
    # Table modifier
    oJumperPtr = EUDVariable()
    cryptKey2 = EUDVariable()
    acts = [cryptKey.QueueAssignTo(cryptKey2), oJumperPtr.SetNumber(EPD(oJumperArray))]
    random.shuffle(acts)
    VProc(cryptKey, acts)
    obfus1 = random.randint(1, 0xFFFFFFFF)
    obfus2 = random.randint(1, 0xFFFFFFFF)

    if EUDInfLoop()():
        jumperEPD = f_dwread_epd(oJumperPtr)
        EUDBreakIf(jumperEPD == 0)

        v = f_dwread_epd(jumperEPD)
        f_bitxor(v, cryptKey2, ret=v)
        acts = [
            cryptKey.QueueAddTo(v),
            jumperEPD.SetDest(EPD(v.getDestAddr())),
            SetMemoryC(oJumperPtr.getValueAddr(), Add, obfus1),
            SetMemoryC(cryptKey2.getValueAddr(), Add, obfus2),
        ]
        random.shuffle(acts)
        VProc([cryptKey, jumperEPD, v], acts)
        acts = [
            SetMemoryC(oJumperPtr.getValueAddr(), Add, 1 - obfus1),
            SetMemoryC(cryptKey2.getValueAddr(), Add, 0x46B8622C - obfus2),
        ]
        random.shuffle(acts)
        DoActions(acts)
    EUDEndInfLoop()


def encryptOffsets():
    # Table modifier
    oJumperPtr = EUDVariable()
    cryptKeyInv = -cryptKey
    obfus1 = random.randint(1, 0xFFFFFFFF)
    obfus2 = random.randint(1, 0xFFFFFFFF)
    cryptKey2 = EUDVariable()
    VProc(
        cryptKey,
        [cryptKey.QueueAssignTo(cryptKey2), oJumperPtr.SetNumber(EPD(oJumperArray))],
    )

    if EUDInfLoop()():
        jumperEPD = f_dwread_epd(oJumperPtr)
        EUDBreakIf(jumperEPD == 0)

        v = f_dwread_epd(jumperEPD)
        acts = [
            cryptKeyInv.QueueAddTo(v),
            SetMemoryC(oJumperPtr.getValueAddr(), Add, obfus1),
        ]
        random.shuffle(acts)
        VProc(cryptKeyInv, acts)
        x = v ^ cryptKey2
        acts = [
            SetMemoryC(jumperEPD.getDestAddr(), SetTo, EPD(x.getDestAddr())),
            SetMemoryC(cryptKey2.getValueAddr(), Add, obfus2),
        ]
        random.shuffle(acts)
        VProc([jumperEPD, x], acts)
        acts = [
            SetMemoryC(oJumperPtr.getValueAddr(), Add, 1 - obfus1),
            SetMemoryC(cryptKey2.getValueAddr(), Add, 0x46B8622C - obfus2),
        ]
        random.shuffle(acts)
        DoActions(acts)
    EUDEndInfLoop()
