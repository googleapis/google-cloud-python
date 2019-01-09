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
from google.cloud.ndb import _datastore_api as _api
from google.cloud.ndb import _runstate
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
        with _runstate.state_context(client):
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
        with _runstate.state_context(client):
            stub = _api.stub()
        assert stub is datastore_pb2_grpc.DatastoreStub.return_value
        datastore_pb2_grpc.DatastoreStub.assert_called_once_with(channel)
        grpc.insecure_channel.assert_called_once_with("thehost")


def _mock_key(key_str):
    key = mock.Mock(spec=("to_protobuf",))
    key.to_protobuf.return_value = protobuf = mock.Mock(
        spec=("SerializeToString",)
    )
    protobuf.SerializeToString.return_value = key_str
    return key


class TestLookup:
    @staticmethod
    def test_it(runstate):
        runstate.eventloop = mock.Mock(spec=("add_idle", "run"))
        future1 = _api.lookup(_mock_key("foo"))
        future2 = _api.lookup(_mock_key("foo"))
        future3 = _api.lookup(_mock_key("bar"))

        batch = runstate.batches[_api._LookupBatch][()]
        assert batch["foo"] == [future1, future2]
        assert batch["bar"] == [future3]
        runstate.eventloop.add_idle.assert_called_once_with(batch.idle_callback)

    @staticmethod
    def test_it_with_options(runstate):
        runstate.eventloop = mock.Mock(spec=("add_idle", "run"))
        future1 = _api.lookup(_mock_key("foo"))
        future2 = _api.lookup(_mock_key("foo"), read_consistency=_api.EVENTUAL)
        future3 = _api.lookup(_mock_key("bar"))

        batches = runstate.batches[_api._LookupBatch]
        batch1 = batches[()]
        assert batch1["foo"] == [future1]
        assert batch1["bar"] == [future3]

        batch2 = batches[(("read_consistency", _api.EVENTUAL),)]
        assert batch2 == {"foo": [future2]}

        add_idle = runstate.eventloop.add_idle
        assert add_idle.call_count == 2

    @staticmethod
    def test_it_with_bad_option(runstate):
        with pytest.raises(NotImplementedError):
            _api.lookup(_mock_key("foo"), foo="bar")


class Test_LookupBatch:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_api.entity_pb2")
    @mock.patch("google.cloud.ndb._datastore_api._datastore_lookup")
    def test_idle_callback(_datastore_lookup, entity_pb2, runstate):
        class MockKey:
            def __init__(self, key=None):
                self.key = key

            def ParseFromString(self, key):
                self.key = key

        entity_pb2.Key = MockKey
        runstate.eventloop = mock.Mock(spec=("queue_rpc", "run"))
        batch = _api._LookupBatch({})
        batch.update({"foo": ["one", "two"], "bar": ["three"]})
        batch.idle_callback()

        called_with = _datastore_lookup.call_args[0]
        called_with_keys = set((mock_key.key for mock_key in called_with[0]))
        assert called_with_keys == set(["foo", "bar"])
        called_with_options = called_with[1]
        assert called_with_options == datastore_pb2.ReadOptions()

        rpc = _datastore_lookup.return_value
        runstate.eventloop.queue_rpc.assert_called_once_with(
            rpc, batch.lookup_callback)

    @staticmethod
    def test_lookup_callback_exception():
        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.update({"foo": [future1, future2], "bar": [future3]})
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
        batch.update({"foo": [future1, future2], "bar": [future3]})

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
        batch.update({"foo": [future1, future2], "bar": [future3]})

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
    def test_deferred(runstate):
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        runstate.eventloop = mock.Mock(spec=("add_idle", "run"))
        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.update({"foo": [future1, future2], "bar": [future3]})

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

        next_batch = runstate.batches[_api._LookupBatch][()]
        assert next_batch == batch and next_batch is not batch
        runstate.eventloop.add_idle.assert_called_once_with(
            next_batch.idle_callback
        )

    @staticmethod
    def test_found_missing_deferred(runstate):
        def key_pb(key):
            mock_key = mock.Mock(spec=("SerializeToString",))
            mock_key.SerializeToString.return_value = key
            return mock_key

        runstate.eventloop = mock.Mock(spec=("add_idle", "run"))
        future1, future2, future3 = (tasklets.Future() for _ in range(3))
        batch = _api._LookupBatch({})
        batch.update({"foo": [future1], "bar": [future2], "baz": [future3]})

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

        next_batch = runstate.batches[_api._LookupBatch][()]
        assert next_batch == {"baz": [future3]}
        runstate.eventloop.add_idle.assert_called_once_with(
            next_batch.idle_callback
        )


@mock.patch("google.cloud.ndb._datastore_api.datastore_pb2")
def test__datastore_lookup(datastore_pb2, runstate):
    runstate.client = mock.Mock(project="theproject", spec=("project",))
    runstate.stub = mock.Mock(spec=("Lookup",))
    runstate.stub.Lookup = Lookup = mock.Mock(spec=("future",))
    future = Lookup.future.return_value
    assert _api._datastore_lookup(["foo", "bar"], None) is future

    datastore_pb2.LookupRequest.assert_called_once_with(
        project_id="theproject", keys=["foo", "bar"], read_options=None,
    )
    runstate.stub.Lookup.future.assert_called_once_with(
        datastore_pb2.LookupRequest.return_value
    )


class Test_check_unsupported_options:

    @staticmethod
    def test_supported():
        _api._check_unsupported_options({
            "transaction": None,
            "read_consistency": None,
            "read_policy": None,
        })

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
    def test_no_args_no_transaction(runstate):
        assert _api._get_read_options({}) == datastore_pb2.ReadOptions()

    @staticmethod
    def test_no_args_transaction(runstate):
        runstate.transaction = b"txfoo"
        options = _api._get_read_options({})
        assert options == datastore_pb2.ReadOptions(transaction=b"txfoo")

    @staticmethod
    def test_args_override_transaction(runstate):
        runstate.transaction = b"txfoo"
        options = _api._get_read_options({"transaction": b"txbar"})
        assert options == datastore_pb2.ReadOptions(transaction=b"txbar")

    @staticmethod
    def test_eventually_consistent(runstate):
        options = _api._get_read_options({
            "read_consistency": _api.EVENTUAL
        })
        assert options == datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.EVENTUAL
        )

    @staticmethod
    def test_eventually_consistent_legacy(runstate):
        options = _api._get_read_options({
            "read_policy": _api.EVENTUAL_CONSISTENCY,
        })
        assert options == datastore_pb2.ReadOptions(
            read_consistency=datastore_pb2.ReadOptions.EVENTUAL
        )

    @staticmethod
    def test_eventually_consistent_with_transaction(runstate):
        with pytest.raises(ValueError):
            _api._get_read_options({
                "read_consistency": _api.EVENTUAL,
                "transaction": b"txfoo",
            })
