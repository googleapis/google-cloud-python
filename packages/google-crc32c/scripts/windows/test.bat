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

@rem python version should be set as an argument, if not, default to python 3.9
set PYTHON_VERSION=%1
if "%PYTHON_VERSION%"=="" (
  echo "Python version was not provided, using Python 3.9"
  set PYTHON_VERSION=3.9
)

@rem update python deps and build wheels (requires CRC32C_INSTALL_PREFIX is set)
@rem FOR %%V IN (3.5-64,3.5-32,3.6-64,3.6-32,3.7-64,3.7-32) DO (
@REM FOR %%V IN (3.9-64,3.9-32) DO (
FOR %%V IN (%PYTHON_VERSION%-32, %PYTHON_VERSION%-64) DO (
    py -%%V -m pip install cffi pyparser
    py -%%V -m pip install --no-index --find-links=wheels google-crc32c --force-reinstall
    py -%%V -m pip install pytest
    py -%%V -m pytest tests
)