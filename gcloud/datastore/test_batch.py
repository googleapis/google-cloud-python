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


class Test_Batches(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.batch import _Batches

        return _Batches

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        batch1, batch2 = object(), object()
        batches = self._makeOne()
        self.assertEqual(list(batches), [])
        self.assertTrue(batches.top is None)
        batches.push(batch1)
        self.assertTrue(batches.top is batch1)
        batches.push(batch2)
        self.assertTrue(batches.top is batch2)
        popped = batches.pop()
        self.assertTrue(popped is batch2)
        self.assertTrue(batches.top is batch1)
        self.assertEqual(list(batches), [batch1])
        popped = batches.pop()
        self.assertTrue(batches.top is None)
        self.assertEqual(list(batches), [])


class TestBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.batch import Batch

        return Batch

    def _makeOne(self, dataset_id=None, connection=None):
        return self._getTargetClass()(dataset_id=dataset_id,
                                      connection=connection)

    def test_ctor_missing_required(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ

        with _Monkey(_implicit_environ,
                     DATASET_ID=None,
                     CONNECTION=None):
            self.assertRaises(ValueError, self._makeOne)
            self.assertRaises(ValueError, self._makeOne, dataset_id=object())
            self.assertRaises(ValueError, self._makeOne, connection=object())

    def test_ctor_explicit(self):
        from gcloud.datastore._datastore_v1_pb2 import Mutation
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)

        self.assertEqual(batch.dataset_id, _DATASET)
        self.assertEqual(batch.connection, connection)
        self.assertTrue(isinstance(batch.mutation, Mutation))
        self.assertEqual(batch._auto_id_entities, [])

    def test_ctor_implicit(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ
        from gcloud.datastore._datastore_v1_pb2 import Mutation
        DATASET_ID = 'DATASET'
        CONNECTION = _Connection()

        with _Monkey(_implicit_environ,
                     DATASET_ID=DATASET_ID,
                     CONNECTION=CONNECTION):
            batch = self._makeOne()

        self.assertEqual(batch.dataset_id, DATASET_ID)
        self.assertEqual(batch.connection, CONNECTION)
        self.assertTrue(isinstance(batch.mutation, Mutation))
        self.assertEqual(batch._auto_id_entities, [])

    def test_current(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch1 = self._makeOne(_DATASET, connection)
        batch2 = self._makeOne(_DATASET, connection)
        self.assertTrue(batch1.current() is None)
        self.assertTrue(batch2.current() is None)
        with batch1:
            self.assertTrue(batch1.current() is batch1)
            self.assertTrue(batch2.current() is batch1)
            with batch2:
                self.assertTrue(batch1.current() is batch2)
                self.assertTrue(batch2.current() is batch2)
            self.assertTrue(batch1.current() is batch1)
            self.assertTrue(batch2.current() is batch1)
        self.assertTrue(batch1.current() is None)
        self.assertTrue(batch2.current() is None)

    def test_add_auto_id_entity_w_partial_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        key = entity.key = _Key(_DATASET)
        key._id = None

        batch.add_auto_id_entity(entity)

        self.assertEqual(batch._auto_id_entities, [entity])

    def test_add_auto_id_entity_w_completed_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        entity.key = _Key(_DATASET)

        self.assertRaises(ValueError, batch.add_auto_id_entity, entity)

    def test_put_entity_wo_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)

        self.assertRaises(ValueError, batch.put, _Entity())

    def test_put_entity_w_key_wrong_dataset_id(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        entity.key = _Key('OTHER')

        self.assertRaises(ValueError, batch.put, entity)

    def test_put_entity_w_partial_key(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)
        key._id = None

        batch.put(entity)

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 1)
        self.assertEqual(insert_auto_ids[0].key, key._key)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 0)
        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 0)
        self.assertEqual(batch._auto_id_entities, [entity])

    def test_put_entity_w_completed_key(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {
            'foo': 'bar',
            'baz': 'qux',
            'spam': [1, 2, 3],
            'frotz': [],  # will be ignored
            }
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity(_PROPERTIES)
        entity.exclude_from_indexes = ('baz', 'spam')
        key = entity.key = _Key(_DATASET)

        batch.put(entity)

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 1)

        upsert = upserts[0]
        self.assertEqual(upsert.key, key._key)
        props = dict([(prop.name, prop.value) for prop in upsert.property])
        self.assertTrue(props['foo'].indexed)
        self.assertFalse(props['baz'].indexed)
        self.assertTrue(props['spam'].indexed)
        self.assertFalse(props['spam'].list_value[0].indexed)
        self.assertFalse(props['spam'].list_value[1].indexed)
        self.assertFalse(props['spam'].list_value[2].indexed)
        self.assertFalse('frotz' in props)

        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 0)

    def test_put_entity_w_completed_key_prefixed_dataset_id(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {
            'foo': 'bar',
            'baz': 'qux',
            'spam': [1, 2, 3],
            'frotz': [],  # will be ignored
            }
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity(_PROPERTIES)
        entity.exclude_from_indexes = ('baz', 'spam')
        key = entity.key = _Key('s~' + _DATASET)

        batch.put(entity)

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 1)

        upsert = upserts[0]
        self.assertEqual(upsert.key, key._key)
        props = dict([(prop.name, prop.value) for prop in upsert.property])
        self.assertTrue(props['foo'].indexed)
        self.assertFalse(props['baz'].indexed)
        self.assertTrue(props['spam'].indexed)
        self.assertFalse(props['spam'].list_value[0].indexed)
        self.assertFalse(props['spam'].list_value[1].indexed)
        self.assertFalse(props['spam'].list_value[2].indexed)
        self.assertFalse('frotz' in props)

        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 0)

    def test_delete_w_partial_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key(_DATASET)
        key._id = None

        self.assertRaises(ValueError, batch.delete, key)

    def test_delete_w_key_wrong_dataset_id(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key('OTHER')

        self.assertRaises(ValueError, batch.delete, key)

    def test_delete_w_completed_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key(_DATASET)

        batch.delete(key)

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 0)
        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 1)
        self.assertEqual(deletes[0], key._key)

    def test_delete_w_completed_key_w_prefixed_dataset_id(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key('s~' + _DATASET)

        batch.delete(key)

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 0)
        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 1)
        self.assertEqual(deletes[0], key._key)

    def test_commit(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)

        batch.commit()

        self.assertEqual(connection._committed, [(_DATASET, batch.mutation)])

    def test_commit_w_auto_id_entities(self):
        _DATASET = 'DATASET'
        _NEW_ID = 1234
        connection = _Connection(_NEW_ID)
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity({})
        key = entity.key = _Key(_DATASET)
        key._id = None
        batch._auto_id_entities.append(entity)

        batch.commit()

        self.assertEqual(connection._committed, [(_DATASET, batch.mutation)])
        self.assertFalse(key.is_partial)
        self.assertEqual(key._id, _NEW_ID)

    def test_as_context_mgr_wo_error(self):
        from gcloud.datastore.batch import _BATCHES
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)

        self.assertEqual(list(_BATCHES), [])

        with self._makeOne(dataset_id=_DATASET,
                           connection=connection) as batch:
            self.assertEqual(list(_BATCHES), [batch])
            batch.put(entity)

        self.assertEqual(list(_BATCHES), [])

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 1)
        self.assertEqual(upserts[0].key, key._key)
        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 0)
        self.assertEqual(connection._committed, [(_DATASET, batch.mutation)])

    def test_as_context_mgr_nested(self):
        from gcloud.datastore.batch import _BATCHES
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        entity1 = _Entity(_PROPERTIES)
        key1 = entity1.key = _Key(_DATASET)
        entity2 = _Entity(_PROPERTIES)
        key2 = entity2.key = _Key(_DATASET)

        self.assertEqual(list(_BATCHES), [])

        with self._makeOne(dataset_id=_DATASET,
                           connection=connection) as batch1:
            self.assertEqual(list(_BATCHES), [batch1])
            batch1.put(entity1)
            with self._makeOne(dataset_id=_DATASET,
                               connection=connection) as batch2:
                self.assertEqual(list(_BATCHES), [batch2, batch1])
                batch2.put(entity2)

            self.assertEqual(list(_BATCHES), [batch1])

        self.assertEqual(list(_BATCHES), [])

        insert_auto_ids = list(batch1.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch1.mutation.upsert)
        self.assertEqual(len(upserts), 1)
        self.assertEqual(upserts[0].key, key1._key)
        deletes = list(batch1.mutation.delete)
        self.assertEqual(len(deletes), 0)

        insert_auto_ids = list(batch2.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch2.mutation.upsert)
        self.assertEqual(len(upserts), 1)
        self.assertEqual(upserts[0].key, key2._key)
        deletes = list(batch2.mutation.delete)
        self.assertEqual(len(deletes), 0)

        self.assertEqual(connection._committed,
                         [(_DATASET, batch2.mutation),
                          (_DATASET, batch1.mutation)])

    def test_as_context_mgr_w_error(self):
        from gcloud.datastore.batch import _BATCHES
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)

        self.assertEqual(list(_BATCHES), [])

        try:
            with self._makeOne(dataset_id=_DATASET,
                               connection=connection) as batch:
                self.assertEqual(list(_BATCHES), [batch])
                batch.put(entity)
                raise ValueError("testing")
        except ValueError:
            pass

        self.assertEqual(list(_BATCHES), [])

        insert_auto_ids = list(batch.mutation.insert_auto_id)
        self.assertEqual(len(insert_auto_ids), 0)
        upserts = list(batch.mutation.upsert)
        self.assertEqual(len(upserts), 1)
        self.assertEqual(upserts[0].key, key._key)
        deletes = list(batch.mutation.delete)
        self.assertEqual(len(deletes), 0)
        self.assertEqual(connection._committed, [])


class _CommitResult(object):

    def __init__(self, *new_keys):
        self.insert_auto_id_key = [_KeyPB(key) for key in new_keys]


class _PathElementPB(object):

    def __init__(self, id):
        self.id = id


class _KeyPB(object):

    def __init__(self, id):
        self.path_element = [_PathElementPB(id)]


class _Connection(object):
    _marker = object()
    _save_result = (False, None)

    def __init__(self, *new_keys):
        self._commit_result = _CommitResult(*new_keys)
        self._committed = []

    def commit(self, dataset_id, mutation):
        self._committed.append((dataset_id, mutation))
        return self._commit_result


class _Entity(dict):
    key = None
    exclude_from_indexes = ()


class _Key(object):
    _MARKER = object()
    _kind = 'KIND'
    _key = 'KEY'
    _path = None
    _id = 1234
    _stored = None

    def __init__(self, dataset_id):
        self.dataset_id = dataset_id

    @property
    def is_partial(self):
        return self._id is None

    def to_protobuf(self):
        from gcloud.datastore import _datastore_v1_pb2
        key = self._key = _datastore_v1_pb2.Key()
        # Don't assign it, because it will just get ripped out
        # key.partition_id.dataset_id = self.dataset_id

        element = key.path_element.add()
        element.kind = self._kind
        if self._id is not None:
            element.id = self._id

        return key

    def completed_key(self, new_id):
        assert self.is_partial
        self._id = new_id
