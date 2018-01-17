# We omitted cryptographic checks intentionally, cause that would be handled properly by GitHub

import re
import sys
import os
import io
import zipfile
import atexit
from threading import Thread

from urllib.request import urlopen
from urllib.error import URLError

import msgbox


VERSION_URL = 'https://raw.githubusercontent.com/phu54321/euddraft/master/latest/VERSION'
RELEASE_URL = 'https://raw.githubusercontent.com/phu54321/euddraft/master/latest/euddraft%s.zip'


def download(url):
    try:
        with urlopen(url) as urlf:
            return urlf.read()
    except URLError:
        return None


def getLatestUpdateCheckpoint():
    try:
        dataDir = os.path.dirname(sys.executable)
        with open(os.path.join(dataDir, 'vcheckpoint.txt'), 'r') as vchp:
            return vchp.read()
    except OSError:
        from euddraft import version
        return version


def writeVersionCheckpoint(version):
    try:
        dataDir = os.path.dirname(sys.executable)
        with open(os.path.join(dataDir, 'vcheckpoint.txt'), 'w') as vchp:
            vchp.write(version)
    except OSError:
        pass


def getLatestVersion():
    v = download(VERSION_URL)
    if v is None:
        return None
    else:
        return v.decode('utf-8')


def versionLt(version1, version2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split('.')]
    return normalize(version1) < normalize(version2)


def requireUpdate(currentVersion):
    version = getLatestUpdateCheckpoint()
    return currentVersion and versionLt(version, currentVersion)


def getRelease(version):
    return download(RELEASE_URL % version)


def checkUpdate():
    # auto update only supports Win32 by now.
    # Also, the application should be frozen
    if not msgbox.isWindows or not getattr(sys, 'frozen', False):
        return False

    currentVersion = getLatestVersion()
    if requireUpdate(currentVersion):
        MB_YESNO = 0x00000004
        IDYES = 6

        if msgbox.MessageBox(
            'New version',
            'A new version %s is found. Would you like to update?' %
            currentVersion,
            MB_YESNO
        ) == IDYES:
            # Download the needed data
            release = getRelease(currentVersion)
            if not release:
                msgbox.MessageBox('Update failed', 'Cannot get update file.')

            dataDir = os.path.dirname(sys.executable)
            updateDir = os.path.join(dataDir, '_update')

            with zipfile.ZipFile(io.BytesIO(release), 'r') as zipf:
                zipf.extractall(updateDir)

            with open(os.path.join(dataDir, '_update.bat'), 'w') as batf:
                batf.write('''\
@echo off
echo Updating euddraft.
xcopy _update . /e /y
del /s /f /q _update\*.*
rd _update /s /q
echo Update completed
del _update.bat /q
''')

            def onExit():
                from subprocess import Popen
                Popen('_update.bat')
            atexit.register(onExit)

        else:
            writeVersionCheckpoint(currentVersion)


def issueAutoUpdate():
    checkUpdateThread = Thread(target=checkUpdate)
    checkUpdateThread.start()
    # We don't join this thread. This thread will automatically join when
    # the whole euddraft process is completed.
    #
    # Also, we don't want this thread to finish before it completes its update
    # process, even if the main thread has already finished. So we don't make
    # this thread a daemon thread.
