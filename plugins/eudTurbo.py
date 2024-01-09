from eudplib import *


if settings:
    ep_warn(f"Unused manifest keys in [eudTurbo] plugin: {', '.join(settings)}")


def afterTriggerExec():
    DoActions(SetMemory(0x6509A0, SetTo, 0))
