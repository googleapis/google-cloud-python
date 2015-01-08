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
        from gcloud.datastore.datastore_v1_pb2 import Mutation
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
        from gcloud.datastore.datastore_v1_pb2 import Mutation
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

    def test_add_auto_id_entity_w_partial_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        key = entity.key = _Key(_Entity)
        key._partial = True

        batch.add_auto_id_entity(entity)

        self.assertEqual(batch._auto_id_entities, [entity])

    def test_add_auto_id_entity_w_completed_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        key = entity.key = _Key(_Entity)

        self.assertRaises(ValueError, batch.add_auto_id_entity, entity)

    def test_put_entity_wo_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)

        self.assertRaises(ValueError, batch.put, _Entity())

    def test_put_entity_w_partial_key(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)
        key._partial = True

        batch.put(entity)

        self.assertEqual(
            connection._saved,
            (_DATASET, key._key, _PROPERTIES, (), batch.mutation))
        self.assertEqual(batch._auto_id_entities, [entity])

    def test_put_entity_w_completed_key(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)

        batch.put(entity)

        self.assertEqual(
            connection._saved,
            (_DATASET, key._key, _PROPERTIES, (), batch.mutation))

    def test_delete_w_partial_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key(_DATASET)
        key._partial = True

        self.assertRaises(ValueError, batch.delete, key)

    def test_delete_w_completed_key(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        key = _Key(_DATASET)

        batch.delete(key)

        self.assertEqual(
            connection._deleted,
            (_DATASET, [key._key], batch.mutation))

    def test_commit(self):
        _DATASET = 'DATASET'
        connection = _Connection()
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)

        batch.commit()

        self.assertEqual(connection._committed, (_DATASET, batch.mutation))

    def test_commit_w_auto_id_entities(self):
        _DATASET = 'DATASET'
        _NEW_ID = 1234
        connection = _Connection(_NEW_ID)
        batch = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity({})
        key = entity.key = _Key(_DATASET)
        key._partial = True
        batch._auto_id_entities.append(entity)

        batch.commit()

        self.assertEqual(connection._committed, (_DATASET, batch.mutation))
        self.assertFalse(key._partial)
        self.assertEqual(key._id, _NEW_ID)

    def test_as_context_mgr_wo_error(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)

        with self._makeOne(dataset_id=_DATASET,
                           connection=connection) as batch:
            batch.put(entity)

        self.assertEqual(
            connection._saved,
            (_DATASET, key._key, _PROPERTIES, (), batch.mutation))
        self.assertEqual(connection._committed, (_DATASET, batch.mutation))

    def test_as_context_mgr_w_error(self):
        _DATASET = 'DATASET'
        _PROPERTIES = {'foo': 'bar'}
        connection = _Connection()
        entity = _Entity(_PROPERTIES)
        key = entity.key = _Key(_DATASET)

        try:
            with self._makeOne(dataset_id=_DATASET,
                               connection=connection) as batch:
                batch.put(entity)
                raise ValueError("testing")
        except ValueError:
            pass

        self.assertEqual(
            connection._saved,
            (_DATASET, key._key, _PROPERTIES, (), batch.mutation))
        self.assertEqual(connection._committed, None)


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
    _committed = _saved = _deleted = None
    _save_result = (False, None)

    def __init__(self, *new_keys):
        self._commit_result = _CommitResult(*new_keys)

    def save_entity(self, dataset_id, key_pb, properties,
                    exclude_from_indexes=(), mutation=None):
        self._saved = (dataset_id, key_pb, properties,
                       tuple(exclude_from_indexes), mutation)
        return self._save_result

    def delete_entities(self, dataset_id, key_pbs, mutation=None):
        self._deleted = (dataset_id, key_pbs, mutation)

    def commit(self, dataset_id, mutation):
        self._committed = (dataset_id, mutation)
        return self._commit_result


class _Entity(dict):
    key = None
    exclude_from_indexes = ()


class _Key(object):
    _MARKER = object()
    _key = 'KEY'
    _partial = False
    _path = None
    _id = None
    _stored = None

    def __init__(self, dataset_id):
        self.dataset_id = dataset_id

    @property
    def is_partial(self):
        return self._partial

    def to_protobuf(self):
        return self._key

    def completed_key(self, new_id):
        assert self._partial
        self._id = new_id
        self._partial = False
