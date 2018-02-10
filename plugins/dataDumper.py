from eudplib import *

inputDatas = []


class _Flag:
    pass


copy = _Flag()
unpatchable = _Flag()


def onPluginStart():
    for inputData, outOffsets, flags in inputDatas:
        if len(outOffsets) == 0:
            continue

        # Reset?
        if unpatchable in flags:
            assert(
                copy not in flags,
                "Cannot apply both 'copy' and 'unpatchable'"
            )
            for outOffset in outOffsets:
                f_dwpatch_epd(EPD(outOffset), Db(inputData))

        elif copy in flags:
            inputData_db = Db(inputData)
            inputDwordN = (len(inputData) + 3) // 4

            for outOffset in outOffsets:
                addrEPD = f_epdread_epd(EPD(outOffset))
                f_repmovsd_epd(addrEPD, EPD(inputData_db), inputDwordN)

        else:
            DoActions([
                SetMemory(outOffset, SetTo, Db(inputData))
                for outOffset in outOffsets])


def onInit():
    for dataPath, outOffsetStr in settings.items():
        print(' - Loading file \"%s\"...' % dataPath)
        inputData = open(dataPath, 'rb').read()
        flags = set()
        outOffsets = []

        for outOffset in outOffsetStr.split(','):
            outOffset = eval(outOffset)
            if isinstance(outOffset, _Flag):
                flags.add(outOffset)
            else:
                outOffsets.append(outOffset)

        inputDatas.append((inputData, outOffsets, flags))


onInit()
