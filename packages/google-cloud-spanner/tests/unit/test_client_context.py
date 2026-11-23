# Copyright 2026 Google LLC All rights reserved.
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

import threading
import unittest
from unittest import mock

from google.protobuf import struct_pb2

from google.cloud.spanner_v1._helpers import (
    _merge_client_context,
    _merge_request_options,
)
from google.cloud.spanner_v1.types import (
    ExecuteSqlRequest,
    RequestOptions,
)


class TestClientContext(unittest.TestCase):
    def test__merge_client_context_both_none(self):
        self.assertIsNone(_merge_client_context(None, None))

    def test__merge_client_context_base_none(self):
        merge = RequestOptions.ClientContext(
            secure_context={"a": struct_pb2.Value(string_value="A")}
        )
        result = _merge_client_context(None, merge)
        self.assertEqual(result.secure_context["a"], "A")

    def test__merge_client_context_merge_none(self):
        base = RequestOptions.ClientContext(
            secure_context={"a": struct_pb2.Value(string_value="A")}
        )
        result = _merge_client_context(base, None)
        self.assertEqual(result.secure_context["a"], "A")

    def test__merge_client_context_both_set(self):
        base = RequestOptions.ClientContext(
            secure_context={
                "a": struct_pb2.Value(string_value="A"),
                "b": struct_pb2.Value(string_value="B1"),
            }
        )
        merge = RequestOptions.ClientContext(
            secure_context={
                "b": struct_pb2.Value(string_value="B2"),
                "c": struct_pb2.Value(string_value="C"),
            }
        )
        result = _merge_client_context(base, merge)
        self.assertEqual(result.secure_context["a"], "A")
        self.assertEqual(result.secure_context["b"], "B2")
        self.assertEqual(result.secure_context["c"], "C")

    def test__merge_request_options_with_client_context(self):
        request_options = RequestOptions(priority=RequestOptions.Priority.PRIORITY_LOW)
        client_context = RequestOptions.ClientContext(
            secure_context={"a": struct_pb2.Value(string_value="A")}
        )

        result = _merge_request_options(request_options, client_context)

        self.assertEqual(result.priority, RequestOptions.Priority.PRIORITY_LOW)
        self.assertEqual(result.client_context.secure_context["a"], "A")

    def test_client_init_with_client_context(self):
        from google.cloud.spanner_v1.client import Client

        project = "PROJECT"
        credentials = mock.Mock(spec=["_resource_prefix__"])
        with (
            mock.patch("google.auth.default", return_value=(credentials, project)),
            mock.patch(
                "google.cloud.spanner_v1.client._get_spanner_enable_builtin_metrics_env",
                return_value=False,
            ),
        ):
            client_context = {
                "secure_context": {"a": struct_pb2.Value(string_value="A")}
            }
            client = Client(
                project=project,
                client_context=client_context,
                disable_builtin_metrics=True,
            )

        self.assertIsInstance(client._client_context, RequestOptions.ClientContext)
        self.assertEqual(client._client_context.secure_context["a"], "A")

    def test_snapshot_execute_sql_propagates_client_context(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        session = mock.Mock(spec=["name", "_database"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database._directed_read_options = None

        client = database._instance._client = mock.Mock()
        client._query_options = None
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        snapshot_context = RequestOptions.ClientContext(
            secure_context={"snapshot": struct_pb2.Value(string_value="from-snapshot")}
        )
        snapshot = Snapshot(session, client_context=snapshot_context)

        with mock.patch.object(snapshot, "_get_streamed_result_set") as mocked:
            snapshot.execute_sql("SELECT 1")
            kwargs = mocked.call_args.kwargs
            request = kwargs["request"]
            self.assertIsInstance(request, ExecuteSqlRequest)
            self.assertEqual(
                request.request_options.client_context.secure_context["client"],
                "from-client",
            )
            self.assertEqual(
                request.request_options.client_context.secure_context["snapshot"],
                "from-snapshot",
            )

    def test_transaction_commit_propagates_client_context(self):
        from google.cloud.spanner_v1.transaction import Transaction
        from google.cloud.spanner_v1.types import (
            CommitRequest,
            CommitResponse,
            MultiplexedSessionPrecommitToken,
        )

        session = mock.Mock(spec=["name", "_database", "is_multiplexed"])
        session.name = "session-name"
        session.is_multiplexed = False
        database = session._database = mock.Mock()
        database.name = "projects/p/instances/i/databases/d"
        database._route_to_leader_enabled = False
        database.log_commit_stats = False
        database.with_error_augmentation.return_value = (None, mock.MagicMock())
        database._next_nth_request = 1

        client = database._instance._client = mock.Mock()
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        transaction_context = RequestOptions.ClientContext(
            secure_context={"txn": struct_pb2.Value(string_value="from-txn")}
        )
        transaction = Transaction(session, client_context=transaction_context)
        transaction._transaction_id = b"tx-id"

        api = database.spanner_api = mock.Mock()

        token = MultiplexedSessionPrecommitToken(seq_num=1)
        response = CommitResponse(precommit_token=token)

        def side_effect(f, **kw):
            return f()

        api.commit.return_value = response

        with mock.patch(
            "google.cloud.spanner_v1.transaction._retry", side_effect=side_effect
        ):
            transaction.commit()

        args, kwargs = api.commit.call_args
        request = kwargs["request"]
        self.assertIsInstance(request, CommitRequest)
        self.assertEqual(
            request.request_options.client_context.secure_context["client"],
            "from-client",
        )
        self.assertEqual(
            request.request_options.client_context.secure_context["txn"], "from-txn"
        )

    def test_snapshot_execute_sql_request_level_override(self):
        from google.cloud.spanner_v1.snapshot import Snapshot

        session = mock.Mock(spec=["name", "_database"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database._directed_read_options = None

        client = database._instance._client = mock.Mock()
        client._query_options = None
        client._client_context = RequestOptions.ClientContext(
            secure_context={"a": struct_pb2.Value(string_value="from-client")}
        )

        snapshot_context = RequestOptions.ClientContext(
            secure_context={
                "a": struct_pb2.Value(string_value="from-snapshot"),
                "b": struct_pb2.Value(string_value="B"),
            }
        )
        snapshot = Snapshot(session, client_context=snapshot_context)

        request_options = RequestOptions(
            client_context=RequestOptions.ClientContext(
                secure_context={"a": struct_pb2.Value(string_value="from-request")}
            )
        )

        with mock.patch.object(snapshot, "_get_streamed_result_set") as mocked:
            snapshot.execute_sql("SELECT 1", request_options=request_options)
            kwargs = mocked.call_args.kwargs
            request = kwargs["request"]
            self.assertEqual(
                request.request_options.client_context.secure_context["a"],
                "from-request",
            )
            self.assertEqual(
                request.request_options.client_context.secure_context["b"], "B"
            )

    def test_batch_commit_propagates_client_context(self):
        from google.cloud.spanner_v1 import DefaultTransactionOptions
        from google.cloud.spanner_v1.batch import Batch
        from google.cloud.spanner_v1.types import CommitRequest, CommitResponse

        session = mock.Mock(spec=["name", "_database"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database.log_commit_stats = False
        database.default_transaction_options = DefaultTransactionOptions()
        database.with_error_augmentation.return_value = (None, mock.MagicMock())
        database._next_nth_request = 1
        client = database._instance._client = mock.Mock()
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        batch_context = RequestOptions.ClientContext(
            secure_context={"batch": struct_pb2.Value(string_value="from-batch")}
        )
        batch = Batch(session, client_context=batch_context)

        api = database.spanner_api = mock.Mock()
        response = CommitResponse()
        api.commit.return_value = response

        batch.commit()

        args, kwargs = api.commit.call_args
        request = kwargs["request"]
        self.assertIsInstance(request, CommitRequest)
        self.assertEqual(
            request.request_options.client_context.secure_context["client"],
            "from-client",
        )
        self.assertEqual(
            request.request_options.client_context.secure_context["batch"], "from-batch"
        )

    def test_transaction_execute_update_propagates_client_context(self):
        from google.cloud.spanner_v1.transaction import Transaction
        from google.cloud.spanner_v1.types import (
            ExecuteSqlRequest,
            MultiplexedSessionPrecommitToken,
            ResultSet,
        )

        session = mock.Mock(spec=["name", "_database", "_precommit_token"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database.with_error_augmentation.return_value = (None, mock.MagicMock())
        database._next_nth_request = 1

        client = database._instance._client = mock.Mock()
        client._query_options = None
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        transaction_context = RequestOptions.ClientContext(
            secure_context={"txn": struct_pb2.Value(string_value="from-txn")}
        )
        transaction = Transaction(session, client_context=transaction_context)
        transaction._transaction_id = b"tx-id"
        transaction._precommit_token = MultiplexedSessionPrecommitToken(seq_num=1)

        database.spanner_api = mock.Mock()
        response = ResultSet(
            precommit_token=MultiplexedSessionPrecommitToken(seq_num=2)
        )

        with mock.patch.object(transaction, "_execute_request", return_value=response):
            transaction.execute_update("UPDATE T SET C = 1")

            args, kwargs = transaction._execute_request.call_args
            request = args[1]
            self.assertIsInstance(request, ExecuteSqlRequest)
            self.assertEqual(
                request.request_options.client_context.secure_context["client"],
                "from-client",
            )
            self.assertEqual(
                request.request_options.client_context.secure_context["txn"], "from-txn"
            )

    def test_mutation_groups_batch_write_propagates_client_context(self):
        from google.cloud.spanner_v1.batch import MutationGroups
        from google.cloud.spanner_v1.types import BatchWriteRequest

        session = mock.Mock(spec=["name", "_database"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database.with_error_augmentation.return_value = (None, mock.MagicMock())
        database.metadata_with_request_id.return_value = []
        database._next_nth_request = 1

        client = database._instance._client = mock.Mock()
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        mg_context = RequestOptions.ClientContext(
            secure_context={"mg": struct_pb2.Value(string_value="from-mg")}
        )
        mg = MutationGroups(session, client_context=mg_context)

        api = database.spanner_api = mock.Mock()

        with mock.patch(
            "google.cloud.spanner_v1._helpers._retry", side_effect=lambda f, **kw: f()
        ):
            mg.batch_write()

        args, kwargs = api.batch_write.call_args
        request = kwargs["request"]
        self.assertIsInstance(request, BatchWriteRequest)
        self.assertEqual(
            request.request_options.client_context.secure_context["client"],
            "from-client",
        )
        self.assertEqual(
            request.request_options.client_context.secure_context["mg"], "from-mg"
        )

    def test_batch_snapshot_propagates_client_context(self):
        from google.cloud.spanner_v1.database import BatchSnapshot

        database = mock.Mock()
        database.name = "database-name"
        client = database._instance._client = mock.Mock()
        client._query_options = None
        client._client_context = RequestOptions.ClientContext(
            secure_context={"client": struct_pb2.Value(string_value="from-client")}
        )

        batch_context = RequestOptions.ClientContext(
            secure_context={"batch": struct_pb2.Value(string_value="from-batch")}
        )
        batch_snapshot = BatchSnapshot(database, client_context=batch_context)

        session = mock.Mock(spec=["name", "_database", "session_id", "snapshot"])
        session.name = "session-name"
        session.session_id = "session-id"
        database.sessions_manager.get_session.return_value = session

        snapshot = mock.Mock()
        session.snapshot.return_value = snapshot

        batch_snapshot.execute_sql("SELECT 1")

        session.snapshot.assert_called_once()
        kwargs = session.snapshot.call_args.kwargs
        self.assertEqual(kwargs["client_context"], batch_context)

    def test_database_snapshot_propagates_client_context(self):
        from google.cloud.spanner_v1.database import Database

        instance = mock.Mock()
        instance._client = mock.Mock()
        instance._client._query_options = None
        instance._client._client_context = None

        database = Database("db", instance)
        with mock.patch(
            "google.cloud.spanner_v1.database.SnapshotCheckout"
        ) as mocked_checkout:
            client_context = {
                "secure_context": {"a": struct_pb2.Value(string_value="A")}
            }
            database.snapshot(client_context=client_context)

            mocked_checkout.assert_called_once_with(
                database, client_context=client_context
            )

    def test_transaction_rollback_propagates_client_context_is_not_supported(self):
        # Verify that rollback DOES NOT take client_context as it's not in RollbackRequest
        from google.cloud.spanner_v1.transaction import Transaction

        session = mock.Mock(spec=["name", "_database"])
        session.name = "session-name"
        database = session._database = mock.Mock()
        database.name = "database-name"
        database._route_to_leader_enabled = False
        database.with_error_augmentation.return_value = (None, mock.MagicMock())
        database._next_nth_request = 1

        transaction = Transaction(session)
        transaction._transaction_id = b"tx-id"

        api = database.spanner_api = mock.Mock()

        transaction.rollback()

        args, kwargs = api.rollback.call_args
        self.assertEqual(kwargs["session"], "session-name")
        self.assertEqual(kwargs["transaction_id"], b"tx-id")
        # Ensure no request_options or client_context passed to rollback
        self.assertNotIn("request_options", kwargs)

    def test__merge_request_options_does_not_mutate_shared_instance(self):
        shared_options = RequestOptions(priority=RequestOptions.Priority.PRIORITY_LOW)
        ctx_a = RequestOptions.ClientContext(
            secure_context={
                "tenant": struct_pb2.Value(string_value="A"),
                "only_a": struct_pb2.Value(string_value="secret"),
            }
        )
        ctx_b = RequestOptions.ClientContext(
            secure_context={"tenant": struct_pb2.Value(string_value="B")}
        )

        result_a = _merge_request_options(shared_options, ctx_a)
        result_b = _merge_request_options(shared_options, ctx_b)

        self.assertIsNot(result_a, shared_options)
        self.assertIsNot(result_b, shared_options)
        self.assertNotIn("client_context", shared_options)
        self.assertEqual(result_a.priority, RequestOptions.Priority.PRIORITY_LOW)
        self.assertEqual(
            dict(result_a.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(result_b.priority, RequestOptions.Priority.PRIORITY_LOW)
        self.assertEqual(
            dict(result_b.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertNotIn("only_a", result_b.client_context.secure_context)

    def test__merge_request_options_input_matrix(self):
        ctx_snapshot = RequestOptions.ClientContext(
            secure_context={
                "a": struct_pb2.Value(string_value="from-snapshot"),
                "b": struct_pb2.Value(string_value="B"),
            }
        )

        # (None, None) preserves the zero-allocation fast path.
        self.assertIsNone(_merge_request_options(None, None))

        # (None, ctx) allocates a fresh RequestOptions carrying ctx.
        from_none = _merge_request_options(None, ctx_snapshot)
        self.assertIsInstance(from_none, RequestOptions)
        self.assertEqual(
            dict(from_none.client_context.secure_context),
            {"a": "from-snapshot", "b": "B"},
        )

        # Proto-plus RequestOptions with explicit request-level client_context:
        # request-level keys override snapshot keys without mutating caller input.
        caller_options = RequestOptions(
            priority=RequestOptions.Priority.PRIORITY_MEDIUM,
            client_context=RequestOptions.ClientContext(
                secure_context={"a": struct_pb2.Value(string_value="from-request")}
            ),
        )
        merged_proto = _merge_request_options(caller_options, ctx_snapshot)
        self.assertIsNot(merged_proto, caller_options)
        self.assertEqual(
            dict(merged_proto.client_context.secure_context),
            {"a": "from-request", "b": "B"},
        )
        self.assertEqual(
            dict(caller_options.client_context.secure_context),
            {"a": "from-request"},
        )

        # Raw protobuf RequestOptions input is cloned without mutating raw_pb.
        raw_pb = RequestOptions.pb()(
            priority=RequestOptions.Priority.PRIORITY_HIGH,
            request_tag="raw-tag",
        )
        merged_raw = _merge_request_options(raw_pb, ctx_snapshot)
        self.assertIsInstance(merged_raw, RequestOptions)
        self.assertEqual(merged_raw.priority, RequestOptions.Priority.PRIORITY_HIGH)
        self.assertEqual(merged_raw.request_tag, "raw-tag")
        self.assertEqual(
            dict(merged_raw.client_context.secure_context),
            {"a": "from-snapshot", "b": "B"},
        )
        self.assertFalse(raw_pb.HasField("client_context"))

        # dict subclass input is normalized without mutating the dict.
        class _OptionsDict(dict):
            pass

        dict_sub = _OptionsDict(
            priority=RequestOptions.Priority.PRIORITY_LOW,
            request_tag="dict-tag",
        )
        merged_dict = _merge_request_options(dict_sub, ctx_snapshot)
        self.assertEqual(merged_dict.priority, RequestOptions.Priority.PRIORITY_LOW)
        self.assertEqual(merged_dict.request_tag, "dict-tag")
        self.assertEqual(
            dict(merged_dict.client_context.secure_context),
            {"a": "from-snapshot", "b": "B"},
        )
        self.assertNotIn("client_context", dict_sub)

        # Malformed input fails closed with TypeError even when client_context is None.
        with self.assertRaises(TypeError):
            _merge_request_options(123, None)
        with self.assertRaises(TypeError):
            _merge_request_options(123, ctx_snapshot)

    def test__merge_request_options_clones_when_client_context_none(self):
        shared_options = RequestOptions(
            priority=RequestOptions.Priority.PRIORITY_LOW,
            request_tag="req-1",
            transaction_tag="txn-1",
        )
        result = _merge_request_options(shared_options, None)

        self.assertIsNot(result, shared_options)
        self.assertEqual(result, shared_options)

        result.transaction_tag = "mutated-txn"
        result.request_tag = None

        self.assertEqual(shared_options.transaction_tag, "txn-1")
        self.assertEqual(shared_options.request_tag, "req-1")

    def test_snapshot_transaction_batch_reuse_shared_request_options(self):
        from google.cloud.spanner_v1 import DefaultTransactionOptions, KeySet
        from google.cloud.spanner_v1.batch import Batch, MutationGroups
        from google.cloud.spanner_v1.snapshot import Snapshot
        from google.cloud.spanner_v1.transaction import Transaction
        from google.cloud.spanner_v1.types import (
            CommitResponse,
            ExecuteBatchDmlResponse,
            MultiplexedSessionPrecommitToken,
            ResultSet,
        )

        shared_options = RequestOptions(
            priority=RequestOptions.Priority.PRIORITY_LOW,
            request_tag="req-orig",
            transaction_tag="txn-orig",
        )
        ctx_a = RequestOptions.ClientContext(
            secure_context={
                "tenant": struct_pb2.Value(string_value="A"),
                "only_a": struct_pb2.Value(string_value="secret"),
            }
        )
        ctx_b = RequestOptions.ClientContext(
            secure_context={"tenant": struct_pb2.Value(string_value="B")}
        )

        def _make_session():
            session = mock.Mock(
                spec=["name", "_database", "is_multiplexed", "_precommit_token"]
            )
            session.name = "session-name"
            session.is_multiplexed = False
            database = session._database = mock.Mock()
            database.name = "projects/p/instances/i/databases/d"
            database._route_to_leader_enabled = False
            database._directed_read_options = None
            database.log_commit_stats = False
            database.default_transaction_options = DefaultTransactionOptions()
            database.with_error_augmentation.return_value = (None, mock.MagicMock())
            database.metadata_with_request_id.return_value = []
            database._next_nth_request = 1
            client = database._instance._client = mock.Mock()
            client._query_options = None
            client._client_context = None
            return session, database

        def _assert_shared_untouched():
            self.assertEqual(
                shared_options.priority, RequestOptions.Priority.PRIORITY_LOW
            )
            self.assertEqual(shared_options.request_tag, "req-orig")
            self.assertEqual(shared_options.transaction_tag, "txn-orig")
            self.assertNotIn("client_context", shared_options)

        # 1. Snapshot.execute_sql across tenant A and tenant B
        session, _ = _make_session()
        snap_a = Snapshot(session, client_context=ctx_a)
        snap_b = Snapshot(session, client_context=ctx_b)
        with mock.patch.object(snap_a, "_get_streamed_result_set") as mock_a:
            snap_a.execute_sql("SELECT 1", request_options=shared_options)
            req_a = mock_a.call_args.kwargs["request"]
        with mock.patch.object(snap_b, "_get_streamed_result_set") as mock_b:
            snap_b.execute_sql("SELECT 1", request_options=shared_options)
            req_b = mock_b.call_args.kwargs["request"]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "")
        self.assertEqual(req_b.request_options.transaction_tag, "")
        _assert_shared_untouched()

        # 2. Snapshot.read across tenant A and tenant B
        snap_read_a = Snapshot(session, client_context=ctx_a)
        snap_read_b = Snapshot(session, client_context=ctx_b)
        with mock.patch.object(snap_read_a, "_get_streamed_result_set") as mock_a:
            snap_read_a.read(
                "T", ["c"], KeySet(all_=True), request_options=shared_options
            )
            req_a = mock_a.call_args.kwargs["request"]
        with mock.patch.object(snap_read_b, "_get_streamed_result_set") as mock_b:
            snap_read_b.read(
                "T", ["c"], KeySet(all_=True), request_options=shared_options
            )
            req_b = mock_b.call_args.kwargs["request"]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "")
        self.assertEqual(req_b.request_options.transaction_tag, "")
        _assert_shared_untouched()

        # 3. Transaction.commit across tenant A and tenant B
        session, database = _make_session()
        database.spanner_api.commit.return_value = CommitResponse(
            precommit_token=MultiplexedSessionPrecommitToken(seq_num=1)
        )
        txn_a = Transaction(session, client_context=ctx_a)
        txn_a._transaction_id = b"tx-a"
        txn_a.transaction_tag = "txn-a"
        txn_b = Transaction(session, client_context=ctx_b)
        txn_b._transaction_id = b"tx-b"
        txn_b.transaction_tag = "txn-b"
        with mock.patch(
            "google.cloud.spanner_v1.transaction._retry",
            side_effect=lambda f, **kw: f(),
        ):
            txn_a.commit(request_options=shared_options)
            req_a = database.spanner_api.commit.call_args.kwargs["request"]
            txn_b.commit(request_options=shared_options)
            req_b = database.spanner_api.commit.call_args.kwargs["request"]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "txn-a")
        self.assertEqual(req_b.request_options.transaction_tag, "txn-b")
        self.assertEqual(req_a.request_options.request_tag, "")
        self.assertEqual(req_b.request_options.request_tag, "")
        _assert_shared_untouched()

        # 4. Transaction.execute_update across tenant A and tenant B
        session, _ = _make_session()
        txn_upd_a = Transaction(session, client_context=ctx_a)
        txn_upd_a._transaction_id = b"tx-a"
        txn_upd_a.transaction_tag = "upd-a"
        txn_upd_b = Transaction(session, client_context=ctx_b)
        txn_upd_b._transaction_id = b"tx-b"
        txn_upd_b.transaction_tag = "upd-b"
        rs = ResultSet(precommit_token=MultiplexedSessionPrecommitToken(seq_num=2))
        with mock.patch.object(txn_upd_a, "_execute_request", return_value=rs) as m_a:
            txn_upd_a.execute_update(
                "UPDATE T SET C = 1", request_options=shared_options
            )
            req_a = m_a.call_args.args[1]
        with mock.patch.object(txn_upd_b, "_execute_request", return_value=rs) as m_b:
            txn_upd_b.execute_update(
                "UPDATE T SET C = 1", request_options=shared_options
            )
            req_b = m_b.call_args.args[1]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "upd-a")
        self.assertEqual(req_b.request_options.transaction_tag, "upd-b")
        _assert_shared_untouched()

        # 5. Transaction.batch_update across tenant A and tenant B
        session, _ = _make_session()
        txn_bu_a = Transaction(session, client_context=ctx_a)
        txn_bu_a._transaction_id = b"tx-a"
        txn_bu_a.transaction_tag = "bu-a"
        txn_bu_b = Transaction(session, client_context=ctx_b)
        txn_bu_b._transaction_id = b"tx-b"
        txn_bu_b.transaction_tag = "bu-b"
        bu_resp = ExecuteBatchDmlResponse()
        with mock.patch.object(
            txn_bu_a, "_execute_request", return_value=bu_resp
        ) as m_a:
            txn_bu_a.batch_update(
                ["UPDATE T SET C = 1"], request_options=shared_options
            )
            req_a = m_a.call_args.args[1]
        with mock.patch.object(
            txn_bu_b, "_execute_request", return_value=bu_resp
        ) as m_b:
            txn_bu_b.batch_update(
                ["UPDATE T SET C = 1"], request_options=shared_options
            )
            req_b = m_b.call_args.args[1]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "bu-a")
        self.assertEqual(req_b.request_options.transaction_tag, "bu-b")
        _assert_shared_untouched()

        # 6. Batch.commit across tenant A and tenant B
        session, database = _make_session()
        database.spanner_api.commit.return_value = CommitResponse()
        batch_a = Batch(session, client_context=ctx_a)
        batch_a.transaction_tag = "batch-a"
        batch_b = Batch(session, client_context=ctx_b)
        batch_b.transaction_tag = "batch-b"
        batch_a.commit(request_options=shared_options)
        req_a = database.spanner_api.commit.call_args.kwargs["request"]
        batch_b.commit(request_options=shared_options)
        req_b = database.spanner_api.commit.call_args.kwargs["request"]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        self.assertEqual(req_a.request_options.transaction_tag, "batch-a")
        self.assertEqual(req_b.request_options.transaction_tag, "batch-b")
        self.assertEqual(req_a.request_options.request_tag, "")
        self.assertEqual(req_b.request_options.request_tag, "")
        _assert_shared_untouched()

        # 7. MutationGroups.batch_write across tenant A and tenant B
        session, database = _make_session()
        mg_a = MutationGroups(session, client_context=ctx_a)
        mg_b = MutationGroups(session, client_context=ctx_b)
        with mock.patch(
            "google.cloud.spanner_v1._helpers._retry",
            side_effect=lambda f, **kw: f(),
        ):
            mg_a.batch_write(request_options=shared_options)
            req_a = database.spanner_api.batch_write.call_args.kwargs["request"]
            mg_b.batch_write(request_options=shared_options)
            req_b = database.spanner_api.batch_write.call_args.kwargs["request"]
        self.assertEqual(
            dict(req_a.request_options.client_context.secure_context),
            {"tenant": "A", "only_a": "secret"},
        )
        self.assertEqual(
            dict(req_b.request_options.client_context.secure_context),
            {"tenant": "B"},
        )
        _assert_shared_untouched()

    def test__merge_request_options_concurrent_shared_isolation(self):
        shared_options = RequestOptions(
            priority=RequestOptions.Priority.PRIORITY_LOW,
            request_tag="shared-tag",
        )
        num_threads = 8
        iterations = 50
        barrier = threading.Barrier(num_threads)
        errors = [None] * num_threads

        def _worker(worker_id):
            tenant_val = f"tenant-{worker_id}"
            ctx = RequestOptions.ClientContext(
                secure_context={
                    "tenant": struct_pb2.Value(string_value=tenant_val),
                    f"only_{worker_id}": struct_pb2.Value(string_value="v"),
                }
            )
            try:
                barrier.wait(timeout=5.0)
                for _ in range(iterations):
                    merged = _merge_request_options(shared_options, ctx)
                    merged.transaction_tag = f"txn-{worker_id}"
                    actual = dict(merged.client_context.secure_context)
                    expected = {"tenant": tenant_val, f"only_{worker_id}": "v"}
                    if actual != expected:
                        raise AssertionError(
                            f"Worker {worker_id} saw {actual}, expected {expected}"
                        )
                    if merged.request_tag != "shared-tag":
                        raise AssertionError(
                            f"Worker {worker_id} saw request_tag={merged.request_tag}"
                        )
            except BaseException as exc:
                errors[worker_id] = exc

        threads = [
            threading.Thread(target=_worker, args=(i,)) for i in range(num_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)
            self.assertFalse(t.is_alive())

        for err in errors:
            self.assertIsNone(err)

        self.assertEqual(shared_options.request_tag, "shared-tag")
        self.assertEqual(shared_options.transaction_tag, "")
        self.assertNotIn("client_context", shared_options)


if __name__ == "__main__":
    unittest.main()
