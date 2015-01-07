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

    def test__must_key_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne()
        self.assertRaises(NoKey, getattr, entity, '_must_key')

    def test_reload_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne()
        entity['foo'] = 'Foo'
        self.assertRaises(NoKey, entity.reload)

    def test_reload_miss(self):
        key = _Key()
        key._stored = None  # Explicit miss.
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        # Does not raise, does not update on miss.
        entity.reload()
        self.assertEqual(entity['foo'], 'Foo')

    def test_reload_hit(self):
        key = _Key()
        NEW_VAL = 'Baz'
        key._stored = {'foo': NEW_VAL}
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        entity.reload()
        self.assertEqual(entity['foo'], NEW_VAL)
        self.assertEqual(entity.keys(), ['foo'])

    def test_save_no_key(self):
        from gcloud.datastore.entity import NoKey

        entity = self._makeOne()
        entity['foo'] = 'Foo'
        self.assertRaises(NoKey, entity.save)

    def test_save_wo_transaction_wo_auto_id_wo_returned_key(self):
        connection = _Connection()
        key = _Key()
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        entity.save(connection=connection)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}, ()))
        self.assertEqual(key._path, None)

    def test_save_w_transaction_wo_partial_key(self):
        connection = _Connection()
        transaction = connection._transaction = _Transaction()
        key = _Key()
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        entity.save(connection=connection)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}, ()))
        self.assertEqual(transaction._added, ())
        self.assertEqual(key._path, None)

    def test_save_w_transaction_w_partial_key(self):
        connection = _Connection()
        transaction = connection._transaction = _Transaction()
        key = _Key()
        key._partial = True
        entity = self._makeOne(key=key)
        entity['foo'] = 'Foo'
        entity.save(connection=connection)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved,
                         (_DATASET_ID, 'KEY', {'foo': 'Foo'}, ()))
        self.assertEqual(transaction._added, (entity,))
        self.assertEqual(key._path, None)

    def test_save_w_returned_key_exclude_from_indexes(self):
        from gcloud.datastore import datastore_v1_pb2 as datastore_pb
        from gcloud.datastore.key import Key

        key_pb = datastore_pb.Key()
        key_pb.partition_id.dataset_id = _DATASET_ID
        key_pb.path_element.add(kind=_KIND, id=_ID)
        connection = _Connection()
        connection._save_result = (True, _ID)
        key = Key('KIND', dataset_id=_DATASET_ID)
        entity = self._makeOne(key=key, exclude_from_indexes=['foo'])
        entity['foo'] = 'Foo'
        entity.save(connection=connection)
        self.assertEqual(entity['foo'], 'Foo')
        self.assertEqual(connection._saved[0], _DATASET_ID)
        self.assertEqual(connection._saved[1], key.to_protobuf())
        self.assertEqual(connection._saved[2], {'foo': 'Foo'})
        self.assertEqual(connection._saved[3], ('foo',))
        self.assertEqual(len(connection._saved), 4)

        self.assertEqual(entity.key._path, [{'kind': _KIND, 'id': _ID}])

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

    def to_protobuf(self):
        return self._key

    @property
    def is_partial(self):
        return self._partial

    @property
    def path(self):
        return self._path

    def get(self, connection=None):
        self._connection_used = connection
        return self._stored


class _Connection(object):
    _transaction = _saved = _deleted = None
    _save_result = (False, None)

    def transaction(self):
        return self._transaction

    def save_entity(self, dataset_id, key_pb, properties,
                    exclude_from_indexes=()):
        self._saved = (dataset_id, key_pb, properties,
                       tuple(exclude_from_indexes))
        return self._save_result


class _Transaction(object):
    _added = ()

    def __nonzero__(self):
        return True
    __bool__ = __nonzero__

    def add_auto_id_entity(self, entity):
        self._added += (entity,)
