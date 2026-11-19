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

import datetime
import types

import mock
import pytest

from google.cloud.firestore_v1.base_client import DEFAULT_DATABASE
from google.cloud.firestore_v1.query_profile import ExplainMetrics, QueryExplainError
from google.cloud.firestore_v1.query_results import QueryResultsList
from tests.unit.v1._test_helpers import DEFAULT_TEST_PROJECT, make_client, make_query
from tests.unit.v1.test_base_query import _make_cursor_pb, _make_query_response


def test_query_constructor():
    query = make_query(mock.sentinel.parent)
    assert query._parent is mock.sentinel.parent
    assert query._projection is None
    assert query._field_filters == ()
    assert query._orders == ()
    assert query._limit is None
    assert query._offset is None
    assert query._start_at is None
    assert query._end_at is None
    assert not query._all_descendants


def _query_get_helper(
    retry=None,
    timeout=None,
    database=None,
    explain_options=None,
    read_time=None,
):
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")

    # Add a dummy response to the minimal fake GAPIC.
    _, expected_prefix = parent._parent_info()
    name = "{}/sleep".format(expected_prefix)
    data = {"snooze": 10}
    explain_metrics = {"execution_stats": {"results_returned": 1}}

    response_pb = _make_query_response(
        name=name,
        data=data,
        explain_metrics=explain_metrics,
    )
    firestore_api.run_query.return_value = iter([response_pb])
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    query = make_query(parent)
    returned = query.get(**kwargs, explain_options=explain_options, read_time=read_time)

    assert isinstance(returned, QueryResultsList)
    assert len(returned) == 1

    snapshot = returned[0]
    assert snapshot.reference._path, "dee" == "sleep"
    assert snapshot.to_dict() == data

    if explain_options is None:
        with pytest.raises(QueryExplainError, match="explain_options not set"):
            returned.get_explain_metrics()
    else:
        actual_explain_metrics = returned.get_explain_metrics()
        assert isinstance(actual_explain_metrics, ExplainMetrics)
        assert actual_explain_metrics.execution_stats.results_returned == 1

    # Create expected request body.
    parent_path, _ = parent._parent_info()
    request = {
        "parent": parent_path,
        "structured_query": query._to_protobuf(),
        "transaction": None,
    }
    if explain_options:
        request["explain_options"] = explain_options._to_dict()
    if read_time:
        request["read_time"] = read_time

    # Verify the mock call.
    firestore_api.run_query.assert_called_once_with(
        request=request,
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


def test_query_get_w_read_time():
    read_time = datetime.datetime.now(tz=datetime.timezone.utc)
    _query_get_helper(read_time=read_time)


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_get_limit_to_last(database):
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import _enum_from_direction

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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
    query = make_query(parent)
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


def test_query_get_w_explain_options():
    from google.cloud.firestore_v1.query_profile import ExplainOptions

    explain_options = ExplainOptions(analyze=True)
    _query_get_helper(explain_options=explain_options)


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_sum(database):
    from google.cloud.firestore_v1.base_aggregation import SumAggregation
    from google.cloud.firestore_v1.field_path import FieldPath

    client = make_client(database=database)
    parent = client.collection("dee")
    field_str = "field_str"
    field_path = FieldPath("foo", "bar")
    query = make_query(parent)
    # test with only field populated
    sum_query = query.sum(field_str)
    sum_agg = sum_query._aggregations[0]
    assert isinstance(sum_agg, SumAggregation)
    assert sum_agg.field_ref == field_str
    assert sum_agg.alias is None
    # test with field and alias populated
    sum_query = query.sum(field_str, alias="alias")
    sum_agg = sum_query._aggregations[0]
    assert isinstance(sum_agg, SumAggregation)
    assert sum_agg.field_ref == field_str
    assert sum_agg.alias == "alias"
    # test with field_path
    sum_query = query.sum(field_path, alias="alias")
    sum_agg = sum_query._aggregations[0]
    assert isinstance(sum_agg, SumAggregation)
    assert sum_agg.field_ref == "foo.bar"
    assert sum_agg.alias == "alias"


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_avg(database):
    from google.cloud.firestore_v1.base_aggregation import AvgAggregation
    from google.cloud.firestore_v1.field_path import FieldPath

    client = make_client(database=database)
    parent = client.collection("dee")
    field_str = "field_str"
    field_path = FieldPath("foo", "bar")
    query = make_query(parent)
    # test with only field populated
    avg_query = query.avg(field_str)
    avg_agg = avg_query._aggregations[0]
    assert isinstance(avg_agg, AvgAggregation)
    assert avg_agg.field_ref == field_str
    assert avg_agg.alias is None
    # test with field and alias populated
    avg_query = query.avg(field_str, alias="alias")
    avg_agg = avg_query._aggregations[0]
    assert isinstance(avg_agg, AvgAggregation)
    assert avg_agg.field_ref == field_str
    assert avg_agg.alias == "alias"
    # test with field_path
    avg_query = query.avg(field_path, alias="alias")
    avg_agg = avg_query._aggregations[0]
    assert isinstance(avg_agg, AvgAggregation)
    assert avg_agg.field_ref == "foo.bar"
    assert avg_agg.alias == "alias"


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_chunkify_w_empty(database):
    client = make_client(database=database)
    firestore_api = mock.Mock(spec=["run_query"])
    firestore_api.run_query.return_value = iter([])
    client._firestore_api_internal = firestore_api
    query = client.collection("asdf")._query()

    chunks = list(query._chunkify(10))

    assert chunks == [[]]


@pytest.mark.parametrize(
    "database, expected", [(None, DEFAULT_DATABASE), ("somedb", "somedb")]
)
def test_query_chunkify_w_chunksize_lt_limit(database, expected):
    from google.cloud.firestore_v1.types.document import Document
    from google.cloud.firestore_v1.types.firestore import RunQueryResponse

    client = make_client(database=database)
    firestore_api = mock.Mock(spec=["run_query"])
    doc_ids = [
        f"projects/{DEFAULT_TEST_PROJECT}/databases/{expected}/documents/asdf/{index}"
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


@pytest.mark.parametrize(
    "database, expected", [(None, DEFAULT_DATABASE), ("somedb", "somedb")]
)
def test_query_chunkify_w_chunksize_gt_limit(database, expected):
    from google.cloud.firestore_v1.types.document import Document
    from google.cloud.firestore_v1.types.firestore import RunQueryResponse

    client = make_client(database=database)
    firestore_api = mock.Mock(spec=["run_query"])
    doc_ids = [
        f"projects/{DEFAULT_TEST_PROJECT}/databases/{expected}/documents/asdf/{index}"
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


def _query_stream_helper(
    retry=None,
    timeout=None,
    database=None,
    explain_options=None,
    read_time=None,
):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")

    # Add a dummy response to the minimal fake GAPIC.
    _, expected_prefix = parent._parent_info()
    name = "{}/sleep".format(expected_prefix)
    data = {"snooze": 10}
    if explain_options is not None:
        explain_metrics = {"execution_stats": {"results_returned": 1}}
    else:
        explain_metrics = None
    response_pb = _make_query_response(
        name=name, data=data, explain_metrics=explain_metrics
    )
    firestore_api.run_query.return_value = iter([response_pb])
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    query = make_query(parent)

    get_response = query.stream(
        **kwargs, explain_options=explain_options, read_time=read_time
    )

    assert isinstance(get_response, StreamGenerator)
    returned = list(get_response)
    assert len(returned) == 1
    snapshot = returned[0]
    assert snapshot.reference._path == ("dee", "sleep")
    assert snapshot.to_dict() == data

    # Verify explain_metrics.
    if explain_options is None:
        with pytest.raises(QueryExplainError, match="explain_options not set"):
            get_response.get_explain_metrics()
    else:
        explain_metrics = get_response.get_explain_metrics()
        assert isinstance(explain_metrics, ExplainMetrics)
        assert explain_metrics.execution_stats.results_returned == 1

    # Create expected request body.
    parent_path, _ = parent._parent_info()
    request = {
        "parent": parent_path,
        "structured_query": query._to_protobuf(),
        "transaction": None,
    }
    if explain_options is not None:
        request["explain_options"] = explain_options._to_dict()
    if read_time is not None:
        request["read_time"] = read_time

    # Verify the mock call.
    firestore_api.run_query.assert_called_once_with(
        request=request,
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


def test_query_stream_w_read_time():
    read_time = datetime.datetime.now(tz=datetime.timezone.utc)
    _query_stream_helper(read_time=read_time)


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_with_limit_to_last(database):
    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    # Execute the query and check the response.
    query = make_query(parent)
    query = query.limit_to_last(2)

    stream_response = query.stream()

    with pytest.raises(ValueError):
        list(stream_response)


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_with_transaction(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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
    query = make_query(parent)
    get_response = query.stream(transaction=transaction)
    assert isinstance(get_response, StreamGenerator)
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


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_with_transaction_and_read_time(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    client._firestore_api_internal = firestore_api

    # Create a real-ish transaction for this client.
    transaction = client.transaction()
    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id

    # Create a read_time for this client.
    read_time = datetime.datetime.now(tz=datetime.timezone.utc)

    # Make a **real** collection reference as parent.
    parent = client.collection("declaration")

    # Add a dummy response to the minimal fake GAPIC.
    parent_path, expected_prefix = parent._parent_info()
    name = "{}/burger".format(expected_prefix)
    data = {"lettuce": b"\xee\x87"}
    response_pb = _make_query_response(name=name, data=data)
    firestore_api.run_query.return_value = iter([response_pb])

    # Execute the query and check the response.
    query = make_query(parent)
    get_response = query.stream(transaction=transaction, read_time=read_time)
    assert isinstance(get_response, StreamGenerator)
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
            "read_time": read_time,
        },
        metadata=client._rpc_metadata,
    )


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_no_results(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC with a dummy response.
    firestore_api = mock.Mock(spec=["run_query"])
    empty_response = _make_query_response()
    run_query_response = iter([empty_response])
    firestore_api.run_query.return_value = run_query_response

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dah", "dah", "dum")
    query = make_query(parent)

    get_response = query.stream()
    assert isinstance(get_response, StreamGenerator)
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


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_second_response_in_empty_stream(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC with a dummy response.
    firestore_api = mock.Mock(spec=["run_query"])
    empty_response1 = _make_query_response()
    empty_response2 = _make_query_response()
    run_query_response = iter([empty_response1, empty_response2])
    firestore_api.run_query.return_value = run_query_response

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dah", "dah", "dum")
    query = make_query(parent)

    get_response = query.stream()
    assert isinstance(get_response, StreamGenerator)
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


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_with_skipped_results(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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
    query = make_query(parent)
    get_response = query.stream()
    assert isinstance(get_response, StreamGenerator)
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


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_empty_after_first_response(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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
    query = make_query(parent)
    get_response = query.stream()
    assert isinstance(get_response, StreamGenerator)
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


@pytest.mark.parametrize("database", [None, "somedb"])
def test_query_stream_w_collection_group(database):
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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
    query = make_query(parent)
    query._all_descendants = True
    get_response = query.stream()
    assert isinstance(get_response, StreamGenerator)
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
    database=None,
    read_time=None,
):
    from google.api_core import exceptions, gapic_v1

    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.stream_generator import StreamGenerator

    if retry is _not_passed:
        retry = gapic_v1.method.DEFAULT

    if transaction is not None:
        expect_retry = False

    # Use the client's real GAPIC client and transport, so the default retry
    # policy is looked up as it is in production. Stub out only the RPC.
    client = make_client(database=database)
    firestore_api = client._firestore_api
    firestore_api.run_query = mock.Mock()

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
    query = make_query(parent)

    get_response = query.stream(transaction=transaction, read_time=read_time, **kwargs)

    assert isinstance(get_response, StreamGenerator)
    with mock.patch("time.sleep") as sleep:
        if expect_retry:
            returned = list(get_response)
        else:
            returned = [next(get_response)]
            with pytest.raises(exceptions.ServiceUnavailable):
                next(get_response)

    assert sleep.call_count == (1 if expect_retry else 0)
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

    expected_request = {
        "parent": parent_path,
        "structured_query": query._to_protobuf(),
        "transaction": expected_transaction_id,
    }
    if read_time is not None:
        expected_request["read_time"] = read_time

    assert calls[0] == mock.call(
        request=expected_request,
        metadata=client._rpc_metadata,
        **kwargs,
    )

    if expect_retry:
        new_query = query.start_after(snapshot)
        expected_request = {
            "parent": parent_path,
            "structured_query": new_query._to_protobuf(),
            "transaction": None,
        }
        if read_time is not None:
            expected_request["read_time"] = read_time
        assert calls[1] == mock.call(
            request=expected_request,
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


def test_query_stream_w_retriable_exc_w_read_time():
    read_time = datetime.datetime.now(tz=datetime.timezone.utc)
    _query_stream_w_retriable_exc_helper(read_time=read_time)


def _make_resumable_query(*query_methods, database=None):
    """A query on a real client whose ``run_query`` RPC is stubbed out."""
    client = make_client(database=database)
    client._firestore_api.run_query = mock.Mock()
    query = make_query(client.collection("dee"))
    for name, args in query_methods:
        query = getattr(query, name)(*args)
    return client, query


def _doc_response(client, doc_id):
    _, expected_prefix = client.collection("dee")._parent_info()
    return _make_query_response(
        name="{}/{}".format(expected_prefix, doc_id), data={"id": doc_id}
    )


def _stream_then_raise(responses, exc):
    yield from responses
    raise exc


def _sent_query(call):
    return call.kwargs["request"]["structured_query"]


@pytest.mark.parametrize(
    "exc_class, expected",
    [
        ("ServiceUnavailable", True),
        ("InternalServerError", True),
        ("DeadlineExceeded", True),
        ("PermissionDenied", False),
        ("InvalidArgument", False),
    ],
)
def test_query__retry_query_after_exception_w_default_retry(exc_class, expected):
    # Regression test for #19129: the default retry policy must be read from
    # the wrapped GAPIC method, not from the raw gRPC stub.
    from google.api_core import exceptions, gapic_v1

    client, query = _make_resumable_query()
    exc = getattr(exceptions, exc_class)("testing")

    assert (
        query._retry_query_after_exception(exc, gapic_v1.method.DEFAULT, None)
        is expected
    )


def test_query__retry_query_after_exception_w_retry_none():
    from google.api_core import exceptions

    client, query = _make_resumable_query()
    exc = exceptions.ServiceUnavailable("testing")

    assert query._retry_query_after_exception(exc, None, None) is False


def test_query_stream_w_retry_none_reraises_original_exc():
    from google.api_core import exceptions

    client, query = _make_resumable_query()
    exc = exceptions.ServiceUnavailable("testing")
    client._firestore_api.run_query.side_effect = [_stream_then_raise([], exc)]

    with pytest.raises(exceptions.ServiceUnavailable) as exc_info:
        list(query.stream(retry=None))

    assert exc_info.value is exc
    assert client._firestore_api.run_query.call_count == 1


def test_query_stream_w_default_retry_non_retriable_exc():
    from google.api_core import exceptions

    client, query = _make_resumable_query()
    exc = exceptions.PermissionDenied("testing")
    client._firestore_api.run_query.side_effect = [_stream_then_raise([], exc)]

    with pytest.raises(exceptions.PermissionDenied) as exc_info:
        list(query.stream())

    assert exc_info.value is exc
    assert client._firestore_api.run_query.call_count == 1


def test_query_stream_resume_before_first_doc_keeps_original_cursor():
    from google.api_core import exceptions

    client, query = _make_resumable_query(
        ("order_by", ("a",)), ("start_at", ({"a": 5},))
    )
    run_query = client._firestore_api.run_query
    run_query.side_effect = [
        _stream_then_raise([], exceptions.ServiceUnavailable("testing")),
        iter([_doc_response(client, "one")]),
    ]

    with mock.patch("time.sleep"):
        returned = list(query.stream())

    assert [snap.id for snap in returned] == ["one"]
    first, second = run_query.call_args_list
    # The resumed query is the original query, start cursor included.
    assert _sent_query(second) == _sent_query(first) == query._to_protobuf()
    assert _sent_query(second).start_at.values


def test_query_stream_resume_adjusts_limit_and_offset():
    from google.api_core import exceptions

    client, query = _make_resumable_query(("limit", (3,)), ("offset", (2,)))
    run_query = client._firestore_api.run_query
    run_query.side_effect = [
        _stream_then_raise(
            [_doc_response(client, "one")], exceptions.ServiceUnavailable("x")
        ),
        iter([_doc_response(client, "two"), _doc_response(client, "three")]),
    ]

    with mock.patch("time.sleep"):
        returned = list(query.stream())

    assert [snap.id for snap in returned] == ["one", "two", "three"]
    resumed = _sent_query(run_query.call_args_list[1])
    expected = query.start_after(returned[0])._copy(limit=2, offset=None)
    assert resumed == expected._to_protobuf()
    assert resumed.limit == 2
    assert resumed.offset == 0


def test_query_stream_resume_skipped_when_limit_reached():
    from google.api_core import exceptions

    client, query = _make_resumable_query(("limit", (1,)))
    run_query = client._firestore_api.run_query
    run_query.side_effect = [
        _stream_then_raise(
            [_doc_response(client, "one")], exceptions.ServiceUnavailable("x")
        ),
    ]

    with mock.patch("time.sleep") as sleep:
        returned = list(query.stream())

    assert [snap.id for snap in returned] == ["one"]
    assert run_query.call_count == 1
    sleep.assert_not_called()


def test_query_stream_resume_gives_up_after_retry_timeout():
    from google.api_core import exceptions
    from google.api_core import retry as retries

    client, query = _make_resumable_query()
    exc = exceptions.ServiceUnavailable("testing")
    client._firestore_api.run_query.side_effect = lambda **_: _stream_then_raise(
        [], exc
    )
    retry = retries.Retry(
        predicate=retries.if_exception_type(exceptions.ServiceUnavailable),
        initial=1.0,
        maximum=1.0,
        timeout=10.0,
    )

    # The clock advances 4 seconds per check: give up on the third attempt.
    clock = iter(range(0, 100, 4))
    with (
        mock.patch("time.sleep") as sleep,
        mock.patch("time.monotonic", side_effect=lambda: next(clock)),
    ):
        with pytest.raises(exceptions.ServiceUnavailable) as exc_info:
            list(query.stream(retry=retry))

    assert exc_info.value is exc
    assert sleep.call_count == 2
    assert client._firestore_api.run_query.call_count == 3


def test_query_stream_resume_backoff_resets_after_progress():
    from google.api_core import exceptions

    client, query = _make_resumable_query()
    run_query = client._firestore_api.run_query
    run_query.side_effect = [
        _stream_then_raise(
            [_doc_response(client, "one")], exceptions.ServiceUnavailable("x")
        ),
        _stream_then_raise(
            [_doc_response(client, "two")], exceptions.ServiceUnavailable("x")
        ),
        iter([]),
    ]

    with mock.patch(
        "google.cloud.firestore_v1._helpers.StreamResumeBackoff"
    ) as backoff_class:
        backoff_class.return_value.wait.return_value = True
        returned = list(query.stream())

    assert [snap.id for snap in returned] == ["one", "two"]
    # A document arrived between the two failures, so a fresh backoff is used.
    assert backoff_class.call_count == 2
    assert run_query.call_count == 3


def test_query_stream_w_explain_options():
    from google.cloud.firestore_v1.query_profile import ExplainOptions

    explain_options = ExplainOptions(analyze=True)
    _query_stream_helper(explain_options=explain_options)


@mock.patch("google.cloud.firestore_v1.query.Watch", autospec=True)
def test_query_on_snapshot(watch):
    query = make_query(mock.sentinel.parent)
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


def _collection_group_get_partitions_helper(
    retry=None, timeout=None, database=None, read_time=None
):
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["partition_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client(database=database)
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

    get_response = query.get_partitions(2, read_time=read_time, **kwargs)

    assert isinstance(get_response, types.GeneratorType)
    returned = list(get_response)
    assert len(returned) == 3

    # Verify the mock call.
    parent_path, _ = parent._parent_info()
    partition_query = _make_collection_group(
        parent,
        orders=(query._make_order("__name__", query.ASCENDING),),
    )
    expected_request = {
        "parent": parent_path,
        "structured_query": partition_query._to_protobuf(),
        "partition_count": 2,
    }
    if read_time is not None:
        expected_request["read_time"] = read_time
    firestore_api.partition_query.assert_called_once_with(
        request=expected_request,
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


def test_collection_group_get_partitions_w_read_time():
    read_time = datetime.datetime.now(tz=datetime.timezone.utc)
    _collection_group_get_partitions_helper(read_time=read_time)


@pytest.mark.parametrize("database", [None, "somedb"])
def test_collection_group_get_partitions_w_filter(database):
    # Make a **real** collection reference as parent.
    client = make_client(database=database)
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).where("foo", "==", "bar")
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


@pytest.mark.parametrize("database", [None, "somedb"])
def test_collection_group_get_partitions_w_projection(database):
    # Make a **real** collection reference as parent.
    client = make_client(database=database)
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).select("foo")
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


@pytest.mark.parametrize("database", [None, "somedb"])
def test_collection_group_get_partitions_w_limit(database):
    # Make a **real** collection reference as parent.
    client = make_client(database=database)
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).limit(10)
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


@pytest.mark.parametrize("database", [None, "somedb"])
def test_collection_group_get_partitions_w_offset(database):
    # Make a **real** collection reference as parent.
    client = make_client(database=database)
    parent = client.collection("charles")

    # Make a query that fails to partition
    query = _make_collection_group(parent).offset(10)
    with pytest.raises(ValueError):
        list(query.get_partitions(2))


def test_asyncquery_collection_pipeline_type():
    from google.cloud.firestore_v1.pipeline import Pipeline

    client = make_client()
    parent = client.collection("test")
    query = parent._query()
    ppl = query._build_pipeline(client.pipeline())
    assert isinstance(ppl, Pipeline)


def test_asyncquery_collectiongroup_pipeline_type():
    from google.cloud.firestore_v1.pipeline import Pipeline

    client = make_client()
    query = client.collection_group("test")
    ppl = query._build_pipeline(client.pipeline())
    assert isinstance(ppl, Pipeline)
