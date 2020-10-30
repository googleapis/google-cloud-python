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

import unittest

import mock


class TestQuery(unittest.TestCase):

    _PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.query import Query

        return Query

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_client(self):
        return _Client(self._PROJECT)

    def test_ctor_defaults(self):
        client = self._make_client()
        query = self._make_one(client)
        self.assertIs(query._client, client)
        self.assertEqual(query.project, client.project)
        self.assertIsNone(query.kind)
        self.assertEqual(query.namespace, client.namespace)
        self.assertIsNone(query.ancestor)
        self.assertEqual(query.filters, [])
        self.assertEqual(query.projection, [])
        self.assertEqual(query.order, [])
        self.assertEqual(query.distinct_on, [])

    def test_ctor_explicit(self):
        from google.cloud.datastore.key import Key

        _PROJECT = "OTHER_PROJECT"
        _KIND = "KIND"
        _NAMESPACE = "OTHER_NAMESPACE"
        client = self._make_client()
        ancestor = Key("ANCESTOR", 123, project=_PROJECT)
        FILTERS = [("foo", "=", "Qux"), ("bar", "<", 17)]
        PROJECTION = ["foo", "bar", "baz"]
        ORDER = ["foo", "bar"]
        DISTINCT_ON = ["foo"]
        query = self._make_one(
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
        self.assertIs(query._client, client)
        self.assertEqual(query.project, _PROJECT)
        self.assertEqual(query.kind, _KIND)
        self.assertEqual(query.namespace, _NAMESPACE)
        self.assertEqual(query.ancestor.path, ancestor.path)
        self.assertEqual(query.filters, FILTERS)
        self.assertEqual(query.projection, PROJECTION)
        self.assertEqual(query.order, ORDER)
        self.assertEqual(query.distinct_on, DISTINCT_ON)

    def test_ctor_bad_projection(self):
        BAD_PROJECTION = object()
        self.assertRaises(
            TypeError, self._make_one, self._make_client(), projection=BAD_PROJECTION
        )

    def test_ctor_bad_order(self):
        BAD_ORDER = object()
        self.assertRaises(
            TypeError, self._make_one, self._make_client(), order=BAD_ORDER
        )

    def test_ctor_bad_distinct_on(self):
        BAD_DISTINCT_ON = object()
        self.assertRaises(
            TypeError, self._make_one, self._make_client(), distinct_on=BAD_DISTINCT_ON
        )

    def test_ctor_bad_filters(self):
        FILTERS_CANT_UNPACK = [("one", "two")]
        self.assertRaises(
            ValueError, self._make_one, self._make_client(), filters=FILTERS_CANT_UNPACK
        )

    def test_namespace_setter_w_non_string(self):
        query = self._make_one(self._make_client())

        def _assign(val):
            query.namespace = val

        self.assertRaises(ValueError, _assign, object())

    def test_namespace_setter(self):
        _NAMESPACE = "OTHER_NAMESPACE"
        query = self._make_one(self._make_client())
        query.namespace = _NAMESPACE
        self.assertEqual(query.namespace, _NAMESPACE)

    def test_kind_setter_w_non_string(self):
        query = self._make_one(self._make_client())

        def _assign(val):
            query.kind = val

        self.assertRaises(TypeError, _assign, object())

    def test_kind_setter_wo_existing(self):
        _KIND = "KIND"
        query = self._make_one(self._make_client())
        query.kind = _KIND
        self.assertEqual(query.kind, _KIND)

    def test_kind_setter_w_existing(self):
        _KIND_BEFORE = "KIND_BEFORE"
        _KIND_AFTER = "KIND_AFTER"
        query = self._make_one(self._make_client(), kind=_KIND_BEFORE)
        self.assertEqual(query.kind, _KIND_BEFORE)
        query.kind = _KIND_AFTER
        self.assertEqual(query.project, self._PROJECT)
        self.assertEqual(query.kind, _KIND_AFTER)

    def test_ancestor_setter_w_non_key(self):
        query = self._make_one(self._make_client())

        def _assign(val):
            query.ancestor = val

        self.assertRaises(TypeError, _assign, object())
        self.assertRaises(TypeError, _assign, ["KIND", "NAME"])

    def test_ancestor_setter_w_key(self):
        from google.cloud.datastore.key import Key

        _NAME = "NAME"
        key = Key("KIND", 123, project=self._PROJECT)
        query = self._make_one(self._make_client())
        query.add_filter("name", "=", _NAME)
        query.ancestor = key
        self.assertEqual(query.ancestor.path, key.path)

    def test_ancestor_deleter_w_key(self):
        from google.cloud.datastore.key import Key

        key = Key("KIND", 123, project=self._PROJECT)
        query = self._make_one(client=self._make_client(), ancestor=key)
        del query.ancestor
        self.assertIsNone(query.ancestor)

    def test_add_filter_setter_w_unknown_operator(self):
        query = self._make_one(self._make_client())
        self.assertRaises(ValueError, query.add_filter, "firstname", "~~", "John")

    def test_add_filter_w_known_operator(self):
        query = self._make_one(self._make_client())
        query.add_filter("firstname", "=", "John")
        self.assertEqual(query.filters, [("firstname", "=", "John")])

    def test_add_filter_w_all_operators(self):
        query = self._make_one(self._make_client())
        query.add_filter("leq_prop", "<=", "val1")
        query.add_filter("geq_prop", ">=", "val2")
        query.add_filter("lt_prop", "<", "val3")
        query.add_filter("gt_prop", ">", "val4")
        query.add_filter("eq_prop", "=", "val5")
        self.assertEqual(len(query.filters), 5)
        self.assertEqual(query.filters[0], ("leq_prop", "<=", "val1"))
        self.assertEqual(query.filters[1], ("geq_prop", ">=", "val2"))
        self.assertEqual(query.filters[2], ("lt_prop", "<", "val3"))
        self.assertEqual(query.filters[3], ("gt_prop", ">", "val4"))
        self.assertEqual(query.filters[4], ("eq_prop", "=", "val5"))

    def test_add_filter_w_known_operator_and_entity(self):
        from google.cloud.datastore.entity import Entity

        query = self._make_one(self._make_client())
        other = Entity()
        other["firstname"] = "John"
        other["lastname"] = "Smith"
        query.add_filter("other", "=", other)
        self.assertEqual(query.filters, [("other", "=", other)])

    def test_add_filter_w_whitespace_property_name(self):
        query = self._make_one(self._make_client())
        PROPERTY_NAME = "  property with lots of space "
        query.add_filter(PROPERTY_NAME, "=", "John")
        self.assertEqual(query.filters, [(PROPERTY_NAME, "=", "John")])

    def test_add_filter___key__valid_key(self):
        from google.cloud.datastore.key import Key

        query = self._make_one(self._make_client())
        key = Key("Foo", project=self._PROJECT)
        query.add_filter("__key__", "=", key)
        self.assertEqual(query.filters, [("__key__", "=", key)])

    def test_add_filter_return_query_obj(self):
        from google.cloud.datastore.query import Query

        query = self._make_one(self._make_client())
        query_obj = query.add_filter("firstname", "=", "John")
        self.assertIsInstance(query_obj, Query)
        self.assertEqual(query_obj.filters, [("firstname", "=", "John")])

    def test_filter___key__not_equal_operator(self):
        from google.cloud.datastore.key import Key

        key = Key("Foo", project=self._PROJECT)
        query = self._make_one(self._make_client())
        query.add_filter("__key__", "<", key)
        self.assertEqual(query.filters, [("__key__", "<", key)])

    def test_filter___key__invalid_value(self):
        query = self._make_one(self._make_client())
        self.assertRaises(ValueError, query.add_filter, "__key__", "=", None)

    def test_projection_setter_empty(self):
        query = self._make_one(self._make_client())
        query.projection = []
        self.assertEqual(query.projection, [])

    def test_projection_setter_string(self):
        query = self._make_one(self._make_client())
        query.projection = "field1"
        self.assertEqual(query.projection, ["field1"])

    def test_projection_setter_non_empty(self):
        query = self._make_one(self._make_client())
        query.projection = ["field1", "field2"]
        self.assertEqual(query.projection, ["field1", "field2"])

    def test_projection_setter_multiple_calls(self):
        _PROJECTION1 = ["field1", "field2"]
        _PROJECTION2 = ["field3"]
        query = self._make_one(self._make_client())
        query.projection = _PROJECTION1
        self.assertEqual(query.projection, _PROJECTION1)
        query.projection = _PROJECTION2
        self.assertEqual(query.projection, _PROJECTION2)

    def test_keys_only(self):
        query = self._make_one(self._make_client())
        query.keys_only()
        self.assertEqual(query.projection, ["__key__"])

    def test_key_filter_defaults(self):
        from google.cloud.datastore.key import Key

        client = self._make_client()
        query = self._make_one(client)
        self.assertEqual(query.filters, [])
        key = Key("Kind", 1234, project="project")
        query.key_filter(key)
        self.assertEqual(query.filters, [("__key__", "=", key)])

    def test_key_filter_explicit(self):
        from google.cloud.datastore.key import Key

        client = self._make_client()
        query = self._make_one(client)
        self.assertEqual(query.filters, [])
        key = Key("Kind", 1234, project="project")
        query.key_filter(key, operator=">")
        self.assertEqual(query.filters, [("__key__", ">", key)])

    def test_order_setter_empty(self):
        query = self._make_one(self._make_client(), order=["foo", "-bar"])
        query.order = []
        self.assertEqual(query.order, [])

    def test_order_setter_string(self):
        query = self._make_one(self._make_client())
        query.order = "field"
        self.assertEqual(query.order, ["field"])

    def test_order_setter_single_item_list_desc(self):
        query = self._make_one(self._make_client())
        query.order = ["-field"]
        self.assertEqual(query.order, ["-field"])

    def test_order_setter_multiple(self):
        query = self._make_one(self._make_client())
        query.order = ["foo", "-bar"]
        self.assertEqual(query.order, ["foo", "-bar"])

    def test_distinct_on_setter_empty(self):
        query = self._make_one(self._make_client(), distinct_on=["foo", "bar"])
        query.distinct_on = []
        self.assertEqual(query.distinct_on, [])

    def test_distinct_on_setter_string(self):
        query = self._make_one(self._make_client())
        query.distinct_on = "field1"
        self.assertEqual(query.distinct_on, ["field1"])

    def test_distinct_on_setter_non_empty(self):
        query = self._make_one(self._make_client())
        query.distinct_on = ["field1", "field2"]
        self.assertEqual(query.distinct_on, ["field1", "field2"])

    def test_distinct_on_multiple_calls(self):
        _DISTINCT_ON1 = ["field1", "field2"]
        _DISTINCT_ON2 = ["field3"]
        query = self._make_one(self._make_client())
        query.distinct_on = _DISTINCT_ON1
        self.assertEqual(query.distinct_on, _DISTINCT_ON1)
        query.distinct_on = _DISTINCT_ON2
        self.assertEqual(query.distinct_on, _DISTINCT_ON2)

    def test_fetch_defaults_w_client_attr(self):
        from google.cloud.datastore.query import Iterator

        client = self._make_client()
        query = self._make_one(client)

        iterator = query.fetch()

        self.assertIsInstance(iterator, Iterator)
        self.assertIs(iterator._query, query)
        self.assertIs(iterator.client, client)
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator._offset, 0)
        self.assertIsNone(iterator._retry)
        self.assertIsNone(iterator._timeout)

    def test_fetch_w_explicit_client_w_retry_w_timeout(self):
        from google.cloud.datastore.query import Iterator

        client = self._make_client()
        other_client = self._make_client()
        query = self._make_one(client)
        retry = mock.Mock()
        timeout = 100000

        iterator = query.fetch(
            limit=7, offset=8, client=other_client, retry=retry, timeout=timeout
        )

        self.assertIsInstance(iterator, Iterator)
        self.assertIs(iterator._query, query)
        self.assertIs(iterator.client, other_client)
        self.assertEqual(iterator.max_results, 7)
        self.assertEqual(iterator._offset, 8)
        self.assertEqual(iterator._retry, retry)
        self.assertEqual(iterator._timeout, timeout)


class TestIterator(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.query import Iterator

        return Iterator

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        query = object()
        client = object()

        iterator = self._make_one(query, client)

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token)
        self.assertEqual(iterator.num_results, 0)
        self.assertIs(iterator._query, query)
        self.assertIsNone(iterator._offset)
        self.assertIsNone(iterator._end_cursor)
        self.assertTrue(iterator._more_results)
        self.assertIsNone(iterator._retry)
        self.assertIsNone(iterator._timeout)

    def test_constructor_explicit(self):
        query = object()
        client = object()
        limit = 43
        offset = 9
        start_cursor = b"8290\xff"
        end_cursor = b"so20rc\ta"
        retry = mock.Mock()
        timeout = 100000

        iterator = self._make_one(
            query,
            client,
            limit=limit,
            offset=offset,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
            retry=retry,
            timeout=timeout,
        )

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertEqual(iterator.max_results, limit)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, start_cursor)
        self.assertEqual(iterator.num_results, 0)
        self.assertIs(iterator._query, query)
        self.assertEqual(iterator._offset, offset)
        self.assertEqual(iterator._end_cursor, end_cursor)
        self.assertTrue(iterator._more_results)
        self.assertEqual(iterator._retry, retry)
        self.assertEqual(iterator._timeout, timeout)

    def test__build_protobuf_empty(self):
        from google.cloud.datastore_v1.types import query as query_pb2
        from google.cloud.datastore.query import Query

        client = _Client(None)
        query = Query(client)
        iterator = self._make_one(query, client)

        pb = iterator._build_protobuf()
        expected_pb = query_pb2.Query()
        self.assertEqual(pb, expected_pb)

    def test__build_protobuf_all_values_except_offset(self):
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
        iterator = self._make_one(
            query, client, limit=limit, start_cursor=start_cursor, end_cursor=end_cursor
        )
        self.assertEqual(iterator.max_results, limit)
        iterator.num_results = 4
        iterator._skipped_results = 1

        pb = iterator._build_protobuf()
        expected_pb = query_pb2.Query(start_cursor=start_bytes, end_cursor=end_bytes)
        expected_pb._pb.limit.value = limit - iterator.num_results
        self.assertEqual(pb, expected_pb)

    def test__build_protobuf_all_values_except_start_and_end_cursor(self):
        # this test and the previous (all_values_except_start_offset)
        # test mutually exclusive states; the offset is ignored
        # if a start_cursor is supplied
        from google.cloud.datastore_v1.types import query as query_pb2
        from google.cloud.datastore.query import Query

        client = _Client(None)
        query = Query(client)
        limit = 15
        offset = 9
        iterator = self._make_one(query, client, limit=limit, offset=offset)
        self.assertEqual(iterator.max_results, limit)
        iterator.num_results = 4

        pb = iterator._build_protobuf()
        expected_pb = query_pb2.Query(offset=offset - iterator._skipped_results)
        expected_pb._pb.limit.value = limit - iterator.num_results
        self.assertEqual(pb, expected_pb)

    def test__process_query_results(self):
        from google.cloud.datastore_v1.types import query as query_pb2

        iterator = self._make_one(None, None, end_cursor="abcd")
        self.assertIsNotNone(iterator._end_cursor)

        entity_pbs = [_make_entity("Hello", 9998, "PRAHJEKT")]
        cursor_as_bytes = b"\x9ai\xe7"
        cursor = b"mmnn"
        skipped_results = 4
        more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
        response_pb = _make_query_response(
            entity_pbs, cursor_as_bytes, more_results_enum, skipped_results
        )
        result = iterator._process_query_results(response_pb)
        self.assertEqual(result, entity_pbs)

        self.assertEqual(iterator._skipped_results, skipped_results)
        self.assertEqual(iterator.next_page_token, cursor)
        self.assertTrue(iterator._more_results)

    def test__process_query_results_done(self):
        from google.cloud.datastore_v1.types import query as query_pb2

        iterator = self._make_one(None, None, end_cursor="abcd")
        self.assertIsNotNone(iterator._end_cursor)

        entity_pbs = [_make_entity("World", 1234, "PROJECT")]
        cursor_as_bytes = b"\x9ai\xe7"
        skipped_results = 44
        more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS
        response_pb = _make_query_response(
            entity_pbs, cursor_as_bytes, more_results_enum, skipped_results
        )
        result = iterator._process_query_results(response_pb)
        self.assertEqual(result, entity_pbs)

        self.assertEqual(iterator._skipped_results, skipped_results)
        self.assertIsNone(iterator.next_page_token)
        self.assertFalse(iterator._more_results)

    def test__process_query_results_bad_enum(self):
        iterator = self._make_one(None, None)
        more_results_enum = 999
        response_pb = _make_query_response([], b"", more_results_enum, 0)
        with self.assertRaises(ValueError):
            iterator._process_query_results(response_pb)

    def _next_page_helper(self, txn_id=None, retry=None, timeout=None):
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

        iterator = self._make_one(query, client, **kwargs)

        page = iterator._next_page()

        self.assertIsInstance(page, page_iterator.Page)
        self.assertIs(page._parent, iterator)

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

    def test__next_page(self):
        self._next_page_helper()

    def test__next_page_w_retry(self):
        self._next_page_helper(retry=mock.Mock())

    def test__next_page_w_timeout(self):
        self._next_page_helper(timeout=100000)

    def test__next_page_in_transaction(self):
        txn_id = b"1xo1md\xe2\x98\x83"
        self._next_page_helper(txn_id)

    def test__next_page_no_more(self):
        from google.cloud.datastore.query import Query

        ds_api = _make_datastore_api()
        client = _Client(None, datastore_api=ds_api)
        query = Query(client)
        iterator = self._make_one(query, client)
        iterator._more_results = False

        page = iterator._next_page()
        self.assertIsNone(page)
        ds_api.run_query.assert_not_called()


class Test__item_to_entity(unittest.TestCase):
    def _call_fut(self, iterator, entity_pb):
        from google.cloud.datastore.query import _item_to_entity

        return _item_to_entity(iterator, entity_pb)

    def test_it(self):
        entity_pb = mock.Mock()
        entity_pb._pb = mock.sentinel.entity_pb
        patch = mock.patch("google.cloud.datastore.helpers.entity_from_protobuf")
        with patch as entity_from_protobuf:
            result = self._call_fut(None, entity_pb)
            self.assertIs(result, entity_from_protobuf.return_value)

        entity_from_protobuf.assert_called_once_with(entity_pb)


class Test__pb_from_query(unittest.TestCase):
    def _call_fut(self, query):
        from google.cloud.datastore.query import _pb_from_query

        return _pb_from_query(query)

    def test_empty(self):
        from google.cloud.datastore_v1.types import query as query_pb2

        pb = self._call_fut(_Query())
        self.assertEqual(list(pb.projection), [])
        self.assertEqual(list(pb.kind), [])
        self.assertEqual(list(pb.order), [])
        self.assertEqual(list(pb.distinct_on), [])
        self.assertEqual(pb.filter.property_filter.property.name, "")
        cfilter = pb.filter.composite_filter
        self.assertEqual(
            cfilter.op, query_pb2.CompositeFilter.Operator.OPERATOR_UNSPECIFIED
        )
        self.assertEqual(list(cfilter.filters), [])
        self.assertEqual(pb.start_cursor, b"")
        self.assertEqual(pb.end_cursor, b"")
        self.assertEqual(pb._pb.limit.value, 0)
        self.assertEqual(pb.offset, 0)

    def test_projection(self):
        pb = self._call_fut(_Query(projection=["a", "b", "c"]))
        self.assertEqual(
            [item.property.name for item in pb.projection], ["a", "b", "c"]
        )

    def test_kind(self):
        pb = self._call_fut(_Query(kind="KIND"))
        self.assertEqual([item.name for item in pb.kind], ["KIND"])

    def test_ancestor(self):
        from google.cloud.datastore.key import Key
        from google.cloud.datastore_v1.types import query as query_pb2

        ancestor = Key("Ancestor", 123, project="PROJECT")
        pb = self._call_fut(_Query(ancestor=ancestor))
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.Operator.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, "__key__")
        ancestor_pb = ancestor.to_protobuf()
        self.assertEqual(pfilter.value.key_value, ancestor_pb)

    def test_filter(self):
        from google.cloud.datastore_v1.types import query as query_pb2

        query = _Query(filters=[("name", "=", "John")])
        query.OPERATORS = {"=": query_pb2.PropertyFilter.Operator.EQUAL}
        pb = self._call_fut(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.Operator.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, "name")
        self.assertEqual(pfilter.value.string_value, "John")

    def test_filter_key(self):
        from google.cloud.datastore.key import Key
        from google.cloud.datastore_v1.types import query as query_pb2

        key = Key("Kind", 123, project="PROJECT")
        query = _Query(filters=[("__key__", "=", key)])
        query.OPERATORS = {"=": query_pb2.PropertyFilter.Operator.EQUAL}
        pb = self._call_fut(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.Operator.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, "__key__")
        key_pb = key.to_protobuf()
        self.assertEqual(pfilter.value.key_value, key_pb)

    def test_order(self):
        from google.cloud.datastore_v1.types import query as query_pb2

        pb = self._call_fut(_Query(order=["a", "-b", "c"]))
        self.assertEqual([item.property.name for item in pb.order], ["a", "b", "c"])
        self.assertEqual(
            [item.direction for item in pb.order],
            [
                query_pb2.PropertyOrder.Direction.ASCENDING,
                query_pb2.PropertyOrder.Direction.DESCENDING,
                query_pb2.PropertyOrder.Direction.ASCENDING,
            ],
        )

    def test_distinct_on(self):
        pb = self._call_fut(_Query(distinct_on=["a", "b", "c"]))
        self.assertEqual([item.name for item in pb.distinct_on], ["a", "b", "c"])


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


def _make_datastore_api(result=None):
    run_query = mock.Mock(return_value=result, spec=[])
    return mock.Mock(run_query=run_query, spec=["run_query"])
