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

_PROJECT = 'PROJECT'
_KIND = 'KIND'
_ID = 1234


class TestEntity(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.entity import Entity
        return Entity

    def _make_one(self, key=None, exclude_from_indexes=()):
        klass = self._get_target_class()
        return klass(key=key, exclude_from_indexes=exclude_from_indexes)

    def test_ctor_defaults(self):
        klass = self._get_target_class()
        entity = klass()
        self.assertIsNone(entity.key)
        self.assertIsNone(entity.kind)
        self.assertEqual(sorted(entity.exclude_from_indexes), [])

    def test_ctor_explicit(self):
        _EXCLUDE_FROM_INDEXES = ['foo', 'bar']
        key = _Key()
        entity = self._make_one(
            key=key, exclude_from_indexes=_EXCLUDE_FROM_INDEXES)
        self.assertEqual(sorted(entity.exclude_from_indexes),
                         sorted(_EXCLUDE_FROM_INDEXES))

    def test_ctor_bad_exclude_from_indexes(self):
        BAD_EXCLUDE_FROM_INDEXES = object()
        key = _Key()
        self.assertRaises(TypeError, self._make_one, key=key,
                          exclude_from_indexes=BAD_EXCLUDE_FROM_INDEXES)

    def test___eq_____ne___w_non_entity(self):
        from google.cloud.datastore.key import Key
        key = Key(_KIND, _ID, project=_PROJECT)
        entity = self._make_one(key=key)
        self.assertFalse(entity == object())
        self.assertTrue(entity != object())

    def test___eq_____ne___w_different_keys(self):
        from google.cloud.datastore.key import Key
        _ID1 = 1234
        _ID2 = 2345
        key1 = Key(_KIND, _ID1, project=_PROJECT)
        entity1 = self._make_one(key=key1)
        key2 = Key(_KIND, _ID2, project=_PROJECT)
        entity2 = self._make_one(key=key2)
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys(self):
        from google.cloud.datastore.key import Key

        name = 'foo'
        value = 42
        meaning = 9

        key1 = Key(_KIND, _ID, project=_PROJECT)
        entity1 = self._make_one(key=key1, exclude_from_indexes=(name,))
        entity1[name] = value
        entity1._meanings[name] = (meaning, value)

        key2 = Key(_KIND, _ID, project=_PROJECT)
        entity2 = self._make_one(key=key2, exclude_from_indexes=(name,))
        entity2[name] = value
        entity2._meanings[name] = (meaning, value)

        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_different_props(self):
        from google.cloud.datastore.key import Key
        key1 = Key(_KIND, _ID, project=_PROJECT)
        entity1 = self._make_one(key=key1)
        entity1['foo'] = 'Foo'
        key2 = Key(_KIND, _ID, project=_PROJECT)
        entity2 = self._make_one(key=key2)
        entity1['bar'] = 'Bar'
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_equiv_keys_as_value(self):
        from google.cloud.datastore.key import Key
        key1 = Key(_KIND, _ID, project=_PROJECT)
        key2 = Key(_KIND, _ID, project=_PROJECT)
        entity1 = self._make_one(key=key1)
        entity1['some_key'] = key1
        entity2 = self._make_one(key=key1)
        entity2['some_key'] = key2
        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_diff_keys_as_value(self):
        from google.cloud.datastore.key import Key
        _ID1 = 1234
        _ID2 = 2345
        key1 = Key(_KIND, _ID1, project=_PROJECT)
        key2 = Key(_KIND, _ID2, project=_PROJECT)
        entity1 = self._make_one(key=key1)
        entity1['some_key'] = key1
        entity2 = self._make_one(key=key1)
        entity2['some_key'] = key2
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_equiv_entities_as_value(self):
        from google.cloud.datastore.key import Key
        key = Key(_KIND, _ID, project=_PROJECT)
        entity1 = self._make_one(key=key)
        sub1 = self._make_one()
        sub1.update({'foo': 'Foo'})
        entity1['some_entity'] = sub1
        entity2 = self._make_one(key=key)
        sub2 = self._make_one()
        sub2.update({'foo': 'Foo'})
        entity2['some_entity'] = sub2
        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_diff_entities_as_value(self):
        from google.cloud.datastore.key import Key
        key = Key(_KIND, _ID, project=_PROJECT)
        entity1 = self._make_one(key=key)
        sub1 = self._make_one()
        sub1.update({'foo': 'Foo'})
        entity1['some_entity'] = sub1
        entity2 = self._make_one(key=key)
        sub2 = self._make_one()
        sub2.update({'foo': 'Bar'})
        entity2['some_entity'] = sub2
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test__eq__same_value_different_exclude(self):
        from google.cloud.datastore.key import Key

        name = 'foo'
        value = 42
        key = Key(_KIND, _ID, project=_PROJECT)

        entity1 = self._make_one(key=key, exclude_from_indexes=(name,))
        entity1[name] = value

        entity2 = self._make_one(key=key, exclude_from_indexes=())
        entity2[name] = value

        self.assertFalse(entity1 == entity2)

    def test__eq__same_value_different_meanings(self):
        from google.cloud.datastore.key import Key

        name = 'foo'
        value = 42
        meaning = 9
        key = Key(_KIND, _ID, project=_PROJECT)

        entity1 = self._make_one(key=key, exclude_from_indexes=(name,))
        entity1[name] = value

        entity2 = self._make_one(key=key, exclude_from_indexes=(name,))
        entity2[name] = value
        entity2._meanings[name] = (meaning, value)

        self.assertFalse(entity1 == entity2)

    def test___repr___no_key_empty(self):
        entity = self._make_one()
        self.assertEqual(repr(entity), '<Entity {}>')

    def test___repr___w_key_non_empty(self):
        key = _Key()
        flat_path = ('bar', 12, 'baz', 'himom')
        key._flat_path = flat_path
        entity = self._make_one(key=key)
        entity_vals = {'foo': 'Foo'}
        entity.update(entity_vals)
        expected = '<Entity%s %s>' % (flat_path, entity_vals)
        self.assertEqual(repr(entity), expected)


class _Key(object):
    _MARKER = object()
    _key = 'KEY'
    _partial = False
    _path = None
    _id = None
    _stored = None

    def __init__(self, project=_PROJECT):
        self.project = project
