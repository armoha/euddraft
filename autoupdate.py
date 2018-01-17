from urllib.request import urlopen
from urllib.error import URLError
import re
from euddraft import version


VERSION_URL = "https://raw.githubusercontent.com/phu54321/euddraft/master/latest/VERSION"
RELEASE_URL = "https://raw.githubusercontent.com/phu54321/euddraft/master/latest/euddraft%s.zip"


def download(url):
    try:
        with urlopen(url) as urlf:
            return urlf.read()
    except URLError:
        return None


def getCurrentVersion():
    v = download(VERSION_URL)
    if v is None:
        return None
    else:
        return v.decode('utf-8')


def versionLt(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]
    return normalize(version1) < normalize(version2)


def requireUpdate(currentVersion):
    return currentVersion and versionLt(version, currentVersion)


def getRelease(version):
    return download(RELEASE_URL % version)


currentVersion = getCurrentVersion()
print(requireUpdate(currentVersion))
print(len(getRelease(currentVersion)))
