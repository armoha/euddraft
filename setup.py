import sys
from cx_Freeze import setup, Executable
from euddraft import version

if 'build_exe' not in sys.argv:
    sys.argv.append('build_exe')


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
