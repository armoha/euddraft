import runpy
from edpkgutil.cleanDir import cleanDirectory
from edpkgutil.packageZip import packageZip
from euddraft import version
buildDir = "build/exe.win32-3.4"

cleanDirectory(buildDir)

runpy.run_module('setup')

outputZipList = [
    'latest/euddraft%s.zip' % version,
    'latest/euddraft_latest.zip'
]

for outputZip in outputZipList:
    print('Packaging to %s' % outputZip)
    packageZip(buildDir, outputZip, version)
