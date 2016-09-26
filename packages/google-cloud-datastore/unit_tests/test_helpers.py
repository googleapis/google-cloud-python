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


class Test__new_value_pb(unittest.TestCase):

    def _callFUT(self, entity_pb, name):
        from google.cloud.datastore.helpers import _new_value_pb
        return _new_value_pb(entity_pb, name)

    def test_it(self):
        from google.cloud.datastore._generated import entity_pb2

        entity_pb = entity_pb2.Entity()
        name = 'foo'
        result = self._callFUT(entity_pb, name)

        self.assertIsInstance(result, entity_pb2.Value)
        self.assertEqual(len(entity_pb.properties), 1)
        self.assertEqual(entity_pb.properties[name], result)


class Test__property_tuples(unittest.TestCase):

    def _callFUT(self, entity_pb):
        from google.cloud.datastore.helpers import _property_tuples
        return _property_tuples(entity_pb)

    def test_it(self):
        import types
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        entity_pb = entity_pb2.Entity()
        name1 = 'foo'
        name2 = 'bar'
        val_pb1 = _new_value_pb(entity_pb, name1)
        val_pb2 = _new_value_pb(entity_pb, name2)

        result = self._callFUT(entity_pb)
        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(sorted(result),
                         sorted([(name1, val_pb1), (name2, val_pb2)]))


class Test_entity_from_protobuf(unittest.TestCase):

    def _callFUT(self, val):
        from google.cloud.datastore.helpers import entity_from_protobuf
        return entity_from_protobuf(val)

    def test_it(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = entity_pb2.Entity()
        entity_pb.key.partition_id.project_id = _PROJECT
        entity_pb.key.path.add(kind=_KIND, id=_ID)

        value_pb = _new_value_pb(entity_pb, 'foo')
        value_pb.string_value = 'Foo'

        unindexed_val_pb = _new_value_pb(entity_pb, 'bar')
        unindexed_val_pb.integer_value = 10
        unindexed_val_pb.exclude_from_indexes = True

        array_val_pb1 = _new_value_pb(entity_pb, 'baz')
        array_pb1 = array_val_pb1.array_value.values

        unindexed_array_val_pb = array_pb1.add()
        unindexed_array_val_pb.integer_value = 11
        unindexed_array_val_pb.exclude_from_indexes = True

        array_val_pb2 = _new_value_pb(entity_pb, 'qux')
        array_pb2 = array_val_pb2.array_value.values

        indexed_array_val_pb = array_pb2.add()
        indexed_array_val_pb.integer_value = 12

        entity = self._callFUT(entity_pb)
        self.assertEqual(entity.kind, _KIND)
        self.assertEqual(entity.exclude_from_indexes,
                         frozenset(['bar', 'baz']))
        entity_props = dict(entity)
        self.assertEqual(entity_props,
                         {'foo': 'Foo', 'bar': 10, 'baz': [11], 'qux': [12]})

        # Also check the key.
        key = entity.key
        self.assertEqual(key.project, _PROJECT)
        self.assertIsNone(key.namespace)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.id, _ID)

    def test_mismatched_value_indexed(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 1234
        entity_pb = entity_pb2.Entity()
        entity_pb.key.partition_id.project_id = _PROJECT
        entity_pb.key.path.add(kind=_KIND, id=_ID)

        array_val_pb = _new_value_pb(entity_pb, 'baz')
        array_pb = array_val_pb.array_value.values

        unindexed_value_pb1 = array_pb.add()
        unindexed_value_pb1.integer_value = 10
        unindexed_value_pb1.exclude_from_indexes = True

        unindexed_value_pb2 = array_pb.add()
        unindexed_value_pb2.integer_value = 11

        with self.assertRaises(ValueError):
            self._callFUT(entity_pb)

    def test_entity_no_key(self):
        from google.cloud.datastore._generated import entity_pb2

        entity_pb = entity_pb2.Entity()
        entity = self._callFUT(entity_pb)

        self.assertIsNone(entity.key)
        self.assertEqual(dict(entity), {})

    def test_entity_with_meaning(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        entity_pb = entity_pb2.Entity()
        name = 'hello'
        value_pb = _new_value_pb(entity_pb, name)
        value_pb.meaning = meaning = 9
        value_pb.string_value = val = u'something'

        entity = self._callFUT(entity_pb)
        self.assertIsNone(entity.key)
        self.assertEqual(dict(entity), {name: val})
        self.assertEqual(entity._meanings, {name: (meaning, val)})

    def test_nested_entity_no_key(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb

        PROJECT = 'FOO'
        KIND = 'KIND'
        INSIDE_NAME = 'IFOO'
        OUTSIDE_NAME = 'OBAR'
        INSIDE_VALUE = 1337

        entity_inside = entity_pb2.Entity()
        inside_val_pb = _new_value_pb(entity_inside, INSIDE_NAME)
        inside_val_pb.integer_value = INSIDE_VALUE

        entity_pb = entity_pb2.Entity()
        entity_pb.key.partition_id.project_id = PROJECT
        element = entity_pb.key.path.add()
        element.kind = KIND

        outside_val_pb = _new_value_pb(entity_pb, OUTSIDE_NAME)
        outside_val_pb.entity_value.CopyFrom(entity_inside)

        entity = self._callFUT(entity_pb)
        self.assertEqual(entity.key.project, PROJECT)
        self.assertEqual(entity.key.flat_path, (KIND,))
        self.assertEqual(len(entity), 1)

        inside_entity = entity[OUTSIDE_NAME]
        self.assertIsNone(inside_entity.key)
        self.assertEqual(len(inside_entity), 1)
        self.assertEqual(inside_entity[INSIDE_NAME], INSIDE_VALUE)


class Test_entity_to_protobuf(unittest.TestCase):

    def _callFUT(self, entity):
        from google.cloud.datastore.helpers import entity_to_protobuf
        return entity_to_protobuf(entity)

    def _compareEntityProto(self, entity_pb1, entity_pb2):
        from google.cloud.datastore.helpers import _property_tuples

        self.assertEqual(entity_pb1.key, entity_pb2.key)
        value_list1 = sorted(_property_tuples(entity_pb1))
        value_list2 = sorted(_property_tuples(entity_pb2))
        self.assertEqual(len(value_list1), len(value_list2))
        for pair1, pair2 in zip(value_list1, value_list2):
            name1, val1 = pair1
            name2, val2 = pair2
            self.assertEqual(name1, name2)
            if val1.HasField('entity_value'):  # Message field (Entity)
                self.assertEqual(val1.meaning, val2.meaning)
                self._compareEntityProto(val1.entity_value,
                                         val2.entity_value)
            else:
                self.assertEqual(val1, val2)

    def test_empty(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity

        entity = Entity()
        entity_pb = self._callFUT(entity)
        self._compareEntityProto(entity_pb, entity_pb2.Entity())

    def test_key_only(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.key import Key

        kind, name = 'PATH', 'NAME'
        project = 'PROJECT'
        key = Key(kind, name, project=project)
        entity = Entity(key=key)
        entity_pb = self._callFUT(entity)

        expected_pb = entity_pb2.Entity()
        expected_pb.key.partition_id.project_id = project
        path_elt = expected_pb.key.path.add()
        path_elt.kind = kind
        path_elt.name = name

        self._compareEntityProto(entity_pb, expected_pb)

    def test_simple_fields(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _new_value_pb

        entity = Entity()
        name1 = 'foo'
        entity[name1] = value1 = 42
        name2 = 'bar'
        entity[name2] = value2 = u'some-string'
        entity_pb = self._callFUT(entity)

        expected_pb = entity_pb2.Entity()
        val_pb1 = _new_value_pb(expected_pb, name1)
        val_pb1.integer_value = value1
        val_pb2 = _new_value_pb(expected_pb, name2)
        val_pb2.string_value = value2

        self._compareEntityProto(entity_pb, expected_pb)

    def test_with_empty_list(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity

        entity = Entity()
        entity['foo'] = []
        entity_pb = self._callFUT(entity)

        self._compareEntityProto(entity_pb, entity_pb2.Entity())

    def test_inverts_to_protobuf(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import _new_value_pb
        from google.cloud.datastore.helpers import entity_from_protobuf

        original_pb = entity_pb2.Entity()
        # Add a key.
        original_pb.key.partition_id.project_id = project = 'PROJECT'
        elem1 = original_pb.key.path.add()
        elem1.kind = 'Family'
        elem1.id = 1234
        elem2 = original_pb.key.path.add()
        elem2.kind = 'King'
        elem2.name = 'Spades'

        # Add an integer property.
        val_pb1 = _new_value_pb(original_pb, 'foo')
        val_pb1.integer_value = 1337
        val_pb1.exclude_from_indexes = True
        # Add a string property.
        val_pb2 = _new_value_pb(original_pb, 'bar')
        val_pb2.string_value = u'hello'

        # Add a nested (entity) property.
        val_pb3 = _new_value_pb(original_pb, 'entity-baz')
        sub_pb = entity_pb2.Entity()
        sub_val_pb1 = _new_value_pb(sub_pb, 'x')
        sub_val_pb1.double_value = 3.14
        sub_val_pb2 = _new_value_pb(sub_pb, 'y')
        sub_val_pb2.double_value = 2.718281828
        val_pb3.meaning = 9
        val_pb3.entity_value.CopyFrom(sub_pb)

        # Add a list property.
        val_pb4 = _new_value_pb(original_pb, 'list-quux')
        array_val1 = val_pb4.array_value.values.add()
        array_val1.exclude_from_indexes = False
        array_val1.meaning = meaning = 22
        array_val1.blob_value = b'\xe2\x98\x83'
        array_val2 = val_pb4.array_value.values.add()
        array_val2.exclude_from_indexes = False
        array_val2.meaning = meaning
        array_val2.blob_value = b'\xe2\x98\x85'

        # Convert to the user-space Entity.
        entity = entity_from_protobuf(original_pb)
        # Convert the user-space Entity back to a protobuf.
        new_pb = self._callFUT(entity)

        # NOTE: entity_to_protobuf() strips the project so we "cheat".
        new_pb.key.partition_id.project_id = project
        self._compareEntityProto(original_pb, new_pb)

    def test_meaning_with_change(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _new_value_pb

        entity = Entity()
        name = 'foo'
        entity[name] = value = 42
        entity._meanings[name] = (9, 1337)
        entity_pb = self._callFUT(entity)

        expected_pb = entity_pb2.Entity()
        value_pb = _new_value_pb(expected_pb, name)
        value_pb.integer_value = value
        # NOTE: No meaning is used since the value differs from the
        #       value stored.
        self._compareEntityProto(entity_pb, expected_pb)

    def test_variable_meanings(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _new_value_pb

        entity = Entity()
        name = 'quux'
        entity[name] = values = [1, 20, 300]
        meaning = 9
        entity._meanings[name] = ([None, meaning, None], values)
        entity_pb = self._callFUT(entity)

        # Construct the expected protobuf.
        expected_pb = entity_pb2.Entity()
        value_pb = _new_value_pb(expected_pb, name)
        value0 = value_pb.array_value.values.add()
        value0.integer_value = values[0]
        # The only array entry with a meaning is the middle one.
        value1 = value_pb.array_value.values.add()
        value1.integer_value = values[1]
        value1.meaning = meaning
        value2 = value_pb.array_value.values.add()
        value2.integer_value = values[2]

        self._compareEntityProto(entity_pb, expected_pb)


class Test_key_from_protobuf(unittest.TestCase):

    def _callFUT(self, val):
        from google.cloud.datastore.helpers import key_from_protobuf

        return key_from_protobuf(val)

    def _makePB(self, project=None, namespace=None, path=()):
        from google.cloud.datastore._generated import entity_pb2
        pb = entity_pb2.Key()
        if project is not None:
            pb.partition_id.project_id = project
        if namespace is not None:
            pb.partition_id.namespace_id = namespace
        for elem in path:
            added = pb.path.add()
            added.kind = elem['kind']
            if 'id' in elem:
                added.id = elem['id']
            if 'name' in elem:
                added.name = elem['name']
        return pb

    def test_wo_namespace_in_pb(self):
        _PROJECT = 'PROJECT'
        pb = self._makePB(path=[{'kind': 'KIND'}], project=_PROJECT)
        key = self._callFUT(pb)
        self.assertEqual(key.project, _PROJECT)
        self.assertIsNone(key.namespace)

    def test_w_namespace_in_pb(self):
        _PROJECT = 'PROJECT'
        _NAMESPACE = 'NAMESPACE'
        pb = self._makePB(path=[{'kind': 'KIND'}], namespace=_NAMESPACE,
                          project=_PROJECT)
        key = self._callFUT(pb)
        self.assertEqual(key.project, _PROJECT)
        self.assertEqual(key.namespace, _NAMESPACE)

    def test_w_nested_path_in_pb(self):
        _PATH = [
            {'kind': 'PARENT', 'name': 'NAME'},
            {'kind': 'CHILD', 'id': 1234},
            {'kind': 'GRANDCHILD', 'id': 5678},
        ]
        pb = self._makePB(path=_PATH, project='PROJECT')
        key = self._callFUT(pb)
        self.assertEqual(key.path, _PATH)

    def test_w_nothing_in_pb(self):
        pb = self._makePB()
        self.assertRaises(ValueError, self._callFUT, pb)


class Test__pb_attr_value(unittest.TestCase):

    def _callFUT(self, val):
        from google.cloud.datastore.helpers import _pb_attr_value

        return _pb_attr_value(val)

    def test_datetime_naive(self):
        import calendar
        import datetime
        from google.cloud._helpers import UTC

        micros = 4375
        naive = datetime.datetime(2014, 9, 16, 10, 19, 32, micros)  # No zone.
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, micros, UTC)
        name, value = self._callFUT(naive)
        self.assertEqual(name, 'timestamp_value')
        self.assertEqual(value.seconds, calendar.timegm(utc.timetuple()))
        self.assertEqual(value.nanos, 1000 * micros)

    def test_datetime_w_zone(self):
        import calendar
        import datetime
        from google.cloud._helpers import UTC

        micros = 4375
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, micros, UTC)
        name, value = self._callFUT(utc)
        self.assertEqual(name, 'timestamp_value')
        self.assertEqual(value.seconds, calendar.timegm(utc.timetuple()))
        self.assertEqual(value.nanos, 1000 * micros)

    def test_key(self):
        from google.cloud.datastore.key import Key

        key = Key('PATH', 1234, project='PROJECT')
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

    def test_native_str(self):
        import six
        name, value = self._callFUT('str')
        if six.PY2:
            self.assertEqual(name, 'blob_value')
        else:  # pragma: NO COVER Python 3
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
        from google.cloud.datastore.entity import Entity
        entity = Entity()
        name, value = self._callFUT(entity)
        self.assertEqual(name, 'entity_value')
        self.assertIs(value, entity)

    def test_array(self):
        values = ['a', 0, 3.14]
        name, value = self._callFUT(values)
        self.assertEqual(name, 'array_value')
        self.assertIs(value, values)

    def test_geo_point(self):
        from google.type import latlng_pb2
        from google.cloud.datastore.helpers import GeoPoint

        lat = 42.42
        lng = 99.0007
        geo_pt = GeoPoint(latitude=lat, longitude=lng)
        geo_pt_pb = latlng_pb2.LatLng(latitude=lat, longitude=lng)
        name, value = self._callFUT(geo_pt)
        self.assertEqual(name, 'geo_point_value')
        self.assertEqual(value, geo_pt_pb)

    def test_null(self):
        from google.protobuf import struct_pb2

        name, value = self._callFUT(None)
        self.assertEqual(name, 'null_value')
        self.assertEqual(value, struct_pb2.NULL_VALUE)

    def test_object(self):
        self.assertRaises(ValueError, self._callFUT, object())


class Test__get_value_from_value_pb(unittest.TestCase):

    def _callFUT(self, pb):
        from google.cloud.datastore.helpers import _get_value_from_value_pb

        return _get_value_from_value_pb(pb)

    def _makePB(self, attr_name, value):
        from google.cloud.datastore._generated import entity_pb2

        pb = entity_pb2.Value()
        setattr(pb, attr_name, value)
        return pb

    def test_datetime(self):
        import calendar
        import datetime
        from google.cloud._helpers import UTC
        from google.cloud.datastore._generated import entity_pb2

        micros = 4375
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, micros, UTC)
        pb = entity_pb2.Value()
        pb.timestamp_value.seconds = calendar.timegm(utc.timetuple())
        pb.timestamp_value.nanos = 1000 * micros
        self.assertEqual(self._callFUT(pb), utc)

    def test_key(self):
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.key import Key

        pb = entity_pb2.Value()
        expected = Key('KIND', 1234, project='PROJECT').to_protobuf()
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
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _new_value_pb

        pb = entity_pb2.Value()
        entity_pb = pb.entity_value
        entity_pb.key.path.add(kind='KIND')
        entity_pb.key.partition_id.project_id = 'PROJECT'

        value_pb = _new_value_pb(entity_pb, 'foo')
        value_pb.string_value = 'Foo'
        entity = self._callFUT(pb)
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity['foo'], 'Foo')

    def test_array(self):
        from google.cloud.datastore._generated import entity_pb2

        pb = entity_pb2.Value()
        array_pb = pb.array_value.values
        item_pb = array_pb.add()
        item_pb.string_value = 'Foo'
        item_pb = array_pb.add()
        item_pb.string_value = 'Bar'
        items = self._callFUT(pb)
        self.assertEqual(items, ['Foo', 'Bar'])

    def test_geo_point(self):
        from google.type import latlng_pb2
        from google.cloud.datastore._generated import entity_pb2
        from google.cloud.datastore.helpers import GeoPoint

        lat = -3.14
        lng = 13.37
        geo_pt_pb = latlng_pb2.LatLng(latitude=lat, longitude=lng)
        pb = entity_pb2.Value(geo_point_value=geo_pt_pb)
        result = self._callFUT(pb)
        self.assertIsInstance(result, GeoPoint)
        self.assertEqual(result.latitude, lat)
        self.assertEqual(result.longitude, lng)

    def test_null(self):
        from google.protobuf import struct_pb2
        from google.cloud.datastore._generated import entity_pb2

        pb = entity_pb2.Value(null_value=struct_pb2.NULL_VALUE)
        result = self._callFUT(pb)
        self.assertIsNone(result)

    def test_unknown(self):
        from google.cloud.datastore._generated import entity_pb2

        pb = entity_pb2.Value()
        with self.assertRaises(ValueError):
            self._callFUT(pb)


class Test_set_protobuf_value(unittest.TestCase):

    def _callFUT(self, value_pb, val):
        from google.cloud.datastore.helpers import _set_protobuf_value

        return _set_protobuf_value(value_pb, val)

    def _makePB(self):
        from google.cloud.datastore._generated import entity_pb2
        return entity_pb2.Value()

    def test_datetime(self):
        import calendar
        import datetime
        from google.cloud._helpers import UTC

        pb = self._makePB()
        micros = 4375
        utc = datetime.datetime(2014, 9, 16, 10, 19, 32, micros, UTC)
        self._callFUT(pb, utc)
        value = pb.timestamp_value
        self.assertEqual(value.seconds, calendar.timegm(utc.timetuple()))
        self.assertEqual(value.nanos, 1000 * micros)

    def test_key(self):
        from google.cloud.datastore.key import Key

        pb = self._makePB()
        key = Key('KIND', 1234, project='PROJECT')
        self._callFUT(pb, key)
        value = pb.key_value
        self.assertEqual(value, key.to_protobuf())

    def test_none(self):
        pb = self._makePB()
        self._callFUT(pb, None)
        self.assertEqual(pb.WhichOneof('value_type'), 'null_value')

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
        else:  # pragma: NO COVER Python 3
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
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _property_tuples

        pb = self._makePB()
        entity = Entity()
        self._callFUT(pb, entity)
        value = pb.entity_value
        self.assertEqual(value.key.SerializeToString(), b'')
        self.assertEqual(len(list(_property_tuples(value))), 0)

    def test_entity_w_key(self):
        from google.cloud.datastore.entity import Entity
        from google.cloud.datastore.helpers import _property_tuples
        from google.cloud.datastore.key import Key

        name = 'foo'
        value = u'Foo'
        pb = self._makePB()
        key = Key('KIND', 123, project='PROJECT')
        entity = Entity(key=key)
        entity[name] = value
        self._callFUT(pb, entity)
        entity_pb = pb.entity_value
        self.assertEqual(entity_pb.key, key.to_protobuf())

        prop_dict = dict(_property_tuples(entity_pb))
        self.assertEqual(len(prop_dict), 1)
        self.assertEqual(list(prop_dict.keys()), [name])
        self.assertEqual(prop_dict[name].string_value, value)

    def test_array(self):
        pb = self._makePB()
        values = [u'a', 0, 3.14]
        self._callFUT(pb, values)
        marshalled = pb.array_value.values
        self.assertEqual(len(marshalled), len(values))
        self.assertEqual(marshalled[0].string_value, values[0])
        self.assertEqual(marshalled[1].integer_value, values[1])
        self.assertEqual(marshalled[2].double_value, values[2])

    def test_geo_point(self):
        from google.type import latlng_pb2
        from google.cloud.datastore.helpers import GeoPoint

        pb = self._makePB()
        lat = 9.11
        lng = 3.337
        geo_pt = GeoPoint(latitude=lat, longitude=lng)
        geo_pt_pb = latlng_pb2.LatLng(latitude=lat, longitude=lng)
        self._callFUT(pb, geo_pt)
        self.assertEqual(pb.geo_point_value, geo_pt_pb)


class Test__get_meaning(unittest.TestCase):

    def _callFUT(self, *args, **kwargs):
        from google.cloud.datastore.helpers import _get_meaning
        return _get_meaning(*args, **kwargs)

    def test_no_meaning(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        result = self._callFUT(value_pb)
        self.assertIsNone(result)

    def test_single(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        value_pb.meaning = meaning = 22
        value_pb.string_value = u'hi'
        result = self._callFUT(value_pb)
        self.assertEqual(meaning, result)

    def test_empty_array_value(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        value_pb.array_value.values.add()
        value_pb.array_value.values.pop()

        result = self._callFUT(value_pb, is_list=True)
        self.assertEqual(None, result)

    def test_array_value(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        meaning = 9
        sub_value_pb1 = value_pb.array_value.values.add()
        sub_value_pb2 = value_pb.array_value.values.add()

        sub_value_pb1.meaning = sub_value_pb2.meaning = meaning
        sub_value_pb1.string_value = u'hi'
        sub_value_pb2.string_value = u'bye'

        result = self._callFUT(value_pb, is_list=True)
        self.assertEqual(meaning, result)

    def test_array_value_multiple_meanings(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        meaning1 = 9
        meaning2 = 10
        sub_value_pb1 = value_pb.array_value.values.add()
        sub_value_pb2 = value_pb.array_value.values.add()

        sub_value_pb1.meaning = meaning1
        sub_value_pb2.meaning = meaning2
        sub_value_pb1.string_value = u'hi'
        sub_value_pb2.string_value = u'bye'

        result = self._callFUT(value_pb, is_list=True)
        self.assertEqual(result, [meaning1, meaning2])

    def test_array_value_meaning_partially_unset(self):
        from google.cloud.datastore._generated import entity_pb2

        value_pb = entity_pb2.Value()
        meaning1 = 9
        sub_value_pb1 = value_pb.array_value.values.add()
        sub_value_pb2 = value_pb.array_value.values.add()

        sub_value_pb1.meaning = meaning1
        sub_value_pb1.string_value = u'hi'
        sub_value_pb2.string_value = u'bye'

        result = self._callFUT(value_pb, is_list=True)
        self.assertEqual(result, [meaning1, None])


class TestGeoPoint(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore.helpers import GeoPoint
        return GeoPoint

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        lat = 81.2
        lng = 359.9999
        geo_pt = self._makeOne(lat, lng)
        self.assertEqual(geo_pt.latitude, lat)
        self.assertEqual(geo_pt.longitude, lng)

    def test_to_protobuf(self):
        from google.type import latlng_pb2

        lat = 0.0001
        lng = 20.03
        geo_pt = self._makeOne(lat, lng)
        result = geo_pt.to_protobuf()
        geo_pt_pb = latlng_pb2.LatLng(latitude=lat, longitude=lng)
        self.assertEqual(result, geo_pt_pb)

    def test___eq__(self):
        lat = 0.0001
        lng = 20.03
        geo_pt1 = self._makeOne(lat, lng)
        geo_pt2 = self._makeOne(lat, lng)
        self.assertEqual(geo_pt1, geo_pt2)

    def test___eq__type_differ(self):
        lat = 0.0001
        lng = 20.03
        geo_pt1 = self._makeOne(lat, lng)
        geo_pt2 = object()
        self.assertNotEqual(geo_pt1, geo_pt2)

    def test___ne__same_value(self):
        lat = 0.0001
        lng = 20.03
        geo_pt1 = self._makeOne(lat, lng)
        geo_pt2 = self._makeOne(lat, lng)
        comparison_val = (geo_pt1 != geo_pt2)
        self.assertFalse(comparison_val)

    def test___ne__(self):
        geo_pt1 = self._makeOne(0.0, 1.0)
        geo_pt2 = self._makeOne(2.0, 3.0)
        self.assertNotEqual(geo_pt1, geo_pt2)
