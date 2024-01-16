# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import annotations

import datetime
import concurrent.futures
from unittest import mock

import freezegun
import google.cloud.bigquery
import pytest

import pandas_gbq.exceptions
import pandas_gbq.gbq
import pandas_gbq.query as module_under_test


def _make_connector(project_id: str = "some-project", **kwargs):
    return pandas_gbq.gbq.GbqConnector(project_id, **kwargs)


@pytest.mark.parametrize(
    ["size_in_bytes", "formatted_text"],
    [
        (999, "999.0 B"),
        (1024, "1.0 KB"),
        (1099, "1.1 KB"),
        (1044480, "1020.0 KB"),
        (1048576, "1.0 MB"),
        (1048576000, "1000.0 MB"),
        (1073741824, "1.0 GB"),
        (1.099512e12, "1.0 TB"),
        (1.125900e15, "1.0 PB"),
        (1.152922e18, "1.0 EB"),
        (1.180592e21, "1.0 ZB"),
        (1.208926e24, "1.0 YB"),
        (1.208926e28, "10000.0 YB"),
    ],
)
def test_query_response_bytes(size_in_bytes, formatted_text):
    assert module_under_test.sizeof_fmt(size_in_bytes) == formatted_text


def test__wait_for_query_job_exits_when_done(mock_bigquery_client):
    connector = _make_connector()
    connector.client = mock_bigquery_client
    connector.start = datetime.datetime(2020, 1, 1).timestamp()

    mock_query = mock.create_autospec(google.cloud.bigquery.QueryJob)
    type(mock_query).state = mock.PropertyMock(side_effect=("RUNNING", "DONE"))
    mock_query.result.side_effect = concurrent.futures.TimeoutError("fake timeout")

    with freezegun.freeze_time("2020-01-01 00:00:00", tick=False):
        module_under_test._wait_for_query_job(
            connector, mock_bigquery_client, mock_query, 60
        )

    mock_bigquery_client.cancel_job.assert_not_called()


def test__wait_for_query_job_cancels_after_timeout(mock_bigquery_client):
    connector = _make_connector()
    connector.client = mock_bigquery_client
    connector.start = datetime.datetime(2020, 1, 1).timestamp()

    mock_query = mock.create_autospec(google.cloud.bigquery.QueryJob)
    mock_query.job_id = "a-random-id"
    mock_query.location = "job-location"
    mock_query.state = "RUNNING"
    mock_query.result.side_effect = concurrent.futures.TimeoutError("fake timeout")

    with freezegun.freeze_time(
        "2020-01-01 00:00:00", auto_tick_seconds=15
    ), pytest.raises(pandas_gbq.exceptions.QueryTimeout):
        module_under_test._wait_for_query_job(
            connector, mock_bigquery_client, mock_query, 60
        )

    mock_bigquery_client.cancel_job.assert_called_with(
        "a-random-id", location="job-location"
    )
