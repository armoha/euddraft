'''
dataDumper v2
'''

from eudplib import *

inputDatas = []


def onPluginStart():
    for inputData, outOffsets in inputDatas:
        if len(outOffsets) == 0:
            continue

        # Reset?
        if isinstance(outOffsets[-1], bool):
            doReset = bool(outOffsets[-1])
            outOffsets = outOffsets[:-1]
        else:
            doReset = False

        if doReset:
            for outOffset in outOffsets:
                f_dwpatch_epd(EPD(outOffset), inputData)

        else:
            DoActions([
                SetMemory(outOffset, SetTo, inputData)
                for outOffset in outOffsets])


def onInit():
    for dataPath, outOffsets in settings.items():
        print(' - Loading file \"%s\"...' % dataPath)
        inputData = Db(open(dataPath, 'rb').read())
        outOffsets = map(lambda x: eval(x), outOffsets.split(','))
        inputDatas.append((inputData, outOffsets))

onInit()
