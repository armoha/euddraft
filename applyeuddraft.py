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

import os
import subprocess
import sys
import traceback

import eudplib as ep

import freezeMpq
import msgbox
import scbank_core
from freeze import decryptOffsets, encryptOffsets, obfpatch, obfunpatch, unFreeze
from msgbox import MB_ICONHAND, MB_OK, MessageBeep, MessageBox
from pluginLoader import (
    isFreezeIssued,
    isPromptIssued,
    isSCBankIssued,
    loadPluginsFromConfig,
)
from readconfig import readconfig


def createPayloadMain(pluginList, pluginFuncDict):
    @ep.EUDFunc
    def payloadMain():
        """Main function of euddraft payload."""
        # init plugins
        if isFreezeIssued():
            unFreeze()
            # ep.PRT_SetInliningRate(0.05)

        if isSCBankIssued():
            scbank_core.onPluginStart()

        for pluginName in pluginList:
            onPluginStart = pluginFuncDict[pluginName][0]
            onPluginStart()

        # Do trigger loop
        if ep.EUDInfLoop()():
            if isFreezeIssued():
                decryptOffsets()
                obfpatch()

            if isSCBankIssued():
                scbank_core.beforeTriggerExec()

            for pluginName in pluginList:
                beforeTriggerExec = pluginFuncDict[pluginName][1]
                beforeTriggerExec()

            ep.RunTrigTrigger()

            for pluginName in reversed(pluginList):
                afterTriggerExec = pluginFuncDict[pluginName][2]
                afterTriggerExec()

            if isSCBankIssued():
                scbank_core.afterTriggerExec()

            if isFreezeIssued():
                obfunpatch()
                encryptOffsets()

            ep.EUDDoEvents()

        ep.EUDEndInfLoop()

    return payloadMain


##############################

if getattr(sys, "frozen", False):
    # frozen
    basepath = os.path.dirname(sys.executable)
else:
    # unfrozen
    basepath = os.path.dirname(os.path.realpath(__file__))

globalPluginPath = os.path.join(basepath, "plugins").lower()
# cx_Freeze modifies ep.__file__ to library.zip. So we use this convoluted
# way of getting eudplib install path.
epPath = os.path.dirname(ep.eudplibVersion.__code__.co_filename).lower()
edPath = os.path.dirname(MessageBox.__code__.co_filename).lower()


def isEpExc(s):
    s = s.lower()
    return (
        epPath in s
        or edPath in s
        or "<frozen " in s
        or (basepath in s and globalPluginPath not in s)
        or "runpy.py" in s
        or s.startswith('  file "eudplib')
    )


##############################


def applyEUDDraft(sfname):
    from eudplib.core.mapdata.tblformat import DecodeUnitNameAs
    from eudplib.eudlib.objpool import SetGlobalPoolFieldN
    from eudplib.epscript.epsimp import IsSCDBMap

    try:
        config, excs = readconfig(sfname)
        if excs:
            raise ExceptionGroup("Invalid config", excs)
        mainSection = config["main"]
        ifname = mainSection["input"]
        ofname = mainSection["output"]
        if ifname == ofname:
            raise RuntimeError("input and output file should be different.")

        mainOptions = (
            "input",
            "output",
            "shufflePayload",
            "debug",
            "decodeUnitName",
            "objFieldN",
            "sectorSize",
        )
        for mainOption in mainSection:
            if mainOption not in mainOptions:
                raise RuntimeError(f"Invalid option in [main]: {mainOption}")

        if "shufflePayload" in mainSection:
            ep.ShufflePayload(eval(mainSection["shufflePayload"]))

        if "debug" in mainSection:
            ep.EPS_SetDebug(True)

        if "decodeUnitName" in mainSection:
            unitname_encoding = mainSection["decodeUnitName"]
            DecodeUnitNameAs(unitname_encoding)

        if "objFieldN" in mainSection:
            field_n = int(mainSection["objFieldN"])
            SetGlobalPoolFieldN(field_n)

        sectorSize = 15
        if "sectorSize" in mainSection:
            sectorSize = int(mainSection["sectorSize"])

        print("---------- Loading plugins... ----------")
        ep.LoadMap(ifname)
        pluginList, pluginFuncDict = loadPluginsFromConfig(ep, config)

        print("--------- Injecting plugins... ---------")

        payloadMain = createPayloadMain(pluginList, pluginFuncDict)
        ep.CompressPayload(True)

        if IsSCDBMap():
            if isFreezeIssued():
                raise RuntimeError(
                    "Can't use freeze protection on SCDB map!\nDisable freeze by following plugin settings:\n\n[freeze]\nfreeze : 0\n"
                )
            print("SCDB - sectorSize disabled")
            sectorSize = None
        elif isFreezeIssued():
            # FIXME: Add variable sectorSize support for freeze
            print("Freeze - sectorSize disabled")
            sectorSize = None
        ep.SaveMap(ofname, payloadMain, sector_size=sectorSize)

        if isFreezeIssued():
            if isPromptIssued():
                print("Freeze - prompt enabled ")
                sys.stdout.flush()
                os.system("pause")
            print("[Stage 4/3] Applying freeze mpq modification...")
            try:
                ofname = ofname.encode("mbcs")
            except LookupError:
                ofname = ofname.encode(sys.getfilesystemencoding())
            ret = freezeMpq.applyFreezeMpqModification(ofname, ofname)
            if ret != 0:
                raise RuntimeError("Error on mpq protection (%d)" % ret)

        MessageBeep(MB_OK)
        return True

    except Exception as err:
        print("==========================================")
        MessageBeep(MB_ICONHAND)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        excs = traceback.format_exception(exc_type, exc_value, exc_traceback)
        formatted_excs = []

        for i, exc in enumerate(excs):
            if isEpExc(exc) and not all(isEpExc(e) for e in excs[i + 1 : -1]):
                continue
            plibPath = "C:\\Users\\armo\\AppData\\Local\\pypoetry\\Cache\\virtualenvs\\euddraft-rwy7uEJp-py3.11\\Lib\\site-packages\\eudplib\\"
            exc = exc.replace(plibPath, "eudplib\\")
            exc = exc.replace("C:\dev\euddraftPrivate\\", "euddraft\\")
            formatted_excs.append(exc)

        print(f"[Error] {err}", "".join(formatted_excs), file=sys.stderr)

        if msgbox.isWindows:
            msgbox.SetForegroundWindow(msgbox.GetConsoleWindow())
        return False
