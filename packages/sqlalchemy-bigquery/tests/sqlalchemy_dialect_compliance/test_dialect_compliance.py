# Copyright (c) 2021 The PyBigQuery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import mock
import pytest
import pytz
from sqlalchemy import and_
from sqlalchemy.testing.assertions import eq_
from sqlalchemy.testing.suite import config, select, exists
from sqlalchemy.testing.suite import *  # noqa
from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
    CTETest as _CTETest,
    ExistsTest as _ExistsTest,
    InsertBehaviorTest as _InsertBehaviorTest,
    LimitOffsetTest as _LimitOffsetTest,
    LongNameBlowoutTest,
    QuotedNameArgumentTest,
    SimpleUpdateDeleteTest as _SimpleUpdateDeleteTest,
    TimestampMicrosecondsTest as _TimestampMicrosecondsTest,
)

# Quotes aren't allowed in BigQuery table names.
del QuotedNameArgumentTest


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.skip()
    def test_insert_from_select_autoinc(cls):
        """BQ has no autoinc and client-side defaults can't work for select."""


class ExistsTest(_ExistsTest):
    """
    Override

    Becaise Bigquery requires FROM when there's a WHERE and
    the base tests didn't do provide a FROM.
    """

    def test_select_exists(self, connection):
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select([stuff.c.id]).where(
                    and_(stuff.c.id == 1, exists().where(stuff.c.data == "some data"),)
                )
            ).fetchall(),
            [(1,)],
        )

    def test_select_exists_false(self, connection):
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select([stuff.c.id]).where(exists().where(stuff.c.data == "no data"))
            ).fetchall(),
            [],
        )


class LimitOffsetTest(_LimitOffsetTest):
    @pytest.mark.skip()
    def test_simple_offset(self):
        """BigQuery doesn't allow an offset without a limit."""

    test_bound_offset = test_simple_offset


# This test requires features (indexes, primary keys, etc., that BigQuery doesn't have.
del LongNameBlowoutTest


class SimpleUpdateDeleteTest(_SimpleUpdateDeleteTest):
    """The base tests fail if operations return rows for some reason."""

    def test_update(self):
        t = self.tables.plain_pk
        r = config.db.execute(t.update().where(t.c.id == 2), data="d2_new")
        assert not r.is_insert
        # assert not r.returns_rows

        eq_(
            config.db.execute(t.select().order_by(t.c.id)).fetchall(),
            [(1, "d1"), (2, "d2_new"), (3, "d3")],
        )

    def test_delete(self):
        t = self.tables.plain_pk
        r = config.db.execute(t.delete().where(t.c.id == 2))
        assert not r.is_insert
        # assert not r.returns_rows
        eq_(
            config.db.execute(t.select().order_by(t.c.id)).fetchall(),
            [(1, "d1"), (3, "d3")],
        )


class CTETest(_CTETest):
    @pytest.mark.skip("Can't use CTEs with insert")
    def test_insert_from_select_round_trip(self):
        pass

    @pytest.mark.skip("Recusive CTEs aren't supported.")
    def test_select_recursive_round_trip(self):
        pass


class ComponentReflectionTest(_ComponentReflectionTest):
    @pytest.mark.skip("Big query types don't track precision, length, etc.")
    def course_grained_types():
        pass

    test_numeric_reflection = test_varchar_reflection = course_grained_types


class TimestampMicrosecondsTest(_TimestampMicrosecondsTest):

    data = datetime.datetime(2012, 10, 15, 12, 57, 18, 396, tzinfo=pytz.UTC)

    def test_literal(self):
        # The base tests doesn't set up the literal properly, because
        # it doesn't pass its datatype to `literal`.

        def literal(value):
            assert value == self.data
            import sqlalchemy.sql.sqltypes

            return sqlalchemy.sql.elements.literal(value, self.datatype)

        with mock.patch("sqlalchemy.testing.suite.test_types.literal", literal):
            super(TimestampMicrosecondsTest, self).test_literal()
