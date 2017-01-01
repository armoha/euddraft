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

from eudplib import (
    EUDFunc
)


@EUDFunc
def T(x):
    xsq = x * x
    return x * (xsq * (xsq * xsq + 1) + 1) + 0x8ada4053


unTDict = {}


def T2(x):
    x &= 0xFFFFFFFF
    xsq = x * x
    ret = (x * (xsq * (xsq * xsq + 1) + 1) + 0x8ada4053) & 0xFFFFFFFF
    unTDict[ret] = x
    return ret


def tryUnT(x):
    try:
        return T(unTDict[x])
    except KeyError:
        return x


def mix(x, y):
    return T(x) + y + 0x10f874f3


def mix2(x, y):
    return (T2(x) + y + 0x10f874f3) & 0xFFFFFFFF


def unT2(y):
    x = 0
    for bitindex in range(32):
        mask = (2 << bitindex) - 1
        if (y - T2(x)) & mask != 0:
            x += 1 << bitindex
    return x


def unmix2(z, y):
    return unT2((z - 0x10f874f3 - y) & 0xFFFFFFFF)
