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

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_dataset = _implicit_environ.DATASET
        _implicit_environ.DATASET = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET = self._replaced_dataset

    def _getTargetClass(self):
        from gcloud.datastore.query import Query
        return Query

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        query = self._getTargetClass()()
        self.assertEqual(query.dataset, None)
        self.assertEqual(query.kind, None)
        self.assertEqual(query.namespace, None)
        self.assertEqual(query.ancestor, None)
        self.assertEqual(query.filters, [])
        self.assertEqual(query.projection, [])
        self.assertEqual(query.order, [])
        self.assertEqual(query.group_by, [])

    def test_ctor_explicit(self):
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAMESPACE = 'NAMESPACE'
        dataset = Dataset(_DATASET)
        ancestor = Key('ANCESTOR', 123, dataset_id=_DATASET)
        FILTERS = [('foo', '=', 'Qux'), ('bar', '<', 17)]
        PROJECTION = ['foo', 'bar', 'baz']
        ORDER = ['foo', 'bar']
        GROUP_BY = ['foo']
        query = self._makeOne(
            kind=_KIND,
            dataset=dataset,
            namespace=_NAMESPACE,
            ancestor=ancestor,
            filters=FILTERS,
            projection=PROJECTION,
            order=ORDER,
            group_by=GROUP_BY,
            )
        self.assertTrue(query.dataset is dataset)
        self.assertEqual(query.kind, _KIND)
        self.assertEqual(query.namespace, _NAMESPACE)
        self.assertEqual(query.ancestor.path, ancestor.path)
        self.assertEqual(query.filters, FILTERS)
        self.assertEqual(query.projection, PROJECTION)
        self.assertEqual(query.order, ORDER)
        self.assertEqual(query.group_by, GROUP_BY)

    def test_dataset_setter_w_non_dataset(self):
        query = self._makeOne()

        def _assign(val):
            query.dataset = val

        self.assertRaises(ValueError, _assign, object())

    def test_dataset_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND)
        query.dataset = dataset
        self.assertTrue(query.dataset is dataset)
        self.assertEqual(query.kind, _KIND)

    def test_namespace_setter_w_non_string(self):
        query = self._makeOne()

        def _assign(val):
            query.namespace = val

        self.assertRaises(ValueError, _assign, object())

    def test_namespace_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        dataset = Dataset(_DATASET)
        query = self._makeOne(dataset=dataset)
        query.namespace = _NAMESPACE
        self.assertTrue(query.dataset is dataset)
        self.assertEqual(query.namespace, _NAMESPACE)

    def test_kind_setter_w_non_string(self):
        query = self._makeOne()

        def _assign(val):
            query.kind = val

        self.assertRaises(TypeError, _assign, object())

    def test_kind_setter_wo_existing(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        dataset = Dataset(_DATASET)
        query = self._makeOne(dataset=dataset)
        query.kind = _KIND
        self.assertTrue(query.dataset is dataset)
        self.assertEqual(query.kind, _KIND)

    def test_kind_setter_w_existing(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND_BEFORE, dataset)
        self.assertEqual(query.kind, _KIND_BEFORE)
        query.kind = _KIND_AFTER
        self.assertTrue(query.dataset is dataset)
        self.assertEqual(query.kind, _KIND_AFTER)

    def test_ancestor_setter_w_non_key(self):
        query = self._makeOne()

        def _assign(val):
            query.ancestor = val

        self.assertRaises(TypeError, _assign, object())
        self.assertRaises(TypeError, _assign, ['KIND', 'NAME'])

    def test_ancestor_setter_w_key(self):
        from gcloud.datastore.key import Key
        _NAME = u'NAME'
        key = Key('KIND', 123, dataset_id='DATASET')
        query = self._makeOne()
        query.add_filter('name', '=', _NAME)
        query.ancestor = key
        self.assertEqual(query.ancestor.path, key.path)

    def test_ancestor_deleter_w_key(self):
        from gcloud.datastore.key import Key
        key = Key('KIND', 123, dataset_id='DATASET')
        query = self._makeOne(ancestor=key)
        del query.ancestor
        self.assertTrue(query.ancestor is None)

    def test_add_filter_setter_w_unknown_operator(self):
        query = self._makeOne()
        self.assertRaises(ValueError, query.add_filter,
                          'firstname', '~~', 'John')

    def test_add_filter_w_known_operator(self):
        query = self._makeOne()
        query.add_filter('firstname', '=', u'John')
        self.assertEqual(query.filters, [('firstname', '=', u'John')])

    def test_add_filter_w_all_operators(self):
        query = self._makeOne()
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
        query = self._makeOne()
        other = Entity()
        other['firstname'] = u'John'
        other['lastname'] = u'Smith'
        query.add_filter('other', '=', other)
        self.assertEqual(query.filters, [('other', '=', other)])

    def test_add_filter_w_whitespace_property_name(self):
        query = self._makeOne()
        PROPERTY_NAME = '  property with lots of space '
        query.add_filter(PROPERTY_NAME, '=', u'John')
        self.assertEqual(query.filters, [(PROPERTY_NAME, '=', u'John')])

    def test_add_filter___key__valid_key(self):
        from gcloud.datastore.key import Key
        query = self._makeOne()
        key = Key('Foo', dataset_id='DATASET')
        query.add_filter('__key__', '=', key)
        self.assertEqual(query.filters, [('__key__', '=', key)])

    def test_filter___key__invalid_operator(self):
        from gcloud.datastore.key import Key
        key = Key('Foo', dataset_id='DATASET')
        query = self._makeOne()
        self.assertRaises(ValueError, query.add_filter, '__key__', '<', key)

    def test_filter___key__invalid_value(self):
        query = self._makeOne()
        self.assertRaises(ValueError, query.add_filter, '__key__', '=', None)

    def test_projection_setter_empty(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.projection = []
        self.assertEqual(query.projection, [])

    def test_projection_setter_string(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.projection = 'field1'
        self.assertEqual(query.projection, ['field1'])

    def test_projection_setter_non_empty(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.projection = ['field1', 'field2']
        self.assertEqual(query.projection, ['field1', 'field2'])

    def test_projection_setter_multiple_calls(self):
        _KIND = 'KIND'
        _PROJECTION1 = ['field1', 'field2']
        _PROJECTION2 = ['field3']
        query = self._makeOne(_KIND)
        query.projection = _PROJECTION1
        self.assertEqual(query.projection, _PROJECTION1)
        query.projection = _PROJECTION2
        self.assertEqual(query.projection, _PROJECTION2)

    def test_keys_only(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.keys_only()
        self.assertEqual(query.projection, ['__key__'])

    def test_order_setter_empty(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND, order=['foo', '-bar'])
        query.order = []
        self.assertEqual(query.order, [])

    def test_order_setter_string(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.order = 'field'
        self.assertEqual(query.order, ['field'])

    def test_order_setter_single_item_list_desc(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.order = ['-field']
        self.assertEqual(query.order, ['-field'])

    def test_order_setter_multiple(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.order = ['foo', '-bar']
        self.assertEqual(query.order, ['foo', '-bar'])

    def test_group_by_setter_empty(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND, group_by=['foo', 'bar'])
        query.group_by = []
        self.assertEqual(query.group_by, [])

    def test_group_by_setter_string(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.group_by = 'field1'
        self.assertEqual(query.group_by, ['field1'])

    def test_group_by_setter_non_empty(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        query.group_by = ['field1', 'field2']
        self.assertEqual(query.group_by, ['field1', 'field2'])

    def test_group_by_multiple_calls(self):
        _KIND = 'KIND'
        _GROUP_BY1 = ['field1', 'field2']
        _GROUP_BY2 = ['field3']
        query = self._makeOne(_KIND)
        query.group_by = _GROUP_BY1
        self.assertEqual(query.group_by, _GROUP_BY1)
        query.group_by = _GROUP_BY2
        self.assertEqual(query.group_by, _GROUP_BY2)

    def test_fetch_defaults(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        iterator = query.fetch()
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, 0)
        self.assertEqual(iterator._offset, 0)

    def test_fetch_explicit(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        iterator = query.fetch(limit=7, offset=8)
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, 7)
        self.assertEqual(iterator._offset, 8)


class Test__pb_from_query(unittest2.TestCase):

    def _callFUT(self, query):
        from gcloud.datastore.query import _pb_from_query
        return _pb_from_query(query)

    def test_empty(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
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
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
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
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
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
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
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
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
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


class TestIterator(unittest2.TestCase):
    _DATASET = 'DATASET'
    _NAMESPACE = 'NAMESPACE'
    _KIND = 'KIND'
    _ID = 123
    _START = b'\x00'
    _END = b'\xFF'

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_dataset = _implicit_environ.DATASET
        _implicit_environ.DATASET = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET = self._replaced_dataset

    def _getTargetClass(self):
        from gcloud.datastore.query import Iterator
        return Iterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeDataset(self):
        connection = _Connection()
        dataset = _Dataset(self._DATASET, connection)
        return dataset, connection

    def _addQueryResults(self, dataset, cursor=_END, more=False):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        MORE = datastore_pb.QueryResultBatch.NOT_FINISHED
        NO_MORE = datastore_pb.QueryResultBatch.MORE_RESULTS_AFTER_LIMIT
        _ID = 123
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = dataset.id()
        path_element = entity_pb.key.path_element.add()
        path_element.kind = self._KIND
        path_element.id = _ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = u'Foo'
        dataset.connection()._results.append(
            ([entity_pb], cursor, MORE if more else NO_MORE))

    def test_ctor_defaults(self):
        query = object()
        iterator = self._makeOne(query)
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, 0)
        self.assertEqual(iterator._offset, 0)

    def test_ctor_explicit(self):
        query = object()
        iterator = self._makeOne(query, 13, 29)
        self.assertTrue(iterator._query is query)
        self.assertEqual(iterator._limit, 13)
        self.assertEqual(iterator._offset, 29)

    def test_next_page_no_cursors_no_more(self):
        from base64 import b64encode
        from gcloud.datastore.query import _pb_from_query
        self._KIND = 'KIND'
        dataset, connection = self._makeDataset()
        query = _Query(self._KIND, dataset, self._NAMESPACE)
        self._addQueryResults(dataset)
        iterator = self._makeOne(query)
        entities, more_results, cursor = iterator.next_page()

        self.assertEqual(cursor, b64encode(self._END))
        self.assertFalse(more_results)
        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key().path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.limit = qpb.offset = 0
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test_next_page_w_cursors_w_more(self):
        from base64 import b64decode
        from base64 import b64encode
        from gcloud.datastore.query import _pb_from_query
        dataset, connection = self._makeDataset()
        query = _Query(self._KIND, dataset, self._NAMESPACE)
        self._addQueryResults(dataset, cursor=self._END, more=True)
        iterator = self._makeOne(query)
        iterator._start_cursor = self._START
        iterator._end_cursor = self._END
        entities, more_results, cursor = iterator.next_page()

        self.assertEqual(cursor, b64encode(self._END))
        self.assertTrue(more_results)
        self.assertTrue(iterator._more_results)
        self.assertEqual(iterator._end_cursor, None)
        self.assertEqual(b64decode(iterator._start_cursor), self._END)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key().path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.limit = qpb.offset = 0
        qpb.start_cursor = b64decode(self._START)
        qpb.end_cursor = b64decode(self._END)
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test_next_page_w_cursors_w_bogus_more(self):
        dataset, connection = self._makeDataset()
        query = _Query(self._KIND, dataset, self._NAMESPACE)
        self._addQueryResults(dataset, cursor=self._END, more=True)
        epb, cursor, _ = connection._results.pop()
        connection._results.append((epb, cursor, 4))  # invalid enum
        iterator = self._makeOne(query)
        self.assertRaises(ValueError, iterator.next_page)

    def test___iter___no_more(self):
        from gcloud.datastore.query import _pb_from_query
        self._KIND = 'KIND'
        dataset, connection = self._makeDataset()
        query = _Query(self._KIND, dataset, self._NAMESPACE)
        self._addQueryResults(dataset)
        iterator = self._makeOne(query)
        entities = list(iterator)

        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key().path,
                         [{'kind': self._KIND, 'id': self._ID}])
        self.assertEqual(entities[0]['foo'], u'Foo')
        qpb = _pb_from_query(query)
        qpb.limit = qpb.offset = 0
        EXPECTED = {
            'dataset_id': self._DATASET,
            'query_pb': qpb,
            'namespace': self._NAMESPACE,
        }
        self.assertEqual(connection._called_with, [EXPECTED])

    def test___iter___w_more(self):
        from gcloud.datastore.query import _pb_from_query
        dataset, connection = self._makeDataset()
        query = _Query(self._KIND, dataset, self._NAMESPACE)
        self._addQueryResults(dataset, cursor=self._END, more=True)
        self._addQueryResults(dataset)
        iterator = self._makeOne(query)
        entities = list(iterator)

        self.assertFalse(iterator._more_results)
        self.assertEqual(len(entities), 2)
        for entity in entities:
            self.assertEqual(
                entity.key().path,
                [{'kind': self._KIND, 'id': self._ID}])
            self.assertEqual(entities[1]['foo'], u'Foo')
        qpb1 = _pb_from_query(query)
        qpb1.limit = qpb1.offset = 0
        qpb2 = _pb_from_query(query)
        qpb2.limit = qpb2.offset = 0
        qpb2.start_cursor = self._END
        EXPECTED1 = {
            'dataset_id': self._DATASET,
            'query_pb': qpb1,
            'namespace': self._NAMESPACE,
        }
        EXPECTED2 = {
            'dataset_id': self._DATASET,
            'query_pb': qpb2,
            'namespace': self._NAMESPACE,
        }
        self.assertEqual(len(connection._called_with), 2)
        self.assertEqual(connection._called_with[0], EXPECTED1)
        self.assertEqual(connection._called_with[1], EXPECTED2)


class _Query(object):

    def __init__(self,
                 kind=None,
                 dataset=None,
                 namespace=None,
                 ancestor=None,
                 filters=(),
                 projection=(),
                 order=(),
                 group_by=()):
        self.kind = kind
        self.dataset = dataset
        self.namespace = namespace
        self.ancestor = ancestor
        self.filters = filters
        self.projection = projection
        self.order = order
        self.group_by = group_by


class _Dataset(object):

    def __init__(self, id, connection):
        self._id = id
        self._connection = connection

    def id(self):
        return self._id

    def connection(self):
        return self._connection


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
