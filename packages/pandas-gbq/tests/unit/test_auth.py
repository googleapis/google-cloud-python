# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-

import json
import logging
import os
import stat
from unittest import mock

import pytest

from pandas_gbq import auth

posix_only = pytest.mark.skipif(
    os.name == "nt", reason="POSIX file modes do not apply on Windows."
)


def test_get_credentials_private_key_raises_notimplementederror(monkeypatch):
    private_key = json.dumps(
        {
            "private_key": "some_key",
            "client_email": "service-account@example.com",
            "project_id": "private-key-project",
        }
    )
    with pytest.raises(NotImplementedError, match="private_key"):
        auth.get_credentials(private_key=private_key)


def test_get_credentials_default_credentials(monkeypatch):
    import google.auth
    import google.auth.credentials
    import google.cloud.bigquery
    import pydata_google_auth

    mock_user_credentials = mock.create_autospec(google.auth.credentials.Credentials)

    def mock_default_credentials(scopes, **kwargs):
        return (mock_user_credentials, "test-project")

    monkeypatch.setattr(pydata_google_auth, "default", mock_default_credentials)

    credentials, project = auth.get_credentials()
    assert project == "test-project"
    assert credentials is not None


def test_get_credentials_load_user_no_default(monkeypatch):
    import google.auth
    import google.auth.credentials
    import pydata_google_auth
    import pydata_google_auth.cache

    mock_user_credentials = mock.create_autospec(google.auth.credentials.Credentials)

    def mock_default_credentials(scopes, **kwargs):
        return (mock_user_credentials, None)

    monkeypatch.setattr(pydata_google_auth, "default", mock_default_credentials)

    credentials, project = auth.get_credentials()
    assert project is None
    assert credentials is mock_user_credentials


def test_get_credentials_cache_w_reauth():
    import pydata_google_auth.cache

    cache = auth.get_credentials_cache(True)
    assert isinstance(cache, pydata_google_auth.cache.WriteOnlyCredentialsCache)


def test_get_credentials_cache_wo_reauth():
    import pydata_google_auth.cache

    cache = auth.get_credentials_cache(False)
    assert isinstance(cache, pydata_google_auth.cache.ReadWriteCredentialsCache)


CACHED_CREDENTIALS_JSON = json.dumps(
    {
        "refresh_token": "my-refresh-token",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "my-client-id",
        "client_secret": "my-client-secret",
        "type": "authorized_user",
    }
)


def _file_mode(path):
    return stat.S_IMODE(os.stat(path).st_mode)


class RecordingCredentials:
    """Fake user credentials that record the mode of the cache file.

    pydata-google-auth reads ``refresh_token`` while it writes the cache file,
    so ``modes_seen`` holds the mode the file has when the token is saved.
    """

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.modes_seen = []
        self.id_token = None
        self.token_uri = "https://oauth2.googleapis.com/token"
        self.client_id = "my-client-id"
        self.client_secret = "my-client-secret"
        self.scopes = auth.SCOPES

    @property
    def refresh_token(self):
        self.modes_seen.append(_file_mode(self.cache_path))
        return "my-refresh-token"


@pytest.fixture
def cache_path(monkeypatch, tmp_path):
    """Points the credentials cache at tmp_path and sets the umask to 022.

    Yields the path of the cache file.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    old_umask = os.umask(0o022)
    yield tmp_path / ".config" / "pandas_gbq" / "bigquery_credentials.dat"
    os.umask(old_umask)


@pytest.fixture
def no_refresh(monkeypatch):
    """Keeps loaded credentials from refreshing over the network."""
    import google.oauth2.credentials

    monkeypatch.setattr(
        google.oauth2.credentials.Credentials, "refresh", lambda self, request: None
    )


@posix_only
@pytest.mark.parametrize("umask", [0o022, 0o000], ids=["umask022", "umask000"])
@pytest.mark.parametrize("reauth", [False, True])
def test_get_credentials_cache_save_creates_owner_only_file(cache_path, reauth, umask):
    os.umask(umask)
    credentials = RecordingCredentials(cache_path)

    auth.get_credentials_cache(reauth).save(credentials)

    assert set(credentials.modes_seen) == {0o600}
    assert _file_mode(cache_path) == 0o600
    assert _file_mode(cache_path.parent) == 0o700
    assert json.loads(cache_path.read_text())["refresh_token"] == "my-refresh-token"


@posix_only
@pytest.mark.parametrize("reauth", [False, True])
def test_get_credentials_cache_save_restricts_existing_file(cache_path, reauth):
    # Simulate a cache file from an earlier version, which other users can read.
    cache_path.parent.mkdir(parents=True)
    cache_path.write_text(CACHED_CREDENTIALS_JSON)
    cache_path.chmod(0o644)
    credentials = RecordingCredentials(cache_path)

    auth.get_credentials_cache(reauth).save(credentials)

    assert set(credentials.modes_seen) == {0o600}
    assert _file_mode(cache_path) == 0o600


@posix_only
def test_get_credentials_cache_load_restricts_existing_file(cache_path, no_refresh):
    # Simulate a cache file from an earlier version, which other users can read.
    cache_path.parent.mkdir(parents=True)
    cache_path.write_text(CACHED_CREDENTIALS_JSON)
    cache_path.chmod(0o644)

    credentials = auth.get_credentials_cache(False).load()

    assert credentials.refresh_token == "my-refresh-token"
    assert _file_mode(cache_path) == 0o600


@posix_only
def test_get_credentials_cache_load_wo_file(cache_path):
    assert auth.get_credentials_cache(False).load() is None
    assert not cache_path.parent.exists()


@posix_only
def test_get_credentials_cache_save_keeps_existing_directory_mode(cache_path):
    cache_path.parent.mkdir(parents=True)
    cache_path.parent.chmod(0o755)

    auth.get_credentials_cache(False).save(RecordingCredentials(cache_path))

    assert _file_mode(cache_path.parent) == 0o755
    assert _file_mode(cache_path) == 0o600


@posix_only
def test_get_credentials_cache_leaves_directory_at_cache_path_alone(cache_path):
    cache_path.mkdir(parents=True)
    cache_path.chmod(0o755)
    cache = auth.get_credentials_cache(False)

    assert cache.load() is None
    cache.save(RecordingCredentials(cache_path))

    assert _file_mode(cache_path) == 0o755


@posix_only
def test_get_credentials_cache_chmod_failure_does_not_fail_auth(
    cache_path, no_refresh, monkeypatch, caplog
):
    cache_path.parent.mkdir(parents=True)
    cache_path.write_text(CACHED_CREDENTIALS_JSON)
    cache_path.chmod(0o644)

    def chmod_not_permitted(path, mode):
        raise PermissionError("Operation not permitted")

    monkeypatch.setattr(os, "chmod", chmod_not_permitted)
    cache = auth.get_credentials_cache(False)

    with caplog.at_level(logging.WARNING, logger="pandas_gbq.auth"):
        cache.save(RecordingCredentials(cache_path))
        credentials = cache.load()

    assert credentials.refresh_token == "my-refresh-token"
    assert "Unable to restrict access" in caplog.text


def test_get_credentials_cache_on_windows_leaves_file_mode_alone(
    monkeypatch, tmp_path, no_refresh
):
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setenv("APPDATA", str(tmp_path))
    cache_path = tmp_path / "pandas_gbq" / "bigquery_credentials.dat"
    cache_path.parent.mkdir()
    cache_path.write_text(CACHED_CREDENTIALS_JSON)
    cache_path.chmod(0o644)
    mode_before = _file_mode(cache_path)

    credentials = auth.get_credentials_cache(False).load()

    assert credentials.refresh_token == "my-refresh-token"
    assert _file_mode(cache_path) == mode_before


def test_make_cache_file_private_wo_path_does_nothing():
    # object() has no _path attribute. The helper must skip it instead of raising.
    auth._make_cache_file_private(object(), create=True)


@posix_only
@pytest.mark.parametrize("reauth", [False, True])
def test_get_credentials_saves_owner_only_file(cache_path, monkeypatch, reauth):
    import pydata_google_auth

    credentials = RecordingCredentials(cache_path)

    def mock_default_credentials(scopes, credentials_cache=None, **kwargs):
        credentials_cache.save(credentials)
        return mock.sentinel.credentials, "test-project"

    monkeypatch.setattr(pydata_google_auth, "default", mock_default_credentials)

    auth.get_credentials(reauth=reauth)

    assert set(credentials.modes_seen) == {0o600}
    assert _file_mode(cache_path) == 0o600
