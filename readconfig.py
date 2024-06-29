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


def readconfig(fname) -> tuple[Dict[str, Dict[str, str]], list[Exception]]:
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
        exception_dict = OrderedDict()

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
                    exception_dict.setdefault(
                        ("header", currentSectionName, "", fname),
                        [(header_lineno[currentSectionName], "")],
                    ).append((lineno, ""))
                    while currentSectionName in config:
                        currentSectionName += "_dup"
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
                if currentSection is None:
                    errormsg = f"'key : value' pair ({line}) should be below [header]"
                    exception_dict[lineno] = RuntimeError(errormsg)
                    continue
                if key in currentSection:
                    exception_dict.setdefault(
                        ("key", key, currentSectionName, fname),
                        [(config_lineno[key], f"{currentSection[key]}")],
                    ).append((lineno, f"{value}"))
                    continue
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
                if currentSection is None:
                    errormsg = f"plugin option ({line}) should be below [header]"
                    exception_dict[lineno] = RuntimeError(errormsg)
                    continue
                if key in currentSection:
                    exception_dict.setdefault(
                        ("key", key, currentSectionName, fname),
                        [(config_lineno[key], f"{currentSection[key]}")],
                    ).append((lineno, ""))
                    continue
                currentSection[key] = ""
                config_lineno[key] = lineno
                continue

            # Try comment
            comment_match = comment_regex.match(line)
            if comment_match:
                continue

            exception_dict[lineno] = RuntimeError(f"Invalid config {line}")
            continue

        def encode_error(kind, dup, section, fname, *line_entry_pairs):
            where = f"{dup!r}"
            if section:
                where = f"{where} in [{section}]"
            line_digits = len(str(line_entry_pairs[-1][0]))
            other_lines = ",".join(str(line) for line, _entry in line_entry_pairs[1:])
            error_messages = [
                f"""Duplicated {kind} {where}
[bright_black]{fname}:{other_lines}[/]
"""
            ]
            for line, entry in line_entry_pairs:
                if entry != "":
                    entry = f" : {entry}"
                error_messages.append(
                    f"[red]>[/] {line:>{line_digits}} | [on red]{dup}[/]{entry}"
                )
            return "\n".join(error_messages)

        exceptions = []
        for k, v in exception_dict.items():
            if isinstance(k, tuple):
                exceptions.append(RuntimeError(encode_error(*k, *v)))
            else:
                exceptions.append(v)

        return config, exceptions

    try:
        text = open(fname, encoding="UTF-8")
    except UnicodeDecodeError:
        text = open(fname)
    with text:
        config, excs = parse_config(text)

    return config, excs
