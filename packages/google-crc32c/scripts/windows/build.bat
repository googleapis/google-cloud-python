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

set CMAKE_GENERATOR="Visual Studio 17 2022"
set CONFIGURATION=RelWithDebInfo
set CRC32C_INSTALL_PREFIX=%cd%\build\%CONFIGURATION%

@rem Iterate through supported Python versions.
@rem Unfortunately pyenv for Windows has an out-of-date versions list. Choco's
@rem installer seems to have some problems with installing multiple versions at
@rem once, so as a workaround, we will install and then uninstall every version.
FOR %%P IN (3.9, 3.10, 3.11, 3.12) DO (

    echo "Installing Python version %%P"
    choco install python --version=%%P -y --no-progress

    echo "Listing available Python versions'
    py -0

    py -%%P-64 -m pip install --upgrade pip

    echo "Installing cmake for Python %%P"
    py -%%P-64 -m pip install cmake

    @rem Add directory as safe to avoid "detected dubious ownership" fatal issue
    git config --global --add safe.directory %cd%
    git config --global --add safe.directory C:/tmpfs/src/github/python-crc32c
    git submodule update --init --recursive

    git config --global --add safe.directory %cd%\google_crc32c
    git config --global --add safe.directory C:/tmpfs/src/github/python-crc32c/google_crc32c
    pushd google_crc32c
    @rem reset hard to cleanup any changes done by a previous build.
    git reset --hard
    git clean -fxd

    del /s /q CMakeFiles\
    del CMakeCache.txt

    mkdir build
    cd build

    echo "Running cmake with Generator:  %CMAKE_GENERATOR%, Platform: x64, Install Prefix: %CRC32C_INSTALL_PREFIX%"

    py -%%P-64 -m cmake -G %CMAKE_GENERATOR% -A x64 -DCRC32C_BUILD_BENCHMARKS=no -DCRC32C_BUILD_TESTS=no -DBUILD_SHARED_LIBS=yes -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=yes -DCRC32C_USE_GLOG=0 -DCMAKE_INSTALL_PREFIX:PATH=%CRC32C_INSTALL_PREFIX% ..

    py -%%P-64 -m cmake --build . --config "%CONFIGURATION%" --target install

    dir %CRC32C_INSTALL_PREFIX% /b /s
    popd

    dir  %CRC32C_INSTALL_PREFIX%\bin
    echo "Copying Binary to root: %CRC32C_INSTALL_PREFIX%\bin\crc32c.dll"
    copy %CRC32C_INSTALL_PREFIX%\bin\crc32c.dll .

    py -%%P-64 -m pip install --upgrade pip setuptools wheel
    echo "Building C extension"
    py -%%P-64 setup.py build_ext -v --include-dirs=%CRC32C_INSTALL_PREFIX%\include --library-dirs=%CRC32C_INSTALL_PREFIX%\lib
    echo "Building Wheel"
    py -%%P-64 -m pip wheel . --wheel-dir wheels/

    echo "Built wheel, now running tests."
    call %~dp0/test.bat %%P || goto :error

    echo "Finished with Python version %%P, now uninstalling"
    choco uninstall python -y
)
