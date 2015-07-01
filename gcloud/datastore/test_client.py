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


class TestClient(unittest2.TestCase):

    DATASET_ID = 'DATASET'
    CONNECTION = object()

    def _getTargetClass(self):
        from gcloud.datastore.client import Client
        return Client

    def _makeOne(self, dataset_id=DATASET_ID, connection=CONNECTION,
                 namespace=None):
        return self._getTargetClass()(dataset_id, connection=connection,
                                      namespace=namespace)

    def test_ctor_w_dataset_id_no_environ(self):
        self.assertRaises(EnvironmentError, self._makeOne, None)

    def test_ctor_w_implicit_inputs(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import client as _MUT
        OTHER = 'other'
        conn = object()
        klass = self._getTargetClass()
        with _Monkey(_MUT,
                     _determine_default_dataset_id=lambda x: x or OTHER,
                     get_connection=lambda: conn):
            client = klass()
        self.assertEqual(client.dataset_id, OTHER)
        self.assertEqual(client.namespace, None)
        self.assertTrue(client.connection is conn)

    def test_ctor_w_explicit_inputs(self):
        OTHER = 'other'
        NAMESPACE = 'namespace'
        conn = object()
        client = self._makeOne(dataset_id=OTHER,
                               namespace=NAMESPACE,
                               connection=conn)
        self.assertEqual(client.dataset_id, OTHER)
        self.assertEqual(client.namespace, NAMESPACE)
        self.assertTrue(client.connection is conn)

    def test_get_defaults(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        key = object()

        with _Monkey(MUT, get=_get):
            client.get(key)

        self.assertEqual(_called_with[0][0], (key,))
        self.assertTrue(_called_with[0][1]['missing'] is None)
        self.assertTrue(_called_with[0][1]['deferred'] is None)
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_get_explicit(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        conn = object()
        client = self._makeOne(connection=conn)
        key, missing, deferred = object(), [], []

        with _Monkey(MUT, get=_get):
            client.get(key, missing, deferred)

        self.assertEqual(_called_with[0][0], (key,))
        self.assertTrue(_called_with[0][1]['missing'] is missing)
        self.assertTrue(_called_with[0][1]['deferred'] is deferred)
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_get_multi_defaults(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get_multi(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        key = object()

        with _Monkey(MUT, get_multi=_get_multi):
            client.get_multi([key])

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['missing'] is None)
        self.assertTrue(_called_with[0][1]['deferred'] is None)
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_get_multi_explicit(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get_multi(*args, **kw):
            _called_with.append((args, kw))

        conn = object()
        client = self._makeOne(connection=conn)
        key, missing, deferred = object(), [], []

        with _Monkey(MUT, get_multi=_get_multi):
            client.get_multi([key], missing, deferred)

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['missing'] is missing)
        self.assertTrue(_called_with[0][1]['deferred'] is deferred)
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        entity = object()

        with _Monkey(MUT, put=_put):
            client.put(entity)

        self.assertEqual(_called_with[0][0], (entity,))
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        entity, conn = object(), object()
        client = self._makeOne(connection=conn)

        with _Monkey(MUT, put=_put):
            client.put(entity)

        self.assertEqual(_called_with[0][0], (entity,))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_multi_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put_multi(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        entity = object()

        with _Monkey(MUT, put_multi=_put_multi):
            client.put_multi([entity])

        self.assertEqual(_called_with[0][0], ([entity],))
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_multi_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put_multi(*args, **kw):
            _called_with.append((args, kw))

        entity, conn = object(), object()
        client = self._makeOne(connection=conn)

        with _Monkey(MUT, put_multi=_put_multi):
            client.put_multi([entity])

        self.assertEqual(_called_with[0][0], ([entity],))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        key = object()

        with _Monkey(MUT, delete=_delete):
            client.delete(key)

        self.assertEqual(_called_with[0][0], (key,))
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        key, conn = object(), object()
        client = self._makeOne(connection=conn)
        with _Monkey(MUT, delete=_delete):
            client.delete(key)

        self.assertEqual(_called_with[0][0], (key,))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_multi_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete_multi(*args, **kw):
            _called_with.append((args, kw))

        client = self._makeOne()
        key = object()

        with _Monkey(MUT, delete_multi=_delete_multi):
            client.delete_multi([key])

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['connection'] is self.CONNECTION)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_multi_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete_multi(*args, **kw):
            _called_with.append((args, kw))

        key, conn = object(), object()
        client = self._makeOne(connection=conn)
        with _Monkey(MUT, delete_multi=_delete_multi):
            client.delete_multi([key])

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_key_w_dataset_id(self):
        KIND = 'KIND'
        ID = 1234
        client = self._makeOne()
        self.assertRaises(TypeError,
                          client.key, KIND, ID, dataset_id=self.DATASET_ID)

    def test_key_wo_dataset_id(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        KIND = 'KIND'
        ID = 1234
        client = self._makeOne()

        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID)

        self.assertTrue(isinstance(key, _Dummy))
        self.assertEqual(key.args, (KIND, ID))
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': None,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_key_w_namespace(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        ID = 1234
        NAMESPACE = object()
        client = self._makeOne(namespace=NAMESPACE)
        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID)

        self.assertTrue(isinstance(key, _Dummy))
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': NAMESPACE,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_key_w_namespace_collision(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        ID = 1234
        NAMESPACE1 = object()
        NAMESPACE2 = object()
        client = self._makeOne(namespace=NAMESPACE1)
        with _Monkey(MUT, Key=_Dummy):
            key = client.key(KIND, ID, namespace=NAMESPACE2)

        self.assertTrue(isinstance(key, _Dummy))
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': NAMESPACE2,
        }
        self.assertEqual(key.kwargs, expected_kwargs)

    def test_batch_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne()

        with _Monkey(MUT, Batch=_Dummy):
            batch = client.batch()

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID,
                          'connection': self.CONNECTION})

    def test_batch_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        conn = object()
        client = self._makeOne(connection=conn)

        with _Monkey(MUT, Batch=_Dummy):
            batch = client.batch()

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': conn})

    def test_transaction_wo_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne()

        with _Monkey(MUT, Transaction=_Dummy):
            xact = client.transaction()

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        self.assertEqual(xact.kwargs,
                         {'dataset_id': self.DATASET_ID,
                          'connection': self.CONNECTION})

    def test_transaction_w_connection(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        conn = object()
        client = self._makeOne(connection=conn)

        with _Monkey(MUT, Transaction=_Dummy):
            xact = client.transaction()

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'connection': conn,
        }
        self.assertEqual(xact.kwargs, expected_kwargs)

    def test_query_w_dataset_id(self):
        KIND = 'KIND'
        client = self._makeOne()
        self.assertRaises(TypeError,
                          client.query, kind=KIND, dataset_id=self.DATASET_ID)

    def test_query_w_defaults(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        client = self._makeOne()

        with _Monkey(MUT, Query=_Dummy):
            query = client.query()

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, ())
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': None,
        }
        self.assertEqual(query.kwargs, expected_kwargs)

    def test_query_explicit(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey
        KIND = 'KIND'
        NAMESPACE = 'NAMESPACE'
        ANCESTOR = object()
        FILTERS = [('PROPERTY', '==', 'VALUE')]
        PROJECTION = ['__key__']
        ORDER = ['PROPERTY']
        GROUP_BY = ['GROUPBY']
        client = self._makeOne()

        with _Monkey(MUT, Query=_Dummy):
            query = client.query(
                kind=KIND,
                namespace=NAMESPACE,
                ancestor=ANCESTOR,
                filters=FILTERS,
                projection=PROJECTION,
                order=ORDER,
                group_by=GROUP_BY,
                )

        self.assertTrue(isinstance(query, _Dummy))
        kwargs = {
            'dataset_id': self.DATASET_ID,
            'kind': KIND,
            'namespace': NAMESPACE,
            'ancestor': ANCESTOR,
            'filters': FILTERS,
            'projection': PROJECTION,
            'order': ORDER,
            'group_by': GROUP_BY,
        }
        self.assertEqual(query.args, ())
        self.assertEqual(query.kwargs, kwargs)

    def test_query_w_namespace(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        NAMESPACE = object()
        client = self._makeOne(namespace=NAMESPACE)
        with _Monkey(MUT, Query=_Dummy):
            query = client.query(kind=KIND)

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, ())
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': NAMESPACE,
            'kind': KIND,
        }
        self.assertEqual(query.kwargs, expected_kwargs)

    def test_query_w_namespace_collision(self):
        from gcloud.datastore import client as MUT
        from gcloud._testing import _Monkey

        KIND = 'KIND'
        NAMESPACE1 = object()
        NAMESPACE2 = object()
        client = self._makeOne(namespace=NAMESPACE1)
        with _Monkey(MUT, Query=_Dummy):
            query = client.query(kind=KIND, namespace=NAMESPACE2)

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, ())
        expected_kwargs = {
            'dataset_id': self.DATASET_ID,
            'namespace': NAMESPACE2,
            'kind': KIND,
        }
        self.assertEqual(query.kwargs, expected_kwargs)


class _Dummy(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
