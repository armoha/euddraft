#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import re
from collections import OrderedDict


def readconfig(fname):
    s = open(fname, 'rb').read()

    try:
        s = s.decode('cp949')
    except UnicodeDecodeError:
        s = s.decode('utf-8')

    currentSectionName = None
    currentSection = None
    config = OrderedDict()

    header_regex = re.compile(r"\[(.+)\]$")
    keyvalue_regex = re.compile(r"(([^\\:=]|\\.)+)\s*[:=]\s*(.+)$")
    keyonly_regex = re.compile(r"(([^\\:=]|\\.)+)")
    key_replace_regex = re.compile(r"\\([\\:=])")
    comment_regex = re.compile(r"[;#].*")

    lines = s.splitlines()
    for line in lines:
        line = line.strip()
        if not line:  # empty line
            continue

        # Try header
        header_match = header_regex.match(line)
        if header_match:
            currentSectionName = header_match.group(1)
            if currentSectionName in config:
                raise RuntimeError('Duplicate header %s' % currentSectionName)
            currentSection = {}
            config[currentSectionName] = currentSection
            continue

        # Try key-value pair
        keyvalue_match = keyvalue_regex.match(line)
        if keyvalue_match:
            key = keyvalue_match.group(1)
            key = key_replace_regex.sub(r"\1", key)
            key = key.strip()
            value = keyvalue_match.group(3)
            currentSection[key] = value
            continue

        # Try key-only pair
        keyonly_match = keyonly_regex.match(line)
        if keyonly_match:
            key = keyonly_match.group(1)
            key = key_replace_regex.sub(r"\1", key)
            key = key.replace('\\:', ':')
            key = key.replace('\\=', '=')
            key = key.strip()
            currentSection[key] = ''
            continue

        # Try comment
        comment_match = comment_regex.match(line)
        if comment_match:
            continue

    return config
