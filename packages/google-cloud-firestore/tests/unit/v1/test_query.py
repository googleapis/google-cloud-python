# Copyright 2017 Google LLC All rights reserved.
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

import types
import unittest

import mock
import pytest

from tests.unit.v1.test_base_query import _make_credentials
from tests.unit.v1.test_base_query import _make_cursor_pb
from tests.unit.v1.test_base_query import _make_query_response


class TestQuery(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.query import Query

        return Query

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertIs(query._parent, mock.sentinel.parent)
        self.assertIsNone(query._projection)
        self.assertEqual(query._field_filters, ())
        self.assertEqual(query._orders, ())
        self.assertIsNone(query._limit)
        self.assertIsNone(query._offset)
        self.assertIsNone(query._start_at)
        self.assertIsNone(query._end_at)
        self.assertFalse(query._all_descendants)

    def _get_helper(self, retry=None, timeout=None):
        from google.cloud.firestore_v1 import _helpers

        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("dee")

        # Add a dummy response to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = "{}/sleep".format(expected_prefix)
        data = {"snooze": 10}

        response_pb = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb])
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        # Execute the query and check the response.
        query = self._make_one(parent)
        returned = query.get(**kwargs)

        self.assertIsInstance(returned, list)
        self.assertEqual(len(returned), 1)

        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("dee", "sleep"))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    def test_get(self):
        self._get_helper()

    def test_get_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        self._get_helper(retry=retry, timeout=timeout)

    def test_get_limit_to_last(self):
        from google.cloud import firestore
        from google.cloud.firestore_v1.base_query import _enum_from_direction

        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("dee")

        # Add a dummy response to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = "{}/sleep".format(expected_prefix)
        data = {"snooze": 10}
        data2 = {"snooze": 20}

        response_pb = _make_query_response(name=name, data=data)
        response_pb2 = _make_query_response(name=name, data=data2)

        firestore_api.run_query.return_value = iter([response_pb2, response_pb])

        # Execute the query and check the response.
        query = self._make_one(parent)
        query = query.order_by(
            "snooze", direction=firestore.Query.DESCENDING
        ).limit_to_last(2)
        returned = query.get()

        self.assertIsInstance(returned, list)
        self.assertEqual(
            query._orders[0].direction, _enum_from_direction(firestore.Query.ASCENDING)
        )
        self.assertEqual(len(returned), 2)

        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("dee", "sleep"))
        self.assertEqual(snapshot.to_dict(), data)

        snapshot2 = returned[1]
        self.assertEqual(snapshot2.reference._path, ("dee", "sleep"))
        self.assertEqual(snapshot2.to_dict(), data2)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    def _stream_helper(self, retry=None, timeout=None):
        from google.cloud.firestore_v1 import _helpers

        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("dee")

        # Add a dummy response to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = "{}/sleep".format(expected_prefix)
        data = {"snooze": 10}
        response_pb = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb])
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        # Execute the query and check the response.
        query = self._make_one(parent)

        get_response = query.stream(**kwargs)

        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("dee", "sleep"))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    def test_stream_simple(self):
        self._stream_helper()

    def test_stream_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        self._stream_helper(retry=retry, timeout=timeout)

    def test_stream_with_limit_to_last(self):
        # Attach the fake GAPIC to a real client.
        client = _make_client()
        # Make a **real** collection reference as parent.
        parent = client.collection("dee")
        # Execute the query and check the response.
        query = self._make_one(parent)
        query = query.limit_to_last(2)

        stream_response = query.stream()

        with self.assertRaises(ValueError):
            list(stream_response)

    def test_stream_with_transaction(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Create a real-ish transaction for this client.
        transaction = client.transaction()
        txn_id = b"\x00\x00\x01-work-\xf2"
        transaction._id = txn_id

        # Make a **real** collection reference as parent.
        parent = client.collection("declaration")

        # Add a dummy response to the minimal fake GAPIC.
        parent_path, expected_prefix = parent._parent_info()
        name = "{}/burger".format(expected_prefix)
        data = {"lettuce": b"\xee\x87"}
        response_pb = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.stream(transaction=transaction)
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("declaration", "burger"))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": txn_id,
            },
            metadata=client._rpc_metadata,
        )

    def test_stream_no_results(self):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=["run_query"])
        empty_response = _make_query_response()
        run_query_response = iter([empty_response])
        firestore_api.run_query.return_value = run_query_response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("dah", "dah", "dum")
        query = self._make_one(parent)

        get_response = query.stream()
        self.assertIsInstance(get_response, types.GeneratorType)
        self.assertEqual(list(get_response), [])

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    def test_stream_second_response_in_empty_stream(self):
        # Create a minimal fake GAPIC with a dummy response.
        firestore_api = mock.Mock(spec=["run_query"])
        empty_response1 = _make_query_response()
        empty_response2 = _make_query_response()
        run_query_response = iter([empty_response1, empty_response2])
        firestore_api.run_query.return_value = run_query_response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("dah", "dah", "dum")
        query = self._make_one(parent)

        get_response = query.stream()
        self.assertIsInstance(get_response, types.GeneratorType)
        self.assertEqual(list(get_response), [])

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    def test_stream_with_skipped_results(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("talk", "and", "chew-gum")

        # Add two dummy responses to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        response_pb1 = _make_query_response(skipped_results=1)
        name = "{}/clock".format(expected_prefix)
        data = {"noon": 12, "nested": {"bird": 10.5}}
        response_pb2 = _make_query_response(name=name, data=data)
        firestore_api.run_query.return_value = iter([response_pb1, response_pb2])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.stream()
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("talk", "and", "chew-gum", "clock"))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    def test_stream_empty_after_first_response(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("charles")

        # Add two dummy responses to the minimal fake GAPIC.
        _, expected_prefix = parent._parent_info()
        name = "{}/bark".format(expected_prefix)
        data = {"lee": "hoop"}
        response_pb1 = _make_query_response(name=name, data=data)
        response_pb2 = _make_query_response()
        firestore_api.run_query.return_value = iter([response_pb1, response_pb2])

        # Execute the query and check the response.
        query = self._make_one(parent)
        get_response = query.stream()
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        self.assertEqual(snapshot.reference._path, ("charles", "bark"))
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    def test_stream_w_collection_group(self):
        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["run_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("charles")
        other = client.collection("dora")

        # Add two dummy responses to the minimal fake GAPIC.
        _, other_prefix = other._parent_info()
        name = "{}/bark".format(other_prefix)
        data = {"lee": "hoop"}
        response_pb1 = _make_query_response(name=name, data=data)
        response_pb2 = _make_query_response()
        firestore_api.run_query.return_value = iter([response_pb1, response_pb2])

        # Execute the query and check the response.
        query = self._make_one(parent)
        query._all_descendants = True
        get_response = query.stream()
        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 1)
        snapshot = returned[0]
        to_match = other.document("bark")
        self.assertEqual(snapshot.reference._document_path, to_match._document_path)
        self.assertEqual(snapshot.to_dict(), data)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        firestore_api.run_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
        )

    @mock.patch("google.cloud.firestore_v1.query.Watch", autospec=True)
    def test_on_snapshot(self, watch):
        query = self._make_one(mock.sentinel.parent)
        query.on_snapshot(None)
        watch.for_query.assert_called_once()


class TestCollectionGroup(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.query import CollectionGroup

        return CollectionGroup

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        query = self._make_one(mock.sentinel.parent)
        self.assertIs(query._parent, mock.sentinel.parent)
        self.assertIsNone(query._projection)
        self.assertEqual(query._field_filters, ())
        self.assertEqual(query._orders, ())
        self.assertIsNone(query._limit)
        self.assertIsNone(query._offset)
        self.assertIsNone(query._start_at)
        self.assertIsNone(query._end_at)
        self.assertTrue(query._all_descendants)

    def test_constructor_all_descendents_is_false(self):
        with pytest.raises(ValueError):
            self._make_one(mock.sentinel.parent, all_descendants=False)

    def _get_partitions_helper(self, retry=None, timeout=None):
        from google.cloud.firestore_v1 import _helpers

        # Create a minimal fake GAPIC.
        firestore_api = mock.Mock(spec=["partition_query"])

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Make a **real** collection reference as parent.
        parent = client.collection("charles")

        # Make two **real** document references to use as cursors
        document1 = parent.document("one")
        document2 = parent.document("two")

        # Add cursor pb's to the minimal fake GAPIC.
        cursor_pb1 = _make_cursor_pb(([document1], False))
        cursor_pb2 = _make_cursor_pb(([document2], False))
        firestore_api.partition_query.return_value = iter([cursor_pb1, cursor_pb2])
        kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

        # Execute the query and check the response.
        query = self._make_one(parent)

        get_response = query.get_partitions(2, **kwargs)

        self.assertIsInstance(get_response, types.GeneratorType)
        returned = list(get_response)
        self.assertEqual(len(returned), 3)

        # Verify the mock call.
        parent_path, _ = parent._parent_info()
        partition_query = self._make_one(
            parent, orders=(query._make_order("__name__", query.ASCENDING),),
        )
        firestore_api.partition_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_query": partition_query._to_protobuf(),
                "partition_count": 2,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )

    def test_get_partitions(self):
        self._get_partitions_helper()

    def test_get_partitions_w_retry_timeout(self):
        from google.api_core.retry import Retry

        retry = Retry(predicate=object())
        timeout = 123.0
        self._get_partitions_helper(retry=retry, timeout=timeout)

    def test_get_partitions_w_filter(self):
        # Make a **real** collection reference as parent.
        client = _make_client()
        parent = client.collection("charles")

        # Make a query that fails to partition
        query = self._make_one(parent).where("foo", "==", "bar")
        with pytest.raises(ValueError):
            list(query.get_partitions(2))

    def test_get_partitions_w_projection(self):
        # Make a **real** collection reference as parent.
        client = _make_client()
        parent = client.collection("charles")

        # Make a query that fails to partition
        query = self._make_one(parent).select("foo")
        with pytest.raises(ValueError):
            list(query.get_partitions(2))

    def test_get_partitions_w_limit(self):
        # Make a **real** collection reference as parent.
        client = _make_client()
        parent = client.collection("charles")

        # Make a query that fails to partition
        query = self._make_one(parent).limit(10)
        with pytest.raises(ValueError):
            list(query.get_partitions(2))

    def test_get_partitions_w_offset(self):
        # Make a **real** collection reference as parent.
        client = _make_client()
        parent = client.collection("charles")

        # Make a query that fails to partition
        query = self._make_one(parent).offset(10)
        with pytest.raises(ValueError):
            list(query.get_partitions(2))


def _make_client(project="project-project"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
