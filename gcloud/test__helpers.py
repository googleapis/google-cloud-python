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


class Test__LocalStack(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._helpers import _LocalStack

        return _LocalStack

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


class Test__LazyProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._helpers import _LazyProperty
        return _LazyProperty

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_prop_on_class(self):
        # Don't actually need a callable for ``method`` since
        # __get__ will just return ``self`` in this test.
        data_prop = self._makeOne('dataset_id', None)

        class FakeEnv(object):
            dataset_id = data_prop

        self.assertTrue(FakeEnv.dataset_id is data_prop)

    def test_prop_on_instance(self):
        RESULT = object()
        data_prop = self._makeOne('dataset_id', lambda: RESULT)

        class FakeEnv(object):
            dataset_id = data_prop

        self.assertTrue(FakeEnv().dataset_id is RESULT)


class Test__lazy_property_deco(unittest2.TestCase):

    def _callFUT(self, deferred_callable):
        from gcloud._helpers import _lazy_property_deco
        return _lazy_property_deco(deferred_callable)

    def test_on_function(self):
        def test_func():
            pass  # pragma: NO COVER never gets called

        lazy_prop = self._callFUT(test_func)
        self.assertTrue(lazy_prop._deferred_callable is test_func)
        self.assertEqual(lazy_prop._name, 'test_func')

    def test_on_staticmethod(self):
        def test_func():
            pass  # pragma: NO COVER never gets called

        lazy_prop = self._callFUT(staticmethod(test_func))
        self.assertTrue(lazy_prop._deferred_callable is test_func)
        self.assertEqual(lazy_prop._name, 'test_func')
