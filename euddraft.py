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

import sys
import os
import time
from pluginLoader import getGlobalPluginDirectory

import multiprocessing as mp
import ctypes


GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState


def applyEUDDraft(fname, queue=None):
    try:
        import applyeuddraft
        applyeuddraft.applyEUDDraft(fname)
        if queue:
            queue.put(True)
    except ImportError as e:
        if queue:
            if str(e).startswith('DLL load failed:'):
                queue.put(False)
            else:
                queue.put(True)
                raise
        else:
            raise


def hasModifiedFile(dirname, since):
    for root, dirs, files in os.walk(dirname):
        dirs[:] = [d for d in dirs if d[:1] != '.']
        for f in files:
            finalpath = os.path.join(root, f)
            try:
                mtime = max(
                    os.path.getmtime(finalpath),
                    os.path.getctime(finalpath)
                )
                if mtime > since:
                    return True
            except OSError:
                pass
    return False


if __name__ == '__main__' or __name__ == 'euddraft__main__':
    mp.freeze_support()

    print("euddraft v0.7.3 : Simple eudplib plugin system")
    sys.argv.append("test.eds")

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
    if sfname[-4:] == '.eds':
        applyEUDDraft(sfname)

    # Daemoning system
    elif sfname[-4:] == '.edd':
        print(" - Daemon mode. Ctrl+C to quit, Ctrl+R to force recompile")
        mp.set_start_method('spawn')
        lasttime = None

        globalPluginDir = getGlobalPluginDirectory()

        try:
            while True:
                # Wait for changes
                while (
                    lasttime and
                    not hasModifiedFile(globalPluginDir, lasttime) and
                    not hasModifiedFile('.', lasttime)
                ):
                    if GetAsyncKeyState(0x11) and GetAsyncKeyState(ord('R')):
                        break
                    time.sleep(1)

                # epscript can alter other files if some file changes.
                # Wait 0.5 sec more for additional changes
                while True:
                    lasttime = time.time()
                    time.sleep(0.5)
                    if not (
                        hasModifiedFile(globalPluginDir, lasttime) or
                        hasModifiedFile('.', lasttime)
                    ):
                        break

                print(
                    "\n\n[[Updating on %s]]" %
                    time.strftime("%Y-%m-%d %H:%M:%S"))

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
                        print("# Compile failed [%d/%d]" % (count, 5))

                if count == 5:
                    print('Unexpected error!')
                else:
                    print("Done!")
                lasttime = time.time()
                time.sleep(1)

        except KeyboardInterrupt:
            pass

    else:
        print("Invalid extension %s" % os.path.splitext(sfname)[1])

    os.chdir(os.getcwd())
