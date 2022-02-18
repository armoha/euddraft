from itertools import combinations
from operator import itemgetter

from eudplib import *
import sys

"""[chatEvent]
__addr__ : 0x58D900
__encoding__ : UTF-8, cp949
message 1 : value 1
message 2 : value 2
^start.*middle.*end$ : value
message 3 : value 3
..."""
Addr = 0x58D900
lenAddr, ptrAddr, patternAddr = 0, 0, 0
minlen, maxlen = 78, 0


def onInit():
    global Addr, lenAddr, ptrAddr, patternAddr
    chatList, regexList = [], []
    chatEncoding = set(["UTF-8"])
    sys.stdout.reconfigure(encoding="utf-8")

    def delrem4(x):
        return x - x % 4

    for k, v in settings.items():
        rL = k.split(".*")
        if k[:1] == "^" and k[-1:] == "$" and len(rL) == 3:
            regexList.append([rL[0][1:], rL[1], rL[2][:-1], int(v, 0)])
        elif k == "__addr__":
            Addr = delrem4(int(v, 0))  # 주소를 정수로 가져온다.
        elif k == "__lenAddr__":
            lenAddr = delrem4(int(v, 0))  # 주소를 정수로 가져온다.
        elif k == "__ptrAddr__":
            ptrAddr = delrem4(int(v, 0))  # 주소를 정수로 가져온다.
        elif k == "__patternAddr__":
            patternAddr = delrem4(int(v, 0))  # 주소를 정수로 가져온다.
        elif k == "__encoding__":
            chatEncoding = set([_.strip() for _ in v.split(",")])
        else:
            if v == "1" or v == "0":
                raise EPError("오류: 더할 값은 2 이상이어야 합니다.")
            chatList.append([k.strip(), int(v, 0)])

    detect_duplicates = list()
    for v in (Addr, lenAddr, ptrAddr, patternAddr):
        if v >= 1:
            detect_duplicates.append(v)
    if not all(a != b for a, b in combinations(detect_duplicates, 2)):
        raise EPError("주소가 중복됐습니다; {}".format(detect_duplicates))

    chatList.sort(key=itemgetter(1, 0))
    regexList.sort()
    for s in chatList:
        print('{} : "{}"'.format(s[0], s[1]))
    print(
        "(not belong to any pattern) : 1",
        "__encoding__ : {}".format(chatEncoding),
        "__addr__ : %s" % hex(Addr),
        "__lenAddr__ : %s" % hex(lenAddr),
        "__ptrAddr__ : %s" % hex(ptrAddr),
        "Memory(%s, Exactly, Right-sided value); <- Use this condition for chat-detect(desync). Total: %d"
        % (hex(Addr), len(chatList)),
        sep="\n",
    )
    for r in regexList:
        print("^{0}.*{1}.*{2}$ : {3}".format(*r))
    print("__patternAddr__ : %s" % hex(patternAddr))

    chatSet = set()
    global minlen, maxlen
    for i, s in enumerate(chatList):
        for e in chatEncoding:
            t = s[0].encode(e)
            chatSet.add((t, s[1]))
            if len(t) > 78:
                raise EPError(
                    "스타크래프트에서 채팅은 78바이트까지만 입력할 수 있습니다.\n현재 크기: {} > {}".format(
                        len(t), s[0]
                    )
                )
            if len(t) > maxlen:
                maxlen = len(t)
            if len(t) < minlen:
                minlen = len(t)
    global chatDict
    chatDict = [0 for _ in range(maxlen - minlen + 1)]
    chatList = list(chatSet)
    for i, s in enumerate(chatList):
        size = len(s[0]) - minlen
        if isinstance(chatDict[size], list):
            chatDict[size][0].append(Db(s[0] + b"\0"))
            chatDict[size][1].append(s[1])
        else:
            chatDict[size] = [[Db(s[0] + b"\0")], [s[1]]]
    for i, s in enumerate(chatDict):
        if isinstance(s, list):
            chatDict[i] = EUDArray([len(s[0])] + s[0] + s[1])
    chatDict = EUDArray(chatDict)

    rSet = set()
    for r in regexList:
        start, middle, end, value = r
        for e in chatEncoding:
            rSet.add((start.encode(e), middle.encode(e), end.encode(e), value))
    global rList, rListlen
    rList = list(rSet)
    for i, r in enumerate(rList):
        start, middle, end, value = r
        rList[i] = EUDArray(
            (
                Db(start + b"\0"),
                Db(middle + b"\0"),
                Db(end + b"\0"),
                value,
                len(start),
                len(end),
            )
        )
    rListlen = len(rList)
    rList = EUDArray(rList)


onInit()

con = [[Forward() for _ in range(2)] for __ in range(5)]
act = [[Forward() for _ in range(2)] for __ in range(5)]
chatptr, exit = EUDVariable(), Forward()
cp = [[Forward() for _ in range(2)] for __ in range(3)]
trg = [Forward() for _ in range(2)]
event_init, chat_detected = Forward(), Forward()
detect_oddline, detect_evenline = Forward(), Forward()


@EUDFunc
def f_init():
    pNumber = f_getuserplayerid()  # 플레이어 번호 (비공유)
    idptr = 0x57EEEB + 36 * pNumber
    idlen = f_strlen(idptr)
    idDb, myChat = Db(28), Db(b":\x07 ")
    DoActions([SetMemory(idDb + i, SetTo, 0) for i in range(0, 28, 4)])
    f_memcpy(idDb, idptr, idlen)
    f_dbstr_addstr(idDb + idlen, myChat)

    odd, even = EUDCreateVariables(2)
    set_mask = [Forward() for _ in range(4)]

    DoActions(
        [
            SetMemory(event_init + 348, SetTo, 0x640B63 + idlen),
            odd.SetNumber(0),
            even.SetNumber(16),
            SetMemory(set_mask[0] + 16, SetTo, EPD(detect_oddline + 8)),
            SetMemory(set_mask[1] + 16, SetTo, EPD(detect_oddline + 8 + 8)),
            SetMemory(set_mask[2] + 16, SetTo, EPD(detect_evenline + 8)),
            SetMemory(set_mask[3] + 16, SetTo, EPD(detect_evenline + 8 + 8)),
        ]
        + [
            [
                SetMemory(detect_oddline + 8 + 20 * c, SetTo, 0),  # 비트 마스크
                SetMemory(detect_oddline + 8 + 8 + 20 * c, SetTo, 0),  # 값
            ]
            for c in range(7)
        ]
        + [
            [
                SetMemory(detect_evenline + 8 + 20 * c, SetTo, 0),  # 비트 마스크
                SetMemory(detect_evenline + 8 + 8 + 20 * c, SetTo, 0),  # 값
            ]
            for c in range(8)
        ]
    )
    br = EUDByteReader()
    br.seekepd(EPD(idDb))
    if EUDWhile()(True):
        b = br.readbyte()
        EUDBreakIf(b == 0)
        DoActions(
            [
                set_mask[0] << SetMemory(0, Add, f_bitlshift(0xFF, odd)),
                set_mask[1] << SetMemory(0, Add, f_bitlshift(b, odd)),
                set_mask[2] << SetMemory(0, Add, f_bitlshift(0xFF, even)),
                set_mask[3] << SetMemory(0, Add, f_bitlshift(b, even)),
                odd.AddNumber(8),
                even.AddNumber(8),
            ]
        )
        RawTrigger(
            conditions=odd.AtLeast(32),
            actions=[
                odd.SubtractNumber(32),
                SetMemory(set_mask[0] + 16, Add, 5),
                SetMemory(set_mask[1] + 16, Add, 5),
            ],
        )
        RawTrigger(
            conditions=even.AtLeast(32),
            actions=[
                even.SubtractNumber(32),
                SetMemory(set_mask[2] + 16, Add, 5),
                SetMemory(set_mask[3] + 16, Add, 5),
            ],
        )
    EUDEndWhile()


def onPluginStart():
    f_init()


@EUDFunc
def f_chatcmp():
    chatlen = f_strlen(chatptr)
    if lenAddr >= 1:
        VProc(chatlen, chatlen.QueueAssignTo(EPD(lenAddr)))
    if ptrAddr >= 1:
        DoActions(SetMemory(ptrAddr, SetTo, chatptr))
    if EUDIf()([chatlen >= minlen, chatlen <= maxlen]):
        t = EUDArray.cast(chatDict[chatlen - minlen])
        if EUDIf()(t >= 1):
            n = t[0]
            i = EUDVariable()
            i << 1
            if EUDWhile()(i <= n):
                if EUDIf()(f_strcmp(chatptr, t[i]) == 0):
                    DoActions(SetMemory(Addr, SetTo, t[n + i]))
                    EUDJump(exit)
                EUDEndIf()
                i += 1
            EUDEndWhile()
        EUDEndIf()
    EUDEndIf()
    if rListlen >= 1:
        for i in EUDLoopRange(rListlen):
            subArray = EUDArray.cast(rList[i])
            if EUDIf()(f_memcmp(chatptr, subArray[0], subArray[4]) == 0):
                endlen = subArray[5]
                if EUDIf()(
                    f_memcmp(chatptr + chatlen - endlen, subArray[2], endlen) == 0
                ):
                    if EUDIfNot()(f_strnstr(chatptr, subArray[1], chatlen) == -1):
                        DoActions(SetMemory(patternAddr, SetTo, subArray[3]))
                        EUDJump(exit)
                    EUDEndIf()
                EUDEndIf()
            EUDEndIf()


temp = EUDVariable()


def chatEvent():
    event_init << RawTrigger(  # 조건의 EPD 초기화
        actions=[chatptr.SetNumber(0x640B63)]
        + [
            SetMemory(detect_oddline + 8 + 4 + 20 * c, SetTo, EPD(0x640B60) + c)
            for c in range(7)
        ]
        + [
            SetMemory(detect_evenline + 8 + 4 + 20 * c, SetTo, EPD(0x640C3A) + c)
            for c in range(8)
        ]
    )

    if EUDWhile()(chatptr <= 0x640B60 + 436 * 6 - 1):
        oddline_nptr, evenline_nptr = Forward(), Forward()
        # odd linenumber
        detect_oddline << RawTrigger(
            conditions=[DeathsX(0, Exactly, 0, 0, 0) for _ in range(7)],
            actions=[
                SetMemory(chat_detected + 8 + 320 + 16, SetTo, EPD(detect_oddline + 4)),
                SetMemory(chat_detected + 8 + 320 + 20, SetTo, oddline_nptr),
                SetNextPtr(detect_oddline, chat_detected),
            ],
        )
        oddline_nptr << NextTrigger()

        EUDBreakIf(chatptr >= 0x640B60 + 436 * 5)
        # even linenumber
        detect_evenline << RawTrigger(
            conditions=[DeathsX(0, Exactly, 0, 0, 0) for _ in range(8)],
            actions=[
                chatptr.AddNumber(218),
                SetMemory(chat_detected + 344, SetTo, EPD(detect_evenline + 4)),
                SetMemory(chat_detected + 348, SetTo, evenline_nptr),
                SetNextPtr(detect_evenline, chat_detected),
            ],
        )
        evenline_nptr << NextTrigger()

        EUDSetContinuePoint()
        DoActions(
            [chatptr.AddNumber(436)]
            + [SetMemory(detect_oddline + 12 + 20 * c, Add, 109) for c in range(7)]
            + [SetMemory(detect_evenline + 12 + 20 * c, Add, 109) for c in range(8)]
        )
    EUDEndWhile()
    chatptr << 0


def beforeTriggerExec():
    if EUDIf()(Memory(Addr, Exactly, -1)):
        f_init()
    EUDEndIf()

    DoActions(
        [SetMemory(Addr, SetTo, 0), chatptr.SetNumber(0)]  # 초기화
        + [SetMemory(lenAddr, SetTo, 0) if lenAddr >= 1 else []]
        + [SetMemory(ptrAddr, SetTo, 0) if ptrAddr >= 1 else []]
        + [SetMemory(patternAddr, SetTo, 0) if rListlen >= 1 else []]
    )

    oldcp = f_getcurpl()
    chatEvent()

    PushTriggerScope()
    chat_detected << RawTrigger(
        actions=[SetMemory(0, SetTo, 0), SetMemory(Addr, SetTo, 1)]
    )
    f_wwrite(chatptr - 2, 0x0720)
    f_chatcmp()
    SetNextTrigger(exit)
    PopTriggerScope()

    exit << NextTrigger()
    f_setcurpl(oldcp)
