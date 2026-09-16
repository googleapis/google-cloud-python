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

cd /d %~dp0..\..\..\packages\google-crc32c || goto :error

if "%PUBLISH_WHEELS%"=="" set PUBLISH_WHEELS=true

@echo "Build and Test Wheels"
call scripts\windows\build.bat || goto :error

@echo "Ensure that we have the latest versions of Twine, Wheel, Setuptools, and pkginfo."
call py -3 -m pip install --upgrade twine wheel setuptools pkginfo || goto :error

@echo "Build the source distribution (sdist) and validate with twine check"
call py -3 setup.py sdist || goto :error
call py -3 -m twine check dist/* wheels/google_crc32c* || goto :error

if "%PUBLISH_WHEELS%"=="true" (
    @echo "Start the releasetool reporter"
    call py -3 -m pip install gcp-releasetool || goto :error
    if not exist C:\temp mkdir C:\temp
    call py -3 -m releasetool publish-reporter-script > C:\temp\publisher-script || goto :error

    @echo "Disable buffering, so that the logs stream through."
    set PYTHONUNBUFFERED=1

    @echo "## RELEASE WORKFLOW SUCCESSFUL ##"
    @echo "## Uploading Wheels and sdist ##"

    set /p TWINE_PASSWORD=<%KOKORO_KEYSTORE_DIR%/73713_google-cloud-pypi-token-keystore-3
    call py -3 -m twine upload --skip-existing --username __token__ --password "%TWINE_PASSWORD%" dist/* wheels/google_crc32c* || goto :error
    dir wheels
    dir dist
) else (
    @echo "PUBLISH_WHEELS is '%PUBLISH_WHEELS%'. Skipping PyPI upload after sdist and wheel validation."
)

goto :EOF

:error
exit /b 1
