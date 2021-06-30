# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-

from unittest import mock

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


def test_read_gbq_should_use_dialect(mock_bigquery_client):
    import pandas_gbq

    assert pandas_gbq.context.dialect is None
    pandas_gbq.context.dialect = "legacy"
    pandas_gbq.read_gbq("SELECT 1")

    _, kwargs = mock_bigquery_client.query.call_args
    assert kwargs["job_config"].use_legacy_sql

    pandas_gbq.context.dialect = "standard"
    pandas_gbq.read_gbq("SELECT 1")

    _, kwargs = mock_bigquery_client.query.call_args
    assert not kwargs["job_config"].use_legacy_sql
    pandas_gbq.context.dialect = None  # Reset the global state.
