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


class TestDataset(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_missing_dataset_id(self):
        self.assertRaises(TypeError, self._makeOne)

    def test_ctor_defaults(self):
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertEqual(dataset.connection(), None)

    def test_ctor_explicit(self):
        DATASET_ID = 'DATASET'
        CONNECTION = object()
        dataset = self._makeOne(DATASET_ID, CONNECTION)
        self.assertEqual(dataset.id(), DATASET_ID)
        self.assertTrue(dataset.connection() is CONNECTION)

    def test_query_factory(self):
        from gcloud.datastore.query import Query
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        query = dataset.query()
        self.assertIsInstance(query, Query)
        self.assertTrue(query.dataset() is dataset)

    def test_entity_factory_defaults(self):
        from gcloud.datastore.entity import Entity
        DATASET_ID = 'DATASET'
        KIND = 'KIND'
        dataset = self._makeOne(DATASET_ID)
        entity = dataset.entity(KIND)
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.kind(), KIND)
        self.assertEqual(sorted(entity.exclude_from_indexes()), [])

    def test_entity_factory_explicit(self):
        from gcloud.datastore.entity import Entity
        DATASET_ID = 'DATASET'
        KIND = 'KIND'
        dataset = self._makeOne(DATASET_ID)
        entity = dataset.entity(KIND, ['foo', 'bar'])
        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.kind(), KIND)
        self.assertEqual(sorted(entity.exclude_from_indexes()), ['bar', 'foo'])

    def test_transaction_factory(self):
        from gcloud.datastore.transaction import Transaction
        DATASET_ID = 'DATASET'
        dataset = self._makeOne(DATASET_ID)
        transaction = dataset.transaction()
        self.assertIsInstance(transaction, Transaction)
        self.assertTrue(transaction.dataset() is dataset)

    def test_get_entity_miss(self):
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=[{'kind': 'Kind', 'id': 1234}])
        self.assertEqual(dataset.get_entity(key), None)

    def test_get_entity_hit(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH)
        result = dataset.get_entity(key)
        key = result.key()
        self.assertEqual(key._dataset_id, DATASET_ID)
        self.assertEqual(key.path(), PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_get_entity_path(self):
        from gcloud.datastore.connection import datastore_pb
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = self._makeOne(DATASET_ID, connection)
        result = dataset.get_entity([KIND, ID])
        key = result.key()
        self.assertEqual(key._dataset_id, DATASET_ID)
        self.assertEqual(key.path(), PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_get_entity_odd_nonetype(self):
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        with self.assertRaises(ValueError):
            dataset.get_entity([KIND])
        with self.assertRaises(TypeError):
            dataset.get_entity(None)

    def test_get_entities_miss(self):
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=[{'kind': 'Kind', 'id': 1234}])
        self.assertEqual(dataset.get_entities([key]), [])

    def test_get_entities_miss_w_missing(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        missed = datastore_pb.Entity()
        missed.key.partition_id.dataset_id = DATASET_ID
        path_element = missed.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        connection = _Connection()
        connection._missing = [missed]
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH, dataset_id=DATASET_ID)
        missing = []
        entities = dataset.get_entities([key], missing=missing)
        self.assertEqual(entities, [])
        self.assertEqual([missed.key().to_protobuf() for missed in missing],
                         [key.to_protobuf()])

    def test_get_entities_miss_w_deferred(self):
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        connection = _Connection()
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH, dataset_id=DATASET_ID)
        connection._deferred = [key.to_protobuf()]
        deferred = []
        entities = dataset.get_entities([key], deferred=deferred)
        self.assertEqual(entities, [])
        self.assertEqual([def_key.to_protobuf() for def_key in deferred],
                         [key.to_protobuf()])

    def test_get_entities_hit(self):
        from gcloud.datastore.connection import datastore_pb
        from gcloud.datastore.key import Key
        DATASET_ID = 'DATASET'
        KIND = 'Kind'
        ID = 1234
        PATH = [{'kind': KIND, 'id': ID}]
        entity_pb = datastore_pb.Entity()
        entity_pb.key.partition_id.dataset_id = DATASET_ID
        path_element = entity_pb.key.path_element.add()
        path_element.kind = KIND
        path_element.id = ID
        prop = entity_pb.property.add()
        prop.name = 'foo'
        prop.value.string_value = 'Foo'
        connection = _Connection(entity_pb)
        dataset = self._makeOne(DATASET_ID, connection)
        key = Key(path=PATH)
        result, = dataset.get_entities([key])
        key = result.key()
        self.assertEqual(key._dataset_id, DATASET_ID)
        self.assertEqual(key.path(), PATH)
        self.assertEqual(list(result), ['foo'])
        self.assertEqual(result['foo'], 'Foo')

    def test_allocate_ids(self):
        from gcloud.datastore.test_entity import _Key

        INCOMPLETE_KEY = _Key()
        PROTO_ID = object()
        INCOMPLETE_KEY._key = _KeyProto(PROTO_ID)
        INCOMPLETE_KEY._partial = True

        CONNECTION = _Connection()
        NUM_IDS = 2
        DATASET_ID = 'foo'
        DATASET = self._makeOne(DATASET_ID, connection=CONNECTION)
        result = DATASET.allocate_ids(INCOMPLETE_KEY, NUM_IDS)

        # Check the IDs returned match.
        self.assertEqual([key._id for key in result], range(NUM_IDS))

        # Check connection is called correctly.
        self.assertEqual(CONNECTION._called_dataset_id, DATASET_ID)
        self.assertEqual(len(CONNECTION._called_key_pbs), NUM_IDS)

        # Check the IDs passed to Connection.allocate_ids.
        key_paths = [key_pb.path_element[-1].id
                     for key_pb in CONNECTION._called_key_pbs]
        self.assertEqual(key_paths, [PROTO_ID] * NUM_IDS)

    def test_allocate_ids_with_complete(self):
        from gcloud.datastore.test_entity import _Key

        COMPLETE_KEY = _Key()
        DATASET = self._makeOne(None)
        self.assertRaises(ValueError, DATASET.allocate_ids,
                          COMPLETE_KEY, 2)


class _Connection(object):
    _called_with = None
    _missing = _deferred = ()

    def __init__(self, *result):
        self._result = list(result)

    def lookup(self, **kw):
        self._called_with = kw
        missing = kw.pop('missing', None)
        if missing is not None:
            missing.extend(self._missing)
        deferred = kw.pop('deferred', None)
        if deferred is not None:
            deferred.extend(self._deferred)
        return self._result

    def allocate_ids(self, dataset_id, key_pbs):
        self._called_dataset_id = dataset_id
        self._called_key_pbs = key_pbs
        num_pbs = len(key_pbs)
        return [_KeyProto(i) for i in range(num_pbs)]


class _PathElementProto(object):

    def __init__(self, _id):
        self.id = _id


class _KeyProto(object):

    def __init__(self, id_):
        self.path_element = [_PathElementProto(id_)]
