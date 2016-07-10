from eudplib import *


def afterTriggerExec():
    DoActions(SetMemory(0x6509A0, SetTo, 0))
