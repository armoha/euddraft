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

import ctypes
import sys

try:
    from winsound import MB_OK, MB_ICONHAND, MessageBeep

    def MessageBox(title, text, style=0, textio=sys.stdout):
        print("[%s]\n%s" % (title, text), file=textio)

        """ Helper function """
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.SetForegroundWindow(hWnd)
        ctypes.windll.user32.BringWindowToTop(hWnd)
        ctypes.windll.user32.SetForegroundWindow(hWnd)
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    isWindows = True

    from ctypes import WINFUNCTYPE, windll, c_int
    from ctypes.wintypes import HWND, SHORT

    prototype = WINFUNCTYPE(HWND)
    GetForegroundWindow = prototype(("GetForegroundWindow", windll.user32))
    GetConsoleWindow = prototype(("GetConsoleWindow", windll.kernel32))
    prototype = WINFUNCTYPE(HWND, HWND)
    SetForegroundWindow = prototype(("SetForegroundWindow", windll.user32))
    prototype = WINFUNCTYPE(SHORT, c_int)
    GetAsyncKeyState = prototype(("GetAsyncKeyState", windll.user32))

    def IsThisForeground():
        return GetForegroundWindow() == GetConsoleWindow()


except ImportError:
    MB_OK = 1
    MB_ICONHAND = 2

    def MessageBeep(type):
        for _ in range(type):
            sys.stdout.write("\a")

    def MessageBox(title, text, style=0, textio=sys.stdout):
        print("[%s]\n%s\n" % (title, text), file=textio)

    isWindows = False
