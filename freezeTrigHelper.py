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
    GetPlayerInfo
)

from eudplib.maprw.inlinecode.ilcprocesstrig import GetInlineCodePlayerList


def getExpectedTriggerCount():
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
