# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from google.cloud.ndb import context as context_module
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(context_module)


class TestContext:
    def test_clear_cache(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.clear_cache()

    def test_flush(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.flush()

    def test_get_cache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.get_cache_policy()

    def test_get_datastore_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.get_datastore_policy()

    def test_get_memcache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.get_memcache_policy()

    def test_get_memcache_timeout_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.get_memcache_timeout_policy()

    def test_set_cache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.set_cache_policy(None)

    def test_set_datastore_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.set_datastore_policy(None)

    def test_set_memcache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.set_memcache_policy(None)

    def test_set_memcache_timeout_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.set_memcache_timeout_policy(None)

    def test_call_on_commit(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.call_on_commit(None)

    def test_in_transaction(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.in_transaction()

    def test_default_cache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.default_cache_policy(None)

    def test_default_datastore_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.default_datastore_policy(None)

    def test_default_memcache_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.default_memcache_policy(None)

    def test_default_memcache_timeout_policy(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.default_memcache_timeout_policy(None)

    def test_memcache_add(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_add()

    def test_memcache_cas(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_cas()

    def test_memcache_decr(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_decr()

    def test_memcache_replace(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_replace()

    def test_memcache_set(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_set()

    def test_memcache_delete(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_delete()

    def test_memcache_get(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_get()

    def test_memcache_gets(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_gets()

    def test_memcache_incr(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.memcache_incr()

    def test_urlfetch(self):
        context = context_module.Context()
        with pytest.raises(NotImplementedError):
            context.urlfetch()


class TestAutoBatcher:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context_module.AutoBatcher()


class TestContextOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context_module.ContextOptions()


class TestTransactionOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            context_module.TransactionOptions()
