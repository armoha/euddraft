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

import eudplib as ep
import traceback
import sys
import os
import subprocess
from readconfig import readconfig
from pluginLoader import loadPluginsFromConfig, isFreezeIssued, isMpaqIssued
from msgbox import MessageBox, MessageBeep, MB_OK, MB_ICONHAND
import msgbox
import freezeMpq


from freeze import (
    unFreeze,
    decryptOffsets,
    encryptOffsets,
    obfpatch,
    obfunpatch,
)


def createPayloadMain(pluginList, pluginFuncDict):
    @ep.EUDFunc
    def payloadMain():
        """ Main function of euddraft payload """
        # init plugins
        if isFreezeIssued():
            unFreeze()
            ep.PRT_SetInliningRate(0.05)

        for pluginName in pluginList:
            onPluginStart = pluginFuncDict[pluginName][0]
            onPluginStart()

        # Do trigger loop
        if ep.EUDInfLoop()():
            if isFreezeIssued():
                decryptOffsets()
                obfpatch()

            for pluginName in pluginList:
                beforeTriggerExec = pluginFuncDict[pluginName][1]
                beforeTriggerExec()

            ep.RunTrigTrigger()

            for pluginName in reversed(pluginList):
                afterTriggerExec = pluginFuncDict[pluginName][2]
                afterTriggerExec()

            if isFreezeIssued():
                obfunpatch()
                encryptOffsets()

            ep.EUDDoEvents()

        ep.EUDEndInfLoop()

    return payloadMain


##############################

if getattr(sys, 'frozen', False):
    # frozen
    basepath = os.path.dirname(sys.executable)
else:
    # unfrozen
    basepath = os.path.dirname(os.path.realpath(__file__))

globalPluginPath = os.path.join(basepath, 'plugins').lower()
# cx_Freeze modifies ep.__file__ to library.zip. So we use this convoluted
# way of getting eudplib install path.
epPath = os.path.dirname(ep.eudplibVersion.__code__.co_filename).lower()
edPath = os.path.dirname(MessageBox.__code__.co_filename).lower()


def isEpExc(s):
    s = s.lower()
    return (
        epPath in s or
        edPath in s or
        '<frozen ' in s or
        (basepath in s and globalPluginPath not in s) or
        'runpy.py' in s or
        s.startswith('  file "eudplib')
    )

##############################


def applyEUDDraft(sfname):
    try:
        config = readconfig(sfname)
        mainSection = config['main']
        ifname = mainSection['input']
        ofname = mainSection['output']
        if ifname == ofname:
            raise RuntimeError('input and output file should be different.')

        try:
            if mainSection['debug']:
                ep.EPS_SetDebug(True)
        except KeyError:
            pass

        print('---------- Loading plugins... ----------')
        ep.LoadMap(ifname)
        pluginList, pluginFuncDict = loadPluginsFromConfig(ep, config)

        print('--------- Injecting plugins... ---------')

        payloadMain = createPayloadMain(pluginList, pluginFuncDict)
        ep.CompressPayload(True)
        ep.SaveMap(ofname, payloadMain)

        if isFreezeIssued():
            print("[Stage 4/3] Applying freeze mpq modification...")
            ret = freezeMpq.applyFreezeMpqModification(ep.u2b(ofname), ep.u2b(ofname), isMpaqIssued())
            if ret != 0:
                raise RuntimeError("Error on mpq protection (%d)" % ret)

        MessageBeep(MB_OK)
        return True

    except Exception as e:
        print("==========================================")
        MessageBeep(MB_ICONHAND)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        excs = traceback.format_exception(exc_type, exc_value, exc_traceback)
        formatted_excs = []

        for i, exc in enumerate(excs):
            if isEpExc(exc) and not all(isEpExc(e) for e in excs[i + 1:-1]):
                continue
            formatted_excs.append(exc)

        print("[Error] %s" % e, ''.join(formatted_excs))
        if msgbox.isWindows:
            msgbox.SetForegroundWindow(msgbox.GetConsoleWindow())
        return False
