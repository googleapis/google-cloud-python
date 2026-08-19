# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import unittest.mock as mock

import google.cloud.bigquery
import pytest

import bigframes.session.time

INITIAL_BQ_TIME = datetime.datetime(
    year=2020,
    month=4,
    day=24,
    hour=8,
    minute=55,
    second=29,
    tzinfo=datetime.timezone.utc,
)


@pytest.fixture()
def bq_client():
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)

    def query_and_wait_mock(query, *args, **kwargs):
        if query.startswith("SELECT CURRENT_TIMESTAMP()"):
            return iter([[INITIAL_BQ_TIME]])
        else:
            return ValueError(f"mock cannot handle query : {query}")

    bqclient.query_and_wait = query_and_wait_mock
    return bqclient


def test_bqsyncedclock_get_time(bq_client):
    freezegun = pytest.importorskip("freezegun")

    # this initial local time is actually irrelevant, only the ticks matter
    initial_local_datetime = datetime.datetime(
        year=1, month=7, day=12, hour=15, minute=6, second=3
    )

    with freezegun.freeze_time(initial_local_datetime) as frozen_datetime:
        clock = bigframes.session.time.BigQuerySyncedClock(bq_client)

        t1 = clock.get_time()
        assert t1 == INITIAL_BQ_TIME

        frozen_datetime.tick(datetime.timedelta(seconds=3))
        t2 = clock.get_time()
        assert t2 == INITIAL_BQ_TIME + datetime.timedelta(seconds=3)

        frozen_datetime.tick(datetime.timedelta(seconds=23529385))
        t3 = clock.get_time()
        assert t3 == INITIAL_BQ_TIME + datetime.timedelta(
            seconds=3
        ) + datetime.timedelta(seconds=23529385)
