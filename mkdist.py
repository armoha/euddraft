#!/usr/bin/env python3

import os
import runpy
import shutil
import sys

from edpkgutil.cleanDir import cleanDirectory
from edpkgutil.packageZip import packageZip
from euddraft import version

buildDir = "build/exe.win-amd64-%u.%u" % sys.version_info[0:2]
outputZipList = [
    "latest/euddraft%s.zip" % version,
    # 'latest/euddraft_latest.zip'
]

cleanDirectory(buildDir)

if sys.platform.startswith("win"):
    runpy.run_module("setup")
else:
    os.system("wine python setup.py")
    shutil.copy("python310.dll", os.path.join(buildDir, "python310.dll"))

for outputZipPath in outputZipList:
    print("Packaging to %s" % outputZipPath)
    packageZip(buildDir, outputZipPath, version)

open("latest/VERSION", "w").write(version)
