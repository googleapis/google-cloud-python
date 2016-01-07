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

    def _makeOne(self, client, **kw):
        return self._getTargetClass()(client, **kw)

    def test_ctor_defaults(self):
        from gcloud.datastore._generated import datastore_pb2

        _PROJECT = 'PROJECT'
        connection = _Connection()
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        self.assertEqual(xact.project, _PROJECT)
        self.assertEqual(xact.connection, connection)
        self.assertEqual(xact.id, None)
        self.assertEqual(xact._status, self._getTargetClass()._INITIAL)
        self.assertTrue(isinstance(xact._commit_request,
                                   datastore_pb2.CommitRequest))
        self.assertTrue(xact.mutations is xact._commit_request.mutations)
        self.assertEqual(len(xact._partial_key_entities), 0)

    def test_current(self):
        from gcloud.datastore.test_client import _NoCommitBatch
        _PROJECT = 'PROJECT'
        connection = _Connection()
        client = _Client(_PROJECT, connection)
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
        self.assertEqual(xact.id, None)

        self.assertRaises(ValueError, xact.begin)

    def test_rollback(self):
        _PROJECT = 'PROJECT'
        connection = _Connection(234)
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        xact.begin()
        xact.rollback()
        self.assertEqual(xact.id, None)
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
        self.assertEqual(xact.id, None)

    def test_commit_w_partial_keys(self):
        _PROJECT = 'PROJECT'
        _KIND = 'KIND'
        _ID = 123
        connection = _Connection(234)
        connection._completed_keys = [_make_key(_KIND, _ID, _PROJECT)]
        client = _Client(_PROJECT, connection)
        xact = self._makeOne(client)
        entity = _Entity()
        xact.put(entity)
        xact._commit_request = commit_request = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed,
                         (_PROJECT, commit_request, 234))
        self.assertEqual(xact.id, None)
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
        self.assertEqual(xact.id, None)

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
            self.assertEqual(xact.id, None)
            self.assertEqual(connection._rolled_back, (_PROJECT, 234))
        self.assertEqual(connection._committed, None)
        self.assertEqual(xact.id, None)


def _make_key(kind, id_, project):
    from gcloud.datastore._generated import entity_pb2

    key = entity_pb2.Key()
    key.partition_id.project_id = project
    elem = key.path.add()
    elem.kind = kind
    elem.id = id_
    return key


class _Connection(object):
    _marker = object()
    _begun = _rolled_back = _committed = None

    def __init__(self, xact_id=123):
        self._xact_id = xact_id
        self._completed_keys = []
        self._index_updates = 0

    def begin_transaction(self, project):
        self._begun = project
        return self._xact_id

    def rollback(self, project, transaction_id):
        self._rolled_back = project, transaction_id

    def commit(self, project, commit_request, transaction_id):
        self._committed = (project, commit_request, transaction_id)
        return self._index_updates, self._completed_keys


class _Entity(dict):

    def __init__(self):
        super(_Entity, self).__init__()
        from gcloud.datastore.key import Key
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
