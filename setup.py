import sys
from cx_Freeze import setup, Executable

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
        "plugins"
    ],
    'zip_include_packages': ['*'],
    'zip_exclude_packages': []
}


setup(
    name="euddraft",
    version='0.8.0.0',
    description="euddraft compilication system",
    options={
        "build_exe": build_exe_options
    },
    executables=[
        Executable("euddraft.py", base="Console")
    ]
)
