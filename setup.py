import os
import shutil
import zipfile
from cx_Freeze import setup, Executable
from euddraft import version


beta = True

buildDir = "build/exe.win32-3.4"

if not beta:
    if os.path.exists(buildDir):
        for the_file in os.listdir(buildDir):
            fpath = os.path.join(buildDir, the_file)
            try:
                if os.path.isfile(fpath):
                    os.unlink(fpath)
                elif os.path.isdir(fpath):
                    shutil.rmtree(fpath)
            except Exception as e:
                print(e)


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "importlib", "json", "eudplib"],
    "optimize": 2,
    "include_msvcr": True,
    "include_files": [
        "freezeMpq.pyd",
        "StormLib32.dll",
        "libepScriptLib.dll",
        "license.txt",
        "plugins",
        'lib',
        'epTrace.exe',
    ],
}


setup(
    name="euddraft",
    version=version,
    description="euddraft compilication system",
    options={
        "build_exe": build_exe_options
    },
    executables=[
        Executable("euddraft.py", base="Console")
    ]
)


# Package them to latest/ folder


if not beta:
    print("Packaging data...")

    def package_zip(fname):
        with zipfile.ZipFile(fname, 'w', zipfile.ZIP_DEFLATED) as zipf:
            os.chdir(buildDir)
            for root, dirs, files in os.walk('.'):
                for file in files:
                    zipf.write(os.path.join(root, file))
            zipf.writestr('VERSION', str(version))
            os.chdir('../../')

    package_zip('latest/euddraft%s.zip' % version)
    package_zip('latest/euddraft_latest.zip')

    with open('latest/VERSION', 'w') as f:
        f.write(version)
