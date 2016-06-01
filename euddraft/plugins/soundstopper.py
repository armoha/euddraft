from eudplib import *


@EUDRegistered
def stopSound(fname):
    fname = u2b(fname)
    fnameDb = Db(fname)

    _stopSound(fnameDb)


@EUDFunc
def _stopSound(fnameDb):
    sfxVector = 0x51A208

    ptr, epd = f_dwepdread_epd(EPD(sfxVector + 8))
    if EUDWhile()(ptr <= 0x7FFFFFFF):
        hMPQFile, hMPQFile_epd = f_dwepdread_epd(epd + 2)
        if EUDIf()(f_strcmp(fnameDb, hMPQFile + 8) == 0):
            f_dwwrite_epd(hMPQFile_epd + (0x11C // 4), 0x7FFFFFFF)
        EUDEndIf()
        SetVariables([ptr, epd], f_dwepdread_epd(epd + 1))
    EUDEndWhile()
