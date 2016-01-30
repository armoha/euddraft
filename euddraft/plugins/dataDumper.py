'''
dataDumper v2
'''

from eudplib import *

inputDatas = []


def onPluginStart():
    for inputData, outOffsets in inputDatas:
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
