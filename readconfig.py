import re


def readconfig(fname):
    s = open(fname, 'rb').read()

    try:
        s = s.decode('cp949')
    except UnicodeDecodeError:
        s = s.decode('utf-8')

    currentSectionName = None
    currentSection = None
    config = {}

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
