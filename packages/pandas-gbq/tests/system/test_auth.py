"""System tests for fetching Google BigQuery credentials."""

try:
    import mock
except ImportError:  # pragma: NO COVER
    from unittest import mock
import pytest

from pandas_gbq import auth


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

    return auth._try_credentials(project, credentials) is not None


def test_should_be_able_to_get_valid_credentials(project_id, private_key_path):
    credentials, _ = auth.get_credentials(
        project_id=project_id, private_key=private_key_path
    )
    assert credentials.valid


def test_get_service_account_credentials_private_key_path(private_key_path):
    from google.auth.credentials import Credentials

    credentials, project_id = auth.get_service_account_credentials(
        private_key_path
    )
    assert isinstance(credentials, Credentials)
    assert auth._try_credentials(project_id, credentials) is not None


def test_get_service_account_credentials_private_key_contents(
    private_key_contents
):
    from google.auth.credentials import Credentials

    credentials, project_id = auth.get_service_account_credentials(
        private_key_contents
    )
    assert isinstance(credentials, Credentials)
    assert auth._try_credentials(project_id, credentials) is not None


def test_get_application_default_credentials_does_not_throw_error():
    if _check_if_can_get_correct_default_credentials():
        # Can get real credentials, so mock it out to fail.
        from google.auth.exceptions import DefaultCredentialsError

        with mock.patch(
            "google.auth.default", side_effect=DefaultCredentialsError()
        ):
            credentials, _ = auth.get_application_default_credentials()
    else:
        credentials, _ = auth.get_application_default_credentials()
    assert credentials is None


def test_get_application_default_credentials_returns_credentials():
    if not _check_if_can_get_correct_default_credentials():
        pytest.skip("Cannot get default_credentials " "from the environment!")
    from google.auth.credentials import Credentials

    credentials, default_project = auth.get_application_default_credentials()

    assert isinstance(credentials, Credentials)
    assert default_project is not None


@pytest.mark.local_auth
def test_get_user_account_credentials_bad_file_returns_credentials():
    from google.auth.credentials import Credentials

    with mock.patch("__main__.open", side_effect=IOError()):
        credentials = auth.get_user_account_credentials()
    assert isinstance(credentials, Credentials)


@pytest.mark.local_auth
def test_get_user_account_credentials_returns_credentials(project_id):
    from google.auth.credentials import Credentials

    credentials = auth.get_user_account_credentials(
        project_id=project_id, auth_local_webserver=True
    )
    assert isinstance(credentials, Credentials)


@pytest.mark.local_auth
def test_get_user_account_credentials_reauth_returns_credentials(project_id):
    from google.auth.credentials import Credentials

    credentials = auth.get_user_account_credentials(
        project_id=project_id, auth_local_webserver=True, reauth=True
    )
    assert isinstance(credentials, Credentials)
