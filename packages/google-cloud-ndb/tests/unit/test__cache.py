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

try:
    from unittest import mock
except ImportError:  # pragma: NO PY3 COVER
    import mock

import pytest

from google.cloud.ndb import _cache
from google.cloud.ndb import tasklets


def future_result(result):
    future = tasklets.Future()
    future.set_result(result)
    return future


class TestContextCache:
    @staticmethod
    def test_get_and_validate_valid():
        cache = _cache.ContextCache()
        test_entity = mock.Mock(_key="test")
        cache["test"] = test_entity
        assert cache.get_and_validate("test") is test_entity

    @staticmethod
    def test_get_and_validate_invalid():
        cache = _cache.ContextCache()
        test_entity = mock.Mock(_key="test")
        cache["test"] = test_entity
        test_entity._key = "changed_key"
        with pytest.raises(KeyError):
            cache.get_and_validate("test")

    @staticmethod
    def test_get_and_validate_none():
        cache = _cache.ContextCache()
        cache["test"] = None
        assert cache.get_and_validate("test") is None

    @staticmethod
    def test_get_and_validate_miss():
        cache = _cache.ContextCache()
        with pytest.raises(KeyError):
            cache.get_and_validate("nonexistent_key")


class Test_GlobalCacheBatch:
    @staticmethod
    def test_make_call():
        batch = _cache._GlobalCacheBatch()
        with pytest.raises(NotImplementedError):
            batch.make_call()

    @staticmethod
    def test_future_info():
        batch = _cache._GlobalCacheBatch()
        with pytest.raises(NotImplementedError):
            batch.future_info(None)


@mock.patch("google.cloud.ndb._cache._batch")
def test_global_get(_batch):
    batch = _batch.get_batch.return_value
    assert _cache.global_get(b"foo") is batch.add.return_value
    _batch.get_batch.assert_called_once_with(_cache._GlobalCacheGetBatch)
    batch.add.assert_called_once_with(b"foo")


class Test_GlobalCacheGetBatch:
    @staticmethod
    def test_add_and_idle_and_done_callbacks(in_context):
        cache = mock.Mock()
        cache.get.return_value = future_result([b"one", b"two"])

        batch = _cache._GlobalCacheGetBatch(None)
        future1 = batch.add(b"foo")
        future2 = batch.add(b"bar")
        future3 = batch.add(b"foo")

        assert set(batch.todo.keys()) == {b"foo", b"bar"}
        assert batch.keys == [b"foo", b"bar"]

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.get.assert_called_once_with(batch.keys)
        assert future1.result() == b"one"
        assert future2.result() == b"two"
        assert future3.result() == b"one"

    @staticmethod
    def test_add_and_idle_and_done_callbacks_synchronous(in_context):
        cache = mock.Mock()
        cache.get.return_value = [b"one", b"two"]

        batch = _cache._GlobalCacheGetBatch(None)
        future1 = batch.add(b"foo")
        future2 = batch.add(b"bar")

        assert set(batch.todo.keys()) == {b"foo", b"bar"}
        assert batch.keys == [b"foo", b"bar"]

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.get.assert_called_once_with(batch.keys)
        assert future1.result() == b"one"
        assert future2.result() == b"two"

    @staticmethod
    def test_add_and_idle_and_done_callbacks_w_error(in_context):
        error = Exception("spurious error")
        cache = mock.Mock()
        cache.get.return_value = tasklets.Future()
        cache.get.return_value.set_exception(error)

        batch = _cache._GlobalCacheGetBatch(None)
        future1 = batch.add(b"foo")
        future2 = batch.add(b"bar")

        assert set(batch.todo.keys()) == {b"foo", b"bar"}
        assert batch.keys == [b"foo", b"bar"]

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.get.assert_called_once_with(batch.keys)
        assert future1.exception() is error
        assert future2.exception() is error

    @staticmethod
    def test_full():
        batch = _cache._GlobalCacheGetBatch(None)
        assert batch.full() is False


class Test_global_set:
    @staticmethod
    @mock.patch("google.cloud.ndb._cache._batch")
    def test_without_expires(_batch):
        batch = _batch.get_batch.return_value
        assert _cache.global_set(b"key", b"value") is batch.add.return_value
        _batch.get_batch.assert_called_once_with(
            _cache._GlobalCacheSetBatch, {}
        )
        batch.add.assert_called_once_with(b"key", b"value")

    @staticmethod
    @mock.patch("google.cloud.ndb._cache._batch")
    def test_with_expires(_batch):
        batch = _batch.get_batch.return_value
        future = _cache.global_set(b"key", b"value", expires=5)
        assert future is batch.add.return_value
        _batch.get_batch.assert_called_once_with(
            _cache._GlobalCacheSetBatch, {"expires": 5}
        )
        batch.add.assert_called_once_with(b"key", b"value")


class Test_GlobalCacheSetBatch:
    @staticmethod
    def test_add_and_idle_and_done_callbacks(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheSetBatch({})
        future1 = batch.add(b"foo", b"one")
        future2 = batch.add(b"bar", b"two")

        assert batch.expires is None

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.set.assert_called_once_with(
            {b"foo": b"one", b"bar": b"two"}, expires=None
        )
        assert future1.result() is None
        assert future2.result() is None

    @staticmethod
    def test_add_and_idle_and_done_callbacks_with_expires(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheSetBatch({"expires": 5})
        future1 = batch.add(b"foo", b"one")
        future2 = batch.add(b"bar", b"two")

        assert batch.expires == 5

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.set.assert_called_once_with(
            {b"foo": b"one", b"bar": b"two"}, expires=5
        )
        assert future1.result() is None
        assert future2.result() is None

    @staticmethod
    def test_add_and_idle_and_done_callbacks_w_error(in_context):
        error = Exception("spurious error")
        cache = mock.Mock()
        cache.set.return_value = tasklets.Future()
        cache.set.return_value.set_exception(error)

        batch = _cache._GlobalCacheSetBatch({})
        future1 = batch.add(b"foo", b"one")
        future2 = batch.add(b"bar", b"two")

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.set.assert_called_once_with(
            {b"foo": b"one", b"bar": b"two"}, expires=None
        )
        assert future1.exception() is error
        assert future2.exception() is error


@mock.patch("google.cloud.ndb._cache._batch")
def test_global_delete(_batch):
    batch = _batch.get_batch.return_value
    assert _cache.global_delete(b"key") is batch.add.return_value
    _batch.get_batch.assert_called_once_with(_cache._GlobalCacheDeleteBatch)
    batch.add.assert_called_once_with(b"key")


class Test_GlobalCacheDeleteBatch:
    @staticmethod
    def test_add_and_idle_and_done_callbacks(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheDeleteBatch({})
        future1 = batch.add(b"foo")
        future2 = batch.add(b"bar")

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.delete.assert_called_once_with([b"foo", b"bar"])
        assert future1.result() is None
        assert future2.result() is None


@mock.patch("google.cloud.ndb._cache._batch")
def test_global_watch(_batch):
    batch = _batch.get_batch.return_value
    assert _cache.global_watch(b"key") is batch.add.return_value
    _batch.get_batch.assert_called_once_with(_cache._GlobalCacheWatchBatch)
    batch.add.assert_called_once_with(b"key")


class Test_GlobalCacheWatchBatch:
    @staticmethod
    def test_add_and_idle_and_done_callbacks(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheWatchBatch({})
        future1 = batch.add(b"foo")
        future2 = batch.add(b"bar")

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.watch.assert_called_once_with([b"foo", b"bar"])
        assert future1.result() is None
        assert future2.result() is None


class Test_global_compare_and_swap:
    @staticmethod
    @mock.patch("google.cloud.ndb._cache._batch")
    def test_without_expires(_batch):
        batch = _batch.get_batch.return_value
        assert (
            _cache.global_compare_and_swap(b"key", b"value")
            is batch.add.return_value
        )
        _batch.get_batch.assert_called_once_with(
            _cache._GlobalCacheCompareAndSwapBatch, {}
        )
        batch.add.assert_called_once_with(b"key", b"value")

    @staticmethod
    @mock.patch("google.cloud.ndb._cache._batch")
    def test_with_expires(_batch):
        batch = _batch.get_batch.return_value
        future = _cache.global_compare_and_swap(b"key", b"value", expires=5)
        assert future is batch.add.return_value
        _batch.get_batch.assert_called_once_with(
            _cache._GlobalCacheCompareAndSwapBatch, {"expires": 5}
        )
        batch.add.assert_called_once_with(b"key", b"value")


class Test_GlobalCacheCompareAndSwapBatch:
    @staticmethod
    def test_add_and_idle_and_done_callbacks(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheCompareAndSwapBatch({})
        future1 = batch.add(b"foo", b"one")
        future2 = batch.add(b"bar", b"two")

        assert batch.expires is None

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.compare_and_swap.assert_called_once_with(
            {b"foo": b"one", b"bar": b"two"}, expires=None
        )
        assert future1.result() is None
        assert future2.result() is None

    @staticmethod
    def test_add_and_idle_and_done_callbacks_with_expires(in_context):
        cache = mock.Mock()

        batch = _cache._GlobalCacheCompareAndSwapBatch({"expires": 5})
        future1 = batch.add(b"foo", b"one")
        future2 = batch.add(b"bar", b"two")

        assert batch.expires == 5

        with in_context.new(global_cache=cache).use():
            batch.idle_callback()

        cache.compare_and_swap.assert_called_once_with(
            {b"foo": b"one", b"bar": b"two"}, expires=5
        )
        assert future1.result() is None
        assert future2.result() is None


@mock.patch("google.cloud.ndb._cache._batch")
def test_global_lock(_batch):
    batch = _batch.get_batch.return_value
    assert _cache.global_lock(b"key") is batch.add.return_value
    _batch.get_batch.assert_called_once_with(
        _cache._GlobalCacheSetBatch, {"expires": _cache._LOCK_TIME}
    )
    batch.add.assert_called_once_with(b"key", _cache._LOCKED)


def test_is_locked_value():
    assert _cache.is_locked_value(_cache._LOCKED)
    assert not _cache.is_locked_value("new db, who dis?")


def test_global_cache_key():
    key = mock.Mock()
    key.to_protobuf.return_value.SerializeToString.return_value = b"himom!"
    assert _cache.global_cache_key(key) == _cache._PREFIX + b"himom!"
    key.to_protobuf.assert_called_once_with()
    key.to_protobuf.return_value.SerializeToString.assert_called_once_with()
