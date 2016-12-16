# Copyright 2014 Google Inc.
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


class TestQuery(unittest.TestCase):

    _PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.query import Query
        return Query

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _makeClient(self, connection=None):
        if connection is None:
            connection = _Connection()
        return _Client(self._PROJECT, connection)

    def test_ctor_defaults(self):
        client = self._makeClient()
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
        _PROJECT = 'OTHER_PROJECT'
        _KIND = 'KIND'
        _NAMESPACE = 'OTHER_NAMESPACE'
        client = self._makeClient()
        ancestor = Key('ANCESTOR', 123, project=_PROJECT)
        FILTERS = [('foo', '=', 'Qux'), ('bar', '<', 17)]
        PROJECTION = ['foo', 'bar', 'baz']
        ORDER = ['foo', 'bar']
        DISTINCT_ON = ['foo']
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
        self.assertRaises(TypeError, self._make_one, self._makeClient(),
                          projection=BAD_PROJECTION)

    def test_ctor_bad_order(self):
        BAD_ORDER = object()
        self.assertRaises(TypeError, self._make_one, self._makeClient(),
                          order=BAD_ORDER)

    def test_ctor_bad_distinct_on(self):
        BAD_DISTINCT_ON = object()
        self.assertRaises(TypeError, self._make_one, self._makeClient(),
                          distinct_on=BAD_DISTINCT_ON)

    def test_ctor_bad_filters(self):
        FILTERS_CANT_UNPACK = [('one', 'two')]
        self.assertRaises(ValueError, self._make_one, self._makeClient(),
                          filters=FILTERS_CANT_UNPACK)

    def test_namespace_setter_w_non_string(self):
        query = self._make_one(self._makeClient())

        def _assign(val):
            query.namespace = val

        self.assertRaises(ValueError, _assign, object())

    def test_namespace_setter(self):
        _NAMESPACE = 'OTHER_NAMESPACE'
        query = self._make_one(self._makeClient())
        query.namespace = _NAMESPACE
        self.assertEqual(query.namespace, _NAMESPACE)

    def test_kind_setter_w_non_string(self):
        query = self._make_one(self._makeClient())

        def _assign(val):
            query.kind = val

        self.assertRaises(TypeError, _assign, object())

    def test_kind_setter_wo_existing(self):
        _KIND = 'KIND'
        query = self._make_one(self._makeClient())
        query.kind = _KIND
        self.assertEqual(query.kind, _KIND)

    def test_kind_setter_w_existing(self):
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        query = self._make_one(self._makeClient(), kind=_KIND_BEFORE)
        self.assertEqual(query.kind, _KIND_BEFORE)
        query.kind = _KIND_AFTER
        self.assertEqual(query.project, self._PROJECT)
        self.assertEqual(query.kind, _KIND_AFTER)

    def test_ancestor_setter_w_non_key(self):
        query = self._make_one(self._makeClient())

        def _assign(val):
            query.ancestor = val

        self.assertRaises(TypeError, _assign, object())
        self.assertRaises(TypeError, _assign, ['KIND', 'NAME'])

    def test_ancestor_setter_w_key(self):
        from google.cloud.datastore.key import Key
        _NAME = u'NAME'
        key = Key('KIND', 123, project=self._PROJECT)
        query = self._make_one(self._makeClient())
        query.add_filter('name', '=', _NAME)
        query.ancestor = key
        self.assertEqual(query.ancestor.path, key.path)

    def test_ancestor_deleter_w_key(self):
        from google.cloud.datastore.key import Key
        key = Key('KIND', 123, project=self._PROJECT)
        query = self._make_one(client=self._makeClient(), ancestor=key)
        del query.ancestor
        self.assertIsNone(query.ancestor)

    def test_add_filter_setter_w_unknown_operator(self):
        query = self._make_one(self._makeClient())
        self.assertRaises(ValueError, query.add_filter,
                          'firstname', '~~', 'John')

    def test_add_filter_w_known_operator(self):
        query = self._make_one(self._makeClient())
        query.add_filter('firstname', '=', u'John')
        self.assertEqual(query.filters, [('firstname', '=', u'John')])

    def test_add_filter_w_all_operators(self):
        query = self._make_one(self._makeClient())
        query.add_filter('leq_prop', '<=', u'val1')
        query.add_filter('geq_prop', '>=', u'val2')
        query.add_filter('lt_prop', '<', u'val3')
        query.add_filter('gt_prop', '>', u'val4')
        query.add_filter('eq_prop', '=', u'val5')
        self.assertEqual(len(query.filters), 5)
        self.assertEqual(query.filters[0], ('leq_prop', '<=', u'val1'))
        self.assertEqual(query.filters[1], ('geq_prop', '>=', u'val2'))
        self.assertEqual(query.filters[2], ('lt_prop', '<', u'val3'))
        self.assertEqual(query.filters[3], ('gt_prop', '>', u'val4'))
        self.assertEqual(query.filters[4], ('eq_prop', '=', u'val5'))

    def test_add_filter_w_known_operator_and_entity(self):
        from google.cloud.datastore.entity import Entity
        query = self._make_one(self._makeClient())
        other = Entity()
        other['firstname'] = u'John'
        other['lastname'] = u'Smith'
        query.add_filter('other', '=', other)
        self.assertEqual(query.filters, [('other', '=', other)])

    def test_add_filter_w_whitespace_property_name(self):
        query = self._make_one(self._makeClient())
        PROPERTY_NAME = '  property with lots of space '
        query.add_filter(PROPERTY_NAME, '=', u'John')
        self.assertEqual(query.filters, [(PROPERTY_NAME, '=', u'John')])

    def test_add_filter___key__valid_key(self):
        from google.cloud.datastore.key import Key
        query = self._make_one(self._makeClient())
        key = Key('Foo', project=self._PROJECT)
        query.add_filter('__key__', '=', key)
        self.assertEqual(query.filters, [('__key__', '=', key)])

    def test_filter___key__not_equal_operator(self):
        from google.cloud.datastore.key import Key
        key = Key('Foo', project=self._PROJECT)
        query = self._make_one(self._makeClient())
        query.add_filter('__key__', '<', key)
        self.assertEqual(query.filters, [('__key__', '<', key)])

    def test_filter___key__invalid_value(self):
        query = self._make_one(self._makeClient())
        self.assertRaises(ValueError, query.add_filter, '__key__', '=', None)

    def test_projection_setter_empty(self):
        query = self._make_one(self._makeClient())
        query.projection = []
        self.assertEqual(query.projection, [])

    def test_projection_setter_string(self):
        query = self._make_one(self._makeClient())
        query.projection = 'field1'
        self.assertEqual(query.projection, ['field1'])

    def test_projection_setter_non_empty(self):
        query = self._make_one(self._makeClient())
        query.projection = ['field1', 'field2']
        self.assertEqual(query.projection, ['field1', 'field2'])

    def test_projection_setter_multiple_calls(self):
        _PROJECTION1 = ['field1', 'field2']
        _PROJECTION2 = ['field3']
        query = self._make_one(self._makeClient())
        query.projection = _PROJECTION1
        self.assertEqual(query.projection, _PROJECTION1)
        query.projection = _PROJECTION2
        self.assertEqual(query.projection, _PROJECTION2)

    def test_keys_only(self):
        query = self._make_one(self._makeClient())
        query.keys_only()
        self.assertEqual(query.projection, ['__key__'])

    def test_key_filter_defaults(self):
        from google.cloud.datastore.key import Key

        client = self._makeClient()
        query = self._make_one(client)
        self.assertEqual(query.filters, [])
        key = Key('Kind', 1234, project='project')
        query.key_filter(key)
        self.assertEqual(query.filters, [('__key__', '=', key)])

    def test_key_filter_explicit(self):
        from google.cloud.datastore.key import Key

        client = self._makeClient()
        query = self._make_one(client)
        self.assertEqual(query.filters, [])
        key = Key('Kind', 1234, project='project')
        query.key_filter(key, operator='>')
        self.assertEqual(query.filters, [('__key__', '>', key)])

    def test_order_setter_empty(self):
        query = self._make_one(self._makeClient(), order=['foo', '-bar'])
        query.order = []
        self.assertEqual(query.order, [])

    def test_order_setter_string(self):
        query = self._make_one(self._makeClient())
        query.order = 'field'
        self.assertEqual(query.order, ['field'])

    def test_order_setter_single_item_list_desc(self):
        query = self._make_one(self._makeClient())
        query.order = ['-field']
        self.assertEqual(query.order, ['-field'])

    def test_order_setter_multiple(self):
        query = self._make_one(self._makeClient())
        query.order = ['foo', '-bar']
        self.assertEqual(query.order, ['foo', '-bar'])

    def test_distinct_on_setter_empty(self):
        query = self._make_one(self._makeClient(), distinct_on=['foo', 'bar'])
        query.distinct_on = []
        self.assertEqual(query.distinct_on, [])

    def test_distinct_on_setter_string(self):
        query = self._make_one(self._makeClient())
        query.distinct_on = 'field1'
        self.assertEqual(query.distinct_on, ['field1'])

    def test_distinct_on_setter_non_empty(self):
        query = self._make_one(self._makeClient())
        query.distinct_on = ['field1', 'field2']
        self.assertEqual(query.distinct_on, ['field1', 'field2'])

    def test_distinct_on_multiple_calls(self):
        _DISTINCT_ON1 = ['field1', 'field2']
        _DISTINCT_ON2 = ['field3']
        query = self._make_one(self._makeClient())
        query.distinct_on = _DISTINCT_ON1
        self.assertEqual(query.distinct_on, _DISTINCT_ON1)
        query.distinct_on = _DISTINCT_ON2
        self.assertEqual(query.distinct_on, _DISTINCT_ON2)

    def test_fetch_defaults_w_client_attr(self):
        from google.cloud.datastore.query import Iterator

        connection = _Connection()
        client = self._makeClient(connection)
        query = self._make_one(client)
        iterator = query.fetch()

        self.assertIsInstance(iterator, Iterator)
        self.assertIs(iterator._query, query)
        self.assertIs(iterator.client, client)
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator._offset, 0)

    def test_fetch_w_explicit_client(self):
        from google.cloud.datastore.query import Iterator

        connection = _Connection()
        client = self._makeClient(connection)
        other_client = self._makeClient(connection)
        query = self._make_one(client)
        iterator = query.fetch(limit=7, offset=8, client=other_client)
        self.assertIsInstance(iterator, Iterator)
        self.assertIs(iterator._query, query)
        self.assertIs(iterator.client, other_client)
        self.assertEqual(iterator.max_results, 7)
        self.assertEqual(iterator._offset, 8)


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
        self.assertIsNotNone(iterator._item_to_value)
        self.assertIsNone(iterator.max_results)
        self.assertEqual(iterator.page_number, 0)
        self.assertIsNone(iterator.next_page_token,)
        self.assertEqual(iterator.num_results, 0)
        self.assertIs(iterator._query, query)
        self.assertIsNone(iterator._offset)
        self.assertIsNone(iterator._end_cursor)
        self.assertTrue(iterator._more_results)

    def test_constructor_explicit(self):
        query = object()
        client = object()
        limit = 43
        offset = 9
        start_cursor = b'8290\xff'
        end_cursor = b'so20rc\ta'
        iterator = self._make_one(
            query, client, limit=limit, offset=offset,
            start_cursor=start_cursor, end_cursor=end_cursor)

        self.assertFalse(iterator._started)
        self.assertIs(iterator.client, client)
        self.assertIsNotNone(iterator._item_to_value)
        self.assertEqual(iterator.max_results, limit)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, start_cursor)
        self.assertEqual(iterator.num_results, 0)
        self.assertIs(iterator._query, query)
        self.assertEqual(iterator._offset, offset)
        self.assertEqual(iterator._end_cursor, end_cursor)
        self.assertTrue(iterator._more_results)

    def test__build_protobuf_empty(self):
        from google.cloud.grpc.datastore.v1 import query_pb2
        from google.cloud.datastore.query import Query

        client = _Client(None, None)
        query = Query(client)
        iterator = self._make_one(query, client)

        pb = iterator._build_protobuf()
        expected_pb = query_pb2.Query()
        self.assertEqual(pb, expected_pb)

    def test__build_protobuf_all_values(self):
        from google.cloud.grpc.datastore.v1 import query_pb2
        from google.cloud.datastore.query import Query

        client = _Client(None, None)
        query = Query(client)
        limit = 15
        offset = 9
        start_bytes = b'i\xb7\x1d'
        start_cursor = 'abcd'
        end_bytes = b'\xc3\x1c\xb3'
        end_cursor = 'wxyz'
        iterator = self._make_one(
            query, client, limit=limit, offset=offset,
            start_cursor=start_cursor, end_cursor=end_cursor)
        self.assertEqual(iterator.max_results, limit)
        iterator.num_results = 4
        iterator._skipped_results = 1

        pb = iterator._build_protobuf()
        expected_pb = query_pb2.Query(
            start_cursor=start_bytes,
            end_cursor=end_bytes,
            offset=offset - iterator._skipped_results,
        )
        expected_pb.limit.value = limit - iterator.num_results
        self.assertEqual(pb, expected_pb)

    def test__process_query_results(self):
        from google.cloud.grpc.datastore.v1 import query_pb2

        iterator = self._make_one(None, None,
                                  end_cursor='abcd')
        self.assertIsNotNone(iterator._end_cursor)

        entity_pbs = object()
        cursor_as_bytes = b'\x9ai\xe7'
        cursor = b'mmnn'
        skipped_results = 4
        more_results_enum = query_pb2.QueryResultBatch.NOT_FINISHED
        result = iterator._process_query_results(
            entity_pbs, cursor_as_bytes,
            more_results_enum, skipped_results)
        self.assertIs(result, entity_pbs)

        self.assertEqual(iterator._skipped_results, skipped_results)
        self.assertEqual(iterator.next_page_token, cursor)
        self.assertTrue(iterator._more_results)

    def test__process_query_results_done(self):
        from google.cloud.grpc.datastore.v1 import query_pb2

        iterator = self._make_one(None, None,
                                  end_cursor='abcd')
        self.assertIsNotNone(iterator._end_cursor)

        entity_pbs = object()
        cursor_as_bytes = b''
        skipped_results = 44
        more_results_enum = query_pb2.QueryResultBatch.NO_MORE_RESULTS
        result = iterator._process_query_results(
            entity_pbs, cursor_as_bytes,
            more_results_enum, skipped_results)
        self.assertIs(result, entity_pbs)

        self.assertEqual(iterator._skipped_results, skipped_results)
        self.assertIsNone(iterator.next_page_token)
        self.assertFalse(iterator._more_results)

    def test__process_query_results_bad_enum(self):
        iterator = self._make_one(None, None)
        more_results_enum = 999
        with self.assertRaises(ValueError):
            iterator._process_query_results(
                None, b'', more_results_enum, None)

    def test__next_page(self):
        from google.cloud.iterator import Page
        from google.cloud.grpc.datastore.v1 import query_pb2
        from google.cloud.datastore.query import Query

        connection = _Connection()
        more_enum = query_pb2.QueryResultBatch.NOT_FINISHED
        result = ([], b'', more_enum, 0)
        connection._results = [result]
        project = 'prujekt'
        client = _Client(project, connection)
        query = Query(client)
        iterator = self._make_one(query, client)

        page = iterator._next_page()
        self.assertIsInstance(page, Page)
        self.assertIs(page._parent, iterator)

        self.assertEqual(connection._called_with, [{
            'query_pb': query_pb2.Query(),
            'project': project,
            'namespace': None,
            'transaction_id': None,
        }])

    def test__next_page_no_more(self):
        from google.cloud.datastore.query import Query

        connection = _Connection()
        client = _Client(None, connection)
        query = Query(client)
        iterator = self._make_one(query, client)
        iterator._more_results = False

        page = iterator._next_page()
        self.assertIsNone(page)
        self.assertEqual(connection._called_with, [])


class Test__item_to_entity(unittest.TestCase):

    def _call_fut(self, iterator, entity_pb):
        from google.cloud.datastore.query import _item_to_entity
        return _item_to_entity(iterator, entity_pb)

    def test_it(self):
        from google.cloud._testing import _Monkey
        from google.cloud.datastore import helpers

        result = object()
        entities = []

        def mocked(entity_pb):
            entities.append(entity_pb)
            return result

        entity_pb = object()
        with _Monkey(helpers, entity_from_protobuf=mocked):
            self.assertIs(result, self._call_fut(None, entity_pb))

        self.assertEqual(entities, [entity_pb])


class Test__pb_from_query(unittest.TestCase):

    def _call_fut(self, query):
        from google.cloud.datastore.query import _pb_from_query
        return _pb_from_query(query)

    def test_empty(self):
        from google.cloud.grpc.datastore.v1 import query_pb2

        pb = self._call_fut(_Query())
        self.assertEqual(list(pb.projection), [])
        self.assertEqual(list(pb.kind), [])
        self.assertEqual(list(pb.order), [])
        self.assertEqual(list(pb.distinct_on), [])
        self.assertEqual(pb.filter.property_filter.property.name, '')
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op,
                         query_pb2.CompositeFilter.OPERATOR_UNSPECIFIED)
        self.assertEqual(list(cfilter.filters), [])
        self.assertEqual(pb.start_cursor, b'')
        self.assertEqual(pb.end_cursor, b'')
        self.assertEqual(pb.limit.value, 0)
        self.assertEqual(pb.offset, 0)

    def test_projection(self):
        pb = self._call_fut(_Query(projection=['a', 'b', 'c']))
        self.assertEqual([item.property.name for item in pb.projection],
                         ['a', 'b', 'c'])

    def test_kind(self):
        pb = self._call_fut(_Query(kind='KIND'))
        self.assertEqual([item.name for item in pb.kind], ['KIND'])

    def test_ancestor(self):
        from google.cloud.datastore.key import Key
        from google.cloud.grpc.datastore.v1 import query_pb2

        ancestor = Key('Ancestor', 123, project='PROJECT')
        pb = self._call_fut(_Query(ancestor=ancestor))
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, '__key__')
        ancestor_pb = ancestor.to_protobuf()
        self.assertEqual(pfilter.value.key_value, ancestor_pb)

    def test_filter(self):
        from google.cloud.grpc.datastore.v1 import query_pb2

        query = _Query(filters=[('name', '=', u'John')])
        query.OPERATORS = {
            '=': query_pb2.PropertyFilter.EQUAL,
        }
        pb = self._call_fut(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, 'name')
        self.assertEqual(pfilter.value.string_value, u'John')

    def test_filter_key(self):
        from google.cloud.datastore.key import Key
        from google.cloud.grpc.datastore.v1 import query_pb2

        key = Key('Kind', 123, project='PROJECT')
        query = _Query(filters=[('__key__', '=', key)])
        query.OPERATORS = {
            '=': query_pb2.PropertyFilter.EQUAL,
        }
        pb = self._call_fut(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.op, query_pb2.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filters), 1)
        pfilter = cfilter.filters[0].property_filter
        self.assertEqual(pfilter.property.name, '__key__')
        key_pb = key.to_protobuf()
        self.assertEqual(pfilter.value.key_value, key_pb)

    def test_order(self):
        from google.cloud.grpc.datastore.v1 import query_pb2

        pb = self._call_fut(_Query(order=['a', '-b', 'c']))
        self.assertEqual([item.property.name for item in pb.order],
                         ['a', 'b', 'c'])
        self.assertEqual([item.direction for item in pb.order],
                         [query_pb2.PropertyOrder.ASCENDING,
                          query_pb2.PropertyOrder.DESCENDING,
                          query_pb2.PropertyOrder.ASCENDING])

    def test_distinct_on(self):
        pb = self._call_fut(_Query(distinct_on=['a', 'b', 'c']))
        self.assertEqual([item.name for item in pb.distinct_on],
                         ['a', 'b', 'c'])


class _Query(object):

    def __init__(self,
                 client=object(),
                 kind=None,
                 project=None,
                 namespace=None,
                 ancestor=None,
                 filters=(),
                 projection=(),
                 order=(),
                 distinct_on=()):
        self._client = client
        self.kind = kind
        self.project = project
        self.namespace = namespace
        self.ancestor = ancestor
        self.filters = filters
        self.projection = projection
        self.order = order
        self.distinct_on = distinct_on


class _Connection(object):

    _called_with = None
    _cursor = b'\x00'
    _skipped = 0

    def __init__(self):
        self._results = []
        self._called_with = []

    def run_query(self, **kw):
        self._called_with.append(kw)
        result, self._results = self._results[0], self._results[1:]
        return result


class _Client(object):

    def __init__(self, project, connection, namespace=None):
        self.project = project
        self._connection = connection
        self.namespace = namespace

    @property
    def current_transaction(self):
        pass
