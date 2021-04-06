import google.auth.credentials
import mock
import pytest


@pytest.fixture
def creds():
    """
    Provide test creds to unit tests so that they can run without
    GOOGLE_APPLICATION_CREDENTIALS set.
    """
    yield mock.Mock(spec=google.auth.credentials.Credentials)
