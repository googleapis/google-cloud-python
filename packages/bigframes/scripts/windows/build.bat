@rem Copyright 2024 Google LLC
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

:; Change directory to repo root.
SET script_dir="%~dp0"
cd "%~dp0"\..\..

echo "Listing available Python versions'
py -0 || goto :error

py -3.10 -m pip install --upgrade pip || goto :error
py -3.10 -m pip install --upgrade pip setuptools wheel || goto :error

echo "Building Wheel"
py -3.10 -m pip wheel . --wheel-dir wheels || goto :error/

echo "Built wheel, now running tests."
call "%script_dir%"/test.bat 3.10 || goto :error

echo "Windows build has completed successfully"

:; https://stackoverflow.com/a/46813196/101923
:; exit 0
exit /b 0

:error
exit /b %errorlevel%
