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
from eudplib.core.variable.evcommon import _ev
from eudplib.eudlib.s import MoveCP, SetMemoryC, SetMemoryS, srand
from eudplib.maprw.inlinecode.ilcprocesstrig import GetInlineCodePlayerList

from .pdefault import default_ptex, default_pupx


def getExpectedTriggerCount():
    """Get expected output trigger counts for each players.

    Get expected trigger counts for each players, excluding eudplib injector
    triggers, but including eudplib trigger intro.

    Returns:
        count -- Trigger count for each players.
    """
    chkt = GetChkTokenized()
    trigSection = chkt.getsection("TRIG")
    count = [4] * 8
    for i in range(0, len(trigSection), 2400):
        bTrigger = trigSection[i : i + 2400]

        # Check for inline_eudplib code
        inlPC = GetInlineCodePlayerList(bTrigger)
        if inlPC:
            dummyTrigger = (
                bytes(320 + 2048 + 4)
                + b"".join([b"\x01" if inlPC & (1 << p) else b"\0" for p in range(27)])
                + b"\0"
            )
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


obf_pupx = None  # Memory related
obf_ptex = None
restore_pupx = None
restore_ptex = None
randonset = random.randint(1, 0xFFFFFFFF)
randbits = [random.randint(2**i, 0xFFFFFFFF) for i in range(32)]
obfuData = Db(360 + 480)


def BackupOrigPUPx():
    global obf_pupx, obf_ptex, restore_pupx, restore_ptex
    if obf_pupx is not None:
        return
    chkt = GetChkTokenized()
    try:
        orig_pupx = chkt.getsection("PUPx")
    except KeyError:
        orig_pupx = default_pupx
    try:
        orig_ptex = chkt.getsection("PTEx")
    except KeyError:
        orig_ptex = default_ptex
    for orig, count, bw in [(orig_pupx, 61, 46), (orig_ptex, 44, 24)]:
        smax = list()  # chk related
        sstart = list()
        sgmax = list()
        sgstart = list()
        sglobal = list()
        bwMax, bwStart = list(), list()  # Memory related
        bwMax_obf, bwStart_obf = list(), list()
        for i in range(count):
            max_p = [orig[i + p * count] for p in range(12)]
            start_p = [orig[i + p * count] for p in range(12, 24)]
            max_global = orig[i + 24 * count]
            start_global = orig[i + 25 * count]
            use_global = [orig[i + p * count] for p in range(26, 38)]
            if i >= bw:
                max_obf = [random.randint(0, 0xFF) for _ in range(12)]
                start_obf = [random.randint(0, 0xFF) for _ in range(12)]
                for p in range(12):
                    if use_global[p] == 1:
                        orig_max, orig_start = max_global, start_global
                    else:
                        orig_max, orig_start = max_p[p], start_p[p]
                    if i == 53:  # exclude [53] Anabolic synthesis
                        max_obf[p], start_obf[p] = orig_max, orig_start
                    else:
                        use_global[p] = 0
                    bwMax.append(orig_max)  # Memory related
                    bwStart.append(orig_start)
                bwMax_obf.extend(max_obf)
                bwStart_obf.extend(start_obf)
                max_p = max_obf
                start_p = start_obf
            smax.extend(max_p)  # chk related
            sstart.extend(start_p)
            sgmax.append(max_global)
            sgstart.append(start_global)
            sglobal.extend(use_global)
        tmax = list()
        tstart = list()
        tglobal = list()
        maxBW = list()
        startBW = list()
        oBFmaxBW = list()
        oBFstartBW = list()
        for p in range(12):
            ut_map = [
                (smax, tmax),
                (sstart, tstart),
                (sglobal, tglobal),
                (bwMax, maxBW),
                (bwStart, startBW),
                (bwMax_obf, oBFmaxBW),
                (bwStart_obf, oBFstartBW),
            ]
            for prv, nxt in ut_map:
                for i in range(p, len(prv), 12):
                    nxt.append(prv[i])
        t = tmax + tstart + sgmax + sgstart + tglobal
        if count == 61:
            restore_pupx = maxBW + startBW
            obf_pupx = oBFmaxBW + oBFstartBW
            pupx = b"".join([i2b1(i) for i in t])
            ep_assert(len(pupx) == 2318, "?")
            chkt.setsection("PUPx", pupx)
        else:
            restore_ptex = maxBW + startBW
            obf_ptex = oBFmaxBW + oBFstartBW
            ptex = b"".join([i2b1(i) for i in t])
            ep_assert(len(ptex) == 1672, "?")
            chkt.setsection("PTEx", ptex)
    _tmp_ru, _tmp_ou = list(), list()
    for i in range(0, 360, 4):
        v = restore_pupx[i]
        v += restore_pupx[i + 1] << 8
        v += restore_pupx[i + 2] << 16
        v += restore_pupx[i + 3] << 24
        w = obf_pupx[i]
        w += obf_pupx[i + 1] << 8
        w += obf_pupx[i + 2] << 16
        w += obf_pupx[i + 3] << 24
        _tmp_ru.append(v)
        _tmp_ou.append(w)
    restore_pupx = _tmp_ru
    obf_pupx = _tmp_ou
    _tmp_rt, _tmp_ot = list(), list()
    for i in range(0, 480, 4):
        v = restore_ptex[i]
        v += restore_ptex[i + 1] << 8
        v += restore_ptex[i + 2] << 16
        v += restore_ptex[i + 3] << 24
        w = obf_ptex[i]
        w += obf_ptex[i + 1] << 8
        w += obf_ptex[i + 2] << 16
        w += obf_ptex[i + 3] << 24
        _tmp_rt.append(v)
        _tmp_ot.append(w)
    restore_ptex = _tmp_rt
    obf_ptex = _tmp_ot


def RestorePUPx():
    BackupOrigPUPx()
    dst = Forward()
    k = EUDVariable()
    DoActions(
        srand(),
        SetMemoryS(dst, SetTo, EPD(obfuData) - 1),
        srand(),
        MoveCP(EPD(0x58F278)),
    )
    if EUDWhile()(k <= 360 // 4 - 1):
        x = f_dwread_cp(0)
        dst << x.getDestAddr()
        VProc(
            x,
            [
                SetMemoryC(dst, Add, 1),
                SetMemoryC(k.getValueAddr(), Add, 1),
                SetMemoryC(0x6509B0, Add, 1),
            ],
        )
    EUDEndWhile()
    DoActions(
        srand(),
        MoveCP(EPD(0x58F050)),
    )
    if EUDWhile()(k <= (360 + 480) // 4 - 1):
        f_dwread_cp(0, ret=[x])
        VProc(
            x,
            [
                SetMemoryC(0x6509B0, Add, 1),
                SetMemoryC(dst, Add, 1),
                SetMemoryC(k.getValueAddr(), Add, 1),
            ],
        )
    EUDEndWhile()
    t, acts = list(), list()
    for i, v in enumerate(restore_pupx):
        acts.append((0x58F278 + 4 * i, v))
    for i, v in enumerate(restore_ptex):
        acts.append((0x58F050 + 4 * i, v))
    random.shuffle(acts)
    t.append(srand())
    for dst, val in acts:
        t.append(SetMemoryS(dst, SetTo, val))
    t.append(SetMemoryC(0x6509B0, SetTo, 0))
    DoActions(t)


@EUDFunc
def fread():
    fread._frets = [c.SetDeaths(0, c.SetTo, 0, 0)]
    fread._retn = 1
    ret = EUDLightVariable(_from=fread._frets[0])

    ret << randonset
    r = list(range(32))
    random.shuffle(r)
    for i in r:
        Trigger(DeathsX(CurrentPlayer, AtLeast, 1, 0, 2**i), ret.AddNumber(randbits[i]))
    # return ret


def _fread(x):
    ret = randonset
    for i in range(32):
        if x & (2**i):
            ret += randbits[i]
    return ret & 0xFFFFFFFF


def getObf():
    obf, count, offset = obf_pupx, 360, obfuData
    if random.random() >= 0.5:
        obf, count, offset = obf_ptex, 480, obfuData + 360
    i = random.randrange(count // 4)
    offset += 4 * i
    f = _fread(obf[i])
    return offset, f


def ObfuscatedAdd(var, amount, acts=[]):
    ptr = var.getValueAddr()
    dst1, e1 = getObf()
    dst2, e2 = getObf()
    DoActions(srand(), MoveCP(EPD(dst1)))
    f1 = fread()
    DoActions(srand(), SetMemoryS(ptr, Add, f1), srand(), MoveCP(EPD(dst2)))
    f2 = fread()
    DoActions(
        srand(),
        SetMemoryS(ptr, Add, f2),
        srand(),
        SetMemoryS(ptr, Add, amount - e1 - e2),
        acts,
    )
