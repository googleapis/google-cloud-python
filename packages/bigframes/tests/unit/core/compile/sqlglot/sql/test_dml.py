# Copyright 2026 Google LLC
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

import bigframes_vendored.sqlglot.expressions as sge
from google.cloud import bigquery
import pytest

from bigframes.core.compile.sqlglot.sql import base, dml

pytest.importorskip("pytest_snapshot")


def test_insert_from_select(snapshot):
    query = sge.select("*").from_(
        sge.Table(this=sge.Identifier(this="source_table", quoted=True))
    )
    destination = bigquery.TableReference.from_string(
        "bigframes-dev.sqlglot_test.dest_table"
    )

    expr = dml.insert(query, destination)
    sql = base.to_sql(expr)

    snapshot.assert_match(sql, "out.sql")


def test_insert_from_table(snapshot):
    query = sge.Table(this=sge.Identifier(this="source_table", quoted=True))
    destination = bigquery.TableReference.from_string(
        "bigframes-dev.sqlglot_test.dest_table"
    )

    expr = dml.insert(query, destination)
    sql = base.to_sql(expr)

    snapshot.assert_match(sql, "out.sql")


def test_replace_from_select(snapshot):
    query = sge.select("*").from_(
        sge.Table(this=sge.Identifier(this="source_table", quoted=True))
    )
    destination = bigquery.TableReference.from_string(
        "bigframes-dev.sqlglot_test.dest_table"
    )

    expr = dml.replace(query, destination)
    sql = base.to_sql(expr)

    snapshot.assert_match(sql, "out.sql")


def test_replace_from_table(snapshot):
    query = sge.Table(this=sge.Identifier(this="source_table", quoted=True))
    destination = bigquery.TableReference.from_string(
        "bigframes-dev.sqlglot_test.dest_table"
    )

    expr = dml.replace(query, destination)
    sql = base.to_sql(expr)

    snapshot.assert_match(sql, "out.sql")
