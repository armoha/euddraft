import os
import shutil
import zipfile
from cx_Freeze import setup, Executable
from euddraft import version


beta = True

buildDir = "build/exe.win32-3.6"

if not beta:
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
        "StormLib32.dll",
        "libepScriptLib.dll",
        "mpq.exc",
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

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    with zipfile.ZipFile(
        'latest/euddraft%s.zip' % version,
        'w',
        zipfile.ZIP_DEFLATED
    ) as zipf:
        os.chdir(buildDir)
        zipdir('.', zipf)
        os.chdir('../..')

    with zipfile.ZipFile(
        'latest/euddraft_latest.zip' % version,
        'w',
        zipfile.ZIP_DEFLATED
    ) as zipf:
        os.chdir(buildDir)
        zipdir('.', zipf)
        os.chdir('../..')

    with open('latest/VERSION', 'w') as f:
        f.write(version)
