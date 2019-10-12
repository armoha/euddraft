#
# periodic bgm player
#

from eudplib import *

bgmPath = settings["path"]
bgmLength = float(settings["length"])


###############################################################################
# Timing functions

dsttimer = EUDVariable()


@EUDFunc
def f_time():
    return 0xFFFFFFFF - f_dwread_epd(EPD(0x51CE8C))


@EUDFunc
def f_starttimer(duration):
    duration += f_time()
    VProc(duration, [duration.SetDest(dsttimer), duration.AddNumber(-42)])


@EUDFunc
def f_istimerhit():
    ret = EUDVariable()
    if EUDIf()(dsttimer <= f_time()):
        ret << 1
    if EUDElse()():
        ret << 0
    EUDEndIf()
    return ret


###############################################################################


def onPluginStart():
    f_starttimer(0)


def beforeTriggerExec():
    MPQAddFile("bgm", open(bgmPath, "rb").read())

    if EUDIf()(f_istimerhit()):
        oldcp = f_getcurpl()
        localcp = f_getuserplayerid()
        DoActions(
            [
                SetMemory(0x6509B0, SetTo, localcp),
                PlayWAV("bgm"),
                SetMemory(0x6509B0, SetTo, oldcp),
            ]
        )
        f_starttimer(int(1000 * bgmLength))
    EUDEndIf()
