# Copyright 2024 Google LLC All rights reserved.
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

import datetime
import unittest
from datetime import timedelta
from unittest import mock

from google.api_core.exceptions import (
    InternalServerError,
    InvalidArgument,
    ServiceUnavailable,
)

from google.cloud.spanner_v1._async.snapshot import Snapshot
from google.cloud.spanner_v1.types.result_set import PartialResultSet, ResultSetMetadata
from google.cloud.spanner_v1.types.spanner import (
    ExecuteSqlRequest,
    Partition,
    PartitionResponse,
)
from google.cloud.spanner_v1.types.transaction import Transaction as TransactionPB
from google.cloud.spanner_v1.types.transaction import TransactionSelector
from google.cloud.spanner_v1.types.type import StructType, Type, TypeCode

TABLE_NAME = "citizens"
COLUMNS = ["email", "first_name", "last_name", "age"]
SQL_QUERY = """SELECT first_name, last_name, age FROM citizens ORDER BY age"""
TXN_ID = b"DEAFBEAD"
TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)
DURATION = timedelta(seconds=3)


class Test_snapshot_coverage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.patch_metrics = mock.patch(
            "google.cloud.spanner_v1._async.snapshot.MetricsCapture"
        )
        self.patch_trace = mock.patch(
            "google.cloud.spanner_v1._async.snapshot.trace_call"
        )
        self.mock_metrics = self.patch_metrics.start()
        self.mock_trace = self.patch_trace.start()
        self.mock_metrics.return_value.__enter__.return_value = None
        self.mock_trace.return_value.__enter__.return_value = mock.Mock()

    def tearDown(self):
        self.patch_metrics.stop()
        self.patch_trace.stop()

    def _make_snapshot(self, *args, **kwargs):
        s = Snapshot(*args, **kwargs)
        # FORCE _lock to exist if it doesn't (though constructor should handle it)
        if not hasattr(s, "_lock"):
            from google.cloud.aio._cross_sync.cross_sync import CrossSync

            s._lock = CrossSync.Lock()
        return s

    async def test_read_errors(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._read_request_count = 1
        with self.assertRaises(ValueError):
            await snapshot.read(TABLE_NAME, COLUMNS, None)

        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._read_request_count = 1
        snapshot._transaction_id = None
        with self.assertRaises(ValueError):
            await snapshot.read(TABLE_NAME, COLUMNS, None)

    async def test_execute_sql_errors(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._read_request_count = 1
        with self.assertRaises(ValueError):
            await snapshot.execute_sql(SQL_QUERY)

    async def test_partition_read_ok(self):
        token_1 = b"TOKEN1"
        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database.spanner_api.partition_read = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        from google.cloud.spanner_v1.keyset import KeySet

        tokens = await snapshot.partition_read(TABLE_NAME, COLUMNS, KeySet(all_=True))
        self.assertEqual(tokens, [token_1])

    def test__update_for_transaction_pb(self):
        snapshot = self._make_snapshot(_Session())
        pb = TransactionPB(id=TXN_ID, read_timestamp=TIMESTAMP)
        snapshot._update_for_transaction_pb(pb)
        self.assertEqual(snapshot._transaction_id, TXN_ID)
        self.assertEqual(snapshot._transaction_read_timestamp, TIMESTAMP)

    async def test_restart_on_unavailable_precommit(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from tests._builders import build_precommit_token_pb

        token_pb = build_precommit_token_pb(precommit_token=b"token", seq_num=1)
        item = PartialResultSet(precommit_token=token_pb)

        raw = _MockIterator(item)
        restart = mock.Mock(return_value=raw)
        request = mock.Mock()
        request.transaction = None
        request.resume_token = b""
        session = _Session()
        snapshot = self._make_snapshot(session)

        resumable = _restart_on_unavailable(
            restart,
            request,
            metadata=None,
            trace_name="span",
            session=session,
            attributes={},
            transaction=snapshot,
            request_id_manager=session._database,
        )
        async for _ in resumable:
            pass
        self.assertEqual(snapshot._precommit_token, token_pb)

    async def test_execute_sql_ok(self):
        database = _Database()
        fields = [StructType.Field(name="col", type_=Type(code=TypeCode.STRING))]
        metadata_pb = ResultSetMetadata(row_type=StructType(fields=fields))
        metadata_pb.transaction.id = TXN_ID
        database.spanner_api.execute_streaming_sql.return_value = _MockIterator(
            PartialResultSet(metadata=metadata_pb)
        )

        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        from google.cloud.spanner_v1.types.spanner import ExecuteSqlRequest

        query_options = ExecuteSqlRequest.QueryOptions(optimizer_version="1")

        result = await snapshot.execute_sql(SQL_QUERY, query_options=query_options)
        async for _ in result:
            pass

    async def test_begin_ok(self):
        database = _Database()
        database.spanner_api.begin_transaction = mock.AsyncMock(
            return_value=TransactionPB(id=TXN_ID)
        )
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)

        res = await snapshot.begin()
        self.assertEqual(res, TXN_ID)
        self.assertEqual(snapshot._transaction_id, TXN_ID)

    async def test_read_ok(self):
        database = _Database()
        fields = [StructType.Field(name="col", type_=Type(code=TypeCode.STRING))]
        metadata_pb = ResultSetMetadata(row_type=StructType(fields=fields))
        metadata_pb.transaction.id = TXN_ID
        database.spanner_api.streaming_read.return_value = _MockIterator(
            PartialResultSet(metadata=metadata_pb)
        )

        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        from google.cloud.spanner_v1.keyset import KeySet
        from google.cloud.spanner_v1.types import RequestOptions

        request_options = RequestOptions(priority=RequestOptions.Priority.PRIORITY_HIGH)

        result = await snapshot.read(
            TABLE_NAME, COLUMNS, KeySet(all_=True), request_options=request_options
        )
        async for _ in result:
            pass

    async def test_restart_on_unavailable_service_unavailable(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from google.cloud.spanner_v1.types.result_set import PartialResultSet

        item = PartialResultSet()
        method = mock.AsyncMock(
            side_effect=[ServiceUnavailable("testing"), _MockIterator(item)]
        )
        request = mock.Mock()
        request.transaction = None
        request.resume_token = b""
        session = _Session()
        snapshot = self._make_snapshot(session)
        request_id_manager = mock.Mock()
        request_id_manager.metadata_and_request_id.return_value = (None, None)

        # Position 7 is transaction, Position 9 is request_id_manager
        result = _restart_on_unavailable(
            method,
            request,
            None,
            None,
            None,
            None,
            snapshot,
            None,
            None,
            request_id_manager,
        )
        async for i in result:
            self.assertEqual(i, item)
        self.assertEqual(method.call_count, 2)

    async def test_restart_on_unavailable_internal_error_rst_stream(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from google.cloud.spanner_v1.types.result_set import PartialResultSet

        item = PartialResultSet()
        method = mock.AsyncMock(
            side_effect=[InternalServerError("RST_STREAM"), _MockIterator(item)]
        )
        request = mock.Mock()
        request.transaction = None
        request.resume_token = b""
        session = _Session()
        snapshot = self._make_snapshot(session)
        request_id_manager = mock.Mock()
        request_id_manager.metadata_and_request_id.return_value = (None, None)

        # Position 7 is transaction, Position 9 is request_id_manager
        result = _restart_on_unavailable(
            method,
            request,
            None,
            None,
            None,
            None,
            snapshot,
            None,
            None,
            request_id_manager,
        )
        async for i in result:
            self.assertEqual(i, item)
        self.assertEqual(method.call_count, 2)

    async def test_execute_sql_w_multi_use_options(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        # First call works
        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        await snapshot.execute_sql(SQL_QUERY)

        # Second call works because multi_use=True
        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        await snapshot.execute_sql(SQL_QUERY)

    async def test_read_w_multi_use_options(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        api.streaming_read.return_value = _MockIterator(PartialResultSet())
        from google.cloud.spanner_v1.keyset import KeySet

        await snapshot.read(TABLE_NAME, COLUMNS, KeySet(all_=True))

        api.streaming_read.return_value = _MockIterator(PartialResultSet())
        await snapshot.read(TABLE_NAME, COLUMNS, KeySet(all_=True))

    async def test_restart_on_unavailable_no_transaction_or_selector(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable

        method = mock.AsyncMock()
        request = mock.Mock()

        with self.assertRaises(InvalidArgument):
            # args: method, request, metadata, trace_name, session, attributes, transaction, transaction_selector, observability_options, request_id_manager, resource_info
            gen = _restart_on_unavailable(
                method, request, None, None, None, None, None, None, None, None, None
            )
            async for _ in gen:
                pass

    async def test_restart_on_unavailable_with_resume_token(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from google.cloud.spanner_v1.types.result_set import PartialResultSet

        # Provide an item with a resume_token
        item1 = PartialResultSet(resume_token=b"resume-token")
        item2 = PartialResultSet()
        # First iterator yields item1 then fails
        it1 = _MockIterator(item1)
        it1.set_exception(ServiceUnavailable("retry"))
        # Second iterator yields item2
        it2 = _MockIterator(item2)

        method = mock.AsyncMock(side_effect=[it1, it2])

        request = mock.Mock()
        request.transaction = None
        request.resume_token = b""

        request_id_manager = mock.Mock()
        request_id_manager.metadata_and_request_id.return_value = ({}, "req-id")

        # args: method, request, metadata, trace_name, session, attributes, transaction, transaction_selector, observability_options, request_id_manager, resource_info
        gen = _restart_on_unavailable(
            method,
            request,
            None,
            None,
            None,
            None,
            None,
            mock.Mock(),
            None,
            request_id_manager,
            None,
        )
        items = []
        async for item in gen:
            items.append(item)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], item1)
        self.assertEqual(items[1], item2)
        self.assertEqual(request.resume_token, b"resume-token")
        self.assertEqual(method.call_count, 2)

    async def test_restart_on_unavailable_non_resumable_internal_error(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable

        method = mock.AsyncMock(side_effect=InternalServerError("testing"))
        request = mock.Mock()
        request_id_manager = mock.Mock()
        request_id_manager.metadata_and_request_id.return_value = (None, "req-id")

        with self.assertRaises(InternalServerError) as exc:
            # args: method, request, metadata, trace_name, session, attributes, transaction, transaction_selector, observability_options, request_id_manager, resource_info
            gen = _restart_on_unavailable(
                method,
                request,
                None,
                None,
                None,
                None,
                None,
                mock.Mock(),
                None,
                request_id_manager,
                None,
            )
            async for _ in gen:
                pass
        self.assertIn("req-id", str(exc.exception))

    async def test_partition_query_ok(self):
        token_1 = b"TOKEN1"
        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database.spanner_api.partition_query = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        tokens = await snapshot.partition_query(SQL_QUERY)
        self.assertEqual(tokens, [token_1])
        self.assertEqual(database.spanner_api.partition_query.call_count, 1)

    async def test_partition_read_errors(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):  # not multi_use
            await snapshot.partition_read(TABLE_NAME, COLUMNS, None)

        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._transaction_id = None
        with self.assertRaises(ValueError):  # not begun
            await snapshot.partition_read(TABLE_NAME, COLUMNS, None)

    async def test_partition_query_errors(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):  # not multi_use
            await snapshot.partition_query(SQL_QUERY)

        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._transaction_id = None
        with self.assertRaises(ValueError):  # not begun
            await snapshot.partition_query(SQL_QUERY)

    async def test_snapshot_constructor_errors(self):
        with self.assertRaises(ValueError):
            Snapshot(_Session(), read_timestamp=TIMESTAMP, exact_staleness=DURATION)

        with self.assertRaises(ValueError):
            Snapshot(_Session(), multi_use=True, min_read_timestamp=TIMESTAMP)

    async def test_snapshot_read_only_default(self):
        snapshot = self._make_snapshot(_Session())
        self.assertTrue(snapshot._read_only)

    async def test_snapshot_begin_errors(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        with self.assertRaises(ValueError):
            await snapshot.begin()

        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            await snapshot.begin()

    async def test_snapshot_precommit_token(self):
        from google.cloud.spanner_v1.types import MultiplexedSessionPrecommitToken

        snapshot = self._make_snapshot(_Session())
        token = MultiplexedSessionPrecommitToken(seq_num=1)
        await snapshot._update_for_precommit_token_pb(token)
        self.assertEqual(snapshot._precommit_token, token)

        # Newer token
        token2 = MultiplexedSessionPrecommitToken(seq_num=2)
        await snapshot._update_for_precommit_token_pb(token2)
        self.assertEqual(snapshot._precommit_token, token2)

        # Older token ignored
        await snapshot._update_for_precommit_token_pb(token)
        self.assertEqual(snapshot._precommit_token, token2)

    async def test_restart_on_unavailable_w_transaction_retry(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from google.cloud.spanner_v1.types import TransactionSelector

        request = mock.Mock(resume_token=b"", spec=["resume_token", "transaction"])

        # Second call succeeds
        partial_result_set = PartialResultSet()
        iterator = _MockIterator(partial_result_set)

        # First call fails
        fail_iterator = _MockIterator(
            fail_after=True, error=ServiceUnavailable("failed")
        )
        method = mock.AsyncMock(side_effect=[fail_iterator, iterator])

        database = _Database()
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        # Mock transaction and transaction selector
        transaction = mock.Mock()
        selector_pb = TransactionSelector(id=TXN_ID)
        transaction._build_transaction_selector_pb.return_value = selector_pb

        results = _restart_on_unavailable(
            method,
            request,
            metadata=[],
            trace_name="test",
            session=session,
            attributes={},
            transaction=transaction,  # Passing transaction instead of snapshot to trigger selector build
            transaction_selector=selector_pb,
            observability_options=None,
            request_id_manager=database,
            resource_info=None,
        )

        async for _ in results:
            pass

        self.assertEqual(method.call_count, 2)
        transaction._build_transaction_selector_pb.assert_called()
        self.assertEqual(request.transaction, selector_pb)

    async def test_restart_on_unavailable_resumable_internal_error(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable
        from google.cloud.spanner_v1.types import TransactionSelector

        request = mock.Mock(resume_token=b"", spec=["resume_token", "transaction"])

        # Resumable error message
        error = InternalServerError("RST_STREAM")

        # Second call succeeds
        partial_result_set = PartialResultSet()
        iterator = _MockIterator(partial_result_set)

        # First call fails
        fail_iterator = _MockIterator(fail_after=True, error=error)
        method = mock.AsyncMock(side_effect=[fail_iterator, iterator])

        database = _Database()
        session = _Session(database)
        transaction = mock.Mock()
        selector_pb = TransactionSelector(id=TXN_ID)
        transaction._build_transaction_selector_pb.return_value = selector_pb

        results = _restart_on_unavailable(
            method,
            request,
            metadata=[],
            trace_name="test",
            session=session,
            attributes={},
            transaction=transaction,
            transaction_selector=selector_pb,
            observability_options=None,
            request_id_manager=database,
            resource_info=None,
        )

        async for _ in results:
            pass

        self.assertEqual(method.call_count, 2)
        transaction._build_transaction_selector_pb.assert_called()

    async def test_restart_on_unavailable_generic_exception(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable

        request = mock.Mock(resume_token=b"", spec=["resume_token", "transaction"])
        method = mock.AsyncMock(side_effect=RuntimeError("unexpected"))

        database = _Database()
        session = _Session(database)

        results = _restart_on_unavailable(
            method,
            request,
            metadata=[],
            trace_name="test",
            session=session,
            attributes={},
            transaction=None,
            transaction_selector=TransactionSelector(id=TXN_ID),
            observability_options=None,
            request_id_manager=database,
            resource_info=None,
        )

        with self.assertRaises(RuntimeError):
            async for _ in results:
                pass

    async def test_restart_on_unavailable_unexpected_exception(self):
        from google.cloud.spanner_v1._async.snapshot import _restart_on_unavailable

        # Use InternalServerError because wrap_with_request_id only augments GoogleAPICallError
        method = mock.AsyncMock(side_effect=InternalServerError("unexpected"))
        request = mock.Mock()
        request_id_manager = mock.Mock()
        request_id_manager.metadata_and_request_id.return_value = (None, "req-id")

        with self.assertRaises(InternalServerError) as exc:
            # args: method, request, metadata, trace_name, session, attributes, transaction, transaction_selector, observability_options, request_id_manager, resource_info
            gen = _restart_on_unavailable(
                method,
                request,
                None,
                None,
                None,
                None,
                None,
                mock.Mock(),
                None,
                request_id_manager,
                None,
            )
            async for _ in gen:
                pass
        self.assertIn("req-id", str(exc.exception))

    async def test_read_w_request_options_dict(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        api.streaming_read.return_value = _MockIterator(PartialResultSet())
        from google.cloud.spanner_v1.keyset import KeySet

        results = await snapshot.read(
            TABLE_NAME, COLUMNS, KeySet(all_=True), request_options={"priority": 1}
        )
        async for _ in results:
            pass

        call_args = api.streaming_read.call_args
        self.assertEqual(call_args.kwargs["request"].request_options.priority, 1)

    async def test_read_w_directed_read_options(self):
        from google.cloud.spanner_v1.types import DirectedReadOptions

        database = _Database()
        database._directed_read_options = DirectedReadOptions()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        api.streaming_read.return_value = _MockIterator(PartialResultSet())
        from google.cloud.spanner_v1.keyset import KeySet

        results = await snapshot.read(TABLE_NAME, COLUMNS, KeySet(all_=True))
        async for _ in results:
            pass

        call_args = api.streaming_read.call_args
        self.assertIsNotNone(call_args.kwargs["request"].directed_read_options)

    async def test_read_w_transaction_tag(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID
        snapshot.transaction_tag = "tag"
        # Bypassing _read_only=True check which explicitly clears transaction_tag in snapshot.py
        snapshot._read_only = False

        api.streaming_read.return_value = _MockIterator(PartialResultSet())
        from google.cloud.spanner_v1.keyset import KeySet

        # Passing an explicit empty dict to ensure it's not None if that's causing issues
        results = await snapshot.read(
            TABLE_NAME, COLUMNS, KeySet(all_=True), request_options={}
        )
        async for _ in results:
            pass

        call_args = api.streaming_read.call_args
        self.assertIsNotNone(call_args, "streaming_read should have been called")
        self.assertEqual(
            call_args.kwargs["request"].request_options.transaction_tag, "tag"
        )

    async def test_execute_sql_w_request_options_dict(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(SQL_QUERY, request_options={"priority": 1})
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        self.assertEqual(call_args.kwargs["request"].request_options.priority, 1)

    async def test_execute_sql_w_partition(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(SQL_QUERY, partition=b"token")
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        self.assertEqual(call_args.kwargs["request"].partition_token, b"token")

    async def test_execute_sql_not_begun_error(self):
        session = _Session()
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._read_request_count = 1
        snapshot._transaction_id = None
        with self.assertRaises(ValueError):
            await snapshot.execute_sql(SQL_QUERY)

    async def test_execute_sql_w_params(self):
        from google.cloud.spanner_v1.param_types import INT64

        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(
            SQL_QUERY, params={"id": 1}, param_types={"id": INT64}
        )
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        # ExecuteSqlRequest might wrap params in a way that fields are not directly accessible
        # so we just check if it's there
        self.assertTrue(hasattr(call_args.kwargs["request"], "params"))
        self.assertIn("id", call_args.kwargs["request"].params)

    async def test_execute_sql_w_route_to_leader(self):
        database = _Database()
        database._route_to_leader_enabled = True
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID
        snapshot._read_only = False  # Force route to leader check
        snapshot.transaction_tag = None  # Add missing attribute

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(SQL_QUERY)
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        metadata = call_args.kwargs.get("metadata", [])
        metadata_dict = dict(metadata) if metadata else {}
        self.assertIn("x-goog-spanner-route-to-leader", metadata_dict)

    async def test_execute_sql_w_directed_read_options(self):
        from google.cloud.spanner_v1.types import DirectedReadOptions

        database = _Database()
        database._directed_read_options = DirectedReadOptions()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID
        snapshot._read_only = True

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(SQL_QUERY)
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        self.assertIsNotNone(call_args.kwargs["request"].directed_read_options)

    async def test_execute_sql_w_transaction_tag(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session)
        snapshot._transaction_id = TXN_ID
        snapshot.transaction_tag = "tag"
        snapshot._read_only = False

        api.execute_streaming_sql.return_value = _MockIterator(PartialResultSet())
        results = await snapshot.execute_sql(SQL_QUERY, request_options={})
        async for _ in results:
            pass

        call_args = api.execute_streaming_sql.call_args
        self.assertEqual(
            call_args.kwargs["request"].request_options.transaction_tag, "tag"
        )

    def test_ctor_incompatible_options(self):
        import datetime

        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        session = _Session()
        with self.assertRaises(ValueError):
            self._make_snapshot(
                session,
                read_timestamp=timestamp,
                exact_staleness=datetime.timedelta(seconds=10),
            )

    def test_ctor_multi_use_incompatible_options(self):
        import datetime

        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        session = _Session()
        with self.assertRaises(ValueError):
            self._make_snapshot(session, multi_use=True, min_read_timestamp=timestamp)

    def test_build_transaction_options_pb_timestamp(self):
        import datetime

        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        session = _Session()
        snapshot = self._make_snapshot(session, read_timestamp=timestamp)
        pb = snapshot._build_transaction_options_pb()
        self.assertEqual(pb.read_only.read_timestamp, timestamp)

    def test_build_transaction_options_pb_min_read_timestamp(self):
        import datetime

        timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        session = _Session()
        snapshot = self._make_snapshot(session, min_read_timestamp=timestamp)
        pb = snapshot._build_transaction_options_pb()
        self.assertEqual(pb.read_only.min_read_timestamp, timestamp)

    def test_build_transaction_options_pb_max_staleness(self):
        import datetime

        duration = datetime.timedelta(seconds=10)
        session = _Session()
        snapshot = self._make_snapshot(session, max_staleness=duration)
        pb = snapshot._build_transaction_options_pb()
        self.assertEqual(pb.read_only.max_staleness, duration)

    def test_build_transaction_options_pb_exact_staleness(self):
        import datetime

        duration = datetime.timedelta(seconds=10)
        session = _Session()
        snapshot = self._make_snapshot(session, exact_staleness=duration)
        pb = snapshot._build_transaction_options_pb()
        self.assertEqual(pb.read_only.exact_staleness, duration)

    async def test_partition_read_not_multi_use(self):
        from google.cloud.spanner_v1.keyset import KeySet

        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            await snapshot.partition_read(TABLE_NAME, COLUMNS, KeySet(all_=True))

    async def test_partition_query_not_multi_use(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            await snapshot.partition_query(SQL_QUERY)

    async def test_begin_transaction_reuse_error(self):
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            await snapshot.begin()

    async def test_snapshot_precommit_token_unsafe(self):
        from google.cloud.spanner_v1.types import MultiplexedSessionPrecommitToken

        snapshot = self._make_snapshot(_Session())
        token = MultiplexedSessionPrecommitToken(seq_num=1)
        snapshot._update_for_precommit_token_pb_unsafe(token)
        self.assertEqual(snapshot._precommit_token, token)

    async def test_get_streamed_result_set_inline_begin_success(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = None  # Trigger inline begin

        from google.cloud.spanner_v1.types import ResultSetMetadata
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        # Metadata with transaction
        metadata = ResultSetMetadata(transaction=TransactionPB(id=TXN_ID))
        partial_result_set = PartialResultSet(metadata=metadata)

        api.execute_streaming_sql.return_value = _MockIterator(partial_result_set)
        results = await snapshot.execute_sql(SQL_QUERY)
        async for _ in results:
            pass

        self.assertEqual(snapshot._transaction_id, TXN_ID)

    async def test_partition_read_w_index_and_leader(self):
        token_1 = b"TOKEN1"
        from google.cloud.spanner_v1.types import Partition, PartitionResponse
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database._route_to_leader_enabled = True
        database.spanner_api.partition_read = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        from google.cloud.spanner_v1.keyset import KeySet

        tokens = await snapshot.partition_read(
            TABLE_NAME, COLUMNS, KeySet(all_=True), index="idx"
        )
        self.assertEqual(tokens, [token_1])
        self.assertEqual(database.spanner_api.partition_read.call_count, 1)
        call_args = database.spanner_api.partition_read.call_args
        self.assertEqual(call_args.kwargs["request"].index, "idx")

    async def test_partition_query_w_params_and_leader(self):
        token_1 = b"TOKEN1"
        from google.cloud.spanner_v1.types import Partition, PartitionResponse
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database._route_to_leader_enabled = True
        database.spanner_api.partition_query = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        tokens = await snapshot.partition_query(SQL_QUERY, params={"a": 1})
        self.assertEqual(tokens, [token_1])
        call_args = database.spanner_api.partition_query.call_args
        self.assertIn("a", call_args.kwargs["request"].params)

    async def test_begin_transaction_exhaustive_errors(self):
        # 1. Already begun
        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._transaction_id = TXN_ID
        with self.assertRaises(ValueError):
            await snapshot._begin_transaction()

        # 2. Not multi-use
        snapshot = self._make_snapshot(_Session(), multi_use=False)
        with self.assertRaises(ValueError):
            await snapshot._begin_transaction()

        # 3. Already pending
        snapshot = self._make_snapshot(_Session(), multi_use=True)
        snapshot._read_request_count = 1
        with self.assertRaises(ValueError):
            await snapshot._begin_transaction()

    async def test_begin_transaction_w_tag_and_leader(self):
        database = _Database()
        database._route_to_leader_enabled = True
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._read_only = False

        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        api.begin_transaction.return_value = TransactionPB(id=TXN_ID)

        tid = await snapshot._begin_transaction(transaction_tag="mytag")
        self.assertEqual(tid, TXN_ID)
        call_args = api.begin_transaction.call_args
        self.assertEqual(
            call_args.kwargs["request"].request_options.transaction_tag, "mytag"
        )
        # Check leader metadata
        metadata = call_args.kwargs["metadata"]
        leader_header = ("x-goog-spanner-route-to-leader", "true")
        self.assertTrue(
            any(
                t[0] == leader_header[0] and t[1] == leader_header[1] for t in metadata
            ),
            f"Expected {leader_header} in {metadata}",
        )

    async def test_begin_transaction_retry(self):
        database = _Database()
        api = database.spanner_api
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)

        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        # Fail once, then succeed
        api.begin_transaction.side_effect = [
            InternalServerError("RST_STREAM"),
            TransactionPB(id=TXN_ID),
        ]

        tid = await snapshot._begin_transaction()
        self.assertEqual(tid, TXN_ID)
        self.assertEqual(api.begin_transaction.call_count, 2)

    async def test_update_for_transaction_pb_w_precommit_token(self):
        from google.cloud.spanner_v1.types import MultiplexedSessionPrecommitToken
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        snapshot = self._make_snapshot(_Session())
        token = MultiplexedSessionPrecommitToken(seq_num=1)
        transaction_pb = TransactionPB(id=TXN_ID, precommit_token=token)

        snapshot._update_for_transaction_pb(transaction_pb)
        self.assertEqual(snapshot._transaction_id, TXN_ID)
        self.assertEqual(snapshot._precommit_token, token)

    async def test_partition_read_w_leader_enabled(self):
        token_1 = b"TOKEN1"
        from google.cloud.spanner_v1.types import Partition, PartitionResponse
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database._route_to_leader_enabled = True
        database.spanner_api.partition_read = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        from google.cloud.spanner_v1.keyset import KeySet

        await snapshot.partition_read(TABLE_NAME, COLUMNS, KeySet(all_=True))

        call_args = database.spanner_api.partition_read.call_args
        metadata = call_args.kwargs["metadata"]
        leader_header = ("x-goog-spanner-route-to-leader", "true")
        self.assertTrue(
            any(
                t[0] == leader_header[0] and t[1] == leader_header[1] for t in metadata
            ),
            f"Expected {leader_header} in {metadata}",
        )

    async def test_partition_query_w_leader_enabled(self):
        token_1 = b"TOKEN1"
        from google.cloud.spanner_v1.types import Partition, PartitionResponse
        from google.cloud.spanner_v1.types import Transaction as TransactionPB

        response = PartitionResponse(
            partitions=[Partition(partition_token=token_1)],
            transaction=TransactionPB(id=TXN_ID),
        )
        database = _Database()
        database._route_to_leader_enabled = True
        database.spanner_api.partition_query = mock.AsyncMock(return_value=response)
        session = _Session(database)
        snapshot = self._make_snapshot(session, multi_use=True)
        snapshot._transaction_id = TXN_ID

        await snapshot.partition_query(SQL_QUERY)

        call_args = database.spanner_api.partition_query.call_args
        metadata = call_args.kwargs["metadata"]
        leader_header = ("x-goog-spanner-route-to-leader", "true")
        self.assertTrue(
            any(
                t[0] == leader_header[0] and t[1] == leader_header[1] for t in metadata
            ),
            f"Expected {leader_header} in {metadata}",
        )


class _Database(object):
    def __init__(self):
        self.name = "testing"
        self.database_id = "d"
        self._instance = mock.Mock()
        self._instance.instance_id = "i"
        self._instance._client = mock.Mock()
        self._instance._client.project = "p"
        self._instance._client._client_context = None
        self._instance._client._query_options = ExecuteSqlRequest.QueryOptions()
        self._route_to_leader_enabled = True
        self._directed_read_options = None
        self.spanner_api = mock.AsyncMock()
        self.observability_options = None
        self.query_options = ExecuteSqlRequest.QueryOptions()
        self._next_nth_request = 0

    @property
    def _resource_info(self):
        return {"project": "p", "instance": "i", "database": "d"}

    def metadata_and_request_id(self, nth_request, attempt, metadata, span):
        if metadata and not isinstance(metadata, list):
            metadata = [metadata]
        return metadata or [], "request-id"

    def metadata_with_request_id(self, nth_request, attempt, metadata, span):
        if metadata and not isinstance(metadata, list):
            metadata = [metadata]
        return metadata or []

    def with_error_augmentation(self, nth_request, attempt, metadata, span):
        return metadata or [], mock.MagicMock()


class _Session(object):
    def __init__(self, database=None):
        self._database = database or _Database()
        self.name = "session-name"


class _MockIterator(object):
    def __init__(self, *values, fail_after=False, error=None):
        self._values = list(values)
        self._exception = error
        self._fail_after = fail_after

    def set_exception(self, exc):
        self._exception = exc

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._fail_after and self._exception:
            if not self._values:
                exc, self._exception = self._exception, None
                raise exc
        elif self._exception and not self._values:
            exc, self._exception = self._exception, None
            raise exc

        if self._values:
            return self._values.pop(0)

        if self._exception:
            exc, self._exception = self._exception, None
            raise exc

        raise StopAsyncIteration
