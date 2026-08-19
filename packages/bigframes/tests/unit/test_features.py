# Copyright 2024 Google LLC
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

import pandas
import pytest

import bigframes.features


def test_pandas_installed_version_returns_cached():
    versions = bigframes.features.PandasVersions()
    versions._installed_version = object()
    assert versions.installed_version is versions._installed_version


def test_pandas_installed_version_returns_parsed_version(monkeypatch):
    versions = bigframes.features.PandasVersions()
    monkeypatch.setattr(pandas, "__version__", "1.2.3")
    major, minor, micro = versions.installed_version
    assert major == "1"
    assert minor == "2"
    assert micro == "3"


@pytest.mark.parametrize(
    ("version", "expected"),
    (
        ("1.2.3", False),
        ("1.5.3", False),
        ("2.0.0", True),
        ("2.2.3", True),
        ("3.0.0", True),
    ),
)
def test_pandas_is_arrow_list_dtype_usable(version, expected):
    versions = bigframes.features.PandasVersions()
    versions._installed_version = version.split(".")
    assert versions.is_arrow_list_dtype_usable == expected
