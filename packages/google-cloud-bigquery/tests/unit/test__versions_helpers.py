# Copyright 2023 Google LLC
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

import pytest

import mock

from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import exceptions

pyarrow = pytest.importorskip("pyarrow")


def test_try_import_raises_no_error_w_recent_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="5.0.0"):
        try:
            pyarrow = versions.try_import(raise_if_error=True)
            assert pyarrow is not None
        except exceptions.LegacyPyarrowError:  # pragma: NO COVER
            raise ("Legacy error raised with a non-legacy dependency version.")


def test_try_import_returns_none_w_legacy_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="2.0.0"):
        pyarrow = versions.try_import()
        assert pyarrow is None


def test_try_import_raises_error_w_legacy_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="2.0.0"):
        with pytest.raises(exceptions.LegacyPyarrowError):
            versions.try_import(raise_if_error=True)


def test_installed_version_returns_cached():
    versions = _versions_helpers.PyarrowVersions()
    versions._installed_version = object()
    assert versions.installed_version is versions._installed_version


def test_installed_version_returns_parsed_version():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="1.2.3"):
        version = versions.installed_version

    assert version.major == 1
    assert version.minor == 2
    assert version.micro == 3
