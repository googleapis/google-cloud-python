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
SQL_QUERY = """\
SELECT first_name, last_name, age FROM citizens ORDER BY age"""
SQL_QUERY_WITH_PARAM = """
SELECT first_name, last_name, email FROM citizens WHERE age <= @max_age"""
PARAMS = {'max_age': 30}
PARAM_TYPES = {'max_age': 'INT64'}
SQL_QUERY_WITH_BYTES_PARAM = """\
SELECT image_name FROM images WHERE @bytes IN image_data"""
PARAMS_WITH_BYTES = {'bytes': b'DEADBEEF'}


class Test_SnapshotBase(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner.snapshot import _SnapshotBase

        return _SnapshotBase

    def _make_one(self, session):
        return self._getTargetClass()(session)

    def _makeDerived(self, session):

        class _Derived(self._getTargetClass()):

            def _make_txn_selector(self):
                from google.cloud.proto.spanner.v1.transaction_pb2 import (
                    TransactionOptions, TransactionSelector)

                options = TransactionOptions(
                    read_only=TransactionOptions.ReadOnly(strong=True))
                return TransactionSelector(single_use=options)

        return _Derived(session)

    def test_ctor(self):
        session = _Session()
        base = self._make_one(session)
        self.assertTrue(base._session is session)

    def test__make_txn_selector_virtual(self):
        session = _Session()
        base = self._make_one(session)
        with self.assertRaises(NotImplementedError):
            base._make_txn_selector()

    def test_read_grpc_error(self):
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            TransactionSelector)
        from google.gax.errors import GaxError
        from google.cloud.spanner.keyset import KeySet

        KEYSET = KeySet(all_=True)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _random_gax_error=True)
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(GaxError):
            derived.read(TABLE_NAME, COLUMNS, KEYSET)

        (r_session, table, columns, key_set, transaction, index,
         limit, resume_token, options) = api._streaming_read_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertTrue(transaction.single_use.read_only.strong)
        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(key_set, KEYSET.to_pb())
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertEqual(index, '')
        self.assertEqual(limit, 0)
        self.assertEqual(resume_token, b'')
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_read_normal(self):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.proto.spanner.v1.result_set_pb2 import (
            PartialResultSet, ResultSetMetadata, ResultSetStats)
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            TransactionSelector)
        from google.cloud.proto.spanner.v1.type_pb2 import Type, StructType
        from google.cloud.proto.spanner.v1.type_pb2 import STRING, INT64
        from google.cloud.spanner.keyset import KeySet
        from google.cloud.spanner._helpers import _make_value_pb

        VALUES = [
            [u'bharney', 31],
            [u'phred', 32],
        ]
        VALUE_PBS = [
            [_make_value_pb(item) for item in row]
            for row in VALUES
        ]
        struct_type_pb = StructType(fields=[
            StructType.Field(name='name', type=Type(code=STRING)),
            StructType.Field(name='age', type=Type(code=INT64)),
        ])
        metadata_pb = ResultSetMetadata(row_type=struct_type_pb)
        stats_pb = ResultSetStats(
            query_stats=Struct(fields={
                'rows_returned': _make_value_pb(2),
            }))
        result_sets = [
            PartialResultSet(values=VALUE_PBS[0], metadata=metadata_pb),
            PartialResultSet(values=VALUE_PBS[1], stats=stats_pb),
        ]
        KEYS = ['bharney@example.com', 'phred@example.com']
        KEYSET = KeySet(keys=KEYS)
        INDEX = 'email-address-index'
        LIMIT = 20
        TOKEN = b'DEADBEEF'
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _streaming_read_response=_MockCancellableIterator(*result_sets))
        session = _Session(database)
        derived = self._makeDerived(session)

        result_set = derived.read(
            TABLE_NAME, COLUMNS, KEYSET,
            index=INDEX, limit=LIMIT, resume_token=TOKEN)

        result_set.consume_all()
        self.assertEqual(list(result_set.rows), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        (r_session, table, columns, key_set, transaction, index,
         limit, resume_token, options) = api._streaming_read_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(key_set, KEYSET.to_pb())
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertTrue(transaction.single_use.read_only.strong)
        self.assertEqual(index, INDEX)
        self.assertEqual(limit, LIMIT)
        self.assertEqual(resume_token, TOKEN)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_execute_sql_grpc_error(self):
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            TransactionSelector)
        from google.gax.errors import GaxError

        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _random_gax_error=True)
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(GaxError):
            derived.execute_sql(SQL_QUERY)

        (r_session, sql, transaction, params, param_types,
         resume_token, query_mode, options) = api._executed_streaming_sql_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(sql, SQL_QUERY)
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertTrue(transaction.single_use.read_only.strong)
        self.assertEqual(params, None)
        self.assertEqual(param_types, None)
        self.assertEqual(resume_token, b'')
        self.assertEqual(query_mode, None)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])

    def test_execute_sql_w_params_wo_param_types(self):
        database = _Database()
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(ValueError):
            derived.execute_sql(SQL_QUERY_WITH_PARAM, PARAMS)

    def test_execute_sql_normal(self):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.proto.spanner.v1.result_set_pb2 import (
            PartialResultSet, ResultSetMetadata, ResultSetStats)
        from google.cloud.proto.spanner.v1.transaction_pb2 import (
            TransactionSelector)
        from google.cloud.proto.spanner.v1.type_pb2 import Type, StructType
        from google.cloud.proto.spanner.v1.type_pb2 import STRING, INT64
        from google.cloud.spanner._helpers import _make_value_pb

        VALUES = [
            [u'bharney', u'rhubbyl', 31],
            [u'phred', u'phlyntstone', 32],
        ]
        VALUE_PBS = [
            [_make_value_pb(item) for item in row]
            for row in VALUES
        ]
        MODE = 2  # PROFILE
        TOKEN = b'DEADBEEF'
        struct_type_pb = StructType(fields=[
            StructType.Field(name='first_name', type=Type(code=STRING)),
            StructType.Field(name='last_name', type=Type(code=STRING)),
            StructType.Field(name='age', type=Type(code=INT64)),
        ])
        metadata_pb = ResultSetMetadata(row_type=struct_type_pb)
        stats_pb = ResultSetStats(
            query_stats=Struct(fields={
                'rows_returned': _make_value_pb(2),
            }))
        result_sets = [
            PartialResultSet(values=VALUE_PBS[0], metadata=metadata_pb),
            PartialResultSet(values=VALUE_PBS[1], stats=stats_pb),
        ]
        iterator = _MockCancellableIterator(*result_sets)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _execute_streaming_sql_response=iterator)
        session = _Session(database)
        derived = self._makeDerived(session)

        result_set = derived.execute_sql(
            SQL_QUERY_WITH_PARAM, PARAMS, PARAM_TYPES,
            query_mode=MODE, resume_token=TOKEN)

        result_set.consume_all()
        self.assertEqual(list(result_set.rows), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        (r_session, sql, transaction, params, param_types,
         resume_token, query_mode, options) = api._executed_streaming_sql_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(sql, SQL_QUERY_WITH_PARAM)
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertTrue(transaction.single_use.read_only.strong)
        expected_params = Struct(fields={
            key: _make_value_pb(value) for (key, value) in PARAMS.items()})
        self.assertEqual(params, expected_params)
        self.assertEqual(param_types, PARAM_TYPES)
        self.assertEqual(query_mode, MODE)
        self.assertEqual(resume_token, TOKEN)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', database.name)])


class _MockCancellableIterator(object):

    cancel_calls = 0

    def __init__(self, *values):
        self.iter_values = iter(values)

    def next(self):
        return next(self.iter_values)

    def __next__(self):  # pragma: NO COVER Py3k
        return self.next()


class TestSnapshot(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner.snapshot import Snapshot
        return Snapshot

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _makeTimestamp(self):
        import datetime
        from google.cloud._helpers import UTC

        return datetime.datetime.utcnow().replace(tzinfo=UTC)

    def _makeDuration(self, seconds=1, microseconds=0):
        import datetime

        return datetime.timedelta(seconds=seconds, microseconds=microseconds)

    def test_ctor_defaults(self):
        session = _Session()
        snapshot = self._make_one(session)
        self.assertTrue(snapshot._session is session)
        self.assertTrue(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)

    def test_ctor_w_multiple_options(self):
        timestamp = self._makeTimestamp()
        duration = self._makeDuration()
        session = _Session()

        with self.assertRaises(ValueError):
            self._make_one(
                session, read_timestamp=timestamp, max_staleness=duration)

    def test_ctor_w_read_timestamp(self):
        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, read_timestamp=timestamp)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertEqual(snapshot._read_timestamp, timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)

    def test_ctor_w_min_read_timestamp(self):
        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, min_read_timestamp=timestamp)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertEqual(snapshot._min_read_timestamp, timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)

    def test_ctor_w_max_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(session, max_staleness=duration)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertEqual(snapshot._max_staleness, duration)
        self.assertIsNone(snapshot._exact_staleness)

    def test_ctor_w_exact_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertEqual(snapshot._exact_staleness, duration)

    def test__make_txn_selector_strong(self):
        session = _Session()
        snapshot = self._make_one(session)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertTrue(options.read_only.strong)

    def test__make_txn_selector_w_read_timestamp(self):
        from google.cloud._helpers import _pb_timestamp_to_datetime

        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, read_timestamp=timestamp)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(
            _pb_timestamp_to_datetime(options.read_only.read_timestamp),
            timestamp)

    def test__make_txn_selector_w_min_read_timestamp(self):
        from google.cloud._helpers import _pb_timestamp_to_datetime

        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, min_read_timestamp=timestamp)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(
            _pb_timestamp_to_datetime(options.read_only.min_read_timestamp),
            timestamp)

    def test__make_txn_selector_w_max_staleness(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(session, max_staleness=duration)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(options.read_only.max_staleness.seconds, 3)
        self.assertEqual(options.read_only.max_staleness.nanos, 123456000)

    def test__make_txn_selector_w_exact_staleness(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(options.read_only.exact_staleness.seconds, 3)
        self.assertEqual(options.read_only.exact_staleness.nanos, 123456000)


class _Session(object):

    def __init__(self, database=None, name=TestSnapshot.SESSION_NAME):
        self._database = database
        self.name = name


class _Database(object):
    name = 'testing'


class _FauxSpannerAPI(_GAXBaseAPI):

    _read_with = None

    # pylint: disable=too-many-arguments
    def streaming_read(self, session, table, columns, key_set,
                       transaction=None, index='', limit=0,
                       resume_token='', options=None):
        from google.gax.errors import GaxError

        self._streaming_read_with = (
            session, table, columns, key_set, transaction, index,
            limit, resume_token, options)
        if self._random_gax_error:
            raise GaxError('error')
        return self._streaming_read_response
    # pylint: enable=too-many-arguments

    def execute_streaming_sql(self, session, sql, transaction=None,
                              params=None, param_types=None,
                              resume_token='', query_mode=None, options=None):
        from google.gax.errors import GaxError

        self._executed_streaming_sql_with = (
            session, sql, transaction, params, param_types, resume_token,
            query_mode, options)
        if self._random_gax_error:
            raise GaxError('error')
        return self._execute_streaming_sql_response
