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

import pytest

from google.cloud.firestore_v1.base_aggregation import (
    AggregationResult,
    AvgAggregation,
    CountAggregation,
    SumAggregation,
)
from tests.unit.v1._test_helpers import (
    make_aggregation_query_response,
    make_async_aggregation_query,
    make_async_client,
    make_async_query,
)
from tests.unit.v1.test__helpers import AsyncIter, AsyncMock

_PROJECT = "PROJECT"


def test_async_aggregation_query_constructor():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    assert aggregation_query._collection_ref == parent
    assert aggregation_query._nested_query == parent._query()
    assert len(aggregation_query._aggregations) == 0
    assert aggregation_query._client == client


def test_async_aggregation_query_add_aggregation():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.add_aggregation(CountAggregation(alias="all"))
    aggregation_query.add_aggregation(SumAggregation("someref", alias="sum_all"))
    aggregation_query.add_aggregation(AvgAggregation("otherref", alias="avg_all"))

    assert len(aggregation_query._aggregations) == 3

    assert aggregation_query._aggregations[0].alias == "all"
    assert isinstance(aggregation_query._aggregations[0], CountAggregation)

    assert aggregation_query._aggregations[1].field_ref == "someref"
    assert aggregation_query._aggregations[1].alias == "sum_all"
    assert isinstance(aggregation_query._aggregations[1], SumAggregation)

    assert aggregation_query._aggregations[2].field_ref == "otherref"
    assert aggregation_query._aggregations[2].alias == "avg_all"
    assert isinstance(aggregation_query._aggregations[2], AvgAggregation)


def test_async_aggregation_query_add_aggregations():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.add_aggregations(
        [
            CountAggregation(alias="all"),
            CountAggregation(alias="total"),
            SumAggregation("someref", alias="sum_all"),
            AvgAggregation("otherref", alias="avg_all"),
        ]
    )

    assert len(aggregation_query._aggregations) == 4
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[1].alias == "total"

    assert aggregation_query._aggregations[2].field_ref == "someref"
    assert aggregation_query._aggregations[2].alias == "sum_all"

    assert aggregation_query._aggregations[3].field_ref == "otherref"
    assert aggregation_query._aggregations[3].alias == "avg_all"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)
    assert isinstance(aggregation_query._aggregations[1], CountAggregation)
    assert isinstance(aggregation_query._aggregations[2], SumAggregation)
    assert isinstance(aggregation_query._aggregations[3], AvgAggregation)


def test_async_aggregation_query_count():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.count(alias="all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "all"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)


def test_async_aggregation_query_count_twice():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.count(alias="all").count(alias="total")

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[1].alias == "total"

    assert isinstance(aggregation_query._aggregations[0], CountAggregation)
    assert isinstance(aggregation_query._aggregations[1], CountAggregation)


def test_async_aggregation_sum():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.sum("someref", alias="sum_all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "sum_all"
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)


def test_async_aggregation_query_sum_twice():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.sum("someref", alias="sum_all").sum(
        "another_ref", alias="sum_total"
    )

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "sum_all"
    assert aggregation_query._aggregations[0].field_ref == "someref"
    assert aggregation_query._aggregations[1].alias == "sum_total"
    assert aggregation_query._aggregations[1].field_ref == "another_ref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)
    assert isinstance(aggregation_query._aggregations[1], SumAggregation)


def test_async_aggregation_sum_no_alias():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.sum("someref")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias is None
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], SumAggregation)


def test_aggregation_query_avg():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.avg("someref", alias="all")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)


def test_aggregation_query_avg_twice():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.avg("someref", alias="all").avg("another_ref", alias="total")

    assert len(aggregation_query._aggregations) == 2
    assert aggregation_query._aggregations[0].alias == "all"
    assert aggregation_query._aggregations[0].field_ref == "someref"
    assert aggregation_query._aggregations[1].alias == "total"
    assert aggregation_query._aggregations[1].field_ref == "another_ref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)
    assert isinstance(aggregation_query._aggregations[1], AvgAggregation)


def test_aggregation_query_avg_no_alias():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.avg("someref")

    assert len(aggregation_query._aggregations) == 1
    assert aggregation_query._aggregations[0].alias is None
    assert aggregation_query._aggregations[0].field_ref == "someref"

    assert isinstance(aggregation_query._aggregations[0], AvgAggregation)


def test_async_aggregation_query_to_protobuf():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sum_all")
    aggregation_query.avg("someref", alias="avg_all")
    pb = aggregation_query._to_protobuf()

    assert pb.structured_query == parent._query()._to_protobuf()
    assert len(pb.aggregations) == 3
    assert pb.aggregations[0] == aggregation_query._aggregations[0]._to_protobuf()
    assert pb.aggregations[1] == aggregation_query._aggregations[1]._to_protobuf()
    assert pb.aggregations[2] == aggregation_query._aggregations[2]._to_protobuf()


def test_async_aggregation_query_prep_stream():
    client = make_async_client()
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)

    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sum_all")
    aggregation_query.avg("someref", alias="avg_all")
    request, kwargs = aggregation_query._prep_stream()

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": None,
    }
    assert request == expected_request
    assert kwargs == {"retry": None}


def test_async_aggregation_query_prep_stream_with_transaction():
    client = make_async_client()
    transaction = client.transaction()
    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id

    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)
    aggregation_query.count(alias="all")
    aggregation_query.sum("someref", alias="sum_all")
    aggregation_query.avg("someref", alias="avg_all")

    request, kwargs = aggregation_query._prep_stream(transaction=transaction)

    parent_path, _ = parent._parent_info()
    expected_request = {
        "parent": parent_path,
        "structured_aggregation_query": aggregation_query._to_protobuf(),
        "transaction": txn_id,
    }
    assert request == expected_request
    assert kwargs == {"retry": None}


@pytest.mark.asyncio
async def _async_aggregation_query_get_helper(retry=None, timeout=None, read_time=None):
    from google.cloud._helpers import _datetime_to_pb_timestamp

    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = AsyncMock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_async_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)
    aggregation_query.count(alias="all")

    aggregation_result = AggregationResult(alias="total", value=5, read_time=read_time)
    response_pb = make_aggregation_query_response(
        [aggregation_result], read_time=read_time
    )
    firestore_api.run_aggregation_query.return_value = AsyncIter([response_pb])
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    returned = await aggregation_query.get(**kwargs)
    assert isinstance(returned, list)
    assert len(returned) == 1

    for result in returned:
        for r in result:
            assert r.alias == aggregation_result.alias
            assert r.value == aggregation_result.value
            if read_time is not None:
                result_datetime = _datetime_to_pb_timestamp(r.read_time)
                assert result_datetime == read_time

    # Verify the mock call.
    parent_path, _ = parent._parent_info()
    firestore_api.run_aggregation_query.assert_called_once_with(
        request={
            "parent": parent_path,
            "structured_aggregation_query": aggregation_query._to_protobuf(),
            "transaction": None,
        },
        metadata=client._rpc_metadata,
        **kwargs,
    )


@pytest.mark.asyncio
async def test_async_aggregation_query_get():
    await _async_aggregation_query_get_helper()


@pytest.mark.asyncio
async def test_async_aggregation_query_get_with_readtime():
    from google.cloud._helpers import _datetime_to_pb_timestamp

    one_hour_ago = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    read_time = _datetime_to_pb_timestamp(one_hour_ago)
    await _async_aggregation_query_get_helper(read_time=read_time)


@pytest.mark.asyncio
async def test_async_aggregation_query_get_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    await _async_aggregation_query_get_helper(retry=retry, timeout=timeout)


@pytest.mark.asyncio
async def test_async_aggregation_query_get_transaction():
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = AsyncMock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_async_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")

    transaction = client.transaction()

    txn_id = b"\x00\x00\x01-work-\xf2"
    transaction._id = txn_id
    query = make_async_query(parent)
    aggregation_query = make_async_aggregation_query(query)
    aggregation_query.count(alias="all")

    aggregation_result = AggregationResult(alias="total", value=5)
    response_pb = make_aggregation_query_response(
        [aggregation_result], transaction=txn_id
    )
    firestore_api.run_aggregation_query.return_value = AsyncIter([response_pb])
    retry = None
    timeout = None
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    # Execute the query and check the response.
    returned = await aggregation_query.get(transaction=transaction, **kwargs)
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


@pytest.mark.asyncio
async def test_async_aggregation_from_query():
    from google.cloud.firestore_v1 import _helpers

    # Create a minimal fake GAPIC.
    firestore_api = AsyncMock(spec=["run_aggregation_query"])

    # Attach the fake GAPIC to a real client.
    client = make_async_client()
    client._firestore_api_internal = firestore_api

    # Make a **real** collection reference as parent.
    parent = client.collection("dee")
    query = make_async_query(parent)

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

    # Execute each aggregation query type and check the response.
    for aggregation_query in [
        query.count(alias="total"),
        query.sum("foo", alias="total"),
        query.avg("foo", alias="total"),
    ]:
        # reset api mock
        firestore_api.run_aggregation_query.reset_mock()
        firestore_api.run_aggregation_query.return_value = AsyncIter([response_pb])
        # run query
        returned = await aggregation_query.get(transaction=transaction, **kwargs)
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
