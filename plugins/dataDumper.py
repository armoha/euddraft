from eudplib import *


def onPluginStart():
    try:
        for dataPath, outOffsets in dataList:
            inputData = Db(open(datapath, 'rb').read())
            if isinstance(outOffsets, int):
                DoActions(SetMemory(outOffsets, SetTo, inputData))
            else:
                DoActions([
                    SetMemory(outOffset, SetTo, inputData)
                    for outOffset in outOffsets])

    except KeyError as e:
        raise RuntimeError('No argument \'datalist\'', e)
