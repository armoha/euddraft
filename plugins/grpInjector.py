'''
grpInjector v1
'''


from eudplib import *

inputGrps = []


def onPluginStart():
    for inputGrp, outOffsets in inputGrps:
        DoActions([
            SetMemory(outOffset, SetTo, inputGrp)
            for outOffset in outOffsets])


def onInit():
    for grpPath, outOffsets in settings.items():
        print(' - Loading file \"%s\"...' % grpPath)
        inputGrp = EUDGrp(grpPath)
        outOffsets = map(lambda x: eval(x), outOffsets.split(','))
        inputGrps.append((inputGrp, outOffsets))

onInit()
