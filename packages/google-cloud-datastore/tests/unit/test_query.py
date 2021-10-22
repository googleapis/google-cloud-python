# Copyright 2014 Google LLC
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

_PROJECT = "PROJECT"


def test_query_ctor_defaults():
    client = _make_client()
    query = _make_query(client)
    assert query._client is client
    assert query.project == client.project
    assert query.kind is None
    assert query.namespace == client.namespace
    assert query.ancestor is None
    assert query.filters == []
    assert query.projection == []
    assert query.order == []
    assert query.distinct_on == []


def test_query_ctor_explicit():
    from google.cloud.datastore.key import Key

    _PROJECT = "OTHER_PROJECT"
    _KIND = "KIND"
    _NAMESPACE = "OTHER_NAMESPACE"
    client = _make_client()
    ancestor = Key("ANCESTOR", 123, project=_PROJECT)
    FILTERS = [("foo", "=", "Qux"), ("bar", "<", 17)]
    PROJECTION = ["foo", "bar", "baz"]
    ORDER = ["foo", "bar"]
    DISTINCT_ON = ["foo"]
    query = _make_query(
        client,
        kind=_KIND,
        project=_PROJECT,
        namespace=_NAMESPACE,
        ancestor=ancestor,
        filters=FILTERS,
        projection=PROJECTION,
        order=ORDER,
        distinct_on=DISTINCT_ON,
    )
    assert query._client is client
    assert query.project == _PROJECT
    assert query.kind == _KIND
    assert query.namespace == _NAMESPACE
    assert query.ancestor.path == ancestor.path
    assert query.filters == FILTERS
    assert query.projection == PROJECTION
    assert query.order == ORDER
    assert query.distinct_on == DISTINCT_ON


def test_query_ctor_bad_projection():
    BAD_PROJECTION = object()
    with pytest.raises(TypeError):
        _make_query(_make_client(), projection=BAD_PROJECTION)


def test_query_ctor_bad_order():
    BAD_ORDER = object()
    with pytest.raises(TypeError):
        _make_query(_make_client(), order=BAD_ORDER)


def test_query_ctor_bad_distinct_on():
    BAD_DISTINCT_ON = object()
    with pytest.raises(TypeError):
        _make_query(_make_client(), distinct_on=BAD_DISTINCT_ON)


def test_query_ctor_bad_filters():
    FILTERS_CANT_UNPACK = [("one", "two")]
    with pytest.raises(ValueError):
        _make_query(_make_client(), filters=FILTERS_CANT_UNPACK)


def test_query_namespace_setter_w_non_string():
    query = _make_query(_make_client())
    with pytest.raises(ValueError):
        query.namespace = object()


def test_query_namespace_setter():
    _NAMESPACE = "OTHER_NAMESPACE"
    query = _make_query(_make_client())
    query.namespace = _NAMESPACE
    assert query.namespace == _NAMESPACE


def test_query_kind_setter_w_non_string():
    query = _make_query(_make_client())
    with pytest.raises(TypeError):
        query.kind = object()


def test_query_kind_setter_wo_existing():
    _KIND = "KIND"
    query = _make_query(_make_client())
    query.kind = _KIND
    assert query.kind == _KIND


def test_query_kind_setter_w_existing():
    _KIND_BEFORE = "KIND_BEFORE"
    _KIND_AFTER = "KIND_AFTER"
    query = _make_query(_make_client(), kind=_KIND_BEFORE)
    assert query.kind == _KIND_BEFORE
    query.kind = _KIND_AFTER
    assert query.project == _PROJECT
    assert query.kind == _KIND_AFTER


def test_query_ancestor_setter_w_non_key():
    query = _make_query(_make_client())

    with pytest.raises(TypeError):
        query.ancestor = object()

    with pytest.raises(TypeError):
        query.ancestor = ["KIND", "NAME"]


def test_query_ancestor_setter_w_key():
    from google.cloud.datastore.key import Key

    _NAME = "NAME"
    key = Key("KIND", 123, project=_PROJECT)
    query = _make_query(_make_client())
    query.add_filter("name", "=", _NAME)
    query.ancestor = key
    assert query.ancestor.path == key.path


def test_query_ancestor_deleter_w_key():
    from google.cloud.datastore.key import Key

    key = Key("KIND", 123, project=_PROJECT)
    query = _make_query(client=_make_client(), ancestor=key)
    del query.ancestor
    assert query.ancestor is None


def test_query_add_filter_setter_w_unknown_operator():
    query = _make_query(_make_client())
    with pytest.raises(ValueError):
        query.add_filter("firstname", "~~", "John")


def test_query_add_filter_w_known_operator():
    query = _make_query(_make_client())
    query.add_filter("firstname", "=", "John")
    assert query.filters == [("firstname", "=", "John")]


def test_query_add_filter_w_all_operators():
    query = _make_query(_make_client())
    query.add_filter("leq_prop", "<=", "val1")
    query.add_filter("geq_prop", ">=", "val2")
    query.add_filter("lt_prop", "<", "val3")
    query.add_filter("gt_prop", ">", "val4")
    query.add_filter("eq_prop", "=", "val5")
    assert len(query.filters) == 5
    assert query.filters[0] == ("leq_prop", "<=", "val1")
    assert query.filters[1] == ("geq_prop", ">=", "val2")
    assert query.filters[2] == ("lt_prop", "<", "val3")
    assert query.filters[3] == ("gt_prop", ">", "val4")
    assert query.filters[4] == ("eq_prop", "=", "val5")


def test_query_add_filter_w_known_operator_and_entity():
    from google.cloud.datastore.entity import Entity

    query = _make_query(_make_client())
    other = Entity()
    other["firstname"] = "John"
    other["lastname"] = "Smith"
    query.add_filter("other", "=", other)
    assert query.filters == [("other", "=", other)]


def test_query_add_filter_w_whitespace_property_name():
    query = _make_query(_make_client())
    PROPERTY_NAME = "  property with lots of space "
    query.add_filter(PROPERTY_NAME, "=", "John")
    assert query.filters == [(PROPERTY_NAME, "=", "John")]


def test_query_add_filter___key__valid_key():
    from google.cloud.datastore.key import Key

    query = _make_query(_make_client())
    key = Key("Foo", project=_PROJECT)
    query.add_filter("__key__", "=", key)
    assert query.filters == [("__key__", "=", key)]


def test_query_add_filter_return_query_obj():
    from google.cloud.datastore.query import Query

    query = _make_query(_make_client())
    query_obj = query.add_filter("firstname", "=", "John")
    assert isinstance(query_obj, Query)
    assert query_obj.filters == [("firstname", "=", "John")]


def test_query_filter___key__not_equal_operator():
    from google.cloud.datastore.key import Key

    key = Key("Foo", project=_PROJECT)
    query = _make_query(_make_client())
    query.add_filter("__key__", "<", key)
    assert query.filters == [("__key__", "<", key)]


def test_query_filter___key__invalid_value():
    query = _make_query(_make_client())
    with pytest.raises(ValueError):
        query.add_filter("__key__", "=", None)


def test_query_projection_setter_empty():
    query = _make_query(_make_client())
    query.projection = []
    assert query.projection == []


def test_query_projection_setter_string():
    query = _make_query(_make_client())
    query.projection = "field1"
    assert query.projection == ["field1"]


def test_query_projection_setter_non_empty():
    query = _make_query(_make_client())
    query.projection = ["field1", "field2"]
    assert query.projection == ["field1", "field2"]


def test_query_projection_setter_multiple_calls():
    _PROJECTION1 = ["field1", "field2"]
    _PROJECTION2 = ["field3"]
    query = _make_query(_make_client())
    query.projection = _PROJECTION1
    assert query.projection == _PROJECTION1
    query.projection = _PROJECTION2
    assert query.projection == _PROJECTION2


def test_query_keys_only():
    query = _make_query(_make_client())
    query.keys_only()
    assert query.projection == ["__key__"]


def test_query_key_filter_defaults():
    from google.cloud.datastore.key import Key

    client = _make_client()
    query = _make_query(client)
    assert query.filters == []
    key = Key("Kind", 1234, project="project")
    query.key_filter(key)
    assert query.filters == [("__key__", "=", key)]


def test_query_key_filter_explicit():
    from google.cloud.datastore.key import Key

    client = _make_client()
    query = _make_query(client)
    assert query.filters == []
    key = Key("Kind", 1234, project="project")
    query.key_filter(key, operator=">")
    assert query.filters == [("__key__", ">", key)]


def test_query_order_setter_empty():
    query = _make_query(_make_client(), order=["foo", "-bar"])
    query.order = []
    assert query.order == []


def test_query_order_setter_string():
    query = _make_query(_make_client())
    query.order = "field"
    assert query.order == ["field"]


def test_query_order_setter_single_item_list_desc():
    query = _make_query(_make_client())
    query.order = ["-field"]
    assert query.order == ["-field"]


def test_query_order_setter_multiple():
    query = _make_query(_make_client())
    query.order = ["foo", "-bar"]
    assert query.order == ["foo", "-bar"]


def test_query_distinct_on_setter_empty():
    query = _make_query(_make_client(), distinct_on=["foo", "bar"])
    query.distinct_on = []
    assert query.distinct_on == []


def test_query_distinct_on_setter_string():
    query = _make_query(_make_client())
    query.distinct_on = "field1"
    assert query.distinct_on == ["field1"]


def test_query_distinct_on_setter_non_empty():
    query = _make_query(_make_client())
    query.distinct_on = ["field1", "field2"]
    assert query.distinct_on == ["field1", "field2"]


def test_query_distinct_on_multiple_calls():
    _DISTINCT_ON1 = ["field1", "field2"]
    _DISTINCT_ON2 = ["field3"]
    query = _make_query(_make_client())
    query.distinct_on = _DISTINCT_ON1
    assert query.distinct_on == _DISTINCT_ON1
    query.distinct_on = _DISTINCT_ON2
    assert query.distinct_on == _DISTINCT_ON2


def test_query_fetch_defaults_w_client_attr():
    from google.cloud.datastore.query import Iterator

    client = _make_client()
    query = _make_query(client)

    iterator = query.fetch()

    assert isinstance(iterator, Iterator)
    assert iterator._query is query
    assert iterator.client is client
    assert iterator.max_results is None
    assert iterator._offset == 0
    assert iterator._retry is None
    assert iterator._timeout is None


def test_query_fetch_w_explicit_client_w_retry_w_timeout():
    from google.cloud.datastore.query import Iterator

    client = _make_client()
    other_client = _make_client()
    query = _make_query(client)
    retry = mock.Mock()
    timeout = 100000

    iterator = query.fetch(
        limit=7, offset=8, client=other_client, retry=retry, timeout=timeout
    )

    assert isinstance(iterator, Iterator)
    assert iterator._query is query
    assert iterator.client is other_client
    assert iterator.max_results == 7
    assert iterator._offset == 8
    assert iterator._retry == retry
    assert iterator._timeout == timeout


def test_iterator_constructor_defaults():
    query = object()
    client = object()

    iterator = _make_iterator(query, client)

    assert not iterator._started
    assert iterator.client is client
    assert iterator.max_results is None
    assert iterator.page_number == 0
    assert iterator.next_page_token is None
    assert iterator.num_results == 0
    assert iterator._query is query
    assert iterator._offset is None
    assert iterator._end_cursor is None
    assert iterator._more_results
    assert iterator._retry is None
    assert iterator._timeout is None


def test_iterator_constructor_explicit():
    query = object()
    client = object()
    limit = 43
    offset = 9
    start_cursor = b"8290\xff"
    end_cursor = b"so20rc\ta"
    retry = mock.Mock()
    timeout = 100000

    iterator = _make_iterator(
        query,
        client,
        limit=limit,
        offset=offset,
        start_cursor=start_cursor,
        end_cursor=end_cursor,
        retry=retry,
        timeout=timeout,
    )

    assert not iterator._started
    assert iterator.client is client
    assert iterator.max_results == limit
    assert iterator.page_number == 0
    assert iterator.next_page_token == start_cursor
    assert iterator.num_results == 0
    assert iterator._query is query
    assert iterator._offset == offset
    assert iterator._end_cursor == end_cursor
    assert iterator._more_results
    assert iterator._retry == retry
    assert iterator._timeout == timeout


def test_iterator__build_protobuf_empty():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    client = _Client(None)
    query = Query(client)
    iterator = _make_iterator(query, client)

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.Query()
    assert pb == expected_pb


def test_iterator__build_protobuf_all_values_except_offset():
    # this test and the following (all_values_except_start_and_end_cursor)
    # test mutually exclusive states; the offset is ignored
    # if a start_cursor is supplied
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    client = _Client(None)
    query = Query(client)
    limit = 15
    start_bytes = b"i\xb7\x1d"
    start_cursor = "abcd"
    end_bytes = b"\xc3\x1c\xb3"
    end_cursor = "wxyz"
    iterator = _make_iterator(
        query, client, limit=limit, start_cursor=start_cursor, end_cursor=end_cursor
    )
    assert iterator.max_results == limit
    iterator.num_results = 4
    iterator._skipped_results = 1

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.Query(start_cursor=start_bytes, end_cursor=end_bytes)
    expected_pb._pb.limit.value = limit - iterator.num_results
    assert pb == expected_pb


def test_iterator__build_protobuf_all_values_except_start_and_end_cursor():
    # this test and the previous (all_values_except_start_offset)
    # test mutually exclusive states; the offset is ignored
    # if a start_cursor is supplied
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    client = _Client(None)
    query = Query(client)
    limit = 15
    offset = 9
    iterator = _make_iterator(query, client, limit=limit, offset=offset)
    assert iterator.max_results == limit
    iterator.num_results = 4

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.Query(offset=offset - iterator._skipped_results)
    expected_pb._pb.limit.value = limit - iterator.num_results
    assert pb == expected_pb


def test_iterator__process_query_results():
    from google.cloud.datastore_v1.types import query as query_pb2

    iterator = _make_iterator(None, None, end_cursor="abcd")
    assert iterator._end_cursor is not None

    entity_pbs = [_make_entity("Hello", 9998, "PRAHJEKT")]
    cursor_as_bytes = b"\x9ai\xe7"
    cursor = b"mmnn"
    skipped_results = 4
    more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
    response_pb = _make_query_response(
        entity_pbs, cursor_as_bytes, more_results_enum, skipped_results
    )
    result = iterator._process_query_results(response_pb)
    assert result == entity_pbs

    assert iterator._skipped_results == skipped_results
    assert iterator.next_page_token == cursor
    assert iterator._more_results


def test_iterator__process_query_results_done():
    from google.cloud.datastore_v1.types import query as query_pb2

    iterator = _make_iterator(None, None, end_cursor="abcd")
    assert iterator._end_cursor is not None

    entity_pbs = [_make_entity("World", 1234, "PROJECT")]
    cursor_as_bytes = b"\x9ai\xe7"
    skipped_results = 44
    more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS
    response_pb = _make_query_response(
        entity_pbs, cursor_as_bytes, more_results_enum, skipped_results
    )
    result = iterator._process_query_results(response_pb)
    assert result == entity_pbs

    assert iterator._skipped_results == skipped_results
    assert iterator.next_page_token is None
    assert not iterator._more_results


@pytest.mark.filterwarnings("ignore")
def test_iterator__process_query_results_bad_enum():
    iterator = _make_iterator(None, None)
    more_results_enum = 999
    response_pb = _make_query_response([], b"", more_results_enum, 0)
    with pytest.raises(ValueError):
        iterator._process_query_results(response_pb)


def _next_page_helper(txn_id=None, retry=None, timeout=None):
    from google.api_core import page_iterator
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import entity as entity_pb2
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    more_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
    result = _make_query_response([], b"", more_enum, 0)
    project = "prujekt"
    ds_api = _make_datastore_api(result)
    if txn_id is None:
        client = _Client(project, datastore_api=ds_api)
    else:
        transaction = mock.Mock(id=txn_id, spec=["id"])
        client = _Client(project, datastore_api=ds_api, transaction=transaction)

    query = Query(client)
    kwargs = {}

    if retry is not None:
        kwargs["retry"] = retry

    if timeout is not None:
        kwargs["timeout"] = timeout

    iterator = _make_iterator(query, client, **kwargs)

    page = iterator._next_page()

    assert isinstance(page, page_iterator.Page)
    assert page._parent is iterator

    partition_id = entity_pb2.PartitionId(project_id=project)
    if txn_id is None:
        read_options = datastore_pb2.ReadOptions()
    else:
        read_options = datastore_pb2.ReadOptions(transaction=txn_id)
    empty_query = query_pb2.Query()
    ds_api.run_query.assert_called_once_with(
        request={
            "project_id": project,
            "partition_id": partition_id,
            "read_options": read_options,
            "query": empty_query,
        },
        **kwargs,
    )


def test_iterator__next_page():
    _next_page_helper()


def test_iterator__next_page_w_retry():
    _next_page_helper(retry=mock.Mock())


def test_iterator__next_page_w_timeout():
    _next_page_helper(timeout=100000)


def test_iterator__next_page_in_transaction():
    txn_id = b"1xo1md\xe2\x98\x83"
    _next_page_helper(txn_id)


def test_iterator__next_page_no_more():
    from google.cloud.datastore.query import Query

    ds_api = _make_datastore_api()
    client = _Client(None, datastore_api=ds_api)
    query = Query(client)
    iterator = _make_iterator(query, client)
    iterator._more_results = False

    page = iterator._next_page()
    assert page is None
    ds_api.run_query.assert_not_called()


def test_iterator__next_page_w_skipped_lt_offset():
    from google.api_core import page_iterator
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import entity as entity_pb2
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    project = "prujekt"
    skipped_1 = 100
    skipped_cursor_1 = b"DEADBEEF"
    skipped_2 = 50
    skipped_cursor_2 = b"FACEDACE"

    more_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED

    result_1 = _make_query_response([], b"", more_enum, skipped_1)
    result_1.batch.skipped_cursor = skipped_cursor_1
    result_2 = _make_query_response([], b"", more_enum, skipped_2)
    result_2.batch.skipped_cursor = skipped_cursor_2

    ds_api = _make_datastore_api(result_1, result_2)
    client = _Client(project, datastore_api=ds_api)

    query = Query(client)
    offset = 150
    iterator = _make_iterator(query, client, offset=offset)

    page = iterator._next_page()

    assert isinstance(page, page_iterator.Page)
    assert page._parent is iterator

    partition_id = entity_pb2.PartitionId(project_id=project)
    read_options = datastore_pb2.ReadOptions()

    query_1 = query_pb2.Query(offset=offset)
    query_2 = query_pb2.Query(
        start_cursor=skipped_cursor_1, offset=(offset - skipped_1)
    )
    expected_calls = [
        mock.call(
            request={
                "project_id": project,
                "partition_id": partition_id,
                "read_options": read_options,
                "query": query,
            }
        )
        for query in [query_1, query_2]
    ]
    assert ds_api.run_query.call_args_list == expected_calls


def test__item_to_entity():
    from google.cloud.datastore.query import _item_to_entity

    entity_pb = mock.Mock()
    entity_pb._pb = mock.sentinel.entity_pb
    patch = mock.patch("google.cloud.datastore.helpers.entity_from_protobuf")
    with patch as entity_from_protobuf:
        result = _item_to_entity(None, entity_pb)
        assert result is entity_from_protobuf.return_value

    entity_from_protobuf.assert_called_once_with(entity_pb)


def test_pb_from_query_empty():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import _pb_from_query

    pb = _pb_from_query(_Query())
    assert list(pb.projection) == []
    assert list(pb.kind) == []
    assert list(pb.order) == []
    assert list(pb.distinct_on) == []
    assert pb.filter.property_filter.property.name == ""
    cfilter = pb.filter.composite_filter
    assert cfilter.op == query_pb2.CompositeFilter.Operator.OPERATOR_UNSPECIFIED
    assert list(cfilter.filters) == []
    assert pb.start_cursor == b""
    assert pb.end_cursor == b""
    assert pb._pb.limit.value == 0
    assert pb.offset == 0


def test_pb_from_query_projection():
    from google.cloud.datastore.query import _pb_from_query

    pb = _pb_from_query(_Query(projection=["a", "b", "c"]))
    assert [item.property.name for item in pb.projection] == ["a", "b", "c"]


def test_pb_from_query_kind():
    from google.cloud.datastore.query import _pb_from_query

    pb = _pb_from_query(_Query(kind="KIND"))
    assert [item.name for item in pb.kind] == ["KIND"]


def test_pb_from_query_ancestor():
    from google.cloud.datastore.key import Key
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import _pb_from_query

    ancestor = Key("Ancestor", 123, project="PROJECT")
    pb = _pb_from_query(_Query(ancestor=ancestor))
    cfilter = pb.filter.composite_filter
    assert cfilter.op == query_pb2.CompositeFilter.Operator.AND
    assert len(cfilter.filters) == 1
    pfilter = cfilter.filters[0].property_filter
    assert pfilter.property.name == "__key__"
    ancestor_pb = ancestor.to_protobuf()
    assert pfilter.value.key_value == ancestor_pb


def test_pb_from_query_filter():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import _pb_from_query

    query = _Query(filters=[("name", "=", "John")])
    query.OPERATORS = {"=": query_pb2.PropertyFilter.Operator.EQUAL}
    pb = _pb_from_query(query)
    cfilter = pb.filter.composite_filter
    assert cfilter.op == query_pb2.CompositeFilter.Operator.AND
    assert len(cfilter.filters) == 1
    pfilter = cfilter.filters[0].property_filter
    assert pfilter.property.name == "name"
    assert pfilter.value.string_value == "John"


def test_pb_from_query_filter_key():
    from google.cloud.datastore.key import Key
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import _pb_from_query

    key = Key("Kind", 123, project="PROJECT")
    query = _Query(filters=[("__key__", "=", key)])
    query.OPERATORS = {"=": query_pb2.PropertyFilter.Operator.EQUAL}
    pb = _pb_from_query(query)
    cfilter = pb.filter.composite_filter
    assert cfilter.op == query_pb2.CompositeFilter.Operator.AND
    assert len(cfilter.filters) == 1
    pfilter = cfilter.filters[0].property_filter
    assert pfilter.property.name == "__key__"
    key_pb = key.to_protobuf()
    assert pfilter.value.key_value == key_pb


def test_pb_from_query_order():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import _pb_from_query

    pb = _pb_from_query(_Query(order=["a", "-b", "c"]))
    assert [item.property.name for item in pb.order] == ["a", "b", "c"]
    expected_directions = [
        query_pb2.PropertyOrder.Direction.ASCENDING,
        query_pb2.PropertyOrder.Direction.DESCENDING,
        query_pb2.PropertyOrder.Direction.ASCENDING,
    ]
    assert [item.direction for item in pb.order] == expected_directions


def test_pb_from_query_distinct_on():
    from google.cloud.datastore.query import _pb_from_query

    pb = _pb_from_query(_Query(distinct_on=["a", "b", "c"]))
    assert [item.name for item in pb.distinct_on] == ["a", "b", "c"]


class _Query(object):
    def __init__(
        self,
        client=object(),
        kind=None,
        project=None,
        namespace=None,
        ancestor=None,
        filters=(),
        projection=(),
        order=(),
        distinct_on=(),
    ):
        self._client = client
        self.kind = kind
        self.project = project
        self.namespace = namespace
        self.ancestor = ancestor
        self.filters = filters
        self.projection = projection
        self.order = order
        self.distinct_on = distinct_on


class _Client(object):
    def __init__(self, project, datastore_api=None, namespace=None, transaction=None):
        self.project = project
        self._datastore_api = datastore_api
        self.namespace = namespace
        self._transaction = transaction

    @property
    def current_transaction(self):
        return self._transaction


def _make_query(*args, **kw):
    from google.cloud.datastore.query import Query

    return Query(*args, **kw)


def _make_iterator(*args, **kw):
    from google.cloud.datastore.query import Iterator

    return Iterator(*args, **kw)


def _make_client():
    return _Client(_PROJECT)


def _make_entity(kind, id_, project):
    from google.cloud.datastore_v1.types import entity as entity_pb2

    key = entity_pb2.Key()
    key.partition_id.project_id = project
    elem = key.path._pb.add()
    elem.kind = kind
    elem.id = id_
    return entity_pb2.Entity(key=key)


def _make_query_response(
    entity_pbs, cursor_as_bytes, more_results_enum, skipped_results
):
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import query as query_pb2

    return datastore_pb2.RunQueryResponse(
        batch=query_pb2.QueryResultBatch(
            skipped_results=skipped_results,
            end_cursor=cursor_as_bytes,
            more_results=more_results_enum,
            entity_results=[
                query_pb2.EntityResult(entity=entity) for entity in entity_pbs
            ],
        )
    )


def _make_datastore_api(*results):
    if len(results) == 0:
        run_query = mock.Mock(return_value=None, spec=[])
    else:
        run_query = mock.Mock(side_effect=results, spec=[])

    return mock.Mock(run_query=run_query, spec=["run_query"])
