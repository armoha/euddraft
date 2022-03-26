from eudplib import *
import sys

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
            assert copy not in flags, "Cannot apply both 'copy' and 'unpatchable'"
            for outOffset in outOffsets:
                f_dwpatch_epd(EPD(outOffset), Db(inputData))

        elif copy in flags:
            inputData_db = Db(inputData)
            inputDwordN = (len(inputData) + 3) // 4

            for outOffset in outOffsets:
                addrEPD = f_epdread_epd(EPD(outOffset))
                f_repmovsd_epd(addrEPD, EPD(inputData_db), inputDwordN)

        else:
            DoActions(
                [SetMemory(outOffset, SetTo, Db(inputData)) for outOffset in outOffsets]
            )


def onInit():
    sys.stdout.reconfigure(encoding="utf-8")
    for dataPath, outOffsetStr in settings.items():
        print(' - Loading file "%s"...' % dataPath)
        inputData = open(dataPath, "rb").read()
        flags = set()
        outOffsets = []

        for outOffset in outOffsetStr.split(","):
            outOffset = eval(outOffset)
            if isinstance(outOffset, _Flag):
                flags.add(outOffset)
            else:
                outOffsets.append(outOffset)

        tblOffset = 0x6D5A30
        if tblOffset in outOffsets:
            inputData = AddNullTBL(inputData)

        inputDatas.append((inputData, outOffsets, flags))


def AddNullTBL(tbl):
    tblCount = b2i2(tbl)
    newTbl = i2b2(tblCount)
    tblOffset = 2 * (tblCount + 1)
    if tblCount % 2 == 0:
        tblOffset += 2
    tblContents = []

    for i in range(tblCount):
        k = 2 * (i + 1)
        tblStart = b2i2(tbl, k)
        tblEnd = b2i2(tbl, k + 2)
        if i == tblCount - 1:
            tblEnd = len(tbl)
        tblContent = tbl[tblStart:tblEnd] + b"\0\0\0"
        while len(tblContent) % 4 >= 1:
            tblContent += b"\0"
        newTbl += i2b2(tblOffset)
        tblContents.append(tblContent)
        tblOffset += len(tblContent)

    if tblCount % 2 == 0:
        newTbl += b"\0\0"

    for tblContent in tblContents:
        newTbl += tblContent

    return newTbl


onInit()
