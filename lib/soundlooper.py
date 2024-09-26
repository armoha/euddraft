"""soundlooper - Manage loop sounds for StarCraft: Remastered."""
import codecs
import io
import os
import random
import string
import struct
from io import BytesIO
from math import ceil

from eudplib import *

# tinytag - an audio meta info reader
# Copyright (c) 2014-2018 Tom Wallroth
#
# Sources on github:
# http://github.com/devsnd/tinytag/

# MIT License

# Copyright (c) 2014-2018 Tom Wallroth

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class _TinyTagException(LookupError):  # inherit LookupError for backwards compat
    pass


class _TinyTag(object):
    def __init__(self, filehandler, filesize):
        self._filehandler = filehandler
        self.filesize = filesize
        self.album = None
        self.albumartist = None
        self.artist = None
        self.audio_offset = None
        self.bitrate = None
        self.channels = None
        self.comment = None
        self.disc = None
        self.duration = None
        self.genre = None
        self.samplerate = None
        self.title = None
        self.track = None
        self.year = None

    @classmethod
    def get(cls, filename):
        size = os.path.getsize(filename)
        if not size > 0:
            return _TinyTag(None, 0)
        with io.open(filename, "rb") as af:
            tag = _Ogg(af, size)
            tag.load()
            return tag

    def load(self):
        self._determine_duration(self._filehandler)

    def _set_field(self, fieldname, bytestring, transfunc=None):
        """
        Convienience function to set fields of the tinytag by name.

        the payload (bytestring) can be changed using the transfunc
        """
        if getattr(self, fieldname):  # do not overwrite existing data
            return
        value = bytestring if transfunc is None else transfunc(bytestring)
        if fieldname in ("track", "disc"):
            if type(value).__name__ in ("str", "unicode") and "/" in value:
                current, total = value.split("/")[:2]
                setattr(self, "%s_total" % fieldname, total)
            else:
                current = value
            setattr(self, fieldname, current)
        else:
            setattr(self, fieldname, value)


class _Ogg(_TinyTag):
    def __init__(self, filehandler, filesize):
        _TinyTag.__init__(self, filehandler, filesize)
        self._tags_parsed = False
        self._max_samplenum = 0  # maximum sample position ever read

    def _determine_duration(self, fh):
        MAX_PAGE_SIZE = 65536  # https://xiph.org/ogg/doc/libogg/ogg_page.html
        if not self._tags_parsed:
            self._parse_tag(fh)  # determine sample rate
            fh.seek(0)  # and rewind to start
        if self.filesize > MAX_PAGE_SIZE:
            fh.seek(-MAX_PAGE_SIZE, 2)  # go to last possible page position
        while True:
            b = fh.peek(4)
            if len(b) == 0:
                return  # EOF
            if b[:4] == b"OggS":  # look for an ogg header
                for packet in self._parse_pages(fh):
                    pass  # parse all remaining pages
                self.duration = self._max_samplenum / float(self.samplerate)
            else:
                idx = b.find(b"OggS")  # try to find header in peeked data
                seekpos = idx if idx != -1 else len(b) - 3
                fh.seek(max(seekpos, 1), os.SEEK_CUR)

    def _parse_tag(self, fh):
        page_start_pos = fh.tell()  # set audio_offest later if its audio data
        for packet in self._parse_pages(fh):
            walker = BytesIO(packet)
            if packet[0:7] == b"\x01vorbis":
                (
                    channels,
                    self.samplerate,
                    max_bitrate,
                    bitrate,
                    min_bitrate,
                ) = struct.unpack("<B4i", packet[11:28])
                if not self.audio_offset:
                    self.bitrate = bitrate / 1024.0
                    self.audio_offset = page_start_pos
            elif packet[0:7] == b"\x03vorbis":
                walker.seek(7, os.SEEK_CUR)  # jump over header name
                self._parse_vorbis_comment(walker)
            elif packet[0:8] == b"OpusHead":  # parse opus header
                # https://www.videolan.org/developers/vlc/modules/codec/opus_header.c
                # https://mf4.xiph.org/jenkins/view/opus/job/opusfile-unix/ws/doc/html/structOpusHead.html
                walker.seek(8, os.SEEK_CUR)  # jump over header name
                (version, ch, _, sr, _, _) = struct.unpack("<BBHIHB", walker.read(11))
                if (version & 0xF0) == 0:  # only major version 0 supported
                    self.channels = ch
                    self.samplerate = sr
            elif packet[0:8] == b"OpusTags":  # parse opus metadata:
                walker.seek(8, os.SEEK_CUR)  # jump over header name
                self._parse_vorbis_comment(walker)
            else:
                break
            page_start_pos = fh.tell()

    def _parse_vorbis_comment(self, fh):
        # for the spec, see: http://xiph.org/vorbis/doc/v-comment.html
        # discnumber tag based on: https://en.wikipedia.org/wiki/Vorbis_comment
        comment_type_to_attr_mapping = {
            "album": "album",
            "albumartist": "albumartist",
            "title": "title",
            "artist": "artist",
            "date": "year",
            "tracknumber": "track",
            "discnumber": "disc",
            "genre": "genre",
            "description": "comment",
        }
        vendor_length = struct.unpack("I", fh.read(4))[0]
        fh.seek(vendor_length, os.SEEK_CUR)  # jump over vendor
        elements = struct.unpack("I", fh.read(4))[0]
        for i in range(elements):
            length = struct.unpack("I", fh.read(4))[0]
            try:
                keyvalpair = codecs.decode(fh.read(length), "UTF-8")
            except UnicodeDecodeError:
                continue
            if "=" in keyvalpair:
                key, value = keyvalpair.split("=", 1)
                fieldname = comment_type_to_attr_mapping.get(key.lower())
                if fieldname:
                    self._set_field(fieldname, value)

    def _parse_pages(self, fh):
        # for the spec, see: https://wiki.xiph.org/Ogg
        previous_page = b""  # contains data from previous (continuing) pages
        header_data = fh.read(27)  # read ogg page header
        while len(header_data) != 0:
            header = struct.unpack("<4sBBqIIiB", header_data)
            oggs, version, flags, pos, serial, pageseq, crc, segments = header
            self._max_samplenum = max(self._max_samplenum, pos)
            if oggs != b"OggS" or version != 0:
                raise _TinyTagException("Not a valid ogg file!")
            segsizes = struct.unpack("B" * segments, fh.read(segments))
            total = 0
            for segsize in segsizes:  # read all segments
                total += segsize
                if total < 255:  # less than 255 bytes means end of page
                    yield previous_page + fh.read(total)
                    previous_page = b""
                    total = 0
            if total != 0:
                if total % 255 == 0:
                    previous_page += fh.read(total)
                else:
                    yield previous_page + fh.read(total)
                    previous_page = b""
            header_data = fh.read(27)


_PATH = ""
_INV_SYS_TIME = 0x51CE8C
_CP = 0x6509B0
_sb = StringBuffer(8)


def _id_generator():
    # generate unique random string of length 5
    chars = string.ascii_letters + string.digits
    return "".join(random.sample(chars * 5, 5))


class _Loop:
    _next_index = 0
    loop_dict = dict()

    def __init__(self, title, identifier, count, intro, bar, bridge, goto=1):
        self.index = _Loop._next_index
        _Loop._next_index += 1
        self.id = identifier
        self.count = count
        self.intro = intro  # lengths
        self.bar = bar
        self.bridge = bridge
        self.goto = goto
        _Loop.loop_dict[title] = self
        print("{}: {} ||: {} | {} :||".format(title, intro, bar, bridge))


def SetPath(new_path):
    """사운드 폴더 경로를 지정합니다."""
    global _PATH
    _PATH = new_path


def AddLoop(title, goto=1):
    """
    사운드 루프를 파일명0.ogg 부터 파일명999.ogg까지 자동으로 추가합니다.

    Args:
        title (str): 사운드 파일 이름.
        goto (int): 마지막까지 재생한 뒤에 돌아갈 사운드 번호 (기본값: 1).
    """
    ep_assert(
        SoundLooper._bars is None, f"{title} 삽입 실패, AddLoop를 함수 밖으로 옮기세요."
    )

    def get_filepath(x):
        fp = _PATH + "/{0}/{0}".format(title)
        fnum = str(x)

        while len(fnum) <= 3:
            file_path = fp + fnum + ".ogg"
            try:
                with open(file_path, "rb") as f:
                    return file_path
            except FileNotFoundError:
                fnum = "0" + fnum  # Prepend a "0" to the file number
    
        return None

    intro, bar, bridge = 0, 0, 0
    identifier = _id_generator()
    for i in range(1000):
        file_path = get_filepath(i)
        if file_path:
            with open(file_path, "rb") as f:
                content = f.read()
                tag = _Ogg.get(file_path)
                if i == 0:
                    intro = round(tag.duration, 3)
                elif bar == 0:
                    bar = round(tag.duration, 3)
                bridge = round(tag.duration, 3)
                MPQAddFile("{}{:03d}".format(identifier, i), content)
        elif i == 0:
            continue
        elif any([intro, bar, bridge]):
            return _Loop(title, identifier, i - 1, intro, bar, bridge, goto)
        else:
            raise EPError("{} 삽입 실패, 파일 경로를 확인하세요.".format(title))


def ManualAddLoop(title, count, intro, bar, bridge, goto=1):
    """
    [고급] 이미 맵에 삽입된 사운드를 루프로 등록합니다.

    Args:
        title (str): 사운드 파일 이름 (5 바이트).
        count (int): 사운드 파일 총 개수.
        intro (int): 인트로 파일 (00번) 재생 길이.
        length (int): 중간 파일 재생 길이.
        bridge (int): 마지막 파일 재생 길이.
        goto (int): 마지막까지 재생한 뒤에 돌아갈 사운드 번호 (기본값: 1).
    """
    if len(title.encode("cp949")) != 5:
        raise EPError("Title length should be 5 bytes")
    _Loop(title, title, count, intro, bar, bridge, goto)


def _u2i4(s):
    return b2i4(u2b(s))


def _T2i(title):
    try:
        return _Loop.loop_dict[title].index
    except KeyError:
        return title


@EUDFunc
def _calculate_error():
    x = EUDVariable()
    DoActions(x.SetNumber(-41))
    _next = Forward()
    EUDJumpIfNot(Memory(0x5124F0, Exactly, 42), _next)
    x << f_dwread_epd(EPD(0x5124F0))
    _next << NextTrigger()
    speed_map = {
        (2047, 2047): 29,
        (4095, 4095): 18,
        (65535, 65535): 1,
        (1157, 1157): 36,
        (1437, 1437): 29,
        (1984, 1984): 29,
        (3472, 3472): 18,
        (41667, 41667): 1,
        (1736, 1736): 36,
        (2155, 2155): 29,
        (2976, 2976): 21,
        (5208, 5208): 18,
        (62500, 62500): 1,
        (2463, 2463): 29,
        (3401, 3401): 21,
        (5952, 5952): 18,
        (71429, 71429): 1,
    }
    for point, speed in speed_map.items():
        V84, V88 = point
        RawTrigger(
            conditions=[Memory(0x51CE84, Exactly, V84), Memory(0x51CE88, Exactly, V88)],
            actions=x.SetNumber(speed),
        )
    EUDReturn((493 - 7 * x) // 41)


localcp = EUDVariable()


def _onInit():
    global localcp
    localcp << f_getuserplayerid()


EUDOnStart(_onInit)


@EUDFunc
def PlaySoundWorkaround(loop, barpp):
    barpp -= 1
    EUDSwitch(loop)
    for title, loop in _Loop.loop_dict.items():
        EUDSwitchCase()(loop.index)
        EUDSwitch(barpp)
        for n in range(loop.count + 1):
            EUDSwitchCase()(n)
            DoActions(PlayWAV("{}{:03d}".format(loop.id, n)))
            EUDReturn()
        EUDEndSwitch()
    EUDEndSwitch()


def get_three_digits(x):
    ab, c = divmod(x, 10)
    a, b = divmod(ab, 10)
    return a, b, c


class SoundLooper:
    """루프 사운드 플레이어."""

    _bars: EUDArray | None = None  # EUDArray(len(_Loop.loop_dict))

    @classmethod
    def bars(cls):
        if cls._bars is None:
            cls._bars = EUDArray(len(_Loop.loop_dict))
        return cls._bars

    def __init__(self):
        """사운드 플레이어 생성."""
        self.current_loop = EUDVariable(-1)
        self.previous_loop = EUDVariable(-1)
        self.current_bar = EUDVariable()
        self._check_time = Forward()
        self._set_bar_length = Forward()
        self._set_loop = [Forward() for _ in range(2)]
        self._set_bar = Forward()
        self._set_localcp = Forward()
        self._check_last_bar = Forward()
        self._add1_bar = Forward()
        self._set_intro_length = Forward()
        self._set_bridge_length = Forward()
        self._set1_bar = Forward()
        self._set_goto = [Forward() for _ in range(2)]

        def _Init():
            self.initialize()

        EUDOnStart(_Init)

    def initialize(self):
        """사운드 플레이어 초기화. onPluginStart에서 1번 실행해주세요."""
        VProc(
            localcp,
            [
                SetMemory(self._set_loop[1] + 16, SetTo, _sb.epd + 1),
                SetMemory(self._set_bar + 16, SetTo, _sb.epd + 1),
                SetMemory(self._set_loop[0] + 16, SetTo, _sb.epd),
                localcp.QueueAssignTo(EPD(self._set_localcp) + 5),
            ],
        )

    def player(self):
        """사운드 플레이어 메인 함수. 사운드 재생이 일어납니다."""
        _end = Forward()
        EUDJumpIf(self.current_loop.Exactly(-1), _end)
        EUDJumpIf([self._check_time << Memory(_INV_SYS_TIME, AtLeast, ~0)], _end)
        inv_time = f_dwread_epd(EPD(_INV_SYS_TIME))
        VProc(
            inv_time,
            [
                inv_time.QueueAssignTo(EPD(self._check_time) + 2),
                self._set_loop[0] << SetMemory(0, SetTo, 0),
                self._set_loop[1] << SetMemory(0, SetTo, 0),
                self._set_bar << SetMemory(0, Add, 0),
                self._set_localcp << SetMemory(_CP, SetTo, 0),
                # PlayWAV(_sb.StringIndex),
                self.current_bar.AddNumber(1),
                SetMemory(self._set_bar + 20, Add, 1 << 16),
                self._add1_bar << SetMemory(0, Add, 1),
            ],
        )
        DoActions([self._set_bar_length << SetMemory(self._check_time + 8, Add, 0)])
        PlaySoundWorkaround(self.current_loop, self.current_bar)
        bar_carry = self._set_bar + 20
        RawTrigger(
            conditions=MemoryX(bar_carry, AtLeast, (ord("9") + 1) << 16, 0xFF << 16),
            actions=SetMemory(bar_carry, Add, (1 << 8) - (10 << 16)),
        )
        RawTrigger(
            conditions=MemoryX(bar_carry, AtLeast, (ord("9") + 1) << 8, 0xFF << 8),
            actions=SetMemory(bar_carry, Add, 1 - (10 << 8)),
        )
        RawTrigger(  # if intro was played, modify playtime
            conditions=self.current_bar.Exactly(1),
            actions=[self._set_intro_length << SetMemory(self._check_time + 8, Add, 0)],
        )
        RawTrigger(  # if last bar was played, go to start
            conditions=[self._check_last_bar << self.current_bar.AtLeast(0)],
            actions=[
                self._set_bridge_length << SetMemory(self._check_time + 8, Add, 0),
                self._set_goto[0] << self.current_bar.SetNumber(1),
                self._set_goto[1] << SetMemory(self._set_bar + 20, SetTo, 0x10000),
                self._set1_bar << SetMemory(0, SetTo, 1),
            ],
        )
        _end << NextTrigger()

    @EUDMethod
    def setbar(self, bar):
        """현재 재생 중인 사운드 루프의 진행도를 설정한다."""
        ab, c = f_div(bar, 10)
        a, b = f_div(ab, 10)
        d = a + (b << 8) + (c << 16)
        DoActions(
            [
                self.current_bar.SetNumber(bar),
                SetMemoryX(self._set_bar + 20, SetTo, d, 0xFFFFFF),
                SetMemoryEPD(EPD(SoundLooper.bars()) + self.current_loop, SetTo, bar),
            ]
        )

    def play(self, title, bar=None):
        """
        사운드 루프를 플레이한다.

        Args:
            title (str): 재생할 사운드 이름.
            bar (int): 재생할 순서. 생략하면 최근에 재생한 위치부터 재생.
        """
        if title is None:
            self._setloop(self.current_loop)
        else:
            index = _T2i(title)
            self._setloop(index)
        if bar is None:
            self.setbar(self.bars()[index])
        else:
            self.setbar(bar)

    @EUDMethod
    def _setloop(self, index):
        """재생할 사운드 루프를 설정한다."""
        err = _calculate_error()
        VProc(
            [self.current_loop, index, err],
            [
                self.current_loop.QueueAssignTo(self.previous_loop),
                index.QueueAssignTo(self.current_loop),
                err.QueueAssignTo(EPD(self._set_bar_length) + 5),
                SetMemory(self._set1_bar + 20, SetTo, 1),
                SetMemory(self._set_goto[0] + 20, SetTo, 1),
                SetMemory(self._set_goto[1] + 20, SetTo, 0x10000),
            ],
        )

        EUDSwitch(index)
        for filename, loop in _Loop.loop_dict.items():
            EUDSwitchCase()(loop.index)
            d2, d1, d0 = get_three_digits(loop.goto)
            goto = (d0 << 16) + (d1 << 8) + d2
            bar = EPD(self.bars()) + loop.index
            DoActions(
                [
                    SetMemory(self._set_loop[0] + 20, SetTo, _u2i4(loop.id[:4])),
                    SetMemory(self._set_loop[1] + 20, SetTo, _u2i4(loop.id[4] + "000")),
                    SetMemory(self._check_last_bar + 8, SetTo, loop.count + 1),
                    SetMemory(
                        self._set_intro_length + 20,
                        SetTo,
                        ceil((loop.bar - loop.intro) * 1000),
                    ),
                    SetMemory(self._set_bar_length + 20, Add, ceil(-loop.bar * 1000)),
                    SetMemory(
                        self._set_bridge_length + 20,
                        SetTo,
                        ceil((loop.bar - loop.bridge) * 1000),
                    ),
                    SetMemory(self._add1_bar + 16, SetTo, bar),
                    SetMemory(self._set1_bar + 16, SetTo, bar),
                    [
                        SetMemory(self._set_goto[0] + 20, SetTo, loop.goto),
                        SetMemory(self._set_goto[1] + 20, SetTo, goto),
                        SetMemory(self._set1_bar + 20, SetTo, loop.goto),
                    ]
                    if loop.goto != 1
                    else [],
                ]
            )
            EUDBreak()
        EUDEndSwitch()

    def pause(self):
        """사운드 루프를 일시정지한다."""
        DoActions(
            [
                self.previous_loop.SetNumber(self.current_loop),
                self.current_loop.SetNumber(-1),
            ]
        )

    def resume(self):
        """일시정지한 사운드 루프를 다시 재생한다."""
        self._setloop(self.previous_loop)

    @EUDMethod
    def toggle(self):
        """사운드 루프의 일시정지/다시재생 상태를 토글한다."""
        if EUDIf()(self.current_loop.Exactly(-1)):
            self.resume()
        if EUDElse()():
            self.pause()
        EUDEndIf()

    def sendcurrentbar(self, loop):
        """
        현재 루프의 진행 정도를 다른 사운드 루프로 전달한다.

        같은 사운드 루프의 낮/밤 버전을 같은 위치에서 전환하는 등에 쓰인다.
        """
        loop = _T2i(loop)
        VProc(
            self.current_bar,
            self.current_bar.QueueAssignTo(EPD(self.bars()) + loop),
        )

    @classmethod
    def sendbar(cls, dst, src, _fdict={}):
        """
        사운드 루프 dst의 진행도를 src의 진행도로 설정한다.

        Args:
            dst (str): 전달 받는 사운드 루프 이름.
            src (str): 진행도를 참고할 사운드 루프 이름.
        """
        dst, src = _T2i(dst), _T2i(src)

        if cls.bars() in _fdict:
            _f = _fdict[cls.bars()]
        else:

            @EUDFunc
            def _f(dst, src):
                cls.bars()[dst] = cls.bars()[src]

            _fdict[cls.bars()] = _f

        _f(dst, src)

    @classmethod
    def setloopbar(cls, loop, bar):
        """
        (현재 재생 중이 아닌) 사운드 루프의 진행도를 설정한다.

        Args:
            loop (str): 사운드 루프 파일명.
            bar (int): 설정할 진행도.
        """
        loop = _T2i(loop)
        return f_dwwrite_epd(EPD(cls.bars()) + loop, bar)

    @classmethod
    def _setloopbar(cls, loop, bar):
        loop = _T2i(loop)
        return SetMemoryEPD(EPD(cls.bars()) + loop, SetTo, bar)

    @classmethod
    def cond(cls, loop, cmptype, value):
        """
        사운드 루프 loop가 얼마나 재생되었는지 조건.

        Args:
            loop (str): 사운드 루프 파일명.
            cmptype (Comparison): Exactly, AtLeast, AtMost.
            value (int): 진행도와 비교할 값.
        """
        loop = _T2i(loop)
        return MemoryEPD(EPD(cls.bars()) + loop, cmptype, value)

    def loopis(self, loop):
        """현재 재생중인 곡을 비교하는 조건."""
        loop = _T2i(loop)
        return self.current_loop.Exactly(loop)
