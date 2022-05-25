#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""soundlooper - Manage loop sounds for StarCraft: Remastered."""
import codecs
import io
import os
import random
import string
import struct
from io import BytesIO
from math import ceil, floor

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


def _create_layout():
    bars = random.sample(range(3), 2)
    if random.random() < 0.5:
        bars = [b + 3 for b in bars]
    identifiers = [i for i in range(6) if i not in bars]
    random.shuffle(identifiers)
    return identifiers, bars


def _create_fstring(identifiers, bars):
    s = [""] * 6
    for i, p in enumerate(identifiers):
        s[p] = f"{{0[{i}]}}"
    for i, q in enumerate(bars):
        s[q] = f"{{1[{i}]}}"
    return chr(random.randint(97, 122)) + "".join(s)


_PATH = ""
_INV_SYS_TIME = 0x51CE8C
_CP = 0x6509B0
_ID, _BARS = _create_layout()
_FSTRING = _create_fstring(_ID, _BARS)
print("ID:", _ID, ", BARS:", _BARS, ", FSTR:", _FSTRING, "\n")  # TODO: DEBUG


def _id_generator(_check_duplicates=[]):
    # generate unique random string of length 4

    def random_4_chars():
        ret = ""
        for n in range(4):
            c = chr(random.randint(1, 96))
            while c == "/":
                c = chr(random.randint(1, 96))
            ret += c
        return ret

    ids = random_4_chars()
    while ids in _check_duplicates:
        ids = random_4_chars()
    _check_duplicates.append(ids)
    return ids


def _i2f(i):
    ret = ""
    for n in range(2):
        i, q = divmod(i, 91)
        ret += chr(q + 1)
    return ret


class _Loop:
    _next_index = 0
    loop_dict = dict()

    def __init__(self, title, identifier, count, intro, bar, bridge, goto=1):
        self.index = _Loop._next_index
        _Loop._next_index += 1
        self.ids = identifier
        self.count = count
        self.intro = intro  # lengths
        self.bar = bar
        self.bridge = bridge
        self.goto = goto
        _Loop.loop_dict[title] = self
        print("{}𝄞 {} 𝄆 {} 𝄀 {} 𝄇".format(title, intro, bar, bridge))


def SetPath(new_path):
    """사운드 폴더 경로를 지정합니다."""
    global _PATH
    _PATH = new_path


def AddLoop(title, goto=1):
    """
    사운드 루프를 파일명0.ogg 부터 파일명8280.ogg까지 자동으로 추가합니다.

    Args:
        title (str): 사운드 파일 이름.
        goto (int): 마지막까지 재생한 뒤에 돌아갈 사운드 번호 (기본값: 1).
    """

    def get_filepath(x):
        fs = _PATH + "/{0}/{0}{{}}.ogg".format(title)
        fnum = str(x)
        while len(fnum) <= len(str(91**2 - 1)):
            file_path = fs.format(fnum)
            try:
                open(file_path, "rb")
            except FileNotFoundError:
                fnum = "0" + fnum
            else:
                return file_path
        return None

    intro, bar, bridge = 0, 0, 0
    identifier = _id_generator()
    for i in range(91**2):
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
                # [8] = s___ ___\0 (4 for identifier, 2 for index)
                MPQAddFile(_FSTRING.format(identifier, _i2f(i)), content)
        elif i == 0:
            continue
        elif any([intro, bar, bridge]):
            return _Loop(title, identifier, i - 1, intro, bar, bridge, goto)
        else:
            raise EPError("{} 삽입 실패, 파일 경로를 확인하세요.".format(title))


def _u2i4(s):
    return b2i4(u2b(s))


def _T2i(title):
    try:
        return _Loop.loop_dict[title].index
    except (KeyError):
        return title


@EUDFunc
def _calculate_error():
    x = EUDVariable()
    x << -41
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


class SoundLooper:
    """루프 사운드 플레이어."""

    bars = EUDArray(len(_Loop.loop_dict))

    def __init__(self):
        """사운드 플레이어 생성."""
        self.current_loop = EUDVariable(-1)
        self.previous_loop = EUDVariable(-1)
        self.current_bar = EUDVariable()
        self._check_time = Forward()
        self._set_bar_length = Forward()
        self._SetStrings = [Forward() for _ in range(2)]
        self._set_bar = Forward()
        self._set_localcp = Forward()
        self._check_last_bar = Forward()
        self._add1_bar = Forward()
        self._set_intro_length = Forward()
        self._set_bridge_length = Forward()
        self._set1_bar = Forward()
        self._set_goto = [Forward() for _ in range(2)]
        self._sb = StringBuffer(_FSTRING.format("\x01" * 4, "\x01" * 2))

        def _Init():
            self.initialize()

        EUDOnStart(_Init)  # TODO: auto-init

    def initialize(self):
        """사운드 플레이어 초기화. onPluginStart에서 1번 실행해주세요."""
        VProc(
            self._sb.epd,
            [
                self._sb.epd.AddNumber(1),
                self._sb.epd.SetDest(EPD(self._SetStrings[1]) + 4),
            ],
        )
        VProc(self._sb.epd, self._sb.epd.SetDest(EPD(self._set_bar) + 4))
        localcp = f_getuserplayerid()
        VProc(
            [self._sb.epd, localcp],
            [
                self._sb.epd.AddNumber(-1),
                self._sb.epd.SetDest(EPD(self._SetStrings[0]) + 4),
                localcp.SetDest(EPD(self._set_localcp) + 5),
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
                inv_time.SetDest(EPD(self._check_time) + 2),
                self._SetStrings[0] << SetMemory(0, SetTo, 0),
                self._SetStrings[1] << SetMemory(0, SetTo, 0),
                self._set_bar << SetMemory(0, Add, 0),
                self._set_localcp << SetMemory(_CP, SetTo, 0),
                PlayWAV(self._sb.StringIndex),
                DisplayText(self._sb.StringIndex),  # TODO: DEBUG
                self.current_bar.AddNumber(1),
                SetMemory(self._set_bar + 20, Add, 1 << 24),
                self._add1_bar << SetMemory(0, Add, 1),
            ],
        )
        DoActions(self._set_bar_length << SetMemory(self._check_time + 8, Add, 0))
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
            self.current_bar.SetNumber(bar),
            SetMemoryX(self._set_bar + 20, SetTo, d, 0xFFFFFF),
            SetMemoryEPD(EPD(SoundLooper.bars) + self.current_loop, SetTo, bar),
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
            self.setbar(SoundLooper.bars[index])
        else:
            self.setbar(bar)

    @staticmethod
    def _write_string(ids, i):
        s = _FSTRING.format(ids, _i2f(i))
        v0, m0 = 0, 0
        for p in range(1, 4):
            n = ord(s[p])
            if n >= 1:
                v0 += n << (8 * p)
                m0 += 255 << (8 * p)
        v1, m1 = 0, 0
        for q in range(3):
            n = ord(s[q + 4])
            if n >= 1:
                v1 += n << (8 * q)
                m1 += 255 << (8 * q)
        return v0, m0, v1, m1

    @EUDMethod
    def _setloop(self, index):
        """재생할 사운드 루프를 설정한다."""
        err = _calculate_error()
        VProc(
            [self.current_loop, index, err],
            [
                self.current_loop.SetDest(self.previous_loop),
                index.SetDest(self.current_loop),
                err.SetDest(EPD(self._set_bar_length) + 5),
                SetMemory(self._set1_bar + 20, SetTo, 1),
                SetMemory(self._set_goto[0] + 20, SetTo, 1),
                SetMemory(self._set_goto[1] + 20, SetTo, 0x10000),
            ],
        )

        EUDSwitch(index)
        for filename, loop in _Loop.loop_dict.items():
            EUDSwitchCase()(loop.index)
            d1, d0 = _i2f(loop.goto)  # ? d2
            goto = 1  # (d0 << 16) + (d1 << 8)  # + d2
            bar = EPD(SoundLooper.bars) + loop.index
            v0, m0, v1, m1 = self._write_string(loop.ids, _i2f(0))
            DoActions(
                SetMemoryX(self._SetStrings[0] + 20, SetTo, v0, m0),
                SetMemoryX(self._SetStrings[1] + 20, SetTo, v1, m1),
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
            )
            EUDBreak()
        EUDEndSwitch()

    def pause(self):
        """사운드 루프를 일시정지한다."""
        DoActions(
            self.previous_loop.SetNumber(self.current_loop),
            self.current_loop.SetNumber(-1),
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
        VProc(self.current_bar, self.current_bar.SetDest(EPD(SoundLooper.bars) + loop))

    @classmethod
    def sendbar(cls, dst, src, _fdict={}):
        """
        사운드 루프 dst의 진행도를 src의 진행도로 설정한다.

        Args:
            dst (str): 전달 받는 사운드 루프 이름.
            src (str): 진행도를 참고할 사운드 루프 이름.
        """
        dst, src = _T2i(dst), _T2i(src)

        if SoundLooper.bars in _fdict:
            _f = _fdict[SoundLooper.bars]
        else:

            @EUDFunc
            def _f(dst, src):
                SoundLooper.bars[dst] = SoundLooper.bars[src]

            _fdict[SoundLooper.bars] = _f

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
        f_dwwrite_epd(EPD(SoundLooper.bars) + loop, bar)

    @classmethod
    def _setloopbar(cls, loop, bar):
        loop = _T2i(loop)
        return SetMemoryEPD(EPD(SoundLooper.bars) + loop, SetTo, bar)

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
        return MemoryEPD(EPD(SoundLooper.bars) + loop, cmptype, value)

    def loopis(self, loop):
        """현재 재생중인 곡을 비교하는 조건."""
        loop = _T2i(loop)
        return self.current_loop.Exactly(loop)
