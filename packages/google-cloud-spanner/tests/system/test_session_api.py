# Copyright 2021 Google LLC All rights reserved.
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

import collections
import datetime
import decimal
import math
import struct
import threading
import time
import pytest

import grpc
from google.rpc import code_pb2
from google.api_core import datetime_helpers
from google.api_core import exceptions
from google.cloud import spanner_v1
from google.cloud.spanner_admin_database_v1 import DatabaseDialect
from google.cloud._helpers import UTC
from google.cloud.spanner_v1.data_types import JsonObject
from tests import _helpers as ot_helpers
from . import _helpers
from . import _sample_data


SOME_DATE = datetime.date(2011, 1, 17)
SOME_TIME = datetime.datetime(1989, 1, 17, 17, 59, 12, 345612)
NANO_TIME = datetime_helpers.DatetimeWithNanoseconds(1995, 8, 31, nanosecond=987654321)
POS_INF = float("+inf")
NEG_INF = float("-inf")
(OTHER_NAN,) = struct.unpack("<d", b"\x01\x00\x01\x00\x00\x00\xf8\xff")
BYTES_1 = b"Ymlu"
BYTES_2 = b"Ym9vdHM="
NUMERIC_1 = decimal.Decimal("0.123456789")
NUMERIC_2 = decimal.Decimal("1234567890")
JSON_1 = JsonObject(
    {
        "sample_boolean": True,
        "sample_int": 872163,
        "sample float": 7871.298,
        "sample_null": None,
        "sample_string": "abcdef",
        "sample_array": [23, 76, 19],
    }
)
JSON_2 = JsonObject(
    {"sample_object": {"name": "Anamika", "id": 2635}},
)

COUNTERS_TABLE = "counters"
COUNTERS_COLUMNS = ("name", "value")
ALL_TYPES_TABLE = "all_types"
LIVE_ALL_TYPES_COLUMNS = (
    "pkey",
    "int_value",
    "int_array",
    "bool_value",
    "bool_array",
    "bytes_value",
    "bytes_array",
    "date_value",
    "date_array",
    "float_value",
    "float_array",
    "string_value",
    "string_array",
    "timestamp_value",
    "timestamp_array",
    "numeric_value",
    "numeric_array",
    "json_value",
    "json_array",
)

EMULATOR_ALL_TYPES_COLUMNS = LIVE_ALL_TYPES_COLUMNS[:-4]
# ToDo: Clean up generation of POSTGRES_ALL_TYPES_COLUMNS
POSTGRES_ALL_TYPES_COLUMNS = (
    LIVE_ALL_TYPES_COLUMNS[:1]
    + LIVE_ALL_TYPES_COLUMNS[1:7:2]
    + LIVE_ALL_TYPES_COLUMNS[9:17:2]
)

AllTypesRowData = collections.namedtuple("AllTypesRowData", LIVE_ALL_TYPES_COLUMNS)
AllTypesRowData.__new__.__defaults__ = tuple([None for colum in LIVE_ALL_TYPES_COLUMNS])
EmulatorAllTypesRowData = collections.namedtuple(
    "EmulatorAllTypesRowData", EMULATOR_ALL_TYPES_COLUMNS
)
EmulatorAllTypesRowData.__new__.__defaults__ = tuple(
    [None for colum in EMULATOR_ALL_TYPES_COLUMNS]
)
PostGresAllTypesRowData = collections.namedtuple(
    "PostGresAllTypesRowData", POSTGRES_ALL_TYPES_COLUMNS
)
PostGresAllTypesRowData.__new__.__defaults__ = tuple(
    [None for colum in POSTGRES_ALL_TYPES_COLUMNS]
)

LIVE_ALL_TYPES_ROWDATA = (
    # all nulls
    AllTypesRowData(pkey=0),
    # Non-null values
    AllTypesRowData(pkey=101, int_value=123),
    AllTypesRowData(pkey=102, bool_value=False),
    AllTypesRowData(pkey=103, bytes_value=BYTES_1),
    AllTypesRowData(pkey=104, date_value=SOME_DATE),
    AllTypesRowData(pkey=105, float_value=1.4142136),
    AllTypesRowData(pkey=106, string_value="VALUE"),
    AllTypesRowData(pkey=107, timestamp_value=SOME_TIME),
    AllTypesRowData(pkey=108, timestamp_value=NANO_TIME),
    AllTypesRowData(pkey=109, numeric_value=NUMERIC_1),
    AllTypesRowData(pkey=110, json_value=JSON_1),
    AllTypesRowData(pkey=111, json_value=[JSON_1, JSON_2]),
    # empty array values
    AllTypesRowData(pkey=201, int_array=[]),
    AllTypesRowData(pkey=202, bool_array=[]),
    AllTypesRowData(pkey=203, bytes_array=[]),
    AllTypesRowData(pkey=204, date_array=[]),
    AllTypesRowData(pkey=205, float_array=[]),
    AllTypesRowData(pkey=206, string_array=[]),
    AllTypesRowData(pkey=207, timestamp_array=[]),
    AllTypesRowData(pkey=208, numeric_array=[]),
    AllTypesRowData(pkey=209, json_array=[]),
    # non-empty array values, including nulls
    AllTypesRowData(pkey=301, int_array=[123, 456, None]),
    AllTypesRowData(pkey=302, bool_array=[True, False, None]),
    AllTypesRowData(pkey=303, bytes_array=[BYTES_1, BYTES_2, None]),
    AllTypesRowData(pkey=304, date_array=[SOME_DATE, None]),
    AllTypesRowData(pkey=305, float_array=[3.1415926, 2.71828, None]),
    AllTypesRowData(pkey=306, string_array=["One", "Two", None]),
    AllTypesRowData(pkey=307, timestamp_array=[SOME_TIME, NANO_TIME, None]),
    AllTypesRowData(pkey=308, numeric_array=[NUMERIC_1, NUMERIC_2, None]),
    AllTypesRowData(pkey=309, json_array=[JSON_1, JSON_2, None]),
)
EMULATOR_ALL_TYPES_ROWDATA = (
    # all nulls
    EmulatorAllTypesRowData(pkey=0),
    # Non-null values
    EmulatorAllTypesRowData(pkey=101, int_value=123),
    EmulatorAllTypesRowData(pkey=102, bool_value=False),
    EmulatorAllTypesRowData(pkey=103, bytes_value=BYTES_1),
    EmulatorAllTypesRowData(pkey=104, date_value=SOME_DATE),
    EmulatorAllTypesRowData(pkey=105, float_value=1.4142136),
    EmulatorAllTypesRowData(pkey=106, string_value="VALUE"),
    EmulatorAllTypesRowData(pkey=107, timestamp_value=SOME_TIME),
    EmulatorAllTypesRowData(pkey=108, timestamp_value=NANO_TIME),
    # empty array values
    EmulatorAllTypesRowData(pkey=201, int_array=[]),
    EmulatorAllTypesRowData(pkey=202, bool_array=[]),
    EmulatorAllTypesRowData(pkey=203, bytes_array=[]),
    EmulatorAllTypesRowData(pkey=204, date_array=[]),
    EmulatorAllTypesRowData(pkey=205, float_array=[]),
    EmulatorAllTypesRowData(pkey=206, string_array=[]),
    EmulatorAllTypesRowData(pkey=207, timestamp_array=[]),
    # non-empty array values, including nulls
    EmulatorAllTypesRowData(pkey=301, int_array=[123, 456, None]),
    EmulatorAllTypesRowData(pkey=302, bool_array=[True, False, None]),
    EmulatorAllTypesRowData(pkey=303, bytes_array=[BYTES_1, BYTES_2, None]),
    EmulatorAllTypesRowData(pkey=304, date_array=[SOME_DATE, None]),
    EmulatorAllTypesRowData(pkey=305, float_array=[3.1415926, 2.71828, None]),
    EmulatorAllTypesRowData(pkey=306, string_array=["One", "Two", None]),
    EmulatorAllTypesRowData(pkey=307, timestamp_array=[SOME_TIME, NANO_TIME, None]),
)

POSTGRES_ALL_TYPES_ROWDATA = (
    # all nulls
    PostGresAllTypesRowData(pkey=0),
    # Non-null values
    PostGresAllTypesRowData(pkey=101, int_value=123),
    PostGresAllTypesRowData(pkey=102, bool_value=False),
    PostGresAllTypesRowData(pkey=103, bytes_value=BYTES_1),
    PostGresAllTypesRowData(pkey=105, float_value=1.4142136),
    PostGresAllTypesRowData(pkey=106, string_value="VALUE"),
    PostGresAllTypesRowData(pkey=107, timestamp_value=SOME_TIME),
    PostGresAllTypesRowData(pkey=108, timestamp_value=NANO_TIME),
    PostGresAllTypesRowData(pkey=109, numeric_value=NUMERIC_1),
)

if _helpers.USE_EMULATOR:
    ALL_TYPES_COLUMNS = EMULATOR_ALL_TYPES_COLUMNS
    ALL_TYPES_ROWDATA = EMULATOR_ALL_TYPES_ROWDATA
elif _helpers.DATABASE_DIALECT:
    ALL_TYPES_COLUMNS = POSTGRES_ALL_TYPES_COLUMNS
    ALL_TYPES_ROWDATA = POSTGRES_ALL_TYPES_ROWDATA
else:
    ALL_TYPES_COLUMNS = LIVE_ALL_TYPES_COLUMNS
    ALL_TYPES_ROWDATA = LIVE_ALL_TYPES_ROWDATA


@pytest.fixture(scope="session")
def sessions_database(shared_instance, database_operation_timeout, database_dialect):
    database_name = _helpers.unique_id("test_sessions", separator="_")
    pool = spanner_v1.BurstyPool(labels={"testcase": "session_api"})

    if database_dialect == DatabaseDialect.POSTGRESQL:
        sessions_database = shared_instance.database(
            database_name,
            pool=pool,
            database_dialect=database_dialect,
        )

        operation = sessions_database.create()
        operation.result(database_operation_timeout)

        operation = sessions_database.update_ddl(ddl_statements=_helpers.DDL_STATEMENTS)
        operation.result(database_operation_timeout)

    else:
        sessions_database = shared_instance.database(
            database_name,
            ddl_statements=_helpers.DDL_STATEMENTS,
            pool=pool,
        )

        operation = sessions_database.create()
        operation.result(database_operation_timeout)

    _helpers.retry_has_all_dll(sessions_database.reload)()
    # Some tests expect there to be a session present in the pool.
    pool.put(pool.get())

    yield sessions_database

    sessions_database.drop()


@pytest.fixture(scope="function")
def sessions_to_delete():
    to_delete = []

    yield to_delete

    for session in to_delete:
        session.delete()


@pytest.fixture(scope="function")
def ot_exporter():
    if ot_helpers.HAS_OPENTELEMETRY_INSTALLED:
        ot_helpers.use_test_ot_exporter()
        ot_exporter = ot_helpers.get_test_ot_exporter()

        ot_exporter.clear()  # XXX?

        yield ot_exporter

        ot_exporter.clear()

    else:
        yield None


def assert_no_spans(ot_exporter):
    if ot_exporter is not None:
        span_list = ot_exporter.get_finished_spans()
        assert len(span_list) == 0


def assert_span_attributes(
    ot_exporter, name, status=ot_helpers.StatusCode.OK, attributes=None, span=None
):
    if ot_exporter is not None:
        if not span:
            span_list = ot_exporter.get_finished_spans()
            assert len(span_list) == 1
            span = span_list[0]

        assert span.name == name
        assert span.status.status_code == status
        assert dict(span.attributes) == attributes


def _make_attributes(db_instance, **kwargs):

    attributes = {
        "db.type": "spanner",
        "db.url": "spanner.googleapis.com",
        "net.host.name": "spanner.googleapis.com",
        "db.instance": db_instance,
    }
    attributes.update(kwargs)

    return attributes


class _ReadAbortTrigger(object):
    """Helper for tests provoking abort-during-read."""

    KEY1 = "key1"
    KEY2 = "key2"

    def __init__(self):
        self.provoker_started = threading.Event()
        self.provoker_done = threading.Event()
        self.handler_running = threading.Event()
        self.handler_done = threading.Event()

    def _provoke_abort_unit_of_work(self, transaction):
        keyset = spanner_v1.KeySet(keys=[(self.KEY1,)])
        rows = list(transaction.read(COUNTERS_TABLE, COUNTERS_COLUMNS, keyset))

        assert len(rows) == 1
        row = rows[0]
        value = row[1]

        self.provoker_started.set()

        self.handler_running.wait()

        transaction.update(COUNTERS_TABLE, COUNTERS_COLUMNS, [[self.KEY1, value + 1]])

    def provoke_abort(self, database):
        database.run_in_transaction(self._provoke_abort_unit_of_work)
        self.provoker_done.set()

    def _handle_abort_unit_of_work(self, transaction):
        keyset_1 = spanner_v1.KeySet(keys=[(self.KEY1,)])
        rows_1 = list(transaction.read(COUNTERS_TABLE, COUNTERS_COLUMNS, keyset_1))

        assert len(rows_1) == 1
        row_1 = rows_1[0]
        value_1 = row_1[1]

        self.handler_running.set()

        self.provoker_done.wait()

        keyset_2 = spanner_v1.KeySet(keys=[(self.KEY2,)])
        rows_2 = list(transaction.read(COUNTERS_TABLE, COUNTERS_COLUMNS, keyset_2))

        assert len(rows_2) == 1
        row_2 = rows_2[0]
        value_2 = row_2[1]

        transaction.update(
            COUNTERS_TABLE, COUNTERS_COLUMNS, [[self.KEY2, value_1 + value_2]]
        )

    def handle_abort(self, database):
        database.run_in_transaction(self._handle_abort_unit_of_work)
        self.handler_done.set()


def test_session_crud(sessions_database):
    session = sessions_database.session()
    assert not session.exists()

    session.create()
    _helpers.retry_true(session.exists)()

    session.delete()
    _helpers.retry_false(session.exists)()


def test_batch_insert_then_read(sessions_database, ot_exporter):
    db_name = sessions_database.name
    sd = _sample_data

    with sessions_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)
        batch.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    with sessions_database.snapshot(read_timestamp=batch.committed) as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))

    sd._check_rows_data(rows)

    if ot_exporter is not None:
        span_list = ot_exporter.get_finished_spans()
        assert len(span_list) == 4

        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.GetSession",
            attributes=_make_attributes(db_name, session_found=True),
            span=span_list[0],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.Commit",
            attributes=_make_attributes(db_name, num_mutations=2),
            span=span_list[1],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.GetSession",
            attributes=_make_attributes(db_name, session_found=True),
            span=span_list[2],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.ReadOnlyTransaction",
            attributes=_make_attributes(db_name, columns=sd.COLUMNS, table_id=sd.TABLE),
            span=span_list[3],
        )


def test_batch_insert_then_read_string_array_of_string(sessions_database, not_postgres):
    table = "string_plus_array_of_string"
    columns = ["id", "name", "tags"]
    rowdata = [
        (0, None, None),
        (1, "phred", ["yabba", "dabba", "do"]),
        (2, "bharney", []),
        (3, "wylma", ["oh", None, "phred"]),
    ]
    sd = _sample_data

    with sessions_database.batch() as batch:
        batch.delete(table, sd.ALL)
        batch.insert(table, columns, rowdata)

    with sessions_database.snapshot(read_timestamp=batch.committed) as snapshot:
        rows = list(snapshot.read(table, columns, sd.ALL))

    sd._check_rows_data(rows, expected=rowdata)


def test_batch_insert_then_read_all_datatypes(sessions_database):
    sd = _sample_data

    with sessions_database.batch() as batch:
        batch.delete(ALL_TYPES_TABLE, sd.ALL)
        batch.insert(ALL_TYPES_TABLE, ALL_TYPES_COLUMNS, ALL_TYPES_ROWDATA)

    with sessions_database.snapshot(read_timestamp=batch.committed) as snapshot:
        rows = list(snapshot.read(ALL_TYPES_TABLE, ALL_TYPES_COLUMNS, sd.ALL))

    sd._check_rows_data(rows, expected=ALL_TYPES_ROWDATA)


def test_batch_insert_or_update_then_query(sessions_database):
    sd = _sample_data

    with sessions_database.batch() as batch:
        batch.insert_or_update(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    with sessions_database.snapshot(read_timestamp=batch.committed) as snapshot:
        rows = list(snapshot.execute_sql(sd.SQL))

    sd._check_rows_data(rows)


def test_batch_insert_w_commit_timestamp(sessions_database, not_postgres):
    table = "users_history"
    columns = ["id", "commit_ts", "name", "email", "deleted"]
    user_id = 1234
    name = "phred"
    email = "phred@example.com"
    row_data = [[user_id, spanner_v1.COMMIT_TIMESTAMP, name, email, False]]
    sd = _sample_data

    with sessions_database.batch() as batch:
        batch.delete(table, sd.ALL)
        batch.insert(table, columns, row_data)

    with sessions_database.snapshot(read_timestamp=batch.committed) as snapshot:
        rows = list(snapshot.read(table, columns, sd.ALL))

    assert len(rows) == 1

    r_id, commit_ts, r_name, r_email, deleted = rows[0]
    assert r_id == user_id
    assert commit_ts == batch.committed
    assert r_name == name
    assert r_email == email
    assert not deleted


@_helpers.retry_mabye_aborted_txn
def test_transaction_read_and_insert_then_rollback(
    sessions_database,
    ot_exporter,
    sessions_to_delete,
):
    sd = _sample_data
    db_name = sessions_database.name

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with sessions_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    transaction = session.transaction()
    transaction.begin()

    rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    assert rows == []

    transaction.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

    # Inserted rows can't be read until after commit.
    rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    assert rows == []
    transaction.rollback()

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    assert rows == []

    if ot_exporter is not None:
        span_list = ot_exporter.get_finished_spans()
        assert len(span_list) == 8

        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.CreateSession",
            attributes=_make_attributes(db_name),
            span=span_list[0],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.GetSession",
            attributes=_make_attributes(db_name, session_found=True),
            span=span_list[1],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.Commit",
            attributes=_make_attributes(db_name, num_mutations=1),
            span=span_list[2],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.BeginTransaction",
            attributes=_make_attributes(db_name),
            span=span_list[3],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.ReadOnlyTransaction",
            attributes=_make_attributes(
                db_name,
                table_id=sd.TABLE,
                columns=sd.COLUMNS,
            ),
            span=span_list[4],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.ReadOnlyTransaction",
            attributes=_make_attributes(
                db_name,
                table_id=sd.TABLE,
                columns=sd.COLUMNS,
            ),
            span=span_list[5],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.Rollback",
            attributes=_make_attributes(db_name),
            span=span_list[6],
        )
        assert_span_attributes(
            ot_exporter,
            "CloudSpanner.ReadOnlyTransaction",
            attributes=_make_attributes(
                db_name,
                table_id=sd.TABLE,
                columns=sd.COLUMNS,
            ),
            span=span_list[7],
        )


@_helpers.retry_mabye_conflict
def test_transaction_read_and_insert_then_exception(sessions_database):
    class CustomException(Exception):
        pass

    sd = _sample_data

    def _transaction_read_then_raise(transaction):
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert len(rows) == 0

        transaction.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)
        raise CustomException()

    with sessions_database.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    with pytest.raises(CustomException):
        sessions_database.run_in_transaction(_transaction_read_then_raise)

    # Transaction was rolled back.
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))

    assert rows == []


@_helpers.retry_mabye_conflict
def test_transaction_read_and_insert_or_update_then_commit(
    sessions_database,
    sessions_to_delete,
):
    # [START spanner_test_dml_read_your_writes]
    sd = _sample_data

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    with session.transaction() as transaction:
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        transaction.insert_or_update(sd.TABLE, sd.COLUMNS, sd.ROW_DATA)

        # Inserted rows can't be read until after commit.
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows)
    # [END spanner_test_dml_read_your_writes]


def _generate_insert_statements():
    table = _sample_data.TABLE
    column_list = ", ".join(_sample_data.COLUMNS)

    for row in _sample_data.ROW_DATA:
        row_data = "{}, '{}', '{}', '{}'".format(*row)
        yield f"INSERT INTO {table} ({column_list}) VALUES ({row_data})"


@_helpers.retry_mabye_conflict
@_helpers.retry_mabye_aborted_txn
def test_transaction_execute_sql_w_dml_read_rollback(
    sessions_database,
    sessions_to_delete,
):
    # [START spanner_test_dml_rollback_txn_not_committed]
    sd = _sample_data

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    transaction = session.transaction()
    transaction.begin()

    rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    assert rows == []

    for insert_statement in _generate_insert_statements():
        result = transaction.execute_sql(insert_statement)
        list(result)  # iterate to get stats
        assert result.stats.row_count_exact == 1

    # Rows inserted via DML *can* be read before commit.
    during_rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(during_rows)

    transaction.rollback()

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows, [])
    # [END spanner_test_dml_rollback_txn_not_committed]


@_helpers.retry_mabye_conflict
def test_transaction_execute_update_read_commit(sessions_database, sessions_to_delete):
    # [START spanner_test_dml_read_your_writes]
    sd = _sample_data

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    with session.transaction() as transaction:
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        for insert_statement in _generate_insert_statements():
            row_count = transaction.execute_update(insert_statement)
            assert row_count == 1

        # Rows inserted via DML *can* be read before commit.
        during_rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_rows_data(during_rows)

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows)
    # [END spanner_test_dml_read_your_writes]


@_helpers.retry_mabye_conflict
def test_transaction_execute_update_then_insert_commit(
    sessions_database, sessions_to_delete
):
    # [START spanner_test_dml_with_mutation]
    # [START spanner_test_dml_update]
    sd = _sample_data

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    insert_statement = list(_generate_insert_statements())[0]

    with session.transaction() as transaction:
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        row_count = transaction.execute_update(insert_statement)
        assert row_count == 1

        transaction.insert(sd.TABLE, sd.COLUMNS, sd.ROW_DATA[1:])

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows)
    # [END spanner_test_dml_update]
    # [END spanner_test_dml_with_mutation]


def test_transaction_batch_update_success(
    sessions_database, sessions_to_delete, database_dialect
):
    # [START spanner_test_dml_with_mutation]
    # [START spanner_test_dml_update]
    sd = _sample_data
    param_types = spanner_v1.param_types

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    keys = (
        ["p1", "p2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else ["contact_id", "email"]
    )
    placeholders = (
        ["$1", "$2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else [f"@{key}" for key in keys]
    )

    insert_statement = list(_generate_insert_statements())[0]
    update_statement = (
        f"UPDATE contacts SET email = {placeholders[1]} WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1, keys[1]: "phreddy@example.com"},
        {keys[0]: param_types.INT64, keys[1]: param_types.STRING},
    )
    delete_statement = (
        f"DELETE FROM contacts WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1},
        {keys[0]: param_types.INT64},
    )

    def unit_of_work(transaction):
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        status, row_counts = transaction.batch_update(
            [insert_statement, update_statement, delete_statement]
        )
        _check_batch_status(status.code)
        assert len(row_counts) == 3

        for row_count in row_counts:
            assert row_count == 1

    session.run_in_transaction(unit_of_work)

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows, [])
    # [END spanner_test_dml_with_mutation]
    # [END spanner_test_dml_update]


def test_transaction_batch_update_and_execute_dml(
    sessions_database, sessions_to_delete, database_dialect
):
    sd = _sample_data
    param_types = spanner_v1.param_types

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    keys = (
        ["p1", "p2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else ["contact_id", "email"]
    )
    placeholders = (
        ["$1", "$2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else [f"@{key}" for key in keys]
    )

    insert_statements = list(_generate_insert_statements())
    update_statements = [
        (
            f"UPDATE contacts SET email = {placeholders[1]} WHERE contact_id = {placeholders[0]};",
            {keys[0]: 1, keys[1]: "phreddy@example.com"},
            {keys[0]: param_types.INT64, keys[1]: param_types.STRING},
        )
    ]

    delete_statement = "DELETE FROM contacts WHERE TRUE;"

    def unit_of_work(transaction):
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        status, row_counts = transaction.batch_update(
            insert_statements + update_statements
        )
        _check_batch_status(status.code)
        assert len(row_counts) == len(insert_statements) + 1

        for row_count in row_counts:
            assert row_count == 1

        row_count = transaction.execute_update(delete_statement)

        assert row_count == len(insert_statements)

    session.run_in_transaction(unit_of_work)

    rows = list(session.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(rows, [])


def test_transaction_batch_update_w_syntax_error(
    sessions_database, sessions_to_delete, database_dialect
):
    from google.rpc import code_pb2

    sd = _sample_data
    param_types = spanner_v1.param_types

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    keys = (
        ["p1", "p2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else ["contact_id", "email"]
    )
    placeholders = (
        ["$1", "$2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else [f"@{key}" for key in keys]
    )

    insert_statement = list(_generate_insert_statements())[0]
    update_statement = (
        f"UPDTAE contacts SET email = {placeholders[1]} WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1, keys[1]: "phreddy@example.com"},
        {keys[0]: param_types.INT64, keys[1]: param_types.STRING},
    )
    delete_statement = (
        f"DELETE FROM contacts WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1},
        {keys[0]: param_types.INT64},
    )

    def unit_of_work(transaction):
        rows = list(transaction.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        assert rows == []

        status, row_counts = transaction.batch_update(
            [insert_statement, update_statement, delete_statement]
        )
        _check_batch_status(status.code, code_pb2.INVALID_ARGUMENT)
        assert len(row_counts) == 1
        assert row_counts[0] == 1

    session.run_in_transaction(unit_of_work)


def test_transaction_batch_update_wo_statements(sessions_database, sessions_to_delete):
    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.transaction() as transaction:
        with pytest.raises(exceptions.InvalidArgument):
            transaction.batch_update([])


@pytest.mark.skipif(
    not ot_helpers.HAS_OPENTELEMETRY_INSTALLED,
    reason="trace requires OpenTelemetry",
)
def test_transaction_batch_update_w_parent_span(
    sessions_database, sessions_to_delete, ot_exporter, database_dialect
):
    from opentelemetry import trace

    sd = _sample_data
    param_types = spanner_v1.param_types
    tracer = trace.get_tracer(__name__)

    session = sessions_database.session()
    session.create()
    sessions_to_delete.append(session)

    with session.batch() as batch:
        batch.delete(sd.TABLE, sd.ALL)

    keys = (
        ["p1", "p2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else ["contact_id", "email"]
    )
    placeholders = (
        ["$1", "$2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else [f"@{key}" for key in keys]
    )

    insert_statement = list(_generate_insert_statements())[0]
    update_statement = (
        f"UPDATE contacts SET email = {placeholders[1]} WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1, keys[1]: "phreddy@example.com"},
        {keys[0]: param_types.INT64, keys[1]: param_types.STRING},
    )
    delete_statement = (
        f"DELETE FROM contacts WHERE contact_id = {placeholders[0]};",
        {keys[0]: 1},
        {keys[0]: param_types.INT64},
    )

    def unit_of_work(transaction):

        status, row_counts = transaction.batch_update(
            [insert_statement, update_statement, delete_statement]
        )
        _check_batch_status(status.code)
        assert len(row_counts) == 3
        for row_count in row_counts:
            assert row_count == 1

    with tracer.start_as_current_span("Test Span"):
        session.run_in_transaction(unit_of_work)

    span_list = ot_exporter.get_finished_spans()
    assert len(span_list) == 6
    expected_span_names = [
        "CloudSpanner.CreateSession",
        "CloudSpanner.Commit",
        "CloudSpanner.BeginTransaction",
        "CloudSpanner.DMLTransaction",
        "CloudSpanner.Commit",
        "Test Span",
    ]
    assert [span.name for span in span_list] == expected_span_names
    for span in span_list[2:-1]:
        assert span.context.trace_id == span_list[-1].context.trace_id
        assert span.parent.span_id == span_list[-1].context.span_id


def test_execute_partitioned_dml(sessions_database, database_dialect):
    # [START spanner_test_dml_partioned_dml_update]
    sd = _sample_data
    param_types = spanner_v1.param_types

    delete_statement = f"DELETE FROM {sd.TABLE} WHERE true"

    def _setup_table(txn):
        txn.execute_update(delete_statement)
        for insert_statement in _generate_insert_statements():
            txn.execute_update(insert_statement)

    committed = sessions_database.run_in_transaction(_setup_table)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        before_pdml = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))

    sd._check_rows_data(before_pdml)

    keys = (
        ["p1", "p2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else ["email", "target"]
    )
    placeholders = (
        ["$1", "$2"]
        if database_dialect == DatabaseDialect.POSTGRESQL
        else [f"@{key}" for key in keys]
    )
    nonesuch = "nonesuch@example.com"
    target = "phred@example.com"
    update_statement = (
        f"UPDATE contacts SET email = {placeholders[0]} WHERE email = {placeholders[1]}"
    )

    row_count = sessions_database.execute_partitioned_dml(
        update_statement,
        params={keys[0]: nonesuch, keys[1]: target},
        param_types={keys[0]: param_types.STRING, keys[1]: param_types.STRING},
        request_options=spanner_v1.RequestOptions(
            priority=spanner_v1.RequestOptions.Priority.PRIORITY_MEDIUM
        ),
    )
    assert row_count == 1

    row = sd.ROW_DATA[0]
    updated = [row[:3] + (nonesuch,)] + list(sd.ROW_DATA[1:])

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        after_update = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))
    sd._check_rows_data(after_update, updated)

    row_count = sessions_database.execute_partitioned_dml(delete_statement)
    assert row_count == len(sd.ROW_DATA)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        after_delete = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL))

    sd._check_rows_data(after_delete, [])
    # [END spanner_test_dml_partioned_dml_update]


def _transaction_concurrency_helper(
    sessions_database, unit_of_work, pkey, database_dialect=None
):
    initial_value = 123
    num_threads = 3  # conforms to equivalent Java systest.

    with sessions_database.batch() as batch:
        batch.insert_or_update(
            COUNTERS_TABLE, COUNTERS_COLUMNS, [[pkey, initial_value]]
        )

    # We don't want to run the threads' transactions in the current
    # session, which would fail.
    txn_sessions = []

    for _ in range(num_threads):
        txn_sessions.append(sessions_database)

    args = (
        (unit_of_work, pkey, database_dialect)
        if database_dialect
        else (unit_of_work, pkey)
    )

    threads = [
        threading.Thread(target=txn_session.run_in_transaction, args=args)
        for txn_session in txn_sessions
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with sessions_database.snapshot() as snapshot:
        keyset = spanner_v1.KeySet(keys=[(pkey,)])
        rows = list(snapshot.read(COUNTERS_TABLE, COUNTERS_COLUMNS, keyset))
        assert len(rows) == 1
        _, value = rows[0]
        assert value == initial_value + len(threads)


def _read_w_concurrent_update(transaction, pkey):
    keyset = spanner_v1.KeySet(keys=[(pkey,)])
    rows = list(transaction.read(COUNTERS_TABLE, COUNTERS_COLUMNS, keyset))
    assert len(rows) == 1
    pkey, value = rows[0]
    transaction.update(COUNTERS_TABLE, COUNTERS_COLUMNS, [[pkey, value + 1]])


def test_transaction_read_w_concurrent_updates(sessions_database):
    pkey = "read_w_concurrent_updates"
    _transaction_concurrency_helper(sessions_database, _read_w_concurrent_update, pkey)


def _query_w_concurrent_update(transaction, pkey, database_dialect):
    param_types = spanner_v1.param_types
    key = "p1" if database_dialect == DatabaseDialect.POSTGRESQL else "name"
    placeholder = "$1" if database_dialect == DatabaseDialect.POSTGRESQL else f"@{key}"
    sql = f"SELECT * FROM {COUNTERS_TABLE} WHERE name = {placeholder}"
    rows = list(
        transaction.execute_sql(
            sql, params={key: pkey}, param_types={key: param_types.STRING}
        )
    )
    assert len(rows) == 1
    pkey, value = rows[0]
    transaction.update(COUNTERS_TABLE, COUNTERS_COLUMNS, [[pkey, value + 1]])


def test_transaction_query_w_concurrent_updates(sessions_database, database_dialect):
    pkey = "query_w_concurrent_updates"
    _transaction_concurrency_helper(
        sessions_database, _query_w_concurrent_update, pkey, database_dialect
    )


def test_transaction_read_w_abort(not_emulator, sessions_database):
    sd = _sample_data
    trigger = _ReadAbortTrigger()

    with sessions_database.batch() as batch:
        batch.delete(COUNTERS_TABLE, sd.ALL)
        batch.insert(
            COUNTERS_TABLE, COUNTERS_COLUMNS, [[trigger.KEY1, 0], [trigger.KEY2, 0]]
        )

    provoker = threading.Thread(target=trigger.provoke_abort, args=(sessions_database,))
    handler = threading.Thread(target=trigger.handle_abort, args=(sessions_database,))

    provoker.start()
    trigger.provoker_started.wait()

    handler.start()
    trigger.handler_done.wait()

    provoker.join()
    handler.join()
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(COUNTERS_TABLE, COUNTERS_COLUMNS, sd.ALL))
        sd._check_row_data(rows, expected=[[trigger.KEY1, 1], [trigger.KEY2, 1]])


def _row_data(max_index):
    for index in range(max_index):
        yield (
            index,
            f"First{index:09}",
            f"Last{max_index - index:09}",
            f"test-{index:09}@example.com",
        )


def _set_up_table(database, row_count):

    sd = _sample_data

    def _unit_of_work(transaction):
        transaction.delete(sd.TABLE, sd.ALL)
        transaction.insert(sd.TABLE, sd.COLUMNS, _row_data(row_count))

    committed = database.run_in_transaction(_unit_of_work)

    return committed


def test_read_with_single_keys_index(sessions_database):
    # [START spanner_test_single_key_index_read]
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)

    expected = [[row[1], row[2]] for row in _row_data(row_count)]
    row = 5
    keyset = [[expected[row][0], expected[row][1]]]
    with sessions_database.snapshot() as snapshot:
        results_iter = snapshot.read(
            sd.TABLE, columns, spanner_v1.KeySet(keys=keyset), index="name"
        )
        rows = list(results_iter)
        assert rows == [expected[row]]

    # [END spanner_test_single_key_index_read]


def test_empty_read_with_single_keys_index(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)
    keyset = [["Non", "Existent"]]

    with sessions_database.snapshot() as snapshot:
        results_iter = snapshot.read(
            sd.TABLE, columns, spanner_v1.KeySet(keys=keyset), index="name"
        )
        rows = list(results_iter)
    assert rows == []


def test_read_with_multiple_keys_index(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)
    expected = [[row[1], row[2]] for row in _row_data(row_count)]

    with sessions_database.snapshot() as snapshot:
        rows = list(
            snapshot.read(
                sd.TABLE,
                columns,
                spanner_v1.KeySet(keys=expected),
                index="name",
            )
        )
    assert rows == expected


def test_snapshot_read_w_various_staleness(sessions_database):
    sd = _sample_data
    row_count = 400
    committed = _set_up_table(sessions_database, row_count)
    all_data_rows = list(_row_data(row_count))

    before_reads = datetime.datetime.utcnow().replace(tzinfo=UTC)

    # Test w/ read timestamp
    with sessions_database.snapshot(read_timestamp=committed) as read_tx:
        rows = list(read_tx.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(rows, all_data_rows)

    # Test w/ min read timestamp
    with sessions_database.snapshot(min_read_timestamp=committed) as min_read_ts:
        rows = list(min_read_ts.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(rows, all_data_rows)

    staleness = datetime.datetime.utcnow().replace(tzinfo=UTC) - before_reads

    # Test w/ max staleness
    with sessions_database.snapshot(max_staleness=staleness) as max_staleness:
        rows = list(max_staleness.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(rows, all_data_rows)

    # Test w/ exact staleness
    with sessions_database.snapshot(exact_staleness=staleness) as exact_staleness:
        rows = list(exact_staleness.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(rows, all_data_rows)

    # Test w/ strong
    with sessions_database.snapshot() as strong:
        rows = list(strong.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(rows, all_data_rows)


def test_multiuse_snapshot_read_isolation_strong(sessions_database):
    sd = _sample_data
    row_count = 40
    _set_up_table(sessions_database, row_count)
    all_data_rows = list(_row_data(row_count))
    with sessions_database.snapshot(multi_use=True) as strong:
        before = list(strong.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(before, all_data_rows)

        with sessions_database.batch() as batch:
            batch.delete(sd.TABLE, sd.ALL)

        after = list(strong.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(after, all_data_rows)


def test_multiuse_snapshot_read_isolation_read_timestamp(sessions_database):
    sd = _sample_data
    row_count = 40
    committed = _set_up_table(sessions_database, row_count)
    all_data_rows = list(_row_data(row_count))

    with sessions_database.snapshot(
        read_timestamp=committed, multi_use=True
    ) as read_ts:

        before = list(read_ts.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(before, all_data_rows)

        with sessions_database.batch() as batch:
            batch.delete(sd.TABLE, sd.ALL)

        after = list(read_ts.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(after, all_data_rows)


def test_multiuse_snapshot_read_isolation_exact_staleness(sessions_database):
    sd = _sample_data
    row_count = 40

    _set_up_table(sessions_database, row_count)
    all_data_rows = list(_row_data(row_count))

    time.sleep(1)
    delta = datetime.timedelta(microseconds=1000)

    with sessions_database.snapshot(exact_staleness=delta, multi_use=True) as exact:

        before = list(exact.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(before, all_data_rows)

        with sessions_database.batch() as batch:
            batch.delete(sd.TABLE, sd.ALL)

        after = list(exact.read(sd.TABLE, sd.COLUMNS, sd.ALL))
        sd._check_row_data(after, all_data_rows)


def test_read_w_index(
    shared_instance, database_operation_timeout, databases_to_delete, database_dialect
):
    # Indexed reads cannot return non-indexed columns
    sd = _sample_data
    row_count = 2000
    my_columns = sd.COLUMNS[0], sd.COLUMNS[2]

    # Create an alternate dataase w/ index.
    extra_ddl = ["CREATE INDEX contacts_by_last_name ON contacts(last_name)"]
    pool = spanner_v1.BurstyPool(labels={"testcase": "read_w_index"})

    if database_dialect == DatabaseDialect.POSTGRESQL:
        temp_db = shared_instance.database(
            _helpers.unique_id("test_read", separator="_"),
            pool=pool,
            database_dialect=database_dialect,
        )
        operation = temp_db.create()
        operation.result(database_operation_timeout)

        operation = temp_db.update_ddl(
            ddl_statements=_helpers.DDL_STATEMENTS + extra_ddl,
        )
        operation.result(database_operation_timeout)

    else:
        temp_db = shared_instance.database(
            _helpers.unique_id("test_read", separator="_"),
            ddl_statements=_helpers.DDL_STATEMENTS + extra_ddl,
            pool=pool,
            database_dialect=database_dialect,
        )
        operation = temp_db.create()
        operation.result(database_operation_timeout)  # raises on failure / timeout.

    databases_to_delete.append(temp_db)
    committed = _set_up_table(temp_db, row_count)

    with temp_db.snapshot(read_timestamp=committed) as snapshot:
        rows = list(
            snapshot.read(sd.TABLE, my_columns, sd.ALL, index="contacts_by_last_name")
        )

    expected = list(reversed([(row[0], row[2]) for row in _row_data(row_count)]))
    sd._check_rows_data(rows, expected)


def test_read_w_single_key(sessions_database):
    # [START spanner_test_single_key_read]
    sd = _sample_data
    row_count = 40
    committed = _set_up_table(sessions_database, row_count)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, spanner_v1.KeySet(keys=[(0,)])))

    all_data_rows = list(_row_data(row_count))
    expected = [all_data_rows[0]]
    sd._check_row_data(rows, expected)
    # [END spanner_test_single_key_read]


def test_empty_read(sessions_database):
    # [START spanner_test_empty_read]
    sd = _sample_data
    row_count = 40
    _set_up_table(sessions_database, row_count)
    with sessions_database.snapshot() as snapshot:
        rows = list(
            snapshot.read(sd.TABLE, sd.COLUMNS, spanner_v1.KeySet(keys=[(40,)]))
        )
    sd._check_row_data(rows, [])
    # [END spanner_test_empty_read]


def test_read_w_multiple_keys(sessions_database):
    sd = _sample_data
    row_count = 40
    indices = [0, 5, 17]
    committed = _set_up_table(sessions_database, row_count)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        rows = list(
            snapshot.read(
                sd.TABLE,
                sd.COLUMNS,
                spanner_v1.KeySet(keys=[(index,) for index in indices]),
            )
        )

    all_data_rows = list(_row_data(row_count))
    expected = [row for row in all_data_rows if row[0] in indices]
    sd._check_row_data(rows, expected)


def test_read_w_limit(sessions_database):
    sd = _sample_data
    row_count = 3000
    limit = 100
    committed = _set_up_table(sessions_database, row_count)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, sd.ALL, limit=limit))

    all_data_rows = list(_row_data(row_count))
    expected = all_data_rows[:limit]
    sd._check_row_data(rows, expected)


def test_read_w_ranges(sessions_database):
    sd = _sample_data
    row_count = 3000
    start = 1000
    end = 2000
    committed = _set_up_table(sessions_database, row_count)
    with sessions_database.snapshot(
        read_timestamp=committed,
        multi_use=True,
    ) as snapshot:
        all_data_rows = list(_row_data(row_count))

        single_key = spanner_v1.KeyRange(start_closed=[start], end_open=[start + 1])
        keyset = spanner_v1.KeySet(ranges=(single_key,))
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = all_data_rows[start : start + 1]
        sd._check_rows_data(rows, expected)

        closed_closed = spanner_v1.KeyRange(start_closed=[start], end_closed=[end])
        keyset = spanner_v1.KeySet(ranges=(closed_closed,))
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = all_data_rows[start : end + 1]
        sd._check_row_data(rows, expected)

        closed_open = spanner_v1.KeyRange(start_closed=[start], end_open=[end])
        keyset = spanner_v1.KeySet(ranges=(closed_open,))
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = all_data_rows[start:end]
        sd._check_row_data(rows, expected)

        open_open = spanner_v1.KeyRange(start_open=[start], end_open=[end])
        keyset = spanner_v1.KeySet(ranges=(open_open,))
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = all_data_rows[start + 1 : end]
        sd._check_row_data(rows, expected)

        open_closed = spanner_v1.KeyRange(start_open=[start], end_closed=[end])
        keyset = spanner_v1.KeySet(ranges=(open_closed,))
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = all_data_rows[start + 1 : end + 1]
        sd._check_row_data(rows, expected)


def test_read_partial_range_until_end(sessions_database):
    sd = _sample_data
    row_count = 3000
    start = 1000
    committed = _set_up_table(sessions_database, row_count)
    with sessions_database.snapshot(
        read_timestamp=committed,
        multi_use=True,
    ) as snapshot:
        all_data_rows = list(_row_data(row_count))

        expected_map = {
            ("start_closed", "end_closed"): all_data_rows[start:],
            ("start_closed", "end_open"): [],
            ("start_open", "end_closed"): all_data_rows[start + 1 :],
            ("start_open", "end_open"): [],
        }

        for start_arg in ("start_closed", "start_open"):
            for end_arg in ("end_closed", "end_open"):
                range_kwargs = {start_arg: [start], end_arg: []}
                keyset = spanner_v1.KeySet(
                    ranges=(spanner_v1.KeyRange(**range_kwargs),)
                )

                rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
                expected = expected_map[(start_arg, end_arg)]
                sd._check_row_data(rows, expected)


def test_read_partial_range_from_beginning(sessions_database):
    sd = _sample_data
    row_count = 3000
    end = 2000
    committed = _set_up_table(sessions_database, row_count)

    all_data_rows = list(_row_data(row_count))

    expected_map = {
        ("start_closed", "end_closed"): all_data_rows[: end + 1],
        ("start_closed", "end_open"): all_data_rows[:end],
        ("start_open", "end_closed"): [],
        ("start_open", "end_open"): [],
    }

    for start_arg in ("start_closed", "start_open"):
        for end_arg in ("end_closed", "end_open"):
            range_kwargs = {start_arg: [], end_arg: [end]}
            keyset = spanner_v1.KeySet(ranges=(spanner_v1.KeyRange(**range_kwargs),))

    with sessions_database.snapshot(
        read_timestamp=committed,
        multi_use=True,
    ) as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))
        expected = expected_map[(start_arg, end_arg)]
        sd._check_row_data(rows, expected)


def test_read_with_range_keys_index_single_key(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start = 3
    krange = spanner_v1.KeyRange(start_closed=data[start], end_open=data[start + 1])
    keyset = spanner_v1.KeySet(ranges=(krange,))

    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        assert rows == data[start : start + 1]


def test_read_with_range_keys_index_closed_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end = 3, 7
    krange = spanner_v1.KeyRange(start_closed=data[start], end_closed=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))

    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        assert rows == data[start : end + 1]


def test_read_with_range_keys_index_closed_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end = 3, 7
    krange = spanner_v1.KeyRange(start_closed=data[start], end_open=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))

    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        assert rows == data[start:end]


def test_read_with_range_keys_index_open_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end = 3, 7
    krange = spanner_v1.KeyRange(start_open=data[start], end_closed=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))

    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        assert rows == data[start + 1 : end + 1]


def test_read_with_range_keys_index_open_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end = 3, 7
    krange = spanner_v1.KeyRange(start_open=data[start], end_open=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))

    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        assert rows == data[start + 1 : end]


def test_read_with_range_keys_index_limit_closed_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end, limit = 3, 7, 2
    krange = spanner_v1.KeyRange(start_closed=data[start], end_closed=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name", limit=limit))
        expected = data[start : end + 1]
        assert rows == expected[:limit]


def test_read_with_range_keys_index_limit_closed_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end, limit = 3, 7, 2
    krange = spanner_v1.KeyRange(start_closed=data[start], end_open=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name", limit=limit))
        expected = data[start:end]
        assert rows == expected[:limit]


def test_read_with_range_keys_index_limit_open_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end, limit = 3, 7, 2
    krange = spanner_v1.KeyRange(start_open=data[start], end_closed=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name", limit=limit))
        expected = data[start + 1 : end + 1]
        assert rows == expected[:limit]


def test_read_with_range_keys_index_limit_open_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    _set_up_table(sessions_database, row_count)
    start, end, limit = 3, 7, 2
    krange = spanner_v1.KeyRange(start_open=data[start], end_open=data[end])
    keyset = spanner_v1.KeySet(ranges=(krange,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name", limit=limit))
        expected = data[start + 1 : end]
        assert rows == expected[:limit]


def test_read_with_range_keys_and_index_closed_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]

    _set_up_table(sessions_database, row_count)
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    keyrow, start, end = 1, 3, 7
    closed_closed = spanner_v1.KeyRange(start_closed=data[start], end_closed=data[end])
    keys = [data[keyrow]]
    keyset = spanner_v1.KeySet(keys=keys, ranges=(closed_closed,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        expected = [data[keyrow]] + data[start : end + 1]
        assert rows == expected


def test_read_with_range_keys_and_index_closed_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    keyrow, start, end = 1, 3, 7
    closed_open = spanner_v1.KeyRange(start_closed=data[start], end_open=data[end])
    keys = [data[keyrow]]
    keyset = spanner_v1.KeySet(keys=keys, ranges=(closed_open,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        expected = [data[keyrow]] + data[start:end]
        assert rows == expected


def test_read_with_range_keys_and_index_open_closed(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    keyrow, start, end = 1, 3, 7
    open_closed = spanner_v1.KeyRange(start_open=data[start], end_closed=data[end])
    keys = [data[keyrow]]
    keyset = spanner_v1.KeySet(keys=keys, ranges=(open_closed,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        expected = [data[keyrow]] + data[start + 1 : end + 1]
        assert rows == expected


def test_read_with_range_keys_and_index_open_open(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    _set_up_table(sessions_database, row_count)
    data = [[row[1], row[2]] for row in _row_data(row_count)]
    keyrow, start, end = 1, 3, 7
    open_open = spanner_v1.KeyRange(start_open=data[start], end_open=data[end])
    keys = [data[keyrow]]
    keyset = spanner_v1.KeySet(keys=keys, ranges=(open_open,))
    with sessions_database.snapshot() as snapshot:
        rows = list(snapshot.read(sd.TABLE, columns, keyset, index="name"))
        expected = [data[keyrow]] + data[start + 1 : end]
        assert rows == expected


def test_partition_read_w_index(sessions_database):
    sd = _sample_data
    row_count = 10
    columns = sd.COLUMNS[1], sd.COLUMNS[2]
    committed = _set_up_table(sessions_database, row_count)

    expected = [[row[1], row[2]] for row in _row_data(row_count)]
    union = []

    batch_txn = sessions_database.batch_snapshot(read_timestamp=committed)
    batches = batch_txn.generate_read_batches(
        sd.TABLE, columns, spanner_v1.KeySet(all_=True), index="name"
    )
    for batch in batches:
        p_results_iter = batch_txn.process(batch)
        union.extend(list(p_results_iter))

    assert union == expected
    batch_txn.close()


def test_execute_sql_w_manual_consume(sessions_database):
    sd = _sample_data
    row_count = 3000
    committed = _set_up_table(sessions_database, row_count)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        streamed = snapshot.execute_sql(sd.SQL)

    keyset = spanner_v1.KeySet(all_=True)

    with sessions_database.snapshot(read_timestamp=committed) as snapshot:
        rows = list(snapshot.read(sd.TABLE, sd.COLUMNS, keyset))

    assert list(streamed) == rows
    assert streamed._current_row == []
    assert streamed._pending_chunk is None


def _check_sql_results(
    database,
    sql,
    params,
    param_types,
    expected,
    order=True,
    recurse_into_lists=True,
):
    if order and "ORDER" not in sql:
        sql += " ORDER BY pkey"

    with database.snapshot() as snapshot:
        rows = list(snapshot.execute_sql(sql, params=params, param_types=param_types))

    _sample_data._check_rows_data(
        rows, expected=expected, recurse_into_lists=recurse_into_lists
    )


def test_multiuse_snapshot_execute_sql_isolation_strong(sessions_database):
    sd = _sample_data
    row_count = 40
    _set_up_table(sessions_database, row_count)
    all_data_rows = list(_row_data(row_count))

    with sessions_database.snapshot(multi_use=True) as strong:

        before = list(strong.execute_sql(sd.SQL))
        sd._check_row_data(before, all_data_rows)

        with sessions_database.batch() as batch:
            batch.delete(sd.TABLE, sd.ALL)

        after = list(strong.execute_sql(sd.SQL))
        sd._check_row_data(after, all_data_rows)


def test_execute_sql_returning_array_of_struct(sessions_database, not_postgres):
    sql = (
        "SELECT ARRAY(SELECT AS STRUCT C1, C2 "
        "FROM (SELECT 'a' AS C1, 1 AS C2 "
        "UNION ALL SELECT 'b' AS C1, 2 AS C2) "
        "ORDER BY C1 ASC)"
    )
    _check_sql_results(
        sessions_database,
        sql=sql,
        params=None,
        param_types=None,
        expected=[[[["a", 1], ["b", 2]]]],
    )


def test_execute_sql_returning_empty_array_of_struct(sessions_database, not_postgres):
    sql = (
        "SELECT ARRAY(SELECT AS STRUCT C1, C2 "
        "FROM (SELECT 2 AS C1) X "
        "JOIN (SELECT 1 AS C2) Y "
        "ON X.C1 = Y.C2 "
        "ORDER BY C1 ASC)"
    )
    sessions_database.snapshot(multi_use=True)

    _check_sql_results(
        sessions_database, sql=sql, params=None, param_types=None, expected=[[[]]]
    )


def test_invalid_type(sessions_database):
    sd = _sample_data
    table = "counters"
    columns = ("name", "value")

    valid_input = (("", 0),)
    with sessions_database.batch() as batch:
        batch.delete(table, sd.ALL)
        batch.insert(table, columns, valid_input)

    invalid_input = ((0, ""),)
    with pytest.raises(exceptions.FailedPrecondition):
        with sessions_database.batch() as batch:
            batch.delete(table, sd.ALL)
            batch.insert(table, columns, invalid_input)


def test_execute_sql_select_1(sessions_database):

    sessions_database.snapshot(multi_use=True)

    # Hello, world query
    _check_sql_results(
        sessions_database,
        sql="SELECT 1",
        params=None,
        param_types=None,
        expected=[(1,)],
        order=False,
    )


def _bind_test_helper(
    database,
    database_dialect,
    param_type,
    single_value,
    array_value,
    expected_array_value=None,
    recurse_into_lists=True,
):
    database.snapshot(multi_use=True)

    key = "p1" if database_dialect == DatabaseDialect.POSTGRESQL else "v"
    placeholder = "$1" if database_dialect == DatabaseDialect.POSTGRESQL else f"@{key}"

    # Bind a non-null <type_name>
    _check_sql_results(
        database,
        sql=f"SELECT {placeholder}",
        params={key: single_value},
        param_types={key: param_type},
        expected=[(single_value,)],
        order=False,
        recurse_into_lists=recurse_into_lists,
    )

    # Bind a null <type_name>
    _check_sql_results(
        database,
        sql=f"SELECT {placeholder}",
        params={key: None},
        param_types={key: param_type},
        expected=[(None,)],
        order=False,
        recurse_into_lists=recurse_into_lists,
    )

    # Bind an array of <type_name>
    array_element_type = param_type
    array_type = spanner_v1.Type(
        code=spanner_v1.TypeCode.ARRAY, array_element_type=array_element_type
    )

    if expected_array_value is None:
        expected_array_value = array_value

    _check_sql_results(
        database,
        sql=f"SELECT {placeholder}",
        params={key: array_value},
        param_types={key: array_type},
        expected=[(expected_array_value,)],
        order=False,
        recurse_into_lists=recurse_into_lists,
    )

    # Bind an empty array of <type_name>
    _check_sql_results(
        database,
        sql=f"SELECT {placeholder}",
        params={key: []},
        param_types={key: array_type},
        expected=[([],)],
        order=False,
        recurse_into_lists=recurse_into_lists,
    )

    # Bind a null array of <type_name>
    _check_sql_results(
        database,
        sql=f"SELECT {placeholder}",
        params={key: None},
        param_types={key: array_type},
        expected=[(None,)],
        order=False,
        recurse_into_lists=recurse_into_lists,
    )


def test_execute_sql_w_string_bindings(sessions_database, database_dialect):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.STRING,
        "Phred",
        ["Phred", "Bharney"],
    )


def test_execute_sql_w_bool_bindings(sessions_database, database_dialect):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.BOOL,
        True,
        [True, False, True],
    )


def test_execute_sql_w_int64_bindings(sessions_database, database_dialect):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.INT64,
        42,
        [123, 456, 789],
    )


def test_execute_sql_w_float64_bindings(sessions_database, database_dialect):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.FLOAT64,
        42.3,
        [12.3, 456.0, 7.89],
    )


def test_execute_sql_w_float_bindings_transfinite(sessions_database, database_dialect):
    key = "p1" if database_dialect == DatabaseDialect.POSTGRESQL else "neg_inf"
    placeholder = "$1" if database_dialect == DatabaseDialect.POSTGRESQL else f"@{key}"

    # Find -inf
    _check_sql_results(
        sessions_database,
        sql=f"SELECT {placeholder}",
        params={key: NEG_INF},
        param_types={key: spanner_v1.param_types.FLOAT64},
        expected=[(NEG_INF,)],
        order=False,
    )

    key = "p1" if database_dialect == DatabaseDialect.POSTGRESQL else "pos_inf"
    placeholder = "$1" if database_dialect == DatabaseDialect.POSTGRESQL else f"@{key}"
    # Find +inf
    _check_sql_results(
        sessions_database,
        sql=f"SELECT {placeholder}",
        params={key: POS_INF},
        param_types={key: spanner_v1.param_types.FLOAT64},
        expected=[(POS_INF,)],
        order=False,
    )


def test_execute_sql_w_bytes_bindings(sessions_database, database_dialect):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.BYTES,
        b"DEADBEEF",
        [b"FACEDACE", b"DEADBEEF"],
    )


def test_execute_sql_w_timestamp_bindings(sessions_database, database_dialect):

    timestamp_1 = datetime_helpers.DatetimeWithNanoseconds(
        1989, 1, 17, 17, 59, 12, nanosecond=345612789
    )

    timestamp_2 = datetime_helpers.DatetimeWithNanoseconds(
        1989, 1, 17, 17, 59, 13, nanosecond=456127893
    )

    timestamps = [timestamp_1, timestamp_2]

    # In round-trip, timestamps acquire a timezone value.
    expected_timestamps = [timestamp.replace(tzinfo=UTC) for timestamp in timestamps]

    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.TIMESTAMP,
        timestamp_1,
        timestamps,
        expected_timestamps,
        recurse_into_lists=False,
    )


def test_execute_sql_w_date_bindings(sessions_database, not_postgres, database_dialect):
    dates = [SOME_DATE, SOME_DATE + datetime.timedelta(days=1)]
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.DATE,
        SOME_DATE,
        dates,
    )


def test_execute_sql_w_numeric_bindings(
    not_emulator, sessions_database, database_dialect
):
    if database_dialect == DatabaseDialect.POSTGRESQL:
        _bind_test_helper(
            sessions_database,
            database_dialect,
            spanner_v1.param_types.PG_NUMERIC,
            NUMERIC_1,
            [NUMERIC_1, NUMERIC_2],
        )
    else:
        _bind_test_helper(
            sessions_database,
            database_dialect,
            spanner_v1.param_types.NUMERIC,
            NUMERIC_1,
            [NUMERIC_1, NUMERIC_2],
        )


def test_execute_sql_w_json_bindings(
    not_emulator, not_postgres, sessions_database, database_dialect
):
    _bind_test_helper(
        sessions_database,
        database_dialect,
        spanner_v1.param_types.JSON,
        JSON_1,
        [JSON_1, JSON_2],
    )


def test_execute_sql_w_query_param_struct(sessions_database, not_postgres):
    name = "Phred"
    count = 123
    size = 23.456
    height = 188.0
    weight = 97.6
    param_types = spanner_v1.param_types

    record_type = param_types.Struct(
        [
            param_types.StructField("name", param_types.STRING),
            param_types.StructField("count", param_types.INT64),
            param_types.StructField("size", param_types.FLOAT64),
            param_types.StructField(
                "nested",
                param_types.Struct(
                    [
                        param_types.StructField("height", param_types.FLOAT64),
                        param_types.StructField("weight", param_types.FLOAT64),
                    ]
                ),
            ),
        ]
    )

    # Query with null struct, explicit type
    _check_sql_results(
        sessions_database,
        sql="SELECT @r.name, @r.count, @r.size, @r.nested.weight",
        params={"r": None},
        param_types={"r": record_type},
        expected=[(None, None, None, None)],
        order=False,
    )

    # Query with non-null struct, explicit type, NULL values
    _check_sql_results(
        sessions_database,
        sql="SELECT @r.name, @r.count, @r.size, @r.nested.weight",
        params={"r": (None, None, None, None)},
        param_types={"r": record_type},
        expected=[(None, None, None, None)],
        order=False,
    )

    # Query with non-null struct, explicit type, nested NULL values
    _check_sql_results(
        sessions_database,
        sql="SELECT @r.nested.weight",
        params={"r": (None, None, None, (None, None))},
        param_types={"r": record_type},
        expected=[(None,)],
        order=False,
    )

    # Query with non-null struct, explicit type
    _check_sql_results(
        sessions_database,
        sql="SELECT @r.name, @r.count, @r.size, @r.nested.weight",
        params={"r": (name, count, size, (height, weight))},
        param_types={"r": record_type},
        expected=[(name, count, size, weight)],
        order=False,
    )

    # Query with empty struct, explicitly empty type
    empty_type = param_types.Struct([])
    _check_sql_results(
        sessions_database,
        sql="SELECT @r IS NULL",
        params={"r": ()},
        param_types={"r": empty_type},
        expected=[(False,)],
        order=False,
    )

    # Query with null struct, explicitly empty type
    _check_sql_results(
        sessions_database,
        sql="SELECT @r IS NULL",
        params={"r": None},
        param_types={"r": empty_type},
        expected=[(True,)],
        order=False,
    )

    # Query with equality check for struct value
    struct_equality_query = (
        "SELECT " '@struct_param=STRUCT<threadf INT64, userf STRING>(1,"bob")'
    )
    struct_type = param_types.Struct(
        [
            param_types.StructField("threadf", param_types.INT64),
            param_types.StructField("userf", param_types.STRING),
        ]
    )
    _check_sql_results(
        sessions_database,
        sql=struct_equality_query,
        params={"struct_param": (1, "bob")},
        param_types={"struct_param": struct_type},
        expected=[(True,)],
        order=False,
    )

    # Query with nullness test for struct
    _check_sql_results(
        sessions_database,
        sql="SELECT @struct_param IS NULL",
        params={"struct_param": None},
        param_types={"struct_param": struct_type},
        expected=[(True,)],
        order=False,
    )

    # Query with null array-of-struct
    array_elem_type = param_types.Struct(
        [param_types.StructField("threadid", param_types.INT64)]
    )
    array_type = param_types.Array(array_elem_type)
    _check_sql_results(
        sessions_database,
        sql="SELECT a.threadid FROM UNNEST(@struct_arr_param) a",
        params={"struct_arr_param": None},
        param_types={"struct_arr_param": array_type},
        expected=[],
        order=False,
    )

    # Query with non-null array-of-struct
    _check_sql_results(
        sessions_database,
        sql="SELECT a.threadid FROM UNNEST(@struct_arr_param) a",
        params={"struct_arr_param": [(123,), (456,)]},
        param_types={"struct_arr_param": array_type},
        expected=[(123,), (456,)],
        order=False,
    )

    # Query with null array-of-struct field
    struct_type_with_array_field = param_types.Struct(
        [
            param_types.StructField("intf", param_types.INT64),
            param_types.StructField("arraysf", array_type),
        ]
    )
    _check_sql_results(
        sessions_database,
        sql="SELECT a.threadid FROM UNNEST(@struct_param.arraysf) a",
        params={"struct_param": (123, None)},
        param_types={"struct_param": struct_type_with_array_field},
        expected=[],
        order=False,
    )

    # Query with non-null array-of-struct field
    _check_sql_results(
        sessions_database,
        sql="SELECT a.threadid FROM UNNEST(@struct_param.arraysf) a",
        params={"struct_param": (123, ((456,), (789,)))},
        param_types={"struct_param": struct_type_with_array_field},
        expected=[(456,), (789,)],
        order=False,
    )

    # Query with anonymous / repeated-name fields
    anon_repeated_array_elem_type = param_types.Struct(
        [
            param_types.StructField("", param_types.INT64),
            param_types.StructField("", param_types.STRING),
        ]
    )
    anon_repeated_array_type = param_types.Array(anon_repeated_array_elem_type)
    _check_sql_results(
        sessions_database,
        sql="SELECT CAST(t as STRUCT<threadid INT64, userid STRING>).* "
        "FROM UNNEST(@struct_param) t",
        params={"struct_param": [(123, "abcdef")]},
        param_types={"struct_param": anon_repeated_array_type},
        expected=[(123, "abcdef")],
        order=False,
    )

    # Query and return a struct parameter
    value_type = param_types.Struct(
        [
            param_types.StructField("message", param_types.STRING),
            param_types.StructField("repeat", param_types.INT64),
        ]
    )
    value_query = (
        "SELECT ARRAY(SELECT AS STRUCT message, repeat "
        "FROM (SELECT @value.message AS message, "
        "@value.repeat AS repeat)) AS value"
    )
    _check_sql_results(
        sessions_database,
        sql=value_query,
        params={"value": ("hello", 1)},
        param_types={"value": value_type},
        expected=[([["hello", 1]],)],
        order=False,
    )


def test_execute_sql_returning_transfinite_floats(sessions_database, not_postgres):

    with sessions_database.snapshot(multi_use=True) as snapshot:
        # Query returning -inf, +inf, NaN as column values
        rows = list(
            snapshot.execute_sql(
                "SELECT "
                'CAST("-inf" AS FLOAT64), '
                'CAST("+inf" AS FLOAT64), '
                'CAST("NaN" AS FLOAT64)'
            )
        )
        assert len(rows) == 1
        assert rows[0][0] == float("-inf")
        assert rows[0][1] == float("+inf")
        # NaNs cannot be compared by equality.
        assert math.isnan(rows[0][2])

        # Query returning array of -inf, +inf, NaN as one column
        rows = list(
            snapshot.execute_sql(
                "SELECT"
                ' [CAST("-inf" AS FLOAT64),'
                ' CAST("+inf" AS FLOAT64),'
                ' CAST("NaN" AS FLOAT64)]'
            )
        )
        assert len(rows) == 1

        float_array = rows[0][0]
        assert float_array[0] == float("-inf")
        assert float_array[1] == float("+inf")

        # NaNs cannot be searched for by equality.
        assert math.isnan(float_array[2])


def test_partition_query(sessions_database):
    row_count = 40
    sql = f"SELECT * FROM {_sample_data.TABLE}"
    committed = _set_up_table(sessions_database, row_count)

    # Paritioned query does not support ORDER BY
    all_data_rows = set(_row_data(row_count))
    union = set()
    batch_txn = sessions_database.batch_snapshot(read_timestamp=committed)
    for batch in batch_txn.generate_query_batches(sql):
        p_results_iter = batch_txn.process(batch)
        # Lists aren't hashable so the results need to be converted
        rows = [tuple(result) for result in p_results_iter]
        union.update(set(rows))

    assert union == all_data_rows
    batch_txn.close()


class FauxCall:
    def __init__(self, code, details="FauxCall"):
        self._code = code
        self._details = details

    def initial_metadata(self):
        return {}

    def trailing_metadata(self):
        return {}

    def code(self):
        return self._code

    def details(self):
        return self._details


def _check_batch_status(status_code, expected=code_pb2.OK):
    if status_code != expected:

        _status_code_to_grpc_status_code = {
            member.value[0]: member for member in grpc.StatusCode
        }
        grpc_status_code = _status_code_to_grpc_status_code[status_code]
        call = FauxCall(status_code)
        raise exceptions.from_grpc_status(
            grpc_status_code, "batch_update failed", errors=[call]
        )
