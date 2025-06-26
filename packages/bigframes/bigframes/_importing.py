# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
from types import ModuleType

from packaging import version

# Keep this in sync with setup.py
POLARS_MIN_VERSION = version.Version("1.7.0")


def import_polars() -> ModuleType:
    polars_module = importlib.import_module("polars")
    imported_version = version.Version(polars_module.build_info()["version"])
    if imported_version < POLARS_MIN_VERSION:
        raise ImportError(
            f"Imported polars version: {imported_version} is below the minimum version: {POLARS_MIN_VERSION}"
        )
    return polars_module
