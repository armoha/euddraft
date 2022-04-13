#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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
"""

import re
from collections import OrderedDict
from typing import Dict

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def readconfig(fname) -> Dict[str, Dict[str, str]]:
    header_regex = re.compile(r"\[(.+)\]$")
    keyvalue_regex = re.compile(r"(([^\\:=]|\\.)+)\s*[:=]\s*(.+)$")
    keyonly_regex = re.compile(r"(([^\\:=]|\\.)+)")
    key_replace_regex = re.compile(r"\\([\\:=])")
    comment_regex = re.compile(r"::.*")

    def parse_config(text):
        currentSectionName = None
        currentSection = None
        config = OrderedDict()
        header_lineno = {}
        config_lineno = {}
        for lineno, line in enumerate(text):
            lineno += 1
            line = line.strip()
            if not line:  # empty line
                continue

            # Try header
            header_match = header_regex.fullmatch(line)
            if header_match:
                currentSectionName = header_match.group(1)
                if currentSectionName in config:
                    origin_lineno_length, duplicated_lineno_length = str(header_lineno[currentSectionName]).__len__(), str(lineno).__len__()
                    currentSectionName_length = currentSectionName.__len__()
                    raise RuntimeError(
                        f'''Duplicate header '{currentSectionName}'
                        {header_lineno[currentSectionName]} | [{currentSectionName}]
                        {bcolors.FAIL}{" " * (origin_lineno_length + 3)}{"^" * (currentSectionName_length + 2)}{bcolors.ENDC}
                        {lineno} | [{currentSectionName}]
                        {bcolors.FAIL}{" " * (duplicated_lineno_length + 3)}{"^" * (currentSectionName_length + 2)}{bcolors.ENDC}''',
                    )
                currentSection = {}
                config[currentSectionName] = currentSection
                header_lineno[currentSectionName] = lineno
                config_lineno.clear()
                continue

            # Try key-value pair
            keyvalue_match = keyvalue_regex.fullmatch(line)
            if keyvalue_match:
                key = keyvalue_match.group(1)
                key = key_replace_regex.sub(r"\1", key)
                key = key.strip()
                value = keyvalue_match.group(3)
                if key in currentSection:
                    origin_lineno_length, duplicated_lineno_length = str(config_lineno[key]).__len__(), str(lineno).__len__()
                    current_key_length = key.__len__()
                    raise RuntimeError(
                        f'''Duplicate key '{key}'
                        {config_lineno[key]} | {key} : {currentSection[key]}
                        {bcolors.FAIL}{" " * (origin_lineno_length + 3)}{"^" * current_key_length}{bcolors.ENDC}
                        {lineno} | {key} : {value}
                        {bcolors.FAIL}{" " * (duplicated_lineno_length + 3)}{"^" * current_key_length}{bcolors.ENDC}
                        '''
                    )
                currentSection[key] = value
                config_lineno[key] = lineno
                continue

            # Try key-only pair
            keyonly_match = keyonly_regex.fullmatch(line)
            if keyonly_match:
                key = keyonly_match.group(1)
                key = key_replace_regex.sub(r"\1", key)
                key = key.replace("\\:", ":")
                key = key.replace("\\=", "=")
                key = key.strip()
                if key in currentSection:
                    origin_lineno_length, duplicated_lineno_length = str(config_lineno[key]).__len__(), str(lineno).__len__()
                    current_key_length = key.__len__()
                    raise RuntimeError(
                        f'''Duplicate key '{key}' in '{currentSectionName}'
                        {config_lineno[key]} | {key} : {currentSection[key]}
                        {bcolors.FAIL}{" " * (origin_lineno_length + 3)}{"^" * current_key_length}{bcolors.ENDC}
                        {lineno} | {key}
                        {bcolors.FAIL}{" " * (duplicated_lineno_length + 3)}{"^" * current_key_length}{bcolors.ENDC}
                        '''
                    )
                currentSection[key] = ""
                config_lineno[key] = lineno
                continue

            # Try comment
            comment_match = comment_regex.match(line)
            if comment_match:
                continue

            raise RuntimeError("Invalid config %s" % line)
        return config

    try:
        text = open(fname, encoding="UTF-8")
        config = parse_config(text)
    except UnicodeDecodeError:
        text = open(fname)
        config = parse_config(text)

    text.close()
    return config
