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

from eudplib import (
    GetChkTokenized,
    GetPlayerInfo,
    b2i4,
    i2b4,
    EUDFunc,
    EUDIf,
    EUDEndIf,

    f_dwbreak,
    f_dwread_epd,
    f_dwwrite_epd,
)

from .freezecrypt import (
    mix,
    mix2,
    unmix2,
)

from eudplib.maprw.inlinecode.ilcprocesstrig import GetInlineCodePlayerList


def getExpectedTriggerCount():
    """Get expected output trigger counts for each players.

    Get expected trigger counts for each players, excluding eudplib injector
    triggers, but including eudplib trigger intro.

    Returns:
        count -- Trigger count for each players.
    """
    chkt = GetChkTokenized()
    trigSection = chkt.getsection('TRIG')
    count = [4] * 8
    for i in range(0, len(trigSection), 2400):
        bTrigger = trigSection[i:i + 2400]

        # Check for inline_eudplib code
        inlPC = GetInlineCodePlayerList(bTrigger)
        if inlPC:
            dummyTrigger = bytes(320 + 2048 + 4) + b''.join([
                b'\x01' if inlPC & (1 << p) else b'\0' for p in range(27)
            ]) + b'\0'
            tExcPlayers = getTriggerExecutingPlayers(dummyTrigger)

        # For normal triggers
        else:
            tExcPlayers = getTriggerExecutingPlayers(bTrigger)

        for i in range(8):
            if tExcPlayers[i]:
                count[i] += 1

    return count


def getTriggerExecutingPlayers(bTrigger):
    if bTrigger[320 + 2048 + 4 + 17] != 0:
        playerExecutesTrigger = [True] * 8

    else:  # Should check manually
        playerExecutesTrigger = [False] * 8
        # By player
        for player in range(8):
            if bTrigger[320 + 2048 + 4 + player] != 0:
                playerExecutesTrigger[player] = True

        # By force
        playerForce = [0] * 8
        for player in range(8):
            playerForce[player] = GetPlayerInfo(player).force

        for force in range(4):
            if bTrigger[320 + 2048 + 4 + 18 + force] != 0:
                for player in range(8):
                    if playerForce[player] == force:
                        playerExecutesTrigger[player] = True

    return playerExecutesTrigger


def bseti4(b, pos, dw):
    """ Inverse of b2i4 """
    b[pos: pos + 4] = i2b4(dw)


# Trigger encryption

def encryptTrigger(bTrigger, key):
    """ Encrypt trigger with key """
    bTrigger = bytearray(bTrigger)

    # Generate key
    r = random.randint(0, 0xFFFFFFFF)
    flag = b2i4(bTrigger, 320 + 2048)
    if flag >= 0x10:
        return None
    flag = (flag + 0x80000000) + (r & 0x7FFFF000)
    bTrigger[2368: 2372] = i2b4(flag)  # Apply flag

    # Generate encryption key
    flag -= 0x80000000
    r = mix2(key, flag)
    r = mix2(r, key)
    w0, w1 = r & 0xFFFF, (r >> 16) & 0xFFFF
    w0 %= 2368 // 4
    w1 %= 2368 // 4

    dw0 = b2i4(bTrigger, w0 * 4)
    dw1 = b2i4(bTrigger, w1 * 4)
    bseti4(bTrigger, w0 * 4, unmix2(dw0, flag))
    bseti4(bTrigger, w1 * 4, unmix2(dw1, flag))


@EUDFunc
def decryptTrigger(triggerEPD, key):
    """ Decrypt trigger with key """

    triggerEPD += 2  # Skip linked list part

    flag = f_dwread_epd(triggerEPD + (2368 // 4))
    if EUDIf()(flag >= 0x80000000):
        flag -= 0x80000000
        r = mix(key, flag)
        r = mix(r, key)

        w0, w1 = f_dwbreak(r)[0:2]
        w0 %= 2368 // 4
        w1 %= 2368 // 4

        dw0 = f_dwread_epd(triggerEPD + w0)
        dw1 = f_dwread_epd(triggerEPD + w1)
        f_dwwrite_epd(triggerEPD + w0, mix(dw0, flag))
        f_dwwrite_epd(triggerEPD + w1, mix(dw1, flag))
    EUDEndIf()
