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

    def _makeOne(self, dataset_id=None, connection=None):
        return self._getTargetClass()(dataset_id=dataset_id,
                                      connection=connection)

    def test_ctor_missing_required(self):
        from gcloud.datastore import _implicit_environ

        self.assertEqual(_implicit_environ.DATASET_ID, None)

        with self.assertRaises(ValueError):
            self._makeOne()
        with self.assertRaises(ValueError):
            self._makeOne(dataset_id=object())
        with self.assertRaises(ValueError):
            self._makeOne(connection=object())

    def test_ctor(self):
        from gcloud.datastore.datastore_v1_pb2 import Mutation

        _DATASET = 'DATASET'
        connection = _Connection()
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        self.assertEqual(xact.dataset_id, _DATASET)
        self.assertEqual(xact.connection, connection)
        self.assertEqual(xact.id, None)
        self.assertTrue(isinstance(xact.mutation, Mutation))
        self.assertEqual(len(xact._auto_id_entities), 0)

    def test_ctor_with_env(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import _implicit_environ

        DATASET_ID = 'DATASET'
        CONNECTION = _Connection()

        with _Monkey(_implicit_environ, DATASET_ID=DATASET_ID,
                     CONNECTION=CONNECTION):
            transaction = self._makeOne()

        self.assertEqual(transaction.dataset_id, DATASET_ID)
        self.assertEqual(transaction.connection, CONNECTION)

    def test_add_auto_id_entity(self):
        entity = _Entity()
        _DATASET = 'DATASET'
        connection = _Connection()
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact.add_auto_id_entity(entity)
        self.assertEqual(xact._auto_id_entities, [entity])

    def test_begin(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact.begin()
        self.assertEqual(xact.id, 234)
        self.assertEqual(connection._begun, _DATASET)
        self.assertTrue(connection._xact is xact)

    def test_rollback(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact.begin()
        xact.rollback()
        self.assertEqual(xact.id, None)
        self.assertEqual(connection._rolled_back, _DATASET)
        self.assertEqual(connection._xact, None)

    def test_commit_no_auto_ids(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id, None)

    def test_commit_w_auto_ids(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 123
        connection = _Connection(234)
        connection._commit_result = _CommitResult(
            _make_key(_KIND, _ID, _DATASET))
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        entity = _Entity()
        xact.add_auto_id_entity(entity)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id, None)
        self.assertEqual(entity.key.path, [{'kind': _KIND, 'id': _ID}])

    def test_commit_w_already(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact._mutation = object()
        xact.begin()
        connection.transaction(())  # Simulate previous commit via false-ish.
        xact.commit()
        self.assertEqual(connection._committed, None)
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id, None)

    def test_context_manager_no_raise(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact._mutation = mutation = object()
        with xact:
            self.assertEqual(xact.id, 234)
            self.assertEqual(connection._begun, _DATASET)
            self.assertTrue(connection._xact is xact)
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id, None)

    def test_context_manager_w_raise(self):
        class Foo(Exception):
            pass
        _DATASET = 'DATASET'
        connection = _Connection(234)
        xact = self._makeOne(dataset_id=_DATASET, connection=connection)
        xact._mutation = object()
        try:
            with xact:
                self.assertEqual(xact.id, 234)
                self.assertEqual(connection._begun, _DATASET)
                self.assertTrue(connection._xact is xact)
                raise Foo()
        except Foo:
            self.assertEqual(xact.id, None)
            self.assertEqual(connection._rolled_back, _DATASET)
            self.assertEqual(connection._xact, None)
        self.assertEqual(connection._committed, None)
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id, None)


def _make_key(kind, id, dataset_id):
    from gcloud.datastore.datastore_v1_pb2 import Key

    key = Key()
    key.partition_id.dataset_id = dataset_id
    elem = key.path_element.add()
    elem.kind = kind
    elem.id = id
    return key


class _Connection(object):
    _marker = object()
    _begun = _rolled_back = _committed = _xact = None

    def __init__(self, xact_id=123):
        self._xact_id = xact_id
        self._commit_result = _CommitResult()

    def transaction(self, xact=_marker):
        if xact is self._marker:
            return self._xact
        self._xact = xact

    def begin_transaction(self, dataset_id):
        self._begun = dataset_id
        return self._xact_id

    def rollback(self, dataset_id):
        self._rolled_back = dataset_id

    def commit(self, dataset_id, mutation):
        self._committed = (dataset_id, mutation)
        return self._commit_result


class _CommitResult(object):

    def __init__(self, *new_keys):
        self.insert_auto_id_key = new_keys


class _Entity(object):

    def __init__(self):
        from gcloud.datastore.key import Key
        self.key = Key('KIND', dataset_id='DATASET')
