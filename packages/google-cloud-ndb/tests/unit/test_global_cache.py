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

from unittest import mock

import pytest

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
