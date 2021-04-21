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

import operator
import pytest
import pytz

import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy import testing
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy.schema import DDL
from sqlalchemy.testing import config
from sqlalchemy.testing import db
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures
from sqlalchemy.testing import provide_metadata
from sqlalchemy.testing.provision import temp_table_keyword_args
from sqlalchemy.testing.schema import Column
from sqlalchemy.testing.schema import Table
from sqlalchemy import bindparam
from sqlalchemy import case
from sqlalchemy import literal
from sqlalchemy import literal_column
from sqlalchemy import select
from sqlalchemy import util
from sqlalchemy import event
from sqlalchemy import exists
from sqlalchemy import LargeBinary
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.types import Integer
from sqlalchemy.types import Numeric
from sqlalchemy.testing import requires

from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from google.cloud import spanner_dbapi

from sqlalchemy.testing.suite.test_cte import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_ddl import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_dialect import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_insert import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_results import *  # noqa: F401, F403
from sqlalchemy.testing.suite.test_update_delete import *  # noqa: F401, F403

from sqlalchemy.testing.suite.test_cte import CTETest as _CTETest
from sqlalchemy.testing.suite.test_ddl import TableDDLTest as _TableDDLTest
from sqlalchemy.testing.suite.test_ddl import (
    LongNameBlowoutTest as _LongNameBlowoutTest,
)
from sqlalchemy.testing.suite.test_dialect import EscapingTest as _EscapingTest
from sqlalchemy.testing.suite.test_insert import (
    InsertBehaviorTest as _InsertBehaviorTest,
)
from sqlalchemy.testing.suite.test_reflection import (
    ComponentReflectionTest as _ComponentReflectionTest,
)
from sqlalchemy.testing.suite.test_reflection import (
    QuotedNameArgumentTest as _QuotedNameArgumentTest,
)
from sqlalchemy.testing.suite.test_results import RowFetchTest as _RowFetchTest
from sqlalchemy.testing.suite.test_select import ExistsTest as _ExistsTest
from sqlalchemy.testing.suite.test_select import (
    IsOrIsNotDistinctFromTest as _IsOrIsNotDistinctFromTest,
)
from sqlalchemy.testing.suite.test_types import BooleanTest as _BooleanTest
from sqlalchemy.testing.suite.test_types import IntegerTest as _IntegerTest
from sqlalchemy.testing.suite.test_types import _LiteralRoundTripFixture

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

from sqlalchemy.testing.suite.test_sequence import (
    SequenceCompilerTest as _SequenceCompilerTest,
    HasSequenceTest as _HasSequenceTest,
    SequenceTest as _SequenceTest,
)

config.test_schema = ""


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
    @classmethod
    def define_tables(cls, metadata):
        """
        The original method creates a foreign key without a name,
        which causes troubles on test cleanup. Overriding the
        method to explicitly set a foreign key name.
        """
        Table(
            "some_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
            Column("parent_id", ForeignKey("some_table.id", name="fk_some_table")),
        )

        Table(
            "some_other_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("data", String(50)),
            Column("parent_id", Integer),
        )

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
    def test_null(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail
        with `400 id must not be NULL in table datetime_table`.
        Overriding the tests to add a manual primary key value to avoid the same
        failures.
        """
        date_table = self.tables.date_table

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
        date_table = self.tables.date_table
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


class IntegerTest(_IntegerTest):
    @provide_metadata
    def _round_trip(self, datatype, data):
        """
        SPANNER OVERRIDE:

        This is the helper method for integer class tests which creates a table and
        performs an insert operation.
        Cloud Spanner supports tables with an empty primary key, but only one
        row can be inserted into such a table - following insertions will fail with
        `400 id must not be NULL in table date_table`.
        Overriding the tests and adding a manual primary key value to avoid the same
        failures.
        """
        metadata = self.metadata
        int_table = Table(
            "integer_table",
            metadata,
            Column("id", Integer, primary_key=True, test_needs_autoincrement=True),
            Column("integer_data", datatype),
        )

        metadata.create_all(config.db)

        config.db.execute(int_table.insert(), {"id": 1, "integer_data": data})

        row = config.db.execute(select([int_table.c.integer_data])).first()

        eq_(row, (data,))

        if util.py3k:
            assert isinstance(row[0], int)
        else:
            assert isinstance(row[0], (long, int))  # noqa

    @provide_metadata
    def _literal_round_trip(self, type_, input_, output, filter_=None):
        """
        SPANNER OVERRIDE:

        Spanner DBAPI does not execute DDL statements unless followed by a
        non DDL statement, which is preventing correct table clean up.
        The table already exists after related tests finish, so it doesn't
        create a new table and when running tests for other data types
        insertions will fail with `400 Duplicate name in schema: t`.
        Overriding the tests to create and drop a new table to prevent
        database existence errors.
        """

        # for literal, we test the literal render in an INSERT
        # into a typed column.  we can then SELECT it back as its
        # official type; ideally we'd be able to use CAST here
        # but MySQL in particular can't CAST fully
        t = Table("int_t", self.metadata, Column("x", type_))
        t.create()

        with db.connect() as conn:
            for value in input_:
                ins = (
                    t.insert()
                    .values(x=literal(value))
                    .compile(
                        dialect=db.dialect, compile_kwargs=dict(literal_binds=True),
                    )
                )
                conn.execute(ins)
                conn.execute("SELECT 1")

            if self.supports_whereclause:
                stmt = t.select().where(t.c.x == literal(value))
            else:
                stmt = t.select()

            stmt = stmt.compile(
                dialect=db.dialect, compile_kwargs=dict(literal_binds=True),
            )
            for row in conn.execute(stmt):
                value = row[0]
                if filter_ is not None:
                    value = filter_(value)
                assert value in output


@pytest.mark.skip("Spanner doesn't support CREATE SEQUENCE.")
class SequenceCompilerTest(_SequenceCompilerTest):
    pass


@pytest.mark.skip("Spanner doesn't support CREATE SEQUENCE.")
class HasSequenceTest(_HasSequenceTest):
    pass


@pytest.mark.skip("Spanner doesn't support CREATE SEQUENCE.")
class SequenceTest(_SequenceTest):
    pass


@pytest.mark.skip("Spanner doesn't support quotes in table names.")
class QuotedNameArgumentTest(_QuotedNameArgumentTest):
    pass


class ComponentReflectionTest(_ComponentReflectionTest):
    @classmethod
    def define_temp_tables(cls, metadata):
        """
        SPANNER OVERRIDE:

        In Cloud Spanner unique indexes are used instead of directly
        creating unique constraints. Overriding the test to replace
        constraints with indexes in testing data.
        """
        kw = temp_table_keyword_args(config, config.db)
        user_tmp = Table(
            "user_tmp",
            metadata,
            Column("id", sqlalchemy.INT, primary_key=True),
            Column("name", sqlalchemy.VARCHAR(50)),
            Column("foo", sqlalchemy.INT),
            sqlalchemy.Index("user_tmp_uq", "name", unique=True),
            sqlalchemy.Index("user_tmp_ix", "foo"),
            **kw
        )
        if (
            testing.requires.view_reflection.enabled
            and testing.requires.temporary_views.enabled
        ):
            event.listen(
                user_tmp,
                "after_create",
                DDL("create temporary view user_tmp_v as " "select * from user_tmp"),
            )
            event.listen(user_tmp, "before_drop", DDL("drop view user_tmp_v"))

    @testing.provide_metadata
    def _test_get_unique_constraints(self, schema=None):
        """
        SPANNER OVERRIDE:

        In Cloud Spanner unique indexes are used instead of directly
        creating unique constraints. Overriding the test to replace
        constraints with indexes in testing data.
        """
        # SQLite dialect needs to parse the names of the constraints
        # separately from what it gets from PRAGMA index_list(), and
        # then matches them up.  so same set of column_names in two
        # constraints will confuse it.    Perhaps we should no longer
        # bother with index_list() here since we have the whole
        # CREATE TABLE?
        uniques = sorted(
            [
                {"name": "unique_a", "column_names": ["a"]},
                {"name": "unique_a_b_c", "column_names": ["a", "b", "c"]},
                {"name": "unique_c_a_b", "column_names": ["c", "a", "b"]},
                {"name": "unique_asc_key", "column_names": ["asc", "key"]},
                {"name": "i.have.dots", "column_names": ["b"]},
                {"name": "i have spaces", "column_names": ["c"]},
            ],
            key=operator.itemgetter("name"),
        )
        orig_meta = self.metadata
        table = Table(
            "testtbl",
            orig_meta,
            Column("a", sqlalchemy.String(20)),
            Column("b", sqlalchemy.String(30)),
            Column("c", sqlalchemy.Integer),
            # reserved identifiers
            Column("asc", sqlalchemy.String(30)),
            Column("key", sqlalchemy.String(30)),
            schema=schema,
        )
        for uc in uniques:
            table.append_constraint(
                sqlalchemy.Index(uc["name"], *uc["column_names"], unique=True)
            )
        orig_meta.create_all()

        inspector = inspect(orig_meta.bind)
        reflected = sorted(
            inspector.get_unique_constraints("testtbl", schema=schema),
            key=operator.itemgetter("name"),
        )

        names_that_duplicate_index = set()

        for orig, refl in zip(uniques, reflected):
            # Different dialects handle duplicate index and constraints
            # differently, so ignore this flag
            dupe = refl.pop("duplicates_index", None)
            if dupe:
                names_that_duplicate_index.add(dupe)
            eq_(orig, refl)

        reflected_metadata = MetaData()
        reflected = Table(
            "testtbl", reflected_metadata, autoload_with=orig_meta.bind, schema=schema,
        )

        # test "deduplicates for index" logic.   MySQL and Oracle
        # "unique constraints" are actually unique indexes (with possible
        # exception of a unique that is a dupe of another one in the case
        # of Oracle).  make sure # they aren't duplicated.
        idx_names = set([idx.name for idx in reflected.indexes])
        uq_names = set(
            [
                uq.name
                for uq in reflected.constraints
                if isinstance(uq, sqlalchemy.UniqueConstraint)
            ]
        ).difference(["unique_c_a_b"])

        assert not idx_names.intersection(uq_names)
        if names_that_duplicate_index:
            eq_(names_that_duplicate_index, idx_names)
            eq_(uq_names, set())

    @testing.provide_metadata
    def test_unique_constraint_raises(self):
        """
        Checking that unique constraint creation
        fails due to a ProgrammingError.
        """
        Table(
            "user_tmp_failure",
            self.metadata,
            Column("id", sqlalchemy.INT, primary_key=True),
            Column("name", sqlalchemy.VARCHAR(50)),
            sqlalchemy.UniqueConstraint("name", name="user_tmp_uq"),
        )

        with pytest.raises(spanner_dbapi.exceptions.ProgrammingError):
            self.metadata.create_all()

    @testing.provide_metadata
    def _test_get_table_names(self, schema=None, table_type="table", order_by=None):
        """
        SPANNER OVERRIDE:

        Spanner doesn't support temporary tables, so real tables are
        used for testing. As the original test expects only real
        tables to be read, and in Spanner all the tables are real,
        expected results override is required.
        """
        _ignore_tables = [
            "comment_test",
            "noncol_idx_test_pk",
            "noncol_idx_test_nopk",
            "local_table",
            "remote_table",
            "remote_table_2",
        ]
        meta = self.metadata

        insp = inspect(meta.bind)

        if table_type == "view":
            table_names = insp.get_view_names(schema)
            table_names.sort()
            answer = ["email_addresses_v", "users_v"]
            eq_(sorted(table_names), answer)
        else:
            if order_by:
                tables = [
                    rec[0]
                    for rec in insp.get_sorted_table_and_fkc_names(schema)
                    if rec[0]
                ]
            else:
                tables = insp.get_table_names(schema)
            table_names = [t for t in tables if t not in _ignore_tables]

            if order_by == "foreign_key":
                answer = ["users", "user_tmp", "email_addresses", "dingalings"]
                eq_(table_names, answer)
            else:
                answer = ["dingalings", "email_addresses", "user_tmp", "users"]
                eq_(sorted(table_names), answer)

    @pytest.mark.skip("Spanner doesn't support temporary tables")
    def test_get_temp_table_indexes(self):
        pass

    @pytest.mark.skip("Spanner doesn't support temporary tables")
    def test_get_temp_table_unique_constraints(self):
        pass

    @testing.requires.table_reflection
    def test_numeric_reflection(self):
        """
        SPANNER OVERRIDE:

        Spanner defines NUMERIC type with the constant precision=38
        and scale=9. Overriding the test to check if the NUMERIC
        column is successfully created and has dimensions
        correct for Cloud Spanner.
        """
        for typ in self._type_round_trip(Numeric(18, 5)):
            assert isinstance(typ, Numeric)
            eq_(typ.precision, 38)
            eq_(typ.scale, 9)


class RowFetchTest(_RowFetchTest):
    def test_row_w_scalar_select(self):
        """
        SPANNER OVERRIDE:

        Cloud Spanner returns a DatetimeWithNanoseconds() for date
        data types. Overriding the test to use a DatetimeWithNanoseconds
        type value as an expected result.
        --------------

        test that a scalar select as a column is returned as such
        and that type conversion works OK.

        (this is half a SQLAlchemy Core test and half to catch database
        backends that may have unusual behavior with scalar selects.)
        """
        datetable = self.tables.has_dates
        s = select([datetable.alias("x").c.today]).as_scalar()
        s2 = select([datetable.c.id, s.label("somelabel")])
        row = config.db.execute(s2).first()

        eq_(
            row["somelabel"],
            DatetimeWithNanoseconds(2006, 5, 12, 12, 0, 0, tzinfo=pytz.UTC),
        )


class InsertBehaviorTest(_InsertBehaviorTest):
    @pytest.mark.skip("Spanner doesn't support empty inserts")
    def test_empty_insert(self):
        pass

    @pytest.mark.skip("Spanner doesn't support auto increment")
    def test_insert_from_select_autoinc(self):
        pass

    @pytest.mark.skip("Spanner doesn't support auto increment")
    def test_insert_from_select_autoinc_no_rows(self):
        pass

    @pytest.mark.skip("Spanner doesn't support default column values")
    def test_insert_from_select_with_defaults(self):
        pass


@pytest.mark.skip("Spanner doesn't support IS DISTINCT FROM clause")
class IsOrIsNotDistinctFromTest(_IsOrIsNotDistinctFromTest):
    pass


class BytesTest(_LiteralRoundTripFixture, fixtures.TestBase):
    __backend__ = True

    def test_nolength_binary(self):
        metadata = MetaData()
        foo = Table("foo", metadata, Column("one", LargeBinary))

        foo.create(config.db)
        foo.drop(config.db)
