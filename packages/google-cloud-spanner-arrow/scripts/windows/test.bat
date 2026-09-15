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

set python_version=%1

py -%python_version%-64 -m venv test_venv
call test_venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install --no-index --find-links=wheels google-cloud-spanner-arrow
python -m pip install pytest

pytest tests
python scripts\check_spanner_arrow_extension.py

call deactivate
rmdir /s /q test_venv
