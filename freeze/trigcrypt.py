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

import random

from eudplib import *

from .crypt import (
    mix,
    mix2,
    unmix2,
)

from .trigutils import getTriggerExecutingPlayers
from eudplib.maprw.inlinecode.ilcprocesstrig import GetInlineCodePlayerList


def bseti4(b, pos, dw):
    """ Inverse of b2i4 """
    b[pos: pos + 4] = i2b4(dw)


# Trigger encryption

tabCount = 16


def hexdump(b):
    print(''.join('%02X' % ch for ch in b))


def encryptTrigger(bTrigger_, key):
    """ Encrypt trigger with key """
    bTrigger = bytearray(bTrigger_)

    # Generate key
    r = random.randint(0, 0xFFFFFFFF)
    flag = b2i4(bTrigger, 2368)
    if flag >= 0x10:
        return bTrigger_
    flag = (flag + 0x80000000) + (r & 0x7FFFF000)
    bTrigger[2368: 2372] = i2b4(flag)  # Apply flag

    # Generate encryption key
    flag -= 0x80000000
    r = mix2(key, flag)
    r = mix2(r, key)

    wlist = []
    for i in range(tabCount):
        wlist.append(r % (2368 // 32))
        r = mix2(r, key + i)

    for i in range(tabCount - 1, -1, -1):
        w = wlist[i]
        adddw = mix2(w, i)
        for j in range(8):
            dw = b2i4(bTrigger, w * 4)
            bseti4(bTrigger, w * 4, dw - adddw)
            w += 2368 // 32

    return bTrigger


def encryptTriggers(cryptKey):
    chkt = GetChkTokenized()
    trigSection = chkt.getsection('TRIG')
    p = 0.05

    encryptedCount = [0] * 8

    # Pre-crypt.
    bSet = []
    for i in range(0, len(trigSection), 2400):
        bTrigger = trigSection[i: i + 2400]
        # Only non-inline code can be crypted
        if not GetInlineCodePlayerList(bTrigger):
            if random.random() < p:
                pExc = getTriggerExecutingPlayers(bTrigger)
                for i in range(8):
                    if pExc[i]:
                        encryptedCount[i] += 1
                bTrigger = encryptTrigger(bTrigger, cryptKey)
        bSet.append(bTrigger)

    chkt.setsection('TRIG', b''.join(bSet))
    return encryptedCount


@EUDFunc
def decryptTrigger(triggerEPD, key, index):
    """ Decrypt trigger with key """

    triggerEPD += 2  # Skip linked list part

    flag = f_dwread_epd(triggerEPD + (2368 // 4))
    if EUDIf()(flag >= 0x80000000):
        flag -= 0x80000000
        r = mix(key, flag)
        r = mix(r, key).makeR()

        for i in EUDLoopRange(tabCount):
            w = r % (2368 // 32)
            adddw = mix(w, i)
            oldcp = f_getcurpl()
            f_setcurpl(triggerEPD + w)
            DoActions([[
                SetDeaths(CurrentPlayer, Add, adddw, 0),
                SetMemory(0x6509B0, Add, 2368 // 32)
            ] for _ in range(8)])
            f_setcurpl(oldcp)
            r << mix(r, key + i)

        EUDReturn(1)
    EUDEndIf()
    EUDReturn(0)
