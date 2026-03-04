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

import pytest
from contextlib import contextmanager
import importlib
import google.cloud.spanner_v1._opentelemetry_tracing as spanner_tracing
from unittest.mock import MagicMock
from sqlalchemy.dialects import registry
from sqlalchemy.testing.schema import Column
from sqlalchemy.testing.schema import Table
from sqlalchemy.sql.elements import literal


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


@pytest.fixture
def literal_round_trip_spanner(metadata, connection):
    # for literal, we test the literal render in an INSERT
    # into a typed column.  we can then SELECT it back as its
    # official type;

    def run(
        type_,
        input_,
        output,
        filter_=None,
        compare=None,
        support_whereclause=True,
    ):
        t = Table("t", metadata, Column("x", type_))
        t.create(connection)

        for value in input_:
            ins = t.insert().values(x=literal(value, type_, literal_execute=True))
            connection.execute(ins)

        if support_whereclause:
            if compare:
                stmt = t.select().where(
                    t.c.x
                    == literal(
                        compare,
                        type_,
                        literal_execute=True,
                    ),
                    t.c.x
                    == literal(
                        input_[0],
                        type_,
                        literal_execute=True,
                    ),
                )
            else:
                stmt = t.select().where(
                    t.c.x
                    == literal(
                        compare if compare is not None else input_[0],
                        type_,
                        literal_execute=True,
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

    return run
