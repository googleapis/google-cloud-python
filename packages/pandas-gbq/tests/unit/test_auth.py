# -*- coding: utf-8 -*-

import json
import os.path

from pandas_gbq import auth

try:
    import mock
except ImportError:  # pragma: NO COVER
    from unittest import mock


def test_get_credentials_private_key_contents(monkeypatch):
    from google.oauth2 import service_account

    @classmethod
    def from_service_account_info(cls, key_info):
        mock_credentials = mock.create_autospec(cls)
        mock_credentials.with_scopes.return_value = mock_credentials
        mock_credentials.refresh.return_value = mock_credentials
        return mock_credentials

    monkeypatch.setattr(
        service_account.Credentials,
        "from_service_account_info",
        from_service_account_info,
    )
    private_key = json.dumps(
        {
            "private_key": "some_key",
            "client_email": "service-account@example.com",
            "project_id": "private-key-project",
        }
    )
    credentials, project = auth.get_credentials(private_key=private_key)

    assert credentials is not None
    assert project == "private-key-project"


def test_get_credentials_private_key_path(monkeypatch):
    from google.oauth2 import service_account

    @classmethod
    def from_service_account_info(cls, key_info):
        mock_credentials = mock.create_autospec(cls)
        mock_credentials.with_scopes.return_value = mock_credentials
        mock_credentials.refresh.return_value = mock_credentials
        return mock_credentials

    monkeypatch.setattr(
        service_account.Credentials,
        "from_service_account_info",
        from_service_account_info,
    )
    private_key = os.path.join(
        os.path.dirname(__file__), "..", "data", "dummy_key.json"
    )
    credentials, project = auth.get_credentials(private_key=private_key)

    assert credentials is not None
    assert project is None


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
    mock_client = mock.create_autospec(google.cloud.bigquery.Client)
    monkeypatch.setattr(google.cloud.bigquery, "Client", mock_client)

    credentials, project = auth.get_credentials()
    assert project == "default-project"
    assert credentials is not None


def test_get_credentials_load_user_no_default(monkeypatch):
    import google.auth
    import google.auth.credentials

    def mock_default_credentials(scopes=None, request=None):
        return (None, None)

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)
    mock_user_credentials = mock.create_autospec(
        google.auth.credentials.Credentials
    )

    def mock_load_credentials(
        try_credentials, project_id=None, credentials_path=None
    ):
        return mock_user_credentials

    monkeypatch.setattr(
        auth, "load_user_account_credentials", mock_load_credentials
    )

    credentials, project = auth.get_credentials()
    assert project is None
    assert credentials is mock_user_credentials
