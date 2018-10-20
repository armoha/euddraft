import runpy

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
runpy.run_module('setup')

for outputZipPath in outputZipList:
    print('Packaging to %s' % outputZipPath)
    packageZip(buildDir, outputZipPath, version)

    # Digital signing!
    signature = generateFileSignature(outputZipPath)
    open(outputZipPath + '.sig', 'w').write(signature)
