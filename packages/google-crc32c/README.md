# `google-crc32c`

This package wraps the [`google/crc32c`](https://github.com/google/crc32c)
hardware-based implementation of the CRC32C hashing algorithm. Multiple wheels
are distributed as well as source. If a wheel is not published for the python
version and platform you are using, you will need to compile crc32c using a
C toolchain.


# Building

## Be sure to check out all submodules:

```
$ git clone --recursive https://github.com/googleapis/python-crc32c
```

## Prerequisites

On Linux:

- `docker`
- `python3.7`

On OS X:

- `make`
- [Official][1] `python.org` Python 2.7, 3.5, 3.6 and 3.7

On Windows:

- `cmake`
- [Official][1] `python.org` Python 3.5, 3.6 and 3.7
- Visual Studio 15 2017 (just the compiler toolchain)

Unfortunately, `libcrc32c` relies on many C++11 features, so
building a Python 2.7 extension with the
[Visual C++ Compiler for Python 2.7][2] is infeasible.


## Building Wheels

On Linux:

```
./scripts/manylinux/build.sh
```

On OS X:

```
./scripts/osx/build.sh
```

On Windows: see `.appveyor.yml`.

## Testing/Verify Wheels

On Linux (i.e. a host OS, not a `docker` container):

```
$ ./scripts/manylinux/check-37.sh
...
+ venv/bin/python check_cffi_crc32c.py
_crc32c_cffi: <module 'crc32c._crc32c_cffi' from '.../python-crc32c/venv/lib/python3.7/site-packages/crc32c/_crc32c_cffi.abi3.so'>
_crc32c_cffi.lib: <Lib object for 'crc32c._crc32c_cffi'>
dir(_crc32c_cffi.lib): ['crc32c_extend', 'crc32c_value']
+ unzip -l wheels/google_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl
Archive:  wheels/google_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
    26120  2018-10-25 00:09   crc32c/_crc32c_cffi.abi3.so
      765  2018-10-24 23:57   crc32c/__init__.py
    29552  2018-10-25 00:09   crc32c/.libs/libcrc32c-f865a225.so
      109  2018-10-25 00:09   google_crc32c-0.0.1.dist-info/WHEEL
      766  2018-10-25 00:09   google_crc32c-0.0.1.dist-info/METADATA
      652  2018-10-25 00:09   google_crc32c-0.0.1.dist-info/RECORD
        1  2018-10-25 00:09   google_crc32c-0.0.1.dist-info/zip-safe
        7  2018-10-25 00:09   google_crc32c-0.0.1.dist-info/top_level.txt
---------                     -------
    57972                     8 files
...
```

On OS X:

```
$ ./scripts/osx/check.sh
...
+ venv37/bin/python .../python-crc32c/check_cffi_crc32c.py
_crc32c_cffi: <module 'google_crc32c._crc32c_cffi' from '.../python-crc32c/venv37/lib/python3.7/site-packages/google_crc32c/_crc32c_cffi.abi3.so'>
_crc32c_cffi.lib: <Lib object for 'google_crc32c._crc32c_cffi'>
dir(_crc32c_cffi.lib): ['crc32c_extend', 'crc32c_value']
+ /Library/Frameworks/Python.framework/Versions/3.7/bin/delocate-listdeps --all --depending .../python-crc32c/wheels/google_crc32c-0.0.1-cp37-cp37m-macosx_10_6_intel.whl
/usr/lib/libSystem.B.dylib:
    google_crc32c/_crc32c_cffi.abi3.so
    google_crc32c/.dylibs/libcrc32c.dylib
/usr/lib/libc++.1.dylib:
    google_crc32c/.dylibs/libcrc32c.dylib
@loader_path/.dylibs/libcrc32c.dylib:
    google_crc32c/_crc32c_cffi.abi3.so
...
```

On Windows: TBD.

[1]: https://www.python.org/downloads/
[2]: https://aka.ms/vcpython27

## Installing locally for testing

Initialize the submodules and build the main `libcrc32c.so` shared
library using `cmake` / `make`:

```bash
$ cd python-crc32c
$ git submodule update --init --recursive
$ python -m venv venv
$ venv/bin/pip install --upgrade setuptools pip wheel
$ venv/bin/pip install cmake
$ mkdir usr
$ export CRC32C_INSTALL_PREFIX=$(pwd)/usr
$ mkdir google_crc32c/build
$ cd google_crc32c/build
$ ../../venv/bin/cmake \
>   -DCRC32C_BUILD_TESTS=no \
>   -DCRC32C_BUILD_BENCHMARKS=no \
>   -DBUILD_SHARED_LIBS=yes \
>   -DCMAKE_INSTALL_PREFIX:PATH=${CRC32C_INSTALL_PREFIX} \
>   ..
$ make all install
$ cd ../..
```

Now, run the tests:

```bash
$ venv/bin/pip install -e .[testing]
$ venv/bin/py.test tests/
============================= test session starts ==============================
platform linux -- Python 3.6.7, pytest-3.10.0, py-1.7.0, pluggy-0.8.0
rootdir: ..., inifile:
collected 9 items

tests/test___init__.py .........                                         [100%]

=========================== 9 passed in 0.03 seconds ===========================
```
