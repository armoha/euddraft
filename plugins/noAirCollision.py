from eudplib import *

if settings:
    ep_warn(f"Unused manifest keys in [noAirCollision] plugin: {', '.join(settings)}")

t = [Forward() for _ in range(115)]


def onPluginStart():
    global reph_epd
    reph_epd = f_epdread_epd(EPD(0x6D5CD8))

    s = EUDArray([EPD(x) + 86 for x in t])
    i = EUDVariable()
    if EUDWhile()(i <= 114):
        k = EUDVariable()
        EUDWhile()(k <= 63 * 8)
        EUDBreakIf([i == 114, k >= 15 * 8])
        DoActions(
            SetMemoryEPD(s[i] + k, SetTo, reph_epd),
            reph_epd.AddNumber(1),
            k.AddNumber(8),
        )
        EUDEndWhile()
        DoActions(i.AddNumber(1), k.SetNumber(0))
    EUDEndWhile()


def beforeTriggerExec():
    dummy = reph_epd.getValueAddr() - 8
    for i in range(114):
        t[i] << RawTrigger(actions=[SetMemory(dummy, SetTo, 0) for _ in range(64)])
    t[114] << RawTrigger(actions=[SetMemory(dummy, SetTo, 0) for _ in range(15)])
