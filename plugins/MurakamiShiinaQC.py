# -*- coding: utf-8 -*-
import re
from itertools import product
from math import ceil
from struct import unpack

from eudplib import *

try:
    from loc import SetLoc
except (ImportError):

    def _locfgen(mod1, mod2, mod3, mod4):

        @EUDFunc
        def _locf(epd, x, y):
            act = Forward()

            VProc(epd, [
                epd.AddNumber(EPD(0x58DC60)),
                epd.QueueAssignTo(EPD(act) + 4)
            ])
            VProc(x, x.QueueAssignTo(EPD(act) + 5))

            VProc(epd, [
                epd.AddNumber(1),
                SetMemory(epd._varact + 16, Add, 8)
            ])
            VProc(y, y.QueueAssignTo(EPD(act) + 5 + 8))

            VProc(epd, [
                epd.AddNumber(1),
                SetMemory(epd._varact + 16, Add, 8)
            ])
            VProc(x, SetMemory(x._varact + 16, Add, 16))

            VProc(epd, [
                epd.AddNumber(1),
                SetMemory(epd._varact + 16, Add, 8)
            ])
            VProc(y, SetMemory(y._varact + 16, Add, 16))

            DoActions([
                act << SetMemory(0, mod1, 0),
                SetMemory(0, mod2, 0),
                SetMemory(0, mod3, 0),
                SetMemory(0, mod4, 0),
            ])

        return _locf

    _SetLoc = _locfgen(SetTo, SetTo, SetTo, SetTo)

    def SetLoc(locID, x, y):
        _SetLoc(locID * 5, x, y)


def EncPlayer(s):  # str to int (Player)
    PlayerDict = {
        'p1': 0, 'p2': 1, 'p3': 2, 'p4': 3, 'p5': 4, 'p6': 5, 'p7': 6, 'p8': 7, 'p9': 8, 'p10': 9, 'p11': 10, 'p12': 11,
        'player1': 0, 'player2': 1, 'player3': 2, 'player4': 3,
        'player5': 4, 'player6': 5, 'player7': 6, 'player8': 7,
        'player9': 8, 'player10': 9, 'player11': 10, 'player12': 11,
        'neutral': 11,
        'currentplayer': 13,
        'foes': 14,
        'allies': 15,
        'neutralplayers': 16,
        'allplayers': 17,
        'force1': 18, 'force2': 19, 'force3': 20, 'force4': 21,
        'nonalliedvictoryplayers': 26
    }
    if s.lower() in PlayerDict:
        return PlayerDict[s.lower()]
    else:
        return int(s)


@EUDFunc
def _cunitreader():
    ptr, epd = EUDVariable(), EUDVariable()
    addact = Forward()
    DoActions([
        ptr.SetNumber(0x59CCA8),
        epd.SetNumber(EPD(0x59CCA8)),
        SetMemory(addact + 20, SetTo, 0),
    ])
    for i in range(10, -1, -1):
        RawTrigger(
            conditions=[
                Deaths(CurrentPlayer, AtLeast, 0x59CCA8 + 336 * 2**i, 0)
            ],
            actions=[
                SetDeaths(CurrentPlayer, Subtract, 336 * 2**i, 0),
                ptr.AddNumber(336 * 2**i),
                epd.AddNumber(84 * 2**i),
                SetMemory(addact + 20, Add, 336 * 2**i),
            ]
        )

    DoActions([addact << SetDeaths(CurrentPlayer, Add, 0, 0)])

    EUDReturn(ptr, epd)


def f_dwepdcunitread_cp(cpo):
    if not isinstance(cpo, int) or cpo != 0:
        DoActions(SetMemory(0x6509B0, Add, cpo))
    ptr, epd = _cunitreader()
    if not isinstance(cpo, int) or cpo != 0:
        DoActions(SetMemory(0x6509B0, Add, -cpo))
    return ptr, epd


@EUDFunc
def _cunitcpreader():
    ret, retepd = EUDVariable(), EUDVariable()

    # Common comparison rawtrigger
    PushTriggerScope()
    cmpc = Forward()
    cmp_number = cmpc + 8
    cmpact = Forward()

    cmptrigger = Forward()
    cmptrigger << RawTrigger(
        conditions=[
            cmpc << Deaths(CurrentPlayer, AtMost, 0, 0)
        ],
        actions=[
            cmpact << SetMemory(cmptrigger + 4, SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20
    PopTriggerScope()

    # static_for
    chain1 = [Forward() for _ in range(11)]
    chain2 = [Forward() for _ in range(11)]

    # Main logic start
    error = 1
    SeqCompute([
        (EPD(cmp_number), SetTo, 0x59CCA8 + 336 * (0x7FF - error)),
        (ret, SetTo, 0x59CCA8 + 336 * (0x7FF - error)),
        (retepd, SetTo, EPD(0x59CCA8) + 84 * (0x7FF - error))
    ])

    readend = Forward()

    for i in range(10, -1, -1):
        nextchain = chain1[i - 1] if i > 0 else readend
        epdsubact = [retepd.AddNumber(-84 * 2 ** i)]
        epdaddact = [retepd.AddNumber(84 * 2 ** i)]

        chain1[i] << RawTrigger(
            nextptr=cmptrigger,
            actions=[
                SetMemory(cmp_number, Subtract, 336 * 2 ** i),
                SetNextPtr(cmptrigger, chain2[i]),
                SetMemory(cmpact_ontrueaddr, SetTo, nextchain),
                ret.SubtractNumber(336 * 2 ** i),
            ] + epdsubact
        )

        chain2[i] << RawTrigger(
            actions=[
                SetMemory(cmp_number, Add, 336 * 2 ** i),
                ret.AddNumber(336 * 2 ** i),
            ] + epdaddact
        )

    readend << NextTrigger()

    RawTrigger(
        conditions=ret.AtMost(0x59CCA7),
        actions=[
            ret.SetNumber(0),
            retepd.SetNumber(0),
        ]
    )
    RawTrigger(
        conditions=ret.AtLeast(0x628299),
        actions=[
            ret.SetNumber(0),
            retepd.SetNumber(0),
        ]
    )

    return ret, retepd


def f_dwepdcunitread_cp_safe(cpo):
    if not isinstance(cpo, int) or cpo != 0:
        DoActions(SetMemory(0x6509B0, Add, cpo))
    ptr, epd = _cunitcpreader()
    if not isinstance(cpo, int) or cpo != 0:
        DoActions(SetMemory(0x6509B0, Add, -cpo))
    return ptr, epd


def f_dwcunitread_cp_safe(cpo):
    return f_dwepdcunitread_cp_safe(cpo)[0]


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
cmpScreenX, cmpMouseX, cmpScreenY, cmpMouseY = [Forward() for i in range(4)]
VK, VK_USE, VK_EPD = [None for _ in range(256)], [0 for _ in range(256)], [0 for _ in range(64)]


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
    global safety_option
    safety_option = 1
    # get map size & human player
    global mapX, mapY, humans
    chkt = GetChkTokenized()
    dim, ownr = chkt.getsection('DIM'), chkt.getsection('OWNR')
    mapX, mapY = [k.bit_length() + 3 for k in unpack("<HH", dim[0:4])]
    humans = [p for p in range(12) if ownr[p] == 6]

    global QCUnitID, init_loc, QCPlayer, init_x, init_y
    QCUnitID, init_loc, QCPlayer = 58, 0, 8  # use Valkyrie, loc 0, P9 in default
    init_x, init_y = 8, 8  # create QC units at grid(2, 2)

    global DeathUnits, Trg, VTrg, VTrgLoc
    DeathUnits, Trg, VTrg, VTrgLoc = [[] for i in range(4)]

    for key, value in settings.items():
        V, Con, Ret, Point = [d.strip() for d in value.split(',')], '', '', ''

        # default settings
        if key == 'QCUnitID':
            try:
                QCUnitID = int(EncodeUnit(value.strip()))
            except EPError:
                QCUnitID = int(EncodeUnit(int(value.strip())))
            continue
        elif key == 'QC_XY':
            init_x, init_y = int(V[0]), int(V[1])
            continue
        elif key == 'QCPlayer':
            QCPlayer = EncPlayer(value.strip())
            continue
        elif key.lower() == 'qc_safety':
            safety_option = int(V[0])
            continue

        ConCount = 0
        conditions_ = [_.strip() for _ in key.split(';')]
        for condition_ in conditions_:
            if condition_ == '마우스' or condition_.lower() == 'mouse':
                if len(V) >= len(humans):
                    print('MouseMovelocation enabled: ',
                        ['P{}:{}'.format(h + 1, V[i]) for i, h in enumerate(humans)])
                else:
                    print('※ Error: Mouse following locations should be assigned as much as human players',
                        'Mouse coordinates will send to death counter! (%s)' % (V[0]))
                Con += '(MouseMoved())'
                ConCount += 1
                Point = re.sub(r'(0[xX][0-9a-fA-F]+)', r'f_dwread_epd_safe(EPD(\1))',
                            '0x62848C + 0x6CDDC4 + 65536 * (0x6284A8 + 0x6CDDC8) + 65537 * 64')
            elif condition_.upper() in KeyCodeDict:  # KeyPressDetect
                VirtualKeyValue = KeyCodeDict[condition_.upper()]
                Con += '(VK[{}] == 1)'.format(VirtualKeyValue)
                ConCount += 1
                global VK, VK_USE, VK_EPD
                VK[VirtualKeyValue] = EUDVariable()
                VK_USE[VirtualKeyValue] = 1
                VK_EPD[VirtualKeyValue // 4] = 1
            else:
                C = [_.strip() for _ in condition_.split(',')]
                if C[0].lower() == 'xy':
                    try:
                        Point = '%s + 65536 * (%s) + 65537 * 64' % (C[1], C[2])
                    except IndexError:
                        Point = '{} + 65537 * 64'.format(C[1])
                    Point = re.sub(r'(0[xX][0-9a-fA-F]+)',
                                    r'f_dwread_epd(EPD(\1))', Point)
                elif C[0].lower() == 'val':
                    Point = 'val: {0} % 1000 + ({0}) // 1000 * 65536 + 65537 * 64'.format(C[1])
                    Point = re.sub(r'(0[xX][0-9a-fA-F]+)',
                                    r'f_dwread_epd(EPD(\1))', Point)
                elif re.match(r'0[xX][0-9a-fA-F]+', C[0]):
                    try:
                        Con += '(Memory(%s, %s, %s))' % (C[0], C[1], C[2])
                    except IndexError:
                        Con += '(f_dwread_epd(EPD(%s))&%s==%s)' % (
                            C[0], C[1], C[1])
                    ConCount += 1
                else:
                    Con += '({})'.format(condition_)
                    ConCount += 1

        if Con == '':
            Con = 'Always()'
        elif ConCount >= 2:
            Con = 'EUDSCAnd()' + Con + '()'

        if Point != '':
            if Point[:5] == 'val: ':
                try:
                    UNIT = int(EncodeUnit(V[0]))
                except EPError:
                    UNIT = int(EncodeUnit(int(V[0])))
                Ret = '''PosX, PosY = f_dwbreak(PosXY)[0:2]
DoActions([
    SetDeaths(player, Add, PosX, {0}), SetDeaths(player, Add, PosY * 1000, {0})
])'''.format(UNIT)
                DeathUnits.extend([UNIT])
                Point = Point[5:]
            elif len(V) >= len(humans):  # return locations
                V_L = []
                for v in V:
                    try:
                        V_L.extend([int(GetLocationIndex(v))])
                    except KeyError:
                        V_L.extend([int(v)])
                V = V_L
                Ret = '''PosX, PosY = f_dwbreak(PosXY)[0:2]
SetLoc(VTrgLoc[i][p], PosX, PosY)'''
            elif len(V) == 1:  # return death
                try:
                    UNIT = int(EncodeUnit(V[0]))
                except EPError:
                    UNIT = int(EncodeUnit(int(V[0])))
                Ret = 'DoActions(SetDeaths(player, Add, PosXY, {}))'.format(UNIT)
                DeathUnits.extend([UNIT])
            else:  # return deaths
                try:
                    UNIT0 = int(EncodeUnit(V[0]))
                except EPError:
                    UNIT0 = int(EncodeUnit(int(V[0])))
                try:
                    UNIT1 = int(EncodeUnit(V[1]))
                except EPError:
                    UNIT1 = int(EncodeUnit(int(V[1])))
                Ret = '''PosX, PosY = f_dwbreak(PosXY)[0:2]
DoActions([
    SetDeaths(player, Add, PosX, {}), SetDeaths(player, Add, PosY, {})
])'''.format(UNIT0, UNIT1)
                DeathUnits.extend([UNIT0, UNIT1])
            VTrg.append((Point, Con, Ret))
            VTrgLoc.append(V)
        else:
            try:
                UNIT = int(EncodeUnit(V[0]))
            except EPError:
                UNIT = int(EncodeUnit(int(V[0])))
            Ret = 'SetDeaths(player, Add, %s, %s)' % (V[1], UNIT)
            DeathUnits.extend([UNIT])
            Trg.append((Con, Ret))
    global QCNum
    QCNum = len(VTrg) + ceil(len(Trg) / (mapX + mapY))
    DeathUnits = set(DeathUnits)

    print("[MSQC] map dim. %ux%u, %u humans, %u QCUnits per capita" %
          (2 ** (mapX - 4), 2 ** (mapY - 4), len(humans), QCNum))


onInit()

QCNewIndex = [Forward() for _ in range(QCNum)]
bw = EUDByteWriter()
pOrd = EUDVariable()
QC_EPD = EUDArray(QCNum * len(humans))  # QCUnitArray
MyQC = EUDArray(QCNum)


@EUDFunc
def f_epd2newindex(epd):
    return (epd * 4 + 0x58A364 - 0x59CCA8) // 336 + 1


@EUDFunc
def initQC():
    if EUDPlayerLoop()():
        DoActions(DisplayText("\x13\x16Respawning QC Units..."))
    EUDEndPlayerLoop()
    loc = EUDArray(5)  # temporary saves Locations coordinates
    loc_epd = EPD(0x58DC60) + init_loc * 5
    loc_flags = f_dwread_epd(loc_epd + 4)
    DoActions([
        SetMemory(0x664080 + QCUnitID * 4, SetTo, 0x38000004),  # Advanced Flags
        # Units.dat - Unit Dimensions
        SetMemory(0x6617C8 + QCUnitID * 8, SetTo, 0x20002),
        SetMemory(0x6617CC + QCUnitID * 8, SetTo, 0x20002),
        # Units.dat - Building Dimensions
        SetMemory(0x662860 + QCUnitID * 4, SetTo, 0),
        # temp location to create QCUnits
        SetMemory(0x6509B0, SetTo, loc._epd),
        SetDeaths(CurrentPlayer, SetTo, f_dwread_epd(loc_epd + 0), 0),
        SetMemory(0x6509B0, Add, 1),
        SetDeaths(CurrentPlayer, SetTo, f_dwread_epd(loc_epd + 1), 0),
        SetMemory(0x6509B0, Add, 1),
        SetDeaths(CurrentPlayer, SetTo, f_dwread_epd(loc_epd + 2), 0),
        SetMemory(0x6509B0, Add, 1),
        SetDeaths(CurrentPlayer, SetTo, f_dwread_epd(loc_epd + 3), 0),
        SetMemory(0x6509B0, Add, 1),
        SetDeaths(CurrentPlayer, SetTo, loc_flags, 0),
    ])
    q, mod = divmod(QCUnitID, 4)
    q2, m2 = divmod(QCUnitID, 2)
    f_bwrite_epd(EPD(0x6636B8) + q, mod, 130)  # Units.dat - Ground Weapon
    f_bwrite_epd(EPD(0x6616E0) + q, mod, 130)  # Units.dat - Air Weapon
    f_bwrite_epd(EPD(0x662DB8) + q, mod, 0)  # Units.dat - Seek Range
    f_bwrite_epd(EPD(0x663238) + q, mod, 0)  # Units.dat - Sight Range
    f_wwrite_epd(EPD(0x661518) + q2, 2*m2, 0x1CF)  # Editor Ability Flags
    f_bwrite_epd(EPD(0x660FC8) + q, mod, 0xC5)  # MovementFlags
    f_bwrite_epd(EPD(0x663150) + q, mod, 0x13)  # Elevation
    SetLoc(init_loc, init_x * 32, init_y * 32)
    DoActions([
        SetMemoryEPD(loc_epd + 4, SetTo, loc_flags & 0xFFFF),
        MoveLocation(init_loc + 1, 227, 11, init_loc + 1),
    ])

    global humanArray
    pID, humanArray = f_dwread_epd(EPD(0x57F1B0)), EUDArray(humans)
    IndexArray = EUDArray([QCNewIndex[n] for n in range(QCNum)])
    for p in EUDLoopRange(len(humans)):
        player = humanArray[p]
        for n in EUDLoopRange(QCNum):
            DoActions(SetMemory(0x6509B0, SetTo, EPD(0x628438)))
            ptr, epd = f_dwepdcunitread_cp(0)
            DoActions([
                CreateUnit(1, QCUnitID, init_loc + 1, P8),
                SetMemory(0x6509B0, SetTo, epd + 0x28 // 4),
            ])
            x, y = f_dwbreak(f_dwread_cp(0))[0:2]
            SetLoc(init_loc, x, y)
            DoActions([
                GiveUnits(1, QCUnitID, P8, init_loc + 1, QCPlayer),
                SetMemory(0x6509B0, Subtract, (0x28 - 0x10) // 4),
                SetDeaths(CurrentPlayer, SetTo, 64 * 65537, 0),  # reset waypoint
                SetMemory(0x6509B0, Add, (0x34 - 0x10) // 4),
                SetDeaths(CurrentPlayer, SetTo, 0, 0),  # immobilize
                SetMemory(0x6509B0, Add, (0x4C - 0x34) // 4),
                SetDeaths(CurrentPlayer, Subtract, QCPlayer - player, 0),  # modify unit's player
                SetMemory(0x6509B0, Add, (0xDC - 0x4C) // 4),
                SetDeaths(CurrentPlayer, Add, 0xA00000, 0),  # stackable
            ])
            f_bwrite_epd(epd + 0xA5 // 4, 1, 0)  # uniqueIdentifier
            QC_EPD[n + QCNum * p] = epd
            if EUDIf()(pID == player):
                pOrd << p  # player's own order alomg humans (desync)
                MyQC[n] = ptr
                DoActions(SetMemory(IndexArray[n] + 20, SetTo, f_epd2newindex(epd)))
            EUDEndIf()
    DoActions([
        SetMemoryEPD(loc_epd + 0, SetTo, loc[0]),
        SetMemoryEPD(loc_epd + 1, SetTo, loc[1]),
        SetMemoryEPD(loc_epd + 2, SetTo, loc[2]),
        SetMemoryEPD(loc_epd + 3, SetTo, loc[3]),
        SetMemoryEPD(loc_epd + 4, SetTo, loc[4]),
        MoveLocation(init_loc + 1, 227, 11, init_loc + 1),
    ])
    f_wwrite_epd(EPD(0x661518) + q2, 2*m2, 0)  # Editor Ability Flags
    f_bwrite_epd(EPD(0x6637A0) + q, mod, 0)  # Group Flags


def onPluginStart():
    initQC()


Select_NewIndex = Forward()


@EUDFunc
def QGC_Select():
    buf = Db(b'..\x09\x0112..')
    DoActions([Select_NewIndex << SetMemory(buf + 4, SetTo, 0xEDAC)])
    QueueGameCommand(buf + 2, 4)


@EUDFunc
def QGC_NSelect(n, ptrListepd):
    buf = Db(b'\x090123456789012345678901234')
    bw.seekoffset(buf + 1)
    bw.writebyte(n)
    f_dwwrite_epd(EPD(0x6509B0), ptrListepd)
    for _ in EUDLoopRange(n):
        unitptr, unitepd = f_dwepdcunitread_cp(0)
        unitIndex = (unitptr - 0x59CCA8) // 336 + 1
        uniquenessIdentifier = f_bread_epd(unitepd + 0xA5 // 4, 0xA5 % 4)
        targetID = unitIndex | f_bitlshift(uniquenessIdentifier, 11)
        b0, b1 = f_dwbreak(targetID)[2:4]
        bw.writebyte(b0)
        bw.writebyte(b1)
        f_dwadd_epd(EPD(0x6509B0), 1)
    bw.flushdword()
    QueueGameCommand(buf, 2 * (n + 1))


SelNum, QGCSwitch = EUDCreateVariables(2)  # number of units in selection
SelMem = EUDArray(12)  # backup selected units


def getQC(num):
    mod = num % (mapX + mapY)
    if mod < mapY:
        x = 2 ** (mapY - mod + 15)
    else:
        x = 2 ** (mapX + mapY - mod - 1)
    return x


def beforeTriggerExec():
    DoActions([SetDeaths(human, SetTo, 0, unit)
               for human in humans for unit in DeathUnits])
    if safety_option == 1:
        global ERROR_OCCURED, CRITICAL_ERROR
        ERROR_OCCURED = EUDLightVariable()
        global checkIndex, checkPlayer
        checkIndex = EUDVariable()
        checkPlayer = EUDVariable()
        global check
        check = QC_EPD[checkIndex]
        CRITICAL_ERROR = ")(".join(
            ["EUDSCOr("] + ["MemoryEPD(QC_EPD[{}] + 0xC // 4, Exactly, 0)".format(i) for i in range(QC_EPD.length)]
            + ["f_bread_epd(check + 0x4C // 4, 0) != checkPlayer"] + [")"])
        # ")(".join(
        #     ["EUDSCOr("] + ["MemoryEPD(check + 0xC // 4, Exactly, 0)"]
        #     + ["MemoryEPD(QC_EPD[{}] + 0x4C // 4, Exactly, 0x4000030B)".format(i) for i in range(QC_EPD.length)] + [")"])
        if EUDIf()(eval(CRITICAL_ERROR)):
            ERROR_OCCURED << 1
            if EUDPlayerLoop()():
                DoActions(DisplayText("\x13\x08MSQC FATAL ERROR! QC Unit has been removed."))
            EUDEndPlayerLoop()
            for i in EUDLoopRange(QC_EPD.length):
                f_dwwrite_epd(QC_EPD[i] + 0x110 // 4, 1)
            initQC()
        if EUDElse()():
            ERROR_OCCURED << 0
            b4()
        EUDEndIf()
    else:
        b4()


def b4():
    oldcp = f_getcurpl()

    VK_ARRAY = EPD(0x596A18)
    for e, epd in enumerate(VK_EPD):
        if epd == 1:
            if e in [12, 13, 14]:  # Number key presses should be tackled specially (read-only)
                _end = Forward()
                NumKeyList = list(set([x for i in range(4) if isUnproxyInstance(VK[i + e * 4], EUDVariable) for x in product([0, 1], repeat=4) if x[i] == 1]))
                NumKeyList.sort(key=sum)
                NumKeyTrig = [Forward() for _ in NumKeyList]
                RawTrigger(
                    actions=[
                        [SetNextPtr(NumKeyTrig[n], NumKeyTrig[n+1]) for n in range(len(NumKeyList) - 1)],
                        [[VK[i + e * 4].SetNumber(0) if isUnproxyInstance(VK[i + e * 4], EUDVariable) else []] for i in range(4)],
                    ]
                )
                for n, x in enumerate(NumKeyList):
                    NumKeyTrig[n] << RawTrigger(
                        conditions=MemoryEPD(VK_ARRAY + e, Exactly, sum([256 ** i if t == 1 else 0 for i, t in enumerate(x)])),
                        actions=[
                            [[VK[i + e * 4].SetNumber(1) if isUnproxyInstance(VK[i + e * 4], EUDVariable) and t == 1 else []] for i, t in enumerate(x)],
                            [SetNextPtr(NumKeyTrig[n], _end) if n + 1 < len(NumKeyList) else []],
                        ],
                    )
                _end << NextTrigger()

            else:
                RESTORE = Forward()
                RawTrigger(
                    actions=[
                        SetMemory(RESTORE + 20, SetTo, 0),
                        [[VK[i + e * 4].SetNumber(0) if isUnproxyInstance(VK[i + e * 4], EUDVariable) else []] for i in range(4)],
                    ]
                )
                for i in range(3, -1, -1):
                    RawTrigger(
                        conditions=MemoryEPD(VK_ARRAY + e, AtLeast, 256 ** i),
                        actions=[
                            SetMemoryEPD(VK_ARRAY + e, Subtract, 256 ** i),
                            SetMemory(RESTORE + 20, Add, 256 ** i),
                            [VK[i + e * 4].SetNumber(1) if isUnproxyInstance(VK[i + e * 4], EUDVariable) else []],
                        ]
                    )
                RawTrigger(actions=[RESTORE << SetMemoryEPD(VK_ARRAY + e, Add, 0xEDAC)])

    # 0x6284B8: (desync) *CUnits of units in selection (4 bytes * 12 units)
    fin = Forward()
    for n in range(QCNum):  # don't save if QC units are selected
        EUDJumpIf(Memory(0x6284B8, Exactly, MyQC[n]), fin)
    DoActions([
        SelNum.SetNumber(0),
        SetMemory(0x6509B0, SetTo, EPD(0x6284B8)),
    ])
    for i in EUDLoopRange(12):  # backup units in selection
        EUDJumpIf(Deaths(CurrentPlayer, Exactly, 0, 0), fin)
        DoActions([
            SetMemoryEPD(SelMem._epd + i, SetTo, f_dwcunitread_cp_safe(0)),
            SetMemory(0x6509B0, Add, 1),
            SelNum.AddNumber(1),
        ])
    fin << NextTrigger()

    RC = Db(b'...\x14XXYY\0\0\xE4\0\x00')

    QGCSwitch << 0
    f_setcurpl(EPD(RC) + 1)
    for i, L in enumerate(VTrg):  # VTrg[n]: (Point, Con, Ret)
        if EUDIf()([eval(L[1])]):
            if L[1] == 'MouseMoved(),':
                ScreenX = f_dwread_epd_safe(EPD(0x62848C))
                ScreenY = f_dwread_epd_safe(EPD(0x6284A8))
                MouseX = f_dwread_epd_safe(EPD(0x6CDDC4))
                MouseY = f_dwread_epd_safe(EPD(0x6CDDC8))
                DoActions([
                    SetMemory(cmpScreenX + 8, SetTo, ScreenX),
                    SetMemory(cmpMouseX + 8, SetTo, MouseX),
                    SetMemory(cmpScreenY + 8, SetTo, ScreenY),
                    SetMemory(cmpMouseY + 8, SetTo, MouseY)
                ])
                f_dwwrite_cp(0, ScreenX + MouseX + 65536 * (ScreenY + MouseY) + 65537 * 64)
            else:
                f_dwwrite_cp(0, eval(L[0]))
            DoActions([QCNewIndex[i] << SetMemory(Select_NewIndex + 20, SetTo, 0xEDAC)])
            QGC_Select()
            QueueGameCommand(RC + 3, 10)  # RightClick
            QGCSwitch << 1
        EUDEndIf()

    for n in range(QCNum - len(VTrg)):  # Trg[n]: (Con, Ret)
        f_dwwrite_cp(0, 64 * 65537)
        for i, L in enumerate(Trg[n * (mapX + mapY):min(len(Trg), (n + 1) * (mapX + mapY))]):
            if EUDIf()([eval(L[0])]):  # Add coordinates for RightClick if conditions are fulfilled
                f_dwadd_cp(0, getQC(i))
            EUDEndIf()
        if EUDIf()(Deaths(CurrentPlayer, AtLeast, 64 * 65537 + 1, 0)):
            DoActions([QCNewIndex[n + len(VTrg)] << SetMemory(Select_NewIndex + 20, SetTo, 0xEDAC)])
            QGC_Select()
            QueueGameCommand(RC + 3, 10)  # RightClick
            QGCSwitch << 1
        EUDEndIf()

    for p, player in enumerate(humans):
        for i, L in enumerate(VTrg):  # VTrg[n]: ('Point', Con, Ret)
            f_setcurpl(QC_EPD[i + QCNum * p] + 4)
            if EUDIf()(Deaths(CurrentPlayer, AtLeast, 64 * 65537 + 1, 0)):
                PosXY = f_dwread_cp(0) - 64 * 65537
                exec(L[2])
            EUDEndIf()
        for n in range(QCNum - len(VTrg)):  # Trg[n]: (Con, Ret)
            f_setcurpl(QC_EPD[n + len(VTrg) + QCNum * p] + 4)
            if EUDIf()(Deaths(CurrentPlayer, AtLeast, 64 * 65537 + 1, 0)):
                DoActions(SetDeaths(CurrentPlayer, Subtract, 64 * 65537, 0))
                for i, L in enumerate(Trg[n * (mapX + mapY):min(len(Trg), (n + 1) * (mapX + mapY))]):
                    if EUDIf()(Deaths(CurrentPlayer, AtLeast, getQC(i), 0)):
                        DoActions([
                            eval(L[1]),
                            SetDeaths(CurrentPlayer, Subtract, getQC(i), 0),
                        ])
                    EUDEndIf()
            EUDEndIf()

    f_setcurpl(oldcp)


def afterTriggerExec():
    if safety_option == 1:
        if EUDIfNot()(
            EUDSCOr()
            (ERROR_OCCURED == 1)
            (eval(CRITICAL_ERROR))
            ()
        ):
            a4()
        EUDEndIf()
        checkCounter = EUDLightVariable()
        DoActions([
            checkIndex.AddNumber(1),
            checkCounter.AddNumber(1),
        ])
        RawTrigger(
            conditions=checkIndex.AtLeast(QC_EPD.length),
            actions=checkIndex.SetNumber(0),
        )
        if EUDIf()(checkCounter.AtLeast(QCNum)):
            DoActions([
                checkCounter.SetNumber(0),
                checkPlayer.SetNumber(humanArray[checkIndex // QCNum]),
            ])
        EUDEndIf()
    else:
        a4()


def a4():
    # if QC unit's waypoint isn't (64, 64), it means at least 1 of conditions are fulfilled, so recover original unit selection and reset waypoints
    SelSwitch = EUDVariable()
    SelSwitch << 0
    for p in range(len(humans)):
        for n in range(QCNum):  # reset waypoints
            if EUDIfNot()(MemoryEPD(QC_EPD[n + QCNum * p] + 4, Exactly, 64 * 65537)):
                f_dwwrite_epd(QC_EPD[n + QCNum * p] + 4, 64 * 65537)
                if EUDIf()(pOrd == p):
                    SelSwitch << 1
                EUDEndIf()
            EUDEndIf()
    if EUDIf()(SelNum > 0):  # recovers unit selection from array
        if EUDIf()(EUDSCOr()(SelSwitch == 1)(QGCSwitch == 1)()):
            QGC_NSelect(SelNum, SelMem._epd)
        EUDEndIf()
    EUDEndIf()
