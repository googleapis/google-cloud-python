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

import itertools

from unittest import mock

import pytest

from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.datastore_v1.proto import query_pb2

from google.cloud.ndb import _datastore_query
from google.cloud.ndb import key as key_module
from google.cloud.ndb import query as query_module
from google.cloud.ndb import tasklets


def test_make_filter():
    expected = query_pb2.PropertyFilter(
        property=query_pb2.PropertyReference(name="harry"),
        op=query_pb2.PropertyFilter.EQUAL,
        value=entity_pb2.Value(string_value="Harold"),
    )
    assert _datastore_query.make_filter("harry", "=", "Harold") == expected


def test_make_composite_and_filter():
    filters = [
        query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="harry"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="Harold"),
        ),
        query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="josie"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="Josephine"),
        ),
    ]
    expected = query_pb2.CompositeFilter(
        op=query_pb2.CompositeFilter.AND,
        filters=[
            query_pb2.Filter(property_filter=sub_filter)
            for sub_filter in filters
        ],
    )
    assert _datastore_query.make_composite_and_filter(filters) == expected


@pytest.mark.usefixtures("in_context")
class Test_fetch:
    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._Result.entity",
        lambda self, projection: self.result_type + self.result_pb,
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_project_from_query(_query_to_protobuf, _run_query):
        query = mock.Mock(
            project="myapp",
            filters=None,
            order_by=None,
            namespace="zeta",
            projection=None,
            spec=("app", "filters", "namespace", "projection"),
        )
        query_pb = _query_to_protobuf.return_value

        _run_query_future = tasklets.Future()
        _run_query.return_value = _run_query_future

        tasklet = _datastore_query.fetch(query)
        _run_query_future.set_result([("a", "b"), ("c", "d"), ("e", "f")])
        assert tasklet.result() == ["ab", "cd", "ef"]

        _query_to_protobuf.assert_called_once_with(query, None)
        _run_query.assert_called_once_with("myapp", "zeta", query_pb)

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._Result.entity",
        lambda self, projection: self.result_type + self.result_pb,
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_project_from_context(_query_to_protobuf, _run_query):
        query = mock.Mock(
            project=None,
            filters=None,
            order_by=None,
            namespace=None,
            projection=None,
            spec=("app", "filters", "namespace", "projection"),
        )
        query_pb = _query_to_protobuf.return_value

        _run_query_future = tasklets.Future()
        _run_query.return_value = _run_query_future

        tasklet = _datastore_query.fetch(query)
        _run_query_future.set_result([("a", "b"), ("c", "d"), ("e", "f")])
        assert tasklet.result() == ["ab", "cd", "ef"]

        _query_to_protobuf.assert_called_once_with(query, None)
        _run_query.assert_called_once_with("testing", None, query_pb)

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._Result.entity",
        lambda self, projection: self.result_type + self.result_pb,
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_filter(_query_to_protobuf, _run_query):
        filters = mock.Mock(
            _to_filter=mock.Mock(return_value="thefilter"), spec="_to_filter"
        )
        query = mock.Mock(
            project=None,
            filters=filters,
            order_by=None,
            namespace=None,
            projection=None,
            spec=("app", "filters", "namespace", "projection"),
        )
        query_pb = _query_to_protobuf.return_value

        _run_query_future = tasklets.Future()
        _run_query.return_value = _run_query_future

        tasklet = _datastore_query.fetch(query)
        _run_query_future.set_result([("a", "b"), ("c", "d"), ("e", "f")])
        assert tasklet.result() == ["ab", "cd", "ef"]

        _query_to_protobuf.assert_called_once_with(query, "thefilter")
        _run_query.assert_called_once_with("testing", None, query_pb)

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._Result.entity",
        lambda self, projection: self.result_type + self.result_pb,
    )
    @mock.patch(
        "google.cloud.ndb._datastore_query._merge_results",
        lambda result_sets, sortable: itertools.chain(*result_sets),
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_filters(_query_to_protobuf, _run_query):
        filters = mock.Mock(
            _to_filter=mock.Mock(return_value=["filter1", "filter2"]),
            spec="_to_filter",
        )
        query = query_module.QueryOptions(filters=filters)

        _run_query_future1 = tasklets.Future()
        _run_query_future2 = tasklets.Future()
        _run_query.side_effect = [_run_query_future1, _run_query_future2]

        tasklet = _datastore_query.fetch(query)
        _run_query_future1.set_result([("a", "1"), ("b", "2"), ("c", "3")])
        _run_query_future2.set_result([("d", "4"), ("e", "5"), ("f", "6")])
        assert tasklet.result() == ["a1", "b2", "c3", "d4", "e5", "f6"]

        assert _query_to_protobuf.call_count == 2
        assert _run_query.call_count == 2

    @staticmethod
    @mock.patch(
        "google.cloud.ndb._datastore_query._Result.entity",
        lambda self, projection: self.result_type + self.result_pb,
    )
    @mock.patch(
        "google.cloud.ndb._datastore_query._merge_results",
        lambda result_sets, sortable: itertools.chain(*result_sets),
    )
    @mock.patch("google.cloud.ndb._datastore_query._run_query")
    @mock.patch("google.cloud.ndb._datastore_query._query_to_protobuf")
    def test_filters_with_offset_and_limit(_query_to_protobuf, _run_query):
        filters = mock.Mock(
            _to_filter=mock.Mock(return_value=["filter1", "filter2"]),
            spec="_to_filter",
        )
        query = query_module.QueryOptions(filters=filters, offset=2, limit=3)

        _run_query_future1 = tasklets.Future()
        _run_query_future2 = tasklets.Future()
        _run_query.side_effect = [_run_query_future1, _run_query_future2]

        tasklet = _datastore_query.fetch(query)
        _run_query_future1.set_result([("a", "1"), ("b", "2"), ("c", "3")])
        _run_query_future2.set_result([("d", "4"), ("e", "5"), ("f", "6")])
        assert tasklet.result() == ["c3", "d4", "e5"]

        assert query.offset == 2  # Not mutated
        assert query.limit == 3  # Not mutated
        assert _query_to_protobuf.call_count == 2
        assert _run_query.call_count == 2


class Test__merge_results:
    @staticmethod
    def test_unordered():
        def result(name):
            return _datastore_query._Result(
                None,
                query_pb2.EntityResult(
                    entity=entity_pb2.Entity(
                        key=entity_pb2.Key(
                            path=[
                                entity_pb2.Key.PathElement(
                                    kind="thiskind", name=name
                                )
                            ]
                        )
                    )
                ),
            )

        result_sets = [
            (result("a"), result("b"), result("c")),
            (result("b"), result("d")),
        ]
        merged = _datastore_query._merge_results(result_sets, False)
        expected = [result("a"), result("b"), result("c"), result("d")]
        assert list(merged) == expected

    @staticmethod
    def test_ordered():
        def result(name):
            return _datastore_query._Result(
                None,
                query_pb2.EntityResult(
                    entity=entity_pb2.Entity(
                        key=entity_pb2.Key(
                            path=[
                                entity_pb2.Key.PathElement(
                                    kind="thiskind", name=name
                                )
                            ]
                        ),
                        properties={
                            "foo": entity_pb2.Value(string_value=name)
                        },
                    )
                ),
                order_by=[query_module.PropertyOrder("foo")],
            )

        result_sets = [
            (result("a"), result("c")),
            (result("b"), result("c"), result("d")),
        ]
        merged = list(_datastore_query._merge_results(result_sets, True))
        expected = [result("a"), result("b"), result("c"), result("d")]
        assert merged == expected


class Test_Result:
    @staticmethod
    def test_total_ordering():
        def result(foo, bar=0, baz=""):
            return _datastore_query._Result(
                result_type=None,
                result_pb=query_pb2.EntityResult(
                    entity=entity_pb2.Entity(
                        properties={
                            "foo": entity_pb2.Value(string_value=foo),
                            "bar": entity_pb2.Value(integer_value=bar),
                            "baz": entity_pb2.Value(string_value=baz),
                        }
                    )
                ),
                order_by=[
                    query_module.PropertyOrder("foo"),
                    query_module.PropertyOrder("bar", reverse=True),
                ],
            )

        assert result("a") < result("b")
        assert result("b") > result("a")
        assert result("a") != result("b")

        assert result("a", 2) < result("a", 1)
        assert result("a", 1) > result("a", 2)
        assert result("a", 1) != result("a", 2)

        assert result("a", 1, "femur") == result("a", 1, "patella")
        assert result("a") != "a"

    @staticmethod
    def test__compare_no_order_by():
        result = _datastore_query._Result(None, None)
        with pytest.raises(NotImplementedError):
            result._compare("other")

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_entity_unsupported_result_type(model):
        model._entity_from_protobuf.return_value = "bar"
        result = _datastore_query._Result(
            "foo", mock.Mock(entity="foo", spec=("entity",))
        )
        with pytest.raises(NotImplementedError):
            result.entity(None)

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_entity_full_entity(model):
        model._entity_from_protobuf.return_value = "bar"
        result = _datastore_query._Result(
            _datastore_query.RESULT_TYPE_FULL,
            mock.Mock(entity="foo", spec=("entity",)),
        )

        assert result.entity() == "bar"
        model._entity_from_protobuf.assert_called_once_with("foo")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_entity_key_only():
        key_pb = entity_pb2.Key(
            partition_id=entity_pb2.PartitionId(project_id="testing"),
            path=[entity_pb2.Key.PathElement(kind="ThisKind", id=42)],
        )
        result = _datastore_query._Result(
            _datastore_query.RESULT_TYPE_KEY_ONLY,
            mock.Mock(
                entity=mock.Mock(key=key_pb, spec=("key",)), spec=("entity",)
            ),
        )
        assert result.entity() == key_module.Key("ThisKind", 42)

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.model")
    def test_entity_projection(model):
        entity = mock.Mock(spec=("_set_projection",))
        model._entity_from_protobuf.return_value = entity
        result = _datastore_query._Result(
            _datastore_query.RESULT_TYPE_PROJECTION,
            mock.Mock(entity="foo", spec=("entity",)),
        )

        assert result.entity(("a", "b")) is entity
        model._entity_from_protobuf.assert_called_once_with("foo")
        entity._set_projection.assert_called_once_with(("a", "b"))


@pytest.mark.usefixtures("in_context")
class Test__query_to_protobuf:
    @staticmethod
    def test_no_args():
        query = query_module.QueryOptions()
        assert _datastore_query._query_to_protobuf(query) == query_pb2.Query()

    @staticmethod
    def test_kind():
        query = query_module.QueryOptions(kind="Foo")
        assert _datastore_query._query_to_protobuf(query) == query_pb2.Query(
            kind=[query_pb2.KindExpression(name="Foo")]
        )

    @staticmethod
    def test_ancestor():
        key = key_module.Key("Foo", 123)
        query = query_module.QueryOptions(ancestor=key)
        expected_pb = query_pb2.Query(
            filter=query_pb2.Filter(
                property_filter=query_pb2.PropertyFilter(
                    property=query_pb2.PropertyReference(name="__key__"),
                    op=query_pb2.PropertyFilter.HAS_ANCESTOR,
                )
            )
        )
        expected_pb.filter.property_filter.value.key_value.CopyFrom(
            key._key.to_protobuf()
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb

    @staticmethod
    def test_ancestor_with_property_filter():
        key = key_module.Key("Foo", 123)
        query = query_module.QueryOptions(ancestor=key)
        filter_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="foo"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="bar"),
        )
        ancestor_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="__key__"),
            op=query_pb2.PropertyFilter.HAS_ANCESTOR,
        )
        ancestor_pb.value.key_value.CopyFrom(key._key.to_protobuf())
        expected_pb = query_pb2.Query(
            filter=query_pb2.Filter(
                composite_filter=query_pb2.CompositeFilter(
                    op=query_pb2.CompositeFilter.AND,
                    filters=[
                        query_pb2.Filter(property_filter=filter_pb),
                        query_pb2.Filter(property_filter=ancestor_pb),
                    ],
                )
            )
        )
        query_pb = _datastore_query._query_to_protobuf(query, filter_pb)
        assert query_pb == expected_pb

    @staticmethod
    def test_ancestor_with_composite_filter():
        key = key_module.Key("Foo", 123)
        query = query_module.QueryOptions(ancestor=key)
        filter_pb1 = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="foo"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="bar"),
        )
        filter_pb2 = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="food"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="barn"),
        )
        filter_pb = query_pb2.CompositeFilter(
            op=query_pb2.CompositeFilter.AND,
            filters=[
                query_pb2.Filter(property_filter=filter_pb1),
                query_pb2.Filter(property_filter=filter_pb2),
            ],
        )
        ancestor_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="__key__"),
            op=query_pb2.PropertyFilter.HAS_ANCESTOR,
        )
        ancestor_pb.value.key_value.CopyFrom(key._key.to_protobuf())
        expected_pb = query_pb2.Query(
            filter=query_pb2.Filter(
                composite_filter=query_pb2.CompositeFilter(
                    op=query_pb2.CompositeFilter.AND,
                    filters=[
                        query_pb2.Filter(property_filter=filter_pb1),
                        query_pb2.Filter(property_filter=filter_pb2),
                        query_pb2.Filter(property_filter=ancestor_pb),
                    ],
                )
            )
        )
        query_pb = _datastore_query._query_to_protobuf(query, filter_pb)
        assert query_pb == expected_pb

    @staticmethod
    def test_projection():
        query = query_module.QueryOptions(projection=("a", "b"))
        expected_pb = query_pb2.Query(
            projection=[
                query_pb2.Projection(
                    property=query_pb2.PropertyReference(name="a")
                ),
                query_pb2.Projection(
                    property=query_pb2.PropertyReference(name="b")
                ),
            ]
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb

    @staticmethod
    def test_distinct_on():
        query = query_module.QueryOptions(distinct_on=("a", "b"))
        expected_pb = query_pb2.Query(
            distinct_on=[
                query_pb2.PropertyReference(name="a"),
                query_pb2.PropertyReference(name="b"),
            ]
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb

    @staticmethod
    def test_order_by():
        query = query_module.QueryOptions(
            order_by=[
                query_module.PropertyOrder("a"),
                query_module.PropertyOrder("b", reverse=True),
            ]
        )
        expected_pb = query_pb2.Query(
            order=[
                query_pb2.PropertyOrder(
                    property=query_pb2.PropertyReference(name="a"),
                    direction=query_pb2.PropertyOrder.ASCENDING,
                ),
                query_pb2.PropertyOrder(
                    property=query_pb2.PropertyReference(name="b"),
                    direction=query_pb2.PropertyOrder.DESCENDING,
                ),
            ]
        )
        assert _datastore_query._query_to_protobuf(query) == expected_pb

    @staticmethod
    def test_filter_pb():
        filter_pb = query_pb2.PropertyFilter(
            property=query_pb2.PropertyReference(name="foo"),
            op=query_pb2.PropertyFilter.EQUAL,
            value=entity_pb2.Value(string_value="bar"),
        )
        query = query_module.QueryOptions(kind="Foo")
        query_pb = _datastore_query._query_to_protobuf(query, filter_pb)
        expected_pb = query_pb2.Query(
            kind=[query_pb2.KindExpression(name="Foo")],
            filter=query_pb2.Filter(property_filter=filter_pb),
        )
        assert query_pb == expected_pb

    @staticmethod
    def test_offset():
        query = query_module.QueryOptions(offset=20)
        assert _datastore_query._query_to_protobuf(query) == query_pb2.Query(
            offset=20
        )

    @staticmethod
    def test_limit():
        query = query_module.QueryOptions(limit=20)
        expected_pb = query_pb2.Query()
        expected_pb.limit.value = 20
        assert _datastore_query._query_to_protobuf(query) == expected_pb


@pytest.mark.usefixtures("in_context")
class Test__run_query:
    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_query._datastore_api")
    def test_single_batch(_datastore_api, datastore_pb2):
        request = datastore_pb2.RunQueryRequest.return_value
        query_pb = object()

        make_call_future = tasklets.Future("RunQuery")
        _datastore_api.make_call.return_value = make_call_future

        batch = mock.Mock(
            more_results="nope",
            entity_result_type="this type",
            entity_results=["foo", "bar", "baz"],
            spec=("more_results", "entity_result_type", "entity_results"),
        )

        tasklet = _datastore_query._run_query("testing", None, query_pb)
        make_call_future.set_result(mock.Mock(batch=batch, spec=("batch",)))

        assert tasklet.result() == [
            ("this type", "foo"),
            ("this type", "bar"),
            ("this type", "baz"),
        ]

        partition_id = entity_pb2.PartitionId(
            project_id="testing", namespace_id=None
        )
        datastore_pb2.RunQueryRequest.assert_called_once_with(
            project_id="testing", partition_id=partition_id, query=query_pb
        )
        _datastore_api.make_call.assert_called_once_with("RunQuery", request)

    @staticmethod
    @mock.patch("google.cloud.ndb._datastore_query.datastore_pb2")
    @mock.patch("google.cloud.ndb._datastore_query._datastore_api")
    def test_double_batch(_datastore_api, datastore_pb2):
        query_pb = mock.Mock(spec=("start_cursor",))

        make_call_future1 = tasklets.Future("RunQuery")
        make_call_future2 = tasklets.Future("RunQuery")
        _datastore_api.make_call.side_effect = (
            make_call_future1,
            make_call_future2,
        )

        batch1 = mock.Mock(
            more_results=_datastore_query.MORE_RESULTS_TYPE_NOT_FINISHED,
            entity_result_type="this type",
            entity_results=["foo"],
            end_cursor=b"end",
            spec=(
                "more_results",
                "entity_result_type",
                "entity_results",
                "end_cursor",
            ),
        )
        batch2 = mock.Mock(
            more_results="nope",
            entity_result_type="that type",
            entity_results=["bar", "baz"],
            spec=("more_results", "entity_result_type", "entity_results"),
        )

        tasklet = _datastore_query._run_query("testing", None, query_pb)
        make_call_future1.set_result(mock.Mock(batch=batch1, spec=("batch",)))
        make_call_future2.set_result(mock.Mock(batch=batch2, spec=("batch",)))

        assert tasklet.result() == [
            ("this type", "foo"),
            ("that type", "bar"),
            ("that type", "baz"),
        ]

        assert datastore_pb2.RunQueryRequest.call_count == 2
        assert _datastore_api.make_call.call_count == 2
        assert query_pb.start_cursor == b"end"
