from eudplib import *


def connectDList(el_start, el_end, itemSize, itemN):
    dataDb = Db(bytes(itemSize * itemN))

    a1, a2 = Forward(), Forward()
    if EUDLoopN()(itemN):
        DoActions([
            a1 << SetMemory(dataDb, SetTo, dataDb - itemSize),
            a2 << SetMemory(dataDb + 4, SetTo, dataDb + itemSize),
            SetMemory(a1 + 16, Add, itemSize // 4),
            SetMemory(a1 + 20, Add, itemSize),
            SetMemory(a2 + 16, Add, itemSize // 4),
            SetMemory(a2 + 20, Add, itemSize),
        ])
    EUDEndLoopN()

    DoActions([
        SetMemory(el_start, SetTo, dataDb),
        SetMemory(dataDb, SetTo, 0),
        SetMemory(el_end, SetTo, dataDb + itemSize * (itemN - 1)),
        SetMemory(dataDb + itemSize * (itemN - 1) + 4, SetTo, 0)
    ])


def onPluginStart():
    connectDList(0x64EED8, 0x64EEDC, 112, 8192)  # 총알 갯수 패치
    connectDList(0x63FE30, 0x63FE34, 36, 65536)  # 스프라이트 갯수 패치
    connectDList(0x57EB68, 0x57EB70, 64, 65536)  # 이미지 갯수 패치


def afterTriggerExec():
    DoActions(SetMemory(0x64DEBC, SetTo, 40))
