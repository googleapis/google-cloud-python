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

try:
    from unittest import mock
except ImportError:  # pragma: NO PY3 COVER
    import mock

from google.cloud.ndb import _cache
from google.cloud.ndb import context as context_module
from google.cloud.ndb import _eventloop
from google.cloud.ndb import exceptions
from google.cloud.ndb import global_cache
from google.cloud.ndb import key as key_module
from google.cloud.ndb import model
from google.cloud.ndb import _options
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(context_module)


class TestContext:
    def _make_one(self, **kwargs):
        client = mock.Mock(
            namespace=None,
            project="testing",
            spec=("namespace", "project"),
            stub=mock.Mock(spec=()),
        )
        return context_module.Context(client, **kwargs)

    def test_constructor_defaults(self):
        context = context_module.Context("client")
        assert context.client == "client"
        assert isinstance(context.eventloop, _eventloop.EventLoop)
        assert context.batches == {}
        assert context.transaction is None

    def test_constructor_overrides(self):
        context = context_module.Context(
            client="client",
            eventloop="eventloop",
            batches="batches",
            transaction="transaction",
        )
        assert context.client == "client"
        assert context.eventloop == "eventloop"
        assert context.batches == "batches"
        assert context.transaction == "transaction"

    def test_new_transaction(self):
        context = self._make_one()
        new_context = context.new(transaction="tx123")
        assert new_context.transaction == "tx123"
        assert context.transaction is None

    def test_new_with_cache(self):
        context = self._make_one()
        context.cache["foo"] = "bar"
        new_context = context.new()
        assert context.cache is not new_context.cache
        assert context.cache == new_context.cache

    def test_use(self):
        context = self._make_one()
        with context.use():
            assert context_module.get_context() is context
        with pytest.raises(exceptions.ContextError):
            context_module.get_context()

    def test_use_nested(self):
        context = self._make_one()
        with context.use():
            assert context_module.get_context() is context
            next_context = context.new()
            with next_context.use():
                assert context_module.get_context() is next_context

            assert context_module.get_context() is context

        with pytest.raises(exceptions.ContextError):
            context_module.get_context()

    def test_clear_cache(self):
        context = self._make_one()
        context.cache["testkey"] = "testdata"
        context.clear_cache()
        assert not context.cache

    def test__clear_global_cache(self):
        context = self._make_one(
            global_cache=global_cache._InProcessGlobalCache()
        )
        with context.use():
            key = key_module.Key("SomeKind", 1)
            cache_key = _cache.global_cache_key(key._key)
            context.cache[key] = "testdata"
            context.global_cache.cache[cache_key] = "testdata"
            context.global_cache.cache["anotherkey"] = "otherdata"
            context._clear_global_cache().result()

        assert context.global_cache.cache == {"anotherkey": "otherdata"}

    def test__clear_global_cache_nothing_to_do(self):
        context = self._make_one(
            global_cache=global_cache._InProcessGlobalCache()
        )
        with context.use():
            context.global_cache.cache["anotherkey"] = "otherdata"
            context._clear_global_cache().result()

        assert context.global_cache.cache == {"anotherkey": "otherdata"}

    def test_flush(self):
        eventloop = mock.Mock(spec=("run",))
        context = self._make_one(eventloop=eventloop)
        context.flush()
        eventloop.run.assert_called_once_with()

    def test_get_cache_policy(self):
        context = self._make_one()
        assert (
            context.get_cache_policy() is context_module._default_cache_policy
        )

    def test_get_datastore_policy(self):
        context = self._make_one()
        with pytest.raises(NotImplementedError):
            context.get_datastore_policy()

    def test__use_datastore_default_policy(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = key_module.Key("SomeKind", 1)
            options = _options.Options()
            assert context._use_datastore(key, options) is True

    def test__use_datastore_from_options(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = key_module.Key("SomeKind", 1)
            options = _options.Options(use_datastore=False)
            assert context._use_datastore(key, options) is False

    def test_get_memcache_policy(self):
        context = self._make_one()
        context.get_memcache_policy()
        assert (
            context.get_memcache_policy()
            is context_module._default_global_cache_policy
        )

    def test_get_global_cache_policy(self):
        context = self._make_one()
        context.get_global_cache_policy()
        assert (
            context.get_memcache_policy()
            is context_module._default_global_cache_policy
        )

    def test_get_memcache_timeout_policy(self):
        context = self._make_one()
        assert (
            context.get_memcache_timeout_policy()
            is context_module._default_global_cache_timeout_policy
        )

    def test_get_global_cache_timeout_policy(self):
        context = self._make_one()
        assert (
            context.get_global_cache_timeout_policy()
            is context_module._default_global_cache_timeout_policy
        )

    def test_set_cache_policy(self):
        policy = object()
        context = self._make_one()
        context.set_cache_policy(policy)
        assert context.get_cache_policy() is policy

    def test_set_cache_policy_to_None(self):
        context = self._make_one()
        context.set_cache_policy(None)
        assert (
            context.get_cache_policy() is context_module._default_cache_policy
        )

    def test_set_cache_policy_with_bool(self):
        context = self._make_one()
        context.set_cache_policy(False)
        assert context.get_cache_policy()(None) is False

    def test__use_cache_default_policy(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = key_module.Key("SomeKind", 1)
            options = _options.Options()
            assert context._use_cache(key, options) is True

    def test__use_cache_from_options(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = "whocares"
            options = _options.Options(use_cache=False)
            assert context._use_cache(key, options) is False

    def test_set_datastore_policy(self):
        context = self._make_one()
        context.set_datastore_policy(None)
        assert (
            context.datastore_policy
            is context_module._default_datastore_policy
        )

    def test_set_datastore_policy_as_bool(self):
        context = self._make_one()
        context.set_datastore_policy(False)
        context.datastore_policy(None) is False

    def test_set_memcache_policy(self):
        context = self._make_one()
        context.set_memcache_policy(None)
        assert (
            context.global_cache_policy
            is context_module._default_global_cache_policy
        )

    def test_set_global_cache_policy(self):
        context = self._make_one()
        context.set_global_cache_policy(None)
        assert (
            context.global_cache_policy
            is context_module._default_global_cache_policy
        )

    def test_set_global_cache_policy_as_bool(self):
        context = self._make_one()
        context.set_global_cache_policy(True)
        assert context.global_cache_policy("whatever") is True

    def test__use_global_cache_no_global_cache(self):
        context = self._make_one()
        assert context._use_global_cache("key") is False

    def test__use_global_cache_default_policy(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one(global_cache="yes, there is one")
        with context.use():
            key = key_module.Key("SomeKind", 1)
            assert context._use_global_cache(key._key) is True

    def test__use_global_cache_from_options(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one(global_cache="yes, there is one")
        with context.use():
            key = "whocares"
            options = _options.Options(use_global_cache=False)
            assert context._use_global_cache(key, options=options) is False

    def test_set_memcache_timeout_policy(self):
        context = self._make_one()
        context.set_memcache_timeout_policy(None)
        assert (
            context.global_cache_timeout_policy
            is context_module._default_global_cache_timeout_policy
        )

    def test_set_global_cache_timeout_policy(self):
        context = self._make_one()
        context.set_global_cache_timeout_policy(None)
        assert (
            context.global_cache_timeout_policy
            is context_module._default_global_cache_timeout_policy
        )

    def test_set_global_cache_timeout_policy_as_int(self):
        context = self._make_one()
        context.set_global_cache_timeout_policy(14)
        assert context.global_cache_timeout_policy("whatever") == 14

    def test__global_cache_timeout_default_policy(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = key_module.Key("SomeKind", 1)
            timeout = context._global_cache_timeout(key._key, None)
            assert timeout is None

    def test__global_cache_timeout_from_options(self):
        class SomeKind(model.Model):
            pass

        context = self._make_one()
        with context.use():
            key = "whocares"
            options = _options.Options(global_cache_timeout=49)
            assert context._global_cache_timeout(key, options) == 49

    def test_call_on_commit(self):
        context = self._make_one()
        callback = mock.Mock()
        context.call_on_commit(callback)
        callback.assert_called_once_with()

    def test_call_on_commit_with_transaction(self):
        callbacks = []
        callback = "himom!"
        context = self._make_one(
            transaction=b"tx123", on_commit_callbacks=callbacks
        )
        context.call_on_commit(callback)
        assert context.on_commit_callbacks == ["himom!"]

    def test_in_transaction(self):
        context = self._make_one()
        assert context.in_transaction() is False

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


class Test_default_cache_policy:
    @staticmethod
    def test_key_is_None():
        assert context_module._default_cache_policy(None) is None

    @staticmethod
    def test_no_model_class():
        key = mock.Mock(kind=mock.Mock(return_value="nokind"), spec=("kind",))
        assert context_module._default_cache_policy(key) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model():
        class ThisKind(model.Model):
            pass

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_cache_policy(key) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy():
        flag = object()

        class ThisKind(model.Model):
            @classmethod
            def _use_cache(cls, key):
                return flag

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_cache_policy(key) is flag

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy_as_bool():
        class ThisKind(model.Model):
            _use_cache = False

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_cache_policy(key) is False


class Test_default_global_cache_policy:
    @staticmethod
    def test_key_is_None():
        assert context_module._default_global_cache_policy(None) is None

    @staticmethod
    def test_no_model_class():
        key = mock.Mock(kind="nokind", spec=("kind",))
        assert context_module._default_global_cache_policy(key) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model():
        class ThisKind(model.Model):
            pass

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_global_cache_policy(key._key) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy():
        flag = object()

        class ThisKind(model.Model):
            @classmethod
            def _use_global_cache(cls, key):
                return flag

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_global_cache_policy(key._key) is flag

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy_as_bool():
        class ThisKind(model.Model):
            _use_global_cache = False

        key = key_module.Key("ThisKind", 0)
        assert context_module._default_global_cache_policy(key._key) is False


class Test_default_global_cache_timeout_policy:
    @staticmethod
    def test_key_is_None():
        assert (
            context_module._default_global_cache_timeout_policy(None) is None
        )

    @staticmethod
    def test_no_model_class():
        key = mock.Mock(kind="nokind", spec=("kind",))
        assert context_module._default_global_cache_timeout_policy(key) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model():
        class ThisKind(model.Model):
            pass

        key = key_module.Key("ThisKind", 0)
        assert (
            context_module._default_global_cache_timeout_policy(key._key)
            is None
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy():
        class ThisKind(model.Model):
            @classmethod
            def _global_cache_timeout(cls, key):
                return 13

        key = key_module.Key("ThisKind", 0)
        assert (
            context_module._default_global_cache_timeout_policy(key._key) == 13
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_standard_model_defines_policy_as_int():
        class ThisKind(model.Model):
            _global_cache_timeout = 12

        key = key_module.Key("ThisKind", 0)
        assert (
            context_module._default_global_cache_timeout_policy(key._key) == 12
        )
