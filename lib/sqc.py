#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Library for synchronizing local user data to every players by QueueGameCommand.

Sending local data to each other can be tricky sometimes!
This module provides easy ways to share local data like keyboard input or mouse coordinates without worry of desync.

Available functions:
- Start: Call this function in onPluginStart.
- Main: Call this function in middle of beforeTriggerExec.
- AddQC: Register local event, execute sync action or function when True.
- AddNot: Register local event, execute sync action or function when False.
- AddBefore: Register initialization action or function. Run at the start of Main function.
- AddAfter: Register initialization action or function. Run at the end of Main function.
- KeyDown: Return True once the user presses a Key.
- KeyUp: Return True once the user releases a Key.
- KeyPress: Return True while the user presses a Key.
- NotTyping: Return False if message prompt appears.
- MouseDown: Return True once the user presses a MouseButton.
- MouseUp: Return True once the user releases a MouseButton.
- MousePress: Return True while the user presses a button.
- MouseMoveLocation: Input first location index to MouseLocation.

Globals:
- QCUnit: Terran Valkyrie is Default.
- QCLoc: Location 1 (Index 0) is Default.
- QCPlayer: Player 11 is Default.
- QCX, QCY: 128, 128 (4, 4) are Default.
- QCSafety: _Respawn QCUnit when something bad happened.
"""

from itertools import cycle
from math import ceil
from struct import unpack

from eudplib import *

cw = CPByteWriter()

# Default: Valkyrie, Location 1, P11
QCUnit, QCLoc, QCPlayer = 58, 0, 10
QCX, QCY = 128, 128  # (4, 4)
QCSafety = 1
# fmt: off
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
    ';': 0xBA, '=': 0xBB, ',': 0xBC, '-': 0xBD, '.': 0xBE, '/': 0xBF,
    '`': 0xC0, 'ABNT_C1': 0xC1, 'ABNT_C2': 0xC2,
    '[': 0xDB, '\\': 0xDC, ']': 0xDD, "'": 0xDE, 'OEM_8': 0xDF,
    'OEM_AX': 0xE1, 'OEM_102': 0xE2, 'ICO_HELP': 0xE3, 'ICO_00': 0xE4,
    'PROCESSKEY': 0xE5, 'ICO_CLEAR': 0xE6, 'PACKET': 0xE7, 'OEM_RESET': 0xE9,
    'OEM_JUMP': 0xEA, 'OEM_PA1': 0xEB, 'OEM_PA2': 0xEC, 'OEM_PA3': 0xED,
    'OEM_WSCTRL': 0xEE, 'OEM_CUSEL': 0xEF,
    'OEM_ATTN': 0xF0, 'OEM_FINISH': 0xF1, 'OEM_COPY': 0xF2, 'OEM_AUTO': 0xF3,
    'OEM_ENLW': 0xF4, 'OEM_BACKTAB': 0xF5, 'ATTN': 0xF6, 'CRSEL': 0xF7,
    'EXSEL': 0xF8, 'EREOF': 0xF9, 'PLAY': 0xFA, 'ZOOM': 0xFB, 'NONAME': 0xFC,
    'PA1': 0xFD, 'OEM_CLEAR': 0xFE, '_NONE_': 0xFF
}
# fmt: on
KeyArray = EUDArray(8)
KeyOffset = set()


def _KeyUpdate(offset):
    m = 256 ** (offset % 4)
    n = 2 ** (offset % 32)
    RawTrigger(
        conditions=[  # KeyDown
            MemoryX(0x596A18 + offset, Exactly, m, m),
            MemoryX(KeyArray + offset // 8, Exactly, 0, n),
        ],
        actions=SetMemoryX(KeyArray + offset // 8, SetTo, n, n),
    )
    RawTrigger(
        conditions=[  # KeyUp
            MemoryX(0x596A18 + offset, Exactly, 0, m),
            MemoryX(KeyArray + offset // 8, Exactly, n, n),
        ],
        actions=SetMemoryX(KeyArray + offset // 8, SetTo, 0, n),
    )


def KeyDown(k):
    """Occurs when a key is pressed."""
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
            MemoryX(KeyArray + offset // 8, Exactly, 0, n),
        ]


def KeyUp(k):
    """Occurs when a key is released."""
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
            MemoryX(KeyArray + offset // 8, Exactly, n, n),
        ]


def KeyPress(k):
    """Occurs while a key is pressed."""
    try:
        offset = KeyCodeDict[k.upper()]
    except (KeyError):
        raise EPError("%s doesn't exist in VirtualKeyCode." % (k))
    else:
        m = 256 ** (offset % 4)
        return MemoryX(0x596A18 + offset, Exactly, m, m)


def NotTyping():
    """Occurs when messaging is closed."""
    return Memory(0x68C144, Exactly, 0)


MouseButtonDict = {"L": 2, "LEFT": 2, "R": 8, "RIGHT": 8, "M": 32, "MIDDLE": 32}
MouseArray = EUDArray(1)
MouseOffset = set()


def _MouseUpdate(k):
    RawTrigger(
        conditions=[  # MouseDown
            MemoryX(0x6CDDC0, Exactly, k, k),
            MemoryX(MouseArray, Exactly, 0, k),
        ],
        actions=SetMemoryX(MouseArray, SetTo, k, k),
    )
    RawTrigger(
        conditions=[  # MouseUp
            MemoryX(0x6CDDC0, Exactly, 0, k),
            MemoryX(MouseArray, Exactly, k, k),
        ],
        actions=SetMemoryX(MouseArray, SetTo, 0, k),
    )


def MouseDown(k):
    """Occurs when a mouse button is pressed."""
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        MouseOffset.add(v)
        return [  # MouseDown
            MemoryX(0x6CDDC0, Exactly, v, v),
            MemoryX(MouseArray, Exactly, 0, v),
        ]


def MouseUp(k):
    """Occurs when a mouse button is released."""
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        MouseOffset.add(v)
        return [  # MouseUp
            MemoryX(0x6CDDC0, Exactly, 0, v),
            MemoryX(MouseArray, Exactly, v, v),
        ]


def MousePress(k):
    """Occurs while a mouse button is pressed."""
    try:
        v = MouseButtonDict[k.upper()]
    except (KeyError):
        raise EPError("%s is NOT a MouseButton. Use 'L', 'R' or 'M'." % (k))
    else:
        return MemoryX(0x6CDDC0, Exactly, v, v)


def _onInit():
    chkt = GetChkTokenized()
    dim, ownr = chkt.getsection("DIM"), chkt.getsection("OWNR")
    dim_x, dim_y = b2i2(dim[0:2]), b2i2(dim[2:4])
    global mapX, mapY, mapXY, human, MapXY
    mapX, mapY = dim_x.bit_length() + 3, dim_y.bit_length() + 3
    mapXY = mapX + mapY
    Map_X, Map_Y = (dim_x - 1).bit_length() + 5, (dim_y - 1).bit_length() + 5
    MapXY = [2 ** i for i in range(Map_X)] + [2 ** j for j in range(Map_Y)]
    human = [p for p in range(12) if ownr[p] == 6]


def _ID(x):
    """Identity function."""
    return x


_onInit()
cp = EUDVariable()
QCList, InitList = list(), [[cp.SetNumber(min(human))]]
AfterList = [[]]
setlocalcp = SetCurrentPlayer(0)
ismousemoved = EUDLightVariable()
mouseX, mouseY = EUDCreateVariables(2)

f_mapXread_epd = f_readgen_epd(2 ** (mapX + 1) - 1, (0, _ID))
f_mapYread_epd = f_readgen_epd(2 ** (mapY + 1) - 1, (0, _ID))
f_screenXread_epd = f_readgen_epd(0x3FF, (0, _ID))
f_screenYread_epd = f_readgen_epd(0x1FF, (0, _ID))
f_epdcunitread_epd = f_readgen_epd(0x7FFFF8, (EPD(0), lambda x: x // 4))


def _UpdateMouseInfo():
    ismousemoved << 0
    sX, sY, mX, mY = [Forward() for _ in range(4)]
    if EUDIfNot()(
        [
            sX << Memory(0x62848C, Exactly, 0),
            sY << Memory(0x6284A8, Exactly, 0),
            mX << Memory(0x6CDDC4, Exactly, 0),
            mY << Memory(0x6CDDC8, Exactly, 0),
        ]
    ):
        _sX = f_mapXread_epd(EPD(0x62848C))
        _sY = f_mapYread_epd(EPD(0x6284A8))
        _mX = f_screenXread_epd(EPD(0x6CDDC4))
        _mY = f_screenYread_epd(EPD(0x6CDDC8))
        global mouseX, mouseY
        mouseX << _sX + _mX
        mouseY << _sY + _mY
        DoActions(
            [
                ismousemoved.SetNumber(1),
                SetMemory(sX + 8, SetTo, _sX),
                SetMemory(sY + 8, SetTo, _sY),
                SetMemory(mX + 8, SetTo, _mX),
                SetMemory(mY + 8, SetTo, _mY),
            ]
        )
    EUDEndIf()


_once = EUDVariable()
pv5 = EUDVariable()
XYPool = cycle(MapXY)
_counter = 0
InitList[0].append([pv5.SetNumber(min(human) * 5 + EPD(0x58DC60)), _once.SetNumber(-1)])


def _IsMouseMoved():
    global _counter, mouseX, mouseY
    b = next(XYPool)
    v = mouseY if _counter > mapX else mouseX
    c = MemoryX(v.getValueAddr(), Exactly, b, b)
    _counter += 1
    return [ismousemoved.AtLeast(1), c]


def _AddLoc(loc, _fdict={}):
    if loc in _fdict:
        return _fdict[loc]
    else:

        def _f(_firstcall=[]):
            global _counter, _once
            if loc not in _firstcall:
                _firstcall.append(loc)
                _counter = 0
            lc = 5 * loc
            if EUDIfNot()(_once == cp):
                _once << cp
                DoActions(
                    [
                        SetMemoryEPD(pv5 + lc, SetTo, 0),
                        SetMemoryEPD(pv5 + (lc + 1), SetTo, 0),
                        SetMemoryEPD(pv5 + (lc + 2), SetTo, 0),
                        SetMemoryEPD(pv5 + (lc + 3), SetTo, 0),
                    ]
                )
            EUDEndIf()
            b = next(XYPool)
            if _counter > mapX:
                lc += 1
            DoActions(
                [  # pv5 = 5 * f_getcurpl() + EPD(0x58DC60)
                    SetMemoryEPD(pv5 + lc, Add, b),
                    SetMemoryEPD(pv5 + (lc + 2), Add, b),
                ]
            )
            _counter += 1

        _fdict[loc] = _f
        return _f


def MouseMoveLocation(loc):
    """Move Locations to players' mouse position. Input first location index."""
    loc = GetLocationIndex(loc)
    AddBefore(_UpdateMouseInfo)
    for _ in MapXY:
        AddQC(_IsMouseMoved(), _AddLoc(loc))


def AddQC(condition, action_or_function):
    """Register local (desync) event, execute sync action or function when True."""
    QCList.append((EUDIf, condition, action_or_function))


def AddNot(condition, action_or_function):
    """Register local (desync) event, execute sync action or function when False."""
    QCList.append((EUDIfNot, condition, action_or_function))


def AddBefore(action_or_function):
    """Register initialization action or function. Run at the start of Main function."""
    if callable(action_or_function):
        InitList.append(action_or_function)
    else:
        InitList[0].append(action_or_function)


def AddAfter(action_or_function):
    """Register initialization action or function. Run at the end of Main function."""
    if callable(action_or_function):
        AfterList.append(action_or_function)
    else:
        AfterList[0].append(action_or_function)


def _EUDHumanLoop():
    def _footer():
        block = {"origcp": f_getcurpl(), "playerv": cp}
        playerv = block["playerv"]

        minp, maxp = min(human), max(human)
        EUDWhile()(cp.AtMost(maxp))
        for p in range(minp, maxp):
            if p not in human:
                EUDContinueIf(cp.Exactly(p))
        EUDContinueIfNot(f_playerexist(playerv))
        f_setcurpl(playerv)

        EUDCreateBlock("hloopblock", block)
        return True

    return CtrlStruOpener(_footer)


def _EUDEndHumanLoop():
    block = EUDPopBlock("hloopblock")[1]
    playerv = block["playerv"]
    origcp = block["origcp"]

    if not EUDIsContinuePointSet():
        EUDSetContinuePoint()

    EUDEndWhile()
    f_setcurpl(origcp)


@EUDFunc
def _epd2alphaid(epd):
    # return (ptr - 0x59CCA8) // 336 + 1
    # return (ptr - 56) // 336 - 17514
    # (epd * 4 + 0x58A364 - 56) // 336 - 17514
    # (epd * 4 + 1452235 * 4) // 336 - 17514
    EUDReturn((epd + 43) // 84 - 226)


@EUDFunc
def _Respawn():
    q4, m4 = divmod(QCUnit, 4)
    q2, m2 = divmod(QCUnit, 2)
    p4, p2 = 256 ** m4, 65536 ** m2
    q4, q2 = 4 * q4, 4 * q2
    LOC_TEMP, LocEPD = EUDArray(5), EPD(0x58DC60) + QCLoc * 5
    global cp
    DoActions(
        [  # Units.dat
            # Unit Dimensions, Building Dimensions
            SetMemory(0x6617C8 + QCUnit * 8, SetTo, 0x20002),
            SetMemory(0x6617CC + QCUnit * 8, SetTo, 0x20002),
            SetMemory(0x662860 + QCUnit * 4, SetTo, 0),
            # Ground Weapon, Air Weapon
            SetMemoryX(0x6636B8 + q4, SetTo, 130 * p4, 0xFF * p4),
            SetMemoryX(0x6616E0 + q4, SetTo, 130 * p4, 0xFF * p4),
            # Seek Range, Sight Range
            SetMemoryX(0x662DB8 + q4, SetTo, 0, 0xFF * p4),
            SetMemoryX(0x663238 + q4, SetTo, 0, 0xFF * p4),
            # Advanced Flags, Editor Ability Flags, Group
            SetMemory(0x664080 + QCUnit * 4, SetTo, 0x38000004),
            SetMemoryX(0x661518 + q2, SetTo, 0x1CF * p2, 0xFFFF * p2),
            SetMemoryX(0x6637A0 + q4, SetTo, 0, 0xFF * p4),
            # MovementFlags & Elevation
            SetMemoryX(0x660FC8 + q4, SetTo, 0xC5 * p4, 0xFF * p4),
            SetMemoryX(0x663150 + q4, SetTo, 0x13 * p4, 0xFF * p4),
            # TEMPORARY SAVE PREVIOUS DATA OF QCLOCATION
            SetMemory(LOC_TEMP, SetTo, f_dwread_epd(LocEPD)),
            SetMemory(LOC_TEMP + 4, SetTo, f_dwread_epd(LocEPD + 1)),
            SetMemory(LOC_TEMP + 8, SetTo, f_dwread_epd(LocEPD + 2)),
            SetMemory(LOC_TEMP + 12, SetTo, f_dwread_epd(LocEPD + 3)),
            SetMemory(LOC_TEMP + 16, SetTo, f_dwread_epd(LocEPD + 4)),
            SetMemoryXEPD(LocEPD + 4, SetTo, 0, 0xFFFF0000),
            cp.SetNumber(min(human)),
        ]
    )

    global QCCount, EPDList, MyQC, QCAlphaID
    QCCount = ceil(len(QCList) / mapXY)
    EPDList = [[EUDVariable() for _ in range(QCCount)] for _ in human]
    MyQC = [Forward() for _ in range(QCCount)]
    QCAlphaID = [Forward() for _ in range(QCCount)]
    SetAlphaArray = EUDArray([EPD(act + 20) for act in QCAlphaID])

    _EUDHumanLoop()()
    if QCSafety:
        DoActions(DisplayText("\x13\x16Respawning QC Units..."))
    for i in EUDLoopRange(QCCount):
        ptr, epd = f_dwepdread_epd(EPD(0x628438))
        DoActions(
            [
                # RESET QCLOCATION TO QCXY
                SetMemoryEPD(LocEPD, SetTo, QCX),
                SetMemoryEPD(LocEPD + 1, SetTo, QCY),
                SetMemoryEPD(LocEPD + 2, SetTo, QCX),
                SetMemoryEPD(LocEPD + 3, SetTo, QCY),
                CreateUnit(1, QCUnit, QCLoc + 1, P8),
            ]
        )
        posX, posY = f_dwbreak(f_dwread_epd(epd + 0x28 // 4))[0:2]
        DoActions(
            [
                # MOVE QCLOCATION TO UNIT
                SetMemoryEPD(LocEPD, SetTo, posX),
                SetMemoryEPD(LocEPD + 1, SetTo, posY),
                SetMemoryEPD(LocEPD + 2, SetTo, posX),
                SetMemoryEPD(LocEPD + 3, SetTo, posY),
                GiveUnits(1, QCUnit, P8, QCLoc + 1, QCPlayer),
                SetMemoryEPD(epd + 0x10 // 4, SetTo, 64 * 65537),  # reset waypoint
                SetMemoryEPD(epd + 0x34 // 4, SetTo, 0),  # immobilize
                SetMemoryEPD(
                    epd + 0x4C // 4, Subtract, QCPlayer - f_getcurpl()
                ),  # modify unit's player
                SetMemoryEPD(epd + 0xDC // 4, Add, 0xA00000),  # stackable
                SetMemoryXEPD(epd + 0xA5 // 4, SetTo, 0, 0xFF00),  # uniqueIdentifier
            ]
        )
        getepd = Forward()
        for pi, p in enumerate(human):
            for j in range(QCCount):
                RawTrigger(
                    conditions=[Memory(0x6509B0, Exactly, p), i.Exactly(j)],
                    actions=SetMemory(
                        getepd + 20, SetTo, EPD(EPDList[pi][j].getValueAddr())
                    ),
                )
        VProc(
            epd,
            [
                getepd << SetDeaths(EPD(epd._varact + 16), SetTo, 0, 0),
                SetDeaths(EPD(epd._varact + 24), SetTo, 0x072D0000, 0),
            ],
        )
        if EUDIf()(Memory(0x57F1B0, Exactly, f_getcurpl())):
            f_dwwrite_epd(SetAlphaArray[i], _epd2alphaid(epd))
            getptr = Forward()
            for j in range(QCCount):
                RawTrigger(
                    conditions=i.Exactly(j),
                    actions=SetMemory(getptr + 16, SetTo, EPD(MyQC[j] + 20)),
                )
            VProc(
                ptr,
                [
                    getptr << SetDeaths(EPD(ptr._varact + 16), SetTo, 0, 0),
                    SetDeaths(EPD(ptr._varact + 24), SetTo, 0x072D0000, 0),
                ],
            )
        EUDEndIf()
    EUDSetContinuePoint()
    cp += 1
    _EUDEndHumanLoop()
    DoActions(
        [
            # RESTORE DATA OF QCLOCATION
            SetMemoryEPD(LocEPD, SetTo, LOC_TEMP[0]),
            SetMemoryEPD(LocEPD + 1, SetTo, LOC_TEMP[1]),
            SetMemoryEPD(LocEPD + 2, SetTo, LOC_TEMP[2]),
            SetMemoryEPD(LocEPD + 3, SetTo, LOC_TEMP[3]),
            SetMemoryEPD(LocEPD + 4, SetTo, LOC_TEMP[4]),
            # Editor Ability Flags
            SetMemoryX(0x661518 + q2, SetTo, 0, 0xFFFF * p2),
        ]
    )


def Start():
    """Call this function in onPluginStart."""
    global localcp
    localcp = f_dwread_epd(EPD(0x57F1B0))
    DoActions([SetMemory(act + 20, SetTo, localcp) for act in setlocalcp])
    _Respawn()


SelectIndex = Forward()


@EUDFunc
def _QueueGameCommand_Select():
    buf = Db(b"..\x09\x0112..")
    DoActions([SelectIndex << SetMemory(buf + 4, SetTo, 0xEDAC)])
    QueueGameCommand(buf + 2, 4)


@EUDFunc
def _QueueGameCommand_NSelect(n, ptrListepd):
    buf = Db(b"...\x091234567890123456789012345.......")
    DoActions([SetMemory(0x6509B0, SetTo, EPD(buf) + 1)])
    cw.writebyte(n)
    for _ in EUDLoopRange(n):
        unitepd = f_epdcunitread_epd(ptrListepd)
        unitIndex = _epd2alphaid(unitepd)
        uniquenessIdentifier = f_bread_epd(unitepd + 0xA5 // 4, 0xA5 % 4)
        targetID = unitIndex + f_bitlshift(uniquenessIdentifier, 11)
        b0, b1 = f_dwbreak(targetID)[2:4]
        cw.writebyte(b0)
        cw.writebyte(b1)
        ptrListepd += 1
    cw.flushdword()
    QueueGameCommand(buf + 3, f_bitlshift(n + 1, 1))


def _chunks(l, n):
    """Yield successive n-sized _chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


def _bitXY():
    for x in range(mapX):
        yield 2 ** x
    for y in range(mapY):
        yield 2 ** (16 + y)


def Main():
    """SQC Main Function."""
    global cp
    if QCSafety:
        something_bad_happened = Forward()
        QCBroken = EUDLightVariable()
        DoActions([QCBroken.SetNumber(0), cp.SetNumber(min(human))])
        _EUDHumanLoop()()
        for i in EUDLoopRange(QCCount):
            _restore_nextptr, _skip = Forward(), Forward()
            for pi, p in enumerate(human):
                for j, epd in enumerate(EPDList[pi]):
                    _t, _next = Forward(), Forward()
                    _t << RawTrigger(
                        conditions=[Memory(0x6509B0, Exactly, p), i.Exactly(j)],
                        actions=[
                            SetMemory(0x6509B0, SetTo, 0x4C // 4),
                            epd.QueueAddTo(EPD(0x6509B0)),
                            SetNextPtr(_t, epd.GetVTable()),
                            SetNextPtr(epd.GetVTable(), _skip),
                            SetMemory(_restore_nextptr + 16, SetTo, EPD(_t) + 1),
                            SetMemory(_restore_nextptr + 20, SetTo, _next),
                        ],
                    )
                    _next << NextTrigger()
            _skip << RawTrigger(actions=[_restore_nextptr << SetNextPtr(0, 0)])
            if EUDIfNot()(DeathsX(CurrentPlayer, Exactly, cp, 0, 0xFF)):
                RawTrigger(
                    nextptr=something_bad_happened, actions=QCBroken.SetNumber(1)
                )
            if EUDElseIf()(DeathsX(CurrentPlayer, Exactly, 0, 0, 0xFF00)):
                RawTrigger(
                    nextptr=something_bad_happened, actions=QCBroken.SetNumber(1)
                )
            EUDEndIf()
        EUDSetContinuePoint()
        cp += 1
        _EUDEndHumanLoop()
        something_bad_happened << NextTrigger()
        f_setcurpl(0)
        if EUDIf()(QCBroken >= 1):
            EUDPlayerLoop()()
            DoActions(DisplayText("\x13\x08SQC FATAL ERROR! QC Unit has been removed."))
            EUDEndPlayerLoop()
            DoActions(
                [
                    SetMemoryEPD(epd + 0x110 // 4, SetTo, 1)
                    for epd in FlattenList(EPDList)
                ]
            )
            _Respawn()
        EUDEndIf()

    origcp = f_getcurpl()
    InitList[0].insert(0, setlocalcp)

    # Initialization
    for f in InitList:
        try:
            f()
        except (TypeError):
            DoActions(f)

    # 0x6284B8: (desync) *CUnits of units in selection (4 bytes * 12 units)
    SelCount, SelMem = EUDVariable(), EUDArray(12)
    QGCActivated = EUDLightVariable()
    skipSelSave = Forward()
    global MyQC
    for i in range(QCCount):  # skip if QC
        EUDJumpIf([MyQC[i] << Memory(0x6284B8, Exactly, 0)], skipSelSave)
    DoActions([SelCount.SetNumber(0), SetMemory(0x6509B0, SetTo, EPD(0x6284B8))])
    for i in EUDLoopRange(12):  # backup units in selection
        EUDJumpIf(Deaths(CurrentPlayer, Exactly, 0, 0), skipSelSave)
        DoActions(
            [
                SetMemoryEPD(EPD(SelMem) + i, SetTo, f_cunitread_cp(0)),
                SetMemory(0x6509B0, Add, 1),
                SelCount.AddNumber(1),
            ]
        )
    skipSelSave << NextTrigger()

    RC = Db(b"...\x14XXYY\0\0\xE4\0\x00")
    QGCActivated << 0

    global QCAlphaID, pv5, _once

    for n, l in enumerate(_chunks(QCList, mapXY)):
        DoActions(SetMemory(RC + 4, SetTo, 64 * 65537))
        for b, sl in zip(_bitXY(), l):
            IF, condition, _ = sl
            IF()(condition)
            DoActions(SetMemory(RC + 4, Add, b))
            EUDEndIf()
        if EUDIf()(Memory(RC + 4, AtLeast, 64 * 65537 + 1)):
            DoActions([QCAlphaID[n] << SetMemory(SelectIndex + 20, SetTo, 0xEDAC)])
            _QueueGameCommand_Select()
            QueueGameCommand(RC + 3, 10)  # RightClick
            QGCActivated << 1
        EUDEndIf()

    _EUDHumanLoop()()
    waypoint = EUDVariable()
    for n, l in enumerate(_chunks(QCList, mapXY)):
        resetnextptr = Forward()
        setwaypoint = [Forward() for _ in human] + [Forward()]
        for pi, p in enumerate(human):
            setwaypoint[pi] << RawTrigger(
                conditions=Memory(0x6509B0, Exactly, p),
                actions=[
                    waypoint.SetNumber(4),
                    EPDList[pi][n].QueueAddTo(waypoint),
                    SetNextPtr(setwaypoint[pi], EPDList[pi][n].GetVTable()),
                    SetNextPtr(EPDList[pi][n].GetVTable(), setwaypoint[len(human)]),
                    SetMemory(resetnextptr + 16, SetTo, EPD(setwaypoint[pi]) + 1),
                    SetMemory(resetnextptr + 20, SetTo, setwaypoint[pi + 1]),
                ],
            )
        setwaypoint[len(human)] << RawTrigger(
            actions=[resetnextptr << SetNextPtr(0, 0)]
        )
        if EUDIf()(MemoryEPD(waypoint, AtLeast, 64 * 65537 + 1)):
            f_dwsubtract_epd(waypoint, 64 * 65537)
            for b, sl in zip(_bitXY(), l):
                _, _, f = sl
                if EUDIf()(MemoryXEPD(waypoint, Exactly, b, b)):
                    try:
                        f()
                    except (TypeError):
                        DoActions(f)
                EUDEndIf()
            f_dwwrite_epd(waypoint, 64 * 65537)
        EUDEndIf()
    EUDSetContinuePoint()
    DoActions([cp.AddNumber(1), pv5.AddNumber(5)])
    _EUDEndHumanLoop()

    # Wrap-up
    for f in AfterList:
        try:
            f()
        except (TypeError):
            if f:
                DoActions(f)
    for offset in KeyOffset:
        _KeyUpdate(offset)
    for value in MouseOffset:
        _MouseUpdate(value)

    # restore unit selection from array
    if EUDIf()([SelCount >= 1, QGCActivated >= 1]):
        _QueueGameCommand_NSelect(SelCount, SelMem._epd)
    EUDEndIf()

    f_setcurpl(origcp)
