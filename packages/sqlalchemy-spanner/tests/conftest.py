# -*- coding: utf-8 -*-
#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import uuid
from contextlib import contextmanager
from unittest.mock import MagicMock

import google.cloud.spanner_v1._opentelemetry_tracing as spanner_tracing
import pytest
from sqlalchemy.dialects import registry
from sqlalchemy.sql.elements import literal
from sqlalchemy.testing.schema import Column, Table


# Aggressively monkeypatch trace_call to avoid OpenTelemetry usage entirely.
# This prevents warnings from OpenTelemetry, which would otherwise cause the
# conformance tests to fail.
@contextmanager
def no_op_trace_call(*args, **kwargs):
    yield MagicMock()


# Patch the definition module
spanner_tracing.trace_call = no_op_trace_call

# Patch consumers
modules_to_patch = [
    "google.cloud.spanner_v1.snapshot",
    "google.cloud.spanner_v1.transaction",
    "google.cloud.spanner_v1.session",
    "google.cloud.spanner_v1.database",
]
for module_name in modules_to_patch:
    try:
        module = importlib.import_module(module_name)
        module.trace_call = no_op_trace_call
    except ImportError:
        pass

registry.register("spanner", "google.cloud.sqlalchemy_spanner", "SpannerDialect")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *  # noqa: E402, F401, F403


def _commit_ddl(connection):
    """Flush and commit buffered DDL in Spanner DBAPI or underlying connections."""
    # TODO: modern sqlalchemy uses dbapi_connection, remove the getattr check
    # for "connection" once we drop support for sqlalchemy < 2.0
    dbapi_conn = getattr(
        connection, "dbapi_connection", getattr(connection, "connection", connection)
    )
    commit_fn = getattr(dbapi_conn, "commit", None)
    if callable(commit_fn):
        commit_fn()


def _rollback_txn(connection):
    """Roll back any active Spanner transaction to release schema and row locks."""
    # TODO: modern sqlalchemy uses dbapi_connection, remove the getattr check
    # for "connection" once we drop support for sqlalchemy < 2.0
    dbapi_conn = getattr(
        connection, "dbapi_connection", getattr(connection, "connection", connection)
    )
    rollback_fn = getattr(dbapi_conn, "rollback", None)
    if callable(rollback_fn):
        rollback_fn()


@pytest.fixture
def literal_round_trip_spanner(metadata, connection):
    """Test literal SQL rendering in INSERT and SELECT with full table isolation.

    In SQLAlchemy, literal rendering tests verify that Python data types (such as
    Strings with special escape characters, Decimals, or Booleans) are correctly
    rendered directly into raw SQL text (e.g., 'SELECT ... WHERE x = 15.7563')
    without syntax corruption or parameter escaping failures.

    To ensure test isolation in Cloud Spanner, this fixture:
    1. Generates a unique table name per invocation using the column type and
       UUID entropy.
    2. Wraps table creation in the primary try block so table reference cleanup
       in metadata is guaranteed even if creation fails.
    3. Flushes and commits table creation DDL immediately.
    4. Executes the insert and select assertions.
    5. Cleans up any active read-write transactions before attempting DDL drops,
       preventing Spanner's concurrent schema change rejection.
    6. Drops the table and uses a nested finally block to guarantee table eviction
       from metadata even if the drop operation fails.
    """

    def run(
        type_,
        input_,
        output,
        filter_=None,
        compare=None,
        support_whereclause=True,
    ):
        table_name = f"t_lit_{type_.__class__.__name__.lower()}_{uuid.uuid4().hex[:6]}"
        t = Table(table_name, metadata, Column("x", type_))

        try:
            t.create(connection)
            _commit_ddl(connection)

            try:
                for value in input_:
                    ins = t.insert().values(x=literal(value, type_))
                    connection.execute(ins)

                if support_whereclause:
                    if compare:
                        stmt = t.select().where(
                            t.c.x
                            == literal(
                                compare,
                                type_,
                            ),
                            t.c.x
                            == literal(
                                input_[0],
                                type_,
                            ),
                        )
                    else:
                        stmt = t.select().where(
                            t.c.x
                            == literal(
                                compare if compare is not None else input_[0],
                                type_,
                            )
                        )
                else:
                    stmt = t.select()

                rows = connection.execute(stmt).all()
                assert rows, "No rows returned"
                for row in rows:
                    value = row[0]
                    if filter_ is not None:
                        value = filter_(value)
                    assert value in output
            finally:
                _rollback_txn(connection)
        finally:
            try:
                t.drop(connection, checkfirst=True)
                _commit_ddl(connection)
            except Exception:
                pass
            finally:
                metadata.remove(t)

    return run
