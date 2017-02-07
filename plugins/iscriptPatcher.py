'''
iscript patcher

iscript Data shouldn't be unpatched untill game ends, cause unpatching can
cause sc crash.


This plugin works with following algorithm.


- iscript data is at 6D1200
- MTXM data is at 5993C4 (Fixed 64K)

1. backup mtxm data to internal space
2. copy custom iscript -> mtxm memory
3. set current iscript pointer to mtxm memory
4. set mtxm pointer to internal space

STR is deallocated after MTXM, so sc won't cause any access violation error
while deallocating mtxm, even if we don't use keepSTR plugin.
'''

from eudplib import *

unpatched = EUDVariable()
newIscript = None


def onPluginStart():
    newIscriptDb = Db(newIscript)
    mtxmBackup = Db(65536)

    oldMtxm, oldMtxm_epd = f_dwepdread_epd(EPD(0x5993C4))

    f_repmovsd_epd(EPD(mtxmBackup), oldMtxm_epd, 65536 // 4)
    f_repmovsd_epd(oldMtxm_epd, EPD(newIscriptDb), len(newIscript) // 4)
    DoActions([
        SetMemory(0x6D1200, SetTo, oldMtxm),
        SetMemory(0x5993C4, SetTo, mtxmBackup)
    ])


def onInit():
    global newIscript
    newIscript = open(settings['iscript'], 'rb').read()

onInit()
