from eudplib import *


def onPluginStart():
    global reph_epd
    reph_epd = f_epdread_epd(EPD(0x6D5CD8))


def beforeTriggerExec():
    m = EUDVariable()
    m << reph_epd
    t = EUDLightVariable()
    t << 29244 // 4

    if EUDWhile()(t >= 1):
        DoActions([
            t.SubtractNumber(1),
            SetDeaths(m, SetTo, 0, 0),
            m.AddNumber(1)
        ])
    EUDEndWhile()
