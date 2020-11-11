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


import google.api_core.gapic_v1.method
import mock
from tests._helpers import (
    OpenTelemetryBase,
    StatusCanonicalCode,
    HAS_OPENTELEMETRY_INSTALLED,
)
from google.cloud.spanner_v1.param_types import INT64

TABLE_NAME = "citizens"
COLUMNS = ["email", "first_name", "last_name", "age"]
SQL_QUERY = """\
SELECT first_name, last_name, age FROM citizens ORDER BY age"""
SQL_QUERY_WITH_PARAM = """
SELECT first_name, last_name, email FROM citizens WHERE age <= @max_age"""
PARAMS = {"max_age": 30}
PARAM_TYPES = {"max_age": INT64}
SQL_QUERY_WITH_BYTES_PARAM = """\
SELECT image_name FROM images WHERE @bytes IN image_data"""
PARAMS_WITH_BYTES = {"bytes": b"FACEDACE"}
RESUME_TOKEN = b"DEADBEEF"
TXN_ID = b"DEAFBEAD"
SECONDS = 3
MICROS = 123456
BASE_ATTRIBUTES = {
    "db.type": "spanner",
    "db.url": "spanner.googleapis.com",
    "db.instance": "testing",
    "net.host.name": "spanner.googleapis.com",
}


class Test_restart_on_unavailable(OpenTelemetryBase):
    def _call_fut(self, restart, span_name=None, session=None, attributes=None):
        from google.cloud.spanner_v1.snapshot import _restart_on_unavailable

        return _restart_on_unavailable(restart, span_name, session, attributes)

    def _make_item(self, value, resume_token=b""):
        return mock.Mock(
            value=value, resume_token=resume_token, spec=["value", "resume_token"]
        )

    def test_iteration_w_empty_raw(self):
        raw = _MockIterator()
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), [])
        self.assertNoSpans()

    def test_iteration_w_non_empty_raw(self):
        ITEMS = (self._make_item(0), self._make_item(1))
        raw = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        restart.assert_called_once_with()
        self.assertNoSpans()

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
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_no_token(self):
        from google.api_core.exceptions import ServiceUnavailable

        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(fail_after=True, error=ServiceUnavailable("testing"))
        after = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        self.assertEqual(restart.mock_calls, [mock.call(), mock.call(resume_token=b"")])
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error_no_token(self):
        from google.api_core.exceptions import InternalServerError

        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(
            fail_after=True,
            error=InternalServerError(
                "Received unexpected EOS on DATA frame from server"
            ),
        )
        after = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(ITEMS))
        self.assertEqual(restart.mock_calls, [mock.call(), mock.call(resume_token=b"")])
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error_no_token(self):
        from google.api_core.exceptions import InternalServerError

        ITEMS = (
            self._make_item(0),
            self._make_item(1, resume_token=RESUME_TOKEN),
            self._make_item(2),
        )
        before = _MockIterator(fail_after=True, error=InternalServerError("testing"))
        after = _MockIterator(*ITEMS)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        with self.assertRaises(InternalServerError):
            list(resumable)
        self.assertEqual(restart.mock_calls, [mock.call()])
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable(self):
        from google.api_core.exceptions import ServiceUnavailable

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND), fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*LAST)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + LAST))
        self.assertEqual(
            restart.mock_calls, [mock.call(), mock.call(resume_token=RESUME_TOKEN)]
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND),
            fail_after=True,
            error=InternalServerError(
                "Received unexpected EOS on DATA frame from server"
            )
        )
        after = _MockIterator(*LAST)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + LAST))
        self.assertEqual(
            restart.mock_calls, [mock.call(), mock.call(resume_token=RESUME_TOKEN)]
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2),)  # discarded after 503
        LAST = (self._make_item(3),)
        before = _MockIterator(
            *(FIRST + SECOND), fail_after=True, error=InternalServerError("testing")
        )
        after = _MockIterator(*LAST)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        with self.assertRaises(InternalServerError):
            list(resumable)
        self.assertEqual(restart.mock_calls, [mock.call()])
        self.assertNoSpans()

    def test_iteration_w_raw_raising_unavailable_after_token(self):
        from google.api_core.exceptions import ServiceUnavailable

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=ServiceUnavailable("testing")
        )
        after = _MockIterator(*SECOND)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(
            restart.mock_calls, [mock.call(), mock.call(resume_token=RESUME_TOKEN)]
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_retryable_internal_error_after_token(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST,
            fail_after=True,
            error=InternalServerError(
                "Received unexpected EOS on DATA frame from server"
            )
        )
        after = _MockIterator(*SECOND)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        self.assertEqual(list(resumable), list(FIRST + SECOND))
        self.assertEqual(
            restart.mock_calls, [mock.call(), mock.call(resume_token=RESUME_TOKEN)]
        )
        self.assertNoSpans()

    def test_iteration_w_raw_raising_non_retryable_internal_error_after_token(self):
        from google.api_core.exceptions import InternalServerError

        FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
        SECOND = (self._make_item(2), self._make_item(3))
        before = _MockIterator(
            *FIRST, fail_after=True, error=InternalServerError("testing")
        )
        after = _MockIterator(*SECOND)
        restart = mock.Mock(spec=[], side_effect=[before, after])
        resumable = self._call_fut(restart)
        with self.assertRaises(InternalServerError):
            list(resumable)
        self.assertEqual(restart.mock_calls, [mock.call()])
        self.assertNoSpans()

    def test_iteration_w_span_creation(self):
        name = "TestSpan"
        extra_atts = {"test_att": 1}
        raw = _MockIterator()
        restart = mock.Mock(spec=[], return_value=raw)
        resumable = self._call_fut(restart, name, _Session(_Database()), extra_atts)
        self.assertEqual(list(resumable), [])
        self.assertSpanAttributes(name, attributes=dict(BASE_ATTRIBUTES, test_att=1))

    def test_iteration_w_multiple_span_creation(self):
        from google.api_core.exceptions import ServiceUnavailable

        if HAS_OPENTELEMETRY_INSTALLED:
            FIRST = (self._make_item(0), self._make_item(1, resume_token=RESUME_TOKEN))
            SECOND = (self._make_item(2),)  # discarded after 503
            LAST = (self._make_item(3),)
            before = _MockIterator(
                *(FIRST + SECOND), fail_after=True, error=ServiceUnavailable("testing")
            )
            after = _MockIterator(*LAST)
            restart = mock.Mock(spec=[], side_effect=[before, after])
            name = "TestSpan"
            resumable = self._call_fut(restart, name, _Session(_Database()))
            self.assertEqual(list(resumable), list(FIRST + LAST))
            self.assertEqual(
                restart.mock_calls, [mock.call(), mock.call(resume_token=RESUME_TOKEN)]
            )

            span_list = self.memory_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 2)
            for span in span_list:
                self.assertEqual(span.name, name)
                self.assertEqual(
                    dict(span.attributes),
                    {
                        "db.type": "spanner",
                        "db.url": "spanner.googleapis.com",
                        "db.instance": "testing",
                        "net.host.name": "spanner.googleapis.com",
                    },
                )


class Test_SnapshotBase(OpenTelemetryBase):

    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database-id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session-id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID

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
                from google.cloud.spanner_v1 import (
                    TransactionOptions,
                    TransactionSelector,
                )

                if self._transaction_id:
                    return TransactionSelector(id=self._transaction_id)
                options = TransactionOptions(
                    read_only=TransactionOptions.ReadOnly(strong=True)
                )
                if self._multi_use:
                    return TransactionSelector(begin=options)
                return TransactionSelector(single_use=options)

        return _Derived(session)

    def _make_spanner_api(self):
        from google.cloud.spanner_v1 import SpannerClient

        return mock.create_autospec(SpannerClient, instance=True)

    def test_ctor(self):
        session = _Session()
        base = self._make_one(session)
        self.assertIs(base._session, session)
        self.assertEqual(base._execute_sql_count, 0)

        self.assertNoSpans()

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

        self.assertSpanAttributes(
            "CloudSpanner.ReadOnlyTransaction",
            status=StatusCanonicalCode.UNKNOWN,
            attributes=dict(
                BASE_ATTRIBUTES, table_id=TABLE_NAME, columns=tuple(COLUMNS)
            ),
        )

    def _read_helper(self, multi_use, first=True, count=0, partition=None):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import (
            PartialResultSet,
            ResultSetMetadata,
            ResultSetStats,
        )
        from google.cloud.spanner_v1 import (
            TransactionSelector,
            TransactionOptions,
        )
        from google.cloud.spanner_v1 import ReadRequest
        from google.cloud.spanner_v1 import Type, StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1._helpers import _make_value_pb

        VALUES = [[u"bharney", 31], [u"phred", 32]]
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )
        metadata_pb = ResultSetMetadata(row_type=struct_type_pb)
        stats_pb = ResultSetStats(
            query_stats=Struct(fields={"rows_returned": _make_value_pb(2)})
        )
        result_sets = [
            PartialResultSet(metadata=metadata_pb),
            PartialResultSet(stats=stats_pb),
        ]
        for i in range(len(result_sets)):
            result_sets[i].values.extend(VALUES[i])
        KEYS = [["bharney@example.com"], ["phred@example.com"]]
        keyset = KeySet(keys=KEYS)
        INDEX = "email-address-index"
        LIMIT = 20
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.streaming_read.return_value = _MockIterator(*result_sets)
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        derived._read_request_count = count
        if not first:
            derived._transaction_id = TXN_ID

        if partition is not None:  # 'limit' and 'partition' incompatible
            result_set = derived.read(
                TABLE_NAME, COLUMNS, keyset, index=INDEX, partition=partition
            )
        else:
            result_set = derived.read(
                TABLE_NAME, COLUMNS, keyset, index=INDEX, limit=LIMIT
            )

        self.assertEqual(derived._read_request_count, count + 1)

        if multi_use:
            self.assertIs(result_set._source, derived)
        else:
            self.assertIsNone(result_set._source)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        txn_options = TransactionOptions(
            read_only=TransactionOptions.ReadOnly(strong=True)
        )

        if multi_use:
            if first:
                expected_transaction = TransactionSelector(begin=txn_options)
            else:
                expected_transaction = TransactionSelector(id=TXN_ID)
        else:
            expected_transaction = TransactionSelector(single_use=txn_options)

        if partition is not None:
            expected_limit = 0
        else:
            expected_limit = LIMIT

        expected_request = ReadRequest(
            session=self.SESSION_NAME,
            table=TABLE_NAME,
            columns=COLUMNS,
            key_set=keyset._to_pb(),
            transaction=expected_transaction,
            index=INDEX,
            limit=expected_limit,
            partition_token=partition,
        )
        api.streaming_read.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        self.assertSpanAttributes(
            "CloudSpanner.ReadOnlyTransaction",
            attributes=dict(
                BASE_ATTRIBUTES, table_id=TABLE_NAME, columns=tuple(COLUMNS)
            ),
        )

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
        PARTITION = b"FADEABED"
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

        self.assertEqual(derived._execute_sql_count, 1)

        self.assertSpanAttributes(
            "CloudSpanner.ReadWriteTransaction",
            status=StatusCanonicalCode.UNKNOWN,
            attributes=dict(BASE_ATTRIBUTES, **{"db.statement": SQL_QUERY}),
        )

    def test_execute_sql_w_params_wo_param_types(self):
        database = _Database()
        session = _Session(database)
        derived = self._makeDerived(session)

        with self.assertRaises(ValueError):
            derived.execute_sql(SQL_QUERY_WITH_PARAM, PARAMS)

        self.assertNoSpans()

    def _execute_sql_helper(
        self,
        multi_use,
        first=True,
        count=0,
        partition=None,
        sql_count=0,
        query_options=None,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        retry=google.api_core.gapic_v1.method.DEFAULT,
    ):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import (
            PartialResultSet,
            ResultSetMetadata,
            ResultSetStats,
        )
        from google.cloud.spanner_v1 import (
            TransactionSelector,
            TransactionOptions,
        )
        from google.cloud.spanner_v1 import ExecuteSqlRequest
        from google.cloud.spanner_v1 import Type, StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1._helpers import (
            _make_value_pb,
            _merge_query_options,
        )

        VALUES = [[u"bharney", u"rhubbyl", 31], [u"phred", u"phlyntstone", 32]]
        MODE = 2  # PROFILE
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="first_name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="last_name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )
        metadata_pb = ResultSetMetadata(row_type=struct_type_pb)
        stats_pb = ResultSetStats(
            query_stats=Struct(fields={"rows_returned": _make_value_pb(2)})
        )
        result_sets = [
            PartialResultSet(metadata=metadata_pb),
            PartialResultSet(stats=stats_pb),
        ]
        for i in range(len(result_sets)):
            result_sets[i].values.extend(VALUES[i])
        iterator = _MockIterator(*result_sets)
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.execute_streaming_sql.return_value = iterator
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        derived._read_request_count = count
        derived._execute_sql_count = sql_count
        if not first:
            derived._transaction_id = TXN_ID

        result_set = derived.execute_sql(
            SQL_QUERY_WITH_PARAM,
            PARAMS,
            PARAM_TYPES,
            query_mode=MODE,
            query_options=query_options,
            partition=partition,
            retry=retry,
            timeout=timeout,
        )

        self.assertEqual(derived._read_request_count, count + 1)

        if multi_use:
            self.assertIs(result_set._source, derived)
        else:
            self.assertIsNone(result_set._source)

        self.assertEqual(list(result_set), VALUES)
        self.assertEqual(result_set.metadata, metadata_pb)
        self.assertEqual(result_set.stats, stats_pb)

        txn_options = TransactionOptions(
            read_only=TransactionOptions.ReadOnly(strong=True)
        )

        if multi_use:
            if first:
                expected_transaction = TransactionSelector(begin=txn_options)
            else:
                expected_transaction = TransactionSelector(id=TXN_ID)
        else:
            expected_transaction = TransactionSelector(single_use=txn_options)

        expected_params = Struct(
            fields={key: _make_value_pb(value) for (key, value) in PARAMS.items()}
        )

        expected_query_options = database._instance._client._query_options
        if query_options:
            expected_query_options = _merge_query_options(
                expected_query_options, query_options
            )

        expected_request = ExecuteSqlRequest(
            session=self.SESSION_NAME,
            sql=SQL_QUERY_WITH_PARAM,
            transaction=expected_transaction,
            params=expected_params,
            param_types=PARAM_TYPES,
            query_mode=MODE,
            query_options=expected_query_options,
            partition_token=partition,
            seqno=sql_count,
        )
        api.execute_streaming_sql.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
            timeout=timeout,
            retry=retry,
        )

        self.assertEqual(derived._execute_sql_count, sql_count + 1)

        self.assertSpanAttributes(
            "CloudSpanner.ReadWriteTransaction",
            status=StatusCanonicalCode.OK,
            attributes=dict(BASE_ATTRIBUTES, **{"db.statement": SQL_QUERY_WITH_PARAM}),
        )

    def test_execute_sql_wo_multi_use(self):
        self._execute_sql_helper(multi_use=False)

    def test_execute_sql_wo_multi_use_w_read_request_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=False, count=1)

    def test_execute_sql_w_multi_use_wo_first(self):
        self._execute_sql_helper(multi_use=True, first=False, sql_count=1)

    def test_execute_sql_w_multi_use_wo_first_w_count_gt_0(self):
        self._execute_sql_helper(multi_use=True, first=False, count=1)

    def test_execute_sql_w_multi_use_w_first(self):
        self._execute_sql_helper(multi_use=True, first=True)

    def test_execute_sql_w_multi_use_w_first_w_count_gt_0(self):
        with self.assertRaises(ValueError):
            self._execute_sql_helper(multi_use=True, first=True, count=1)

    def test_execute_sql_w_retry(self):
        self._execute_sql_helper(multi_use=False, retry=None)

    def test_execute_sql_w_timeout(self):
        self._execute_sql_helper(multi_use=False, timeout=None)

    def test_execute_sql_w_query_options(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self._execute_sql_helper(
            multi_use=False,
            query_options=ExecuteSqlRequest.QueryOptions(optimizer_version="3"),
        )

    def _partition_read_helper(
        self, multi_use, w_txn, size=None, max_partitions=None, index=None
    ):
        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1 import Partition
        from google.cloud.spanner_v1 import PartitionOptions
        from google.cloud.spanner_v1 import PartitionReadRequest
        from google.cloud.spanner_v1 import PartitionResponse
        from google.cloud.spanner_v1 import Transaction
        from google.cloud.spanner_v1 import TransactionSelector

        keyset = KeySet(all_=True)
        new_txn_id = b"ABECAB91"
        token_1 = b"FACE0FFF"
        token_2 = b"BADE8CAF"
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.partition_read.return_value = response
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        if w_txn:
            derived._transaction_id = TXN_ID

        tokens = list(
            derived.partition_read(
                TABLE_NAME,
                COLUMNS,
                keyset,
                index=index,
                partition_size_bytes=size,
                max_partitions=max_partitions,
            )
        )

        self.assertEqual(tokens, [token_1, token_2])

        expected_txn_selector = TransactionSelector(id=TXN_ID)

        expected_partition_options = PartitionOptions(
            partition_size_bytes=size, max_partitions=max_partitions
        )

        expected_request = PartitionReadRequest(
            session=self.SESSION_NAME,
            table=TABLE_NAME,
            columns=COLUMNS,
            key_set=keyset._to_pb(),
            transaction=expected_txn_selector,
            index=index,
            partition_options=expected_partition_options,
        )
        api.partition_read.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        self.assertSpanAttributes(
            "CloudSpanner.PartitionReadOnlyTransaction",
            status=StatusCanonicalCode.OK,
            attributes=dict(
                BASE_ATTRIBUTES, table_id=TABLE_NAME, columns=tuple(COLUMNS)
            ),
        )

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

        self.assertSpanAttributes(
            "CloudSpanner.PartitionReadOnlyTransaction",
            status=StatusCanonicalCode.UNKNOWN,
            attributes=dict(
                BASE_ATTRIBUTES, table_id=TABLE_NAME, columns=tuple(COLUMNS)
            ),
        )

    def test_partition_read_ok_w_index_no_options(self):
        self._partition_read_helper(multi_use=True, w_txn=True, index="index")

    def test_partition_read_ok_w_size(self):
        self._partition_read_helper(multi_use=True, w_txn=True, size=2000)

    def test_partition_read_ok_w_max_partitions(self):
        self._partition_read_helper(multi_use=True, w_txn=True, max_partitions=4)

    def _partition_query_helper(self, multi_use, w_txn, size=None, max_partitions=None):
        from google.protobuf.struct_pb2 import Struct
        from google.cloud.spanner_v1 import Partition
        from google.cloud.spanner_v1 import PartitionOptions
        from google.cloud.spanner_v1 import PartitionQueryRequest
        from google.cloud.spanner_v1 import PartitionResponse
        from google.cloud.spanner_v1 import Transaction
        from google.cloud.spanner_v1 import TransactionSelector
        from google.cloud.spanner_v1._helpers import _make_value_pb

        new_txn_id = b"ABECAB91"
        token_1 = b"FACE0FFF"
        token_2 = b"BADE8CAF"
        response = PartitionResponse(
            partitions=[
                Partition(partition_token=token_1),
                Partition(partition_token=token_2),
            ],
            transaction=Transaction(id=new_txn_id),
        )
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.partition_query.return_value = response
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = multi_use
        if w_txn:
            derived._transaction_id = TXN_ID

        tokens = list(
            derived.partition_query(
                SQL_QUERY_WITH_PARAM,
                PARAMS,
                PARAM_TYPES,
                partition_size_bytes=size,
                max_partitions=max_partitions,
            )
        )

        self.assertEqual(tokens, [token_1, token_2])

        expected_params = Struct(
            fields={key: _make_value_pb(value) for (key, value) in PARAMS.items()}
        )

        expected_txn_selector = TransactionSelector(id=TXN_ID)

        expected_partition_options = PartitionOptions(
            partition_size_bytes=size, max_partitions=max_partitions
        )

        expected_request = PartitionQueryRequest(
            session=self.SESSION_NAME,
            sql=SQL_QUERY_WITH_PARAM,
            transaction=expected_txn_selector,
            params=expected_params,
            param_types=PARAM_TYPES,
            partition_options=expected_partition_options,
        )
        api.partition_query.assert_called_once_with(
            request=expected_request,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        self.assertSpanAttributes(
            "CloudSpanner.PartitionReadWriteTransaction",
            status=StatusCanonicalCode.OK,
            attributes=dict(BASE_ATTRIBUTES, **{"db.statement": SQL_QUERY_WITH_PARAM}),
        )

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

        self.assertSpanAttributes(
            "CloudSpanner.PartitionReadWriteTransaction",
            status=StatusCanonicalCode.UNKNOWN,
            attributes=dict(BASE_ATTRIBUTES, **{"db.statement": SQL_QUERY}),
        )

    def test_partition_query_w_params_wo_param_types(self):
        database = _Database()
        session = _Session(database)
        derived = self._makeDerived(session)
        derived._multi_use = True
        derived._transaction_id = TXN_ID

        with self.assertRaises(ValueError):
            list(derived.partition_query(SQL_QUERY_WITH_PARAM, PARAMS))

        self.assertNoSpans()

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
        self._partition_query_helper(multi_use=True, w_txn=True, max_partitions=4)


class TestSnapshot(OpenTelemetryBase):

    PROJECT_ID = "project-id"
    INSTANCE_ID = "instance-id"
    INSTANCE_NAME = "projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID
    DATABASE_ID = "database-id"
    DATABASE_NAME = INSTANCE_NAME + "/databases/" + DATABASE_ID
    SESSION_ID = "session-id"
    SESSION_NAME = DATABASE_NAME + "/sessions/" + SESSION_ID

    def _getTargetClass(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        return Snapshot

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def _make_spanner_api(self):
        from google.cloud.spanner_v1 import SpannerClient

        return mock.create_autospec(SpannerClient, instance=True)

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
            self._make_one(session, read_timestamp=timestamp, max_staleness=duration)

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
        snapshot = self._make_one(session, read_timestamp=timestamp, multi_use=True)
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
            self._make_one(session, min_read_timestamp=timestamp, multi_use=True)

    def test_ctor_w_multi_use_and_max_staleness(self):
        duration = self._makeDuration()
        session = _Session()

        with self.assertRaises(ValueError):
            self._make_one(session, max_staleness=duration, multi_use=True)

    def test_ctor_w_multi_use_and_exact_staleness(self):
        duration = self._makeDuration()
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration, multi_use=True)
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
            _pb_timestamp_to_datetime(
                type(options).pb(options).read_only.read_timestamp
            ),
            timestamp,
        )

    def test__make_txn_selector_w_min_read_timestamp(self):
        from google.cloud._helpers import _pb_timestamp_to_datetime

        timestamp = self._makeTimestamp()
        session = _Session()
        snapshot = self._make_one(session, min_read_timestamp=timestamp)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(
            _pb_timestamp_to_datetime(
                type(options).pb(options).read_only.min_read_timestamp
            ),
            timestamp,
        )

    def test__make_txn_selector_w_max_staleness(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(session, max_staleness=duration)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(type(options).pb(options).read_only.max_staleness.seconds, 3)
        self.assertEqual(
            type(options).pb(options).read_only.max_staleness.nanos, 123456000
        )

    def test__make_txn_selector_w_exact_staleness(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration)
        selector = snapshot._make_txn_selector()
        options = selector.single_use
        self.assertEqual(type(options).pb(options).read_only.exact_staleness.seconds, 3)
        self.assertEqual(
            type(options).pb(options).read_only.exact_staleness.nanos, 123456000
        )

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
        snapshot = self._make_one(session, read_timestamp=timestamp, multi_use=True)
        selector = snapshot._make_txn_selector()
        options = selector.begin
        self.assertEqual(
            _pb_timestamp_to_datetime(
                type(options).pb(options).read_only.read_timestamp
            ),
            timestamp,
        )

    def test__make_txn_selector_w_exact_staleness_w_multi_use(self):
        duration = self._makeDuration(seconds=3, microseconds=123456)
        session = _Session()
        snapshot = self._make_one(session, exact_staleness=duration, multi_use=True)
        selector = snapshot._make_txn_selector()
        options = selector.begin
        self.assertEqual(type(options).pb(options).read_only.exact_staleness.seconds, 3)
        self.assertEqual(
            type(options).pb(options).read_only.exact_staleness.nanos, 123456000
        )

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
        snapshot = self._make_one(session, read_timestamp=timestamp, multi_use=True)

        with self.assertRaises(RuntimeError):
            snapshot.begin()

        self.assertSpanAttributes(
            "CloudSpanner.BeginTransaction",
            status=StatusCanonicalCode.UNKNOWN,
            attributes=BASE_ATTRIBUTES,
        )

    def test_begin_ok_exact_staleness(self):
        from google.protobuf.duration_pb2 import Duration
        from google.cloud.spanner_v1 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )

        transaction_pb = TransactionPB(id=TXN_ID)
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.begin_transaction.return_value = transaction_pb
        duration = self._makeDuration(seconds=SECONDS, microseconds=MICROS)
        session = _Session(database)
        snapshot = self._make_one(session, exact_staleness=duration, multi_use=True)

        txn_id = snapshot.begin()

        self.assertEqual(txn_id, TXN_ID)
        self.assertEqual(snapshot._transaction_id, TXN_ID)

        expected_duration = Duration(seconds=SECONDS, nanos=MICROS * 1000)
        expected_txn_options = TransactionOptions(
            read_only=TransactionOptions.ReadOnly(exact_staleness=expected_duration)
        )

        api.begin_transaction.assert_called_once_with(
            session=session.name,
            options=expected_txn_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        self.assertSpanAttributes(
            "CloudSpanner.BeginTransaction",
            status=StatusCanonicalCode.OK,
            attributes=BASE_ATTRIBUTES,
        )

    def test_begin_ok_exact_strong(self):
        from google.cloud.spanner_v1 import (
            Transaction as TransactionPB,
            TransactionOptions,
        )

        transaction_pb = TransactionPB(id=TXN_ID)
        database = _Database()
        api = database.spanner_api = self._make_spanner_api()
        api.begin_transaction.return_value = transaction_pb
        session = _Session(database)
        snapshot = self._make_one(session, multi_use=True)

        txn_id = snapshot.begin()

        self.assertEqual(txn_id, TXN_ID)
        self.assertEqual(snapshot._transaction_id, TXN_ID)

        expected_txn_options = TransactionOptions(
            read_only=TransactionOptions.ReadOnly(strong=True)
        )

        api.begin_transaction.assert_called_once_with(
            session=session.name,
            options=expected_txn_options,
            metadata=[("google-cloud-resource-prefix", database.name)],
        )

        self.assertSpanAttributes(
            "CloudSpanner.BeginTransaction",
            status=StatusCanonicalCode.OK,
            attributes=BASE_ATTRIBUTES,
        )


class _Client(object):
    def __init__(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        self._query_options = ExecuteSqlRequest.QueryOptions(optimizer_version="1")


class _Instance(object):
    def __init__(self):
        self._client = _Client()


class _Database(object):
    def __init__(self):
        self.name = "testing"
        self._instance = _Instance()


class _Session(object):
    def __init__(self, database=None, name=TestSnapshot.SESSION_NAME):
        self._database = database
        self.name = name


class _MockIterator(object):
    def __init__(self, *values, **kw):
        self._iter_values = iter(values)
        self._fail_after = kw.pop("fail_after", False)
        self._error = kw.pop("error", Exception)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._iter_values)
        except StopIteration:
            if self._fail_after:
                raise self._error
            raise

    next = __next__
