# Copyright 2018 Google LLC
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

from unittest import mock

import pytest

from google.cloud import _http
from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.ndb import context as context_module
from google.cloud.ndb import _datastore_api as _api
from google.cloud.ndb import tasklets


class TestStub:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._helpers")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2_grpc")
    def test_secure_channel(datastore_pb2_grpc, _helpers):
        channel = _helpers.make_secure_channel.return_value
        client = mock.Mock(
            _credentials="creds",
            secure=True,
            host="thehost",
            spec=("_credentials", "secure", "host"),
        )
        context = context_module.Context(client)
        with context:
            stub = _api.stub()
            assert _api.stub() is stub  # one stub per context
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        _helpers.make_secure_channel.assert_called_once_with(
            "creds", _http.DEFAULT_USER_AGENT, "thehost"
        )

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.grpc")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2_grpc")
    def test_insecure_channel(datastore_pb2_grpc, grpc):
        channel = grpc.insecure_channel.return_value
        client = mock.Mock(
            secure=False, host="thehost", spec=("secure", "host")
        )
        context = context_module.Context(client)
        with context:
            stub = _api.stub()
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        grpc.insecure_channel.assert_called_once_with("thehost")


class TestRemoteCall:
    @staticmethod
    def test_constructor():
        call = _api.RemoteCall("future", "info")
        assert call.future == "future"
        assert call.info == "info"

    @staticmethod
    def test_repr():
        call = _api.RemoteCall(None, "a remote call")
        assert repr(call) == "a remote call"

    @staticmethod
    def test_exception():
        error = Exception("Spurious error")
        future = tasklets.Future()
        future.set_exception(error)
        call = _api.RemoteCall(future, "testing")
        assert call.exception() is error

    @staticmethod
    def test_result():
        future = tasklets.Future()
        future.set_result("positive")
        call = _api.RemoteCall(future, "testing")
        assert call.result() == "positive"

    @staticmethod
    def test_add_done_callback():
        future = tasklets.Future()
        call = _api.RemoteCall(future, "testing")
        callback = mock.Mock(spec=())
        call.add_done_callback(callback)
        future.set_result(None)
        callback.assert_called_once_with(future)


def _mock_key(key_str):
    key = mock.Mock(spec=("to_protobuf",))
    key.to_protobuf.return_value = protobuf = mock.Mock(
        spec=("SerializeToString",)
    )
    protobuf.SerializeToString.return_value = key_str
    return key


class TestLookup:
    @staticmethod
    def test_it(context):
        eventloop = mock.Mock(spec=("add_idle", "run"))
        with context.new(eventloop=eventloop) as context:
            future1 = _api.lookup(_mock_key("foo"))
            future2 = _api.lookup(_mock_key("foo"))
            future3 = _api.lookup(_mock_key("bar"))

            batch = context.batches[_api._LookupBatch][()]
            assert batch.todo["foo"] == [future1, future2]
            assert batch.todo["bar"] == [future3]
            assert context.eventloop.add_idle.call_count == 1

    @staticmethod
    def test_it_with_options(context):
        eventloop = mock.Mock(spec=("add_idle", "run"))
        with context.new(eventloop=eventloop) as context:
            future1 = _api.lookup(_mock_key("foo"))
            future2 = _api.lookup(
                _mock_key("foo"), read_consistency=_api.EVENTUAL
            )
            future3 = _api.lookup(_mock_key("bar"))

            batches = context.batches[_api._LookupBatch]
            batch1 = batches[()]
            assert batch1.todo["foo"] == [future1]
            assert batch1.todo["bar"] == [future3]

            batch2 = batches[(("read_consistency", _api.EVENTUAL),)]
            assert batch2.todo == {"foo": [future2]}

            add_idle = context.eventloop.add_idle
            assert add_idle.call_count == 2

    @staticmethod
    def test_it_with_bad_option(context):
        with pytest.raises(NotImplementedError):
            _api.lookup(_mock_key("foo"), foo="bar")

    @staticmethod
    def test_idle_callback(context):
        eventloop = mock.Mock(spec=("add_idle", "run"))
        with context.new(eventloop=eventloop) as context:
            future = _api.lookup(_mock_key("foo"))

            batches = context.batches[_api._LookupBatch]
            batch = batches[()]
            assert batch.todo["foo"] == [future]

            idle = context.eventloop.add_idle.call_args[0][0]
            batch.idle_callback = mock.Mock()
            idle()
            batch.idle_callback.assert_called_once_with()
            assert () not in batches


class Test_LookupBatch:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.entity_pb2")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_lookup")
    def test_idle_callback(_datastore_lookup, entity_pb2, context):
        class MockKey:
            def __init__(self, key=None):
                self.key = key

            def ParseFromString(self, key):
                self.key = key

        entity_pb2.Key = MockKey
        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with context.new(eventloop=eventloop) as context:
            batch = _api._LookupBatch({})
            batch.todo.update({"foo": ["one", "two"], "bar": ["three"]})
            batch.idle_callback()

            called_with = _datastore_lookup.call_args[0]
            called_with_keys = set(
                (mock_key.key for mock_key in called_with[0])
            )
            assert called_with_keys == set(["foo", "bar"])
            called_with_options = called_with[1]
            assert called_with_options == datastore_pb2.ReadOptions()

            rpc = _datastore_lookup.return_value
            context.eventloop.queue_rpc.assert_called_once_with(
                rpc, batch.lookup_callback
            )

    @staticmethod
    def test_lookup_callback_exception():
        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.todo.update({"foo": [future1, future2], "bar": [future3]})
        error = Exception("Spurious error.")

        rpc = tasklets.Future()
        rpc.set_exception(error)
        batch.lookup_callback(rpc)

        assert future1.exception() is error
        assert future2.exception() is error

    @staticmethod
    def test_found():
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.todo.update({"foo": [future1, future2], "bar": [future3]})

        entity1 = mock.Mock(key=key_pb("foo"), spec=("key",))
        entity2 = mock.Mock(key=key_pb("bar"), spec=("key",))
        response = mock.Mock(
            found=[
                mock.Mock(entity=entity1, spec=("entity",)),
                mock.Mock(entity=entity2, spec=("entity",)),
            ],
            missing=[],
            deferred=[],
            spec=("found", "missing", "deferred"),
        )

        rpc = tasklets.Future()
        rpc.set_result(response)
        batch.lookup_callback(rpc)

        assert future1.result() is entity1
        assert future2.result() is entity1
        assert future3.result() is entity2

    @staticmethod
    def test_missing():
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.todo.update({"foo": [future1, future2], "bar": [future3]})

        entity1 = mock.Mock(key=key_pb("foo"), spec=("key",))
        entity2 = mock.Mock(key=key_pb("bar"), spec=("key",))
        response = mock.Mock(
            missing=[
                mock.Mock(entity=entity1, spec=("entity",)),
                mock.Mock(entity=entity2, spec=("entity",)),
            ],
            found=[],
            deferred=[],
            spec=("found", "missing", "deferred"),
        )

        rpc = tasklets.Future()
        rpc.set_result(response)
        batch.lookup_callback(rpc)

        assert future1.result() is _api._NOT_FOUND
        assert future2.result() is _api._NOT_FOUND
        assert future3.result() is _api._NOT_FOUND

    @staticmethod
    def test_deferred(context):
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with context.new(eventloop=eventloop) as context:
            future1, future2, future3 = (tasklets.Future() for _ in range(3))
            batch = _api._LookupBatch({})
            batch.todo.update({"foo": [future1, future2], "bar": [future3]})

            response = mock.Mock(
                missing=[],
                found=[],
                deferred=[key_pb("foo"), key_pb("bar")],
                spec=("found", "missing", "deferred"),
            )

            rpc = tasklets.Future()
            rpc.set_result(response)
            batch.lookup_callback(rpc)

            assert future1.running()
            assert future2.running()
            assert future3.running()

            next_batch = context.batches[_api._LookupBatch][()]
            assert next_batch.todo == batch.todo and next_batch is not batch
            assert context.eventloop.add_idle.call_count == 1

    @staticmethod
    def test_found_missing_deferred(context):
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with context.new(eventloop=eventloop) as context:
            future1, future2, future3 = (tasklets.Future() for _ in range(3))
            batch = _api._LookupBatch({})
            batch.todo.update(
                {"foo": [future1], "bar": [future2], "baz": [future3]}
            )

            entity1 = mock.Mock(key=key_pb("foo"), spec=("key",))
            entity2 = mock.Mock(key=key_pb("bar"), spec=("key",))
            response = mock.Mock(
                found=[mock.Mock(entity=entity1, spec=("entity",))],
                missing=[mock.Mock(entity=entity2, spec=("entity",))],
                deferred=[key_pb("baz")],
                spec=("found", "missing", "deferred"),
            )

            rpc = tasklets.Future()
            rpc.set_result(response)
            batch.lookup_callback(rpc)

            assert future1.result() is entity1
            assert future2.result() is _api._NOT_FOUND
            assert future3.running()

            next_batch = context.batches[_api._LookupBatch][()]
            assert next_batch.todo == {"baz": [future3]}
            assert context.eventloop.add_idle.call_count == 1


@mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
def test__datastore_lookup(datastore_pb2, context):
    client = mock.Mock(project="theproject", spec=("project",))
    stub = mock.Mock(spec=("Lookup",))
    with context.new(client=client, stub=stub) as context:
        context.stub.Lookup = Lookup = mock.Mock(spec=("future",))
        future = Lookup.future.return_value
        assert _api._datastore_lookup(["foo", "bar"], None).future is future

        datastore_pb2.LookupRequest.assert_called_once_with(
            project_id="theproject", keys=["foo", "bar"], read_options=None
        )
        context.stub.Lookup.future.assert_called_once_with(
            datastore_pb2.LookupRequest.return_value
        )


class Test_check_unsupported_options:
    @staticmethod
    def test_supported():
        _api._check_unsupported_options(
            {
                "transaction": None,
                "read_consistency": None,
                "read_policy": None,
            }
        )

    @staticmethod
    def test_not_implemented():
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"deadline": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"force_writes": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"use_cache": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"use_memcache": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"use_datastore": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"memcache_timeout": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"max_memcache_items": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"xg": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"propagation": None})
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"retries": None})

    @staticmethod
    def test_not_supported():
        with pytest.raises(NotImplementedError):
            _api._check_unsupported_options({"say_what": None})


class Test_get_read_options:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_no_args_no_transaction():
        assert _api._get_read_options({}) == datastore_pb2.ReadOptions()

    @staticmethod
    def test_no_args_transaction(context):
        with context.new(transaction=b"txfoo"):
            options = _api._get_read_options({})
            assert options == datastore_pb2.ReadOptions(transaction=b"txfoo")

    @staticmethod
    def test_args_override_transaction(context):
        with context.new(transaction=b"txfoo"):
            options = _api._get_read_options({"transaction": b"txbar"})
            assert options == datastore_pb2.ReadOptions(transaction=b"txbar")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_eventually_consistent():
        options = _api._get_read_options({"read_consistency": _api.EVENTUAL})
        assert options == datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.EVENTUAL
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_eventually_consistent_legacy():
        options = _api._get_read_options(
            {"read_policy": _api.EVENTUAL_CONSISTENCY}
        )
        assert options == datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.EVENTUAL
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_eventually_consistent_with_transaction():
        with pytest.raises(ValueError):
            _api._get_read_options(
                {"read_consistency": _api.EVENTUAL, "transaction": b"txfoo"}
            )


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
def test_put(datastore_pb2, context):
    class Mutation:
        def __init__(self, upsert=None):
            self.upsert = upsert

        def __eq__(self, other):
            return self.upsert is other.upsert

    eventloop = mock.Mock(spec=("add_idle", "run"))
    with context.new(eventloop=eventloop) as context:
        datastore_pb2.Mutation = Mutation

        entity1, entity2, entity3 = object(), object(), object()
        future1 = _api.put(entity1)
        future2 = _api.put(entity2)
        future3 = _api.put(entity3)

        batch = context.batches[_api._CommitBatch][()]
        assert batch.mutations == [
            Mutation(upsert=entity1),
            Mutation(upsert=entity2),
            Mutation(upsert=entity3),
        ]
        assert batch.futures == [future1, future2, future3]


class Test_CommitBatch:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_idle_callback_no_transaction(_datastore_commit, context):
        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with context.new(eventloop=eventloop) as context:
            mutation1, mutation2 = object(), object()
            batch = _api._CommitBatch({})
            batch.mutations = [mutation1, mutation2]
            batch.idle_callback()

            rpc = _datastore_commit.return_value
            _datastore_commit.assert_called_once_with(
                [mutation1, mutation2], None
            )
            context.eventloop.queue_rpc.assert_called_once_with(
                rpc, batch.commit_callback
            )

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_idle_callback_w_transaction(_datastore_commit, context):
        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with context.new(eventloop=eventloop) as context:
            mutation1, mutation2 = object(), object()
            batch = _api._CommitBatch({"transaction": b"tx123"})
            batch.mutations = [mutation1, mutation2]
            batch.idle_callback()

            rpc = _datastore_commit.return_value
            _datastore_commit.assert_called_once_with(
                [mutation1, mutation2], b"tx123"
            )
            context.eventloop.queue_rpc.assert_called_once_with(
                rpc, batch.commit_callback
            )

    @staticmethod
    def test_commit_callback_exception():
        future1, future2 = tasklets.Future(), tasklets.Future()
        batch = _api._CommitBatch({})
        batch.futures = [future1, future2]

        error = Exception("Spurious error.")
        rpc = tasklets.Future()
        rpc.set_exception(error)

        batch.commit_callback(rpc)
        assert future1.exception() is error
        assert future2.exception() is error

    @staticmethod
    def test_commit_callback():
        future1, future2 = tasklets.Future(), tasklets.Future()
        batch = _api._CommitBatch({})
        batch.futures = [future1, future2]

        key1 = mock.Mock(path=["one", "two"], spec=("path",))
        mutation1 = mock.Mock(key=key1, spec=("key",))
        key2 = mock.Mock(path=[], spec=("path",))
        mutation2 = mock.Mock(key=key2, spec=("key",))
        response = mock.Mock(
            mutation_results=(mutation1, mutation2), spec=("mutation_results",)
        )

        rpc = tasklets.Future()
        rpc.set_result(response)

        batch.commit_callback(rpc)
        assert future1.result() is key1
        assert future2.result() is None


class Test_datastore_commit:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_wo_transaction(stub, datastore_pb2):
        mutations = object()
        api = stub.return_value
        future = api.Commit.future.return_value
        assert _api._datastore_commit(mutations, None).future == future

        datastore_pb2.CommitRequest.assert_called_once_with(
            project_id="testing",
            mode=datastore_pb2.CommitRequest.NON_TRANSACTIONAL,
            mutations=mutations,
            transaction=None,
        )

        request = datastore_pb2.CommitRequest.return_value
        assert api.Commit.future.called_once_with(request)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_w_transaction(stub, datastore_pb2):
        mutations = object()
        api = stub.return_value
        future = api.Commit.future.return_value
        assert _api._datastore_commit(mutations, b"tx123").future == future

        datastore_pb2.CommitRequest.assert_called_once_with(
            project_id="testing",
            mode=datastore_pb2.CommitRequest.TRANSACTIONAL,
            mutations=mutations,
            transaction=b"tx123",
        )

        request = datastore_pb2.CommitRequest.return_value
        assert api.Commit.future.called_once_with(request)
