#!/usr/bin/env python3

import os
import runpy
import shutil
import sys
from sysconfig import get_platform

from edpkgutil.cleanDir import cleanDirectory, cleanOutput
from edpkgutil.packageZip import packageZip
from euddraft import version

buildDir = f"build/exe.{get_platform()}-{sys.version_info[0]}.{sys.version_info[1]}"
outputZipList = [
    "latest/euddraft%s.zip" % version,
    # 'latest/euddraft_latest.zip'
]

cleanDirectory(buildDir)

if sys.platform.startswith("win"):
    runpy.run_module("setup")
else:
    os.system("wine python setup.py")
    shutil.copy("python311.dll", os.path.join(buildDir, "python311.dll"))

cleanOutput(buildDir)

for outputZipPath in outputZipList:
    print(f"Packaging to {outputZipPath}")
    packageZip(buildDir, outputZipPath, version)

with open("latest/VERSION", "w") as version_file:
    version_file.write(version)
