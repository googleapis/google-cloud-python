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

from sqlalchemy.testing import config
from sqlalchemy.testing import eq_
from sqlalchemy.testing import provide_metadata
from sqlalchemy.testing.schema import Column
from sqlalchemy.testing.schema import Table
from sqlalchemy import literal_column
from sqlalchemy import select, case, bindparam
from sqlalchemy import exists
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.testing import requires
from sqlalchemy.types import Integer
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from sqlalchemy.testing.suite.test_ddl import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_cte import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_dialect import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_update_delete import *  # noqa: F401, F403

from sqlalchemy.testing.suite.test_cte import CTETest as _CTETest
from sqlalchemy.testing.suite.test_ddl import TableDDLTest as _TableDDLTest
from sqlalchemy.testing.suite.test_ddl import (
    LongNameBlowoutTest as _LongNameBlowoutTest,
)

from sqlalchemy.testing.suite.test_dialect import EscapingTest as _EscapingTest
from sqlalchemy.testing.suite.test_select import ExistsTest as _ExistsTest
from sqlalchemy.testing.suite.test_types import BooleanTest as _BooleanTest

config.test_schema = ""


from sqlalchemy.testing.suite.test_types import (  # noqa: F401, F403
    DateTest as _DateTest,
    DateTimeHistoricTest,
    DateTimeCoercedToDateTimeTest as _DateTimeCoercedToDateTimeTest,
    DateTimeMicrosecondsTest as _DateTimeMicrosecondsTest,
    DateTimeTest as _DateTimeTest,
    TimeTest as _TimeTest,
    TimeMicrosecondsTest as _TimeMicrosecondsTest,
    TimestampMicrosecondsTest,
)


class EscapingTest(_EscapingTest):
    @provide_metadata
    def test_percent_sign_round_trip(self):
        """Test that the DBAPI accommodates for escaped / nonescaped
        percent signs in a way that matches the compiler

        SPANNER OVERRIDE
        Cloud Spanner supports tables with empty primary key, but
        only single one row can be inserted into such a table -
        following insertions will fail with `Row [] already exists".
        Overriding the test to avoid the same failure.
        """
        m = self.metadata
        t = Table("t", m, Column("data", String(50)))
        t.create(config.db)
        with config.db.begin() as conn:
            conn.execute(t.insert(), dict(data="some % value"))

            eq_(
                conn.scalar(
                    select([t.c.data]).where(
                        t.c.data == literal_column("'some % value'")
                    )
                ),
                "some % value",
            )

            conn.execute(t.delete())
            conn.execute(t.insert(), dict(data="some %% other value"))
            eq_(
                conn.scalar(
                    select([t.c.data]).where(
                        t.c.data == literal_column("'some %% other value'")
                    )
                ),
                "some %% other value",
            )


class CTETest(_CTETest):
    @pytest.mark.skip("INSERT from WITH subquery is not supported")
    def test_insert_from_select_round_trip(self):
        """
        The test checks if an INSERT can be done from a cte, like:

        WITH some_cte AS (...)
        INSERT INTO some_other_table (... SELECT * FROM some_cte)

        Such queries are not supported by Spanner.
        """
        pass

    @pytest.mark.skip("DELETE from WITH subquery is not supported")
    def test_delete_scalar_subq_round_trip(self):
        """
        The test checks if a DELETE can be done from a cte, like:

        WITH some_cte AS (...)
        DELETE FROM some_other_table (... SELECT * FROM some_cte)

        Such queries are not supported by Spanner.
        """
        pass

    @pytest.mark.skip("DELETE from WITH subquery is not supported")
    def test_delete_from_round_trip(self):
        """
        The test checks if a DELETE can be done from a cte, like:

        WITH some_cte AS (...)
        DELETE FROM some_other_table (... SELECT * FROM some_cte)

        Such queries are not supported by Spanner.
        """
        pass

    @pytest.mark.skip("UPDATE from WITH subquery is not supported")
    def test_update_from_round_trip(self):
        """
        The test checks if an UPDATE can be done from a cte, like:

        WITH some_cte AS (...)
        UPDATE some_other_table
        SET (... SELECT * FROM some_cte)

        Such queries are not supported by Spanner.
        """
        pass

    @pytest.mark.skip("WITH RECURSIVE subqueries are not supported")
    def test_select_recursive_round_trip(self):
        pass


class BooleanTest(_BooleanTest):
    def test_render_literal_bool(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but
        only a single row can be inserted into such a table -
        following insertions will fail with `Row [] already exists".
        Overriding the test to avoid the same failure.
        """
        self._literal_round_trip(Boolean(), [True], [True])
        self._literal_round_trip(Boolean(), [False], [False])


class ExistsTest(_ExistsTest):
    def test_select_exists(self, connection):
        """
        SPANNER OVERRIDE:

        The original test is trying to execute a query like:

        SELECT ...
        WHERE EXISTS (SELECT ...)

        SELECT WHERE without FROM clause is not supported by Spanner.
        Rewriting the test to force it to generate a query like:

        SELECT EXISTS (SELECT ...)
        """
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select((exists().where(stuff.c.data == "some data"),))
            ).fetchall(),
            [(True,)],
        )

    def test_select_exists_false(self, connection):
        """
        SPANNER OVERRIDE:

        The original test is trying to execute a query like:

        SELECT ...
        WHERE EXISTS (SELECT ...)

        SELECT WHERE without FROM clause is not supported by Spanner.
        Rewriting the test to force it to generate a query like:

        SELECT EXISTS (SELECT ...)
        """
        stuff = self.tables.stuff
        eq_(
            connection.execute(
                select((exists().where(stuff.c.data == "no data"),))
            ).fetchall(),
            [(False,)],
        )


class TableDDLTest(_TableDDLTest):
    @pytest.mark.skip(
        "Spanner table name must start with an uppercase or lowercase letter"
    )
    def test_underscore_names(self):
        pass


@pytest.mark.skip("Max identifier length in Spanner is 128")
class LongNameBlowoutTest(_LongNameBlowoutTest):
    pass


class DateTest(_DateTest):
    def test_round_trip(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table date_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """
        date_table = self.tables.date_table

        config.db.execute(date_table.insert(), {"id": 1, "date_data": self.data})

        row = config.db.execute(select([date_table.c.date_data])).first()

        compare = self.compare or self.data
        eq_(row, (compare,))
        assert isinstance(row[0], type(compare))

    def test_null(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table date_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """
        date_table = self.tables.date_table

        config.db.execute(date_table.insert(), {"id": 1, "date_data": None})

        row = config.db.execute(select([date_table.c.date_data])).first()
        eq_(row, (None,))

    @requires.standalone_null_binds_whereclause
    def test_null_bound_comparison(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table date_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """

        # this test is based on an Oracle issue observed in #4886.
        # passing NULL for an expression that needs to be interpreted as
        # a certain type, does the DBAPI have the info it needs to do this.
        date_table = self.tables.date_table
        with config.db.connect() as conn:
            result = conn.execute(
                date_table.insert(), {"id": 1, "date_data": self.data}
            )
            id_ = result.inserted_primary_key[0]
            stmt = select([date_table.c.id]).where(
                case(
                    [
                        (
                            bindparam("foo", type_=self.datatype)
                            != None,  # noqa: E711,
                            bindparam("foo", type_=self.datatype),
                        )
                    ],
                    else_=date_table.c.date_data,
                )
                == date_table.c.date_data
            )

            row = conn.execute(stmt, {"foo": None}).first()
            eq_(row[0], id_)


class DateTimeMicrosecondsTest(_DateTimeMicrosecondsTest):
    @classmethod
    def define_tables(cls, metadata):
        """
        SPANNER OVERRIDE:

        Spanner is not able cleanup data and drop the table correctly,
        table already exists after related tests finished, so it doesn't
        create a new table and insertions for tests for other data types
        will fail with `400 Invalid value for column date_data in
        table date_table: Expected DATE`.
        Overriding the tests to create a new table for tests to avoid the same
        failures.
        """
        Table(
            "datetime_table",
            metadata,
            Column("id", Integer, primary_key=True, test_needs_autoincrement=True),
            Column("date_data", cls.datatype),
        )

    def test_null(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table datetime_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """
        date_table = self.tables.datetime_table

        config.db.execute(date_table.insert(), {"id": 1, "date_data": None})

        row = config.db.execute(select([date_table.c.date_data])).first()
        eq_(row, (None,))

    def test_round_trip(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table datetime_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.

        Spanner converts timestamp into `%Y-%m-%dT%H:%M:%S.%fZ` format, so to avoid
        assert failures convert datetime input to the desire timestamp format.
        """
        date_table = self.tables.datetime_table
        config.db.execute(date_table.insert(), {"id": 1, "date_data": self.data})

        row = config.db.execute(select([date_table.c.date_data])).first()
        compare = self.compare or self.data
        compare = compare.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        eq_(row[0].rfc3339(), compare)
        assert isinstance(row[0], DatetimeWithNanoseconds)

    @requires.standalone_null_binds_whereclause
    def test_null_bound_comparison(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table datetime_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """
        # this test is based on an Oracle issue observed in #4886.
        # passing NULL for an expression that needs to be interpreted as
        # a certain type, does the DBAPI have the info it needs to do this.
        date_table = self.tables.datetime_table
        with config.db.connect() as conn:
            result = conn.execute(
                date_table.insert(), {"id": 1, "date_data": self.data}
            )
            id_ = result.inserted_primary_key[0]
            stmt = select([date_table.c.id]).where(
                case(
                    [
                        (
                            bindparam("foo", type_=self.datatype)
                            != None,  # noqa: E711,
                            bindparam("foo", type_=self.datatype),
                        )
                    ],
                    else_=date_table.c.date_data,
                )
                == date_table.c.date_data
            )

            row = conn.execute(stmt, {"foo": None}).first()
            eq_(row[0], id_)


class DateTimeTest(_DateTimeTest, DateTimeMicrosecondsTest):
    """
    SPANNER OVERRIDE:

    DateTimeTest tests have the same failures same as DateTimeMicrosecondsTest tests,
    so to avoid those failures and maintain DRY concept just inherit the class to run
    tests successfully.
    """

    pass


@pytest.mark.skip("Spanner doesn't support Time data type.")
class TimeTests(_TimeMicrosecondsTest, _TimeTest):
    pass


@pytest.mark.skip("Spanner doesn't coerce dates from datetime.")
class DateTimeCoercedToDateTimeTest(_DateTimeCoercedToDateTimeTest):
    pass
