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
        return self._getTargetClass()(dataset_id=dataset_id)

    def test_ctor_w_None(self):
        self.assertRaises(ValueError, self._makeOne, None)

    def test_ctor_w_dataset_id(self):
        dataset = self._makeOne()
        self.assertEqual(dataset.dataset_id, self.DATASET_ID)

    def test_get_defaults(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        key = object()

        with _Monkey(MUT, get=_get):
            dataset.get([key])

        args = ([key], None, None, None, self.DATASET_ID)
        self.assertEqual(_called_with, [(args, {})])

    def test_get_explicit(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _get(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        key, missing, deferred, conn = object(), [], [], object()

        with _Monkey(MUT, get=_get):
            dataset.get([key], missing, deferred, conn)

        args = ([key], missing, deferred, conn, self.DATASET_ID)
        self.assertEqual(_called_with, [(args, {})])

    def test_put_wo_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        entity = object()

        with _Monkey(MUT, put=_put):
            dataset.put([entity])

        self.assertEqual(_called_with,
                         [(([entity], None), {'dataset_id': self.DATASET_ID})])

    def test_put_w_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _put(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        entity, conn = object(), object()

        with _Monkey(MUT, put=_put):
            dataset.put([entity], conn)

        self.assertEqual(_called_with,
                         [(([entity], conn), {'dataset_id': self.DATASET_ID})])

    def test_delete_wo_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        key = object()

        with _Monkey(MUT, delete=_delete):
            dataset.delete([key])

        self.assertEqual(_called_with,
                         [(([key], None), {'dataset_id': self.DATASET_ID})])

    def test_delete_w_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey

        _called_with = []

        def _delete(*args, **kw):
            _called_with.append((args, kw))

        dataset = self._makeOne()
        key, conn = object(), object()
        with _Monkey(MUT, delete=_delete):
            dataset.delete([key], conn)

        self.assertEqual(_called_with,
                         [(([key], conn), {'dataset_id': self.DATASET_ID})])

    def test_key_w_conflicting_dataset_id(self):
        KIND = 'KIND'
        ID = 1234
        dataset = self._makeOne()
        self.assertRaises(ValueError,
                          dataset.key, KIND, ID, dataset_id='OTHER')

    def test_key_w_matching_dataset_id(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        KIND = 'KIND'
        ID = 1234
        dataset = self._makeOne()

        with _Monkey(MUT, Key=_Dummy):
            key = dataset.key(KIND, ID, dataset_id=self.DATASET_ID)

        self.assertTrue(isinstance(key, _Dummy))
        self.assertEqual(key.args, (KIND, ID))
        self.assertEqual(key.kwargs, {'dataset_id': self.DATASET_ID})

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

    def test_batch_wo_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()

        with _Monkey(MUT, Batch=_Dummy):
            batch = dataset.batch()

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': None})

    def test_batch_w_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()
        conn = object()

        with _Monkey(MUT, Batch=_Dummy):
            batch = dataset.batch(conn)

        self.assertTrue(isinstance(batch, _Dummy))
        self.assertEqual(batch.args, ())
        self.assertEqual(batch.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': conn})

    def test_transaction_wo_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()

        with _Monkey(MUT, Transaction=_Dummy):
            xact = dataset.transaction()

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        self.assertEqual(xact.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': None})

    def test_transaction_w_connection(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()
        conn = object()

        with _Monkey(MUT, Transaction=_Dummy):
            xact = dataset.transaction(conn)

        self.assertTrue(isinstance(xact, _Dummy))
        self.assertEqual(xact.args, ())
        self.assertEqual(xact.kwargs,
                         {'dataset_id': self.DATASET_ID, 'connection': conn})

    def test_query_w_defaults(self):
        from gcloud.datastore import dataset as MUT
        from gcloud._testing import _Monkey
        dataset = self._makeOne()

        with _Monkey(MUT, Query=_Dummy):
            query = dataset.query()

        self.assertTrue(isinstance(query, _Dummy))
        args = (self.DATASET_ID, None, None, None, (), (), (), ())
        self.assertEqual(query.args, args)
        self.assertEqual(query.kwargs, {})

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
            query = dataset.query(KIND, NAMESPACE, ANCESTOR, FILTERS,
                                  PROJECTION, ORDER, GROUP_BY)

        self.assertTrue(isinstance(query, _Dummy))
        args = (self.DATASET_ID, KIND, NAMESPACE, ANCESTOR, FILTERS,
                PROJECTION, ORDER, GROUP_BY)
        self.assertEqual(query.args, args)
        self.assertEqual(query.kwargs, {})


class _Dummy(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
