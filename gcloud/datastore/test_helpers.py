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


class Test_entity_from_protobuf(unittest2.TestCase):

    def _callFUT(self, val):
        from gcloud.datastore.helpers import entity_from_protobuf
        return entity_from_protobuf(val)

    def test_it(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        _DATASET_ID = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'

        unindexed_prop_pb = entity_pb.property.add()
        unindexed_prop_pb.name = 'bar'
        unindexed_prop_pb.value.integer_value = 10
        unindexed_prop_pb.value.indexed = False

        list_prop_pb1 = entity_pb.property.add()
        list_prop_pb1.name = 'baz'
        list_pb1 = list_prop_pb1.value.list_value

        unindexed_value_pb = list_pb1.add()
        unindexed_value_pb.integer_value = 11
        unindexed_value_pb.indexed = False

        list_prop_pb2 = entity_pb.property.add()
        list_prop_pb2.name = 'qux'
        list_pb2 = list_prop_pb2.value.list_value

        indexed_value_pb = list_pb2.add()
        indexed_value_pb.integer_value = 12
        indexed_value_pb.indexed = True

        entity = self._callFUT(entity_pb)
        self.assertEqual(entity.kind, _KIND)
        self.assertEqual(entity.exclude_from_indexes,
                         frozenset(['bar', 'baz']))
        entity_props = dict(entity)
        self.assertEqual(entity_props,
                         {'foo': 'Foo', 'bar': 10, 'baz': [11], 'qux': [12]})

        # Also check the key.
        key = entity.key
        self.assertEqual(key.dataset_id, _DATASET_ID)
        self.assertEqual(key.namespace, None)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.id, _ID)

    def test_mismatched_value_indexed(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        _DATASET_ID = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)

        list_prop_pb = entity_pb.property.add()
        list_prop_pb.name = 'baz'
        list_pb = list_prop_pb.value.list_value

        unindexed_value_pb1 = list_pb.add()
        unindexed_value_pb1.integer_value = 10
        unindexed_value_pb1.indexed = False

        unindexed_value_pb2 = list_pb.add()
        unindexed_value_pb2.integer_value = 11
        unindexed_value_pb2.indexed = True

        with self.assertRaises(ValueError):
            self._callFUT(entity_pb)

    def test_entity_no_key(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        entity_pb = datastore_pb.Entity()
        entity = self._callFUT(entity_pb)

        self.assertEqual(entity.key, None)
        self.assertEqual(dict(entity), {})

    def test_nested_entity_no_key(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        DATASET_ID = 's~FOO'
        KIND = 'KIND'
        INSIDE_NAME = 'IFOO'
        OUTSIDE_NAME = 'OBAR'
        INSIDE_VALUE = 1337

        entity_inside = datastore_pb.Entity()
        inside_prop = entity_inside.property.add()
        inside_prop.name = INSIDE_NAME
        inside_prop.value.integer_value = INSIDE_VALUE

        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        element = entity_pb.key.path_element.add()
        element.kind = KIND

        outside_prop = entity_pb.property.add()
        outside_prop.name = OUTSIDE_NAME
        outside_prop.value.entity_value.CopyFrom(entity_inside)

        entity = self._callFUT(entity_pb)
        self.assertEqual(entity.key.dataset_id, DATASET_ID)
        self.assertEqual(entity.key.flat_path, (KIND,))
        self.assertEqual(len(entity), 1)

        inside_entity = entity[OUTSIDE_NAME]
        self.assertEqual(inside_entity.key, None)
        self.assertEqual(len(inside_entity), 1)
        self.assertEqual(inside_entity[INSIDE_NAME], INSIDE_VALUE)


class Test_key_from_protobuf(unittest2.TestCase):

    def _callFUT(self, val):
        from gcloud.datastore.helpers import key_from_protobuf

        return key_from_protobuf(val)

    def _makePB(self, dataset_id=None, namespace=None, path=()):
        from gcloud.datastore._datastore_v1_pb2 import Key
        pb = Key()
        if dataset_id is not None:
            pb.partition_id.dataset_id = dataset_id
        if namespace is not None:
            pb.partition_id.namespace = namespace
        for elem in path:
            added = pb.path_element.add()
            added.kind = elem['kind']
            if 'id' in elem:
                added.id = elem['id']
            if 'name' in elem:
                added.name = elem['name']
        return pb

    def test_wo_namespace_in_pb(self):
        _DATASET = 'DATASET'
        pb = self._makePB(path=[{'kind': 'KIND'}], dataset_id=_DATASET)
        key = self._callFUT(pb)
        self.assertEqual(key.dataset_id, _DATASET)
        self.assertEqual(key.namespace, None)

    def test_w_namespace_in_pb(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(path=[{'kind': 'KIND'}], namespace=_NAMESPACE,
                          dataset_id=_DATASET)
        key = self._callFUT(pb)
        self.assertEqual(key.dataset_id, _DATASET)
        self.assertEqual(key.namespace, _NAMESPACE)

    def test_w_nested_path_in_pb(self):
        _PATH = [
            {'kind': 'PARENT', 'name': 'NAME'},
            {'kind': 'CHILD', 'id': 1234},
            {'kind': 'GRANDCHILD', 'id': 5678},
        ]
        pb = self._makePB(path=_PATH, dataset_id='DATASET')
        key = self._callFUT(pb)
        self.assertEqual(key.path, _PATH)

    def test_w_nothing_in_pb(self):
        pb = self._makePB()
        self.assertRaises(ValueError, self._callFUT, pb)


class Test__pb_attr_value(unittest2.TestCase):

    def _callFUT(self, val):
        from gcloud.datastore.helpers import _pb_attr_value

        return _pb_attr_value(val)

    def test_datetime_naive(self):
        import calendar
        import datetime
        from gcloud._helpers import UTC

        naive = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375)  # No zone.
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, UTC)
        name, value = self._callFUT(naive)
        self.assertEqual(name, 'timestamp_microseconds_value')
        self.assertEqual(value // 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_datetime_w_zone(self):
        import calendar
        import datetime
        from gcloud._helpers import UTC

        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, UTC)
        name, value = self._callFUT(utc)
        self.assertEqual(name, 'timestamp_microseconds_value')
        self.assertEqual(value // 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_key(self):
        from gcloud.datastore.key import Key

        key = Key('PATH', 1234, dataset_id='DATASET')
        name, value = self._callFUT(key)
        self.assertEqual(name, 'key_value')
        self.assertEqual(value, key.to_protobuf())

    def test_bool(self):
        name, value = self._callFUT(False)
        self.assertEqual(name, 'boolean_value')
        self.assertEqual(value, False)

    def test_float(self):
        name, value = self._callFUT(3.1415926)
        self.assertEqual(name, 'double_value')
        self.assertEqual(value, 3.1415926)

    def test_int(self):
        name, value = self._callFUT(42)
        self.assertEqual(name, 'integer_value')
        self.assertEqual(value, 42)

    def test_long(self):
        must_be_long = (1 << 63) - 1
        name, value = self._callFUT(must_be_long)
        self.assertEqual(name, 'integer_value')
        self.assertEqual(value, must_be_long)

    def test_long_too_small(self):
        too_small = -(1 << 63) - 1
        self.assertRaises(ValueError, self._callFUT, too_small)

    def test_long_too_large(self):
        too_large = 1 << 63
        self.assertRaises(ValueError, self._callFUT, too_large)

    def test_native_str(self):
        import six
        name, value = self._callFUT('str')
        if six.PY2:
            self.assertEqual(name, 'blob_value')
        else:  # pragma: NO COVER
            self.assertEqual(name, 'string_value')
        self.assertEqual(value, 'str')

    def test_bytes(self):
        name, value = self._callFUT(b'bytes')
        self.assertEqual(name, 'blob_value')
        self.assertEqual(value, b'bytes')

    def test_unicode(self):
        name, value = self._callFUT(u'str')
        self.assertEqual(name, 'string_value')
        self.assertEqual(value, u'str')

    def test_entity(self):
        from gcloud.datastore.entity import Entity
        entity = Entity()
        name, value = self._callFUT(entity)
        self.assertEqual(name, 'entity_value')
        self.assertTrue(value is entity)

    def test_list(self):
        values = ['a', 0, 3.14]
        name, value = self._callFUT(values)
        self.assertEqual(name, 'list_value')
        self.assertTrue(value is values)

    def test_object(self):
        self.assertRaises(ValueError, self._callFUT, object())


class Test__get_value_from_value_pb(unittest2.TestCase):

    def _callFUT(self, pb):
        from gcloud.datastore.helpers import _get_value_from_value_pb

        return _get_value_from_value_pb(pb)

    def _makePB(self, attr_name, value):
        from gcloud.datastore._datastore_v1_pb2 import Value

        pb = Value()
        setattr(pb, attr_name, value)
        return pb

    def test_datetime(self):
        import calendar
        import datetime
        from gcloud._helpers import UTC

        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, UTC)
        micros = (calendar.timegm(utc.timetuple()) * 1000000) + 4375
        pb = self._makePB('timestamp_microseconds_value', micros)
        self.assertEqual(self._callFUT(pb), utc)

    def test_key(self):
        from gcloud.datastore._datastore_v1_pb2 import Value
        from gcloud.datastore.key import Key

        pb = Value()
        expected = Key('KIND', 1234, dataset_id='DATASET').to_protobuf()
        pb.key_value.CopyFrom(expected)
        found = self._callFUT(pb)
        self.assertEqual(found.to_protobuf(), expected)

    def test_bool(self):
        pb = self._makePB('boolean_value', False)
        self.assertEqual(self._callFUT(pb), False)

    def test_float(self):
        pb = self._makePB('double_value', 3.1415926)
        self.assertEqual(self._callFUT(pb), 3.1415926)

    def test_int(self):
        pb = self._makePB('integer_value', 42)
        self.assertEqual(self._callFUT(pb), 42)

    def test_bytes(self):
        pb = self._makePB('blob_value', b'str')
        self.assertEqual(self._callFUT(pb), b'str')

    def test_unicode(self):
        pb = self._makePB('string_value', u'str')
        self.assertEqual(self._callFUT(pb), u'str')

    def test_entity(self):
        from gcloud.datastore._datastore_v1_pb2 import Value
        from gcloud.datastore.entity import Entity

        pb = Value()
        entity_pb = pb.entity_value
        entity_pb.key.path_element.add(kind='KIND')
        entity_pb.key.partition_id.dataset_id = 'DATASET'
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        entity = self._callFUT(pb)
        self.assertTrue(isinstance(entity, Entity))
        self.assertEqual(entity['foo'], 'Foo')

    def test_list(self):
        from gcloud.datastore._datastore_v1_pb2 import Value

        pb = Value()
        list_pb = pb.list_value
        item_pb = list_pb.add()
        item_pb.string_value = 'Foo'
        item_pb = list_pb.add()
        item_pb.string_value = 'Bar'
        items = self._callFUT(pb)
        self.assertEqual(items, ['Foo', 'Bar'])

    def test_unknown(self):
        from gcloud.datastore._datastore_v1_pb2 import Value

        pb = Value()
        self.assertEqual(self._callFUT(pb), None)


class Test__get_value_from_property_pb(unittest2.TestCase):

    def _callFUT(self, pb):
        from gcloud.datastore.helpers import _get_value_from_property_pb

        return _get_value_from_property_pb(pb)

    def test_it(self):
        from gcloud.datastore._datastore_v1_pb2 import Property

        pb = Property()
        pb.value.string_value = 'value'
        self.assertEqual(self._callFUT(pb), 'value')


class Test_set_protobuf_value(unittest2.TestCase):

    def _callFUT(self, value_pb, val):
        from gcloud.datastore.helpers import _set_protobuf_value

        return _set_protobuf_value(value_pb, val)

    def _makePB(self):
        from gcloud.datastore._datastore_v1_pb2 import Value

        return Value()

    def test_datetime(self):
        import calendar
        import datetime
        from gcloud._helpers import UTC

        pb = self._makePB()
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, UTC)
        self._callFUT(pb, utc)
        value = pb.timestamp_microseconds_value
        self.assertEqual(value // 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_key(self):
        from gcloud.datastore.key import Key

        pb = self._makePB()
        key = Key('KIND', 1234, dataset_id='DATASET')
        self._callFUT(pb, key)
        value = pb.key_value
        self.assertEqual(value, key.to_protobuf())

    def test_none(self):
        from gcloud.datastore.entity import Entity

        entity = Entity()
        pb = self._makePB()

        self._callFUT(pb, False)
        self._callFUT(pb, 3.1415926)
        self._callFUT(pb, 42)
        self._callFUT(pb, (1 << 63) - 1)
        self._callFUT(pb, 'str')
        self._callFUT(pb, b'str')
        self._callFUT(pb, u'str')
        self._callFUT(pb, entity)
        self._callFUT(pb, [u'a', 0, 3.14])

        self._callFUT(pb, None)
        self.assertEqual(len(pb.ListFields()), 0)

    def test_bool(self):
        pb = self._makePB()
        self._callFUT(pb, False)
        value = pb.boolean_value
        self.assertEqual(value, False)

    def test_float(self):
        pb = self._makePB()
        self._callFUT(pb, 3.1415926)
        value = pb.double_value
        self.assertEqual(value, 3.1415926)

    def test_int(self):
        pb = self._makePB()
        self._callFUT(pb, 42)
        value = pb.integer_value
        self.assertEqual(value, 42)

    def test_long(self):
        pb = self._makePB()
        must_be_long = (1 << 63) - 1
        self._callFUT(pb, must_be_long)
        value = pb.integer_value
        self.assertEqual(value, must_be_long)

    def test_native_str(self):
        import six
        pb = self._makePB()
        self._callFUT(pb, 'str')
        if six.PY2:
            value = pb.blob_value
        else:  # pragma: NO COVER
            value = pb.string_value
        self.assertEqual(value, 'str')

    def test_bytes(self):
        pb = self._makePB()
        self._callFUT(pb, b'str')
        value = pb.blob_value
        self.assertEqual(value, b'str')

    def test_unicode(self):
        pb = self._makePB()
        self._callFUT(pb, u'str')
        value = pb.string_value
        self.assertEqual(value, u'str')

    def test_entity_empty_wo_key(self):
        from gcloud.datastore.entity import Entity

        pb = self._makePB()
        entity = Entity()
        self._callFUT(pb, entity)
        value = pb.entity_value
        self.assertEqual(value.key.SerializeToString(), b'')
        props = list(value.property)
        self.assertEqual(len(props), 0)

    def test_entity_w_key(self):
        from gcloud.datastore.entity import Entity
        from gcloud.datastore.key import Key

        pb = self._makePB()
        key = Key('KIND', 123, dataset_id='DATASET')
        entity = Entity(key=key)
        entity['foo'] = u'Foo'
        self._callFUT(pb, entity)
        value = pb.entity_value
        self.assertEqual(value.key, key.to_protobuf())
        props = list(value.property)
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0].name, 'foo')
        self.assertEqual(props[0].value.string_value, u'Foo')

    def test_list(self):
        pb = self._makePB()
        values = [u'a', 0, 3.14]
        self._callFUT(pb, values)
        marshalled = pb.list_value
        self.assertEqual(len(marshalled), len(values))
        self.assertEqual(marshalled[0].string_value, values[0])
        self.assertEqual(marshalled[1].integer_value, values[1])
        self.assertEqual(marshalled[2].double_value, values[2])


class Test__prepare_key_for_request(unittest2.TestCase):

    def _callFUT(self, key_pb):
        from gcloud.datastore.helpers import _prepare_key_for_request

        return _prepare_key_for_request(key_pb)

    def test_prepare_dataset_id_valid(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        key = datastore_pb.Key()
        key.partition_id.dataset_id = 'foo'
        new_key = self._callFUT(key)
        self.assertFalse(new_key is key)

        key_without = datastore_pb.Key()
        new_key.ClearField('partition_id')
        self.assertEqual(new_key, key_without)

    def test_prepare_dataset_id_unset(self):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
        key = datastore_pb.Key()
        new_key = self._callFUT(key)
        self.assertTrue(new_key is key)


class Test_find_true_dataset_id(unittest2.TestCase):

    def _callFUT(self, dataset_id, connection):
        from gcloud.datastore.helpers import find_true_dataset_id
        return find_true_dataset_id(dataset_id, connection)

    def test_prefixed(self):
        PREFIXED = 's~DATASET'
        result = self._callFUT(PREFIXED, object())
        self.assertEqual(PREFIXED, result)

    def test_unprefixed_bogus_key_miss(self):
        UNPREFIXED = 'DATASET'
        PREFIX = 's~'
        CONNECTION = _Connection(PREFIX, from_missing=False)
        result = self._callFUT(UNPREFIXED, CONNECTION)

        self.assertEqual(CONNECTION._called_dataset_id, UNPREFIXED)

        self.assertEqual(len(CONNECTION._lookup_result), 1)

        # Make sure just one.
        called_key_pb, = CONNECTION._called_key_pbs
        path_element = called_key_pb.path_element
        self.assertEqual(len(path_element), 1)
        self.assertEqual(path_element[0].kind, '__MissingLookupKind')
        self.assertEqual(path_element[0].id, 1)
        self.assertFalse(path_element[0].HasField('name'))

        PREFIXED = PREFIX + UNPREFIXED
        self.assertEqual(result, PREFIXED)

    def test_unprefixed_bogus_key_hit(self):
        UNPREFIXED = 'DATASET'
        PREFIX = 'e~'
        CONNECTION = _Connection(PREFIX, from_missing=True)
        result = self._callFUT(UNPREFIXED, CONNECTION)

        self.assertEqual(CONNECTION._called_dataset_id, UNPREFIXED)
        self.assertEqual(CONNECTION._lookup_result, [])

        # Make sure just one.
        called_key_pb, = CONNECTION._called_key_pbs
        path_element = called_key_pb.path_element
        self.assertEqual(len(path_element), 1)
        self.assertEqual(path_element[0].kind, '__MissingLookupKind')
        self.assertEqual(path_element[0].id, 1)
        self.assertFalse(path_element[0].HasField('name'))

        PREFIXED = PREFIX + UNPREFIXED
        self.assertEqual(result, PREFIXED)


class _Connection(object):

    _called_dataset_id = _called_key_pbs = _lookup_result = None

    def __init__(self, prefix, from_missing=False):
        self.prefix = prefix
        self.from_missing = from_missing

    def lookup(self, dataset_id, key_pbs):
        from gcloud.datastore import _datastore_v1_pb2 as datastore_pb

        # Store the arguments called with.
        self._called_dataset_id = dataset_id
        self._called_key_pbs = key_pbs

        key_pb, = key_pbs

        response = datastore_pb.Entity()
        response.key.CopyFrom(key_pb)
        response.key.partition_id.dataset_id = self.prefix + dataset_id

        missing = []
        deferred = []
        if self.from_missing:
            missing[:] = [response]
            self._lookup_result = []
        else:
            self._lookup_result = [response]

        return self._lookup_result, missing, deferred
