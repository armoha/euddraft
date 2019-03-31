#
# periodic bgm player
#

from eudplib import *


bgmPath = settings['path']
bgmLength = float(settings['length'])


###############################################################################
# Timing functions

dsttimer = EUDVariable()


@EUDFunc
def f_time():
    return 0xFFFFFFFF - f_dwread_epd(EPD(0x51CE8C))


@EUDFunc
def f_starttimer(duration):
    dsttimer << f_time() + duration - 42


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
    MPQAddFile("bgm", open(bgmPath, 'rb').read())

    if EUDIf()(f_istimerhit()):
        oldcp = f_getcurpl()
        DoActions([
            [
                SetCurrentPlayer(player),
                PlayWAV("bgm"),
            ] for player in range(8)
        ] + [SetCurrentPlayer(oldcp)])
        f_starttimer(int(1000 * bgmLength))
    EUDEndIf()
