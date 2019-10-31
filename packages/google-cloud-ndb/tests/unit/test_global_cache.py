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
import redis as redis_module

from google.cloud.ndb import global_cache


class TestGlobalCache:
    def make_one(self):
        class MockImpl(global_cache.GlobalCache):
            def get(self, keys):
                return super(MockImpl, self).get(keys)

            def set(self, items, expires=None):
                return super(MockImpl, self).set(items, expires=expires)

            def delete(self, keys):
                return super(MockImpl, self).delete(keys)

            def watch(self, keys):
                return super(MockImpl, self).watch(keys)

            def compare_and_swap(self, items, expires=None):
                return super(MockImpl, self).compare_and_swap(
                    items, expires=expires
                )

        return MockImpl()

    def test_get(self):
        cache = self.make_one()
        with pytest.raises(NotImplementedError):
            cache.get(b"foo")

    def test_set(self):
        cache = self.make_one()
        with pytest.raises(NotImplementedError):
            cache.set({b"foo": "bar"})

    def test_delete(self):
        cache = self.make_one()
        with pytest.raises(NotImplementedError):
            cache.delete(b"foo")

    def test_watch(self):
        cache = self.make_one()
        with pytest.raises(NotImplementedError):
            cache.watch(b"foo")

    def test_compare_and_swap(self):
        cache = self.make_one()
        with pytest.raises(NotImplementedError):
            cache.compare_and_swap({b"foo": "bar"})


class TestInProcessGlobalCache:
    @staticmethod
    def test_set_get_delete():
        cache = global_cache._InProcessGlobalCache()
        result = cache.set({b"one": b"foo", b"two": b"bar", b"three": b"baz"})
        assert result is None

        result = cache.get([b"two", b"three", b"one"])
        assert result == [b"bar", b"baz", b"foo"]

        cache = global_cache._InProcessGlobalCache()
        result = cache.get([b"two", b"three", b"one"])
        assert result == [b"bar", b"baz", b"foo"]

        result = cache.delete([b"one", b"two", b"three"])
        assert result is None

        result = cache.get([b"two", b"three", b"one"])
        assert result == [None, None, None]

    @staticmethod
    @mock.patch("google.cloud.ndb.global_cache.time")
    def test_set_get_delete_w_expires(time):
        time.time.return_value = 0

        cache = global_cache._InProcessGlobalCache()
        result = cache.set(
            {b"one": b"foo", b"two": b"bar", b"three": b"baz"}, expires=5
        )
        assert result is None

        result = cache.get([b"two", b"three", b"one"])
        assert result == [b"bar", b"baz", b"foo"]

        time.time.return_value = 10
        result = cache.get([b"two", b"three", b"one"])
        assert result == [None, None, None]

    @staticmethod
    def test_watch_compare_and_swap():
        cache = global_cache._InProcessGlobalCache()
        result = cache.watch([b"one", b"two", b"three"])
        assert result is None

        cache.cache[b"two"] = (b"hamburgers", None)

        result = cache.compare_and_swap(
            {b"one": b"foo", b"two": b"bar", b"three": b"baz"}
        )
        assert result is None

        result = cache.get([b"one", b"two", b"three"])
        assert result == [b"foo", b"hamburgers", b"baz"]

    @staticmethod
    @mock.patch("google.cloud.ndb.global_cache.time")
    def test_watch_compare_and_swap_with_expires(time):
        time.time.return_value = 0

        cache = global_cache._InProcessGlobalCache()
        result = cache.watch([b"one", b"two", b"three"])
        assert result is None

        cache.cache[b"two"] = (b"hamburgers", None)

        result = cache.compare_and_swap(
            {b"one": b"foo", b"two": b"bar", b"three": b"baz"}, expires=5
        )
        assert result is None

        result = cache.get([b"one", b"two", b"three"])
        assert result == [b"foo", b"hamburgers", b"baz"]

        time.time.return_value = 10

        result = cache.get([b"one", b"two", b"three"])
        assert result == [None, b"hamburgers", None]


class TestRedisCache:
    @staticmethod
    def test_constructor():
        redis = object()
        cache = global_cache.RedisCache(redis)
        assert cache.redis is redis

    @staticmethod
    @mock.patch("google.cloud.ndb.global_cache.redis_module")
    def test_from_environment(redis_module):
        redis = redis_module.Redis.from_url.return_value
        with mock.patch.dict("os.environ", {"REDIS_CACHE_URL": "some://url"}):
            cache = global_cache.RedisCache.from_environment()
            assert cache.redis is redis
            redis_module.Redis.from_url.assert_called_once_with("some://url")

    @staticmethod
    def test_from_environment_not_configured():
        with mock.patch.dict("os.environ", {"REDIS_CACHE_URL": ""}):
            cache = global_cache.RedisCache.from_environment()
            assert cache is None

    @staticmethod
    def test_get():
        redis = mock.Mock(spec=("mget",))
        cache_keys = [object(), object()]
        cache_value = redis.mget.return_value
        cache = global_cache.RedisCache(redis)
        assert cache.get(cache_keys) is cache_value
        redis.mget.assert_called_once_with(cache_keys)

    @staticmethod
    def test_set():
        redis = mock.Mock(spec=("mset",))
        cache_items = {"a": "foo", "b": "bar"}
        cache = global_cache.RedisCache(redis)
        cache.set(cache_items)
        redis.mset.assert_called_once_with(cache_items)

    @staticmethod
    def test_set_w_expires():
        expired = {}

        def mock_expire(key, expires):
            expired[key] = expires

        redis = mock.Mock(expire=mock_expire, spec=("mset", "expire"))
        cache_items = {"a": "foo", "b": "bar"}
        cache = global_cache.RedisCache(redis)
        cache.set(cache_items, expires=32)
        redis.mset.assert_called_once_with(cache_items)
        assert expired == {"a": 32, "b": 32}

    @staticmethod
    def test_delete():
        redis = mock.Mock(spec=("delete",))
        cache_keys = [object(), object()]
        cache = global_cache.RedisCache(redis)
        cache.delete(cache_keys)
        redis.delete.assert_called_once_with(*cache_keys)

    @staticmethod
    @mock.patch("google.cloud.ndb.global_cache.uuid")
    def test_watch(uuid):
        uuid.uuid4.return_value = "abc123"
        redis = mock.Mock(
            pipeline=mock.Mock(spec=("watch",)), spec=("pipeline",)
        )
        pipe = redis.pipeline.return_value
        keys = ["foo", "bar"]
        cache = global_cache.RedisCache(redis)
        cache.watch(keys)

        pipe.watch.assert_called_once_with("foo", "bar")
        assert cache.pipes == {
            "foo": global_cache._Pipeline(pipe, "abc123"),
            "bar": global_cache._Pipeline(pipe, "abc123"),
        }

    @staticmethod
    def test_compare_and_swap():
        redis = mock.Mock(spec=())
        cache = global_cache.RedisCache(redis)
        pipe1 = mock.Mock(spec=("multi", "mset", "execute", "reset"))
        pipe2 = mock.Mock(spec=("multi", "mset", "execute", "reset"))
        cache.pipes = {
            "ay": global_cache._Pipeline(pipe1, "abc123"),
            "be": global_cache._Pipeline(pipe1, "abc123"),
            "see": global_cache._Pipeline(pipe2, "def456"),
            "dee": global_cache._Pipeline(pipe2, "def456"),
            "whatevs": global_cache._Pipeline(None, "himom!"),
        }
        pipe2.execute.side_effect = redis_module.exceptions.WatchError

        items = {"ay": "foo", "be": "bar", "see": "baz", "wut": "huh?"}
        cache.compare_and_swap(items)

        pipe1.multi.assert_called_once_with()
        pipe2.multi.assert_called_once_with()
        pipe1.mset.assert_called_once_with({"ay": "foo", "be": "bar"})
        pipe2.mset.assert_called_once_with({"see": "baz"})
        pipe1.execute.assert_called_once_with()
        pipe2.execute.assert_called_once_with()
        pipe1.reset.assert_called_once_with()
        pipe2.reset.assert_called_once_with()

        assert cache.pipes == {
            "whatevs": global_cache._Pipeline(None, "himom!")
        }

    @staticmethod
    def test_compare_and_swap_w_expires():
        expired = {}

        def mock_expire(key, expires):
            expired[key] = expires

        redis = mock.Mock(spec=())
        cache = global_cache.RedisCache(redis)
        pipe1 = mock.Mock(
            expire=mock_expire,
            spec=("multi", "mset", "execute", "expire", "reset"),
        )
        pipe2 = mock.Mock(
            expire=mock_expire,
            spec=("multi", "mset", "execute", "expire", "reset"),
        )
        cache.pipes = {
            "ay": global_cache._Pipeline(pipe1, "abc123"),
            "be": global_cache._Pipeline(pipe1, "abc123"),
            "see": global_cache._Pipeline(pipe2, "def456"),
            "dee": global_cache._Pipeline(pipe2, "def456"),
            "whatevs": global_cache._Pipeline(None, "himom!"),
        }
        pipe2.execute.side_effect = redis_module.exceptions.WatchError

        items = {"ay": "foo", "be": "bar", "see": "baz", "wut": "huh?"}
        cache.compare_and_swap(items, expires=32)

        pipe1.multi.assert_called_once_with()
        pipe2.multi.assert_called_once_with()
        pipe1.mset.assert_called_once_with({"ay": "foo", "be": "bar"})
        pipe2.mset.assert_called_once_with({"see": "baz"})
        pipe1.execute.assert_called_once_with()
        pipe2.execute.assert_called_once_with()
        pipe1.reset.assert_called_once_with()
        pipe2.reset.assert_called_once_with()

        assert cache.pipes == {
            "whatevs": global_cache._Pipeline(None, "himom!")
        }
        assert expired == {"ay": 32, "be": 32, "see": 32}
