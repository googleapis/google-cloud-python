# Copyright 2014 Google Inc. All rights reserved.
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

import unittest2


class TestQuery(unittest2.TestCase):

    _DATASET = 'DATASET'

    def _getTargetClass(self):
        from gcloud.datastore.query import Query
        return Query

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeClient(self, connection=None):
        if connection is None:
            connection = _Connection()
        return _Client(self._DATASET, connection)

    def test_ctor_defaults(self):
        client = self._makeClient()
        query = self._makeOne(client)
        self.assertTrue(query._client is client)
        self.assertEqual(query.dataset_id, client.dataset_id)
        self.assertEqual(query.kind, None)
        self.assertEqual(query.namespace, client.namespace)
        self.assertEqual(query.ancestor, None)
        self.assertEqual(query.filters, [])
        self.assertEqual(query.projection, [])
        self.assertEqual(query.order, [])
        self.assertEqual(query.group_by, [])

    def test_ctor_explicit(self):
        from gcloud.datastore.key import Key
        _DATASET = 'OTHER_DATASET'
        _KIND = 'KIND'
        _NAMESPACE = 'OTHER_NAMESPACE'
        client = self._makeClient()
        ancestor = Key('ANCESTOR', 123, dataset_id=_DATASET)
        FILTERS = [('foo', '=', 'Qux'), ('bar', '<', 17)]
        PROJECTION = ['foo', 'bar', 'baz']
        ORDER = ['foo', 'bar']
        GROUP_BY = ['foo']
        query = self._makeOne(
            client,
            kind=_KIND,
            dataset_id=_DATASET,
            namespace=_NAMESPACE,
            ancestor=ancestor,
            filters=FILTERS,
            projection=PROJECTION,
            order=ORDER,
            group_by=GROUP_BY,
            )
        self.assertTrue(query._client is client)
        self.assertEqual(query.dataset_id, _DATASET)
        self.assertEqual(query.kind, _KIND)
        self.assertEqual(query.namespace, _NAMESPACE)
        self.assertEqual(query.ancestor.path, ancestor.path)
        self.assertEqual(query.filters, FILTERS)
        self.assertEqual(query.projection, PROJECTION)
        self.assertEqual(query.order, ORDER)
        self.assertEqual(query.group_by, GROUP_BY)

    def test_ctor_bad_projection(self):
        BAD_PROJECTION = object()
        self.assertRaises(TypeError, self._makeOne, self._makeClient(),
                          projection=BAD_PROJECTION)

    def test_ctor_bad_order(self):
        BAD_ORDER = object()
        self.assertRaises(TypeError, self._makeOne, self._makeClient(),
                          order=BAD_ORDER)

    def test_ctor_bad_group_by(self):
        BAD_GROUP_BY = object()
        self.assertRaises(TypeError, self._makeOne, self._makeClient(),
                          group_by=BAD_GROUP_BY)

    def test_ctor_bad_filters(self):
        FILTERS_CANT_UNPACK = [('one', 'two')]
        self.assertRaises(ValueError, self._makeOne, self._makeClient(),
                          filters=FILTERS_CANT_UNPACK)

    def test_namespace_setter_w_non_string(self):
        query = self._makeOne(self._makeClient())

        def _assign(val):
            query.namespace = val

        self.assertRaises(ValueError, _assign, object())

    def test_namespace_setter(self):
        _NAMESPACE = 'OTHER_NAMESPACE'
        query = self._makeOne(self._makeClient())
        query.namespace = _NAMESPACE
        self.assertEqual(query.namespace, _NAMESPACE)

    def test_kind_setter_w_non_string(self):
        query = self._makeOne(self._makeClient())

        def _assign(val):
            query.kind = val

        self.assertRaises(TypeError, _assign, object())

    def test_kind_setter_wo_existing(self):
        _KIND = 'KIND'
        query = self._makeOne(self._makeClient())
        query.kind = _KIND
        self.assertEqual(query.kind, _KIND)

    def test_kind_setter_w_existing(self):
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        query = self._makeOne(self._makeClient(), kind=_KIND_BEFORE)
        self.assertEqual(query.kind, _KIND_BEFORE)
        query.kind = _KIND_AFTER
        self.assertEqual(query.dataset_id, self._DATASET)
        self.assertEqual(query.kind, _KIND_AFTER)

    def test_ancestor_setter_w_non_key(self):
        query = self._makeOne(self._makeClient())

        def _assign(val):
            query.ancestor = val

        self.assertRaises(TypeError, _assign, object())
        self.assertRaises(TypeError, _assign, ['KIND', 'NAME'])

    def test_ancestor_setter_w_key(self):
        from gcloud.datastore.key import Key
        _NAME = u'NAME'
        key = Key('KIND', 123, dataset_id=self._DATASET)
        query = self._makeOne(self._makeClient())
        query.add_filter('name', '=', _NAME)
        query.ancestor = key
        self.assertEqual(query.ancestor.path, key.path)

    def test_ancestor_deleter_w_key(self):
        from gcloud.datastore.key import Key
        key = Key('KIND', 123, dataset_id=self._DATASET)
        query = self._makeOne(client=self._makeClient(), ancestor=key)
        del query.ancestor
        self.assertTrue(query.ancestor is None)

    def test_add_filter_setter_w_unknown_operator(self):
        query = self._makeOne(self._makeClient())
        self.assertRaises(ValueError, query.add_filter,
                          'firstname', '~~', 'John')

    def test_add_filter_w_known_operator(self):
        query = self._makeOne(self._makeClient())
        query.add_filter('firstname', '=', u'John')
        self.assertEqual(query.filters, [('firstname', '=', u'John')])

    def test_add_filter_w_all_operators(self):
        query = self._makeOne(self._makeClient())
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
        from gcloud.datastore.entity import Entity
        query = self._makeOne(self._makeClient())
        other = Entity()
        other['firstname'] = u'John'
        other['lastname'] = u'Smith'
        query.add_filter('other', '=', other)
        self.assertEqual(query.filters, [('other', '=', other)])

    def test_add_filter_w_whitespace_property_name(self):
        query = self._makeOne(self._makeClient())
        PROPERTY_NAME = '  property with lots of space '
        query.add_filter(PROPERTY_NAME, '=', u'John')
        self.assertEqual(query.filters, [(PROPERTY_NAME, '=', u'John')])

    def test_add_filter___key__valid_key(self):
        from gcloud.datastore.key import Key
        query = self._makeOne(self._makeClient())
        key = Key('Foo', dataset_id=self._DATASET)
        query.add_filter('__key__', '=', key)
        self.assertEqual(query.filters, [('__key__', '=', key)])

    def test_filter___key__not_equal_operator(self):
        from gcloud.datastore.key import Key
        key = Key('Foo', dataset_id=self._DATASET)
        query = self._makeOne(self._makeClient())
        query.add_filter('__key__', '<', key)
        self.assertEqual(query.filters, [('__key__', '<', key)])

    def test_filter___key__invalid_value(self):
        query = self._makeOne(self._makeClient())
        self.assertRaises(ValueError, query.add_filter, '__key__', '=', None)

    def test_projection_setter_empty(self):
        query = self._makeOne(self._makeClient())
        query.projection = []
        self.assertEqual(query.projection, [])

    def test_projection_setter_string(self):
        query = self._makeOne(self._makeClient())
        query.projection = 'field1'
        self.assertEqual(query.projection, ['field1'])

    def test_projection_setter_non_empty(self):
        query = self._makeOne(self._makeClient())
        query.projection = ['field1', 'field2']
        self.assertEqual(query.projection, ['field1', 'field2'])

    def test_projection_setter_multiple_calls(self):
        _PROJECTION1 = ['field1', 'field2']
        _PROJECTION2 = ['field3']
        query = self._makeOne(self._makeClient())
        query.projection = _PROJECTION1
        self.assertEqual(query.projection, _PROJECTION1)
        query.projection = _PROJECTION2
        self.assertEqual(query.projection, _PROJECTION2)

    def test_keys_only(self):
        query = self._makeOne(self._makeClient())
        query.keys_only()
        self.assertEqual(query.projection, ['__key__'])

    def test_order_setter_empty(self):
        query = self._makeOne(self._makeClient(), order=['foo', '-bar'])
        query.order = []
        self.assertEqual(query.order, [])

    def test_order_setter_string(self):
        query = self._makeOne(self._makeClient())
        query.order = 'field'
        self.assertEqual(query.order, ['field'])

    def test_order_setter_single_item_list_desc(self):
        query = self._makeOne(self._makeClient())
        query.order = ['-field']
        self.assertEqual(query.order, ['-field'])

    def test_order_setter_multiple(self):
        query = self._makeOne(self._makeClient())
        query.order = ['foo', '-bar']
        self.assertEqual(query.order, ['foo', '-bar'])

    def test_group_by_setter_empty(self):
        query = self._makeOne(self._makeClient(), group_by=['foo', 'bar'])
        query.group_by = []
        self.assertEqual(query.group_by, [])

    def test_group_by_setter_string(self):
        query = self._makeOne(self._makeClient())
        query.group_by = 'field1'
        self.assertEqual(query.group_by, ['field1'])

    def test_group_by_setter_non_empty(self):
        query = self._makeOne(self._makeClient())
        query.group_by = ['field1', 'field2']
        self.assertEqual(query.group_by, ['field1', 'field2'])

    def test_group_by_multiple_calls(self):
        _GROUP_BY1 = ['field1', 'field2']
        _GROUP_BY2 = ['field3']
        query = self._makeOne(self._makeClient())
        query.group_by = _GROUP_BY1
        self.assertEqual(query.group_by, _GROUP_BY1)
        query.group_by = _GROUP_BY2
        self.assertEqual(query.group_by, _GROUP_BY2)

    def test_fetch_defaults_w_client_attr(self):
        connection = _Connection()
        client = self._makeClient(connection)
        query = self._makeOne(client)
        iterator = query.fetch()
        self.assertTrue(iterator._query is query)
        self.assertTrue(iterator._client is client)
        self.assertEqual(iterator._limit, None)
        self.assertEqual(iterator._offset, 0)

    def test_fetch_w_explicit_client(self):
        connection = _Connection()
        client = self._makeClient(connection)
        other_client = self._makeClient(connection)
        query = self._makeOne(client)
        iterator = query.fetch(limit=7, offset=8, client=other_client)
        self.assertTrue(iterator._query is query)
        self.assertTrue(iterator._client is other_client)
        self.assertEqual(iterator._limit, 7)
        self.assertEqual(iterator._offset, 8)


class TestIterator(unittest2.TestCase):
    _DATASET = 'DATASET'
    _NAMESPACE = 'NAMESPACE'
    _KIND = 'KIND'
    _ID = 123
    _START = b'\x00'
    _END = b'\xFF'

    def _getTargetClass(self):
        from gcloud.datastore.query import Iterator
        return Iterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _addQueryResults(self, connection, cursor=_END, more=False):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        MORE = datastore_pb.QueryResultBatch.NOT_FINISHED
        NO_MORE = datastore_pb.QueryResultBatch.MORE_RESULTS_AFTER_LIMIT
        _ID = 123
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = self._DATASET
        path_element = entity_pb.key.path_element.add()
        path_element.kind = self._KIND
        path_element.id = _ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = u'Foo'
        connection._results.append(
            ([entity_pb], cursor, MORE if more else NO_MORE))

    def _makeClient(self, connection=None):
        if connection is None:
            connection = _Connection()
        return _Client(self._DATASET, connection)

    def test_ctor_defaults(self):
        connection = _Connection()
        query = object()
        iterator = self._makeOne(query, connection)
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, None)
        self.assertEqual(iterator._offset, 0)

    def test_ctor_explicit(self):
        client = self._makeClient()
        query = _Query(client)
        iterator = self._makeOne(query, client, 13, 29)
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, 13)
        self.assertEqual(iterator._offset, 29)

    def test_next_page_no_cursors_no_more(self):
        from gcloud.datastore.query import _pb_from_query
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection, cursor=b'')
        iterator = self._makeOne(query, client)
        entities, more_results, cursor = iterator.next_page()

        self.assertEqual(cursor, None)
        self.assertFalse(more_results)
        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key.path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.offset = 0
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test_next_page_no_cursors_no_more_w_offset_and_limit(self):
        from gcloud.datastore.query import _pb_from_query
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection, cursor=b'')
        iterator = self._makeOne(query, client, 13, 29)
        entities, more_results, cursor = iterator.next_page()

        self.assertEqual(cursor, None)
        self.assertFalse(more_results)
        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key.path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.limit = 13
        qpb.offset = 29
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test_next_page_w_cursors_w_more(self):
        from base64 import b64decode
        from base64 import b64encode
        from gcloud.datastore.query import _pb_from_query
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection, cursor=self._END, more=True)
        iterator = self._makeOne(query, client)
        iterator._start_cursor = self._START
        iterator._end_cursor = self._END
        entities, more_results, cursor = iterator.next_page()

        self.assertEqual(cursor, b64encode(self._END))
        self.assertTrue(more_results)
        self.assertTrue(iterator._more_results)
        self.assertEqual(iterator._end_cursor, None)
        self.assertEqual(b64decode(iterator._start_cursor), self._END)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key.path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.offset = 0
        qpb.start_cursor = b64decode(self._START)
        qpb.end_cursor = b64decode(self._END)
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test_next_page_w_cursors_w_bogus_more(self):
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection, cursor=self._END, more=True)
        epb, cursor, _ = connection._results.pop()
        connection._results.append((epb, cursor, 4))  # invalid enum
        iterator = self._makeOne(query, client)
        self.assertRaises(ValueError, iterator.next_page)

    def test___iter___no_more(self):
        from gcloud.datastore.query import _pb_from_query
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection)
        iterator = self._makeOne(query, client)
        entities = list(iterator)

        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key.path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.offset = 0
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test___iter___w_more(self):
        from gcloud.datastore.query import _pb_from_query
        connection = _Connection()
        client = self._makeClient(connection)
        query = _Query(client, self._KIND, self._DATASET, self._NAMESPACE)
        self._addQueryResults(connection, cursor=self._END, more=True)
        self._addQueryResults(connection)
        iterator = self._makeOne(query, client)
        entities = list(iterator)

        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 2)
        for entity in entities:
            self.assertEqual(
                entity.key.path,
                [{'kind': self._KIND, 'id': self._ID}])
            self.assertEqual(entities[1]['foo'], u'Foo')
        qpb1 = _pb_from_query(query)
        qpb1.offset = 0
        qpb2 = _pb_from_query(query)
        qpb2.offset = 0
        qpb2.start_cursor = self._END
        EXPECTED1 = {
            'dataset_id': self._DATASET,
            'query_pb': qpb1,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        EXPECTED2 = {
            'dataset_id': self._DATASET,
            'query_pb': qpb2,
            'namespace': self._NAMESPACE,
            'transaction_id': None,
        }
        self.assertEqual(len(connection._called_with), 2)
        self.assertEqual(connection._called_with[0], EXPECTED1)
        self.assertEqual(connection._called_with[1], EXPECTED2)


class Test__pb_from_query(unittest2.TestCase):

    def _callFUT(self, query):
        from gcloud.datastore.query import _pb_from_query
        return _pb_from_query(query)

    def test_empty(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        pb = self._callFUT(_Query())
        self.assertEqual(list(pb.projection), [])
        self.assertEqual(list(pb.kind), [])
        self.assertEqual(list(pb.order), [])
        self.assertEqual(list(pb.group_by), [])
        self.assertEqual(pb.filter.property_filter.property.name, '')
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.operator, datastore_pb.CompositeFilter.AND)
        self.assertEqual(list(cfilter.filter), [])
        self.assertEqual(pb.start_cursor, b'')
        self.assertEqual(pb.end_cursor, b'')
        self.assertEqual(pb.limit, 0)
        self.assertEqual(pb.offset, 0)

    def test_projection(self):
        pb = self._callFUT(_Query(projection=['a', 'b', 'c']))
        self.assertEqual([item.property.name for item in pb.projection],
                         ['a', 'b', 'c'])

    def test_kind(self):
        pb = self._callFUT(_Query(kind='KIND'))
        self.assertEqual([item.name for item in pb.kind], ['KIND'])

    def test_ancestor(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.key import Key
        from gcloud.datastore.helpers import _prepare_key_for_request
        ancestor = Key('Ancestor', 123, dataset_id='DATASET')
        pb = self._callFUT(_Query(ancestor=ancestor))
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.operator, datastore_pb.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filter), 1)
        pfilter = cfilter.filter[0].property_filter
        self.assertEqual(pfilter.property.name, '__key__')
        ancestor_pb = _prepare_key_for_request(ancestor.to_protobuf())
        self.assertEqual(pfilter.value.key_value, ancestor_pb)

    def test_filter(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        query = _Query(filters=[('name', '=', u'John')])
        query.OPERATORS = {
            '=': datastore_pb.PropertyFilter.EQUAL,
        }
        pb = self._callFUT(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.operator, datastore_pb.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filter), 1)
        pfilter = cfilter.filter[0].property_filter
        self.assertEqual(pfilter.property.name, 'name')
        self.assertEqual(pfilter.value.string_value, u'John')

    def test_filter_key(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.key import Key
        from gcloud.datastore.helpers import _prepare_key_for_request
        key = Key('Kind', 123, dataset_id='DATASET')
        query = _Query(filters=[('__key__', '=', key)])
        query.OPERATORS = {
            '=': datastore_pb.PropertyFilter.EQUAL,
        }
        pb = self._callFUT(query)
        cfilter = pb.filter.composite_filter
        self.assertEqual(cfilter.operator, datastore_pb.CompositeFilter.AND)
        self.assertEqual(len(cfilter.filter), 1)
        pfilter = cfilter.filter[0].property_filter
        self.assertEqual(pfilter.property.name, '__key__')
        key_pb = _prepare_key_for_request(key.to_protobuf())
        self.assertEqual(pfilter.value.key_value, key_pb)

    def test_order(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        pb = self._callFUT(_Query(order=['a', '-b', 'c']))
        self.assertEqual([item.property.name for item in pb.order],
                         ['a', 'b', 'c'])
        self.assertEqual([item.direction for item in pb.order],
                         [datastore_pb.PropertyOrder.ASCENDING,
                          datastore_pb.PropertyOrder.DESCENDING,
                          datastore_pb.PropertyOrder.ASCENDING])

    def test_group_by(self):
        pb = self._callFUT(_Query(group_by=['a', 'b', 'c']))
        self.assertEqual([item.name for item in pb.group_by],
                         ['a', 'b', 'c'])


class _Query(object):

    def __init__(self,
                 client=object(),
                 kind=None,
                 dataset_id=None,
                 namespace=None,
                 ancestor=None,
                 filters=(),
                 projection=(),
                 order=(),
                 group_by=()):
        self._client = client
        self.kind = kind
        self.dataset_id = dataset_id
        self.namespace = namespace
        self.ancestor = ancestor
        self.filters = filters
        self.projection = projection
        self.order = order
        self.group_by = group_by


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

    def __init__(self, dataset_id, connection, namespace=None):
        self.dataset_id = dataset_id
        self.connection = connection
        self.namespace = namespace

    @property
    def current_transaction(self):
        pass
