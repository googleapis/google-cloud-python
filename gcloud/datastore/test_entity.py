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

    def setUp(self):
        from gcloud.datastore import _implicit_environ
        self._replaced_dataset_id = _implicit_environ.DATASET_ID
        _implicit_environ.DATASET_ID = None

    def tearDown(self):
        from gcloud.datastore import _implicit_environ
        _implicit_environ.DATASET_ID = self._replaced_dataset_id

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
