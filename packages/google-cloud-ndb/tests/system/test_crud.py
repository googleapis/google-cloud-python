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

"""
System tests for Create, Update, Delete. (CRUD)
"""
import datetime
import functools
import operator
import os
import random
import threading
import zlib

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

import test_utils.system

from google.cloud import ndb
from google.cloud.ndb import _cache
from google.cloud.ndb import global_cache as global_cache_module

from tests.system import KIND, eventually

USE_REDIS_CACHE = bool(os.environ.get("REDIS_CACHE_URL"))


def _equals(n):
    return functools.partial(operator.eq, n)


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none", baz=b"night")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.StringProperty()

    key = ndb.Key(KIND, entity_id)
    entity = key.get()
    assert isinstance(entity, SomeKind)
    assert entity.foo == 42
    assert entity.bar == "none"
    assert entity.baz == "night"


def test_retrieve_entity_with_caching(ds_entity, client_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none", baz=b"night")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.StringProperty()

    client_context.set_cache_policy(None)  # Use default

    key = ndb.Key(KIND, entity_id)
    entity = key.get()
    assert isinstance(entity, SomeKind)
    assert entity.foo == 42
    assert entity.bar == "none"
    assert entity.baz == "night"

    assert key.get() is entity


def test_retrieve_entity_with_global_cache(ds_entity, client_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none", baz=b"night")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.StringProperty()

    global_cache = global_cache_module._InProcessGlobalCache()
    cache_dict = global_cache_module._InProcessGlobalCache.cache
    with client_context.new(global_cache=global_cache).use() as context:
        context.set_global_cache_policy(None)  # Use default

        key = ndb.Key(KIND, entity_id)
        entity = key.get()
        assert isinstance(entity, SomeKind)
        assert entity.foo == 42
        assert entity.bar == "none"
        assert entity.baz == "night"

        cache_key = _cache.global_cache_key(key._key)
        assert cache_key in cache_dict

        patch = mock.patch("google.cloud.ndb._datastore_api._LookupBatch.add")
        patch.side_effect = Exception("Shouldn't call this")
        with patch:
            entity = key.get()
            assert isinstance(entity, SomeKind)
            assert entity.foo == 42
            assert entity.bar == "none"
            assert entity.baz == "night"


@pytest.mark.skipif(not USE_REDIS_CACHE, reason="Redis is not configured")
def test_retrieve_entity_with_redis_cache(ds_entity, redis_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none", baz=b"night")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.StringProperty()

    key = ndb.Key(KIND, entity_id)
    entity = key.get()
    assert isinstance(entity, SomeKind)
    assert entity.foo == 42
    assert entity.bar == "none"
    assert entity.baz == "night"

    cache_key = _cache.global_cache_key(key._key)
    assert redis_context.global_cache.redis.get(cache_key) is not None

    patch = mock.patch("google.cloud.ndb._datastore_api._LookupBatch.add")
    patch.side_effect = Exception("Shouldn't call this")
    with patch:
        entity = key.get()
        assert isinstance(entity, SomeKind)
        assert entity.foo == 42
        assert entity.bar == "none"
        assert entity.baz == "night"


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity_not_found(ds_entity):
    entity_id = test_utils.system.unique_resource_id()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    key = ndb.Key(KIND, entity_id)
    assert key.get() is None


@pytest.mark.usefixtures("client_context")
def test_nested_tasklet(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    @ndb.tasklet
    def get_foo(key):
        entity = yield key.get_async()
        raise ndb.Return(entity.foo)

    key = ndb.Key(KIND, entity_id)
    assert get_foo(key).result() == 42


@pytest.mark.usefixtures("client_context")
def test_retrieve_two_entities_in_parallel(ds_entity):
    entity1_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity1_id, foo=42, bar="none")
    entity2_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity2_id, foo=65, bar="naan")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    key1 = ndb.Key(KIND, entity1_id)
    key2 = ndb.Key(KIND, entity2_id)

    @ndb.tasklet
    def get_two_entities():
        entity1, entity2 = yield key1.get_async(), key2.get_async()
        raise ndb.Return(entity1, entity2)

    entity1, entity2 = get_two_entities().result()

    assert isinstance(entity1, SomeKind)
    assert entity1.foo == 42
    assert entity1.bar == "none"

    assert isinstance(entity2, SomeKind)
    assert entity2.foo == 65
    assert entity2.bar == "naan"


@pytest.mark.usefixtures("client_context")
def test_retrieve_entities_in_parallel_nested(ds_entity):
    """Regression test for #357.

    https://github.com/googleapis/python-ndb/issues/357
    """
    entity1_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity1_id, foo=42, bar="none")
    entity2_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity2_id, foo=65, bar="naan")
    entity3_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity3_id, foo=66, bar="route")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    key1 = ndb.Key(KIND, entity1_id)
    key2 = ndb.Key(KIND, entity2_id)
    key3 = ndb.Key(KIND, entity3_id)

    @ndb.tasklet
    def get_two_entities():
        entity1, (entity2, entity3) = yield (
            key1.get_async(),
            [key2.get_async(), key3.get_async()],
        )
        raise ndb.Return(entity1, entity2, entity3)

    entity1, entity2, entity3 = get_two_entities().result()

    assert isinstance(entity1, SomeKind)
    assert entity1.foo == 42
    assert entity1.bar == "none"

    assert isinstance(entity2, SomeKind)
    assert entity2.foo == 65
    assert entity2.bar == "naan"

    assert isinstance(entity3, SomeKind)
    assert entity3.foo == 66
    assert entity3.bar == "route"


@pytest.mark.usefixtures("client_context")
def test_insert_entity(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    entity = SomeKind(foo=42, bar="none")
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar == "none"

    # Make sure strings are stored as strings in datastore
    ds_entity = ds_client.get(key._key)
    assert ds_entity["bar"] == "none"


@pytest.mark.usefixtures("client_context")
def test_insert_entity_with_stored_name_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.StringProperty()
        bar = ndb.StringProperty(name="notbar")

    entity = SomeKind(foo="something", bar="or other")
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == "something"
    assert retrieved.bar == "or other"

    ds_entity = ds_client.get(key._key)
    assert ds_entity["notbar"] == "or other"


@pytest.mark.usefixtures("client_context")
def test_insert_roundtrip_naive_datetime(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.DateTimeProperty()

    entity = SomeKind(foo=datetime.datetime(2010, 5, 12, 2, 42))
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == datetime.datetime(2010, 5, 12, 2, 42)


@pytest.mark.usefixtures("client_context")
def test_datetime_w_tzinfo(dispose_of, ds_client):
    class timezone(datetime.tzinfo):
        def __init__(self, offset):
            self.offset = datetime.timedelta(hours=offset)

        def utcoffset(self, dt):
            return self.offset

        def dst(self, dt):
            return datetime.timedelta(0)

    mytz = timezone(-4)

    class SomeKind(ndb.Model):
        foo = ndb.DateTimeProperty(tzinfo=mytz)
        bar = ndb.DateTimeProperty(tzinfo=mytz)

    entity = SomeKind(
        foo=datetime.datetime(2010, 5, 12, 2, 42, tzinfo=timezone(-5)),
        bar=datetime.datetime(2010, 5, 12, 2, 42),
    )
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == datetime.datetime(2010, 5, 12, 3, 42, tzinfo=mytz)
    assert retrieved.bar == datetime.datetime(2010, 5, 11, 22, 42, tzinfo=mytz)


def test_parallel_threads(dispose_of, namespace):
    client = ndb.Client(namespace=namespace)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    def insert(foo):
        with client.context(cache_policy=False):
            entity = SomeKind(foo=foo, bar="none")

            key = entity.put()
            dispose_of(key._key)

            retrieved = key.get()
            assert retrieved.foo == foo
            assert retrieved.bar == "none"

    thread1 = threading.Thread(target=insert, args=[42], name="one")
    thread2 = threading.Thread(target=insert, args=[144], name="two")

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


@pytest.mark.usefixtures("client_context")
def test_large_json_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.JsonProperty()

    foo = {str(i): i for i in range(500)}
    entity = SomeKind(foo=foo)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == foo


@pytest.mark.usefixtures("client_context")
def test_compressed_json_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.JsonProperty(compressed=True)

    foo = {str(i): i for i in range(500)}
    entity = SomeKind(foo=foo)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == foo


@pytest.mark.usefixtures("client_context")
def test_compressed_blob_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.BlobProperty(compressed=True)

    foo = b"abc" * 100
    entity = SomeKind(foo=foo)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == foo


@pytest.mark.usefixtures("client_context")
def test_compressed_repeated_local_structured_property(dispose_of, ds_client):
    class Dog(ndb.Model):
        name = ndb.StringProperty()

    class House(ndb.Model):
        dogs = ndb.LocalStructuredProperty(Dog, repeated=True, compressed=True)

    entity = House()
    dogs = [Dog(name="Mika"), Dog(name="Mocha")]
    entity.dogs = dogs

    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.dogs == dogs


def test_get_by_id_with_compressed_repeated_local_structured_property(
    client_context, dispose_of, ds_client
):
    class Dog(ndb.Model):
        name = ndb.TextProperty()

    class House(ndb.Model):
        dogs = ndb.LocalStructuredProperty(Dog, repeated=True, compressed=True)

    with client_context.new(legacy_data=True).use():
        entity = House()
        dogs = [Dog(name="Mika"), Dog(name="Mocha")]
        entity.dogs = dogs

        key = entity.put()
        house_id = key.id()
        dispose_of(key._key)

        retrieved = House.get_by_id(house_id)
        assert retrieved.dogs == dogs


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity_with_legacy_compressed_property(
    ds_entity_with_meanings,
):
    class SomeKind(ndb.Model):
        blob = ndb.BlobProperty()

    value = b"abc" * 1000
    compressed_value = zlib.compress(value)
    entity_id = test_utils.system.unique_resource_id()
    ds_entity_with_meanings(
        {"blob": (22, compressed_value)},
        KIND,
        entity_id,
        **{"blob": compressed_value}
    )

    key = ndb.Key(KIND, entity_id)
    retrieved = key.get()
    assert retrieved.blob == value


@pytest.mark.usefixtures("client_context")
def test_large_pickle_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.PickleProperty()

    foo = {str(i): i for i in range(500)}
    entity = SomeKind(foo=foo)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == foo


@pytest.mark.usefixtures("client_context")
def test_key_property(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.KeyProperty()

    key_value = ndb.Key("Whatevs", 123)
    entity = SomeKind(foo=key_value)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == key_value


@pytest.mark.usefixtures("client_context")
def test_multiple_key_properties(dispose_of, ds_client):
    class SomeKind(ndb.Model):
        foo = ndb.KeyProperty(kind="Whatevs")
        bar = ndb.KeyProperty(kind="Whatevs")

    foo = ndb.Key("Whatevs", 123)
    bar = ndb.Key("Whatevs", 321)
    entity = SomeKind(foo=foo, bar=bar)
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == foo
    assert retrieved.bar == bar
    assert retrieved.foo != retrieved.bar


def test_insert_entity_with_caching(client_context):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    client_context.set_cache_policy(None)  # Use default

    entity = SomeKind(foo=42, bar="none")
    key = entity.put()

    with client_context.new(cache_policy=False).use():
        # Sneaky. Delete entity out from under cache so we know we're getting
        # cached copy.
        key.delete()
        eventually(key.get, _equals(None))

    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar == "none"


def test_insert_entity_with_global_cache(dispose_of, client_context):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    global_cache = global_cache_module._InProcessGlobalCache()
    cache_dict = global_cache_module._InProcessGlobalCache.cache
    with client_context.new(global_cache=global_cache).use() as context:
        context.set_global_cache_policy(None)  # Use default

        entity = SomeKind(foo=42, bar="none")
        key = entity.put()
        dispose_of(key._key)
        cache_key = _cache.global_cache_key(key._key)
        assert not cache_dict

        retrieved = key.get()
        assert retrieved.foo == 42
        assert retrieved.bar == "none"

        assert cache_key in cache_dict

        entity.foo = 43
        entity.put()

        # This is py27 behavior. I can see a case being made for caching the
        # entity on write rather than waiting for a subsequent lookup.
        assert cache_key not in cache_dict


@pytest.mark.skipif(not USE_REDIS_CACHE, reason="Redis is not configured")
def test_insert_entity_with_redis_cache(dispose_of, redis_context):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    entity = SomeKind(foo=42, bar="none")
    key = entity.put()
    dispose_of(key._key)
    cache_key = _cache.global_cache_key(key._key)
    assert redis_context.global_cache.redis.get(cache_key) is None

    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar == "none"

    assert redis_context.global_cache.redis.get(cache_key) is not None

    entity.foo = 43
    entity.put()

    # This is py27 behavior. I can see a case being made for caching the
    # entity on write rather than waiting for a subsequent lookup.
    assert redis_context.global_cache.redis.get(cache_key) is None


@pytest.mark.usefixtures("client_context")
def test_update_entity(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    key = ndb.Key(KIND, entity_id)
    entity = key.get()
    entity.foo = 56
    entity.bar = "high"
    assert entity.put() == key

    retrieved = key.get()
    assert retrieved.foo == 56
    assert retrieved.bar == "high"


@pytest.mark.usefixtures("client_context")
def test_insert_entity_in_transaction(dispose_of):
    commit_callback = mock.Mock()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    def save_entity():
        ndb.get_context().call_on_commit(commit_callback)
        entity = SomeKind(foo=42, bar="none")
        key = entity.put()
        dispose_of(key._key)
        return key

    key = ndb.transaction(save_entity)
    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar == "none"
    commit_callback.assert_called_once_with()


@pytest.mark.usefixtures("client_context")
def test_update_entity_in_transaction(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42, bar="none")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    def update_entity():
        key = ndb.Key(KIND, entity_id)
        entity = key.get()
        entity.foo = 56
        entity.bar = "high"
        assert entity.put() == key
        return key

    key = ndb.transaction(update_entity)
    retrieved = key.get()
    assert retrieved.foo == 56
    assert retrieved.bar == "high"


@pytest.mark.usefixtures("client_context")
def test_parallel_transactions():
    def task(delay):
        @ndb.tasklet
        def callback():
            transaction = ndb.get_context().transaction
            yield ndb.sleep(delay)
            assert ndb.get_context().transaction == transaction
            raise ndb.Return(transaction)

        return callback

    future1 = ndb.transaction_async(task(0.1))
    future2 = ndb.transaction_async(task(0.06))
    ndb.wait_all((future1, future2))
    assert future1.get_result() != future2.get_result()


@pytest.mark.usefixtures("client_context")
def test_delete_entity(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    key = ndb.Key(KIND, entity_id)
    assert key.get().foo == 42

    assert key.delete() is None
    assert key.get() is None
    assert key.delete() is None


def test_delete_entity_with_caching(ds_entity, client_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    client_context.set_cache_policy(None)  # Use default

    key = ndb.Key(KIND, entity_id)
    assert key.get().foo == 42

    assert key.delete() is None
    assert key.get() is None
    assert key.delete() is None


def test_delete_entity_with_global_cache(ds_entity, client_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    key = ndb.Key(KIND, entity_id)
    cache_key = _cache.global_cache_key(key._key)
    global_cache = global_cache_module._InProcessGlobalCache()
    cache_dict = global_cache_module._InProcessGlobalCache.cache

    with client_context.new(global_cache=global_cache).use():
        assert key.get().foo == 42
        assert cache_key in cache_dict

        assert key.delete() is None
        assert cache_key not in cache_dict

        # This is py27 behavior. Not entirely sold on leaving _LOCKED value for
        # Datastore misses.
        assert key.get() is None
        assert cache_dict[cache_key][0] == b"0"


@pytest.mark.skipif(not USE_REDIS_CACHE, reason="Redis is not configured")
def test_delete_entity_with_redis_cache(ds_entity, redis_context):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    key = ndb.Key(KIND, entity_id)
    cache_key = _cache.global_cache_key(key._key)

    assert key.get().foo == 42
    assert redis_context.global_cache.redis.get(cache_key) is not None

    assert key.delete() is None
    assert redis_context.global_cache.redis.get(cache_key) is None

    # This is py27 behavior. Not entirely sold on leaving _LOCKED value for
    # Datastore misses.
    assert key.get() is None
    assert redis_context.global_cache.redis.get(cache_key) == b"0"


@pytest.mark.usefixtures("client_context")
def test_delete_entity_in_transaction(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    key = ndb.Key(KIND, entity_id)
    assert key.get().foo == 42

    def delete_entity():
        assert key.delete() is None
        assert key.get().foo == 42  # not deleted until commit

    ndb.transaction(delete_entity)
    assert key.get() is None


@pytest.mark.usefixtures("client_context")
def test_delete_entity_in_transaction_then_rollback(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    key = ndb.Key(KIND, entity_id)
    assert key.get().foo == 42

    def delete_entity():
        assert key.delete() is None
        raise Exception("Spurious error")

    with pytest.raises(Exception):
        ndb.transaction(delete_entity)

    assert key.get().foo == 42


@pytest.mark.usefixtures("client_context")
def test_allocate_ids():
    class SomeKind(ndb.Model):
        pass

    keys = SomeKind.allocate_ids(5)
    assert len(keys) == 5

    for key in keys:
        assert key.id()
        assert key.get() is None


@pytest.mark.usefixtures("client_context")
def test_get_by_id(ds_entity):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=42)

    key = ndb.Key(KIND, entity_id)
    assert key.get().foo == 42

    entity = SomeKind.get_by_id(entity_id)
    assert entity.foo == 42


@pytest.mark.usefixtures("client_context")
def test_get_or_insert_get(ds_entity):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    name = "Inigo Montoya"
    assert SomeKind.get_by_id(name) is None

    ds_entity(KIND, name, foo=42)
    entity = SomeKind.get_or_insert(name, foo=21)
    assert entity.foo == 42


@pytest.mark.usefixtures("client_context")
def test_get_or_insert_insert(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    name = "Inigo Montoya"
    assert SomeKind.get_by_id(name) is None

    entity = SomeKind.get_or_insert(name, foo=21)
    dispose_of(entity._key._key)
    assert entity.foo == 21


@pytest.mark.usefixtures("client_context")
def test_get_or_insert_get_in_transaction(ds_entity):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    name = "Inigo Montoya"
    assert SomeKind.get_by_id(name) is None

    def do_the_thing():
        ds_entity(KIND, name, foo=42)
        return SomeKind.get_or_insert(name, foo=21)

    entity = ndb.transaction(do_the_thing)
    assert entity.foo == 42


@pytest.mark.usefixtures("client_context")
def test_insert_entity_with_structured_property(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    entity = SomeKind(foo=42, bar=OtherKind(one="hi", two="mom"))
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar.one == "hi"
    assert retrieved.bar.two == "mom"

    assert isinstance(retrieved.bar, OtherKind)


def test_insert_entity_with_structured_property_legacy_data(
    client_context, dispose_of, ds_client
):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    with client_context.new(legacy_data=True).use():
        entity = SomeKind(foo=42, bar=OtherKind(one="hi", two="mom"))
        key = entity.put()
        dispose_of(key._key)

        retrieved = key.get()
        assert retrieved.foo == 42
        assert retrieved.bar.one == "hi"
        assert retrieved.bar.two == "mom"

        assert isinstance(retrieved.bar, OtherKind)

        ds_entity = ds_client.get(key._key)
        assert ds_entity["foo"] == 42
        assert ds_entity["bar.one"] == "hi"
        assert ds_entity["bar.two"] == "mom"


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity_with_legacy_structured_property(ds_entity):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND, entity_id, **{"foo": 42, "bar.one": "hi", "bar.two": "mom"}
    )

    key = ndb.Key(KIND, entity_id)
    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar.one == "hi"
    assert retrieved.bar.two == "mom"

    assert isinstance(retrieved.bar, OtherKind)


@pytest.mark.usefixtures("client_context")
def test_retrieve_entity_with_legacy_repeated_structured_property(ds_entity):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{"foo": 42, "bar.one": ["hi", "hello"], "bar.two": ["mom", "dad"]}
    )

    key = ndb.Key(KIND, entity_id)
    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.bar[0].one == "hi"
    assert retrieved.bar[0].two == "mom"
    assert retrieved.bar[1].one == "hello"
    assert retrieved.bar[1].two == "dad"

    assert isinstance(retrieved.bar[0], OtherKind)
    assert isinstance(retrieved.bar[1], OtherKind)


@pytest.mark.usefixtures("client_context")
def test_insert_expando(dispose_of):
    class SomeKind(ndb.Expando):
        foo = ndb.IntegerProperty()

    entity = SomeKind(foo=42)
    entity.expando_prop = "exp-value"
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == 42
    assert retrieved.expando_prop == "exp-value"


@pytest.mark.usefixtures("client_context")
def test_insert_polymodel(dispose_of):
    class Animal(ndb.PolyModel):
        one = ndb.StringProperty()

    class Feline(Animal):
        two = ndb.StringProperty()

    class Cat(Feline):
        three = ndb.StringProperty()

    entity = Cat(one="hello", two="dad", three="i'm in jail")
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()

    assert isinstance(retrieved, Animal)
    assert isinstance(retrieved, Cat)
    assert retrieved.one == "hello"
    assert retrieved.two == "dad"
    assert retrieved.three == "i'm in jail"


@pytest.mark.usefixtures("client_context")
def test_insert_autonow_property(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.StringProperty()
        created_at = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
        updated_at = ndb.DateTimeProperty(indexed=True, auto_now=True)

    entity = SomeKind(foo="bar")
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()

    assert isinstance(retrieved.created_at, datetime.datetime)
    assert isinstance(retrieved.updated_at, datetime.datetime)


@pytest.mark.usefixtures("client_context")
def test_insert_nested_autonow_property(dispose_of):
    class OtherKind(ndb.Model):
        created_at = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
        updated_at = ndb.DateTimeProperty(indexed=True, auto_now=True)

    class SomeKind(ndb.Model):
        other = ndb.StructuredProperty(OtherKind)

    entity = SomeKind(other=OtherKind())
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()

    assert isinstance(retrieved.other.created_at, datetime.datetime)
    assert isinstance(retrieved.other.updated_at, datetime.datetime)


@pytest.mark.usefixtures("client_context")
def test_uninitialized_property(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.StringProperty(required=True)

    entity = SomeKind()

    with pytest.raises(ndb.exceptions.BadValueError):
        entity.put()


@mock.patch(
    "google.cloud.ndb._datastore_api.make_call",
    mock.Mock(side_effect=Exception("Datastore shouldn't get called.")),
)
def test_crud_without_datastore(ds_entity, client_context):
    entity_id = test_utils.system.unique_resource_id()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.StringProperty()

    global_cache = global_cache_module._InProcessGlobalCache()
    with client_context.new(global_cache=global_cache).use() as context:
        context.set_global_cache_policy(None)  # Use default
        context.set_datastore_policy(False)  # Don't use Datastore

        key = ndb.Key(KIND, entity_id)
        SomeKind(foo=42, bar="none", baz="night", _key=key).put()

        entity = key.get()
        assert isinstance(entity, SomeKind)
        assert entity.foo == 42
        assert entity.bar == "none"
        assert entity.baz == "night"

        key.delete()
        assert key.get() is None


@pytest.mark.usefixtures("client_context")
def test_computed_key_property(dispose_of):
    """Regression test for #284.

    https://github.com/googleapis/python-ndb/issues/284
    """

    class AModel(ndb.Model):
        s_foo = ndb.StringProperty()

    class BModel(ndb.Model):
        s_bar = ndb.StringProperty()
        key_a = ndb.KeyProperty(kind="AModel", indexed=True)

    class CModel(ndb.Model):
        s_foobar = ndb.StringProperty()
        key_b = ndb.KeyProperty(kind="BModel", indexed=True)
        key_a = ndb.ComputedProperty(  # Issue here
            lambda self: self.key_b.get().key_a if self.key_b else None,
        )

    key_a = AModel(s_foo="test").put()
    dispose_of(key_a._key)
    key_b = BModel(s_bar="test", key_a=key_a).put()
    dispose_of(key_b._key)
    key_c = CModel(s_foobar="test", key_b=key_b).put()
    dispose_of(key_c._key)

    entity = key_c.get()
    assert entity.key_a == key_a
    assert entity.key_b == key_b


@pytest.mark.usefixtures("client_context")
def test_user_property(dispose_of):
    class SomeKind(ndb.Model):
        user = ndb.UserProperty()

    user = ndb.User("somebody@example.com", "gmail.com")
    entity = SomeKind(user=user)
    key = entity.put()
    dispose_of(key._key)

    retreived = key.get()
    assert retreived.user.email() == "somebody@example.com"
    assert retreived.user.auth_domain() == "gmail.com"


@pytest.mark.usefixtures("client_context")
def test_user_property_different_user_class(dispose_of):
    class SomeKind(ndb.Model):
        user = ndb.UserProperty()

    class User(object):
        def email(self):
            return "somebody@example.com"

        def auth_domain(self):
            return "gmail.com"

        def user_id(self):
            return None

    entity = SomeKind(user=User())
    key = entity.put()
    dispose_of(key._key)

    retreived = key.get()
    assert retreived.user.email() == "somebody@example.com"
    assert retreived.user.auth_domain() == "gmail.com"


@pytest.mark.usefixtures("client_context")
def test_repeated_empty_strings(dispose_of):
    """Regression test for issue # 300.

    https://github.com/googleapis/python-ndb/issues/300
    """

    class SomeKind(ndb.Model):
        foo = ndb.StringProperty(repeated=True)

    entity = SomeKind(foo=["", ""])
    key = entity.put()
    dispose_of(key._key)

    retreived = key.get()
    assert retreived.foo == ["", ""]


@pytest.mark.usefixtures("redis_context")
def test_multi_get_weirdness_with_redis(dispose_of):
    """Regression test for issue #294.

    https://github.com/googleapis/python-ndb/issues/294
    """

    class SomeKind(ndb.Model):
        foo = ndb.StringProperty()

    objects = [SomeKind(foo=str(i)) for i in range(10)]
    keys = ndb.put_multi(objects)
    for key in keys:
        dispose_of(key._key)
    ndb.get_multi(keys)

    one_object = random.choice(keys).get()
    one_object.foo = "CHANGED"
    one_object.put()

    objects_upd = ndb.get_multi(keys)
    keys_upd = [obj.key for obj in objects_upd]
    assert len(keys_upd) == len(keys)
    assert len(set(keys_upd)) == len(set(keys))
    assert set(keys_upd) == set(keys)


@pytest.mark.usefixtures("client_context")
def test_multi_with_lots_of_keys(dispose_of):
    """Regression test for issue #318.

    https://github.com/googleapis/python-ndb/issues/318
    """
    N = 1001

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    foos = list(range(N))
    entities = [SomeKind(foo=foo) for foo in foos]
    keys = ndb.put_multi(entities)
    dispose_of(*(key._key for key in keys))
    assert len(keys) == N

    entities = ndb.get_multi(keys)
    assert [entity.foo for entity in entities] == foos

    ndb.delete_multi(keys)
    entities = ndb.get_multi(keys)
    assert entities == [None] * N


@pytest.mark.usefixtures("client_context")
def test_allocate_a_lot_of_keys():
    N = 1001

    class SomeKind(ndb.Model):
        pass

    keys = SomeKind.allocate_ids(N)
    assert len(keys) == N


@pytest.mark.usefixtures("client_context")
def test_delete_multi_with_transactional(dispose_of):
    """Regression test for issue #271

    https://github.com/googleapis/python-ndb/issues/271
    """
    N = 10

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.transactional()
    def delete_them(entities):
        ndb.delete_multi([entity.key for entity in entities])

    foos = list(range(N))
    entities = [SomeKind(foo=foo) for foo in foos]
    keys = ndb.put_multi(entities)
    dispose_of(*(key._key for key in keys))

    entities = ndb.get_multi(keys)
    assert [entity.foo for entity in entities] == foos

    assert delete_them(entities) is None
    entities = ndb.get_multi(keys)
    assert entities == [None] * N


@pytest.mark.usefixtures("client_context")
def test_compressed_text_property(dispose_of, ds_client):
    """Regression test for #277

    https://github.com/googleapis/python-ndb/issues/277
    """

    class SomeKind(ndb.Model):
        foo = ndb.TextProperty(compressed=True)

    entity = SomeKind(foo="Compress this!")
    key = entity.put()
    dispose_of(key._key)

    retrieved = key.get()
    assert retrieved.foo == "Compress this!"

    ds_entity = ds_client.get(key._key)
    assert zlib.decompress(ds_entity["foo"]) == b"Compress this!"


def test_insert_entity_with_repeated_local_structured_property_legacy_data(
    client_context, dispose_of, ds_client
):
    """Regression test for #326

    https://github.com/googleapis/python-ndb/issues/326
    """

    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.LocalStructuredProperty(OtherKind, repeated=True)

    with client_context.new(legacy_data=True).use():
        entity = SomeKind(
            foo=42,
            bar=[
                OtherKind(one="hi", two="mom"),
                OtherKind(one="and", two="dad"),
            ],
        )
        key = entity.put()
        dispose_of(key._key)

        retrieved = key.get()
        assert retrieved.foo == 42
        assert retrieved.bar[0].one == "hi"
        assert retrieved.bar[0].two == "mom"
        assert retrieved.bar[1].one == "and"
        assert retrieved.bar[1].two == "dad"

        assert isinstance(retrieved.bar[0], OtherKind)
        assert isinstance(retrieved.bar[1], OtherKind)


def test_insert_structured_property_with_unindexed_subproperty_legacy_data(
    client_context, dispose_of, ds_client
):
    """Regression test for #341

    https://github.com/googleapis/python-ndb/issues/341
    """

    class OtherKind(ndb.Model):
        data = ndb.BlobProperty(indexed=False)

    class SomeKind(ndb.Model):
        entry = ndb.StructuredProperty(OtherKind)

    with client_context.new(legacy_data=True).use():
        entity = SomeKind(entry=OtherKind(data=b"01234567890" * 1000))
        key = entity.put()
        dispose_of(key._key)

        retrieved = key.get()
        assert isinstance(retrieved.entry, OtherKind)
