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

"""Unit tests for read_gbq_table helper functions."""

import datetime

import google.cloud.bigquery as bigquery

import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table

from .. import resources


def test_get_ibis_time_travel_table_doesnt_timetravel_anonymous_datasets():
    bqsession = resources.create_bigquery_session()

    table_ref = bigquery.TableReference.from_string(
        "my-test-project._e8166e0cdb.anonbb92cd"
    )

    table_expression = bf_read_gbq_table.get_ibis_time_travel_table(
        bqsession.ibis_client,
        table_ref,
        index_cols=(),
        columns=(),
        filters=(),
        time_travel_timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    sql = table_expression.compile()

    # Anonymous query results tables don't support time travel.
    assert "SYSTEM_TIME" not in sql

    # Need fully-qualified table name.
    assert "my-test-project" in sql
