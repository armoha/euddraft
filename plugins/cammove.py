# Cammove v3
#
# Algorithm by matbing(sksljh2091@naver.com)
# Pluginified by trgk(phu54321@naver.com)
#
# 2015-12-08 : Initial Release
# 2016-12-09 : Some crash bug fixed, Zero scrolling while camera is following
# 2017-12-20 : Overflow bug fixed, add widescreen support
#


from eudplib import *

cammoveLoc = GetLocationIndex('cammoveLoc')
inertia = int(settings.get('inertia', 5))
maxspeed = int(settings.get('maxspeed', 48))
target = GetLocationIndex(settings['targetloc'])


def onPluginStart():
    DoActions([
        SetMemory(0x58DC60 + 20 * cammoveLoc + 0x0, SetTo, 0),
        SetMemory(0x58DC60 + 20 * cammoveLoc + 0x4, SetTo, 0),
        SetMemory(0x58DC60 + 20 * cammoveLoc + 0x8, SetTo, 640),
        SetMemory(0x58DC60 + 20 * cammoveLoc + 0xC, SetTo, 384),
    ])


@EUDFunc
def sgnAbs(x):
    if EUDIf()(x >= 0x80000000):
        EUDReturn(-1, -x)
    if EUDElse()():
        EUDReturn(1, x)
    EUDEndIf()


def getTicks():
    return f_dwread_epd_safe(EPD(0x57F23C))


lastTick = EUDVariable(-1)
# scrollData = Db(52)
# blank = Db(b'\0' * 52)
screenX = EUDVariable(640)


@EUDFunc
def afterTriggerExec():
    if EUDIf()(Memory(0x57F0B4, Exactly, 0)):
        EUDReturn()
    EUDEndIf()

    if EUDIf()([Switch('cammove', Set)]):
        currentTick = getTicks()
        if EUDIf()(lastTick == -1):  # Just started following
            lastTick << currentTick
            # f_memcpy(scrollData, 0x513B68, 49)
            # f_memcpy(0x513B68, blank, 49)
        EUDEndIf()

        prevCamX = f_dwread_epd_safe(EPD(0x62848C))  # 화면 좌표
        prevCamY = f_dwread_epd_safe(EPD(0x6284A8))

        DoActions(MoveLocation(cammoveLoc + 1, 'Map Revealer', P9, target + 1))
        locx = f_dwread_epd(EPD(0x58DC60 + 20 * cammoveLoc + 0x0))
        locy = f_dwread_epd(EPD(0x58DC60 + 20 * cammoveLoc + 0x4))

        if inertia == 0:
            dstx, dsty = locx, locy

        else:
            # We use fixed point arithmetics here
            fpQ = 256

            dx = (locx - prevCamX)
            dy = (locy - prevCamY)

            dstx, dsty = EUDCreateVariables(2)

            if EUDIf()([dx == 0, dy == 0]):
                dstx << locx
                dsty << locy

            if EUDElse()():
                dx_sgn, dxabs = sgnAbs(dx)
                dy_sgn, dyabs = sgnAbs(dy)

                dt = (currentTick - lastTick) * fpQ // 24

                # Calculating norm of vector (dx, dy), while preventing
                # potential overflows
                d = EUDVariable()
                if EUDIf()([dxabs <= 100, dyabs <= 100]):
                    # Better accuracy
                    d << f_sqrt(fpQ * fpQ * (dxabs * dxabs + dyabs * dyabs))
                if EUDElse()():
                    # Sacrifice accuracy to prevent overflowing
                    d << fpQ * f_sqrt(20000)
                EUDEndIf()

                newd = EUDVariable()
                newd << (d * fpQ * fpQ // (d * dt // inertia + fpQ * fpQ))
                if EUDIf()(d - newd >= maxspeed * fpQ):
                    newd << d - maxspeed * fpQ
                EUDEndIf()

                newdx, newdy = EUDCreateVariables(2)
                newdx = dxabs * (fpQ * fpQ) // d * newd // (fpQ * fpQ)
                newdy = dyabs * (fpQ * fpQ) // d * newd // (fpQ * fpQ)

                dstx << locx - dx_sgn * newdx
                dsty << locy - dy_sgn * newdy
            EUDEndIf()

        dstTileX = dstx // 32
        dstTileY = dsty // 32
        # dstTileXY = dstTileY * 0x10000 + dstTileX

        DoActions([
            SetCurrentPlayer(f_getuserplayerid()),
            SetMemory(0x58DC60 + 20 * cammoveLoc + 0x0, SetTo, dstx),
            SetMemory(0x58DC60 + 20 * cammoveLoc + 0x4, SetTo, dsty),
            SetMemory(0x58DC60 + 20 * cammoveLoc + 0x8, SetTo, dstx + screenX),
            SetMemory(0x58DC60 + 20 * cammoveLoc + 0xC, SetTo, dsty + 384),
            CenterView(cammoveLoc + 1),
            # SetMemory(0x62848C, SetTo, dstx),  화면 좌표: 리마 호환 X
            # SetMemory(0x6284A8, SetTo, dsty),
            SetMemory(0x628498, SetTo, dstTileX),
            SetMemory(0x6284AC, SetTo, dstTileY),
            # SetMemory(0x57F1D0, SetTo, dstTileXY),
        ])

        '''for i in EUDLoopRange(332581, 332881):  이미지 갱신: 리마 호환 X
            f_dwwrite_epd(i, 0x01010101)'''

        postCamX = f_dwread_epd_safe(EPD(0x62848C))  # 화면 X 좌표
        screenX << 2 * dstx + screenX - 2 * postCamX

        lastTick << currentTick

    if EUDElse()():
        if EUDIfNot()(lastTick == -1):
            lastTick << -1
            # f_memcpy(0x513B68, scrollData, 49)
        EUDEndIf()
    EUDEndIf()
