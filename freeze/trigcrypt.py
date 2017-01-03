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


from eudplib.maprw.inlinecode.ilcprocesstrig import GetInlineCodePlayerList


def bseti4(b, pos, dw):
    """ Inverse of b2i4 """
    b[pos: pos + 4] = i2b4(dw)


# Trigger encryption

tabCount = 1


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
        wlist.append(r % (2368 // 4))
        r = mix2(r, key + i)

    for i in range(tabCount - 1, -1, -1):
        w = wlist[i]
        dw = b2i4(bTrigger, w * 4)
        bseti4(bTrigger, w * 4, unmix2(dw, flag - i))

    return bTrigger


def encryptTriggers(cryptKey):
    chkt = GetChkTokenized()
    trigSection = chkt.getsection('TRIG')
    p = 0.05

    # Pre-crypt.
    for i in range(218):
        cryptKey = mix2(cryptKey, i)

    tIndex = 218
    bSet = []
    for i in range(0, len(trigSection), 2400):
        bTrigger = trigSection[i: i + 2400]
        # Only non-inline code can be crypted
        if not GetInlineCodePlayerList(bTrigger):
            if True or random.random() < p:
                bTrigger = encryptTrigger(bTrigger, cryptKey)
        bSet.append(bTrigger)
        cryptKey = mix2(cryptKey, tIndex)
        tIndex += 1

    chkt.setsection('TRIG', b''.join(bSet))


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
            w = r % (2368 // 4)
            dw = f_dwread_epd(triggerEPD + w)
            f_dwwrite_epd(triggerEPD + w, mix(dw, flag - i))
            r << mix(r, key + i)
    EUDEndIf()
