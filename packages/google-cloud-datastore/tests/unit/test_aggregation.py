# Copyright 2022 Google LLC
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

import mock
import pytest

from google.cloud.datastore.aggregation import CountAggregation, AggregationQuery

from tests.unit.test_query import _make_query, _make_client

_PROJECT = "PROJECT"


def test_count_aggregation_to_pb():
    from google.cloud.datastore_v1.types import query as query_pb2

    count_aggregation = CountAggregation(alias="total")

    expected_aggregation_query_pb = query_pb2.AggregationQuery.Aggregation()
    expected_aggregation_query_pb.count = query_pb2.AggregationQuery.Aggregation.Count()
    expected_aggregation_query_pb.alias = count_aggregation.alias
    assert count_aggregation._to_pb() == expected_aggregation_query_pb


@pytest.fixture
def client():
    return _make_client()


def test_pb_over_query(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert pb.aggregations == []


def test_pb_over_query_with_count(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.count(alias="total")
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 1
    assert pb.aggregations[0] == CountAggregation(alias="total")._to_pb()


def test_pb_over_query_with_add_aggregation(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.add_aggregation(CountAggregation(alias="total"))
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 1
    assert pb.aggregations[0] == CountAggregation(alias="total")._to_pb()


def test_pb_over_query_with_add_aggregations(client):
    from google.cloud.datastore.query import _pb_from_query

    aggregations = [
        CountAggregation(alias="total"),
        CountAggregation(alias="all"),
    ]

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.add_aggregations(aggregations)
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 2
    assert pb.aggregations[0] == CountAggregation(alias="total")._to_pb()
    assert pb.aggregations[1] == CountAggregation(alias="all")._to_pb()


def test_query_fetch_defaults_w_client_attr(client):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    iterator = aggregation_query.fetch()

    assert isinstance(iterator, AggregationResultIterator)
    assert iterator._aggregation_query is aggregation_query
    assert iterator.client is client
    assert iterator._retry is None
    assert iterator._timeout is None


def test_query_fetch_w_explicit_client_w_retry_w_timeout(client):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    other_client = _make_client()
    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    retry = mock.Mock()
    timeout = 100000

    iterator = aggregation_query.fetch(
        client=other_client, retry=retry, timeout=timeout
    )

    assert isinstance(iterator, AggregationResultIterator)
    assert iterator._aggregation_query is aggregation_query
    assert iterator.client is other_client
    assert iterator._retry == retry
    assert iterator._timeout == timeout


def test_query_fetch_w_explicit_client_w_limit(client):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    other_client = _make_client()
    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    limit = 2

    iterator = aggregation_query.fetch(client=other_client, limit=limit)

    assert isinstance(iterator, AggregationResultIterator)
    assert iterator._aggregation_query is aggregation_query
    assert iterator.client is other_client
    assert iterator._limit == limit


def test_iterator_constructor_defaults():
    query = object()
    client = object()
    aggregation_query = AggregationQuery(client=client, query=query)
    iterator = _make_aggregation_iterator(aggregation_query, client)

    assert not iterator._started
    assert iterator.client is client
    assert iterator.page_number == 0
    assert iterator.num_results == 0
    assert iterator._aggregation_query is aggregation_query
    assert iterator._more_results
    assert iterator._retry is None
    assert iterator._timeout is None


def test_iterator_constructor_explicit():
    query = object()
    client = object()
    aggregation_query = AggregationQuery(client=client, query=query)
    retry = mock.Mock()
    timeout = 100000
    limit = 2

    iterator = _make_aggregation_iterator(
        aggregation_query, client, retry=retry, timeout=timeout, limit=limit
    )

    assert not iterator._started
    assert iterator.client is client
    assert iterator.page_number == 0
    assert iterator.num_results == 0
    assert iterator._aggregation_query is aggregation_query
    assert iterator._more_results
    assert iterator._retry == retry
    assert iterator._timeout == timeout
    assert iterator._limit == limit


def test_iterator__build_protobuf_empty():
    from google.cloud.datastore_v1.types import query as query_pb2

    client = _Client(None)
    query = _make_query(client)
    aggregation_query = AggregationQuery(client=client, query=query)
    iterator = _make_aggregation_iterator(aggregation_query, client)

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.AggregationQuery()
    expected_pb.nested_query = query_pb2.Query()
    assert pb == expected_pb


def test_iterator__build_protobuf_all_values():
    from google.cloud.datastore_v1.types import query as query_pb2

    client = _Client(None)
    query = _make_query(client)
    alias = "total"
    limit = 2
    aggregation_query = AggregationQuery(client=client, query=query)
    aggregation_query.count(alias)

    iterator = _make_aggregation_iterator(aggregation_query, client, limit=limit)
    iterator.num_results = 4

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.AggregationQuery()
    expected_pb.nested_query = query_pb2.Query()
    expected_count_pb = query_pb2.AggregationQuery.Aggregation(alias=alias)
    expected_count_pb.count.up_to = limit
    expected_pb.aggregations.append(expected_count_pb)
    assert pb == expected_pb


def test_iterator__process_query_results():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.aggregation import AggregationResult

    iterator = _make_aggregation_iterator(None, None)

    aggregation_pbs = [AggregationResult(alias="total", value=1)]

    more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
    response_pb = _make_aggregation_query_response(aggregation_pbs, more_results_enum)
    result = iterator._process_query_results(response_pb)
    assert result == [
        r.aggregate_properties for r in response_pb.batch.aggregation_results
    ]
    assert iterator._more_results


def test_iterator__process_query_results_finished_result():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.aggregation import AggregationResult

    iterator = _make_aggregation_iterator(None, None)

    aggregation_pbs = [AggregationResult(alias="total", value=1)]

    more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS
    response_pb = _make_aggregation_query_response(aggregation_pbs, more_results_enum)
    result = iterator._process_query_results(response_pb)
    assert result == [
        r.aggregate_properties for r in response_pb.batch.aggregation_results
    ]
    assert iterator._more_results is False


def test_iterator__process_query_results_unexpected_result():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.aggregation import AggregationResult

    iterator = _make_aggregation_iterator(None, None)

    aggregation_pbs = [AggregationResult(alias="total", value=1)]

    more_results_enum = (
        query_pb2.QueryResultBatch.MoreResultsType.MORE_RESULTS_TYPE_UNSPECIFIED
    )
    response_pb = _make_aggregation_query_response(aggregation_pbs, more_results_enum)
    with pytest.raises(ValueError):
        iterator._process_query_results(response_pb)


def test_aggregation_iterator__next_page():
    _next_page_helper()


def test_iterator__next_page_w_retry():
    retry = mock.Mock()
    _next_page_helper(retry=retry)


def test_iterator__next_page_w_timeout():
    _next_page_helper(timeout=100000)


def test_iterator__next_page_in_transaction():
    txn_id = b"1xo1md\xe2\x98\x83"
    _next_page_helper(txn_id=txn_id)


def test_iterator__next_page_no_more():
    from google.cloud.datastore.query import Query

    ds_api = _make_datastore_api_for_aggregation()
    client = _Client(None, datastore_api=ds_api)
    query = Query(client)

    iterator = _make_aggregation_iterator(query, client)
    iterator._more_results = False
    page = iterator._next_page()
    assert page is None
    ds_api.run_aggregation_query.assert_not_called()


def _next_page_helper(txn_id=None, retry=None, timeout=None):
    from google.api_core import page_iterator
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import entity as entity_pb2
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.aggregation import AggregationResult

    more_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
    aggregation_pbs = [AggregationResult(alias="total", value=1)]

    result_1 = _make_aggregation_query_response([], more_enum)
    result_2 = _make_aggregation_query_response(
        aggregation_pbs, query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS
    )

    project = "prujekt"
    ds_api = _make_datastore_api_for_aggregation(result_1, result_2)
    if txn_id is None:
        client = _Client(project, datastore_api=ds_api)
    else:
        transaction = mock.Mock(id=txn_id, spec=["id"])
        client = _Client(project, datastore_api=ds_api, transaction=transaction)

    query = _make_query(client)
    kwargs = {}

    if retry is not None:
        kwargs["retry"] = retry

    if timeout is not None:
        kwargs["timeout"] = timeout

    it_kwargs = kwargs.copy()  # so it doesn't get overwritten later

    aggregation_query = AggregationQuery(client=client, query=query)

    iterator = _make_aggregation_iterator(aggregation_query, client, **it_kwargs)
    page = iterator._next_page()

    assert isinstance(page, page_iterator.Page)
    assert page._parent is iterator

    partition_id = entity_pb2.PartitionId(project_id=project)
    if txn_id is not None:
        read_options = datastore_pb2.ReadOptions(transaction=txn_id)
    else:
        read_options = datastore_pb2.ReadOptions()

    aggregation_query = AggregationQuery(client=client, query=query)
    assert ds_api.run_aggregation_query.call_count == 2
    expected_call = mock.call(
        request={
            "project_id": project,
            "partition_id": partition_id,
            "read_options": read_options,
            "aggregation_query": aggregation_query._to_pb(),
        },
        **kwargs
    )
    assert ds_api.run_aggregation_query.call_args_list == (
        [expected_call, expected_call]
    )


def test__item_to_aggregation_result():
    from google.cloud.datastore.aggregation import _item_to_aggregation_result
    from google.cloud.datastore.aggregation import AggregationResult

    with mock.patch(
        "proto.marshal.collections.maps.MapComposite"
    ) as map_composite_mock:
        map_composite_mock.keys.return_value = {"total": {"integer_value": 1}}

        result = _item_to_aggregation_result(None, map_composite_mock)

        assert len(result) == 1
        assert type(result[0]) == AggregationResult

        assert result[0].alias == "total"
        assert result[0].value == map_composite_mock.__getitem__().integer_value


class _Client(object):
    def __init__(self, project, datastore_api=None, namespace=None, transaction=None):
        self.project = project
        self._datastore_api = datastore_api
        self.namespace = namespace
        self._transaction = transaction

    @property
    def current_transaction(self):
        return self._transaction


def _make_aggregation_query(*args, **kw):
    from google.cloud.datastore.aggregation import AggregationQuery

    return AggregationQuery(*args, **kw)


def _make_aggregation_iterator(*args, **kw):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    return AggregationResultIterator(*args, **kw)


def _make_aggregation_query_response(aggregation_pbs, more_results_enum):
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import aggregation_result

    aggregation_results = []
    for aggr in aggregation_pbs:
        result = aggregation_result.AggregationResult()
        result.aggregate_properties.alias = aggr.alias
        result.aggregate_properties.value = aggr.value
        aggregation_results.append(result)

    return datastore_pb2.RunAggregationQueryResponse(
        batch=aggregation_result.AggregationResultBatch(
            aggregation_results=aggregation_results,
            more_results=more_results_enum,
        )
    )


def _make_datastore_api_for_aggregation(*results):
    if len(results) == 0:
        run_aggregation_query = mock.Mock(return_value=None, spec=[])
    else:
        run_aggregation_query = mock.Mock(side_effect=results, spec=[])

    return mock.Mock(
        run_aggregation_query=run_aggregation_query, spec=["run_aggregation_query"]
    )
