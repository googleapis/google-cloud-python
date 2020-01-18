@rem Copyright 2019 Google LLC. All rights reserved.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem     http://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.


@REM available windows versions on CI as of 2019-Nov-25
@REM  -3.7-64
@REM  -3.7-32
@REM  -3.6-64
@REM  -3.6-32
@REM  -3.5-64
@REM  -3.5-32
@REM  -3.4-64
@REM  -3.4-32
@REM  -2.7-64
@REM  -2.7-32

py -3.7 -m pip install cmake

@rem First, build libcrc32c
set CRC32C_INSTALL_PREFIX=%KOKORO_ARTIFACTS_DIR%\bin_win64\

echo %CRC32C_INSTALL_PREFIX%

pushd crc32c
git submodule update --init --recursive
mkdir build

@REM 64 Bit Builds.
@REM removed -DCRC32C_BUILD_TESTS=no 
set CMAKE_GENERATOR="Visual Studio 15 2017"
C:\Python37\Scripts\cmake -G %CMAKE_GENERATOR% -A x64 -DCRC32C_BUILD_BENCHMARKS=no -DBUILD_SHARED_LIBS=yes ^
-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=yes -DCMAKE_INSTALL_PREFIX:PATH=%CRC32C_INSTALL_PREFIX% .

C:\Python37\Scripts\cmake --build . --config RelWithDebInfo --target install
dir %CRC32C_INSTALL_PREFIX% /b /s
popd

copy %CRC32C_INSTALL_PREFIX%bin\crc32c.dll .

@rem update python deps and build wheels (requires CRC32C_INSTALL_PREFIX is set)
FOR %%V IN (3.5-64,3.6-64,3.7-64) DO (
    py -%%V -m pip install --upgrade pip setuptools wheel
    py -%%V -m pip wheel . --wheel-dir wheels/
)


@REM 32 Bit Builds.
@REM removed -DCRC32C_BUILD_TESTS=no 

set CMAKE_GENERATOR="Visual Studio 15 2017"
pushd crc32c
@rem reset hard to cleanup any changes done by 64-bit build.
git reset --hard

del /s /q CMakeFiles\
del CMakeCache.txt
set CRC32C_INSTALL_PREFIX=%KOKORO_ARTIFACTS_DIR%\bin_win32\

C:\Python37\Scripts\cmake -G %CMAKE_GENERATOR% -A Win32 -DCRC32C_BUILD_BENCHMARKS=no -DBUILD_SHARED_LIBS=yes ^
-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=yes -DCMAKE_INSTALL_PREFIX:PATH=%CRC32C_INSTALL_PREFIX% .

C:\Python37\Scripts\cmake --build . --config RelWithDebInfo --target install
dir %CRC32C_INSTALL_PREFIX% /b /s
popd

copy %CRC32C_INSTALL_PREFIX%bin\crc32c.dll .

@rem update python deps and build wheels (requires CRC32C_INSTALL_PREFIX is set)
FOR %%V IN (3.5-32,3.6-32,3.7-32) DO (
    py -%%V -m pip install --upgrade pip setuptools wheel
    py -%%V -m pip wheel . --wheel-dir wheels/
)


