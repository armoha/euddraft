#!/usr/bin/env python3

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

import multiprocessing as mp
import os
import sys
import time

import eudplib as ep

import autoupdate
import msgbox
from pluginLoader import getGlobalPluginDirectory
from readconfig import readconfig

version = "0.9.8.3"


def applylib():
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    libdir = os.path.join(datadir, "lib")
    sys.path.append(libdir)


applylib()


def applyEUDDraft(fname, queue=None):
    try:
        import applyeuddraft

        ret = applyeuddraft.applyEUDDraft(fname)
        if queue:
            queue.put(True)
        return ret
    except ImportError as e:
        if queue:
            if str(e).startswith("DLL load failed:"):
                queue.put(False)
            else:
                queue.put(True)
                raise
        else:
            raise


def isFileModified(path, since):
    # Ignore profile things
    if path.endswith(".epmap") or path.endswith(".epmap.prof"):
        return False

    try:
        mtime = max(os.path.getmtime(path), os.path.getctime(path))
        if mtime > since:
            return True
    except OSError:
        pass
    return False


def hasModifiedFile(dirname, since):
    ret = False
    for root, dirs, files in os.walk(dirname):
        dirs[:] = [d for d in dirs if d[0] != "." and d[0] != "_"]
        for f in files:
            finalpath = os.path.join(root, f)
            if isFileModified(finalpath, since):
                print("[File modified] %s" % finalpath)
                ret = True
    return ret


if __name__ == "__main__" or __name__ == "euddraft__main__":
    mp.freeze_support()
    autoupdate.issueAutoUpdate()

    print("euddraft %s : Simple eudplib plugin system" % version)
    print(" - This program follows MIT License. See license.txt")
    if msgbox.isWindows:
        print(" - Press SHIFT to force check update while opening euddraft.")

    if len(sys.argv) != 2:
        raise RuntimeError("Usage : euddraft [setting file]")

    # Chdir to setting files
    sfname = sys.argv[1]
    oldpath = os.getcwd()
    dirname, sfname = os.path.split(sfname)
    if dirname:
        os.chdir(dirname)
        sys.path.insert(0, os.path.abspath(dirname))

    # Use simple setting system
    if sfname[-4:] == ".eds":
        if not applyEUDDraft(sfname):
            input("Press Enter to continue...")

    # Daemoning system
    elif sfname[-4:] == ".edd":
        print(" - Daemon mode. Ctrl+C to quit. R to recompile (windows only)\n\n")
        mp.set_start_method("spawn")
        lasttime = None

        globalPluginDir = getGlobalPluginDirectory()

        try:
            inputMap = None

            def isModifiedFiles():
                return (
                    hasModifiedFile(globalPluginDir, lasttime)
                    or hasModifiedFile(".", lasttime)
                    or isFileModified(sfname, lasttime)
                    or (inputMap and isFileModified(inputMap, lasttime))
                )

            while True:
                # input map may change with edd update. We re-read inputMap
                # every time here.
                config = readconfig(sfname)
                mainSection = config["main"]
                inputMap = mainSection["input"]

                # Wait for changes
                while lasttime and not isModifiedFiles():
                    if msgbox.isWindows:
                        if msgbox.IsThisForeground() and msgbox.GetAsyncKeyState(ord("R")):
                            print("[Forced recompile issued]")
                            break
                    time.sleep(1)

                # epscript can alter other files if some file changes.
                # Wait 0.5 sec more for additional changes
                while True:
                    lasttime = time.time()
                    time.sleep(0.5)
                    if not isModifiedFiles():
                        break

                print("[[Updating on %s]]" % time.strftime("%Y-%m-%d %H:%M:%S"))

                compileStatus = False
                count = 0
                while not compileStatus and count < 5:
                    time.sleep(0.2)
                    q = mp.Queue()
                    p = mp.Process(target=applyEUDDraft, args=(sfname, q))
                    p.start()
                    compileStatus = q.get()
                    p.join()
                    count += 1
                    if not compileStatus:
                        print("# Compile failed [%d/%d]" % (count, 5), file=sys.stderr)

                if count == 5:
                    print("Unexpected error!\n\n", file=sys.stderr)
                else:
                    print("Done!\n\n")
                lasttime = time.time()
                time.sleep(1)

        except KeyboardInterrupt:
            pass

    # Freeze protection
    elif sfname[-4:].lower() == ".scx":
        print(" - Freeze protector mode.")
        import subprocess

        import applyeuddraft
        import freezeMpq
        import pluginLoader

        pluginLoader.freeze_enabled = True

        ep.LoadMap(sfname)
        payloadMain = applyeuddraft.createPayloadMain([], {})
        ep.CompressPayload(True)
        ofname = sfname[:-4] + " prt.scx"
        ep.SaveMap(ofname, payloadMain)
        print("[Stage 4/3] Applying freeze mpq modification...")
        try:
            ofname = ofname.encode("mbcs")
        except LookupError:
            ofname = ofname.encode(sys.getfilesystemencoding())
        ret = freezeMpq.applyFreezeMpqModification(ofname, ofname)
        if ret != 0:
            raise RuntimeError("Error on mpq protection (%d)" % ret)

    else:
        print("Invalid extension %s" % os.path.splitext(sfname)[1], file=sys.stderr)

    os.chdir(os.getcwd())
