# Copyright 2016 Google LLC All rights reserved.
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
import google.api_core.gapic_v1.method
import mock


def _make_rpc_error(error_cls, trailing_metadata=None):
    import grpc

    grpc_error = mock.create_autospec(grpc.Call, instance=True)
    grpc_error.trailing_metadata.return_value = trailing_metadata
    return error_cls("error", errors=(grpc_error,))


class TestSession(unittest.TestCase):

    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database-id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session-id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner_v1.session import Session

        return Session

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    @staticmethod
    def _make_database(name=DATABASE_NAME):
        from google.cloud.spanner_v1.database import Database

        database = mock.create_autospec(Database, instance=True)
        database.name = name
        return database

    @staticmethod
    def _make_session_pb(name, labels=None):
        from google.cloud.spanner_v1.proto.spanner_pb2 import Session

        return Session(name=name, labels=labels)

    def _make_spanner_api(self):
        from google.cloud.spanner_v1.gapic.spanner_client import SpannerClient

        return mock.Mock(autospec=SpannerClient, instance=True)

    def test_constructor_wo_labels(self):
        database = self._make_database()
        session = self._make_one(database)
        self.assertIs(session.session_id, None)
        self.assertIs(session._database, database)
        self.assertEqual(session.labels, {})

    def test_constructor_w_labels(self):
        database = self._make_database()
        labels = {"foo": "bar"}
        session = self._make_one(database, labels=labels)
        self.assertIs(session.session_id, None)
        self.assertIs(session._database, database)
        self.assertEqual(session.labels, labels)

    def test___lt___(self):
        database = self._make_database()
        lhs = self._make_one(database)
        lhs._session_id = b"123"
        rhs = self._make_one(database)
        rhs._session_id = b"234"
        self.assertTrue(lhs < rhs)

    def test_name_property_wo_session_id(self):
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            (session.name)

    def test_name_property_w_session_id(self):
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = self.SESSION_ID
        self.assertEqual(session.name, self.SESSION_NAME)

    def test_create_w_session_id(self):
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(ValueError):
            session.create()

    def test_create_ok(self):
        session_pb = self._make_session_pb(self.SESSION_NAME)
        gax_api = self._make_spanner_api()
        gax_api.create_session.return_value = session_pb
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)

        session.create()

        self.assertEqual(session.session_id, self.SESSION_ID)

        gax_api.create_session.assert_called_once_with(
            database.name, metadata=[("google-cloud-resource-prefix", database.name)]
        )

    def test_create_w_labels(self):
        labels = {"foo": "bar"}
        session_pb = self._make_session_pb(self.SESSION_NAME, labels=labels)
        gax_api = self._make_spanner_api()
        gax_api.create_session.return_value = session_pb
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database, labels=labels)

        session.create()

        self.assertEqual(session.session_id, self.SESSION_ID)

        gax_api.create_session.assert_called_once_with(
            database.name,
            session={"labels": labels},
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_create_error(self):
        from google.api_core.exceptions import Unknown

        gax_api = self._make_spanner_api()
        gax_api.create_session.side_effect = Unknown("error")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)

        with self.assertRaises(Unknown):
            session.create()

    def test_exists_wo_session_id(self):
        database = self._make_database()
        session = self._make_one(database)
        self.assertFalse(session.exists())

    def test_exists_hit(self):
        session_pb = self._make_session_pb(self.SESSION_NAME)
        gax_api = self._make_spanner_api()
        gax_api.get_session.return_value = session_pb
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        self.assertTrue(session.exists())

        gax_api.get_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_exists_miss(self):
        from google.api_core.exceptions import NotFound

        gax_api = self._make_spanner_api()
        gax_api.get_session.side_effect = NotFound("testing")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        self.assertFalse(session.exists())

        gax_api.get_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_exists_error(self):
        from google.api_core.exceptions import Unknown

        gax_api = self._make_spanner_api()
        gax_api.get_session.side_effect = Unknown("testing")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(Unknown):
            session.exists()

        gax_api.get_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_delete_wo_session_id(self):
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.delete()

    def test_delete_hit(self):
        gax_api = self._make_spanner_api()
        gax_api.delete_session.return_value = None
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        session.delete()

        gax_api.delete_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_delete_miss(self):
        from google.cloud.exceptions import NotFound

        gax_api = self._make_spanner_api()
        gax_api.delete_session.side_effect = NotFound("testing")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(NotFound):
            session.delete()

        gax_api.delete_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_delete_error(self):
        from google.api_core.exceptions import Unknown

        gax_api = self._make_spanner_api()
        gax_api.delete_session.side_effect = Unknown("testing")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        with self.assertRaises(Unknown):
            session.delete()

        gax_api.delete_session.assert_called_once_with(
            self.SESSION_NAME,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_snapshot_not_created(self):
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.snapshot()

    def test_snapshot_created(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"  # emulate 'session.create()'

        snapshot = session.snapshot()

        self.assertIsInstance(snapshot, Snapshot)
        self.assertIs(snapshot._session, session)
        self.assertTrue(snapshot._strong)
        self.assertFalse(snapshot._multi_use)

    def test_snapshot_created_w_multi_use(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"  # emulate 'session.create()'

        snapshot = session.snapshot(multi_use=True)

        self.assertIsInstance(snapshot, Snapshot)
        self.assertTrue(snapshot._session is session)
        self.assertTrue(snapshot._strong)
        self.assertTrue(snapshot._multi_use)

    def test_read_not_created(self):
        from google.cloud.spanner_v1.keyset import KeySet

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        KEYS = ["bharney@example.com", "phred@example.com"]
        KEYSET = KeySet(keys=KEYS)
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.read(TABLE_NAME, COLUMNS, KEYSET)

    def test_read(self):
        from google.cloud.spanner_v1.keyset import KeySet

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        KEYS = ["bharney@example.com", "phred@example.com"]
        KEYSET = KeySet(keys=KEYS)
        INDEX = "email-address-index"
        LIMIT = 20
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        with mock.patch("google.cloud.spanner_v1.session.Snapshot") as snapshot:
            found = session.read(TABLE_NAME, COLUMNS, KEYSET, index=INDEX, limit=LIMIT)

        self.assertIs(found, snapshot().read.return_value)

        snapshot().read.assert_called_once_with(
            TABLE_NAME, COLUMNS, KEYSET, INDEX, LIMIT
        )

    def test_execute_sql_not_created(self):
        SQL = "SELECT first_name, age FROM citizens"
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.execute_sql(SQL)

    def test_execute_sql_defaults(self):
        SQL = "SELECT first_name, age FROM citizens"
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        with mock.patch("google.cloud.spanner_v1.session.Snapshot") as snapshot:
            found = session.execute_sql(SQL)

        self.assertIs(found, snapshot().execute_sql.return_value)

        snapshot().execute_sql.assert_called_once_with(
            SQL,
            None,
            None,
            None,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            retry=google.api_core.gapic_v1.method.DEFAULT,
        )

    def test_execute_sql_non_default_retry(self):
        from google.protobuf.struct_pb2 import Struct, Value
        from google.cloud.spanner_v1.proto.type_pb2 import STRING

        SQL = "SELECT first_name, age FROM citizens"
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        params = Struct(fields={"foo": Value(string_value="bar")})
        param_types = {"foo": STRING}

        with mock.patch("google.cloud.spanner_v1.session.Snapshot") as snapshot:
            found = session.execute_sql(
                SQL, params, param_types, "PLAN", retry=None, timeout=None
            )

        self.assertIs(found, snapshot().execute_sql.return_value)

        snapshot().execute_sql.assert_called_once_with(
            SQL, params, param_types, "PLAN", timeout=None, retry=None
        )

    def test_execute_sql_explicit(self):
        from google.protobuf.struct_pb2 import Struct, Value
        from google.cloud.spanner_v1.proto.type_pb2 import STRING

        SQL = "SELECT first_name, age FROM citizens"
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        params = Struct(fields={"foo": Value(string_value="bar")})
        param_types = {"foo": STRING}

        with mock.patch("google.cloud.spanner_v1.session.Snapshot") as snapshot:
            found = session.execute_sql(SQL, params, param_types, "PLAN")

        self.assertIs(found, snapshot().execute_sql.return_value)

        snapshot().execute_sql.assert_called_once_with(
            SQL,
            params,
            param_types,
            "PLAN",
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            retry=google.api_core.gapic_v1.method.DEFAULT,
        )

    def test_batch_not_created(self):
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.batch()

    def test_batch_created(self):
        from google.cloud.spanner_v1.batch import Batch

        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        batch = session.batch()

        self.assertIsInstance(batch, Batch)
        self.assertIs(batch._session, session)

    def test_transaction_not_created(self):
        database = self._make_database()
        session = self._make_one(database)

        with self.assertRaises(ValueError):
            session.transaction()

    def test_transaction_created(self):
        from google.cloud.spanner_v1.transaction import Transaction

        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        transaction = session.transaction()

        self.assertIsInstance(transaction, Transaction)
        self.assertIs(transaction._session, session)
        self.assertIs(session._transaction, transaction)

    def test_transaction_w_existing_txn(self):
        database = self._make_database()
        session = self._make_one(database)
        session._session_id = "DEADBEEF"

        existing = session.transaction()
        another = session.transaction()  # invalidates existing txn

        self.assertIs(session._transaction, another)
        self.assertTrue(existing._rolled_back)

    def test_run_in_transaction_callback_raises_non_gax_error(self):
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.rollback.return_value = None
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        class Testing(Exception):
            pass

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)
            raise Testing()

        with self.assertRaises(Testing):
            session.run_in_transaction(unit_of_work)

        self.assertIsNone(session._transaction)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertIsNone(txn.committed)
        self.assertTrue(txn._rolled_back)
        self.assertEqual(args, ())
        self.assertEqual(kw, {})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        gax_api.begin_transaction.assert_called_once_with(
            self.SESSION_NAME,
            expected_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        gax_api.rollback.assert_called_once_with(
            self.SESSION_NAME,
            TRANSACTION_ID,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_run_in_transaction_callback_raises_non_abort_rpc_error(self):
        from google.api_core.exceptions import Cancelled
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.rollback.return_value = None
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)
            raise Cancelled("error")

        with self.assertRaises(Cancelled):
            session.run_in_transaction(unit_of_work)

        self.assertIsNone(session._transaction)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertIsNone(txn.committed)
        self.assertFalse(txn._rolled_back)
        self.assertEqual(args, ())
        self.assertEqual(kw, {})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        gax_api.begin_transaction.assert_called_once_with(
            self.SESSION_NAME,
            expected_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        gax_api.rollback.assert_not_called()

    def test_run_in_transaction_w_args_w_kwargs_wo_abort(self):
        import datetime
        from google.cloud.spanner_v1.proto.spanner_pb2 import CommitResponse
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.return_value = response
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)
            return 42

        return_value = session.run_in_transaction(unit_of_work, "abc", some_arg="def")

        self.assertIsNone(session._transaction)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertEqual(return_value, 42)
        self.assertEqual(args, ("abc",))
        self.assertEqual(kw, {"some_arg": "def"})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        gax_api.begin_transaction.assert_called_once_with(
            self.SESSION_NAME,
            expected_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        gax_api.commit.assert_called_once_with(
            self.SESSION_NAME,
            txn._mutations,
            transaction_id=TRANSACTION_ID,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_run_in_transaction_w_commit_error(self):
        from google.api_core.exceptions import Unknown
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        gax_api = self._make_spanner_api()
        gax_api.commit.side_effect = Unknown("error")
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID
        begun_txn = session._transaction = Transaction(session)
        begun_txn._transaction_id = TRANSACTION_ID

        assert session._transaction._transaction_id

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        with self.assertRaises(Unknown):
            session.run_in_transaction(unit_of_work)

        self.assertIsNone(session._transaction)
        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIs(txn, begun_txn)
        self.assertEqual(txn.committed, None)
        self.assertEqual(args, ())
        self.assertEqual(kw, {})

        gax_api.begin_transaction.assert_not_called()
        gax_api.commit.assert_called_once_with(
            self.SESSION_NAME,
            txn._mutations,
            transaction_id=TRANSACTION_ID,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_run_in_transaction_w_abort_no_retry_metadata(self):
        import datetime
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_v1.proto.spanner_pb2 import CommitResponse
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        aborted = _make_rpc_error(Aborted, trailing_metadata=[])
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.side_effect = [aborted, response]
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)
            return "answer"

        return_value = session.run_in_transaction(unit_of_work, "abc", some_arg="def")

        self.assertEqual(len(called_with), 2)
        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            self.assertEqual(return_value, "answer")
            self.assertEqual(args, ("abc",))
            self.assertEqual(kw, {"some_arg": "def"})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        self.assertEqual(
            gax_api.begin_transaction.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    expected_options,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )
        self.assertEqual(
            gax_api.commit.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    txn._mutations,
                    transaction_id=TRANSACTION_ID,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )

    def test_run_in_transaction_w_abort_w_retry_metadata(self):
        import datetime
        from google.api_core.exceptions import Aborted
        from google.protobuf.duration_pb2 import Duration
        from google.rpc.error_details_pb2 import RetryInfo
        from google.cloud.spanner_v1.proto.spanner_pb2 import CommitResponse
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        RETRY_SECONDS = 12
        RETRY_NANOS = 3456
        retry_info = RetryInfo(
            retry_delay=Duration(seconds=RETRY_SECONDS, nanos=RETRY_NANOS)
        )
        trailing_metadata = [
            ("google.rpc.retryinfo-bin", retry_info.SerializeToString())
        ]
        aborted = _make_rpc_error(Aborted, trailing_metadata=trailing_metadata)
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.side_effect = [aborted, response]
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        with mock.patch("time.sleep") as sleep_mock:
            session.run_in_transaction(unit_of_work, "abc", some_arg="def")

        sleep_mock.assert_called_once_with(RETRY_SECONDS + RETRY_NANOS / 1.0e9)
        self.assertEqual(len(called_with), 2)

        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            if index == 1:
                self.assertEqual(txn.committed, now)
            else:
                self.assertIsNone(txn.committed)
            self.assertEqual(args, ("abc",))
            self.assertEqual(kw, {"some_arg": "def"})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        self.assertEqual(
            gax_api.begin_transaction.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    expected_options,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )
        self.assertEqual(
            gax_api.commit.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    txn._mutations,
                    transaction_id=TRANSACTION_ID,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )

    def test_run_in_transaction_w_callback_raises_abort_wo_metadata(self):
        import datetime
        from google.api_core.exceptions import Aborted
        from google.protobuf.duration_pb2 import Duration
        from google.rpc.error_details_pb2 import RetryInfo
        from google.cloud.spanner_v1.proto.spanner_pb2 import CommitResponse
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        RETRY_SECONDS = 1
        RETRY_NANOS = 3456
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        retry_info = RetryInfo(
            retry_delay=Duration(seconds=RETRY_SECONDS, nanos=RETRY_NANOS)
        )
        trailing_metadata = [
            ("google.rpc.retryinfo-bin", retry_info.SerializeToString())
        ]
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.side_effect = [response]
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            if len(called_with) < 2:
                raise _make_rpc_error(Aborted, trailing_metadata)
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        with mock.patch("time.sleep") as sleep_mock:
            session.run_in_transaction(unit_of_work)

        sleep_mock.assert_called_once_with(RETRY_SECONDS + RETRY_NANOS / 1.0e9)
        self.assertEqual(len(called_with), 2)
        for index, (txn, args, kw) in enumerate(called_with):
            self.assertIsInstance(txn, Transaction)
            if index == 0:
                self.assertIsNone(txn.committed)
            else:
                self.assertEqual(txn.committed, now)
            self.assertEqual(args, ())
            self.assertEqual(kw, {})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        self.assertEqual(
            gax_api.begin_transaction.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    expected_options,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )
        gax_api.commit.assert_called_once_with(
            self.SESSION_NAME,
            txn._mutations,
            transaction_id=TRANSACTION_ID,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_run_in_transaction_w_abort_w_retry_metadata_deadline(self):
        import datetime
        from google.api_core.exceptions import Aborted
        from google.protobuf.duration_pb2 import Duration
        from google.rpc.error_details_pb2 import RetryInfo
        from google.cloud.spanner_v1.proto.spanner_pb2 import CommitResponse
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud.spanner_v1.transaction import Transaction
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        RETRY_SECONDS = 1
        RETRY_NANOS = 3456
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        retry_info = RetryInfo(
            retry_delay=Duration(seconds=RETRY_SECONDS, nanos=RETRY_NANOS)
        )
        trailing_metadata = [
            ("google.rpc.retryinfo-bin", retry_info.SerializeToString())
        ]
        aborted = _make_rpc_error(Aborted, trailing_metadata=trailing_metadata)
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.side_effect = [aborted, response]
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        # retry once w/ timeout_secs=1
        def _time(_results=[1, 1.5]):
            return _results.pop(0)

        with mock.patch("time.time", _time):
            with mock.patch("time.sleep") as sleep_mock:
                with self.assertRaises(Aborted):
                    session.run_in_transaction(unit_of_work, "abc", timeout_secs=1)

        sleep_mock.assert_not_called()

        self.assertEqual(len(called_with), 1)
        txn, args, kw = called_with[0]
        self.assertIsInstance(txn, Transaction)
        self.assertIsNone(txn.committed)
        self.assertEqual(args, ("abc",))
        self.assertEqual(kw, {})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        gax_api.begin_transaction.assert_called_once_with(
            self.SESSION_NAME,
            expected_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )
        gax_api.commit.assert_called_once_with(
            self.SESSION_NAME,
            txn._mutations,
            transaction_id=TRANSACTION_ID,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

    def test_run_in_transaction_w_timeout(self):
        from google.api_core.exceptions import Aborted
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )
        from google.cloud.spanner_v1.transaction import Transaction

        TABLE_NAME = "citizens"
        COLUMNS = ["email", "first_name", "last_name", "age"]
        VALUES = [
            ["phred@exammple.com", "Phred", "Phlyntstone", 32],
            ["bharney@example.com", "Bharney", "Rhubble", 31],
        ]
        TRANSACTION_ID = b"FACEDACE"
        transaction_pb = TransactionPB(id=TRANSACTION_ID)
        aborted = _make_rpc_error(Aborted, trailing_metadata=[])
        gax_api = self._make_spanner_api()
        gax_api.begin_transaction.return_value = transaction_pb
        gax_api.commit.side_effect = aborted
        database = self._make_database()
        database.spanner_api = gax_api
        session = self._make_one(database)
        session._session_id = self.SESSION_ID

        called_with = []

        def unit_of_work(txn, *args, **kw):
            called_with.append((txn, args, kw))
            txn.insert(TABLE_NAME, COLUMNS, VALUES)

        # retry once w/ timeout_secs=1
        def _time(_results=[1, 1.5, 2.5]):
            return _results.pop(0)

        with mock.patch("time.time", _time):
            with mock.patch("time.sleep") as sleep_mock:
                with self.assertRaises(Aborted):
                    session.run_in_transaction(unit_of_work, timeout_secs=1)

        sleep_mock.assert_not_called()

        self.assertEqual(len(called_with), 2)
        for txn, args, kw in called_with:
            self.assertIsInstance(txn, Transaction)
            self.assertIsNone(txn.committed)
            self.assertEqual(args, ())
            self.assertEqual(kw, {})

        expected_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        self.assertEqual(
            gax_api.begin_transaction.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    expected_options,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )
        self.assertEqual(
            gax_api.commit.call_args_list,
            [
                mock.call(
                    self.SESSION_NAME,
                    txn._mutations,
                    transaction_id=TRANSACTION_ID,
                    metadata=[("google-cloud-resource-prefix", database.name)],
                )
            ]
            * 2,
        )
