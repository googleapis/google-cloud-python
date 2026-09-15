@rem Copyright 2026 Google LLC
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem     https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.

setlocal ENABLEDELAYEDEXPANSION

FOR %%P IN (3.10, 3.11, 3.12, 3.13, 3.14) DO (
    echo "Building for Python version %%P"
    set python_version=%%P
    set python_version_trimmed=!python_version:~0,4!

    py -!python_version_trimmed!-64 -m pip install --upgrade pip setuptools wheel
    py -!python_version_trimmed!-64 -m pip install -r scripts\dev-requirements.txt

    mkdir wheels 2>nul
    py -!python_version_trimmed!-64 -m pip wheel . --wheel-dir wheels\

    call %~dp0\test.bat !python_version_trimmed! || goto :error
)

goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%
