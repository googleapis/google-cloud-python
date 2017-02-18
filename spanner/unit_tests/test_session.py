# Copyright 2016 Google Inc. All rights reserved.
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


import unittest

from google.cloud._testing import _GAXBaseAPI


class TestSession(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = ('projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID)
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner.session import Session

        return Session

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        self.assertTrue(session.session_id is None)
        self.assertTrue(session._database is database)

    def test___lt___(self):
        database = _Database(self.DATABASE_NAME)
        lhs = self._make_one(database)
        lhs._session_id = b'123'
        rhs = self._make_one(database)
        rhs._session_id = b'234'
        self.assertTrue(lhs < rhs)

    def test_name_property_wo_session_id(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        with self.assertRaises(ValueError):
            _ = session.name

    def test_name_property_w_session_id(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = self.SESSION_ID
        self.assertEqual(session.name, self.SESSION_NAME)

    def test_create_w_session_id(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = self.SESSION_ID
        with self.assertRaises(ValueError):
            session.create()

    def test_create_ok(self):
        session_pb = _SessionPB(self.SESSION_NAME)
        gax_api = _SpannerApi(_create_session_response=session_pb)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)

        session.create()

        self.assertEqual(session.session_id, self.SESSION_ID)

        database_name, options = gax_api._create_session_called_with
        self.assertEqual(database_name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_create_error(self):
        from google.gax.errors import GaxError

        gax_api = _SpannerApi(_random_gax_error=True)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)

        with self.assertRaises(GaxError):
            session.create()

        database_name, options = gax_api._create_session_called_with
        self.assertEqual(database_name, self.DATABASE_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_wo_session_id(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        self.assertFalse(session.exists())

    def test_exists_hit(self):
        session_pb = _SessionPB(self.SESSION_NAME)
        gax_api = _SpannerApi(_get_session_response=session_pb)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        self.assertTrue(session.exists())

        session_name, options = gax_api._get_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_miss(self):
        gax_api = _SpannerApi()
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        self.assertFalse(session.exists())

        session_name, options = gax_api._get_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_exists_error(self):
        from google.gax.errors import GaxError

        gax_api = _SpannerApi(_random_gax_error=True)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(GaxError):
            session.exists()

        session_name, options = gax_api._get_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_delete_wo_session_id(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        with self.assertRaises(ValueError):
            session.delete()

    def test_delete_hit(self):
        gax_api = _SpannerApi(_delete_session_ok=True)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        session.delete()

        session_name, options = gax_api._delete_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_delete_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = _SpannerApi(_delete_session_ok=False)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(NotFound):
            session.delete()

        session_name, options = gax_api._delete_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_delete_error(self):
        from google.gax.errors import GaxError

        gax_api = _SpannerApi(_random_gax_error=True)
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(GaxError):
            session.delete()

        session_name, options = gax_api._delete_session_called_with
        self.assertEqual(session_name, self.SESSION_NAME)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_snapshot_not_created(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.snapshot()

    def test_snapshot_created(self):
        from google.cloud.spanner.snapshot import Snapshot

        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'  # emulate 'session.create()'

        snapshot = session.snapshot()

        self.assertIsInstance(snapshot, Snapshot)
        self.assertTrue(snapshot._session is session)
        self.assertTrue(snapshot._strong)

    def test_read_not_created(self):
        from google.cloud.spanner.keyset import KeySet

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        KEYS = ['bharney@example.com', 'phred@example.com']
        KEYSET = KeySet(keys=KEYS)
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.read(TABLE_NAME, COLUMNS, KEYSET)

    def test_read(self):
        from google.cloud.spanner import session as MUT
        from google.cloud._testing import _Monkey
        from google.cloud.spanner.keyset import KeySet

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        KEYS = ['bharney@example.com', 'phred@example.com']
        KEYSET = KeySet(keys=KEYS)
        INDEX = 'email-address-index'
        LIMIT = 20
        TOKEN = b'DEADBEEF'
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        _read_with = []
        expected = object()

        class _Snapshot(object):

            def __init__(self, session, **kwargs):
                self._session = session
                self._kwargs = kwargs.copy()

            def read(self, table, columns, keyset, index='', limit=0,
                     resume_token=b''):
                _read_with.append(
                    (table, columns, keyset, index, limit, resume_token))
                return expected

        with _Monkey(MUT, Snapshot=_Snapshot):
            found = session.read(
                TABLE_NAME, COLUMNS, KEYSET,
                index=INDEX, limit=LIMIT, resume_token=TOKEN)

        self.assertIs(found, expected)

        self.assertEqual(len(_read_with), 1)
        (table, columns, key_set, index, limit, resume_token) = _read_with[0]

        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(key_set, KEYSET)
        self.assertEqual(index, INDEX)
        self.assertEqual(limit, LIMIT)
        self.assertEqual(resume_token, TOKEN)

    def test_execute_sql_not_created(self):
        SQL = 'SELECT first_name, age FROM citizens'
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.execute_sql(SQL)

    def test_execute_sql_defaults(self):
        from google.cloud.spanner import session as MUT
        from google.cloud._testing import _Monkey

        SQL = 'SELECT first_name, age FROM citizens'
        TOKEN = b'DEADBEEF'
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        _executed_sql_with = []
        expected = object()

        class _Snapshot(object):

            def __init__(self, session, **kwargs):
                self._session = session
                self._kwargs = kwargs.copy()

            def execute_sql(
                    self, sql, params=None, param_types=None, query_mode=None,
                    resume_token=None):
                _executed_sql_with.append(
                    (sql, params, param_types, query_mode, resume_token))
                return expected

        with _Monkey(MUT, Snapshot=_Snapshot):
            found = session.execute_sql(SQL, resume_token=TOKEN)

        self.assertIs(found, expected)

        self.assertEqual(len(_executed_sql_with), 1)
        sql, params, param_types, query_mode, token = _executed_sql_with[0]

        self.assertEqual(sql, SQL)
        self.assertEqual(params, None)
        self.assertEqual(param_types, None)
        self.assertEqual(query_mode, None)
        self.assertEqual(token, TOKEN)

    def test_batch_not_created(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.batch()

    def test_batch_created(self):
        from google.cloud.spanner.batch import Batch

        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        batch = session.batch()

        self.assertIsInstance(batch, Batch)
        self.assertTrue(batch._session is session)

    def test_transaction_not_created(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.transaction()

    def test_transaction_created(self):
        from google.cloud.spanner.transaction import Transaction

        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        transaction = session.transaction()

        self.assertIsInstance(transaction, Transaction)
        self.assertTrue(transaction._session is session)
        self.assertTrue(session._transaction is transaction)

    def test_transaction_w_existing_txn(self):
        database = _Database(self.DATABASE_NAME)
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        existing = session.transaction()
        another = session.transaction()  # invalidates existing txn

        self.assertTrue(session._transaction is another)
        self.assertTrue(existing._rolled_back)

    def test_retry_transaction_w_commit_error_txn_already_begun(self):
        from google.gax.errors import GaxError
        from google.cloud.spanner.transaction import Transaction

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        gax_api = _SpannerApi(
            _commit_error=True,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'
        begun_txn = session._transaction = Transaction(session)
        begun_txn._id = b'FACEDACE'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        with self.assertRaises(GaxError):
            session.run_in_transaction(unit_of_work)

        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIs(txn, begun_txn)
        self.assertEqual(txn.committed, None)
        self.assertEqual(args, ())
        self.assertEqual(kw, {})

    def test_run_in_transaction_callback_raises_abort(self):
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud.spanner.transaction import Transaction

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _rollback_response=None,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        class Testing(Exception):
            pass

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)
            raise Testing()

        with self.assertRaises(Testing):
            session.run_in_transaction(unit_of_work)

        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertIsNone(txn.committed)
        self.assertTrue(txn._rolled_back)
        self.assertEqual(args, ())
        self.assertEqual(kw, {})

    def test_run_in_transaction_w_args_w_kwargs_wo_abort(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.transaction import Transaction

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_response=response,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        committed = session.run_in_transaction(
            unit_of_work, 'abc', some_arg='def')

        self.assertEqual(committed, now)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertEqual(txn.committed, committed)
        self.assertEqual(args, ('abc',))
        self.assertEqual(kw, {'some_arg': 'def'})

    def test_run_in_transaction_w_abort_no_retry_metadata(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.transaction import Transaction

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_abort_count=1,
            _commit_response=response,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        committed = session.run_in_transaction(
            unit_of_work, 'abc', some_arg='def')

        self.assertEqual(committed, now)
        self.assertEqual(len(called_with), 2)
        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            if index == 1:
                self.assertEqual(txn.committed, committed)
            else:
                self.assertIsNone(txn.committed)
            self.assertEqual(args, ('abc',))
            self.assertEqual(kw, {'some_arg': 'def'})

    def test_run_in_transaction_w_abort_w_retry_metadata(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.transaction import Transaction
        from google.cloud.spanner import session as MUT
        from google.cloud._testing import _Monkey

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        RETRY_SECONDS = 12
        RETRY_NANOS = 3456
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_abort_count=1,
            _commit_abort_retry_seconds=RETRY_SECONDS,
            _commit_abort_retry_nanos=RETRY_NANOS,
            _commit_response=response,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        time_module = _FauxTimeModule()

        with _Monkey(MUT, time=time_module):
            committed = session.run_in_transaction(
                unit_of_work, 'abc', some_arg='def')

        self.assertEqual(time_module._slept,
                         RETRY_SECONDS + RETRY_NANOS / 1.0e9)
        self.assertEqual(committed, now)
        self.assertEqual(len(called_with), 2)
        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            if index == 1:
                self.assertEqual(txn.committed, committed)
            else:
                self.assertIsNone(txn.committed)
            self.assertEqual(args, ('abc',))
            self.assertEqual(kw, {'some_arg': 'def'})

    def test_run_in_transaction_w_callback_raises_abort_wo_metadata(self):
        import datetime
        from google.gax.errors import GaxError
        from grpc import StatusCode
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.transaction import Transaction
        from google.cloud.spanner import session as MUT
        from google.cloud._testing import _Monkey

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        RETRY_SECONDS = 1
        RETRY_NANOS = 3456
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_abort_retry_seconds=RETRY_SECONDS,
            _commit_abort_retry_nanos=RETRY_NANOS,
            _commit_response=response,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            if len(called_with) < 2:
                grpc_error = gax_api._make_grpc_error(
                    StatusCode.ABORTED,
                    trailing=gax_api._trailing_metadata())
                raise GaxError('conflict', grpc_error)
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        time_module = _FauxTimeModule()

        with _Monkey(MUT, time=time_module):
            committed = session.run_in_transaction(unit_of_work)

        self.assertEqual(committed, now)
        self.assertEqual(time_module._slept,
                         RETRY_SECONDS + RETRY_NANOS / 1.0e9)
        self.assertEqual(len(called_with), 2)
        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            if index == 0:
                self.assertIsNone(txn.committed)
            else:
                self.assertEqual(txn.committed, now)
            self.assertEqual(args, ())
            self.assertEqual(kw, {})

    def test_run_in_transaction_w_abort_w_retry_metadata_deadline(self):
        import datetime
        from google.gax.errors import GaxError
        from google.gax.grpc import exc_to_code
        from grpc import StatusCode
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner.transaction import Transaction
        from google.cloud.spanner import session as MUT
        from google.cloud._testing import _Monkey

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        RETRY_SECONDS = 1
        RETRY_NANOS = 3456
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_abort_count=1,
            _commit_abort_retry_seconds=RETRY_SECONDS,
            _commit_abort_retry_nanos=RETRY_NANOS,
            _commit_response=response,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        time_module = _FauxTimeModule()

        with _Monkey(MUT, time=time_module):
            with self.assertRaises(GaxError) as exc:
                session.run_in_transaction(
                    unit_of_work, 'abc', some_arg='def', timeout_secs=0.01)

        self.assertEqual(exc_to_code(exc.exception.cause), StatusCode.ABORTED)
        self.assertIsNone(time_module._slept)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertIsNone(txn.committed)
        self.assertEqual(args, ('abc',))
        self.assertEqual(kw, {'some_arg': 'def'})

    def test_run_in_transaction_w_timeout(self):
        from google.gax.errors import GaxError
        from google.gax.grpc import exc_to_code
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from grpc import StatusCode
        from google.cloud.spanner.transaction import Transaction

        TABLE_NAME = 'citizens'
        COLUMNS = ['email', 'first_name', 'last_name', 'age']
        VALUES = [
            ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
            ['bharney@example.com', 'Bharney', 'Rhubble', 31],
        ]
        TRANSACTION_ID = b'FACEDACE'
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        gax_api = _SpannerApi(
            _begin_transaction_response=transaction_pb,
            _commit_abort_count=1e6,
        )
        database = _Database(self.DATABASE_NAME)
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = 'DEADBEEF'

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        with self.assertRaises(GaxError) as exc:
            session.run_in_transaction(unit_of_work, timeout_secs=0.01)

        self.assertEqual(exc_to_code(exc.exception.cause), StatusCode.ABORTED)

        self.assertGreater(len(called_with), 1)
        for txn, args, kw in called_with:
            self.assertIsInstance(txn, Transaction)
            self.assertIsNone(txn.committed)
            self.assertEqual(args, ())
            self.assertEqual(kw, {})


class _Database(object):

    def __init__(self, name):
        self.name = name


class _SpannerApi(_GAXBaseAPI):

    _commit_abort_count = 0
    _commit_abort_retry_seconds = None
    _commit_abort_retry_nanos = None
    _random_gax_error = _commit_error = False

    def create_session(self, database, options=None):
        from google.gax.errors import GaxError

        self._create_session_called_with = database, options
        if self._random_gax_error:
            raise GaxError('error')
        return self._create_session_response

    def get_session(self, name, options=None):
        from google.gax.errors import GaxError

        self._get_session_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._get_session_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())

    def delete_session(self, name, options=None):
        from google.gax.errors import GaxError

        self._delete_session_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        if not self._delete_session_ok:
            raise GaxError('miss', self._make_grpc_not_found())

    def begin_transaction(self, session, options_, options=None):
        self._begun = (session, options_, options)
        return self._begin_transaction_response

    def _trailing_metadata(self):
        from google.protobuf.duration_pb2 import Duration
        from google.rpc.error_details_pb2 import RetryInfo
        from grpc._common import cygrpc_metadata

        if self._commit_abort_retry_nanos is None:
            return cygrpc_metadata(())
        retry_info = RetryInfo(
            retry_delay=Duration(
                seconds=self._commit_abort_retry_seconds,
                nanos=self._commit_abort_retry_nanos))
        return cygrpc_metadata([
            ('google.rpc.retryinfo-bin', retry_info.SerializeToString())])

    def commit(self, session, mutations,
               transaction_id='', single_use_transaction=None, options=None):
        from grpc import StatusCode
        from google.gax.errors import GaxError

        assert single_use_transaction is None
        self._committed = (session, mutations, transaction_id, options)
        if self._commit_error:
            raise GaxError('error', self._make_grpc_error(StatusCode.UNKNOWN))
        if self._commit_abort_count > 0:
            self._commit_abort_count -= 1
            grpc_error = self._make_grpc_error(
                StatusCode.ABORTED, trailing=self._trailing_metadata())
            raise GaxError('conflict', grpc_error)
        return self._commit_response

    def rollback(self, session, transaction_id, options=None):
        self._rolled_back = (session, transaction_id, options)
        return self._rollback_response


class _SessionPB(object):

    def __init__(self, name):
        self.name = name


class _FauxTimeModule(object):

    _slept = None

    def time(self):
        import time
        return time.time()

    def sleep(self, seconds):
        self._slept = seconds
