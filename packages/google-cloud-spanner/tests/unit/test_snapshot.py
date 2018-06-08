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

import mock


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
PARAMS_WITH_BYTES = {'bytes': b'FACEDACE'}
RESUME_TOKEN = b'DEADBEEF'
TXN_ID = b'DEAFBEAD'


class Test_restart_on_unavailable(unittest.TestCase):

    def _call_fut(self, restart):
        from google.cloud.spanner_v1.snapshot import _restart_on_unavailable

        return _restart_on_unavailable(restart)

    def _make_item(self, value, resume_token=b''):
        return mock.Mock(
            value=value, resume_token=resume_token,
            spec=['value', 'resume_token'])

    def test_iteration_w_empty_raw(self):
        raw = _MockIterator()
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), [])

    def test_iteration_w_non_empty_raw(self):
        ITEMS = (self._make_item(0), self._make_item(1))
        raw = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        restart.assert_called_once_with()

    def test_iteration_w_raw_w_resume_tken(self):
        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
            self._make_item(3),
        )
        raw = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        restart.assert_called_once_with()

    def test_iteration_w_raw_raising_unavailable_no_token(self):
        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(fail_after=True)
        after = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        self.assertEqual(
            restart.mock_calls,
            [mock.call(), mock.call(resume_token=b'')])

    def test_iteration_w_raw_raising_unavailable(self):
        FIRST = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
        )
        SECOND = (  # discarded after 503
            self._make_item(2),
        )
        LAST = (
            self._make_item(3),
        )
        before = _MockIterator(*(FIRST + SECOND), fail_after=True)
        after = _MockIterator(*LAST)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + LAST))
        self.assertEqual(
            restart.mock_calls,
            [mock.call(), mock.call(resume_token=RESUME_TOKEN)])

    def test_iteration_w_raw_raising_unavailable_after_token(self):
        FIRST = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
        )
        SECOND = (
            self._make_item(2),
            self._make_item(3),
        )
        before = _MockIterator(*FIRST, fail_after=True)
        after = _MockIterator(*SECOND)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(
            restart.mock_calls,
            [mock.call(), mock.call(resume_token=RESUME_TOKEN)])


class Test_SnapshotBase(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner_v1.snapshot import _SnapshotBase

        return _SnapshotBase

    def _make_one(self, session):
        return self._getTargetClass()(session)

    def _makeDerived(self, session):

        class _Derived(self._getTargetClass()):

            _transaction_id = None
            _multi_use = False

            def _make_txn_selector(self):
                from google.cloud.spanner_v1.proto.transaction_pb2 import (
                    TransactionOptions, TransactionSelector)

                if self._transaction_id:
                    return TransactionSelector(id=self._transaction_id)
                options = TransactionOptions(
                    read_only=TransactionOptions.ReadOnly(strong=True))
                if self._multi_use:
                    return TransactionSelector(begin=options)
                return TransactionSelector(single_use=options)

        return _Derived(session)

    def _make_spanner_api(self):
        import google.cloud.spanner_v1.gapic.spanner_client

        return mock.create_autospec(
            google.cloud.spanner_v1.gapic.spanner_client.SpannerClient,
            instance=True)

    def test_ctor(self):
        session = _Session()
        base = self._make_one(session)
        self.assertIs(base._session, session)

    def test__make_txn_selector_virtual(self):
        session = _Session()
        base = self._make_one(session)
        with self.assertRaises(NotImplementedError):
            base._make_txn_selector()

    def test_read_other_error(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keyset = KeySet(all_=True)
        database = _Database()
        database.spanner_api = self._make_spanner_api()
        database.spanner_api.streaming_read.side_effect = RuntimeError()
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(RuntimeError):
            list(derived.read(TABLE_NAME, COLUMNS, keyset))

    def _read_helper(self, multi_use, first=True, count=0, partition=None):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1.proto.result_set_pb2 import (
            PartialResultSet, ResultSetMetadata, ResultSetStats)
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            TransactionSelector)
        from google.cloud.spanner_v1.proto.type_pb2 import Type, StructType
        from google.cloud.spanner_v1.proto.type_pb2 import STRING, INT64
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1._helpers import _make_value_pb

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
        keyset = KeySet(keys=KEYS)
        INDEX = 'email-address-index'
        LIMIT = 20
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _streaming_read_response=_MockIterator(*result_sets))
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        derived._read_request_count = count
        if not first:
            derived._transaction_id = TXN_ID

        if partition is not None:  # 'limit' and 'partition' incompatible
            result_set = derived.read(
                TABLE_NAME, COLUMNS, keyset,
                index=INDEX, partition=partition)
        else:
            result_set = derived.read(
                TABLE_NAME, COLUMNS, keyset,
                index=INDEX, limit=LIMIT)

        self.assertEqual(derived._read_request_count, count + 1)

        if multi_use:
            self.assertIs(result_set._source, derived)
        else:
            self.assertIsNone(result_set._source)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        (r_session, table, columns, key_set, transaction, index, limit,
         resume_token, r_partition, metadata) = api._streaming_read_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(key_set, keyset._to_pb())
        self.assertIsInstance(transaction, TransactionSelector)
        if multi_use:
            if first:
                self.assertTrue(transaction.begin.read_only.strong)
            else:
                self.assertEqual(transaction.id, TXN_ID)
        else:
            self.assertTrue(transaction.single_use.read_only.strong)
        self.assertEqual(index, INDEX)
        if partition is not None:
            self.assertEqual(limit, 0)
            self.assertEqual(r_partition, partition)
        else:
            self.assertEqual(limit, LIMIT)
            self.assertIsNone(r_partition)
        self.assertEqual(resume_token, b'')
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])

    def test_read_wo_multi_use(self):
        self._read_helper(multi_use=False)

    def test_read_wo_multi_use_w_read_request_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._read_helper(multi_use=False, count=1)

    def test_read_w_multi_use_wo_first(self):
        self._read_helper(multi_use=True, first=False)

    def test_read_w_multi_use_wo_first_w_count_gt_0(self):
        self._read_helper(multi_use=True, first=False, count=1)

    def test_read_w_multi_use_w_first_w_partition(self):
        PARTITION = b'FADEABED'
        self._read_helper(multi_use=True, first=True, partition=PARTITION)

    def test_read_w_multi_use_w_first_w_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._read_helper(multi_use=True, first=True, count=1)

    def test_execute_sql_other_error(self):
        database = _Database()
        database.spanner_api = self._make_spanner_api()
        database.spanner_api.execute_streaming_sql.side_effect = RuntimeError()
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(RuntimeError):
            list(derived.execute_sql(SQL_QUERY))

    def test_execute_sql_w_params_wo_param_types(self):
        database = _Database()
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(ValueError):
            derived.execute_sql(SQL_QUERY_WITH_PARAM, PARAMS)

    def _execute_sql_helper(
            self, multi_use, first=True, count=0, partition=None):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1.proto.result_set_pb2 import (
            PartialResultSet, ResultSetMetadata, ResultSetStats)
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            TransactionSelector)
        from google.cloud.spanner_v1.proto.type_pb2 import Type, StructType
        from google.cloud.spanner_v1.proto.type_pb2 import STRING, INT64
        from google.cloud.spanner_v1._helpers import _make_value_pb

        VALUES = [
            [u'bharney', u'rhubbyl', 31],
            [u'phred', u'phlyntstone', 32],
        ]
        VALUE_PBS = [
            [_make_value_pb(item) for item in row]
            for row in VALUES
        ]
        MODE = 2  # PROFILE
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
        iterator = _MockIterator(*result_sets)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _execute_streaming_sql_response=iterator)
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        derived._read_request_count = count
        if not first:
            derived._transaction_id = TXN_ID

        result_set = derived.execute_sql(
            SQL_QUERY_WITH_PARAM, PARAMS, PARAM_TYPES,
            query_mode=MODE, partition=partition)

        self.assertEqual(derived._read_request_count, count + 1)

        if multi_use:
            self.assertIs(result_set._source, derived)
        else:
            self.assertIsNone(result_set._source)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        (r_session, sql, transaction, params, param_types,
         resume_token, query_mode, partition_token,
         metadata) = api._executed_streaming_sql_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(sql, SQL_QUERY_WITH_PARAM)
        self.assertIsInstance(transaction, TransactionSelector)
        if multi_use:
            if first:
                self.assertTrue(transaction.begin.read_only.strong)
            else:
                self.assertEqual(transaction.id, TXN_ID)
        else:
            self.assertTrue(transaction.single_use.read_only.strong)
        expected_params = Struct(fields={
            key: _make_value_pb(value) for (key, value) in PARAMS.items()})
        self.assertEqual(params, expected_params)
        self.assertEqual(param_types, PARAM_TYPES)
        self.assertEqual(query_mode, MODE)
        self.assertEqual(resume_token, b'')
        self.assertEqual(partition_token, partition)
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])

    def test_execute_sql_wo_multi_use(self):
        self._execute_sql_helper(multi_use=False)

    def test_execute_sql_wo_multi_use_w_read_request_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=False, count=1)

    def test_execute_sql_w_multi_use_wo_first(self):
        self._execute_sql_helper(multi_use=True, first=False)

    def test_execute_sql_w_multi_use_wo_first_w_count_gt_0(self):
        self._execute_sql_helper(multi_use=True, first=False, count=1)

    def test_execute_sql_w_multi_use_w_first(self):
        self._execute_sql_helper(multi_use=True, first=True)

    def test_execute_sql_w_multi_use_w_first_w_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=True, first=True, count=1)

    def _partition_read_helper(
            self, multi_use, w_txn,
            size=None, max_partitions=None, index=None):
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1.types import Partition
        from google.cloud.spanner_v1.types import PartitionOptions
        from google.cloud.spanner_v1.types import PartitionResponse
        from google.cloud.spanner_v1.types import Transaction
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            TransactionSelector)

        keyset = KeySet(all_=True)
        new_txn_id = b'ABECAB91'
        token_1 = b'FACE0FFF'
        token_2 = b'BADE8CAF'
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _partition_read_response=response)
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        if w_txn:
            derived._transaction_id = TXN_ID

        tokens = list(derived.partition_read(
            TABLE_NAME, COLUMNS, keyset,
            index=index,
            partition_size_bytes=size,
            max_partitions=max_partitions,
        ))

        self.assertEqual(tokens, [token_1, token_2])

        (r_session, table, key_set, transaction, r_index, columns,
            partition_options, metadata) = api._partition_read_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(table, TABLE_NAME)
        self.assertEqual(key_set, keyset._to_pb())
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertEqual(transaction.id, TXN_ID)
        self.assertFalse(transaction.HasField('begin'))
        self.assertEqual(r_index, index)
        self.assertEqual(columns, COLUMNS)
        self.assertEqual(
            partition_options,
            PartitionOptions(
                partition_size_bytes=size, max_partitions=max_partitions))
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])

    def test_partition_read_single_use_raises(self):
        with self.assertRaises(ValueError):
            self._partition_read_helper(multi_use=False, w_txn=True)

    def test_partition_read_wo_existing_transaction_raises(self):
        with self.assertRaises(ValueError):
            self._partition_read_helper(multi_use=True, w_txn=False)

    def test_partition_read_other_error(self):
        from google.cloud.spanner_v1.keyset import KeySet

        keyset = KeySet(all_=True)
        database = _Database()
        database.spanner_api = self._make_spanner_api()
        database.spanner_api.partition_read.side_effect = RuntimeError()
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = True
        derived._transaction_id = TXN_ID

        with self.assertRaises(RuntimeError):
            list(derived.partition_read(TABLE_NAME, COLUMNS, keyset))

    def test_partition_read_ok_w_index_no_options(self):
        self._partition_read_helper(multi_use=True, w_txn=True, index='index')

    def test_partition_read_ok_w_size(self):
        self._partition_read_helper(multi_use=True, w_txn=True, size=2000)

    def test_partition_read_ok_w_max_partitions(self):
        self._partition_read_helper(
            multi_use=True, w_txn=True, max_partitions=4)

    def _partition_query_helper(
            self, multi_use, w_txn, size=None, max_partitions=None):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1.types import Partition
        from google.cloud.spanner_v1.types import PartitionOptions
        from google.cloud.spanner_v1.types import PartitionResponse
        from google.cloud.spanner_v1.types import Transaction
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            TransactionSelector)
        from google.cloud.spanner_v1._helpers import _make_value_pb

        new_txn_id = b'ABECAB91'
        token_1 = b'FACE0FFF'
        token_2 = b'BADE8CAF'
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _partition_query_response=response)
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        if w_txn:
            derived._transaction_id = TXN_ID

        tokens = list(derived.partition_query(
            SQL_QUERY_WITH_PARAM, PARAMS, PARAM_TYPES,
            partition_size_bytes=size,
            max_partitions=max_partitions,
        ))

        self.assertEqual(tokens, [token_1, token_2])

        (r_session, sql, transaction, params, param_types,
         partition_options, metadata) = api._partition_query_with

        self.assertEqual(r_session, self.SESSION_NAME)
        self.assertEqual(sql, SQL_QUERY_WITH_PARAM)
        self.assertIsInstance(transaction, TransactionSelector)
        self.assertEqual(transaction.id, TXN_ID)
        self.assertFalse(transaction.HasField('begin'))
        expected_params = Struct(fields={
            key: _make_value_pb(value) for (key, value) in PARAMS.items()})
        self.assertEqual(params, expected_params)
        self.assertEqual(param_types, PARAM_TYPES)
        self.assertEqual(
            partition_options,
            PartitionOptions(
                partition_size_bytes=size, max_partitions=max_partitions))
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])

    def test_partition_query_other_error(self):
        database = _Database()
        database.spanner_api = self._make_spanner_api()
        database.spanner_api.partition_query.side_effect = RuntimeError()
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = True
        derived._transaction_id = TXN_ID

        with self.assertRaises(RuntimeError):
            list(derived.partition_query(SQL_QUERY))

    def test_partition_query_w_params_wo_param_types(self):
        database = _Database()
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = True
        derived._transaction_id = TXN_ID

        with self.assertRaises(ValueError):
            list(derived.partition_query(SQL_QUERY_WITH_PARAM, PARAMS))

    def test_partition_query_single_use_raises(self):
        with self.assertRaises(ValueError):
            self._partition_query_helper(multi_use=False, w_txn=True)

    def test_partition_query_wo_transaction_raises(self):
        with self.assertRaises(ValueError):
            self._partition_query_helper(multi_use=True, w_txn=False)

    def test_partition_query_ok_w_index_no_options(self):
        self._partition_query_helper(multi_use=True, w_txn=True)

    def test_partition_query_ok_w_size(self):
        self._partition_query_helper(multi_use=True, w_txn=True, size=2000)

    def test_partition_query_ok_w_max_partitions(self):
        self._partition_query_helper(
            multi_use=True, w_txn=True, max_partitions=4)


class TestSnapshot(unittest.TestCase):

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = 'projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID
    DATABASE_ID = 'database-id'
    DATABASE_NAME = INSTANCE_NAME + '/databases/' + DATABASE_ID
    SESSION_ID = 'session-id'
    SESSION_NAME = DATABASE_NAME + '/sessions/' + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner_v1.snapshot import Snapshot
        return Snapshot

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _make_spanner_api(self):
        import google.cloud.spanner_v1.gapic.spanner_client

        return mock.create_autospec(
            google.cloud.spanner_v1.gapic.spanner_client.SpannerClient,
            instance=True)

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
        self.assertIs(snapshot._session, session)
        self.assertTrue(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertFalse(snapshot._multi_use)

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
        self.assertIs(snapshot._session, session)
        self.assertFalse(snapshot._strong)
        self.assertEqual(snapshot._read_timestamp, timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertFalse(snapshot._multi_use)

    def test_ctor_w_min_read_timestamp(self):
        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, min_read_timestamp=timestamp)
        self.assertIs(snapshot._session, session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertEqual(snapshot._min_read_timestamp, timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertFalse(snapshot._multi_use)

    def test_ctor_w_max_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(session, max_staleness=duration)
        self.assertIs(snapshot._session, session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertEqual(snapshot._max_staleness, duration)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertFalse(snapshot._multi_use)

    def test_ctor_w_exact_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration)
        self.assertIs(snapshot._session, session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertEqual(snapshot._exact_staleness, duration)
        self.assertFalse(snapshot._multi_use)

    def test_ctor_w_multi_use(self):
        session = _Session()
        snapshot = self._make_one(session, multi_use=True)
        self.assertTrue(snapshot._session is session)
        self.assertTrue(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertTrue(snapshot._multi_use)

    def test_ctor_w_multi_use_and_read_timestamp(self):
        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(
            session, read_timestamp=timestamp, multi_use=True)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertEqual(snapshot._read_timestamp, timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertIsNone(snapshot._exact_staleness)
        self.assertTrue(snapshot._multi_use)

    def test_ctor_w_multi_use_and_min_read_timestamp(self):
        timestamp = self._makeTimestamp()
        session = _Session()

        with self.assertRaises(ValueError):
            self._make_one(
                session, min_read_timestamp=timestamp, multi_use=True)

    def test_ctor_w_multi_use_and_max_staleness(self):
        duration = self._makeDuration()
        session = _Session()

        with self.assertRaises(ValueError):
            self._make_one(session, max_staleness=duration, multi_use=True)

    def test_ctor_w_multi_use_and_exact_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(
            session, exact_staleness=duration, multi_use=True)
        self.assertTrue(snapshot._session is session)
        self.assertFalse(snapshot._strong)
        self.assertIsNone(snapshot._read_timestamp)
        self.assertIsNone(snapshot._min_read_timestamp)
        self.assertIsNone(snapshot._max_staleness)
        self.assertEqual(snapshot._exact_staleness, duration)
        self.assertTrue(snapshot._multi_use)

    def test__make_txn_selector_w_transaction_id(self):
        session = _Session()
        snapshot = self._make_one(session)
        snapshot._transaction_id = TXN_ID
        selector = snapshot._make_txn_selector()
        self.assertEqual(selector.id, TXN_ID)

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

    def test__make_txn_selector_strong_w_multi_use(self):
        session = _Session()
        snapshot = self._make_one(session, multi_use=True)
        selector = snapshot._make_txn_selector()
        options = selector.begin
        self.assertTrue(options.read_only.strong)

    def test__make_txn_selector_w_read_timestamp_w_multi_use(self):
        from google.cloud._helpers import _pb_timestamp_to_datetime

        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(
            session, read_timestamp=timestamp, multi_use=True)
        selector = snapshot._make_txn_selector()
        options = selector.begin
        self.assertEqual(
            _pb_timestamp_to_datetime(options.read_only.read_timestamp),
            timestamp)

    def test__make_txn_selector_w_exact_staleness_w_multi_use(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(
            session, exact_staleness=duration, multi_use=True)
        selector = snapshot._make_txn_selector()
        options = selector.begin
        self.assertEqual(options.read_only.exact_staleness.seconds, 3)
        self.assertEqual(options.read_only.exact_staleness.nanos, 123456000)

    def test_begin_wo_multi_use(self):
        session = _Session()
        snapshot = self._make_one(session)
        with self.assertRaises(ValueError):
            snapshot.begin()

    def test_begin_w_read_request_count_gt_0(self):
        session = _Session()
        snapshot = self._make_one(session, multi_use=True)
        snapshot._read_request_count = 1
        with self.assertRaises(ValueError):
            snapshot.begin()

    def test_begin_w_existing_txn_id(self):
        session = _Session()
        snapshot = self._make_one(session, multi_use=True)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            snapshot.begin()

    def test_begin_w_other_error(self):
        database = _Database()
        database.spanner_api = self._make_spanner_api()
        database.spanner_api.begin_transaction.side_effect = RuntimeError()
        timestamp = self._makeTimestamp()
        session = _Session(database)
        snapshot = self._make_one(
            session, read_timestamp=timestamp, multi_use=True)

        with self.assertRaises(RuntimeError):
            snapshot.begin()

    def test_begin_ok_exact_staleness(self):
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB)

        transaction_pb = TransactionPB(id=TXN_ID)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _begin_transaction_response=transaction_pb)
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session(database)
        snapshot = self._make_one(
            session, exact_staleness=duration, multi_use=True)

        txn_id = snapshot.begin()

        self.assertEqual(txn_id, TXN_ID)
        self.assertEqual(snapshot._transaction_id, TXN_ID)

        session_id, txn_options, metadata = api._begun
        self.assertEqual(session_id, session.name)
        read_only = txn_options.read_only
        self.assertEqual(read_only.exact_staleness.seconds, 3)
        self.assertEqual(read_only.exact_staleness.nanos, 123456000)
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])

    def test_begin_ok_exact_strong(self):
        from google.cloud.spanner_v1.proto.transaction_pb2 import (
            Transaction as TransactionPB)

        transaction_pb = TransactionPB(id=TXN_ID)
        database = _Database()
        api = database.spanner_api = _FauxSpannerAPI(
            _begin_transaction_response=transaction_pb)
        session = _Session(database)
        snapshot = self._make_one(session, multi_use=True)

        txn_id = snapshot.begin()

        self.assertEqual(txn_id, TXN_ID)
        self.assertEqual(snapshot._transaction_id, TXN_ID)

        session_id, txn_options, metadata = api._begun
        self.assertEqual(session_id, session.name)
        self.assertTrue(txn_options.read_only.strong)
        self.assertEqual(
            metadata, [('google-cloud-resource-prefix', database.name)])


class _Session(object):

    def __init__(self, database=None, name=TestSnapshot.SESSION_NAME):
        self._database = database
        self.name = name


class _Database(object):
    name = 'testing'


class _FauxSpannerAPI(object):

    _read_with = _begin = None

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def begin_transaction(self, session, options_, metadata=None):
        self._begun = (session, options_, metadata)
        return self._begin_transaction_response

    # pylint: disable=too-many-arguments
    def streaming_read(self, session, table, columns, key_set,
                       transaction=None, index='', limit=0,
                       resume_token=b'', partition_token=None, metadata=None):
        self._streaming_read_with = (
            session, table, columns, key_set, transaction, index,
            limit, resume_token, partition_token, metadata)
        return self._streaming_read_response
    # pylint: enable=too-many-arguments

    def execute_streaming_sql(self, session, sql, transaction=None,
                              params=None, param_types=None,
                              resume_token=b'', query_mode=None,
                              partition_token=None, metadata=None):
        self._executed_streaming_sql_with = (
            session, sql, transaction, params, param_types, resume_token,
            query_mode, partition_token, metadata)
        return self._execute_streaming_sql_response

    # pylint: disable=too-many-arguments
    def partition_read(self, session, table, key_set,
                       transaction=None,
                       index='',
                       columns=None,
                       partition_options=None,
                       metadata=None):
        self._partition_read_with = (
            session, table, key_set, transaction, index, columns,
            partition_options, metadata)
        return self._partition_read_response
    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def partition_query(self, session, sql,
                        transaction=None,
                        params=None,
                        param_types=None,
                        partition_options=None,
                        metadata=None):
        self._partition_query_with = (
            session, sql, transaction, params, param_types,
            partition_options, metadata)
        return self._partition_query_response
    # pylint: enable=too-many-arguments


class _MockIterator(object):

    def __init__(self, *values, **kw):
        self._iter_values = iter(values)
        self._fail_after = kw.pop('fail_after', False)

    def __iter__(self):
        return self

    def __next__(self):
        from google.api_core.exceptions import ServiceUnavailable

        try:
            return next(self._iter_values)
        except StopIteration:
            if self._fail_after:
                raise ServiceUnavailable('testing')
            raise

    next = __next__
