# Copyright 2021 The PyBigQuery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from unittest import mock

import google.auth
import google.auth.credentials
from google.oauth2 import service_account
import pytest


class AnonymousCredentialsWithProject(google.auth.credentials.AnonymousCredentials):
    """Fake credentials to trick isinstance"""

    def __init__(self, project):
        super().__init__()
        self.project_id = project

    def with_scopes(self, scopes):
        return self


@pytest.fixture(scope="session")
def module_under_test():
    from pybigquery import _helpers

    return _helpers


def test_create_bigquery_client_with_credentials_path(monkeypatch, module_under_test):
    mock_service_account = mock.create_autospec(service_account.Credentials)
    mock_service_account.from_service_account_file.return_value = AnonymousCredentialsWithProject(
        "service-account-project"
    )
    monkeypatch.setattr(service_account, "Credentials", mock_service_account)

    bqclient = module_under_test.create_bigquery_client(
        credentials_path="path/to/key.json",
    )

    assert bqclient.project == "service-account-project"


def test_create_bigquery_client_with_credentials_path_respects_project(
    monkeypatch, module_under_test
):
    """Test that project_id is used, even when there is a default project.

    https://github.com/googleapis/python-bigquery-sqlalchemy/issues/48
    """
    mock_service_account = mock.create_autospec(service_account.Credentials)
    mock_service_account.from_service_account_file.return_value = AnonymousCredentialsWithProject(
        "service-account-project"
    )
    monkeypatch.setattr(service_account, "Credentials", mock_service_account)

    bqclient = module_under_test.create_bigquery_client(
        credentials_path="path/to/key.json", project_id="connection-url-project",
    )

    assert bqclient.project == "connection-url-project"


def test_create_bigquery_client_with_credentials_info(monkeypatch, module_under_test):
    mock_service_account = mock.create_autospec(service_account.Credentials)
    mock_service_account.from_service_account_info.return_value = AnonymousCredentialsWithProject(
        "service-account-project"
    )
    monkeypatch.setattr(service_account, "Credentials", mock_service_account)

    bqclient = module_under_test.create_bigquery_client(
        credentials_info={
            "type": "service_account",
            "project_id": "service-account-project",
        },
    )

    assert bqclient.project == "service-account-project"


def test_create_bigquery_client_with_credentials_info_respects_project(
    monkeypatch, module_under_test
):
    """Test that project_id is used, even when there is a default project.

    https://github.com/googleapis/python-bigquery-sqlalchemy/issues/48
    """
    mock_service_account = mock.create_autospec(service_account.Credentials)
    mock_service_account.from_service_account_info.return_value = AnonymousCredentialsWithProject(
        "service-account-project"
    )
    monkeypatch.setattr(service_account, "Credentials", mock_service_account)

    bqclient = module_under_test.create_bigquery_client(
        credentials_info={
            "type": "service_account",
            "project_id": "service-account-project",
        },
        project_id="connection-url-project",
    )

    assert bqclient.project == "connection-url-project"


def test_create_bigquery_client_with_default_credentials(
    monkeypatch, module_under_test
):
    def mock_default_credentials(*args, **kwargs):
        return (google.auth.credentials.AnonymousCredentials(), "default-project")

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    bqclient = module_under_test.create_bigquery_client()

    assert bqclient.project == "default-project"


def test_create_bigquery_client_with_default_credentials_respects_project(
    monkeypatch, module_under_test
):
    """Test that project_id is used, even when there is a default project.

    https://github.com/googleapis/python-bigquery-sqlalchemy/issues/48
    """

    def mock_default_credentials(*args, **kwargs):
        return (google.auth.credentials.AnonymousCredentials(), "default-project")

    monkeypatch.setattr(google.auth, "default", mock_default_credentials)

    bqclient = module_under_test.create_bigquery_client(
        project_id="connection-url-project",
    )

    assert bqclient.project == "connection-url-project"
