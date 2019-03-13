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
from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.ndb import context as context_module
from google.cloud.ndb import key as key_module
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
        with context.use():
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
        with context.use():
            stub = _api.stub()
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        grpc.insecure_channel.assert_called_once_with("thehost")


class Test_make_call:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api._retry")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_defaults(stub, _retry):
        api = stub.return_value
        future = tasklets.Future()
        api.foo.future.return_value = future
        _retry.retry_async.return_value = mock.Mock(return_value=future)
        future.set_result("bar")

        request = object()
        assert _api.make_call("foo", request).result() == "bar"
        _retry.retry_async.assert_called_once()
        tasklet = _retry.retry_async.call_args[0][0]
        assert tasklet().result() == "bar"
        retries = _retry.retry_async.call_args[1]["retries"]
        assert retries is _retry._DEFAULT_RETRIES

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api._retry")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_explicit_retries(stub, _retry):
        api = stub.return_value
        future = tasklets.Future()
        api.foo.future.return_value = future
        _retry.retry_async.return_value = mock.Mock(return_value=future)
        future.set_result("bar")

        request = object()
        assert _api.make_call("foo", request, retries=4).result() == "bar"
        _retry.retry_async.assert_called_once()
        tasklet = _retry.retry_async.call_args[0][0]
        assert tasklet().result() == "bar"
        retries = _retry.retry_async.call_args[1]["retries"]
        assert retries == 4

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api._retry")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_no_retries(stub, _retry):
        api = stub.return_value
        future = tasklets.Future()
        api.foo.future.return_value = future
        _retry.retry_async.return_value = mock.Mock(return_value=future)
        future.set_result("bar")

        request = object()
        assert _api.make_call("foo", request, retries=0).result() == "bar"
        _retry.retry_async.assert_not_called()


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
        with context.new(eventloop=eventloop).use() as context:
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
        with context.new(eventloop=eventloop).use() as context:
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
        with context.new(eventloop=eventloop).use() as context:
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

        rpc = tasklets.Future("_datastore_lookup")
        _datastore_lookup.return_value = rpc

        entity_pb2.Key = MockKey
        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with context.new(eventloop=eventloop).use() as context:
            batch = _api._LookupBatch({})
            batch.lookup_callback = mock.Mock()
            batch.todo.update({"foo": ["one", "two"], "bar": ["three"]})
            batch.idle_callback()

            called_with = _datastore_lookup.call_args[0]
            called_with_keys = set(
                (mock_key.key for mock_key in called_with[0])
            )
            assert called_with_keys == set(["foo", "bar"])
            called_with_options = called_with[1]
            assert called_with_options == datastore_pb2.ReadOptions()

            rpc.set_result(None)
            batch.lookup_callback.assert_called_once_with(rpc)

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
        with context.new(eventloop=eventloop).use() as context:
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
        with context.new(eventloop=eventloop).use() as context:
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
    with context.new(client=client, stub=stub).use() as context:
        context.stub.Lookup = Lookup = mock.Mock(spec=("future",))
        future = tasklets.Future()
        future.set_result("response")
        Lookup.future.return_value = future
        assert (
            _api._datastore_lookup(["foo", "bar"], None).result() == "response"
        )

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
        with context.new(transaction=b"txfoo").use():
            options = _api._get_read_options({})
            assert options == datastore_pb2.ReadOptions(transaction=b"txfoo")

    @staticmethod
    def test_args_override_transaction(context):
        with context.new(transaction=b"txfoo").use():
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


class Test_put:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    def test_no_transaction(datastore_pb2, in_context):
        class Mutation:
            def __init__(self, upsert=None):
                self.upsert = upsert

            def __eq__(self, other):
                return self.upsert is other.upsert

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with in_context.new(eventloop=eventloop).use() as context:
            datastore_pb2.Mutation = Mutation

            entity1, entity2, entity3 = object(), object(), object()
            future1 = _api.put(entity1)
            future2 = _api.put(entity2)
            future3 = _api.put(entity3)

            batch = context.batches[_api._NonTransactionalCommitBatch][()]
            assert batch.mutations == [
                Mutation(upsert=entity1),
                Mutation(upsert=entity2),
                Mutation(upsert=entity3),
            ]
            assert batch.futures == [future1, future2, future3]

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    def test_w_transaction(datastore_pb2, in_context):
        class Mutation:
            def __init__(self, upsert=None):
                self.upsert = upsert

            def __eq__(self, other):
                return self.upsert is other.upsert

        class PathElement:
            id = None

            def __init__(self, name):
                self.name = name

        def MockEntity(*path):
            path = [PathElement(name) for name in path]
            return mock.Mock(key=mock.Mock(path=path))

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with in_context.new(eventloop=eventloop).use() as context:
            datastore_pb2.Mutation = Mutation

            entity1 = MockEntity("a", "1")
            future1 = _api.put(entity1, transaction=b"123")

            entity2 = MockEntity("a", None)
            future2 = _api.put(entity2, transaction=b"123")

            entity3 = MockEntity()
            future3 = _api.put(entity3, transaction=b"123")

            batch = context.commit_batches[b"123"]
            assert batch.mutations == [
                Mutation(upsert=entity1),
                Mutation(upsert=entity2),
                Mutation(upsert=entity3),
            ]
            assert batch.futures == [future1, future2, future3]
            assert batch.transaction == b"123"
            assert batch.incomplete_mutations == [
                Mutation(upsert=entity2),
                Mutation(upsert=entity3),
            ]
            assert batch.incomplete_futures == [future2, future3]


class Test_delete:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    def test_no_transaction(datastore_pb2, in_context):
        class Mutation:
            def __init__(self, delete=None):
                self.delete = delete

            def __eq__(self, other):
                return self.delete == other.delete

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with in_context.new(eventloop=eventloop).use() as context:
            datastore_pb2.Mutation = Mutation

            key1 = key_module.Key("SomeKind", 1)._key
            key2 = key_module.Key("SomeKind", 2)._key
            key3 = key_module.Key("SomeKind", 3)._key
            future1 = _api.delete(key1)
            future2 = _api.delete(key2)
            future3 = _api.delete(key3)

            batch = context.batches[_api._NonTransactionalCommitBatch][()]
            assert batch.mutations == [
                Mutation(delete=key1.to_protobuf()),
                Mutation(delete=key2.to_protobuf()),
                Mutation(delete=key3.to_protobuf()),
            ]
            assert batch.futures == [future1, future2, future3]

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    def test_w_transaction(datastore_pb2, in_context):
        class Mutation:
            def __init__(self, delete=None):
                self.delete = delete

            def __eq__(self, other):
                return self.delete == other.delete

        eventloop = mock.Mock(spec=("add_idle", "run"))
        with in_context.new(
            eventloop=eventloop, transaction=b"tx123"
        ).use() as context:
            datastore_pb2.Mutation = Mutation

            key1 = key_module.Key("SomeKind", 1)._key
            key2 = key_module.Key("SomeKind", 2)._key
            key3 = key_module.Key("SomeKind", 3)._key
            future1 = _api.delete(key1)
            future2 = _api.delete(key2)
            future3 = _api.delete(key3)

            batch = context.commit_batches[b"tx123"]
            assert batch.mutations == [
                Mutation(delete=key1.to_protobuf()),
                Mutation(delete=key2.to_protobuf()),
                Mutation(delete=key3.to_protobuf()),
            ]
            assert batch.futures == [future1, future2, future3]


class Test_NonTransactionalCommitBatch:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._process_commit")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_idle_callback(_datastore_commit, _process_commit, context):
        eventloop = mock.Mock(spec=("queue_rpc", "run"))

        rpc = tasklets.Future("_datastore_commit")
        _datastore_commit.return_value = rpc

        with context.new(eventloop=eventloop).use() as context:
            mutation1, mutation2 = object(), object()
            batch = _api._NonTransactionalCommitBatch({})
            batch.mutations = [mutation1, mutation2]
            batch.idle_callback()

            _datastore_commit.assert_called_once_with(
                [mutation1, mutation2], None, retries=None
            )
            rpc.set_result(None)
            _process_commit.assert_called_once_with(rpc, batch.futures)


@mock.patch("google.cloud.ndb._datastore_api._get_commit_batch")
def test_commit(get_commit_batch):
    _api.commit(b"123")
    get_commit_batch.assert_called_once_with(b"123", {})
    get_commit_batch.return_value.commit.assert_called_once_with(retries=None)


class Test_get_commit_batch:
    @staticmethod
    def test_create_batch(in_context):
        batch = _api._get_commit_batch(b"123", {})
        assert isinstance(batch, _api._TransactionalCommitBatch)
        assert in_context.commit_batches[b"123"] is batch
        assert batch.transaction == b"123"
        assert _api._get_commit_batch(b"123", {}) is batch
        assert _api._get_commit_batch(b"234", {}) is not batch

    @staticmethod
    def test_bad_options():
        with pytest.raises(NotImplementedError):
            _api._get_commit_batch(b"123", {"foo": "bar"})


class Test__TransactionalCommitBatch:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_idle_callback_nothing_to_do():
        batch = _api._TransactionalCommitBatch({})
        batch.idle_callback()
        assert not batch.allocating_ids

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._datastore_allocate_ids")
    def test_idle_callback_success(datastore_allocate_ids, in_context):
        def Mutation():
            path = [entity_pb2.Key.PathElement(kind="SomeKind")]
            return datastore_pb2.Mutation(
                upsert=entity_pb2.Entity(key=entity_pb2.Key(path=path))
            )

        mutation1, mutation2 = Mutation(), Mutation()
        batch = _api._TransactionalCommitBatch({})
        batch.incomplete_mutations = [mutation1, mutation2]
        future1, future2 = tasklets.Future(), tasklets.Future()
        batch.incomplete_futures = [future1, future2]

        rpc = tasklets.Future("_datastore_allocate_ids")
        datastore_allocate_ids.return_value = rpc

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            batch.idle_callback()

            rpc.set_result(
                mock.Mock(
                    keys=[
                        entity_pb2.Key(
                            path=[
                                entity_pb2.Key.PathElement(
                                    kind="SomeKind", id=1
                                )
                            ]
                        ),
                        entity_pb2.Key(
                            path=[
                                entity_pb2.Key.PathElement(
                                    kind="SomeKind", id=2
                                )
                            ]
                        ),
                    ]
                )
            )

            allocating_ids = batch.allocating_ids[0]
            assert future1.result().path[0].id == 1
            assert mutation1.upsert.key.path[0].id == 1
            assert future2.result().path[0].id == 2
            assert mutation2.upsert.key.path[0].id == 2
            assert allocating_ids.result() is None

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._datastore_allocate_ids")
    def test_idle_callback_failure(datastore_allocate_ids, in_context):
        def Mutation():
            path = [entity_pb2.Key.PathElement(kind="SomeKind")]
            return datastore_pb2.Mutation(
                upsert=entity_pb2.Entity(key=entity_pb2.Key(path=path))
            )

        mutation1, mutation2 = Mutation(), Mutation()
        batch = _api._TransactionalCommitBatch({})
        batch.incomplete_mutations = [mutation1, mutation2]
        future1, future2 = tasklets.Future(), tasklets.Future()
        batch.incomplete_futures = [future1, future2]

        rpc = tasklets.Future("_datastore_allocate_ids")
        datastore_allocate_ids.return_value = rpc

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            batch.idle_callback()

            error = Exception("Spurious error")
            rpc.set_exception(error)

            allocating_ids = batch.allocating_ids[0]
            assert future1.exception() is error
            assert future2.exception() is error
            assert allocating_ids.result() is None

    @staticmethod
    def test_commit_nothing_to_do(in_context):
        batch = _api._TransactionalCommitBatch({})

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            future = batch.commit()
            eventloop.queue_rpc.assert_not_called()

        assert future.result() is None

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._process_commit")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_commit(datastore_commit, process_commit, in_context):
        batch = _api._TransactionalCommitBatch({})
        batch.futures = object()
        batch.mutations = object()
        batch.transaction = b"abc"

        rpc = tasklets.Future("_datastore_commit")
        datastore_commit.return_value = rpc

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            future = batch.commit()

            datastore_commit.assert_called_once_with(
                batch.mutations, transaction=b"abc", retries=None
            )
            rpc.set_result(None)
            process_commit.assert_called_once_with(rpc, batch.futures)

        assert future.result() is None

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._process_commit")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_commit_error(datastore_commit, process_commit, in_context):
        batch = _api._TransactionalCommitBatch({})
        batch.futures = object()
        batch.mutations = object()
        batch.transaction = b"abc"

        rpc = tasklets.Future("_datastore_commit")
        datastore_commit.return_value = rpc

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            future = batch.commit()

            datastore_commit.assert_called_once_with(
                batch.mutations, transaction=b"abc", retries=None
            )

            error = Exception("Spurious error")
            rpc.set_exception(error)

            process_commit.assert_called_once_with(rpc, batch.futures)

        assert future.exception() is error

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api._process_commit")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_commit")
    def test_commit_allocating_ids(
        datastore_commit, process_commit, in_context
    ):
        batch = _api._TransactionalCommitBatch({})
        batch.futures = object()
        batch.mutations = object()
        batch.transaction = b"abc"

        allocated_ids = tasklets.Future("Already allocated ids")
        allocated_ids.set_result(None)
        batch.allocating_ids.append(allocated_ids)

        allocating_ids = tasklets.Future("AllocateIds")
        batch.allocating_ids.append(allocating_ids)

        rpc = tasklets.Future("_datastore_commit")
        datastore_commit.return_value = rpc

        eventloop = mock.Mock(spec=("queue_rpc", "run"))
        with in_context.new(eventloop=eventloop).use():
            future = batch.commit()

            datastore_commit.assert_not_called()
            process_commit.assert_not_called()

            allocating_ids.set_result(None)
            datastore_commit.assert_called_once_with(
                batch.mutations, transaction=b"abc", retries=None
            )

            rpc.set_result(None)
            process_commit.assert_called_once_with(rpc, batch.futures)

        assert future.result() is None


class Test_process_commit:
    @staticmethod
    def test_exception():
        error = Exception("Spurious error.")
        rpc = tasklets.Future()
        rpc.set_exception(error)

        future1, future2 = tasklets.Future(), tasklets.Future()
        _api._process_commit(rpc, [future1, future2])
        assert future1.exception() is error
        assert future2.exception() is error

    @staticmethod
    def test_exception_some_already_done():
        error = Exception("Spurious error.")
        rpc = tasklets.Future()
        rpc.set_exception(error)

        future1, future2 = tasklets.Future(), tasklets.Future()
        future2.set_result("hi mom")
        _api._process_commit(rpc, [future1, future2])
        assert future1.exception() is error
        assert future2.result() == "hi mom"

    @staticmethod
    def test_success():
        key1 = mock.Mock(path=["one", "two"], spec=("path",))
        mutation1 = mock.Mock(key=key1, spec=("key",))
        key2 = mock.Mock(path=[], spec=("path",))
        mutation2 = mock.Mock(key=key2, spec=("key",))
        response = mock.Mock(
            mutation_results=(mutation1, mutation2), spec=("mutation_results",)
        )

        rpc = tasklets.Future()
        rpc.set_result(response)

        future1, future2 = tasklets.Future(), tasklets.Future()
        _api._process_commit(rpc, [future1, future2])
        assert future1.result() is key1
        assert future2.result() is None

    @staticmethod
    def test_success_some_already_done():
        key1 = mock.Mock(path=["one", "two"], spec=("path",))
        mutation1 = mock.Mock(key=key1, spec=("key",))
        key2 = mock.Mock(path=[], spec=("path",))
        mutation2 = mock.Mock(key=key2, spec=("key",))
        response = mock.Mock(
            mutation_results=(mutation1, mutation2), spec=("mutation_results",)
        )

        rpc = tasklets.Future()
        rpc.set_result(response)

        future1, future2 = tasklets.Future(), tasklets.Future()
        future2.set_result(None)
        _api._process_commit(rpc, [future1, future2])
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
        future = tasklets.Future()
        future.set_result("response")
        api.Commit.future.return_value = future
        assert _api._datastore_commit(mutations, None).result() == "response"

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
        future = tasklets.Future()
        future.set_result("response")
        api.Commit.future.return_value = future
        assert (
            _api._datastore_commit(mutations, b"tx123").result() == "response"
        )

        datastore_pb2.CommitRequest.assert_called_once_with(
            project_id="testing",
            mode=datastore_pb2.CommitRequest.TRANSACTIONAL,
            mutations=mutations,
            transaction=b"tx123",
        )

        request = datastore_pb2.CommitRequest.return_value
        assert api.Commit.future.called_once_with(request)


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
@mock.patch("google.cloud.ndb._datastore_api.stub")
def test__datastore_allocate_ids(stub, datastore_pb2):
    keys = object()
    api = stub.return_value
    future = tasklets.Future()
    future.set_result("response")
    api.AllocateIds.future.return_value = future
    assert _api._datastore_allocate_ids(keys).result() == "response"

    datastore_pb2.AllocateIdsRequest.assert_called_once_with(
        project_id="testing", keys=keys
    )

    request = datastore_pb2.AllocateIdsRequest.return_value
    assert api.AllocateIds.future.called_once_with(request)


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api._datastore_begin_transaction")
def test_begin_transaction(_datastore_begin_transaction):
    rpc = tasklets.Future("BeginTransaction()")
    _datastore_begin_transaction.return_value = rpc

    future = _api.begin_transaction("read only")
    _datastore_begin_transaction.assert_called_once_with(
        "read only", retries=None
    )
    rpc.set_result(mock.Mock(transaction=b"tx123", spec=("transaction")))

    assert future.result() == b"tx123"


class Test_datastore_begin_transaction:
    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_read_only(stub, datastore_pb2):
        api = stub.return_value
        future = tasklets.Future()
        future.set_result("response")
        api.BeginTransaction.future.return_value = future
        assert _api._datastore_begin_transaction(True).result() == "response"

        datastore_pb2.TransactionOptions.assert_called_once_with(
            read_only=datastore_pb2.TransactionOptions.ReadOnly()
        )

        transaction_options = datastore_pb2.TransactionOptions.return_value
        datastore_pb2.BeginTransactionRequest.assert_called_once_with(
            project_id="testing", transaction_options=transaction_options
        )

        request = datastore_pb2.BeginTransactionRequest.return_value
        assert api.BeginTransaction.future.called_once_with(request)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_api.stub")
    def test_read_write(stub, datastore_pb2):
        api = stub.return_value
        future = tasklets.Future()
        future.set_result("response")
        api.BeginTransaction.future.return_value = future
        assert _api._datastore_begin_transaction(False).result() == "response"

        datastore_pb2.TransactionOptions.assert_called_once_with(
            read_write=datastore_pb2.TransactionOptions.ReadWrite()
        )

        transaction_options = datastore_pb2.TransactionOptions.return_value
        datastore_pb2.BeginTransactionRequest.assert_called_once_with(
            project_id="testing", transaction_options=transaction_options
        )

        request = datastore_pb2.BeginTransactionRequest.return_value
        assert api.BeginTransaction.future.called_once_with(request)


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api._datastore_rollback")
def test_rollback(_datastore_rollback):
    rpc = tasklets.Future("Rollback()")
    _datastore_rollback.return_value = rpc
    future = _api.rollback(b"tx123")

    _datastore_rollback.assert_called_once_with(b"tx123", retries=None)
    rpc.set_result(None)

    assert future.result() is None


@pytest.mark.usefixtures("in_context")
@mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
@mock.patch("google.cloud.ndb._datastore_api.stub")
def test__datastore_rollback(stub, datastore_pb2):
    api = stub.return_value
    future = tasklets.Future()
    future.set_result("response")
    api.Rollback.future.return_value = future
    assert _api._datastore_rollback(b"tx123").result() == "response"

    datastore_pb2.RollbackRequest.assert_called_once_with(
        project_id="testing", transaction=b"tx123"
    )

    request = datastore_pb2.RollbackRequest.return_value
    assert api.Rollback.future.called_once_with(request)
