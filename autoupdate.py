# We omitted cryptographic checks intentionally.
# That would be handled properly by https protocol used by GitHub

import atexit
import io
import os
import re
import sys
import time
import zipfile
from threading import Thread
from urllib.error import URLError
from urllib.request import urlopen

import msgbox

VERSION_URL = "https://raw.githubusercontent.com/armoha/euddraft/master/latest/VERSION"
RELEASE_URL = "https://github.com/armoha/euddraft/releases/download/v{}/euddraft{}.zip"


def download(url):
    try:
        with urlopen(url) as urlf:
            return urlf.read()
    except URLError:
        return None


def getLatestUpdateCheckpoint():
    from euddraft import version

    try:
        dataDir = os.path.dirname(sys.executable)
        with open(os.path.join(dataDir, "vcheckpoint.dat"), "r") as vchp:
            vstr = vchp.read()
            match = re.match("(.+) (\d+)", vstr)
            if not match:
                raise OSError
            v = match.group(1)
            t = int(match.group(2))

            # If user has manually updated the game, then
            # v can be less than version.
            if versionLt(v, version):
                v = version
                t = 0
            return v, t

    except OSError:
        return version, 0


def writeVersionCheckpoint(version):
    try:
        dataDir = os.path.dirname(sys.executable)
        with open(os.path.join(dataDir, "vcheckpoint.dat"), "w") as vchp:
            vchp.write(f"{version} {int(time.time())}")
    except OSError:
        pass


def getLatestVersion():
    v = download(VERSION_URL)
    if v is None:
        return "0.0.0.0"
    else:
        return (v.decode("utf-8")).strip()


def versionLt(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r"(\.0+)*$", "", v).split(".")]

    return normalize(version1) < normalize(version2)


def getRelease(version):
    return download(RELEASE_URL.format(version, version))


def checkUpdate():
    # auto update only supports Win32 by now.
    # Also, the application should be frozen
    if not msgbox.isWindows or not getattr(sys, "frozen", False):
        return False

    lastCheckedVersion, lastCheckedTime = getLatestUpdateCheckpoint()
    timeSinceLastCheck = time.time() - lastCheckedTime

    if (
        not msgbox.GetAsyncKeyState(0x10)
        and timeSinceLastCheck < 24 * 60 * 60  # VK_SHIFT
    ):
        return lastCheckedVersion, False

    # Re-write checkpoint time
    latestVersion = getLatestVersion()
    if not versionLt(lastCheckedVersion, latestVersion):
        writeVersionCheckpoint(lastCheckedVersion)
        return

    # Ask user whether to update
    MB_YESNO = 0x00000004
    IDYES = 6
    if (
        msgbox.MessageBox(
            "New version",
            f"A new version {latestVersion} is found. Would you like to update?",
            MB_YESNO,
        )
        != IDYES
    ):
        # User don't want to update. Update checkpoint file
        writeVersionCheckpoint(latestVersion)
        return

    # Download the needed data
    print(f"Downloading euddraft {latestVersion}")
    release = getRelease(latestVersion)
    if not release:
        return msgbox.MessageBox("Update failed", "No release", textio=sys.stderr)

    dataDir = os.path.dirname(sys.executable)
    updateDir = os.path.join(dataDir, "_update")

    with zipfile.ZipFile(io.BytesIO(release), "r") as zipf:
        zipf.extractall(updateDir)

    # Write an auto-update script. This script will run after euddraft exits
    with open(os.path.join(dataDir, "_update.bat"), "w") as batf:
        batf.write(
            """\
@echo off
xcopy _update . /e /y /q
rd _update /s /q
del _update.bat /q
"""
        )

    def onExit():
        from subprocess import Popen

        Popen("_update.bat", cwd=os.path.dirname(sys.executable))

    atexit.register(onExit)
    print("Update downloaded. Update will begin after you close the euddraft.")


def issueAutoUpdate():
    checkUpdateThread = Thread(target=checkUpdate)
    checkUpdateThread.start()
    # We don't join this thread. This thread will automatically join when
    # the whole euddraft process is completed.
    #
    # Also, we don't want this thread to finish before it completes its update
    # process, even if the main thread has already finished. So we don't make
    # this thread a daemon thread.
