# euddraft

Framework for creating & applying various plugins to StarCraft map.

Fork of https://github.com/phu54321/euddraft

This fork focuses on optimization and adding high-level features for StarCraft: Remastered UMS map.

Use upstream repo if you're interested in StarCraft 1.16.1 only or SC 1.16.1 and SC:R compatible EUD map.

## Building from source

`mkdist.py` freezes `euddraft.py` into a standalone native executable with
[cx_Freeze](https://cx-freeze.readthedocs.io/) and packages it into
`latest/euddraft<version>.zip` (see `pyproject.toml` → `[tool.cxfreeze]`).

The build is native: each OS builds an executable for itself — no cross-compiling.
Python 3.10–3.14 is supported.

### Prerequisites

- Python >= 3.10, < 3.15
- [uv](https://docs.astral.sh/uv/) (or `python -m venv`)
- [git](https://git-scm.com/)
- CMake >= 3.6 and a C++ compiler (MSVC on Windows, g++ on Linux, clang on macOS)
- Python development headers (e.g. `python3-dev` on Debian/Ubuntu)
- Rust toolchain ([rustup](https://rustup.rs/)) — only for eudplib's `_rust` extension

> eudplib **must be built from source on Linux and macOS**: the PyPI wheel only
> ships the Windows `libepScriptLib.dll`. See the
> [eudplib README](../eudplib/README.md) for details.
>
> The Python development headers and CMake are also needed by `mkdist.py`, which
> builds the `freezeMpq` extension (from `mpqprt/`, a pybind11 module) for the
> current platform into `lib/`.

### 1. Clone the repositories

```bash
git clone https://github.com/armoha/euddraft --recursive
git clone https://github.com/armoha/eudplib --recursive
```

This places `eudplib` as a sibling directory (`../eudplib` relative to `euddraft`).

### 2. Build eudplib's native components

#### Linux / macOS

```bash
cd eudplib/src/epscript
cc -std=gnu89 -O2 -o lemon2 lemon2.c           # parser generator (not needed on Windows)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target epScriptLib
cp build/libepScriptLib.so ../eudplib/epscript/       # Linux
# cp build/libepScriptLib.dylib ../eudplib/epscript/  # macOS
cd ../..
```

#### Windows (PowerShell)

```powershell
cd eudplib\src\epscript
cmake -S . -B build -A x64
cmake --build build --target epScriptLib --config Release
copy build\Release\epScriptLib.dll ..\eudplib\epscript\libepScriptLib.dll
cd ..\..\
```

### 3. Set up the Python environment

```bash
cd euddraft
uv venv --python 3.14
uv pip install -e ../eudplib "cx-Freeze>=8.3.0,<9" "rich>=13.8.1,<14" "openpyxl>=3.1.3,<4" "typing_extensions>=4.12.2,<5"
```

`uv` automatically targets the `.venv` created in the current directory on every
platform. The `-e ../eudplib` install also builds eudplib's `_rust` extension
via maturin, which needs the Rust toolchain.

### 4. Build the distribution

```bash
.venv/bin/python mkdist.py                     # Linux / macOS
.venv\Scripts\python.exe mkdist.py             # Windows
```

`mkdist.py` first builds the `freezeMpq` extension (`mpqprt/`) into
`lib/freezeMpq.pyd` on Windows and `lib/freezeMpq.so` on Linux / macOS, then
freezes `euddraft.py` with cx_Freeze. The frozen executable is written to
`build/exe.<platform>-<python version>/` and the distributable archive to
`latest/euddraft<version>.zip`.
