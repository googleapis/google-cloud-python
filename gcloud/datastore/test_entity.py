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

_DATASET_ID = 'DATASET'
_KIND = 'KIND'
_ID = 1234


class TestEntity(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.entity import Entity
        return Entity

    def _makeOne(self, key=None, exclude_from_indexes=()):
        klass = self._getTargetClass()
        return klass(key=key, exclude_from_indexes=exclude_from_indexes)

    def test_ctor_defaults(self):
        klass = self._getTargetClass()
        entity = klass()
        self.assertEqual(entity.key, None)
        self.assertEqual(entity.kind, None)
        self.assertEqual(sorted(entity.exclude_from_indexes), [])

    def test_ctor_explicit(self):
        _EXCLUDE_FROM_INDEXES = ['foo', 'bar']
        key = _Key()
        entity = self._makeOne(
            key=key, exclude_from_indexes=_EXCLUDE_FROM_INDEXES)
        self.assertEqual(sorted(entity.exclude_from_indexes),
                         sorted(_EXCLUDE_FROM_INDEXES))

    def test_ctor_bad_exclude_from_indexes(self):
        BAD_EXCLUDE_FROM_INDEXES = object()
        key = _Key()
        self.assertRaises(TypeError, self._makeOne, key=key,
                          exclude_from_indexes=BAD_EXCLUDE_FROM_INDEXES)

    def test___eq_____ne___w_non_entity(self):
        from gcloud.datastore.key import Key
        key = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity = self._makeOne(key=key)
        self.assertFalse(entity == object())
        self.assertTrue(entity != object())

    def test___eq_____ne___w_different_keys(self):
        from gcloud.datastore.key import Key
        _ID1 = 1234
        _ID2 = 2345
        key1 = Key(_KIND, _ID1, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key1)
        key2 = Key(_KIND, _ID2, dataset_id=_DATASET_ID)
        entity2 = self._makeOne(key=key2)
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys(self):
        from gcloud.datastore.key import Key
        key1 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key1)
        key2 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity2 = self._makeOne(key=key2)
        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_different_props(self):
        from gcloud.datastore.key import Key
        key1 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key1)
        entity1['foo'] = 'Foo'
        key2 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity2 = self._makeOne(key=key2)
        entity1['bar'] = 'Bar'
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_equiv_keys_as_value(self):
        from gcloud.datastore.key import Key
        key1 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        key2 = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key1)
        entity1['some_key'] = key1
        entity2 = self._makeOne(key=key1)
        entity2['some_key'] = key2
        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_diff_keys_as_value(self):
        from gcloud.datastore.key import Key
        _ID1 = 1234
        _ID2 = 2345
        key1 = Key(_KIND, _ID1, dataset_id=_DATASET_ID)
        key2 = Key(_KIND, _ID2, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key1)
        entity1['some_key'] = key1
        entity2 = self._makeOne(key=key1)
        entity2['some_key'] = key2
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_equiv_entities_as_value(self):
        from gcloud.datastore.key import Key
        key = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key)
        sub1 = self._makeOne()
        sub1.update({'foo': 'Foo'})
        entity1['some_entity'] = sub1
        entity2 = self._makeOne(key=key)
        sub2 = self._makeOne()
        sub2.update({'foo': 'Foo'})
        entity2['some_entity'] = sub2
        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 != entity2)

    def test___eq_____ne___w_same_keys_props_w_diff_entities_as_value(self):
        from gcloud.datastore.key import Key
        key = Key(_KIND, _ID, dataset_id=_DATASET_ID)
        entity1 = self._makeOne(key=key)
        sub1 = self._makeOne()
        sub1.update({'foo': 'Foo'})
        entity1['some_entity'] = sub1
        entity2 = self._makeOne(key=key)
        sub2 = self._makeOne()
        sub2.update({'foo': 'Bar'})
        entity2['some_entity'] = sub2
        self.assertFalse(entity1 == entity2)
        self.assertTrue(entity1 != entity2)

    def test___repr___no_key_empty(self):
        entity = self._makeOne()
        self.assertEqual(repr(entity), '<Entity {}>')

    def test___repr___w_key_non_empty(self):
        key = _Key()
        key._path = '/bar/baz'
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        self.assertEqual(repr(entity), "<Entity/bar/baz {'foo': 'Foo'}>")


class _Key(object):
    _MARKER = object()
    _key = 'KEY'
    _partial = False
    _path = None
    _id = None
    _stored = None

    def __init__(self, dataset_id=_DATASET_ID):
        self.dataset_id = dataset_id

    @property
    def path(self):
        return self._path
