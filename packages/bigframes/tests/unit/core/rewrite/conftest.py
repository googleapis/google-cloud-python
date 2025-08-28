# Copyright 2025 Google LLC
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
import unittest.mock as mock

import google.cloud.bigquery
import pytest

import bigframes.core as core
import bigframes.core.schema

TABLE_REF = google.cloud.bigquery.TableReference.from_string("project.dataset.table")
SCHEMA = (
    google.cloud.bigquery.SchemaField("col_a", "INTEGER"),
    google.cloud.bigquery.SchemaField("col_b", "INTEGER"),
)
TABLE = google.cloud.bigquery.Table(
    table_ref=TABLE_REF,
    schema=SCHEMA,
)
FAKE_SESSION = mock.create_autospec(bigframes.Session, instance=True)
type(FAKE_SESSION)._strictly_ordered = mock.PropertyMock(return_value=True)


@pytest.fixture
def table():
    return TABLE


@pytest.fixture
def fake_session():
    return FAKE_SESSION


@pytest.fixture
def leaf(fake_session, table):
    return core.ArrayValue.from_table(
        session=fake_session,
        table=table,
        schema=bigframes.core.schema.ArraySchema.from_bq_table(table),
    ).node
