# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""System tests for fetching Google BigQuery credentials."""

import os
from unittest import mock

import pytest

from pandas_gbq import auth


def mock_default_credentials(scopes=None, request=None):
    return (None, None)


def _try_credentials(project_id, credentials):
    from google.cloud import bigquery
    import google.api_core.exceptions
    import google.auth.exceptions

    if not credentials:
        return None
    if not project_id:
        return credentials

    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
        # Check if the application has rights to the BigQuery project
        client.query("SELECT 1").result()
        return credentials
    except google.api_core.exceptions.GoogleAPIError:
        return None
    except google.auth.exceptions.RefreshError:
        # Sometimes (such as on Travis) google-auth returns GCE credentials,
        # but fetching the token for those credentials doesn't actually work.
        # See:
        # https://github.com/googleapis/google-auth-library-python/issues/287
        return None


def _check_if_can_get_correct_default_credentials():
    # Checks if "Application Default Credentials" can be fetched
    # from the environment the tests are running in.
    # See https://github.com/pandas-dev/pandas/issues/13577

    import google.auth
    from google.auth.exceptions import DefaultCredentialsError
    import pandas_gbq.auth
    import pandas_gbq.gbq

    try:
        credentials, project = google.auth.default(
            scopes=pandas_gbq.auth.SCOPES
        )
    except (DefaultCredentialsError, IOError):
        return False

    return _try_credentials(project, credentials) is not None


def test_should_be_able_to_get_valid_credentials(project_id, private_key_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private_key_path
    credentials, _ = auth.get_credentials(project_id=project_id)
    assert credentials.valid


@pytest.mark.local_auth
def test_get_credentials_bad_file_returns_user_credentials(
    project_id, monkeypatch
):
    import google.auth
    from google.auth.credentials import Credentials

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    with mock.patch("__main__.open", side_effect=IOError()):
        credentials, _ = auth.get_credentials(
            project_id=project_id, auth_local_webserver=True
        )
    assert isinstance(credentials, Credentials)


@pytest.mark.local_auth
def test_get_credentials_user_credentials_with_reauth(project_id, monkeypatch):
    import google.auth

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    credentials, _ = auth.get_credentials(
        project_id=project_id, reauth=True, auth_local_webserver=True
    )
    assert credentials.valid


@pytest.mark.local_auth
def test_get_credentials_user_credentials(project_id, monkeypatch):
    import google.auth

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    credentials, _ = auth.get_credentials(
        project_id=project_id, auth_local_webserver=True
    )
    assert credentials.valid
