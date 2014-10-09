import unittest2


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
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        key = Key(dataset=Dataset(_DATASET), path=_PATH)
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
        self.assertEqual(name, 'string_value')
        self.assertEqual(value, 'str')

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

    def test_object(self):
        self.assertRaises(ValueError, self._callFUT, object())


class Test__get_value_from_protobuf(unittest2.TestCase):

    def _callFUT(self, pb):
        from gcloud.datastore.helpers import _get_value_from_protobuf

        return _get_value_from_protobuf(pb)

    def _makePB(self, attr_name, value):
        from gcloud.datastore.datastore_v1_pb2 import Property

        prop = Property()
        setattr(prop.value, attr_name, value)
        return prop

    def test_datetime(self):
        import calendar
        import datetime
        import pytz

        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, 4375, pytz.utc)
        micros = (calendar.timegm(utc.timetuple()) * 1000000) + 4375
        pb = self._makePB('timestamp_microseconds_value', micros)
        self.assertEqual(self._callFUT(pb), utc)

    def test_key(self):
        from gcloud.datastore.datastore_v1_pb2 import Property
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        pb = Property()
        expected = Key(dataset=Dataset(_DATASET), path=_PATH).to_protobuf()
        pb.value.key_value.CopyFrom(expected)
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

    def test_native_str(self):
        pb = self._makePB('string_value', 'str')
        self.assertEqual(self._callFUT(pb), 'str')

    def test_unicode(self):
        pb = self._makePB('string_value', u'str')
        self.assertEqual(self._callFUT(pb), u'str')

    def test_entity(self):
        from gcloud.datastore.datastore_v1_pb2 import Property
        from gcloud.datastore.entity import Entity

        pb = Property()
        entity_pb = pb.value.entity_value
        prop_pb = entity_pb.property.add()
        prop_pb.name = 'foo'
        prop_pb.value.string_value = 'Foo'
        entity = self._callFUT(pb)
        self.assertTrue(isinstance(entity, Entity))
        self.assertEqual(entity['foo'], 'Foo')

    def test_unknown(self):
        from gcloud.datastore.datastore_v1_pb2 import Property

        pb = Property()
        self.assertEqual(self._callFUT(pb), None)  # XXX desirable?


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
        from gcloud.datastore.dataset import Dataset
        from gcloud.datastore.key import Key

        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 1234
        _PATH = [{'kind': _KIND, 'id': _ID}]
        pb = self._makePB()
        key = Key(dataset=Dataset(_DATASET), path=_PATH)
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
        value = pb.string_value
        self.assertEqual(value, 'str')

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
        entity['foo'] = 'Foo'
        self._callFUT(pb, entity)
        value = pb.entity_value
        self.assertEqual(value.key, key.to_protobuf())
        props = list(value.property)
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0].name, 'foo')
        self.assertEqual(props[0].value.string_value, 'Foo')
