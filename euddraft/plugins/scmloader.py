from eudplib import *


def onPluginStart():
    firstMPQ, firstMPQ_epd = f_dwepdread_epd(EPD(0x1505AE00))
    mapMPQ, mapMPQ_epd = f_dwepdread_epd(EPD(0x1505ADFC))  # Last mpq

    lPrevMPQ, lPrevMPQ_epd = f_dwepdread_epd(mapMPQ_epd)
    DoActions([
        # Detach mapMPQ from dlist
        SetDeaths(lPrevMPQ_epd + 1, SetTo, ~0x1505ADFC, 0),
        SetMemory(0x1505ADFC, SetTo, lPrevMPQ),

        # Insert mapMPQ before firstMPQ
        SetMemory(0x1505AE00, SetTo, mapMPQ),
        SetDeaths(firstMPQ_epd, SetTo, mapMPQ, 0),
        SetDeaths(mapMPQ_epd, SetTo, 0x1505ADFC, 0),
        SetDeaths(mapMPQ_epd + 1, SetTo, firstMPQ, 0)
    ])


print(' - [Warning] Never use this plugin with TEP version of scmloader!')
