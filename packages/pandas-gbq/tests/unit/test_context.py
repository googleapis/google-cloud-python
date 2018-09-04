# -*- coding: utf-8 -*-

try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock

import pytest


@pytest.fixture(autouse=True)
def mock_get_credentials(monkeypatch):
    from pandas_gbq import auth
    import google.auth.credentials

    mock_credentials = mock.MagicMock(google.auth.credentials.Credentials)
    mock_get_credentials = mock.Mock()
    mock_get_credentials.return_value = (mock_credentials, "my-project")

    monkeypatch.setattr(auth, "get_credentials", mock_get_credentials)
    return mock_get_credentials


def test_read_gbq_should_save_credentials(mock_get_credentials):
    import pandas_gbq

    assert pandas_gbq.context.credentials is None
    assert pandas_gbq.context.project is None

    pandas_gbq.read_gbq("SELECT 1", dialect="standard")

    assert mock_get_credentials.call_count == 1
    mock_get_credentials.reset_mock()
    assert pandas_gbq.context.credentials is not None
    assert pandas_gbq.context.project is not None

    pandas_gbq.read_gbq("SELECT 1", dialect="standard")
    mock_get_credentials.assert_not_called()
