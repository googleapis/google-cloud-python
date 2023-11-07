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

try:
    import pyarrow  # type: ignore
except ImportError:  # pragma: NO COVER
    pyarrow = None

try:
    from google.cloud import bigquery_storage  # type: ignore
except ImportError:  # pragma: NO COVER
    bigquery_storage = None

try:
    import pandas  # type: ignore
except ImportError:  # pragma: NO COVER
    pandas = None

from google.cloud.bigquery import _versions_helpers
from google.cloud.bigquery import exceptions


@pytest.mark.skipif(pyarrow is None, reason="pyarrow is not installed")
def test_try_import_raises_no_error_w_recent_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="5.0.0"):
        try:
            pyarrow = versions.try_import(raise_if_error=True)
            assert pyarrow is not None
        except exceptions.LegacyPyarrowError:  # pragma: NO COVER
            raise ("Legacy error raised with a non-legacy dependency version.")


@pytest.mark.skipif(pyarrow is None, reason="pyarrow is not installed")
def test_try_import_returns_none_w_legacy_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="2.0.0"):
        pyarrow = versions.try_import()
        assert pyarrow is None


@pytest.mark.skipif(pyarrow is None, reason="pyarrow is not installed")
def test_try_import_raises_error_w_legacy_pyarrow():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="2.0.0"):
        with pytest.raises(exceptions.LegacyPyarrowError):
            versions.try_import(raise_if_error=True)


@pytest.mark.skipif(pyarrow is None, reason="pyarrow is not installed")
def test_installed_pyarrow_version_returns_cached():
    versions = _versions_helpers.PyarrowVersions()
    versions._installed_version = object()
    assert versions.installed_version is versions._installed_version


@pytest.mark.skipif(pyarrow is None, reason="pyarrow is not installed")
def test_installed_pyarrow_version_returns_parsed_version():
    versions = _versions_helpers.PyarrowVersions()
    with mock.patch("pyarrow.__version__", new="1.2.3"):
        version = versions.installed_version

    assert version.major == 1
    assert version.minor == 2
    assert version.micro == 3


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_raises_no_error_w_recent_bqstorage():
    with mock.patch("google.cloud.bigquery_storage.__version__", new="2.0.0"):
        try:
            bqstorage_versions = _versions_helpers.BQStorageVersions()
            bqstorage_versions.try_import(raise_if_error=True)
        except exceptions.LegacyBigQueryStorageError:  # pragma: NO COVER
            raise ("Legacy error raised with a non-legacy dependency version.")


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_raises_error_w_legacy_bqstorage():
    with mock.patch("google.cloud.bigquery_storage.__version__", new="1.9.9"):
        with pytest.raises(exceptions.LegacyBigQueryStorageError):
            bqstorage_versions = _versions_helpers.BQStorageVersions()
            bqstorage_versions.try_import(raise_if_error=True)


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_returns_none_with_legacy_bqstorage():
    with mock.patch("google.cloud.bigquery_storage.__version__", new="1.9.9"):
        try:
            bqstorage_versions = _versions_helpers.BQStorageVersions()
            bq_storage = bqstorage_versions.try_import()
        except exceptions.LegacyBigQueryStorageError:  # pragma: NO COVER
            raise ("Legacy error raised when raise_if_error == False.")
        assert bq_storage is None


@pytest.mark.skipif(
    bigquery_storage is not None,
    reason="Tests behavior when `google-cloud-bigquery-storage` isn't installed",
)
def test_returns_none_with_bqstorage_uninstalled():
    try:
        bqstorage_versions = _versions_helpers.BQStorageVersions()
        bq_storage = bqstorage_versions.try_import()
    except exceptions.LegacyBigQueryStorageError:  # pragma: NO COVER
        raise ("NotFound error raised when raise_if_error == False.")
    assert bq_storage is None


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_raises_error_w_unknown_bqstorage_version():
    with mock.patch("google.cloud.bigquery_storage", autospec=True) as fake_module:
        del fake_module.__version__
        error_pattern = r"version found: 0.0.0"
        with pytest.raises(exceptions.LegacyBigQueryStorageError, match=error_pattern):
            bqstorage_versions = _versions_helpers.BQStorageVersions()
            bqstorage_versions.try_import(raise_if_error=True)


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_installed_bqstorage_version_returns_cached():
    bqstorage_versions = _versions_helpers.BQStorageVersions()
    bqstorage_versions._installed_version = object()
    assert bqstorage_versions.installed_version is bqstorage_versions._installed_version


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_installed_bqstorage_version_returns_parsed_version():
    bqstorage_versions = _versions_helpers.BQStorageVersions()
    with mock.patch("google.cloud.bigquery_storage.__version__", new="1.2.3"):
        bqstorage_versions = bqstorage_versions.installed_version

    assert bqstorage_versions.major == 1
    assert bqstorage_versions.minor == 2
    assert bqstorage_versions.micro == 3


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_bqstorage_is_read_session_optional_true():
    bqstorage_versions = _versions_helpers.BQStorageVersions()
    with mock.patch("google.cloud.bigquery_storage.__version__", new="2.6.0"):
        assert bqstorage_versions.is_read_session_optional


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_bqstorage_is_read_session_optional_false():
    bqstorage_versions = _versions_helpers.BQStorageVersions()
    with mock.patch("google.cloud.bigquery_storage.__version__", new="2.5.0"):
        assert not bqstorage_versions.is_read_session_optional


@pytest.mark.skipif(pandas is None, reason="pandas is not installed")
@pytest.mark.parametrize("version", ["1.5.0", "2.0.0", "2.1.0"])
def test_try_import_raises_no_error_w_recent_pandas(version):
    versions = _versions_helpers.PandasVersions()
    with mock.patch("pandas.__version__", new=version):
        try:
            pandas = versions.try_import(raise_if_error=True)
            assert pandas is not None
        except exceptions.LegacyPandasError:  # pragma: NO COVER
            raise ("Legacy error raised with a non-legacy dependency version.")


@pytest.mark.skipif(pandas is None, reason="pandas is not installed")
def test_try_import_returns_none_w_legacy_pandas():
    versions = _versions_helpers.PandasVersions()
    with mock.patch("pandas.__version__", new="1.0.0"):
        pandas = versions.try_import()
        assert pandas is None


@pytest.mark.skipif(pandas is None, reason="pandas is not installed")
def test_try_import_raises_error_w_legacy_pandas():
    versions = _versions_helpers.PandasVersions()
    with mock.patch("pandas.__version__", new="1.0.0"):
        with pytest.raises(exceptions.LegacyPandasError):
            versions.try_import(raise_if_error=True)


@pytest.mark.skipif(pandas is None, reason="pandas is not installed")
def test_installed_pandas_version_returns_cached():
    versions = _versions_helpers.PandasVersions()
    versions._installed_version = object()
    assert versions.installed_version is versions._installed_version


@pytest.mark.skipif(pandas is None, reason="pandas is not installed")
def test_installed_pandas_version_returns_parsed_version():
    versions = _versions_helpers.PandasVersions()
    with mock.patch("pandas.__version__", new="1.1.0"):
        version = versions.installed_version

    assert version.major == 1
    assert version.minor == 1
    assert version.micro == 0
