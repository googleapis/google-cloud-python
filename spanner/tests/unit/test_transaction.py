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


TABLE_NAME = 'citizens'
COLUMNS = ['email', 'first_name', 'last_name', 'age']
VALUES = [
    ['phred@exammple.com', 'Phred', 'Phlyntstone', 32],
    ['bharney@example.com', 'Bharney', 'Rhubble', 31],
]


class TestTransaction(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID
    TRANSACTION_ID = b'DEADBEEF'

    def _getTargetClass(self):
        from google.cloud.spanner.transaction import Transaction

        return Transaction

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        session = _Session()
        transaction = self._make_one(session)
        self.assertTrue(transaction._session is session)
        self.assertIsNone(transaction._id)
        self.assertIsNone(transaction.committed)
        self.assertEqual(transaction._rolled_back, False)

    def test__check_state_not_begun(self):
        session = _Session()
        transaction = self._make_one(session)
        with self.assertRaises(ValueError):
            transaction._check_state()

    def test__check_state_already_committed(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = b'DEADBEEF'
        transaction.committed = object()
        with self.assertRaises(ValueError):
            transaction._check_state()

    def test__check_state_already_rolled_back(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = b'DEADBEEF'
        transaction._rolled_back = True
        with self.assertRaises(ValueError):
            transaction._check_state()

    def test__check_state_ok(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = b'DEADBEEF'
        transaction._check_state()  # does not raise

    def test__make_txn_selector(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        selector = transaction._make_txn_selector()
        self.assertEqual(selector.id, self.TRANSACTION_ID)

    def test_begin_already_begun(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        with self.assertRaises(ValueError):
            transaction.begin()

    def test_begin_already_rolled_back(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._rolled_back = True
        with self.assertRaises(ValueError):
            transaction.begin()

    def test_begin_already_committed(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction.committed = object()
        with self.assertRaises(ValueError):
            transaction.begin()

    def test_begin_w_gax_error(self):
        from google.gax.errors import GaxError

        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _random_gax_error=True)
        session = _Session(database)
        transaction = self._make_one(session)

        with self.assertRaises(GaxError):
            transaction.begin()

        session_id, txn_options, options = api._begun
        self.assertEqual(session_id, session.name)
        self.assertTrue(txn_options.HasField('read_write'))
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_begin_ok(self):
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)

        transaction_pb = TransactionPB(id=self.TRANSACTION_ID)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _begin_transaction_response=transaction_pb)
        session = _Session(database)
        transaction = self._make_one(session)

        txn_id = transaction.begin()

        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(transaction._id, self.TRANSACTION_ID)

        session_id, txn_options, options = api._begun
        self.assertEqual(session_id, session.name)
        self.assertTrue(txn_options.HasField('read_write'))
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_rollback_not_begun(self):
        session = _Session()
        transaction = self._make_one(session)
        with self.assertRaises(ValueError):
            transaction.rollback()

    def test_rollback_already_committed(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.committed = object()
        with self.assertRaises(ValueError):
            transaction.rollback()

    def test_rollback_already_rolled_back(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction._rolled_back = True
        with self.assertRaises(ValueError):
            transaction.rollback()

    def test_rollback_w_gax_error(self):
        from google.gax.errors import GaxError

        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _random_gax_error=True)
        session = _Session(database)
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.insert(TABLE_NAME, COLUMNS, VALUES)

        with self.assertRaises(GaxError):
            transaction.rollback()

        self.assertFalse(transaction._rolled_back)

        session_id, txn_id, options = api._rolled_back
        self.assertEqual(session_id, session.name)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_rollback_ok(self):
        from google.protobuf.empty_pb2 import Empty

        empty_pb = Empty()
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _rollback_response=empty_pb)
        session = _Session(database)
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.replace(TABLE_NAME, COLUMNS, VALUES)

        transaction.rollback()

        self.assertTrue(transaction._rolled_back)

        session_id, txn_id, options = api._rolled_back
        self.assertEqual(session_id, session.name)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_commit_not_begun(self):
        session = _Session()
        transaction = self._make_one(session)
        with self.assertRaises(ValueError):
            transaction.commit()

    def test_commit_already_committed(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.committed = object()
        with self.assertRaises(ValueError):
            transaction.commit()

    def test_commit_already_rolled_back(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction._rolled_back = True
        with self.assertRaises(ValueError):
            transaction.commit()

    def test_commit_no_mutations(self):
        session = _Session()
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        with self.assertRaises(ValueError):
            transaction.commit()

    def test_commit_w_gax_error(self):
        from google.gax.errors import GaxError

        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _random_gax_error=True)
        session = _Session(database)
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.replace(TABLE_NAME, COLUMNS, VALUES)

        with self.assertRaises(GaxError):
            transaction.commit()

        self.assertIsNone(transaction.committed)

        session_id, mutations, txn_id, options = api._committed
        self.assertEqual(session_id, session.name)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(mutations, transaction._mutations)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_commit_ok(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.spanner.keyset import KeySet
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        keys = [[0], [1], [2]]
        keyset = KeySet(keys=keys)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _commit_response=response)
        session = _Session(database)
        transaction = self._make_one(session)
        transaction._id = self.TRANSACTION_ID
        transaction.delete(TABLE_NAME, keyset)

        transaction.commit()

        self.assertEqual(transaction.committed, now)

        session_id, mutations, txn_id, options = api._committed
        self.assertEqual(session_id, session.name)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(mutations, transaction._mutations)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_context_mgr_success(self):
        import datetime
        from google.cloud.proto.spanner.v1.spanner_pb2 import CommitResponse
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)
        from google.cloud._helpers import UTC
        from google.cloud._helpers import _datetime_to_pb_timestamp

        transaction_pb = TransactionPB(id=self.TRANSACTION_ID)
        database = _Database()
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        now_pb = _datetime_to_pb_timestamp(now)
        response = CommitResponse(commit_timestamp=now_pb)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _begin_transaction_response=transaction_pb,
            _commit_response=response)
        session = _Session(database)
        transaction = self._make_one(session)

        with transaction:
            transaction.insert(TABLE_NAME, COLUMNS, VALUES)

        self.assertEqual(transaction.committed, now)

        session_id, mutations, txn_id, options = api._committed
        self.assertEqual(session_id, self.SESSION_NAME)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(mutations, transaction._mutations)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_context_mgr_failure(self):
        from google.protobuf.empty_pb2 import Empty
        empty_pb = Empty()
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            Transaction as TransactionPB)

        transaction_pb = TransactionPB(id=self.TRANSACTION_ID)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _begin_transaction_response=transaction_pb,
            _rollback_response=empty_pb)
        session = _Session(database)
        transaction = self._make_one(session)

        with self.assertRaises(Exception):
            with transaction:
                transaction.insert(TABLE_NAME, COLUMNS, VALUES)
                raise Exception("bail out")

        self.assertEqual(transaction.committed, None)
        self.assertTrue(transaction._rolled_back)
        self.assertEqual(len(transaction._mutations), 1)

        self.assertEqual(api._committed, None)

        session_id, txn_id, options = api._rolled_back
        self.assertEqual(session_id, session.name)
        self.assertEqual(txn_id, self.TRANSACTION_ID)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])


class _Database(object):
    name = 'testing'


class _Session(object):

    def __init__(self, database=None, name=TestTransaction.SESSION_NAME):
        self._database = database
        self.name = name


class _FauxSpannerAPI(_GAXBaseAPI):

    _committed = None

    def begin_transaction(self, session, options_, options=None):
        from google.gax.errors import GaxError

        self._begun = (session, options_, options)
        if self._random_gax_error:
            raise GaxError('error')
        return self._begin_transaction_response

    def rollback(self, session, transaction_id, options=None):
        from google.gax.errors import GaxError

        self._rolled_back = (session, transaction_id, options)
        if self._random_gax_error:
            raise GaxError('error')
        return self._rollback_response

    def commit(self, session, mutations,
               transaction_id='', single_use_transaction=None, options=None):
        from google.gax.errors import GaxError

        assert single_use_transaction is None
        self._committed = (session, mutations, transaction_id, options)
        if self._random_gax_error:
            raise GaxError('error')
        return self._commit_response
