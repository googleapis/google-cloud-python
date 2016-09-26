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


class TestTransaction(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.datastore.transaction import Transaction
        return Transaction

    def _makeOne(self, client, **kw):
        return self._getTargetClass()(client, **kw)

    def test_ctor_defaults(self):
        from google.cloud.datastore._generated import datastore_pb2

        _PROJECT = 'PROJECT'
        connection = _Connection()
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        self.assertEqual(xact.project, _PROJECT)
        self.assertEqual(xact.connection, connection)
        self.assertIsNone(xact.id)
        self.assertEqual(xact._status, self._getTargetClass()._INITIAL)
        self.assertIsInstance(xact._commit_request,
                              datastore_pb2.CommitRequest)
        self.assertIs(xact.mutations, xact._commit_request.mutations)
        self.assertEqual(len(xact._partial_key_entities), 0)

    def test_current(self):
        _PROJECT = 'PROJECT'
        connection = _Connection()
        client = _Client(_PROJECT, connection)
        xact1 = self._makeOne(client)
        xact2 = self._makeOne(client)
        self.assertIsNone(xact1.current())
        self.assertIsNone(xact2.current())
        with xact1:
            self.assertIs(xact1.current(), xact1)
            self.assertIs(xact2.current(), xact1)
            with _NoCommitBatch(client):
                self.assertIsNone(xact1.current())
                self.assertIsNone(xact2.current())
            with xact2:
                self.assertIs(xact1.current(), xact2)
                self.assertIs(xact2.current(), xact2)
                with _NoCommitBatch(client):
                    self.assertIsNone(xact1.current())
                    self.assertIsNone(xact2.current())
            self.assertIs(xact1.current(), xact1)
            self.assertIs(xact2.current(), xact1)
        self.assertIsNone(xact1.current())
        self.assertIsNone(xact2.current())

    def test_begin(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact.begin()
        self.assertEqual(xact.id, 234)
        self.assertEqual(connection._begun, _PROJECT)

    def test_begin_tombstoned(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact.begin()
        self.assertEqual(xact.id, 234)
        self.assertEqual(connection._begun, _PROJECT)

        xact.rollback()
        self.assertIsNone(xact.id)

        self.assertRaises(ValueError, xact.begin)

    def test_begin_w_begin_transaction_failure(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)

        connection._side_effect = RuntimeError
        with self.assertRaises(RuntimeError):
            xact.begin()

        self.assertIsNone(xact.id)
        self.assertEqual(connection._begun, _PROJECT)

    def test_rollback(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact.begin()
        xact.rollback()
        self.assertIsNone(xact.id)
        self.assertEqual(connection._rolled_back, (_PROJECT, 234))

    def test_commit_no_partial_keys(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact._commit_request = commit_request = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed,
                         (_PROJECT, commit_request, 234))
        self.assertIsNone(xact.id)

    def test_commit_w_partial_keys(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 123
        connection = _Connection(234)
        connection._completed_keys = [_make_key(_KIND, _ID, _PROJECT)]
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact.begin()
        entity = _Entity()
        xact.put(entity)
        xact._commit_request = commit_request = object()
        xact.commit()
        self.assertEqual(connection._committed,
                         (_PROJECT, commit_request, 234))
        self.assertIsNone(xact.id)
        self.assertEqual(entity.key.path, [{'kind': _KIND, 'id': _ID}])

    def test_context_manager_no_raise(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact._commit_request = commit_request = object()
        with xact:
            self.assertEqual(xact.id, 234)
            self.assertEqual(connection._begun, _PROJECT)
        self.assertEqual(connection._committed,
                         (_PROJECT, commit_request, 234))
        self.assertIsNone(xact.id)

    def test_context_manager_w_raise(self):

        class Foo(Exception):
            pass

        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact._mutation = object()
        try:
            with xact:
                self.assertEqual(xact.id, 234)
                self.assertEqual(connection._begun, _PROJECT)
                raise Foo()
        except Foo:
            self.assertIsNone(xact.id)
            self.assertEqual(connection._rolled_back, (_PROJECT, 234))
        self.assertIsNone(connection._committed)
        self.assertIsNone(xact.id)


def _make_key(kind, id_, project):
    from google.cloud.datastore._generated import entity_pb2

    key = entity_pb2.Key()
    key.partition_id.project_id = project
    elem = key.path.add()
    elem.kind = kind
    elem.id = id_
    return key


class _Connection(object):
    _marker = object()
    _begun = None
    _rolled_back = None
    _committed = None
    _side_effect = None

    def __init__(self, xact_id=123):
        self._xact_id = xact_id
        self._completed_keys = []
        self._index_updates = 0

    def begin_transaction(self, project):
        self._begun = project
        if self._side_effect is None:
            return self._xact_id
        else:
            raise self._side_effect

    def rollback(self, project, transaction_id):
        self._rolled_back = project, transaction_id

    def commit(self, project, commit_request, transaction_id):
        self._committed = (project, commit_request, transaction_id)
        return self._index_updates, self._completed_keys


class _Entity(dict):

    def __init__(self):
        super(_Entity, self).__init__()
        from google.cloud.datastore.key import Key
        self.key = Key('KIND', project='PROJECT')


class _Client(object):

    def __init__(self, project, connection, namespace=None):
        self.project = project
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


class _NoCommitBatch(object):

    def __init__(self, client):
        from google.cloud.datastore.batch import Batch
        self._client = client
        self._batch = Batch(client)

    def __enter__(self):
        self._client._push_batch(self._batch)
        return self._batch

    def __exit__(self, *args):
        self._client._pop_batch()
