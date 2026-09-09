#!/usr/bin/env python3

import glob
import os
import platform
import shutil
import subprocess
import sys
from sysconfig import get_platform

import eudplib

from edpkgutil.cleanDir import cleanDirectory, cleanOutput
from edpkgutil.packageZip import packageZip
from euddraft import version

here = os.path.dirname(os.path.abspath(__file__))

buildDir = f"build/exe.{get_platform()}-{sys.version_info[0]}.{sys.version_info[1]}"
# Each CI runner (Windows/macOS/Linux) uploads its zip to the same release,
# so the filename must be platform-specific. Otherwise same-name assets from
# the three matrix jobs overwrite each other and only one survives.
distPlatform = {"Windows": "windows", "Darwin": "macos"}.get(
    platform.system(), platform.system().lower()
)
outputZipList = [
    "latest/euddraft%s-%s.zip" % (version, distPlatform),
    # 'latest/euddraft_latest.zip'
]


def buildFreezeMpq() -> None:
    """Build the freezeMpq extension (from mpqprt/) into lib/.

    Produces lib/freezeMpq.pyd on Windows and lib/freezeMpq.so on
    Linux / macOS, matching the Python running mkdist.py.
    """
    cmakeCmd = shutil.which("cmake")
    if cmakeCmd is None:
        raise RuntimeError(
            "cmake not found: required to build the freezeMpq extension "
            "(see README.md)"
        )
    mpqprtDir = os.path.join(here, "mpqprt")
    cmakeBuildDir = os.path.join(
        here, "build", f"mpqprt-{sys.version_info[0]}.{sys.version_info[1]}"
    )
    subprocess.check_call(
        [
            cmakeCmd,
            "-S",
            mpqprtDir,
            "-B",
            cmakeBuildDir,
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
        ]
    )
    subprocess.check_call([cmakeCmd, "--build", cmakeBuildDir, "--config", "Release"])

    # The POST_BUILD copy in mpqprt/CMakeLists.txt only runs when the
    # target is rebuilt, so copy explicitly to make sure lib/ has the
    # extension even on incremental builds.
    ext = "pyd" if os.name == "nt" else "so"
    candidates = [
        f
        for f in glob.glob(os.path.join(cmakeBuildDir, "**", f"freezeMpq*.{ext}"), recursive=True)
        if os.path.isfile(f)
    ]
    if not candidates:
        raise RuntimeError(
            f"freezeMpq build produced no extension module in {cmakeBuildDir}"
        )
    newest = max(candidates, key=os.path.getmtime)
    shutil.copy(newest, os.path.join(here, "lib", f"freezeMpq.{ext}"))


cleanDirectory(buildDir)

buildFreezeMpq()

subprocess.check_call(
    [
        sys.executable,
        "-m",
        "cx_Freeze",
        "build_exe",
        f"--build-exe={buildDir}",
    ]
)

# Bundle the eudplib native library next to the executable, where
# eudplib's find_data_file looks for it when frozen.
libName = {
    "Linux": "libepScriptLib.so",
    "Windows": "libepScriptLib.dll",
    "Darwin": "libepScriptLib.dylib",
}[platform.system()]
eudplibDir = os.path.dirname(eudplib.__file__)
srcPath = os.path.join(eudplibDir, "epscript", libName)
if os.path.exists(srcPath):
    shutil.copy(srcPath, os.path.join(buildDir, libName))
else:
    print(f"Warning: {libName} not found in {os.path.dirname(srcPath)}", file=sys.stderr)

cleanOutput(buildDir)

# Copy platform-specific extras into the build directory
epTraceSrc = os.path.join(here, "epTrace.exe")
if os.path.exists(epTraceSrc):
    shutil.copy(epTraceSrc, buildDir)

for outputZipPath in outputZipList:
    print(f"Packaging to {outputZipPath}")
    packageZip(buildDir, outputZipPath, version)

with open("latest/VERSION", "w", newline="") as version_file:
    version_file.write(version)
