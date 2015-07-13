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


class TestTransaction(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.transaction import Transaction
        return Transaction

    def _makeOne(self, client):
        return self._getTargetClass()(client)

    def test_ctor(self):
        from gcloud.datastore._datastore_v1_pb2 import Mutation

        _DATASET = 'DATASET'
        connection = _Connection()
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        self.assertEqual(xact.dataset_id, _DATASET)
        self.assertEqual(xact.connection, connection)
        self.assertEqual(xact.id, None)
        self.assertEqual(xact._status, self._getTargetClass()._INITIAL)
        self.assertTrue(isinstance(xact.mutation, Mutation))
        self.assertEqual(len(xact._auto_id_entities), 0)

    def test_current(self):
        from gcloud.datastore.test_client import _NoCommitBatch
        _DATASET = 'DATASET'
        connection = _Connection()
        client = _Client(_DATASET, connection)
        xact1 = self._makeOne(client)
        xact2 = self._makeOne(client)
        self.assertTrue(xact1.current() is None)
        self.assertTrue(xact2.current() is None)
        with xact1:
            self.assertTrue(xact1.current() is xact1)
            self.assertTrue(xact2.current() is xact1)
            with _NoCommitBatch(client):
                self.assertTrue(xact1.current() is None)
                self.assertTrue(xact2.current() is None)
            with xact2:
                self.assertTrue(xact1.current() is xact2)
                self.assertTrue(xact2.current() is xact2)
                with _NoCommitBatch(client):
                    self.assertTrue(xact1.current() is None)
                    self.assertTrue(xact2.current() is None)
            self.assertTrue(xact1.current() is xact1)
            self.assertTrue(xact2.current() is xact1)
        self.assertTrue(xact1.current() is None)
        self.assertTrue(xact2.current() is None)

    def test_begin(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact.begin()
        self.assertEqual(xact.id, 234)
        self.assertEqual(connection._begun, _DATASET)

    def test_begin_tombstoned(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact.begin()
        self.assertEqual(xact.id, 234)
        self.assertEqual(connection._begun, _DATASET)

        xact.rollback()
        self.assertEqual(xact.id, None)

        self.assertRaises(ValueError, xact.begin)

    def test_rollback(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact.begin()
        xact.rollback()
        self.assertEqual(xact.id, None)
        self.assertEqual(connection._rolled_back, (_DATASET, 234))

    def test_commit_no_auto_ids(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation, 234))
        self.assertEqual(xact.id, None)

    def test_commit_w_auto_ids(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 123
        connection = _Connection(234)
        connection._commit_result = _CommitResult(
            _make_key(_KIND, _ID, _DATASET))
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        entity = _Entity()
        xact.add_auto_id_entity(entity)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation, 234))
        self.assertEqual(xact.id, None)
        self.assertEqual(entity.key.path, [{'kind': _KIND, 'id': _ID}])

    def test_context_manager_no_raise(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact._mutation = mutation = object()
        with xact:
            self.assertEqual(xact.id, 234)
            self.assertEqual(connection._begun, _DATASET)
        self.assertEqual(connection._committed, (_DATASET, mutation, 234))
        self.assertEqual(xact.id, None)

    def test_context_manager_w_raise(self):

        class Foo(Exception):
            pass

        _DATASET = 'DATASET'
        connection = _Connection(234)
        client = _Client(_DATASET, connection)
        xact = self._makeOne(client)
        xact._mutation = object()
        try:
            with xact:
                self.assertEqual(xact.id, 234)
                self.assertEqual(connection._begun, _DATASET)
                raise Foo()
        except Foo:
            self.assertEqual(xact.id, None)
            self.assertEqual(connection._rolled_back, (_DATASET, 234))
        self.assertEqual(connection._committed, None)
        self.assertEqual(xact.id, None)


def _make_key(kind, id, dataset_id):
    from gcloud.datastore._datastore_v1_pb2 import Key

    key = Key()
    key.partition_id.dataset_id = dataset_id
    elem = key.path_element.add()
    elem.kind = kind
    elem.id = id
    return key


class _Connection(object):
    _marker = object()
    _begun = _rolled_back = _committed = None

    def __init__(self, xact_id=123):
        self._xact_id = xact_id
        self._commit_result = _CommitResult()

    def begin_transaction(self, dataset_id):
        self._begun = dataset_id
        return self._xact_id

    def rollback(self, dataset_id, transaction_id):
        self._rolled_back = dataset_id, transaction_id

    def commit(self, dataset_id, mutation, transaction_id):
        self._committed = (dataset_id, mutation, transaction_id)
        return self._commit_result


class _CommitResult(object):

    def __init__(self, *new_keys):
        self.insert_auto_id_key = new_keys


class _Entity(object):

    def __init__(self):
        from gcloud.datastore.key import Key
        self.key = Key('KIND', dataset_id='DATASET')


class _Client(object):

    def __init__(self, dataset_id, connection, namespace=None):
        self.dataset_id = dataset_id
        self.connection = connection
        self.namespace = namespace
        self._batches = []

    def _push_batch(self, batch):
        self._batches.insert(0, batch)

    def _pop_batch(self):
        return self._batches.pop(0)

    @property
    def current_batch(self):
        return self._batches and self._batches[0] or None
