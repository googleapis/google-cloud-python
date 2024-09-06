# Copyright 2023 Google LLC All rights reserved.
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

from datetime import datetime, timedelta, timezone

import mock
import pytest

from google.cloud.firestore_v1.base_aggregation import (
    AggregationResult,
    AvgAggregation,
    CountAggregation,
    SumAggregation,
)
from google.cloud.firestore_v1.query_profile import ExplainMetrics, QueryExplainError
from google.cloud.firestore_v1.query_results import QueryResultsList
from google.cloud.firestore_v1.stream_generator import StreamGenerator
from tests.unit.v1._test_helpers import (
    make_aggregation_query,
    make_aggregation_query_response,
    make_client,
    make_query,
)

_PROJECT = "PROJECT"


def test_count_aggregation_to_pb():
    from google.cloud.firestore_v1.types import query as query_pb2

    count_aggregation = CountAggregation(alias="total")

    expected_aggregation_query_pb = query_pb2.StructuredAggregationQuery.Aggregation()
    expected_aggregation_query_pb.count = (
        query_pb2.StructuredAggregationQuery.Aggregation.Count()
    )
    expected_aggregation_query_pb.alias = count_aggregation.alias
    assert count_aggregation._to_protobuf() == expected_aggregation_query_pb


def test_sum_aggregation_w_field_path():
    """
    SumAggregation should convert FieldPath inputs into strings
    """
    from google.cloud.firestore_v1.field_path import FieldPath

    field_path = FieldPath("foo", "bar")
    sum_aggregation = SumAggregation(field_path, alias="total")
    assert sum_aggregation.field_ref == "foo.bar"


def test_avg_aggregation_w_field_path():
    """
    AvgAggregation should convert FieldPath inputs into strings
    """
    from google.cloud.firestore_v1.field_path import FieldPath

    field_path = FieldPath("foo", "bar")
    avg_aggregation = AvgAggregation(field_path, alias="total")
    assert avg_aggregation.field_ref == "foo.bar"


def test_sum_aggregation_to_pb():
    from google.cloud.firestore_v1.types import query as query_pb2

    sum_aggregation = SumAggregation("someref", alias="total")

    expected_aggregation_query_pb = query_pb2.StructuredAggregationQuery.Aggregation()
    expected_aggregation_query_pb.sum = (
        query_pb2.StructuredAggregationQuery.Aggregation.Sum()
    )
    expected_aggregation_query_pb.sum.field.field_path = "someref"

    expected_aggregation_query_pb.alias = sum_aggregation.alias
    assert sum_aggregation._to_protobuf() == expected_aggregation_query_pb


def test_avg_aggregation_to_pb():
    from google.cloud.firestore_v1.types import query as query_pb2

    avg_aggregation = AvgAggregation("someref", alias="total")

    expected_aggregation_query_pb = query_pb2.StructuredAggregationQuery.Aggregation()
    expected_aggregation_query_pb.avg = (
        query_pb2.StructuredAggregationQuery.Aggregation.Avg()
    )
    expected_aggregation_query_pb.avg.field.field_path = "someref"
    expected_aggregation_query_pb.alias = avg_aggregation.alias

    assert avg_aggregation._to_protobuf() == expected_aggregation_query_pb


def test_aggregation_query_constructor():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    assert aggregation_query._collection_ref == query._parent
    assert aggregation_query._nested_query == query
    assert len(aggregation_query._aggregations) == 0
    assert aggregation_query._client == query._parent._client


def test_aggregation_query_add_aggregation():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)
    aggregation_query.add_aggregation(CountAggregation(alias="all"))
    aggregation_query.add_aggregation(SumAggregation("sumref", alias="sum_all"))
    aggregation_query.add_aggregation(AvgAggregation("avgref", alias="avg_all"))

    assert len(aggregation_query._aggregations) == 3
    assert aggregation_query._aggregations[0].alias == "all"
    assert isinstance(aggregation_query._aggregations[0], CountAggregation)

    assert len(aggregation_query._aggregations) == 3
    assert aggregation_query._aggregations[1].alias == "sum_all"
    assert aggregation_query._aggregations[1].field_ref == "sumref"
    assert isinstance(aggregation_query._aggregations[1], SumAggregation)

    assert len(aggregation_query._aggregations) == 3
    assert aggregation_query._aggregations[2].alias == "avg_all"
    assert aggregation_query._aggregations[2].field_ref == "avgref"
    assert isinstance(aggregation_query._aggregations[2], AvgAggregation)


def test_aggregation_query_add_aggregations():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.add_aggregations(
        [
            CountAggregation(alias="all"),
            CountAggregation(alias="total"),
            SumAggregation("sumref", alias="sum_all"),
            AvgAggregation("avgref", alias="avg_all"),
        ]
    )

    assert len(aggregation_query._aggregations) == 4
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[1].alias == "total"
    assert aggregation_query._aggregations[2].alias == "sum_all"
    assert aggregation_query._aggregations[2].field_ref == "sumref"
    assert aggregation_query._aggregations[3].alias == "avg_all"
    assert aggregation_query._aggregations[3].field_ref == "avgref"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)
    assert isinstance(aggregation_query._aggregations[1], CountAggregation)
    assert isinstance(aggregation_query._aggregations[2], SumAggregation)
    assert isinstance(aggregation_query._aggregations[3], AvgAggregation)


def test_aggregation_query_count():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "all"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)


def test_aggregation_query_count_twice():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all").count(alias="total")

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[1].alias == "total"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)
    assert isinstance(aggregation_query._aggregations[1], CountAggregation)


def test_aggregation_query_sum():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.sum("someref", alias="all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)


def test_aggregation_query_sum_twice():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.sum("someref", alias="all").sum("another_ref", alias="total")

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"
    assert aggregation_query._aggregations[1].alias == "total"
    assert aggregation_query._aggregations[1].field_ref == "another_ref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)
    assert isinstance(aggregation_query._aggregations[1], SumAggregation)


def test_aggregation_query_sum_no_alias():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.sum("someref")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias is None
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)


def test_aggregation_query_avg():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.avg("someref", alias="all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)


def test_aggregation_query_avg_twice():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.avg("someref", alias="all").avg("another_ref", alias="total")

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"
    assert aggregation_query._aggregations[1].alias == "total"
    assert aggregation_query._aggregations[1].field_ref == "another_ref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)
    assert isinstance(aggregation_query._aggregations[1], AvgAggregation)


def test_aggregation_query_avg_no_alias():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.avg("someref")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias is None
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)


def test_aggregation_query_to_protobuf():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sumall")
    aggregation_query.avg("anotherref", alias="avgall")
    pb = aggregation_query._to_protobuf()

    assert pb.structured_query == parent._query()._to_protobuf()
    assert len(pb.aggregations) == 3
    assert pb.aggregations[0] == aggregation_query._aggregations[0]._to_protobuf()
    assert pb.aggregations[1] == aggregation_query._aggregations[1]._to_protobuf()
    assert pb.aggregations[2] == aggregation_query._aggregations[2]._to_protobuf()


def test_aggregation_query_prep_stream():
    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sumall")
    aggregation_query.avg("anotherref", alias="avgall")

    request, kwargs = aggregation_query._prep_stream()

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": None,
    }
    assert request == expected_request
    assert kwargs == {"retry": None}


def test_aggregation_query_prep_stream_with_transaction():
    client = make_client()
    transaction = client.transaction()
    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id

    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sumall")
    aggregation_query.avg("anotherref", alias="avgall")

    request, kwargs = aggregation_query._prep_stream(transaction=transaction)

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": txn_id,
    }
    assert request == expected_request
    assert kwargs == {"retry": None}


def test_aggregation_query_prep_stream_with_explain_options():
    from google.cloud.firestore_v1 import query_profile

    client = make_client()
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sumall")
    aggregation_query.avg("anotherref", alias="avgall")

    explain_options = query_profile.ExplainOptions(analyze=True)
    request, kwargs = aggregation_query._prep_stream(explain_options=explain_options)

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": None,
        "explain_options": explain_options._to_dict(),
    }
    assert request == expected_request
    assert kwargs == {"retry": None}


def _aggregation_query_get_helper(
    retry=None,
    timeout=None,
    read_time=None,
    explain_options=None,
):
    from google.cloud._helpers import _datetime_to_pb_timestamp

    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.query_profile import (
        ExplainMetrics,
        QueryExplainError,
    )

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)
    aggregation_query.count(alias="all")

    aggregation_result = AggregationResult(alias="total", value=5, read_time=read_time)

    if explain_options is not None:
        explain_metrics = {"execution_stats": {"results_returned": 1}}
    else:
        explain_metrics = None
    response_pb = make_aggregation_query_response(
        [aggregation_result],
        read_time=read_time,
        explain_metrics=explain_metrics,
    )
    firestore_api.run_aggregation_query.return_value = iter([response_pb])
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    returned = aggregation_query.get(**kwargs, explain_options=explain_options)
    assert isinstance(returned, QueryResultsList)
    assert len(returned) == 1

    for result in returned:
        for r in result:
            assert r.alias == aggregation_result.alias
            assert r.value == aggregation_result.value
            if read_time is not None:
                result_datetime = _datetime_to_pb_timestamp(r.read_time)
                assert result_datetime == read_time

    assert returned._explain_options == explain_options
    assert returned.explain_options == explain_options

    if explain_options is None:
        with pytest.raises(QueryExplainError, match="explain_options not set"):
            returned.get_explain_metrics()
    else:
        actual_explain_metrics = returned.get_explain_metrics()
        assert isinstance(actual_explain_metrics, ExplainMetrics)
        assert actual_explain_metrics.execution_stats.results_returned == 1

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": None,
    }
    if explain_options is not None:
        expected_request["explain_options"] = explain_options._to_dict()

    # Verify the mock call.
    firestore_api.run_aggregation_query.assert_called_once_with(
        request=expected_request,
        metadata=client._rpc_metadata,
        **kwargs,
    )


def test_aggregation_query_get():
    _aggregation_query_get_helper()


def test_aggregation_query_get_with_readtime():
    from google.cloud._helpers import _datetime_to_pb_timestamp

    one_hour_ago = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    read_time = _datetime_to_pb_timestamp(one_hour_ago)
    _aggregation_query_get_helper(read_time=read_time)


def test_aggregation_query_get_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _aggregation_query_get_helper(retry=retry, timeout=timeout)


def test_aggregation_query_get_transaction():
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")

    transaction = client.transaction()

    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id

    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)
    aggregation_query.count(alias="all")

    aggregation_result = AggregationResult(alias="total", value=5)
    response_pb = make_aggregation_query_response(
        [aggregation_result], transaction=txn_id
    )
    firestore_api.run_aggregation_query.return_value = iter([response_pb])
    retry = None
    timeout = None
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    returned = aggregation_query.get(transaction=transaction, **kwargs)
    assert isinstance(returned, list)
    assert len(returned) == 1

    for result in returned:
        for r in result:
            assert r.alias == aggregation_result.alias
            assert r.value == aggregation_result.value

    # Verify the mock call.
    parent_path, _ = parent._parent_info()

    firestore_api.run_aggregation_query.assert_called_once_with(
        request={
            "parent": parent_path,
            "structured_aggregation_query": aggregation_query._to_protobuf(),
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
        **kwargs,
    )


def test_aggregation_query_get_w_explain_options():
    from google.cloud.firestore_v1.query_profile import ExplainOptions

    _aggregation_query_get_helper(explain_options=ExplainOptions(analyze=True))


_not_passed = object()


def _aggregation_query_stream_w_retriable_exc_helper(
    retry=_not_passed,
    timeout=None,
    transaction=None,
    expect_retry=True,
):
    from google.api_core import exceptions, gapic_v1

    from google.cloud.firestore_v1 import _helpers, stream_generator

    if retry is _not_passed:
        retry = gapic_v1.method.DEFAULT

    if transaction is not None:
        expect_retry = False

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_aggregation_query", "_transport"])
    transport = firestore_api._transport = mock.Mock(spec=["run_aggregation_query"])
    stub = transport.run_aggregation_query = mock.create_autospec(
        gapic_v1.method._GapicCallable
    )
    stub._retry = mock.Mock(spec=["_predicate"])
    stub._predicate = lambda exc: True  # pragma: NO COVER

    # Attach the fake GAPIC to a real client.
    client = make_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")

    aggregation_result = AggregationResult(alias="total", value=5)
    response_pb = make_aggregation_query_response([aggregation_result])

    retriable_exc = exceptions.ServiceUnavailable("testing")

    def _stream_w_exception(*_args, **_kw):
        yield response_pb
        raise retriable_exc

    firestore_api.run_aggregation_query.side_effect = [_stream_w_exception(), iter([])]
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)

    get_response = aggregation_query.stream(transaction=transaction, **kwargs)

    assert isinstance(get_response, stream_generator.StreamGenerator)
    if expect_retry:
        returned = list(get_response)
    else:
        returned = [next(get_response)]
        with pytest.raises(exceptions.ServiceUnavailable):
            next(get_response)

    assert len(returned) == 1

    for result in returned:
        for r in result:
            assert r.alias == aggregation_result.alias
            assert r.value == aggregation_result.value

    # Verify the mock call.
    parent_path, _ = parent._parent_info()
    calls = firestore_api.run_aggregation_query.call_args_list

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
            "structured_aggregation_query": aggregation_query._to_protobuf(),
            "transaction": expected_transaction_id,
        },
        metadata=client._rpc_metadata,
        **kwargs,
    )

    if expect_retry:
        assert calls[1] == mock.call(
            request={
                "parent": parent_path,
                "structured_aggregation_query": aggregation_query._to_protobuf(),
                "transaction": None,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )


def test_aggregation_query_stream_w_retriable_exc_w_defaults():
    _aggregation_query_stream_w_retriable_exc_helper()


def test_aggregation_query_stream_w_retriable_exc_w_retry():
    retry = mock.Mock(spec=["_predicate"])
    retry._predicate = lambda exc: False
    _aggregation_query_stream_w_retriable_exc_helper(retry=retry, expect_retry=False)


def test_aggregation_query_stream_w_retriable_exc_w_transaction():
    from google.cloud.firestore_v1 import transaction

    txn = transaction.Transaction(client=mock.Mock(spec=[]))
    txn._id = b"DEADBEEF"
    _aggregation_query_stream_w_retriable_exc_helper(transaction=txn)


def _aggregation_query_stream_helper(
    retry=None,
    timeout=None,
    read_time=None,
    explain_options=None,
):
    from google.cloud._helpers import _datetime_to_pb_timestamp

    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    query = make_query(parent)
    aggregation_query = make_aggregation_query(query)
    aggregation_query.count(alias="all")

    if explain_options is not None and explain_options.analyze is False:
        results_list = []
    else:
        aggregation_result = AggregationResult(
            alias="total", value=5, read_time=read_time
        )
        results_list = [aggregation_result]

    if explain_options is not None:
        explain_metrics = {"execution_stats": {"results_returned": 1}}
    else:
        explain_metrics = None
    response_pb = make_aggregation_query_response(
        results_list,
        read_time=read_time,
        explain_metrics=explain_metrics,
    )
    firestore_api.run_aggregation_query.return_value = iter([response_pb])
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    returned = aggregation_query.stream(**kwargs, explain_options=explain_options)
    assert isinstance(returned, StreamGenerator)

    results = []
    for result in returned:
        for r in result:
            assert r.alias == aggregation_result.alias
            assert r.value == aggregation_result.value
            if read_time is not None:
                result_datetime = _datetime_to_pb_timestamp(r.read_time)
                assert result_datetime == read_time
        results.append(result)
    assert len(results) == len(results_list)

    if explain_options is None:
        with pytest.raises(QueryExplainError, match="explain_options not set"):
            returned.get_explain_metrics()
    else:
        explain_metrics = returned.get_explain_metrics()
        assert isinstance(explain_metrics, ExplainMetrics)
        assert explain_metrics.execution_stats.results_returned == 1

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": None,
    }
    if explain_options is not None:
        expected_request["explain_options"] = explain_options._to_dict()

    # Verify the mock call.
    firestore_api.run_aggregation_query.assert_called_once_with(
        request=expected_request,
        metadata=client._rpc_metadata,
        **kwargs,
    )


def test_aggregation_query_stream():
    _aggregation_query_stream_helper()


def test_aggregation_query_stream_with_readtime():
    from google.cloud._helpers import _datetime_to_pb_timestamp

    one_hour_ago = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    read_time = _datetime_to_pb_timestamp(one_hour_ago)
    _aggregation_query_stream_helper(read_time=read_time)


def test_aggregation_query_stream_w_explain_options_analyze_true():
    from google.cloud.firestore_v1.query_profile import ExplainOptions

    _aggregation_query_stream_helper(explain_options=ExplainOptions(analyze=True))


def test_aggregation_query_stream_w_explain_options_analyze_false():
    from google.cloud.firestore_v1.query_profile import ExplainOptions

    _aggregation_query_stream_helper(explain_options=ExplainOptions(analyze=False))


def test_aggregation_from_query():
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = mock.Mock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    query = make_query(parent)

    transaction = client.transaction()

    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id

    aggregation_result = AggregationResult(alias="total", value=5)
    response_pb = make_aggregation_query_response(
        [aggregation_result], transaction=txn_id
    )
    retry = None
    timeout = None
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    for aggregation_query in [
        query.count(alias="total"),
        query.sum("foo", alias="total"),
        query.avg("foo", alias="total"),
    ]:
        # reset api mock
        firestore_api.run_aggregation_query.reset_mock()
        firestore_api.run_aggregation_query.return_value = iter([response_pb])
        # run query
        returned = aggregation_query.get(transaction=transaction, **kwargs)
        assert isinstance(returned, list)
        assert len(returned) == 1

        for result in returned:
            for r in result:
                assert r.alias == aggregation_result.alias
                assert r.value == aggregation_result.value

        # Verify the mock call.
        parent_path, _ = parent._parent_info()

        firestore_api.run_aggregation_query.assert_called_once_with(
            request={
                "parent": parent_path,
                "structured_aggregation_query": aggregation_query._to_protobuf(),
                "transaction": txn_id,
            },
            metadata=client._rpc_metadata,
            **kwargs,
        )
