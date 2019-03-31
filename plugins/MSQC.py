# -*- coding: utf-8 -*-
import re
from math import ceil

from eudplib import *

# Default: Valkyrie, Location 1, P11
QCUnit, QCLoc, QCPlayer = 58, 0, 10
QCX, QCY = 128, 128  # (4, 4)
QCDebug = 1
qc_conds, qc_rets, v_conds, v_rets, deathsUnits = [], [], [], [], set()

KeyArray, KeyOffset = EUDArray(8), set()
MouseArray, MouseOffset = EUDArray(1), set()
cmpScreenX, cmpMouseX, cmpScreenY, cmpMouseY = [Forward() for i in range(4)]

MouseButtonDict = {
    'L': 2,
    'LEFT': 2,
    'R': 8,
    'RIGHT': 8,
    'M': 32,
    'MIDDLE': 32,
}
KeyCodeDict = {
    'LBUTTON': 0x01, 'RBUTTON': 0x02, 'CANCEL': 0x03, 'MBUTTON': 0x04,
    'XBUTTON1': 0x05, 'XBUTTON2': 0x06, 'BACK': 0x08, 'TAB': 0x09,
    'CLEAR': 0x0C, 'ENTER': 0x0D, 'NX5': 0x0E, 'SHIFT': 0x10,
    'LCTRL': 0x11, 'LALT': 0x12, 'PAUSE': 0x13, 'CAPSLOCK': 0x14,
    'RALT': 0x15, 'JUNJA': 0x17, 'FINAL': 0x18, 'RCTRL': 0x19, 'ESC': 0x1B,
    'CONVERT': 0x1C, 'NONCONVERT': 0x1D, 'ACCEPT': 0x1E, 'MODECHANGE': 0x1F,
    'SPACE': 0x20, 'PGUP': 0x21, 'PGDN': 0x22, 'END': 0x23, 'HOME': 0x24,
    'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27, 'DOWN': 0x28,  # ARROW keys
    'SELECT': 0x29, 'PRINTSCREEN': 0x2A, 'EXECUTE': 0x2B, 'SNAPSHOT': 0x2C,
    'INSERT': 0x2D, 'DELETE': 0x2E, 'HELP': 0x2F,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46,
    'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C,
    'M': 0x4D, 'N': 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52,
    'S': 0x53, 'T': 0x54, 'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58,
    'Y': 0x59, 'Z': 0x5A,
    'LWIN': 0x5B, 'RWIN': 0x5C, 'APPS': 0x5D, 'SLEEP': 0x5F,
    'NUMPAD0': 0x60, 'NUMPAD1': 0x61, 'NUMPAD2': 0x62, 'NUMPAD3': 0x63,
    'NUMPAD4': 0x64, 'NUMPAD5': 0x65, 'NUMPAD6': 0x66, 'NUMPAD7': 0x67,
    'NUMPAD8': 0x68, 'NUMPAD9': 0x69,
    'NUMPAD*': 0x6A, 'NUMPAD+': 0x6B, 'SEPARATOR': 0x6C, 'NUMPAD-': 0x6D,
    'NUMPAD.': 0x6E, 'NUMPAD/': 0x6F,
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74,
    'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79,
    'F11': 0x7A, 'F12': 0x7B, 'F13': 0x7C, 'F14': 0x7D, 'F15': 0x7E,
    'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82, 'F20': 0x83,
    'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87,
    'NUMLOCK': 0x90, 'SCROLL': 0x91, 'OEM_FJ_JISHO': 0x92,
    'OEM_FJ_MASSHOU': 0x93, 'OEM_FJ_TOUROKU': 0x94,
    'OEM_FJ_LOYA': 0x95, 'OEM_FJ_ROYA': 0x96,
    'LSHIFT': 0xA0, 'RSHIFT': 0xA1, 'LCONTROL': 0xA2, 'RCONTROL': 0xA3,
    'LMENU': 0xA4, 'RMENU': 0xA5,
    'BROWSER_BACK': 0xA6, 'BROWSER_FORWARD': 0xA7, 'BROWSER_REFRESH': 0xA8,
    'BROWSER_STOP': 0xA9, 'BROWSER_SEARCH': 0xAA, 'BROWSER_FAVORITES': 0xAB,
    'BROWSER_HOME': 0xAC,
    'VOLUME_MUTE': 0xAD, 'VOLUME_DOWN': 0xAE, 'VOLUME_UP': 0xAF,
    'MEDIA_NEXT_TRACK': 0xB0, 'MEDIA_PLAY_PAUSE': 0xB3,
    'MEDIA_PREV_TRACK': 0xB1, 'MEDIA_STOP': 0xB2,
    'LAUNCH_MAIL': 0xB4, 'LAUNCH_MEDIA_SELECT': 0xB5, 'LAUNCH_APP1': 0xB6,
    'LAUNCH_APP2': 0xB7,
    'SEMICOLON': 0xBA, '=': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE, '/': 0xBF,
    '`': 0xC0, 'ABNT_C1': 0xC1, 'ABNT_C2': 0xC2,
    '[': 0xDB, '|': 0xDC, ']': 0xDD, "'": 0xDE, 'OEM_8': 0xDF,
    'OEM_AX': 0xE1, 'OEM_102': 0xE2, 'ICO_HELP': 0xE3, 'ICO_00': 0xE4,
    'PROCESSKEY': 0xE5, 'ICO_CLEAR': 0xE6, 'PACKET': 0xE7, 'OEM_RESET': 0xE9,
    'OEM_JUMP': 0xEA, 'OEM_PA1': 0xEB, 'OEM_PA2': 0xEC, 'OEM_PA3': 0xED,
    'OEM_WSCTRL': 0xEE, 'OEM_CUSEL': 0xEF,
    'OEM_ATTN': 0xF0, 'OEM_FINISH': 0xF1, 'OEM_COPY': 0xF2, 'OEM_AUTO': 0xF3,
    'OEM_ENLW': 0xF4, 'OEM_BACKTAB': 0xF5, 'ATTN': 0xF6, 'CRSEL': 0xF7,
    'EXSEL': 0xF8, 'EREOF': 0xF9, 'PLAY': 0xFA, 'ZOOM': 0xFB, 'NONAME': 0xFC,
    'PA1': 0xFD, 'OEM_CLEAR': 0xFE, '_NONE_': 0xFF
}


def EncPlayer(s):  # str to int (Player)
    PlayerDict = {
        'p1': 0, 'p2': 1, 'p3': 2, 'p4': 3, 'p5': 4, 'p6': 5,
        'p7': 6, 'p8': 7, 'p9': 8, 'p10': 9, 'p11': 10, 'p12': 11,
        'player1': 0, 'player2': 1, 'player3': 2, 'player4': 3,
        'player5': 4, 'player6': 5, 'player7': 6, 'player8': 7,
        'player9': 8, 'player10': 9, 'player11': 10, 'player12': 11,
        'neutral': 11,
        'currentplayer': 13,
        'foes': 14, 'allies': 15, 'neutralplayers': 16,
        'allplayers': 17,
        'force1': 18, 'force2': 19, 'force3': 20, 'force4': 21,
        'nonalliedvictoryplayers': 26
    }
    if s.lower() in PlayerDict:
        return PlayerDict[s.lower()]
    else:
        return int(s)


def RegisterKeyOffset(k):
    try:
        offset = KeyCodeDict[k.upper()]
    except (KeyError):
        raise EPError("%s doesn't exist in VirtualKeyCode." % (k))
    else:
        KeyOffset.add(offset)


def RegisterMouseOffset(k):
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        MouseOffset.add(v)


def KeyUpdate():
    for offset in KeyOffset:
        m = 256 ** (offset % 4)
        n = 2 ** (offset % 32)
        RawTrigger(
            conditions=[  # KeyDown
                MemoryX(0x596A18 + offset, Exactly, m, m),
                MemoryX(KeyArray + offset // 8, Exactly, 0, n)
            ],
            actions=SetMemoryX(KeyArray + offset // 8, SetTo, n, n)
        )
        RawTrigger(
            conditions=[  # KeyUp
                MemoryX(0x596A18 + offset, Exactly, 0, m),
                MemoryX(KeyArray + offset // 8, Exactly, n, n)
            ],
            actions=SetMemoryX(KeyArray + offset // 8, SetTo, 0, n)
        )


def KeyDown(k):
    try:
        offset = KeyCodeDict[k.upper()]
    except (KeyError):
        raise EPError("%s doesn't exist in VirtualKeyCode." % (k))
    else:
        KeyOffset.add(offset)
        m = 256 ** (offset % 4)
        n = 2 ** (offset % 32)
        return [  # KeyDown
            MemoryX(0x596A18 + offset, Exactly, m, m),
            MemoryX(KeyArray + offset // 8, Exactly, 0, n)
        ]


def KeyUp(k):
    try:
        offset = KeyCodeDict[k.upper()]
    except (KeyError):
        raise EPError("%s doesn't exist in VirtualKeyCode." % (k))
    else:
        KeyOffset.add(offset)
        m = 256 ** (offset % 4)
        n = 2 ** (offset % 32)
        return [  # KeyUp
            MemoryX(0x596A18 + offset, Exactly, 0, m),
            MemoryX(KeyArray + offset // 8, Exactly, n, n)
        ]


def KeyPress(k):
    try:
        offset = KeyCodeDict[k.upper()]
    except (KeyError):
        raise EPError("%s doesn't exist in VirtualKeyCode." % (k))
    else:
        m = 256 ** (offset % 4)
        return MemoryX(0x596A18 + offset, Exactly, m, m)


def MouseUpdate():
    for k in MouseOffset:
        RawTrigger(
            conditions=[  # MouseDown
                MemoryX(0x6CDDC0, Exactly, k, k),
                MemoryX(MouseArray, Exactly, 0, k)
            ],
            actions=SetMemoryX(MouseArray, SetTo, k, k)
        )
        RawTrigger(
            conditions=[  # MouseUp
                MemoryX(0x6CDDC0, Exactly, 0, k),
                MemoryX(MouseArray, Exactly, k, k)
            ],
            actions=SetMemoryX(MouseArray, SetTo, 0, k)
        )


def MouseDown(k):
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        MouseOffset.add(v)
        return [  # MouseDown
            MemoryX(0x6CDDC0, Exactly, v, v),
            MemoryX(MouseArray, Exactly, 0, v)
        ]


def MouseUp(k):
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        MouseOffset.add(v)
        return [  # MouseUp
            MemoryX(0x6CDDC0, Exactly, 0, v),
            MemoryX(MouseArray, Exactly, v, v)
        ]


def MousePress(k):
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        return MemoryX(0x6CDDC0, Exactly, v, v)


def NotTyping():
    return Memory(0x68C144, Exactly, 0)


@EUDFunc
def MouseMoved():
    ret = EUDVariable()
    ret << 1

    RawTrigger(
        conditions=[
            cmpScreenX << Memory(0x62848C, Exactly, 0),
            cmpMouseX << Memory(0x6CDDC4, Exactly, 0),
            cmpScreenY << Memory(0x6284A8, Exactly, 0),
            cmpMouseY << Memory(0x6CDDC8, Exactly, 0),
        ],
        actions=ret.SetNumber(0),
    )

    return ret


def onInit():
    # get map size & human player
    chkt = GetChkTokenized()
    dim, ownr = chkt.getsection('DIM'), chkt.getsection('OWNR')
    global bit_xy, map_x, map_y
    dim_x, dim_y = b2i2(dim[0:2]), b2i2(dim[2:4])
    bit_x, bit_y = dim_x.bit_length() + 2, dim_y.bit_length() + 2
    bit_xy = [2**(16+y) for y in range(bit_y, 15, -1)] + [2**x for x in range(bit_x, -1, -1)]
    map_x, map_y = (dim_x - 1).bit_length() + 4, (dim_y - 1).bit_length() + 4
    map_xy = [2**(16+y) for y in range(map_y, 15, -1)] + [2**x for x in range(map_x, -1, -1)]

    global humans, QCUnit, QCLoc, QCPlayer, QCX, QCY, QCDebug
    global qc_conds, qc_rets, v_conds, v_rets, QCCount
    humans = [p for p in range(8) if ownr[p] == 6]

    # simple parsing settings
    for k, v in settings.items():

        def check_settings():
            settings_dict = {
                "QCUnit": (QCUnit, EncodeUnit, "unit"),
                "QCLoc": (QCLoc, GetLocationIndex, "location"),
                "QCPlayer": (QCPlayer, EncPlayer, "player"),
            }
            for s, var_encf_err in settings_dict.items():
                if k == s:
                    var, encf, err = var_encf_err
                    try:
                        var = encf(v)
                    except EPError:
                        try:
                            var = int(v, 0)
                        except ValueError:
                            raise EPError("{} should be {} or number.".format(s, err))
                    return True
            return False

        if check_settings() is True:
            continue
        elif k == "QC_XY":
            coord = v.split(',')
            try:
                QCX, QCY = int(coord[0], 0), int(coord[1], 0)
            except (IndexError, ValueError):
                raise EPError("QC_XY should be two numbers.")
            continue
        elif k == "QCDebug":
            if v.lower() == "true":
                QCDebug = True
            elif v.lower() == "false":
                QCDebug = False
            else:
                try:
                    QCDebug = int(v, 0)
                except ValueError:
                    raise EPError("QCDebug should be True/False or non-zero, 0.")
            continue

        con_final, ret_final = [], None

        # parse conditions
        con_count = 0
        conds = [c.strip() for c in k.split(";")]
        for cond in conds:
            if cond == "마우스" or cond.lower() == "mouse":
                try:
                    mouse_loc = GetLocationIndex(v)
                except EPError:
                    try:
                        mouse_loc = int(v, 0)
                    except ValueError:
                        raise EPError("MouseLocation should be location or index.")
                con_final.append(MouseMoved())
                ret_final = ["mouse", mouse_loc]

            elif cond[:8] == "KeyDown(" and cond[-1] == ")":
                RegisterKeyOffset(cond[8:-1])
                con_final.append(KeyDown(cond[8:-1]))
            elif cond[:6] == "KeyUp(" and cond[-1] == ")":
                RegisterKeyOffset(cond[6:-1])
                con_final.append(KeyUp(cond[6:-1]))
            elif cond[:9] == "KeyPress(" and cond[-1] == ")":
                con_final.append(KeyPress(cond[9:-1]))
            elif cond.upper() in KeyCodeDict:
                RegisterKeyOffset(cond)
                con_final.append(KeyDown(cond))

            elif cond[:10] == "MouseDown(" and cond[-1] == ")":
                RegisterMouseOffset(cond[10:-1])
                con_final.append(MouseDown(cond[10:-1]))
            elif cond[:8] == "MouseUp(" and cond[-1] == ")":
                RegisterMouseOffset(cond[8:-1])
                con_final.append(MouseUp(cond[8:-1]))
            elif cond[:11] == "MousePress(" and cond[-1] == ")":
                con_final.append(MousePress(cond[11:-1]))

            elif cond.lower() == "nottyping":
                con_final.append(NotTyping())

            else:
                c = [con.strip() for con in cond.split(",")]
                if c[0].lower() == "xy":
                    ret = [r.strip() for r in v.split(",")]
                    try:
                        ret_final = ["xy", c[1], c[2], ret[0], ret[1]]
                    except IndexError:
                        ret_final = ["xy", c[1], v]
                        DU = [v]
                    else:
                        DU = [ret[1], ret[0]]
                    for i, du in enumerate(DU):
                        try:
                            deaths_unit = EncodeUnit(du)
                        except EPError:
                            try:
                                deaths_unit = int(du, 0)
                            except ValueError:
                                continue
                            else:
                                deathsUnits.add(deaths_unit)
                        else:
                            deathsUnits.add(deaths_unit)
                        ret_final[-1-i] = deaths_unit
                elif re.fullmatch(r'0[xX][0-9a-fA-F]+', c[0]):
                    try:
                        ptr, mod, val = int(c[0], 0), eval(c[1]), int(c[2], 0)
                    except (IndexError, SyntaxError):
                        ptr, val = int(c[0], 0), int(c[1], 0)
                        con_final.append(MemoryX(ptr, Exactly, val, val))
                    else:
                        con_final.append(Memory(ptr, mod, val))
                else:
                    con_final.append(cond)

        ep_assert(len(con_final) >= 1, "At least 1 condition is needed.")

        # parse returns
        if ret_final is None:
            ret = [r.strip() for r in v.split(",")]
            try:
                increment = int(ret[1], 0)
            except ValueError:
                raise EPError("Value to add deaths/array must be number.")

            try:
                death_unit = EncodeUnit(ret[0])
            except EPError:
                try:
                    death_unit = int(ret[0], 0)
                except ValueError:
                    ret_final = ["array", ret[0], increment]
                else:
                    deathsUnits.add(death_unit)
                    ret_final = ["deaths", death_unit, increment]
            else:
                deathsUnits.add(death_unit)
                ret_final = ["deaths", death_unit, increment]
            qc_conds.append(con_final)
            qc_rets.append(ret_final)
        else:
            v_conds.append(con_final)
            v_rets.append(ret_final)

    QCCount = len(v_rets) + ceil(len(qc_rets) / len(bit_xy))
    ep_assert(QCCount >= 1, "Must add desync cond : sync return pair")
    print("[MSQC] map size: {}x{}, {} men × {} QCUnits".format(dim_x, dim_y, len(humans), QCCount))


onInit()

QC_EPDs = [  # QCUnits = QCCount * humans
    EUDVArray(QCCount)([EPD(0x59CFDE)] * QCCount)
    if p in humans else 0 for p in range(8)
]  # ptr, epd of QC_EPDs. ArrayPtr is used in nextptr modification
ArrayPTRs = PVariable(QC_EPDs)
ArrayEPDs = PVariable([EPD(x) for x in QC_EPDs])
# detect if QCUnit is selected (0x6284B8)
MyQCptrs = [Forward() for _ in range(QCCount)]
# used in SendQC::QGC_Select
MyQCalphaids = [Forward() for _ in range(QCCount)]
cp = EUDVariable()
if QCDebug:
    QCShutdown = EUDLightVariable()
f_mapXread_epd = f_readgen_epd(2**(map_x + 1) - 1, (0, lambda x: x))
f_mapYread_epd = f_readgen_epd(2**(map_y + 1) - 1, (0, lambda y: y << 16))
f_screenXread_epd = f_readgen_epd(0x3FF, (0, lambda x: x))
f_screenYread_epd = f_readgen_epd(0x1FF, (0, lambda y: y << 16))
mapMask = 2**(map_x + 1) - 1 + (2**(map_y + 1) - 1) << 16


def EUDHumanLoop():
    def _footer():
        block = {'origcp': f_getcurpl()}

        minp, maxp = min(humans), max(humans)
        EUDWhile()(cp.AtMost(maxp))
        for p in range(minp, maxp):
            if p not in humans:
                EUDContinueIf(cp.Exactly(p))
        EUDContinueIfNot(f_playerexist(cp))
        f_setcurpl(cp)

        EUDCreateBlock('hloopblock', block)
        return True

    return CtrlStruOpener(_footer)


def EUDEndHumanLoop():
    block = EUDPopBlock('hloopblock')[1]
    origcp = block['origcp']

    if not EUDIsContinuePointSet():
        EUDSetContinuePoint()

    EUDEndWhile()
    f_setcurpl(origcp)


@EUDFunc
def epd2alphaid(epd):
    epd += 43
    ret = epd // 84
    ret -= 226
    # alphaID = (ptr - 0x59CCA8) // 336 + 1
    # = (ptr - 56) // 336 - 17514
    # = (epd * 4 + 0x58A364 - 56) // 336 - 17514
    # = (epd + 1452235) // 84 - 17514
    EUDReturn(ret)


@EUDFunc
def Respawn():
    q4, m4 = divmod(QCUnit, 4)
    q2, m2 = divmod(QCUnit, 2)
    q4, q2 = 4*q4, 4*q2
    m4, m2 = 1 << (8*m4), 1 << (16*m2)
    LOC_TEMP, LocEPD = EUDArray(5), EPD(0x58DC60) + QCLoc * 5
    global cp
    DoActions([  # Units.dat
        # Unit Dimensions, Building Dimensions
        SetMemory(0x6617C8 + QCUnit * 8, SetTo, 0x20002),
        SetMemory(0x6617CC + QCUnit * 8, SetTo, 0x20002),
        SetMemory(0x662860 + QCUnit * 4, SetTo, 0),
        # Ground Weapon, Air Weapon
        SetMemoryX(0x6636B8 + q4, SetTo, 130 * m4, 0xFF * m4),
        SetMemoryX(0x6616E0 + q4, SetTo, 130 * m4, 0xFF * m4),
        # Seek Range, Sight Range
        SetMemoryX(0x662DB8 + q4, SetTo, 0, 0xFF * m4),
        SetMemoryX(0x663238 + q4, SetTo, 0, 0xFF * m4),
        # Advanced Flags, Editor Ability Flags, Group
        SetMemory(0x664080 + QCUnit * 4, SetTo, 0x38000004),
        SetMemoryX(0x661518 + q2, SetTo, 0x1CF * m2, 0xFFFF * m2),
        SetMemoryX(0x6637A0 + q4, SetTo, 0, 0xFF * m4),
        # MovementFlags & Elevation
        SetMemoryX(0x660FC8 + q4, SetTo, 0xC5 * m4, 0xFF * m4),
        SetMemoryX(0x663150 + q4, SetTo, 0x13 * m4, 0xFF * m4),
        # Temporary save previous data of QCLocation
        SetMemory(LOC_TEMP, SetTo, f_dwread_epd(LocEPD)),
        SetMemory(LOC_TEMP + 4, SetTo, f_dwread_epd(LocEPD + 1)),
        SetMemory(LOC_TEMP + 8, SetTo, f_dwread_epd(LocEPD + 2)),
        SetMemory(LOC_TEMP + 12, SetTo, f_dwread_epd(LocEPD + 3)),
        SetMemory(LOC_TEMP + 16, SetTo, f_dwread_epd(LocEPD + 4)),
        SetMemoryXEPD(LocEPD + 4, SetTo, 0, 0xFFFF0000),
        cp.SetNumber(min(humans)),
    ])
    EUDHumanLoop()()
    i = EUDVariable()
    arrayEPD = ArrayEPDs[cp]
    DoActions([
        i.SetNumber(0),
        arrayEPD.AddNumber(5),
        [
            DisplayText("\x13\x04[QCDebug] \x16Respawning QC Units...")
            if QCDebug else []
        ],
    ])
    if EUDWhile()(i <= QCCount - 1):
        if EUDIf()(Memory(0x628438, Exactly, 0)):
            EUDReturn(-1)  # Cannot create more unit
        EUDEndIf()
        ptr, epd = f_cunitepdread_epd(EPD(0x628438))

        DoActions([
            # reset QCLocation to QC_XY
            SetMemoryEPD(LocEPD, SetTo, QCX),
            SetMemoryEPD(LocEPD + 1, SetTo, QCY),
            SetMemoryEPD(LocEPD + 2, SetTo, QCX),
            SetMemoryEPD(LocEPD + 3, SetTo, QCY),
            CreateUnit(1, QCUnit, QCLoc + 1, P8),
            SetMemoryEPD(arrayEPD, SetTo, epd),
        ])
        pos_x, pos_y = f_posread_epd(epd + 0x28//4)
        SetLoc2UnitPos, SetLocRB, Loc2PosTrg = Forward(), Forward(), Forward()
        RawTrigger(
            nextptr=pos_x.GetVTable(),
            actions=[
                pos_x.QueueAssignTo(EPD(SetLoc2UnitPos) + 5),
                SetNextPtr(pos_x.GetVTable(), pos_y.GetVTable()),
                pos_y.QueueAssignTo(EPD(SetLoc2UnitPos) + 5),
                SetNextPtr(pos_y.GetVTable(), SetLocRB),
            ]
        )
        SetLocRB << RawTrigger(
            nextptr=pos_x.GetVTable(),
            actions=[
                SetMemory(pos_x._varact + 16, Add, 16),
                SetMemory(pos_y._varact + 16, Add, 16),
                SetNextPtr(pos_y.GetVTable(), Loc2PosTrg),
            ]
        )
        Loc2PosTrg << NextTrigger()
        DoActions([
            # Move QCLocation to QCUnit
            SetLoc2UnitPos << SetMemoryEPD(LocEPD, SetTo, 0),
            SetMemoryEPD(LocEPD + 1, SetTo, 0),
            SetMemoryEPD(LocEPD + 2, SetTo, 0),
            SetMemoryEPD(LocEPD + 3, SetTo, 0),
            GiveUnits(1, QCUnit, P8, QCLoc + 1, QCPlayer),
            SetMemoryEPD(epd + 0x10 // 4, SetTo, 64 * 65537),  # reset waypoint
            SetMemoryEPD(epd + 0x34 // 4, SetTo, 0),  # immobilize
            SetMemoryEPD(epd + 0x4C // 4, Add, cp - QCPlayer),  # modify unit's player
            SetMemoryEPD(epd + 0xDC // 4, Add, 0xA00000),  # stackable
            SetMemoryXEPD(epd + 0xA5 // 4, SetTo, 0, 0xFF00)  # uniqueIdentifier
        ])
        if EUDIf()(Memory(0x512684, Exactly, cp)):
            MyQCptrsArray = EUDArray([EPD(t) + 2 for t in MyQCptrs])
            MyQCalphaidsArray = EUDArray([EPD(t) + 5 for t in MyQCalphaids])
            SetMyQC, SetMyQCTrg = Forward(), Forward()
    
            myQCptr, myQCalphaID = MyQCptrsArray[i], MyQCalphaidsArray[i]
            alphaID = epd2alphaid(epd)

            RawTrigger(
                nextptr=myQCptr.GetVTable(),
                actions=[
                    myQCptr.QueueAssignTo(EPD(SetMyQC) + 4),
                    SetNextPtr(myQCptr.GetVTable(), myQCalphaID.GetVTable()),
                    myQCalphaID.QueueAssignTo(EPD(SetMyQC) + 12),
                    SetNextPtr(myQCalphaID.GetVTable(), ptr.GetVTable()),
                    ptr.QueueAssignTo(EPD(SetMyQC) + 5),
                    SetNextPtr(ptr.GetVTable(), alphaID.GetVTable()),
                    alphaID.QueueAssignTo(EPD(SetMyQC) + 13),
                    SetNextPtr(alphaID.GetVTable(), SetMyQCTrg),
                ]
            )
            SetMyQCTrg << RawTrigger(
                actions=[
                    SetMyQC << SetMemory(0, SetTo, 0),  # ptr
                    SetMemory(0, SetTo, 0),  # alphaID
                ]
            )
        EUDEndIf()
        EUDSetContinuePoint()
        DoActions([
            i.AddNumber(1),
            arrayEPD.AddNumber(18),
        ])
    EUDEndWhile()
    EUDSetContinuePoint()
    cp += 1
    EUDEndHumanLoop()

    DoActions([
        # Restore previouse data of QCLocation
        SetMemoryEPD(LocEPD, SetTo, LOC_TEMP[0]),
        SetMemoryEPD(LocEPD + 1, SetTo, LOC_TEMP[1]),
        SetMemoryEPD(LocEPD + 2, SetTo, LOC_TEMP[2]),
        SetMemoryEPD(LocEPD + 3, SetTo, LOC_TEMP[3]),
        SetMemoryEPD(LocEPD + 4, SetTo, LOC_TEMP[4]),
        # Editor Ability Flags
        SetMemoryX(0x661518 + q2, SetTo, 0, 0xFFFF * m2),
    ])

    EUDReturn(0)


def eqsplit(iterable, eqr):
    if isinstance(iterable, list):
        for i in range(0, len(iterable), eqr):
            yield iterable[i : i + eqr]

    else:
        it = iter(iterable)
        item = list(itertools.islice(it, eqr))
        while item:
            yield item
            item = list(itertools.islice(it, eqr))


@EUDFunc
def KillQCUnits():
    global cp
    cp << min(humans)
    EUDHumanLoop()()
    arrayPtr = ArrayPTRs[cp]
    arrayEPD = ArrayEPDs[cp]
    i = EUDVariable()
    loopstart, qc2epdv = Forward(), Forward()
    RawTrigger(
        nextptr=arrayPtr.GetVTable(),
        actions=[
            arrayPtr.QueueAssignTo(EPD(qc2epdv) + 1),  # nextptr
            SetNextPtr(arrayPtr.GetVTable(), arrayEPD.GetVTable()),
            arrayEPD.AddNumber(4),  # dest
            arrayEPD.QueueAssignTo(EPD(qc2epdv) + 86),
            i.SetNumber(0),
            SetNextPtr(arrayEPD.GetVTable(), loopstart),
        ]
    )
    loopstart << NextTrigger()
    VProc(arrayEPD, [
        arrayEPD.SubtractNumber(3),  # nextptr
        SetMemory(arrayEPD._varact + 16, Add, 8),
    ])
    if EUDWhile()(i <= QCCount - 1):
        epd, _next = EUDVariable(), Forward()
        qc2epdv << RawTrigger(
            nextptr=0,
            actions=[
                SetMemory(0, SetTo, EPD(epd.getValueAddr())),
                SetNextPtr(0, _next),
            ]
        )
        _next << NextTrigger()
        EUDContinueIf(MemoryEPD(epd + 0xC//4, Exactly, 0))
        DoActions(SetMemoryXEPD(epd + 0x110//4, SetTo, 1, 0xFFFF))

        EUDSetContinuePoint()
        DoActions([
            SetMemory(qc2epdv + 4, Add, 72),
            SetMemory(qc2epdv + 328 + 16, Add, 18),
            SetMemory(qc2epdv + 360 + 16, Add, 18),
            i.AddNumber(1)
        ])
    EUDEndWhile()
    EUDSetContinuePoint()
    cp += 1
    EUDEndHumanLoop()


def DebugQC():
    if not QCDebug:
        return
    something_bad_happend, fin = Forward(), Forward()
    global cp
    cp << min(humans)
    EUDHumanLoop()()
    arrayPtr = ArrayPTRs[cp]
    arrayEPD = ArrayEPDs[cp]
    i = EUDVariable()
    loopstart, qc2epdv = Forward(), Forward()
    playercheck = Forward()
    RawTrigger(
        nextptr=arrayPtr.GetVTable(),
        actions=[
            arrayPtr.QueueAssignTo(EPD(qc2epdv) + 1),  # nextptr
            SetNextPtr(arrayPtr.GetVTable(), arrayEPD.GetVTable()),
            arrayEPD.AddNumber(4),  # dest
            arrayEPD.QueueAssignTo(EPD(qc2epdv) + 86),
            i.SetNumber(0),
            SetNextPtr(arrayEPD.GetVTable(), cp.GetVTable()),
            cp.QueueAssignTo(EPD(playercheck) + 2),
            SetNextPtr(cp.GetVTable(), loopstart),
        ]
    )
    loopstart << NextTrigger()
    VProc(arrayEPD, [
        arrayEPD.SubtractNumber(3),  # nextptr
        SetMemory(arrayEPD._varact + 16, Add, 8),
    ])
    if EUDWhile()(i <= QCCount - 1):
        epd, _next = EUDVariable(), Forward()
        qc2epdv << RawTrigger(
            nextptr=0,
            actions=[
                SetMemory(0, SetTo, EPD(epd.getValueAddr())),
                SetNextPtr(0, _next),
            ]
        )
        _next << NextTrigger()
        # TODO: more helpful debug message
        EUDJumpIf(MemoryEPD(epd + 0xC//4, Exactly, 0), something_bad_happend)
        EUDJumpIf(MemoryXEPD(epd + 0xA5//4, AtLeast, 256, 0xFF00), something_bad_happend)
        EUDJumpIfNot([
            playercheck << MemoryEPD(epd + 0x4C//4, Exactly, 0)
        ], something_bad_happend)

        EUDSetContinuePoint()
        DoActions([
            SetMemory(qc2epdv + 4, Add, 72),
            SetMemory(qc2epdv + 328 + 16, Add, 18),
            SetMemory(qc2epdv + 360 + 16, Add, 18),
            i.AddNumber(1)
        ])
    EUDEndWhile()
    EUDSetContinuePoint()
    cp += 1
    EUDEndHumanLoop()

    PushTriggerScope()
    something_bad_happend << NextTrigger()
    cp << min(humans)
    if EUDHumanLoop()():
        DoActions([
            # TODO: more helpful debug message
            DisplayText("\x13\x08MSQC FATAL ERROR! QC Unit has been removed."),
        ])
        EUDSetContinuePoint()
        cp += 1
    EUDEndHumanLoop()
    KillQCUnits()
    if EUDIf()(Respawn() == -1):
        KillQCUnits()
        DoActions([
            cp.SetNumber(min(humans)),
            QCShutdown.SetNumber(60 * 23),
        ])
        if EUDHumanLoop()():
            DoActions([
                # TODO: more helpful debug message
                DisplayText("\x13\x08QC Respawn failed due to 'Cannot create more unit'\n\x13\x08* MSQC will shutdown for 1 minute."),
            ])
            EUDSetContinuePoint()
            cp += 1
        EUDEndHumanLoop()
    EUDEndIf()
    EUDJump(fin)
    PopTriggerScope()
    fin << NextTrigger()


@EUDFunc
def SendQC():
    SelCount, SelMem = EUDVariable(), EUDVArray(12)()
    QGCActivated = EUDLightVariable()
    skipSelSave = Forward()
    global MyQC

    # 0x6284B8: (desync) *CUnits of units in selection (4 bytes * 12 units)
    SelCount << 0
    for i in range(QCCount):  # skip if QCUnit is selected
        skipper, nextTrg = Forward(), Forward()
        skipper << RawTrigger(
            conditions=[MyQCptrs[i] << Memory(0x6284B8, Exactly, 0)],
            actions=[
                SetNextPtr(skipper, skipSelSave),
                SetMemory(skipSelSave + 344, SetTo, EPD(skipper) + 1),
                SetMemory(skipSelSave + 348, SetTo, nextTrg),
            ]
        )
        nextTrg << NextTrigger()

    SelMemPos = Forward()
    DoActions([  # don't need setcurpl, as read_cp don't use getcurpl
        SetMemory(0x6509B0, SetTo, EPD(0x6284B8)),
        SetMemory(SelMemPos + 16, SetTo, EPD(SelMem)),
    ])
    if EUDLoopN()(12):  # backup units in selection
        EUDJumpIf(Deaths(CurrentPlayer, Exactly, 0, 0), skipSelSave)
        DoActions([
            SelMemPos << SetMemoryEPD(0, SetTo, f_cunitepdread_cp(0)[1]),
            SetMemory(SelMemPos + 16, Add, 1),
            SelCount.AddNumber(1),
            SetMemory(0x6509B0, Add, 1),
        ])
    EUDEndLoopN()

    skipSelSave << RawTrigger(
        actions=[
            SetNextPtr(skipper, nextTrg),
            QGCActivated.SetNumber(0),
            cp.SetNumber(min(humans)),  # initialization for ReceiveQC
        ]
    )

    def parseCond(s):
        _ns = GetEUDNamespace()
        for k, v in ns.items():
            if (IsEUDVariable(v)
                or isUnproxyInstance(v, EUDLightVariable)
                or isUnproxyInstance(v, EUDXVariable)
            ) and k in s:
                s = re.sub(r"\b{}\b".format(k), "_ns.\g<0>", s)
        return s


    RC = Db(b'...\x14XXYY\0\0\xE4\0\x00')
    SEL = Db(b'..\x09\x0112..')
    f_setcurpl(f_getuserplayerid())

    qc_list = eqsplit(qc_conds, len(bit_xy))
    for n, conds in enumerate(qc_list):
        DoActions(SetMemory(RC + 4, SetTo, 64 * 65537))
        for con, bit in zip(conds, bit_xy):
            if len(con) == 1:
                condition = con
            else:
                condition = EUDSCAnd()
                for c in con:
                    _ns = GetEUDNamespace()
                    if type(c) is str:
                        condition = condition(eval(parseCond(c)))
                    else:
                        condition = condition(c)
                condition = condition()
            if EUDIf()(condition):
                DoActions(SetMemory(RC + 4, Add, bit))
            EUDEndIf()
        if EUDIf()(Memory(RC + 4, AtLeast, 64 * 65537 + 1)):
            DoActions([
                MyQCalphaids[n] << SetMemory(SEL + 4, SetTo, 0),
                QGCActivated.SetNumber(1),
            ])
            # TODO: Optimize QueueGameCommand and f_memcpy
            QueueGameCommand(SEL + 2, 4)
            QueueGameCommand(RC + 3, 10)  # RightClick
        EUDEndIf()

    for n, (con, ret) in enumerate(zip(v_conds, v_rets)):
        DoActions(SetMemory(RC + 4, SetTo, 64 * 65537))
        if len(con) == 1:
            condition = con
        else:
            condition = EUDSCAnd()
            for c in con:
                _ns = GetEUDNamespace()
                if type(c) is str:
                    condition = condition(eval(parseCond(c)))
                else:
                    condition = condition(c)
            condition = condition()
        if EUDIf()(condition):
            if ret[0] == "mouse":
                sX = f_mapXread_epd(EPD(0x62848C))
                sY = f_mapYread_epd(EPD(0x6284A8))
                mX = f_screenXread_epd(EPD(0x6CDDC4))
                mY = f_screenYread_epd(EPD(0x6CDDC8))
                addMouseCoord = Forward()
                RawTrigger(
                    nextptr=sX.GetVTable(),
                    actions=[
                        SetMemory(addMouseCoord + 328 + 20, SetTo, 0),
                        sX.QueueAddTo(EPD(addMouseCoord) + 87),
                        SetNextPtr(sX.GetVTable(), sY.GetVTable()),
                        sY.QueueAddTo(EPD(addMouseCoord) + 87),
                        SetNextPtr(sY.GetVTable(), sY.GetVTable()),
                        mX.QueueAddTo(EPD(addMouseCoord) + 87),
                        SetNextPtr(mX.GetVTable(), sY.GetVTable()),
                        mY.QueueAddTo(EPD(addMouseCoord) + 87),
                        SetNextPtr(mY.GetVTable(), addMouseCoord),
                        MyQCalphaids[n + len(qc_list)] << SetMemory(SEL + 4, SetTo, 0),
                        QGCActivated.SetNumber(1),
                    ]
                )
                addMouseCoord << RawTrigger(actions=SetMemory(RC + 4, Add, 0))
            elif ret[0] == "xy":

                def parseSource(src, always=False):
                    try:
                        src = int(ret[1], 0)
                    except ValueError:
                        _ns = GetEUDNamespace()
                        src = eval(parseCond(ret[1]))
                        if isinstance(src, EUDLightVariable) or always:
                            src = EPD(src.getValueAddr())
                    else:
                        src = EPD(src)
                    return src

                if len(ret) == 3:
                    src = parseSource(ret[1])
                    if type(src) not in (EUDVariable, EUDXVariable):
                        src = f_maskread_epd(src, mapMask)
                elif len(ret) == 5:
                    x = parseSource(ret[1])
                    y = parseSource(ret[2], always=True)
                    if type(src) not in (EUDVariable, EUDXVariable):
                        x = f_mapXread_epd(x)
                    y = f_mapYread_epd(y)
                    src = x + y
                VProc(src, [
                    src.QueueAddTo(EPD(RC) + 1),
                    MyQCalphaids[n + len(qc_list)] << SetMemory(SEL + 4, SetTo, 0),
                    QGCActivated.SetNumber(1),
                ])
            else:
                raise EPError("{} is Unknown type for return value".format(ret[0]))
            # TODO: Optimize QueueGameCommand and f_memcpy
            QueueGameCommand(SEL + 2, 4)
            QueueGameCommand(RC + 3, 10)  # RightClick
        EUDEndIf()

    # restore unit selection from array
    if EUDIf()([SelCount >= 1, QGCActivated == 1]):
        NSEL = Db(b'...\x091234567890123456789012345.......')
        n, sel2unitepd, _next = EUDVariable(), Forward(), Forward()
        VProc(SelCount, [
            SetCurrentPlayer(EPD(NSEL) + 1),
            n.SetNumber(2),
            SelCount.QueueAddTo(n),
            SetMemory(sel2unitepd + 4, SetTo, SelMem),
            SetMemory(sel2unitepd + 328 + 16, SetTo, EPD(SelMem) + 4),
            SetMemory(sel2unitepd + 360 + 16, SetTo, EPD(SelMem) + 1),
        ])
        VProc(SelCount, [])
        cw = CPByteWriter()
        cw.writebyte(n)
        if EUDWhile()(SelCount >= 1):
            unitepd = EUDVariable()  # f_epdcunitread_epd(ptrListepd)
            sel2unitepd << RawTrigger(
                nextptr=0,
                actions=[
                    SetMemory(0, SetTo, EPD(unitepd.getValueAddr())),
                    SetNextPtr(0, _next),
                ]
            )
            _next << NextTrigger()
            targetID = epd2alphaid(unitepd)
            b0, b1 = f_dwbreak(targetID)[2:4]
            cw.writebyte(b0)
            cw.writebyte(b1)
    
            EUDSetContinuePoint()
            DoActions([
                SelCount.SubtractNumber(1),
                SetMemory(sel2unitepd + 4, Add, 72),
                SetMemory(sel2unitepd + 328 + 16, Add, 18),
                SetMemory(sel2unitepd + 360 + 16, Add, 18),
            ])
        EUDEndWhile()
        cw.flushdword()
        QueueGameCommand(NSEL + 3, n)
    EUDEndIf()


@EUDFunc
def ReceiveQC():

    vi = EUDVariable()
    DoActions([
        cp.SetNumber(min(humans)),
        vi.SetNumber(min(humans) * 18),
    ])

    EUDHumanLoop()()
    arrayPtr = ArrayPTRs[cp]
    arrayEPD = ArrayEPDs[cp]
    loopstart, qc2epdv = Forward(), Forward()
    RawTrigger(
        nextptr=arrayPtr.GetVTable(),
        actions=[
            arrayPtr.QueueAssignTo(EPD(qc2epdv) + 1),  # nextptr
            SetNextPtr(arrayPtr.GetVTable(), arrayEPD.GetVTable()),
            arrayEPD.AddNumber(4),  # dest
            arrayEPD.QueueAssignTo(EPD(qc2epdv) + 86),
            SetNextPtr(arrayEPD.GetVTable(), loopstart),
        ]
    )
    loopstart << NextTrigger()
    VProc(arrayEPD, [
        arrayEPD.SubtractNumber(3),  # nextptr
        SetMemory(arrayEPD._varact + 16, Add, 8),
    ])
    DoActions([
        SetDeaths(CurrentPlayer, SetTo, 0, deaths_unit)
        for deaths_unit in deathsUnits
    ])
    epd = EUDVariable()

    @EUDFunc
    def updateQCepd():
        _next = Forward()
        qc2epdv << RawTrigger(
            nextptr=0,
            actions=[
                SetMemory(0, SetTo, EPD(epd.getValueAddr())),
                SetNextPtr(0, _next),
            ]
        )
        _next << RawTrigger(
            actions=[
                SetMemory(qc2epdv + 4, Add, 72),
                SetMemory(qc2epdv + 328 + 16, Add, 18),
                SetMemory(qc2epdv + 360 + 16, Add, 18),
            ]
        )

    def parseArray(s):
        _ns = GetEUDNamespace()
        for k, v in _ns.items():
            if (isUnproxyInstance(v, EUDArray)
                or isUnproxyInstance(v, EUDVArray(8))
            ) and k in s:
                s = re.sub(r"\b{}\b".format(k), "_ns.\g<0>", s)
        return s

    init_array = []
    for ret in qc_rets:
        if ret[0] == "array":
            _ns = GetEUDNamespace()
            array = eval(parseArray(ret[1]))
            if isUnproxyInstance(array, EUDArray):
                init_array.append(SetMemoryEPD(EPD(array) + cp, SetTo, 0))
            elif isUnproxyInstance(array, EUDVArray(8)):
                init_array.append(SetMemoryEPD(EPD(array) + vi, SetTo, 0))
            else:
                raise EPError("{} unknown type for return value".format(ret[1]))
    if init_array:
        DoActions(init_array)

    qr_list = eqsplit(qc_rets, len(bit_xy))
    for n, rets in enumerate(qr_list):
        updateQCepd()
        waypoint = epd + 0x10 // 4
        if EUDIf()(MemoryEPD(waypoint, AtLeast, 64 * 65537 + 1)):
            f_dwsubtract_epd(waypoint, 64 * 65537)
            for ret, bit in zip(rets, bit_xy):
                if EUDIf()(MemoryXEPD(waypoint, AtLeast, 1, bit)):
                    if ret[0] == "deaths":
                        DoActions(SetDeaths(CurrentPlayer, Add, ret[2], ret[1]))
                    elif ret[0] == "array":
                        _ns = GetEUDNamespace()
                        array = eval(parseArray(ret[1]))
                        if isUnproxyInstance(array, EUDArray):
                            DoActions(SetMemoryEPD(EPD(array) + cp, Add, ret[2]))
                        elif isUnproxyInstance(array, EUDVArray(8)):
                            DoActions(SetMemoryEPD(EPD(array) + vi, Add, ret[2]))
                        else:
                            raise EPError("{} unknown type for return value".format(ret[1]))
                EUDEndIf()
            f_dwwrite_epd(waypoint, 64 * 65537)
        EUDEndIf()

    vinit_array = []
    for rets in v_rets:
        for ret in rets:
            if type(ret) == str and (ret != "xy" and ret != "mouse"):
                _ns = GetEUDNamespace()
                array = eval(parseArray(ret))
                if isUnproxyInstance(array, EUDArray):
                    vinit.append(SetMemoryEPD(EPD(array) + cp, SetTo, 0))
                elif isUnproxyInstance(array, EUDVArray(8)):
                    vinit_array.append(SetMemoryEPD(EPD(array) + vi, SetTo, 0))
                else:
                    raise EPError("{} unknown type for return value".format(ret))
    if vinit_array:
        DoActions(vinit_array)

    for n, ret in enumerate(v_rets):
        updateQCepd()
        waypoint = epd + 0x10 // 4
        if EUDIf()(MemoryEPD(waypoint, AtLeast, 64 * 65537 + 1)):
            f_dwsubtract_epd(waypoint, 64 * 65537)
            if ret[0] == "mouse":
                x, y = f_posread_epd(waypoint)
                f_setloc(QCLoc + cp, x, y)
            elif ret[0] == "xy":
                if len(ret) == 3:
                    xy = f_maskread_epd(waypoint, mapMask)
                    if isinstance(ret[2], int):
                        DoActions(SetDeaths(CurrentPlayer, SetTo, xy, ret[2]))
                    else:
                        _ns = GetEUDNamespace()
                        array = eval(parseArray(ret[2]))
                        if isUnproxyInstance(array, EUDArray):
                            DoActions(SetMemoryEPD(EPD(array) + cp, SetTo, xy))
                        elif isUnproxyInstance(array, EUDVArray(8)):
                            DoActions(SetMemoryEPD(EPD(array) + vi, SetTo, xy))
                        else:
                            raise EPError("{} unknown type for return value".format(ret[2]))
                elif len(ret) == 5:
                    x, y = f_posread_epd(waypoint)
                    if isinstance(ret[3], int) or isinstance(ret[4], int):
                        DoActions([
                            [
                                SetDeaths(CurrentPlayer, SetTo, x, ret[3])
                                if isinstance(ret[3], int) else []
                            ],
                            [
                                SetDeaths(CurrentPlayer, SetTo, y, ret[4])
                                if isinstance(ret[4], int) else []
                            ],
                        ])
                    _ns = GetEUDNamespace()
                    for s, v in zip([ret[3], ret[4]], [x, y]):
                        if type(s) != str:
                            continue
                        array = eval(parseArray(s))
                        if isUnproxyInstance(array, EUDArray):
                            DoActions(SetMemoryEPD(EPD(array) + cp, SetTo, v))
                        elif isUnproxyInstance(array, EUDVArray(8)):
                            DoActions(SetMemoryEPD(EPD(array) + vi, SetTo, v))
                        else:
                            raise EPError("{} unknown type for return value".format(ret[2]))
            else:
                raise EPError("{} is Unknown type for return value".format(ret[0]))
            f_dwwrite_epd(waypoint, 64 * 65537)
        EUDEndIf()

    EUDSetContinuePoint()
    DoActions([
        cp.AddNumber(1),
        vi.AddNumber(18),
    ])
    EUDEndHumanLoop()

    KeyUpdate()
    MouseUpdate()


def beforeTriggerExec():
    origcp = f_getcurpl()

    if QCDebug:
        end = Forward()
        DebugQC()
        EUDJumpIf(QCShutdown.AtLeast(1), end)
    SendQC()
    ReceiveQC()
    if QCDebug:
        end << RawTrigger(conditions=QCShutdown.AtLeast(1), actions=QCShutdown.SubtractNumber(1))

    f_setcurpl(origcp)
