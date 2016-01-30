from eudplib import *


LoadMap('basemap.scx')


def main():
    iscript_newindex = 1000

    mtxm_pointer = 0x005993C4
    mtxm_length = 2 * 128 * 128

    # 원본 타일맵 백업
    mtxmaddr, mtxmaddr_epd = f_dwepdread_epd(EPD(mtxm_pointer))
    mtxmbuffer = Db(bytes(2 * 128 * 128))
    f_repmovsd_epd(EPD(mtxmbuffer), mtxmaddr_epd, mtxm_length // 4)
    DoActions(SetMemory(mtxm_pointer, SetTo, mtxmbuffer))

    # iscript 데이터를 원래 mtxm 데이터가 있던 곳에 넣는다.
    iscript_pointer = 0x006D1200

    myiscript_data = open('isc_valkyriefix fixed.bin', 'rb').read()
    myiscript_buffer = Db(myiscript_data)
    f_repmovsd_epd(
        mtxmaddr_epd,
        EPD(myiscript_buffer),
        (len(myiscript_data) + 3) // 4
    )

    DoActions(SetMemory(iscript_pointer, SetTo, mtxmaddr))

    # 발키리 이미지의의 iscript 번호를 변경한다.
    IsId_array = 0x0066EC48
    imageID = 939
    DoActions(SetMemory(IsId_array + imageID * 4, SetTo, iscript_newindex))

    # 끝
    Trigger(
        actions=[
            CreateUnit(2, "Terran Valkyrie", "a", P1),
            CreateUnit(10, "Terran Battlecruiser", "b", P2),
        ],
    )

    if EUDInfLoop():
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('out.scx', main)
