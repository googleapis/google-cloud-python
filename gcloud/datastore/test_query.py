import unittest2


class TestQuery(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.query import Query

        return Query

    def _makeOne(self, kind=None, dataset=None, namespace=None):
        return self._getTargetClass()(kind, dataset, namespace)

    def test_ctor_defaults(self):
        query = self._getTargetClass()()
        self.assertEqual(query.dataset(), None)
        self.assertEqual(list(query.kind()), [])
        self.assertEqual(query.limit(), 0)
        self.assertEqual(query.namespace(), None)

    def test_ctor_explicit(self):
        from gcloud.datastore.dataset import Dataset

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _NAMESPACE = 'NAMESPACE'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND, dataset, _NAMESPACE)
        self.assertTrue(query.dataset() is dataset)
        kq_pb, = list(query.kind())
        self.assertEqual(kq_pb.name, _KIND)
        self.assertEqual(query.namespace(), _NAMESPACE)

    def test__clone(self):
        from gcloud.datastore.dataset import Dataset

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _CURSOR = 'DEADBEEF'
        _NAMESPACE = 'NAMESPACE'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND, dataset, _NAMESPACE)
        query._cursor = _CURSOR
        clone = query._clone()
        self.assertFalse(clone is query)
        self.assertTrue(isinstance(clone, self._getTargetClass()))
        self.assertTrue(clone.dataset() is dataset)
        self.assertEqual(clone.namespace(), _NAMESPACE)
        kq_pb, = list(clone.kind())
        self.assertEqual(kq_pb.name, _KIND)
        self.assertEqual(clone._cursor, _CURSOR)

    def test_to_protobuf_empty(self):
        query = self._makeOne()
        q_pb = query.to_protobuf()
        self.assertEqual(list(q_pb.kind), [])
        self.assertEqual(list(q_pb.filter.composite_filter.filter), [])

    def test_to_protobuf_w_kind(self):
        _KIND = 'KIND'
        query = self._makeOne(_KIND)
        q_pb = query.to_protobuf()
        kq_pb, = list(q_pb.kind)
        self.assertEqual(kq_pb.name, _KIND)

    def test_filter_w_unknown_operator(self):
        query = self._makeOne()
        self.assertRaises(ValueError, query.filter, 'firstname ~~', 'John')

    def test_filter_w_known_operator(self):
        query = self._makeOne()
        after = query.filter('firstname =', 'John')
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.filter.composite_filter.operator, 1)  # AND
        f_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = f_pb.property_filter
        self.assertEqual(p_pb.property.name, 'firstname')
        self.assertEqual(p_pb.value.string_value, 'John')

    def test_filter_w_known_operator_and_entity(self):
        import operator
        from gcloud.datastore.entity import Entity
        query = self._makeOne()
        other = Entity()
        other['firstname'] = 'John'
        other['lastname'] = 'Smith'
        after = query.filter('other =', other)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.filter.composite_filter.operator, 1)  # AND
        f_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = f_pb.property_filter
        self.assertEqual(p_pb.property.name, 'other')
        other_pb = p_pb.value.entity_value
        props = sorted(other_pb.property, key=operator.attrgetter('name'))
        self.assertEqual(len(props), 2)
        self.assertEqual(props[0].name, 'firstname')
        self.assertEqual(props[0].value.string_value, 'John')
        self.assertEqual(props[1].name, 'lastname')
        self.assertEqual(props[1].value.string_value, 'Smith')

    def test_ancestor_w_non_key_non_list(self):
        query = self._makeOne()
        self.assertRaises(TypeError, query.ancestor, object())

    def test_ancestor_wo_existing_ancestor_query_w_key_and_propfilter(self):
        from gcloud.datastore.key import Key
        _KIND = 'KIND'
        _ID = 123
        _NAME = 'NAME'
        key = Key(path=[{'kind': _KIND, 'id': _ID}])
        query = self._makeOne().filter('name =', _NAME)
        after = query.ancestor(key)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.filter.composite_filter.operator, 1)  # AND
        n_pb, f_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = n_pb.property_filter
        self.assertEqual(p_pb.property.name, 'name')
        self.assertEqual(p_pb.value.string_value, _NAME)
        p_pb = f_pb.property_filter
        self.assertEqual(p_pb.property.name, '__key__')
        self.assertEqual(p_pb.value.key_value, key.to_protobuf())

    def test_ancestor_wo_existing_ancestor_query_w_key(self):
        from gcloud.datastore.key import Key
        _KIND = 'KIND'
        _ID = 123
        key = Key(path=[{'kind': _KIND, 'id': _ID}])
        query = self._makeOne()
        after = query.ancestor(key)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.filter.composite_filter.operator, 1)  # AND
        f_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = f_pb.property_filter
        self.assertEqual(p_pb.property.name, '__key__')
        self.assertEqual(p_pb.value.key_value, key.to_protobuf())

    def test_ancestor_wo_existing_ancestor_query_w_list(self):
        from gcloud.datastore.key import Key
        _KIND = 'KIND'
        _ID = 123
        key = Key(path=[{'kind': _KIND, 'id': _ID}])
        query = self._makeOne()
        after = query.ancestor([_KIND, _ID])
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.filter.composite_filter.operator, 1)  # AND
        f_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = f_pb.property_filter
        self.assertEqual(p_pb.property.name, '__key__')
        self.assertEqual(p_pb.value.key_value, key.to_protobuf())

    def test_ancestor_clears_existing_ancestor_query_w_only(self):
        _KIND = 'KIND'
        _ID = 123
        query = self._makeOne()
        between = query.ancestor([_KIND, _ID])
        after = between.ancestor(None)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        self.assertEqual(list(q_pb.filter.composite_filter.filter), [])

    def test_ancestor_clears_existing_ancestor_query_w_others(self):
        _KIND = 'KIND'
        _ID = 123
        _NAME = 'NAME'
        query = self._makeOne().filter('name =', _NAME)
        between = query.ancestor([_KIND, _ID])
        after = between.ancestor(None)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        q_pb = after.to_protobuf()
        n_pb, = list(q_pb.filter.composite_filter.filter)
        p_pb = n_pb.property_filter
        self.assertEqual(p_pb.property.name, 'name')
        self.assertEqual(p_pb.value.string_value, _NAME)

    def test_kind_setter_wo_existing(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        dataset = Dataset(_DATASET)
        query = self._makeOne(dataset=dataset)
        after = query.kind(_KIND)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        kq_pb, = list(after.kind())
        self.assertEqual(kq_pb.name, _KIND)

    def test_kind_setter_w_existing(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND_BEFORE = 'KIND_BEFORE'
        _KIND_AFTER = 'KIND_AFTER'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND_BEFORE, dataset)
        after = query.kind(_KIND_AFTER)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        kq_pb1, kq_pb2 = list(after.kind())
        self.assertEqual(kq_pb1.name, _KIND_BEFORE)
        self.assertEqual(kq_pb2.name, _KIND_AFTER)

    def test_limit_setter_wo_existing(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _LIMIT = 42
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND, dataset)
        after = query.limit(_LIMIT)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        self.assertEqual(after.limit(), _LIMIT)
        kq_pb, = list(after.kind())
        self.assertEqual(kq_pb.name, _KIND)

    def test_dataset_setter(self):
        from gcloud.datastore.dataset import Dataset
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        dataset = Dataset(_DATASET)
        query = self._makeOne(_KIND)
        after = query.dataset(dataset)
        self.assertFalse(after is query)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertTrue(after.dataset() is dataset)
        kq_pb, = list(query.kind())
        self.assertEqual(kq_pb.name, _KIND)

    def test_fetch_default_limit(self):
        from gcloud.datastore.datastore_v1_pb2 import Entity
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 123
        entity_pb = Entity()
        path_element = entity_pb.key.path_element.add()
        path_element.kind = _KIND
        path_element.id = _ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        entities = query.fetch()
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key().path(),
                         [{'kind': _KIND, 'id': _ID}])
        expected_called_with = {
            'dataset_id': _DATASET,
            'query_pb': query.to_protobuf(),
        }
        self.assertEqual(connection._called_with, expected_called_with)

    def test_fetch_explicit_limit(self):
        from gcloud.datastore.datastore_v1_pb2 import Entity
        _CURSOR = 'CURSOR'
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 123
        entity_pb = Entity()
        path_element = entity_pb.key.path_element.add()
        path_element.kind = _KIND
        path_element.id = _ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        connection._cursor = _CURSOR
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        limited = query.limit(13)
        entities = query.fetch(13)
        self.assertEqual(query._cursor, _CURSOR)
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0].key().path(),
                         [{'kind': _KIND, 'id': _ID}])
        expected_called_with = {
            'dataset_id': _DATASET,
            'query_pb': limited.to_protobuf(),
        }
        self.assertEqual(connection._called_with, expected_called_with)

    def test_cursor_not_fetched(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        self.assertRaises(RuntimeError, query.cursor)

    def test_cursor_fetched(self):
        import base64
        _CURSOR = 'CURSOR'
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        query._cursor = _CURSOR
        self.assertEqual(query.cursor(), base64.b64encode(_CURSOR))

    def test_with_cursor_neither(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        self.assertTrue(query.with_cursor(None) is query)

    def test_with_cursor_w_start(self):
        import base64
        _CURSOR = 'CURSOR'
        _CURSOR_B64 = base64.b64encode(_CURSOR)
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        after = query.with_cursor(_CURSOR_B64)
        self.assertFalse(after is query)
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.start_cursor, _CURSOR)
        self.assertEqual(q_pb.end_cursor, '')

    def test_with_cursor_w_end(self):
        import base64
        _CURSOR = 'CURSOR'
        _CURSOR_B64 = base64.b64encode(_CURSOR)
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        after = query.with_cursor(None, _CURSOR_B64)
        self.assertFalse(after is query)
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.start_cursor, '')
        self.assertEqual(q_pb.end_cursor, _CURSOR)

    def test_with_cursor_w_both(self):
        import base64
        _START = 'START'
        _START_B64 = base64.b64encode(_START)
        _END = 'CURSOR'
        _END_B64 = base64.b64encode(_END)
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        query = self._makeOne(_KIND, dataset)
        after = query.with_cursor(_START_B64, _END_B64)
        self.assertFalse(after is query)
        q_pb = after.to_protobuf()
        self.assertEqual(q_pb.start_cursor, _START)
        self.assertEqual(q_pb.end_cursor, _END)

    def test_order_empty(self):
        _KIND = 'KIND'
        before = self._makeOne(_KIND)
        after = before.order()
        self.assertFalse(after is before)
        self.assertTrue(isinstance(after, self._getTargetClass()))
        self.assertEqual(before.to_protobuf(), after.to_protobuf())

    def test_order_single_asc(self):
        _KIND = 'KIND'
        before = self._makeOne(_KIND)
        after = before.order('field')
        after_pb = after.to_protobuf()
        order_pb = list(after_pb.order)
        self.assertEqual(len(order_pb), 1)
        prop_pb = order_pb[0]
        self.assertEqual(prop_pb.property.name, 'field')
        self.assertEqual(prop_pb.direction, prop_pb.ASCENDING)

    def test_order_single_desc(self):
        _KIND = 'KIND'
        before = self._makeOne(_KIND)
        after = before.order('-field')
        after_pb = after.to_protobuf()
        order_pb = list(after_pb.order)
        self.assertEqual(len(order_pb), 1)
        prop_pb = order_pb[0]
        self.assertEqual(prop_pb.property.name, 'field')
        self.assertEqual(prop_pb.direction, prop_pb.DESCENDING)

    def test_order_multiple(self):
        _KIND = 'KIND'
        before = self._makeOne(_KIND)
        after = before.order('foo', '-bar')
        after_pb = after.to_protobuf()
        order_pb = list(after_pb.order)
        self.assertEqual(len(order_pb), 2)
        prop_pb = order_pb[0]
        self.assertEqual(prop_pb.property.name, 'foo')
        self.assertEqual(prop_pb.direction, prop_pb.ASCENDING)
        prop_pb = order_pb[1]
        self.assertEqual(prop_pb.property.name, 'bar')
        self.assertEqual(prop_pb.direction, prop_pb.DESCENDING)


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
    _cursor = ''
    _more = True
    _skipped = 0

    def __init__(self, *result):
        self._result = list(result)

    def run_query(self, **kw):
        self._called_with = kw
        return self._result, self._cursor, self._more, self._skipped
