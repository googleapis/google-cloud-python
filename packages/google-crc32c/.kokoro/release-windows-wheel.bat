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

@echo "Starting Windows release"

cd /d %~dp0
cd ..

@echo "Build Wheel"
call scripts\windows\build.bat || goto :error

@echo "Start the releasetool reporter"
call py -3 -m pip install gcp-releasetool || goto :error
call py -3 -m releasetool publish-reporter-script > C:\temp\publisher-script || goto :error

@echo "Ensure that we have the latest versions of Twine, Wheel, and Setuptools."
call py -3 -m pip install --upgrade twine wheel setuptools || goto :error

@echo "Disable buffering, so that the logs stream through."
set PYTHONUNBUFFERED=1

@echo "## RELASE WORKFLOW SUCCESSFUL ##"
@echo "## Uploading Wheels ##"

@echo "Move into the package, build the distribution and upload."
set /p TWINE_PASSWORD=<%KOKORO_KEYSTORE_DIR%/73713_google-cloud-pypi-token-keystore-3
call py -3 setup.py sdist || goto :error
call py -3 -m twine upload --skip-existing --username __token__ --password "%TWINE_PASSWORD%" dist/* wheels/google_crc32c* || goto :error

goto :EOF

:error
exit /b 1
