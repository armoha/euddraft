import sys

from cx_Freeze import Executable, setup

from euddraft import version

if "build_exe" not in sys.argv:
    sys.argv.append("build_exe")


build_exe_options = {
    "packages": [
        "os",
        "ctypes",
        "sys",
        "importlib",
        "json",
        "eudplib",
        "openpyxl",
    ],
    "excludes": ["tkinter"],
    "optimize": 2,
    "include_msvcr": True,
    "include_files": [
        "libepScriptLib.dll",
        "license.txt",
        "plugins",
        "lib",
        "epTrace.exe",
    ],
    "zip_include_packages": "*",
    "zip_exclude_packages": "",
}


setup(
    name="euddraft",
    version=version,
    description="euddraft compilication system",
    options={"build_exe": build_exe_options},
    executables=[Executable("euddraft.py", base="Console")],
)
