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
    IsConstExpr,
    EUDVariable,
)
from freezecrypt import (
    T2,
    tryUnT,
)


class L(list):
    """ Hashable list """

    def __hash__(self):
        return id(self)


def obfuscatedValueAssigner(v, vInsert):
    """ 'v := vInsert' in an obfuscated way  """
    # (+, v, a, vI-a)   v := a + (vInsert - a)
    # (^, v, a, vI^a)   v := a ^ (vInsert ^ a)
    # (-, v, vI+a, a)   v := (vInsert + a) - a
    # (&, v, a, b)      v := (a | vInsert) & (b | vInsert)  ( a & b == 0 )
    # (|, v, a, b)      v := (a & vInsert) | (b & vInsert)  ( a|b = 0xFFFFFFFF)

    assert IsConstExpr(vInsert)

    desiredOperationCount = random.randint(32, 96)
    t = random.randint(0, 0xFFFFFFFF)
    operations = [L(['+', v, vInsert + t, -t])]
    constantHavingOperation = {operations[0]}

    # Operation expander
    while len(operations) < desiredOperationCount:
        # Pick random operation
        targetOperation = random.sample(constantHavingOperation, 1)[0]
        targetOperationIndex = operations.index(targetOperation)
        opType, dst, src1, src2 = targetOperation
        assert IsConstExpr(src1) or IsConstExpr(src2)

        # Pick value to flatten
        srcVariable = EUDVariable()
        if IsConstExpr(src1):
            targetOperation[2] = srcVariable
            targetValue = src1
        else:
            targetOperation[3] = srcVariable
            targetValue = src2

        if not (
            IsConstExpr(targetOperation[2]) or
            IsConstExpr(targetOperation[3])
        ):
            constantHavingOperation.remove(targetOperation)

        targetValue = targetValue & 0xFFFFFFFF
        t1 = T2(random.randint(0, 0xFFFFFFFF))
        t2 = random.randint(0, 0xFFFFFFFF)

        optype = random.randint(0, 4)
        if optype == 0:
            operation = ['+', srcVariable, t1, targetValue - t1]
        elif optype == 1:
            operation = ['^', srcVariable, t1, targetValue ^ t1]
        elif optype == 2:
            operation = ['-', srcVariable, targetValue + t1, t1]
        elif optype == 3:
            t2 &= random.randint(0, 0xFFFFFFFF)
            a = t1 & t2
            b = ~t1 & t2
            operation = ['&', srcVariable, a | targetValue, b | targetValue]
        elif optype == 4:
            t2 &= random.randint(0, 0xFFFFFFFF)
            a = t1 | t2
            b = ~t1 | t2
            operation = ['|', srcVariable, a & targetValue, b & targetValue]

        operation = L(operation)

        constantHavingOperation.add(operation)
        operations.insert(random.randint(0, targetOperationIndex), operation)

    return operations


def assignerMerge(op1, op2):
    """ Merge 2 assigner randomly. """
    dst = [1] * len(op1) + [2] * len(op2)
    random.shuffle(dst)

    op1i, op2i = 0, 0
    for i in range(len(dst)):
        if dst[i] == 1:
            dst[i] = op1[op1i]
            op1i += 1
        else:
            dst[i] = op2[op2i]
            op2i += 1

    op1[:] = dst


def writeAssigner(operations):
    """ Write assigner. """
    for optype, dst, src1, src2 in operations:
        if isinstance(src1, int):
            src1 = tryUnT(src1)
        if isinstance(src2, int):
            src2 = tryUnT(src2)

        if optype == '+':
            dst << src1 + src2
        elif optype == '^':
            dst << (src1 ^ src2)
        elif optype == '-':
            dst << src1 - src2
        elif optype == '&':
            dst << (src1 & src2)
        elif optype == '|':
            dst << (src1 | src2)
