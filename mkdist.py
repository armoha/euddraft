import runpy
import sys
import os

from edpkgutil.cleanDir import cleanDirectory
from edpkgutil.packageZip import packageZip
from edpkgutil.verifyPkg import generateFileSignature
from euddraft import version

buildDir = "build/exe.win32-3.4"
outputZipList = [
    'latest/euddraft%s.zip' % version,
    'latest/euddraft_latest.zip'
]

# ----

cleanDirectory(buildDir)

if sys.platform.startswith('win'):
    runpy.run_module('setup')
else:
    os.system('wine python setup.py')

for outputZipPath in outputZipList:
    print('Packaging to %s' % outputZipPath)
    packageZip(buildDir, outputZipPath, version)

    # Digital signing!
    signature = generateFileSignature(outputZipPath)
    open(outputZipPath + '.sig', 'w').write(signature)

open('latest/VERSION', 'w').write(version)
