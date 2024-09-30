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
            match = re.match(r"(.+) (\d+)", vstr)
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
            r"""\
@echo off

:: Set the working directory to the directory of the script
set "WORKDIR=%~dp0"

:: Remove old files from the working directory
del /q "%WORKDIR%api-ms-win-crt-convert-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-filesystem-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-heap-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-locale-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-math-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-multibyte-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-runtime-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-stdio-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-string-l1-1-0.dll"
del /q "%WORKDIR%api-ms-win-crt-utility-l1-1-0.dll"
del /q "%WORKDIR%concrt140.dll"
del /q "%WORKDIR%epTrace.exe"
del /q "%WORKDIR%euddraft.exe"
del /q "%WORKDIR%freezeMpq.pyd"
del /q "%WORKDIR%frozen_application_license.txt"
del /q "%WORKDIR%libepScriptLib.dll"
del /q "%WORKDIR%license.txt"
del /q "%WORKDIR%mpq.exc"
del /q "%WORKDIR%msvcp100.dll"
del /q "%WORKDIR%msvcp140.dll"
del /q "%WORKDIR%msvcp140_1.dll"
del /q "%WORKDIR%msvcp140_atomic_wait.dll"
del /q "%WORKDIR%MSVCR100.dll"
del /q "%WORKDIR%msvcrt.dll"
del /q "%WORKDIR%python3.dll"
del /q "%WORKDIR%python310.dll"
del /q "%WORKDIR%python311.dll"
del /q "%WORKDIR%python34.dll"
del /q "%WORKDIR%python38.dll"
del /q "%WORKDIR%StormLib32.dll"
del /q "%WORKDIR%StormLib64.dll"
del /q "%WORKDIR%ucrtbase.dll"
del /q "%WORKDIR%vcheckpoint.dat"
del /q "%WORKDIR%VCRUNTIME140.dll"
del /q "%WORKDIR%vcruntime140_1.dll"
del /q "%WORKDIR%VERSION"

:: Remove old subfolders in the lib directory
rmdir /s /q "%WORKDIR%lib\\asn1crypto"
rmdir /s /q "%WORKDIR%lib\\cffi"
rmdir /s /q "%WORKDIR%lib\\collections"
rmdir /s /q "%WORKDIR%lib\\cryptography"
rmdir /s /q "%WORKDIR%lib\\ctypes"
rmdir /s /q "%WORKDIR%lib\\Cython"
rmdir /s /q "%WORKDIR%lib\\distutils"
rmdir /s /q "%WORKDIR%lib\\edpkgutil"
rmdir /s /q "%WORKDIR%lib\\email"
rmdir /s /q "%WORKDIR%lib\\encodings"
rmdir /s /q "%WORKDIR%lib\\eudplib"
rmdir /s /q "%WORKDIR%lib\\freeze"
rmdir /s /q "%WORKDIR%lib\\html"
rmdir /s /q "%WORKDIR%lib\\http"
rmdir /s /q "%WORKDIR%lib\\idna"
rmdir /s /q "%WORKDIR%lib\\importlib"
rmdir /s /q "%WORKDIR%lib\\json"
rmdir /s /q "%WORKDIR%lib\\ko_KR"
rmdir /s /q "%WORKDIR%lib\\lib2to3"
rmdir /s /q "%WORKDIR%lib\\logging"
:: rmdir /s /q "%WORKDIR%lib\\matplotlib"
rmdir /s /q "%WORKDIR%lib\\multiprocessing"
rmdir /s /q "%WORKDIR%lib\\OpenSSL"
rmdir /s /q "%WORKDIR%lib\\pkg_resources"
rmdir /s /q "%WORKDIR%lib\\pycparser"
rmdir /s /q "%WORKDIR%lib\\pydoc_data"
rmdir /s /q "%WORKDIR%lib\\pywin"
rmdir /s /q "%WORKDIR%lib\\pyximport"
rmdir /s /q "%WORKDIR%lib\\setuptools"
rmdir /s /q "%WORKDIR%lib\\test"
rmdir /s /q "%WORKDIR%lib\\unittest"
rmdir /s /q "%WORKDIR%lib\\urllib"
rmdir /s /q "%WORKDIR%lib\\win32com"
rmdir /s /q "%WORKDIR%lib\\xml"
rmdir /s /q "%WORKDIR%lib\\xmlrpc"
rmdir /s /q "%WORKDIR%lib\\_markerlib"
rmdir /s /q "%WORKDIR%lib\\__pycache__"

:: Remove old files from the 'lib' subdirectory
del /q "%WORKDIR%lib\\api-ms-win-core-console-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-console-l1-2-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-datetime-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-debug-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-errorhandling-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-fibers-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-file-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-file-l1-2-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-file-l2-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-handle-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-heap-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-interlocked-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-libraryloader-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-localization-l1-2-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-memory-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-namedpipe-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-processenvironment-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-processthreads-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-processthreads-l1-1-1.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-profile-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-rtlsupport-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-string-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-synch-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-synch-l1-2-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-sysinfo-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-timezone-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-core-util-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-conio-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-convert-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-environment-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-filesystem-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-heap-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-locale-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-math-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-multibyte-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-private-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-process-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-runtime-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-stdio-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-string-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-time-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-crt-utility-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-eventing-controller-l1-1-0.dll"
del /q "%WORKDIR%lib\\api-ms-win-eventing-provider-l1-1-0.dll"
del /q "%WORKDIR%lib\\COMMIT_THIS_DIRECTORY"
del /q "%WORKDIR%lib\\contourpy._contourpy.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\cryptography.hazmat.bindings._constant_time.cp38-win32.pyd"
del /q "%WORKDIR%lib\\cryptography.hazmat.bindings._openssl.cp38-win32.pyd"
del /q "%WORKDIR%lib\\Cython.Compiler.FlowControl.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\Cython.Compiler.FusedNode.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\Cython.Compiler.Scanning.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\Cython.Compiler.Visitor.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\Cython.Tempita._tempita.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\draw.py"
del /q "%WORKDIR%lib\\eudplib.bindings._rust.cp311-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.bindings._rust.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.constexpr.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.constexpr.cp38-win32.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.constexpr.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.pbuffer.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.pbuffer.cp38-win32.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.pbuffer.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.rlocint.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.rlocint.cp38-win32.pyd"
del /q "%WORKDIR%lib\\eudplib.core.allocator.rlocint.pyd"
del /q "%WORKDIR%lib\\eudplib.core.variable.vbuf.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.core.variable.vbuf.cp38-win32.pyd"
del /q "%WORKDIR%lib\\eudplib.core.variable.vbuf.pyd"
del /q "%WORKDIR%lib\\eudplib.utils.stackobjs.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.utils.stackobjs.cp38-win_amd64.pyd"
del /q "%WORKDIR%lib\\eudplib.utils.stackobjs.pyd"
del /q "%WORKDIR%lib\\freezeMpq.pyd"
del /q "%WORKDIR%lib\\kiwisolver._cext.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\libcrypto-1_1.dll"
del /q "%WORKDIR%lib\\libcrypto-3.dll"
del /q "%WORKDIR%lib\\libffi-7.dll"
del /q "%WORKDIR%lib\\libffi-8.dll"
del /q "%WORKDIR%lib\\libopenblas.FB5AE2TYXYH2IJRDKGDGQ3XBKLKTF43H.gfortran-win_amd64.dll"
del /q "%WORKDIR%lib\\library.dat"
del /q "%WORKDIR%lib\\library.zip"
del /q "%WORKDIR%lib\\libssl-1_1.dll"
del /q "%WORKDIR%lib\\libssl-3.dll"
del /q "%WORKDIR%lib\\matplotlib.backends._backend_agg.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib.backends._tkagg.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib.ft2font.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._c_internal_utils.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._image.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._path.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._qhull.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._tri.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\matplotlib._ttconv.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\msvcp140.dll"
del /q "%WORKDIR%lib\\MSVCR100.dll"
del /q "%WORKDIR%lib\\msvcrt.dll"
del /q "%WORKDIR%lib\\NO_DELETE"
del /q "%WORKDIR%lib\\numpy.core._multiarray_tests.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._multiarray_umath.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._operand_flag_tests.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._rational_tests.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._simd.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._struct_ufunc_tests.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.core._umath_tests.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.fft._pocketfft_internal.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.linalg.lapack_lite.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.linalg._umath_linalg.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random.bit_generator.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random.mtrand.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._bounded_integers.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._common.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._generator.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._mt19937.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._pcg64.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._philox.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\numpy.random._sfc64.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imaging.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imagingcms.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imagingft.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imagingmath.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imagingmorph.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._imagingtk.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\PIL._webp.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\pyexpat.pyd"
del /q "%WORKDIR%lib\\python34.dll"
del /q "%WORKDIR%lib\\python38.dll"
del /q "%WORKDIR%lib\\pythoncom310.dll"
del /q "%WORKDIR%lib\\pythoncom34.dll"
del /q "%WORKDIR%lib\\pywintypes310.dll"
del /q "%WORKDIR%lib\\pywintypes34.dll"
del /q "%WORKDIR%lib\\SCBank.py"
del /q "%WORKDIR%lib\\scbank_core.py"
del /q "%WORKDIR%lib\\select.pyd"
del /q "%WORKDIR%lib\\soundlooper.py"
del /q "%WORKDIR%lib\\soundlooper_origin.py"
del /q "%WORKDIR%lib\\soundlooper_screen_print.py"
del /q "%WORKDIR%lib\\sqc.py"
del /q "%WORKDIR%lib\\ucrtbase.dll"
del /q "%WORKDIR%lib\\unicodedata.pyd"
del /q "%WORKDIR%lib\\VCRUNTIME140.dll"
del /q "%WORKDIR%lib\\vcruntime140_1.dll"
del /q "%WORKDIR%lib\\win32api.pyd"
del /q "%WORKDIR%lib\\win32com.shell.shell.pyd"
del /q "%WORKDIR%lib\\win32evtlog.pyd"
del /q "%WORKDIR%lib\\win32gui.pyd"
del /q "%WORKDIR%lib\\win32pdh.pyd"
del /q "%WORKDIR%lib\\win32ui.pyd"
del /q "%WORKDIR%lib\\winsound.pyd"
del /q "%WORKDIR%lib\\_asyncio.pyd"
del /q "%WORKDIR%lib\\_bz2.pyd"
del /q "%WORKDIR%lib\\_cffi_backend.cp310-win_amd64.pyd"
del /q "%WORKDIR%lib\\_cffi_backend.cp38-win32.pyd"
del /q "%WORKDIR%lib\\_cffi_backend.pyd"
del /q "%WORKDIR%lib\\_ctypes.pyd"
del /q "%WORKDIR%lib\\_ctypes_test.pyd"
del /q "%WORKDIR%lib\\_decimal.pyd"
del /q "%WORKDIR%lib\\_elementtree.pyd"
del /q "%WORKDIR%lib\\_hashlib.pyd"
del /q "%WORKDIR%lib\\_lzma.pyd"
del /q "%WORKDIR%lib\\_msi.pyd"
del /q "%WORKDIR%lib\\_multiprocessing.pyd"
del /q "%WORKDIR%lib\\_overlapped.pyd"
del /q "%WORKDIR%lib\\_queue.pyd"
del /q "%WORKDIR%lib\\_socket.pyd"
del /q "%WORKDIR%lib\\_ssl.pyd"
del /q "%WORKDIR%lib\\_testbuffer.pyd"
del /q "%WORKDIR%lib\\_testcapi.pyd"
del /q "%WORKDIR%lib\\_uuid.pyd"
del /q "%WORKDIR%lib\\_win32sysloader.pyd"

:: Now proceed to copy the new files
xcopy "%WORKDIR%_update" "%WORKDIR%." /e /y /q

:: Remove the _update directory
rd "%WORKDIR%_update" /s /q

:: Execute Python script
python "%WORKDIR%py_script.py"
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
