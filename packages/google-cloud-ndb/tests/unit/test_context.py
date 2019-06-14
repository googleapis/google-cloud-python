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
from unittest import mock

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _eventloop
from google.cloud.ndb import exceptions
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(context_module)


class TestContext:
    def _make_one(self):
        client = mock.Mock(spec=())
        stub = mock.Mock(spec=())
        return context_module.Context(client, stub=stub)

    @mock.patch("google.cloud.ndb._datastore_api.make_stub")
    def test_constructor_defaults(self, make_stub):
        context = context_module.Context("client")
        assert context.client == "client"
        assert context.stub is make_stub.return_value
        make_stub.assert_called_once_with("client")
        assert isinstance(context.eventloop, _eventloop.EventLoop)
        assert context.batches == {}
        assert context.transaction is None

    def test_constructor_overrides(self):
        context = context_module.Context(
            client="client",
            stub="stub",
            eventloop="eventloop",
            batches="batches",
            transaction="transaction",
        )
        assert context.client == "client"
        assert context.stub == "stub"
        assert context.eventloop == "eventloop"
        assert context.batches == "batches"
        assert context.transaction == "transaction"

    def test_new_transaction(self):
        context = self._make_one()
        new_context = context.new(transaction="tx123")
        assert new_context.transaction == "tx123"
        assert context.transaction is None

    def test_use(self):
        context = self._make_one()
        with context.use():
            assert context_module.get_context() is context
        with pytest.raises(exceptions.ContextError):
            context_module.get_context()

    def test_clear_cache(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.clear_cache()

    def test_flush(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.flush()

    def test_get_cache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.get_cache_policy()

    def test_get_datastore_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.get_datastore_policy()

    def test_get_memcache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.get_memcache_policy()

    def test_get_memcache_timeout_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.get_memcache_timeout_policy()

    def test_set_cache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.set_cache_policy(None)

    def test_set_datastore_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.set_datastore_policy(None)

    def test_set_memcache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.set_memcache_policy(None)

    def test_set_memcache_timeout_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.set_memcache_timeout_policy(None)

    def test_call_on_commit(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.call_on_commit(None)

    def test_in_transaction(self):
        context = self._make_one()
        assert context.in_transaction() is False

    def test_default_cache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.default_cache_policy(None)

    def test_default_datastore_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.default_datastore_policy(None)

    def test_default_memcache_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.default_memcache_policy(None)

    def test_default_memcache_timeout_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.default_memcache_timeout_policy(None)

    def test_memcache_add(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_add()

    def test_memcache_cas(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_cas()

    def test_memcache_decr(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_decr()

    def test_memcache_replace(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_replace()

    def test_memcache_set(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_set()

    def test_memcache_delete(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_delete()

    def test_memcache_get(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_get()

    def test_memcache_gets(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_gets()

    def test_memcache_incr(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.memcache_incr()

    def test_urlfetch(self):
        context = self._make_one()
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
