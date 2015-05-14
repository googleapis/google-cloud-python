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

    DATASET_ID = 'DATASET'

    def _getTargetClass(self):
        from gcloud.datastore.dataset import Dataset
        return Dataset

    def _makeOne(self, dataset_id=DATASET_ID):
        return self._getTargetClass()(dataset_id)

    def test_ctor_w_dataset_id_None(self):
        self.assertRaises(ValueError, self._makeOne, None)

    def test_ctor_w_dataset_id(self):
        dataset = self._makeOne()
        self.assertEqual(dataset.dataset_id, self.DATASET_ID)

    def test_get_defaults_w_implicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        from gcloud.datastore._testing import _monkey_defaults

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        conn = object()
        dataset = self._makeOne()
        key = object()

        with _Monkey(MUT, get=_get):
            with _monkey_defaults(connection=conn):
                dataset.get([key])

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['missing'] is None)
        self.assertTrue(_called_with[0][1]['deferred'] is None)
        self.assertTrue(_called_with[0][1]['connection'] is None)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_get_explicit_w_explicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        conn = object()
        dataset = self._makeOne()
        key, missing, deferred = object(), [], []

        with _Monkey(MUT, get=_get):
            dataset.get([key], missing, deferred, connection=conn)

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['missing'] is missing)
        self.assertTrue(_called_with[0][1]['deferred'] is deferred)
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_w_implicit_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import dataset as MUT
        from gcloud.datastore._testing import _monkey_defaults

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        entity, conn = object(), object()
        dataset = self._makeOne()

        with _Monkey(MUT, put=_put):
            with _monkey_defaults(connection=conn):
                dataset.put([entity])

        self.assertEqual(_called_with[0][0], ([entity],))
        self.assertTrue(_called_with[0][1]['connection'] is None)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_put_w_explicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        entity, conn = object(), object()
        dataset = self._makeOne()

        with _Monkey(MUT, put=_put):
            dataset.put([entity], connection=conn)

        self.assertEqual(_called_with[0][0], ([entity],))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_w_implicit_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import dataset as MUT
        from gcloud.datastore._testing import _monkey_defaults

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        key, conn = object(), object()
        dataset = self._makeOne()
        with _Monkey(MUT, delete=_delete):
            with _monkey_defaults(connection=conn):
                dataset.delete([key])

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['connection'] is None)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_delete_w_explicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        key, conn = object(), object()
        dataset = self._makeOne()
        with _Monkey(MUT, delete=_delete):
            dataset.delete([key], connection=conn)

        self.assertEqual(_called_with[0][0], ([key],))
        self.assertTrue(_called_with[0][1]['connection'] is conn)
        self.assertEqual(_called_with[0][1]['dataset_id'], self.DATASET_ID)

    def test_key_w_dataset_id(self):
        KIND = 'KIND'
        ID = 1234
        dataset = self._makeOne()
        self.assertRaises(TypeError,
                          dataset.key, KIND, ID, dataset_id=self.DATASET_ID)

    def test_key_wo_dataset_id(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        KIND = 'KIND'
        ID = 1234
        dataset = self._makeOne()

        with _Monkey(MUT, Key=_Dummy):
            key = dataset.key(KIND, ID)

        self.assertTrue(isinstance(key, _Dummy))
        self.assertEqual(key.args, (KIND, ID))
        self.assertEqual(key.kwargs, {'dataset_id': self.DATASET_ID})

    def test_batch_w_implicit_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import dataset as MUT
        from gcloud.datastore._testing import _monkey_defaults
        conn = object()
        dataset = self._makeOne()

        with _Monkey(MUT, Batch=_Dummy):
            with _monkey_defaults(connection=conn):
                batch = dataset.batch()

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': None})

    def test_batch_w_explicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        conn = object()
        dataset = self._makeOne()

        with _Monkey(MUT, Batch=_Dummy):
            batch = dataset.batch(connection=conn)

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': conn})

    def test_transaction_w_implicit_connection(self):
        from gcloud._testing import _Monkey
        from gcloud.datastore import dataset as MUT
        from gcloud.datastore._testing import _monkey_defaults
        conn = object()
        dataset = self._makeOne()

        with _Monkey(MUT, Transaction=_Dummy):
            with _monkey_defaults(connection=conn):
                xact = dataset.transaction()

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        self.assertEqual(xact.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': None})

    def test_transaction_w_explicit_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        conn = object()
        dataset = self._makeOne()

        with _Monkey(MUT, Transaction=_Dummy):
            xact = dataset.transaction(connection=conn)

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        self.assertEqual(xact.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': conn})

    def test_query_w_dataset_id(self):
        KIND = 'KIND'
        dataset = self._makeOne()
        self.assertRaises(TypeError,
                          dataset.query, kind=KIND, dataset_id=self.DATASET_ID)

    def test_query_w_defaults(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()

        with _Monkey(MUT, Query=_Dummy):
            query = dataset.query()

        self.assertTrue(isinstance(query, _Dummy))
        self.assertEqual(query.args, ())
        self.assertEqual(query.kwargs, {'dataset_id': self.DATASET_ID})

    def test_query_explicit(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        KIND = 'KIND'
        NAMESPACE = 'NAMESPACE'
        ANCESTOR = object()
        FILTERS = [('PROPERTY', '==', 'VALUE')]
        PROJECTION = ['__key__']
        ORDER = ['PROPERTY']
        GROUP_BY = ['GROUPBY']
        dataset = self._makeOne()

        with _Monkey(MUT, Query=_Dummy):
            query = dataset.query(
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


class _Dummy(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
