'''
grpInjector v1
'''


from eudplib import *


def onPluginStart():
    try:
        for grpPath, outOffsets in grpList:
            inputGrp = EUDGrp(grppath)
            if isinstance(outOffsets, int):
                DoActions(SetMemory(outOffsets, SetTo, inputGrp))
            else:
                DoActions([
                    SetMemory(outOffset, SetTo, inputGrp)
                    for outOffset in outOffsets])

    except KeyError as e:
        raise RuntimeError('No argument \'grplist\'', e)
