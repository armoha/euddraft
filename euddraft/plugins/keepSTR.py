'''
맵 플레이가 끝난 다음에도 STR 단락이 해제되지 않도록 합니다.

원리는 ..mo 를 변형해서 SMemFree가 이 메모리를 해제하지 못하도록 하는겁니다.
'''

from eudplib import *


def onPluginStart():
    strOffsetEPD = f_epdread_epd(EPD(0x5993D4))
    DoActions(SetDeaths(strOffsetEPD - 1, Add, 0x01000000, 0))
