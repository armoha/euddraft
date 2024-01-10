# Cammove v3
#
# Algorithm by matbing(sksljh2091@naver.com)
# Pluginified by trgk(phu54321@naver.com)
#
# 2015-12-08 : Initial Release
# 2016-12-09 : Some crash bug fixed, Zero scrolling while camera is following
# 2017-12-20 : Overflow bug fixed, add widescreen support
# 2021-04-15 : Fixed off-by-one errors


from eudplib import *

cammoveLoc = GetLocationIndex("cammoveLoc")
inertia = int(settings.get("inertia", 5))
maxspeed = int(settings.get("maxspeed", 48))
target = GetLocationIndex(settings["targetloc"])

supported_keys = ("inertia", "maxspeed", "targetloc")
unsupported_keys = []
for key in settings:
    if key not in supported_keys:
        unsupported_keys.append(key)
if unsupported_keys:
    ep_warn(f"Unused manifest keys in [cammove] plugin: {', '.join(unsupported_keys)}")


def onPluginStart():
    f_setloc(cammoveLoc, 0, 0, 640, 384)


@EUDFunc
def sgnAbs(x):
    if EUDIf()(x >= 0x80000000):
        EUDReturn(-1, -x)
    if EUDElse()():
        EUDReturn(1, x)
    EUDEndIf()


lastTick = EUDVariable(-1)
screenX = EUDVariable(640)


@EUDFunc
def afterTriggerExec():
    if EUDIf()(Memory(0x57F0B4, Exactly, 0)):
        EUDReturn()
    EUDEndIf()

    if EUDIf()(Switch("cammove", Set)):
        currentTick = f_getgametick()
        if EUDIf()(lastTick == -1):  # Just started following
            lastTick << currentTick
        EUDEndIf()

        prevCamX = f_dwread(0x62848C)  # 화면 좌표
        prevCamY = f_dwread(0x6284A8)

        DoActions(MoveLocation(cammoveLoc, "Map Revealer", P9, target))
        locx, locy = f_getlocTL(cammoveLoc)

        if inertia == 0:
            dstx, dsty = locx, locy

        else:
            # We use fixed point arithmetics here
            fpQ = 256
            fpQ2 = fpQ * fpQ

            dx = locx - prevCamX
            dy = locy - prevCamY

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
                    d << f_sqrt(fpQ2 * (dxabs * dxabs + dyabs * dyabs))
                if EUDElse()():
                    # Sacrifice accuracy to prevent overflowing
                    d << fpQ * f_sqrt(20000)
                EUDEndIf()

                newd = EUDVariable()
                newd << (d * fpQ2 // (d * dt // inertia + fpQ2))
                if EUDIf()(d - newd >= maxspeed * fpQ):
                    newd << d - maxspeed * fpQ
                EUDEndIf()

                newdx, newdy = EUDCreateVariables(2)
                newdx = dxabs * fpQ2 // d * newd // fpQ2
                newdy = dyabs * fpQ2 // d * newd // fpQ2

                dstx << locx - dx_sgn * newdx
                dsty << locy - dy_sgn * newdy
            EUDEndIf()

        dstTileX = dstx // 32
        dstTileY = dsty // 32

        locepd = EPD(0x58DC4C) + 5 * cammoveLoc
        SeqCompute(
            [
                (EPD(0x6509B0), SetTo, f_getuserplayerid()),
                (locepd, SetTo, dstx),
                (locepd + 1, SetTo, dsty),
                (locepd + 2, SetTo, dstx + screenX),
                (locepd + 3, SetTo, dsty + 384),
            ]
        )
        f_setcurpl2cpcache(
            [dstTileX, dstTileY],
            [
                CenterView(cammoveLoc),
                dstTileX.SetDest(EPD(0x628498)),
                dstTileY.SetDest(EPD(0x6284AC)),
            ],
        )

        postCamX = f_dwread(0x62848C)  # 화면 X 좌표
        screenX << (dstx + dstx) + screenX - (postCamX + postCamX)

        lastTick << currentTick

    if EUDElseIfNot()(lastTick == -1):
        lastTick << -1
    EUDEndIf()
