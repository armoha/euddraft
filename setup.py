import os
import zipfile
import sys
from cx_Freeze import setup, Executable
from euddraft import version


sys.argv.append('build_exe')

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
    ],
    'zip_include_packages': ['*'],
    'zip_exclude_packages': []
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
    os.chdir('build/exe.win32-3.6')
    zipdir('.', zipf)
    os.chdir('../..')

with open('latest/VERSION', 'w') as f:
    f.write(version)
