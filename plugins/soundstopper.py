'''
dataDumper v2
'''

from eudplib import *


br1, br2 = EUDByteReader(), EUDByteReader()

@EUDFunc
def f_strcmp(s1, s2):
    br1.seekoffset(s1)
    br2.seekoffset(s2)

    if EUDInfLoop()():
        ch1 = br1.readbyte()
        ch2 = br2.readbyte()
        if EUDIf()(ch1 == ch2):
            if EUDIf()(ch1 == 0):
                EUDReturn(0)
            EUDEndIf()
            EUDContinue()
        if EUDElse()():
            EUDReturn(ch1 - ch2)
        EUDEndIf()
    EUDEndInfLoop()


PushTriggerScope()
f_strcmp(0, 0)
PopTriggerScope()


@EUDRegistered
def stopSound(fname):
    fname = u2b(fname)
    fnameDb = Db(fname)

    _stopSound(fnameDb)


@EUDFunc
def _stopSound(fnameDb):
    sfxVector = 0x51A208

    ptr, epd = f_dwepdread_epd(EPD(sfxVector))
    if EUDWhile()(ptr <= 0x7FFFFFFF):
        hMPQFile_epd = f_epdread_epd(epd + 2)
        if EUDIf(f_strcmp(fnameDb, hMPQFile_epd + 8 // 4) == 0):
            f_dwwrite_epd(hMPQFile_epd + (0x11C // 4), 0x7FFFFFFF)
        EUDEndIf()
    EUDEndWhile()
