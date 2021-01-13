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


setlocal ENABLEDELAYEDEXPANSION

set CMAKE_GENERATOR="Visual Studio 16 2019"
set CONFIGURATION=RelWithDebInfo
set CRC32C_INSTALL_PREFIX=%cd%\build\%CONFIGURATION%

@rem Path to cmake, env var to make it easier to point to a specific version
set cmake=cmake

@rem python version should be set as an argument, if not, default to python 3.9
set PYTHON_VERSION=%1
if "%PYTHON_VERSION%"=="" (
  echo "Python version was not provided, using Python 3.9"
  set PYTHON_VERSION=3.9
)

py -0
py -%PYTHON_VERSION% -m pip install cmake

git submodule update --init --recursive

FOR %%V IN (32,64) DO (
    set TARGET_PLATFORM="x64"

    if "%%V"=="32" (
        set TARGET_PLATFORM="Win32"
    )
    echo "Target Platform: !TARGET_PLATFORM!"

    pushd google_crc32c

    @rem reset hard to cleanup any changes done by a previous build.
    git reset --hard
    git clean -fxd

    del /s /q CMakeFiles\
    del CMakeCache.txt

    mkdir build
    cd build

    echo "Running cmake with Generator:  %CMAKE_GENERATOR%, Platform: !TARGET_PLATFORM!, Install Prefix: %CRC32C_INSTALL_PREFIX%"

    %cmake% -G %CMAKE_GENERATOR% -A !TARGET_PLATFORM! -DCRC32C_BUILD_BENCHMARKS=no -DCRC32C_BUILD_TESTS=no -DBUILD_SHARED_LIBS=yes -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=yes -DCRC32C_USE_GLOG=0 -DCMAKE_INSTALL_PREFIX:PATH=%CRC32C_INSTALL_PREFIX% ..

    %cmake% --build . --config "%CONFIGURATION%" --target install

    dir %CRC32C_INSTALL_PREFIX% /b /s
    popd

    dir  %CRC32C_INSTALL_PREFIX%\bin
    echo "Copying Binary to root: %CRC32C_INSTALL_PREFIX%\bin\crc32c.dll"
    copy %CRC32C_INSTALL_PREFIX%\bin\crc32c.dll .

    py -%PYTHON_VERSION%-%%V -m pip install --upgrade pip setuptools wheel
    py -%PYTHON_VERSION%-%%V -m pip wheel . --wheel-dir wheels/
)
