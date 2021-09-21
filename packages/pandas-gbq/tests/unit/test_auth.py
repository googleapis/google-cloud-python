# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-

import json
from unittest import mock

import pytest

from pandas_gbq import auth


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

    def mock_default_credentials(scopes=None, request=None):
        return (
            mock.create_autospec(google.auth.credentials.Credentials),
            "default-project",
        )

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    credentials, project = auth.get_credentials()
    assert project == "default-project"
    assert credentials is not None


def test_get_credentials_load_user_no_default(monkeypatch):
    import google.auth
    import google.auth.credentials
    import pydata_google_auth.cache

    def mock_default_credentials(scopes=None, request=None):
        return (None, None)

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)
    mock_user_credentials = mock.create_autospec(google.auth.credentials.Credentials)

    mock_cache = mock.create_autospec(pydata_google_auth.cache.CredentialsCache)
    mock_cache.load.return_value = mock_user_credentials

    monkeypatch.setattr(auth, "get_credentials_cache", lambda _: mock_cache)

    credentials, project = auth.get_credentials()
    assert project is None
    assert credentials is mock_user_credentials


def test_get_credentials_cache_w_reauth():
    import pydata_google_auth.cache

    cache = auth.get_credentials_cache(True)
    assert isinstance(cache, pydata_google_auth.cache.WriteOnlyCredentialsCache)
