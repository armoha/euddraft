'''
unpatcher
'''

from eudplib import *

unpatched = EUDVariable()
resetCond = None


def beforeTriggerExec():
    if resetCond:
        if EUDIf()([resetCond, unpatched == 0]):
            f_unpatchall()
            unpatched << 1
        EUDEndIf()


def onInit():
    global resetCond
    resetCond = eval(settings['resetCond'])


onInit()
