# Copyright 2023 Google LLC
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

import google.cloud.bigquery as bigquery

import bigframes.core.io


def test_create_snapshot_sql_doesnt_timetravel_anonymous_datasets():
    table_ref = bigquery.TableReference.from_string(
        "my-test-project._e8166e0cdb.anonbb92cd"
    )

    sql = bigframes.core.io.create_snapshot_sql(
        table_ref, datetime.datetime.now(datetime.timezone.utc)
    )

    # Anonymous query results tables don't support time travel.
    assert "SYSTEM_TIME" not in sql

    # Need fully-qualified table name.
    assert "`my-test-project`.`_e8166e0cdb`.`anonbb92cd`" in sql


def test_create_snapshot_sql_doesnt_timetravel_session_datasets():
    table_ref = bigquery.TableReference.from_string("my-test-project._session.abcdefg")

    sql = bigframes.core.io.create_snapshot_sql(
        table_ref, datetime.datetime.now(datetime.timezone.utc)
    )

    # We aren't modifying _SESSION tables, so don't use time travel.
    assert "SYSTEM_TIME" not in sql

    # Don't need the project ID for _SESSION tables.
    assert "my-test-project" not in sql
