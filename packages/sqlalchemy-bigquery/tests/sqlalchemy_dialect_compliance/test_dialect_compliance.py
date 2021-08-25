# Copyright (c) 2021 The sqlalchemy-bigquery Authors
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
import packaging.version
import pytest
import pytz
import sqlalchemy
from sqlalchemy import and_

import sqlalchemy.testing.suite.test_types
from sqlalchemy.testing import util
from sqlalchemy.testing.assertions import eq_
from sqlalchemy.testing.suite import config, select, exists
from sqlalchemy.testing.suite import *  # noqa
from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
    CTETest as _CTETest,
    ExistsTest as _ExistsTest,
    InsertBehaviorTest as _InsertBehaviorTest,
    LongNameBlowoutTest,
    QuotedNameArgumentTest,
    SimpleUpdateDeleteTest as _SimpleUpdateDeleteTest,
    TimestampMicrosecondsTest as _TimestampMicrosecondsTest,
)


if packaging.version.parse(sqlalchemy.__version__) < packaging.version.parse("1.4"):
    from sqlalchemy.testing.suite import LimitOffsetTest as _LimitOffsetTest

    class LimitOffsetTest(_LimitOffsetTest):
        @pytest.mark.skip("BigQuery doesn't allow an offset without a limit.")
        def test_simple_offset(self):
            pass

        test_bound_offset = test_simple_offset

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


else:
    from sqlalchemy.testing.suite import (
        FetchLimitOffsetTest as _FetchLimitOffsetTest,
        RowCountTest as _RowCountTest,
    )

    class FetchLimitOffsetTest(_FetchLimitOffsetTest):
        @pytest.mark.skip("BigQuery doesn't allow an offset without a limit.")
        def test_simple_offset(self):
            pass

        test_bound_offset = test_simple_offset
        test_expr_offset = test_simple_offset_zero = test_simple_offset

        # The original test is missing an order by.

        # Also, note that sqlalchemy union is a union distinct, not a
        # union all. This test caught that were were getting that wrong.
        def test_limit_render_multiple_times(self, connection):
            table = self.tables.some_table
            stmt = select(table.c.id).order_by(table.c.id).limit(1).scalar_subquery()

            u = sqlalchemy.union(select(stmt), select(stmt)).subquery().select()

            self._assert_result(
                connection, u, [(1,)],
            )

    del DifficultParametersTest  # exercises column names illegal in BQ
    del DistinctOnTest  # expects unquoted table names.
    del HasIndexTest  # BQ doesn't do the indexes that SQLA is loooking for.
    del IdentityAutoincrementTest  # BQ doesn't do autoincrement

    # This test makes makes assertions about generated sql and trips
    # over the backquotes that we add everywhere. XXX Why do we do that?
    del PostCompileParamsTest

    class TimestampMicrosecondsTest(_TimestampMicrosecondsTest):

        data = datetime.datetime(2012, 10, 15, 12, 57, 18, 396, tzinfo=pytz.UTC)

        def test_literal(self, literal_round_trip):
            # The base tests doesn't set up the literal properly, because
            # it doesn't pass its datatype to `literal`.

            def literal(value, type_=None):
                assert value == self.data
                if type_ is not None:
                    assert type_ is self.datatype

                import sqlalchemy.sql.sqltypes

                return sqlalchemy.sql.elements.literal(value, self.datatype)

            with mock.patch("sqlalchemy.testing.suite.test_types.literal", literal):
                super(TimestampMicrosecondsTest, self).test_literal(literal_round_trip)

    def test_round_trip_executemany(self, connection):
        unicode_table = self.tables.unicode_table
        connection.execute(
            unicode_table.insert(),
            [{"id": i, "unicode_data": self.data} for i in range(3)],
        )

        rows = connection.execute(select(unicode_table.c.unicode_data)).fetchall()
        eq_(rows, [(self.data,) for i in range(3)])
        for row in rows:
            assert isinstance(row[0], util.text_type)

    sqlalchemy.testing.suite.test_types._UnicodeFixture.test_round_trip_executemany = (
        test_round_trip_executemany
    )

    class RowCountTest(_RowCountTest):
        @classmethod
        def insert_data(cls, connection):
            cls.data = data = [
                ("Angela", "A"),
                ("Andrew", "A"),
                ("Anand", "A"),
                ("Bob", "B"),
                ("Bobette", "B"),
                ("Buffy", "B"),
                ("Charlie", "C"),
                ("Cynthia", "C"),
                ("Chris", "C"),
            ]

            employees_table = cls.tables.employees
            connection.execute(
                employees_table.insert(),
                [
                    {"employee_id": i, "name": n, "department": d}
                    for i, (n, d) in enumerate(data)
                ],
            )


# Quotes aren't allowed in BigQuery table names.
del QuotedNameArgumentTest


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.skip(
        "BQ has no autoinc and client-side defaults can't work for select."
    )
    def test_insert_from_select_autoinc(cls):
        pass


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

    @pytest.mark.skip("BQ doesn't have indexes (in the way these tests expect).")
    def test_get_indexes(self):
        pass
