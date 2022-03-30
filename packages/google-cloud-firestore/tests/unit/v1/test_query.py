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

import mock
import pytest

from tests.unit.v1.test_base_query import _make_credentials
from tests.unit.v1.test_base_query import _make_cursor_pb
from tests.unit.v1.test_base_query import _make_query_response


def _make_query(*args, **kwargs):
    from google.cloud.firestore_v1.query import Query

    return Query(*args, **kwargs)


def test_query_constructor():
    query = _make_query(mock.sentinel.parent)
    assert query._parent is mock.sentinel.parent
    assert query._projection is None
    assert query._field_filters == ()
    assert query._orders == ()
    assert query._limit is None
    assert query._offset is None
    assert query._start_at is None
    assert query._end_at is None
    assert not query._all_descendants


def _query_get_helper(retry=None, timeout=None):
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
    query = _make_query(parent)
    returned = query.get(**kwargs)

    assert isinstance(returned, list)
    assert len(returned) == 1

    snapshot = returned[0]
    assert snapshot.reference._path, "dee" == "sleep"
    assert snapshot.to_dict() == data

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


def test_query_get():
    _query_get_helper()


def test_query_get_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _query_get_helper(retry=retry, timeout=timeout)


def test_query_get_limit_to_last():
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
    query = _make_query(parent)
    query = query.order_by(
        "snooze", direction=firestore.Query.DESCENDING
    ).limit_to_last(2)
    returned = query.get()

    assert isinstance(returned, list)
    assert query._orders[0].direction == _enum_from_direction(firestore.Query.ASCENDING)
    assert len(returned) == 2

    snapshot = returned[0]
    assert snapshot.reference._path == ("dee", "sleep")
    assert snapshot.to_dict() == data

    snapshot2 = returned[1]
    assert snapshot2.reference._path == ("dee", "sleep")
    assert snapshot2.to_dict() == data2
    parent_path, _ = parent._parent_info()

    firestore_api.run_query.assert_called_once_with(
        request={
            "parent": parent_path,
            "structured_query": query._to_protobuf(),
            "transaction": None,
        },
        metadata=client._rpc_metadata,
    )


def test_query_chunkify_w_empty():
    client = _make_client()
    firestore_api = mock.Mock(spec=["run_query"])
    firestore_api.run_query.return_value = iter([])
    client._firestore_api_internal = firestore_api
    query = client.collection("asdf")._query()

    chunks = list(query._chunkify(10))

    assert chunks == [[]]


def test_query_chunkify_w_chunksize_lt_limit():
    from google.cloud.firestore_v1.types.document import Document
    from google.cloud.firestore_v1.types.firestore import RunQueryResponse

    client = _make_client()
    firestore_api = mock.Mock(spec=["run_query"])
    doc_ids = [
        f"projects/project-project/databases/(default)/documents/asdf/{index}"
        for index in range(5)
    ]
    responses1 = [
        RunQueryResponse(
            document=Document(name=doc_id),
        )
        for doc_id in doc_ids[:2]
    ]
    responses2 = [
        RunQueryResponse(
            document=Document(name=doc_id),
        )
        for doc_id in doc_ids[2:4]
    ]
    responses3 = [
        RunQueryResponse(
            document=Document(name=doc_id),
        )
        for doc_id in doc_ids[4:]
    ]
    firestore_api.run_query.side_effect = [
        iter(responses1),
        iter(responses2),
        iter(responses3),
    ]
    client._firestore_api_internal = firestore_api
    query = client.collection("asdf")._query()

    chunks = list(query._chunkify(2))

    assert len(chunks) == 3
    expected_ids = [str(index) for index in range(5)]
    assert [snapshot.id for snapshot in chunks[0]] == expected_ids[:2]
    assert [snapshot.id for snapshot in chunks[1]] == expected_ids[2:4]
    assert [snapshot.id for snapshot in chunks[2]] == expected_ids[4:]


def test_query_chunkify_w_chunksize_gt_limit():
    from google.cloud.firestore_v1.types.document import Document
    from google.cloud.firestore_v1.types.firestore import RunQueryResponse

    client = _make_client()
    firestore_api = mock.Mock(spec=["run_query"])
    doc_ids = [
        f"projects/project-project/databases/(default)/documents/asdf/{index}"
        for index in range(5)
    ]
    responses = [
        RunQueryResponse(
            document=Document(name=doc_id),
        )
        for doc_id in doc_ids
    ]
    firestore_api.run_query.return_value = iter(responses)
    client._firestore_api_internal = firestore_api
    query = client.collection("asdf")._query()

    chunks = list(query.limit(5)._chunkify(10))

    assert len(chunks) == 1
    chunk_ids = [snapshot.id for snapshot in chunks[0]]
    expected_ids = [str(index) for index in range(5)]
    assert chunk_ids == expected_ids


def _query_stream_helper(retry=None, timeout=None):
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
    query = _make_query(parent)

    get_response = query.stream(**kwargs)

    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("dee", "sleep")
    assert snapshot.to_dict() == data

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


def test_query_stream_simple():
    _query_stream_helper()


def test_query_stream_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _query_stream_helper(retry=retry, timeout=timeout)


def test_query_stream_with_limit_to_last():
    # Attach the fake GAPIC to a real client.
    client = _make_client()
    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    # Execute the query and check the response.
    query = _make_query(parent)
    query = query.limit_to_last(2)

    stream_response = query.stream()

    with pytest.raises(ValueError):
        list(stream_response)


def test_query_stream_with_transaction():
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
    query = _make_query(parent)
    get_response = query.stream(transaction=transaction)
    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("declaration", "burger")
    assert snapshot.to_dict() == data

    # Verify the mock call.
    firestore_api.run_query.assert_called_once_with(
        request={
            "parent": parent_path,
            "structured_query": query._to_protobuf(),
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )


def test_query_stream_no_results():
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
    query = _make_query(parent)

    get_response = query.stream()
    assert isinstance(get_response, types.GeneratorType)
    assert list(get_response) == []

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


def test_query_stream_second_response_in_empty_stream():
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
    query = _make_query(parent)

    get_response = query.stream()
    assert isinstance(get_response, types.GeneratorType)
    assert list(get_response) == []

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


def test_query_stream_with_skipped_results():
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
    query = _make_query(parent)
    get_response = query.stream()
    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("talk", "and", "chew-gum", "clock")
    assert snapshot.to_dict() == data

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


def test_query_stream_empty_after_first_response():
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
    query = _make_query(parent)
    get_response = query.stream()
    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("charles", "bark")
    assert snapshot.to_dict() == data

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


def test_query_stream_w_collection_group():
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
    query = _make_query(parent)
    query._all_descendants = True
    get_response = query.stream()
    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    to_match = other.document("bark")
    assert snapshot.reference._document_path == to_match._document_path
    assert snapshot.to_dict() == data

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


# Marker: avoids needing to import 'gapic_v1' at module scope.
_not_passed = object()


def _query_stream_w_retriable_exc_helper(
    retry=_not_passed,
    timeout=None,
    transaction=None,
    expect_retry=True,
):
    from google.api_core import exceptions
    from google.api_core import gapic_v1
    from google.cloud.firestore_v1 import _helpers

    if retry is _not_passed:
        retry = gapic_v1.method.DEFAULT

    if transaction is not None:
        expect_retry = False

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query", "_transport"])
    transport = firestore_api._transport = mock.Mock(spec=["run_query"])
    stub = transport.run_query = mock.create_autospec(gapic_v1.method._GapicCallable)
    stub._retry = mock.Mock(spec=["_predicate"])
    stub._predicate = lambda exc: True  # pragma: NO COVER

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
    retriable_exc = exceptions.ServiceUnavailable("testing")

    def _stream_w_exception(*_args, **_kw):
        yield response_pb
        raise retriable_exc

    firestore_api.run_query.side_effect = [_stream_w_exception(), iter([])]
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    query = _make_query(parent)

    get_response = query.stream(transaction=transaction, **kwargs)

    assert isinstance(get_response, types.GeneratorType)
    if expect_retry:
        returned = list(get_response)
    else:
        returned = [next(get_response)]
        with pytest.raises(exceptions.ServiceUnavailable):
            next(get_response)

    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("dee", "sleep")
    assert snapshot.to_dict() == data

    # Verify the mock call.
    parent_path, _ = parent._parent_info()
    calls = firestore_api.run_query.call_args_list

    if expect_retry:
        assert len(calls) == 2
    else:
        assert len(calls) == 1

    if transaction is not None:
        expected_transaction_id = transaction.id
    else:
        expected_transaction_id = None

    assert calls[0] == mock.call(
        request={
            "parent": parent_path,
            "structured_query": query._to_protobuf(),
            "transaction": expected_transaction_id,
        },
        metadata=client._rpc_metadata,
        **kwargs,
    )

    if expect_retry:
        new_query = query.start_after(snapshot)
        assert calls[1] == mock.call(
            request={
                "parent": parent_path,
                "structured_query": new_query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )


def test_query_stream_w_retriable_exc_w_defaults():
    _query_stream_w_retriable_exc_helper()


def test_query_stream_w_retriable_exc_w_retry():
    retry = mock.Mock(spec=["_predicate"])
    retry._predicate = lambda exc: False
    _query_stream_w_retriable_exc_helper(retry=retry, expect_retry=False)


def test_query_stream_w_retriable_exc_w_transaction():
    from google.cloud.firestore_v1 import transaction

    txn = transaction.Transaction(client=mock.Mock(spec=[]))
    txn._id = b"DEADBEEF"
    _query_stream_w_retriable_exc_helper(transaction=txn)


@mock.patch("google.cloud.firestore_v1.query.Watch", autospec=True)
def test_query_on_snapshot(watch):
    query = _make_query(mock.sentinel.parent)
    query.on_snapshot(None)
    watch.for_query.assert_called_once()


def _make_collection_group(*args, **kwargs):
    from google.cloud.firestore_v1.query import CollectionGroup

    return CollectionGroup(*args, **kwargs)


def test_collection_group_constructor():
    query = _make_collection_group(mock.sentinel.parent)
    assert query._parent is mock.sentinel.parent
    assert query._projection is None
    assert query._field_filters == ()
    assert query._orders == ()
    assert query._limit is None
    assert query._offset is None
    assert query._start_at is None
    assert query._end_at is None
    assert query._all_descendants


def test_collection_group_constructor_all_descendents_is_false():
    with pytest.raises(ValueError):
        _make_collection_group(mock.sentinel.parent, all_descendants=False)


def _collection_group_get_partitions_helper(retry=None, timeout=None):
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
    query = _make_collection_group(parent)

    get_response = query.get_partitions(2, **kwargs)

    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 3

    # Verify the mock call.
    parent_path, _ = parent._parent_info()
    partition_query = _make_collection_group(
        parent,
        orders=(query._make_order("__name__", query.ASCENDING),),
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


def test_collection_group_get_partitions():
    _collection_group_get_partitions_helper()


def test_collection_group_get_partitions_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _collection_group_get_partitions_helper(retry=retry, timeout=timeout)


def test_collection_group_get_partitions_w_filter():
    # Make a **real** collection reference as parent.
    client = _make_client()
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).where("foo", "==", "bar")
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


def test_collection_group_get_partitions_w_projection():
    # Make a **real** collection reference as parent.
    client = _make_client()
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).select("foo")
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


def test_collection_group_get_partitions_w_limit():
    # Make a **real** collection reference as parent.
    client = _make_client()
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).limit(10)
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


def test_collection_group_get_partitions_w_offset():
    # Make a **real** collection reference as parent.
    client = _make_client()
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).offset(10)
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


def _make_client(project="project-project"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)
