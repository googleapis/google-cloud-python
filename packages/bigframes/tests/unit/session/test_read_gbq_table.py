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


def test_create_snapshot_sql_doesnt_timetravel_anonymous_datasets():
    table_ref = bigquery.TableReference.from_string(
        "my-test-project._e8166e0cdb.anonbb92cd"
    )

    sql = bf_read_gbq_table._create_time_travel_sql(
        table_ref, datetime.datetime.now(datetime.timezone.utc)
    )

    # Anonymous query results tables don't support time travel.
    assert "SYSTEM_TIME" not in sql

    # Need fully-qualified table name.
    assert "`my-test-project`.`_e8166e0cdb`.`anonbb92cd`" in sql
