import unittest2


class Test_entity_from_protobuf(unittest2.TestCase):

    _MARKER = object()

    def _callFUT(self, val, dataset=_MARKER):
        from gcloud.datastore.helpers import entity_from_protobuf

        if dataset is self._MARKER:
            return entity_from_protobuf(val)

        return entity_from_protobuf(val, dataset)

    def test_wo_dataset(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb

        _DATASET_ID = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        entity = self._callFUT(entity_pb)
        self.assertTrue(entity.dataset() is None)
        self.assertEqual(entity.kind(), _KIND)
        self.assertEqual(entity['foo'], 'Foo')
        key = entity.key()
        self.assertEqual(key._dataset_id, _DATASET_ID)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)

    def test_w_dataset(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.dataset import Dataset

        _DATASET_ID = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        entity_pb.key.path_element.add(kind=_KIND, id=_ID)
        entity_pb.key.partition_id.dataset_id = _DATASET_ID
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        dataset = Dataset(_DATASET_ID)
        entity = self._callFUT(entity_pb, dataset)
        self.assertTrue(entity.dataset() is dataset)
        self.assertEqual(entity.kind(), _KIND)
        self.assertEqual(entity['foo'], 'Foo')
        key = entity.key()
        self.assertEqual(key._dataset_id, _DATASET_ID)
        self.assertEqual(key.kind(), _KIND)
        self.assertEqual(key.id(), _ID)


class Test_key_from_protobuf(unittest2.TestCase):

    def _callFUT(self, val):
        from gcloud.datastore.helpers import key_from_protobuf

        return key_from_protobuf(val)

    def _makePB(self, dataset_id=None, namespace=None, path=()):
        from gcloud.datastore.datastore_v1_pb2 import Key
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

    def test_w_dataset_id_in_pb(self):
        _DATASET = 'DATASET'
        pb = self._makePB(_DATASET)
        key = self._callFUT(pb)
        self.assertEqual(key._dataset_id, _DATASET)

    def test_w_namespace_in_pb(self):
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(namespace=_NAMESPACE)
        key = self._callFUT(pb)
        self.assertEqual(key.namespace(), _NAMESPACE)

    def test_w_path_in_pb(self):
        _DATASET = 'DATASET'
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(_DATASET, _NAMESPACE)
        _PARENT = 'PARENT'
        _CHILD = 'CHILD'
        _GRANDCHILD = 'GRANDCHILD'
        _ID = 1234
        _ID2 = 5678
        _NAME = 'NAME'
        _NAME2 = 'NAME2'
        _PATH = [
            {'kind': _PARENT, 'name': _NAME},
            {'kind': _CHILD, 'id': _ID},
            {'kind': _GRANDCHILD, 'id': _ID2, 'name': _NAME2},
        ]
        pb = self._makePB(path=_PATH)
        key = self._callFUT(pb)
        self.assertEqual(key.path(), _PATH)


class Test__get_protobuf_attribute_and_value(unittest2.TestCase):

    def _callFUT(self, val):
        from gcloud.datastore.helpers import _get_protobuf_attribute_and_value

        return _get_protobuf_attribute_and_value(val)

    def test_datetime_naive(self):
        import calendar
        import datetime
        import pytz

        naive = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375)  # No zone.
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, pytz.utc)
        name, value = self._callFUT(naive)
        self.assertEqual(name, 'timestamp_microseconds_value')
        self.assertEqual(value / 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_datetime_w_zone(self):
        import calendar
        import datetime
        import pytz

        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, pytz.utc)
        name, value = self._callFUT(utc)
        self.assertEqual(name, 'timestamp_microseconds_value')
        self.assertEqual(value / 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_key(self):
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = Key(dataset_id=_DATASET, path=_PATH)
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
        name, value = self._callFUT('str')
        self.assertEqual(name, 'blob_value')
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
        from gcloud.datastore.datastore_v1_pb2 import Value

        pb = Value()
        setattr(pb, attr_name, value)
        return pb

    def test_datetime(self):
        import calendar
        import datetime
        import pytz

        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, pytz.utc)
        micros = (calendar.timegm(utc.timetuple()) * 1000000) + 4375
        pb = self._makePB('timestamp_microseconds_value', micros)
        self.assertEqual(self._callFUT(pb), utc)

    def test_key(self):
        from gcloud.datastore.datastore_v1_pb2 import Value
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        pb = Value()
        expected = Key(dataset_id=_DATASET, path=_PATH).to_protobuf()
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
        from gcloud.datastore.datastore_v1_pb2 import Value
        from gcloud.datastore.entity import Entity

        pb = Value()
        entity_pb = pb.entity_value
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        entity = self._callFUT(pb)
        self.assertTrue(isinstance(entity, Entity))
        self.assertEqual(entity['foo'], 'Foo')

    def test_list(self):
        from gcloud.datastore.datastore_v1_pb2 import Value

        pb = Value()
        list_pb = pb.list_value
        item_pb = list_pb.add()
        item_pb.string_value = 'Foo'
        item_pb = list_pb.add()
        item_pb.string_value = 'Bar'
        items = self._callFUT(pb)
        self.assertEqual(items, ['Foo', 'Bar'])

    def test_unknown(self):
        from gcloud.datastore.datastore_v1_pb2 import Value

        pb = Value()
        self.assertEqual(self._callFUT(pb), None)


class Test__get_value_from_property_pb(unittest2.TestCase):

    def _callFUT(self, pb):
        from gcloud.datastore.helpers import _get_value_from_property_pb

        return _get_value_from_property_pb(pb)

    def test_it(self):
        from gcloud.datastore.datastore_v1_pb2 import Property

        pb = Property()
        pb.value.string_value = 'value'
        self.assertEqual(self._callFUT(pb), 'value')


class Test_set_protobuf_value(unittest2.TestCase):

    def _callFUT(self, value_pb, val):
        from gcloud.datastore.helpers import _set_protobuf_value

        return _set_protobuf_value(value_pb, val)

    def _makePB(self):
        from gcloud.datastore.datastore_v1_pb2 import Value

        return Value()

    def test_datetime(self):
        import calendar
        import datetime
        import pytz

        pb = self._makePB()
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, pytz.utc)
        self._callFUT(pb, utc)
        value = pb.timestamp_microseconds_value
        self.assertEqual(value / 1000000, calendar.timegm(utc.timetuple()))
        self.assertEqual(value % 1000000, 4375)

    def test_key(self):
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        pb = self._makePB()
        key = Key(dataset_id=_DATASET, path=_PATH)
        self._callFUT(pb, key)
        value = pb.key_value
        self.assertEqual(value, key.to_protobuf())

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
        pb = self._makePB()
        self._callFUT(pb, 'str')
        value = pb.blob_value
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
        self.assertEqual(value.key.SerializeToString(), '')
        props = list(value.property)
        self.assertEqual(len(props), 0)

    def test_entity_w_key(self):
        from gcloud.datastore.entity import Entity
        from gcloud.datastore.key import Key

        pb = self._makePB()
        key = Key(path=[{'kind': 'KIND', 'id': 123}])
        entity = Entity().key(key)
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
