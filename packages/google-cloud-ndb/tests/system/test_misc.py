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
Difficult to classify regression tests.
"""
import os
import pickle

import pytest

from google.cloud import ndb

USE_REDIS_CACHE = bool(os.environ.get("REDIS_CACHE_URL"))


# Pickle can only pickle/unpickle global classes
class PickleOtherKind(ndb.Model):
    foo = ndb.IntegerProperty()

    @classmethod
    def _get_kind(cls):
        return "OtherKind"


class PickleSomeKind(ndb.Model):
    other = ndb.StructuredProperty(PickleOtherKind)

    @classmethod
    def _get_kind(cls):
        return "SomeKind"


@pytest.mark.usefixtures("client_context")
def test_pickle_roundtrip_structured_property(dispose_of):
    """Regression test for Issue #281.

    https://github.com/googleapis/python-ndb/issues/281
    """
    ndb.Model._kind_map["SomeKind"] = PickleSomeKind
    ndb.Model._kind_map["OtherKind"] = PickleOtherKind

    entity = PickleSomeKind(other=PickleOtherKind(foo=1))
    key = entity.put()
    dispose_of(key._key)

    entity = key.get(use_cache=False)
    assert entity.other.key is None or entity.other.key.id() is None
    entity = pickle.loads(pickle.dumps(entity))
    assert entity.other.foo == 1


@pytest.mark.usefixtures("client_context")
def test_tasklet_yield_emtpy_list():
    """Regression test for Issue #353.

    https://github.com/googleapis/python-ndb/issues/353
    """

    @ndb.tasklet
    def test_it():
        nothing = yield []
        raise ndb.Return(nothing)

    assert test_it().result() == ()


@pytest.mark.usefixtures("client_context")
def test_transactional_composable(dispose_of):
    """Regression test for Issue #366.

    https://github.com/googleapis/python-ndb/issues/366
    """

    class OtherKind(ndb.Model):
        bar = ndb.IntegerProperty()

    class SomeKind(ndb.Model):
        foos = ndb.KeyProperty(repeated=True)
        bar = ndb.IntegerProperty(default=42)

    others = [OtherKind(bar=bar) for bar in range(5)]
    other_keys = ndb.put_multi(others)
    for key in other_keys:
        dispose_of(key._key)

    entity = SomeKind(foos=other_keys[1:])
    entity_key = entity.put()
    dispose_of(entity_key._key)

    @ndb.transactional()
    def get_entities(*keys):
        entities = []
        for entity in ndb.get_multi(keys):
            entities.append(entity)
            if isinstance(entity, SomeKind):
                entities.extend(get_foos(entity))

        return entities

    @ndb.transactional()
    def get_foos(entity):
        return ndb.get_multi(entity.foos)

    results = get_entities(entity_key, other_keys[0])
    assert [result.bar for result in results] == [42, 1, 2, 3, 4, 0]


@pytest.mark.usefixtures("client_context")
def test_parallel_transactions(dispose_of):
    """Regression test for Issue #394

    https://github.com/googleapis/python-ndb/issues/394
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.transactional_tasklet()
    def update(id, add, delay=0):
        entity = yield SomeKind.get_by_id_async(id)
        foo = entity.foo
        foo += add

        yield ndb.sleep(delay)
        entity.foo = foo

        yield entity.put_async()

    @ndb.tasklet
    def concurrent_tasks(id):
        yield [
            update(id, 100),
            update(id, 100, 0.01),
        ]

    key = SomeKind(foo=42).put()
    dispose_of(key._key)
    id = key.id()

    concurrent_tasks(id).get_result()

    entity = SomeKind.get_by_id(id)
    assert entity.foo == 242


def test_parallel_transactions_w_context_cache(client_context, dispose_of):
    """Regression test for Issue #394

    https://github.com/googleapis/python-ndb/issues/394
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.transactional_tasklet()
    def update(id, add, delay=0):
        entity = yield SomeKind.get_by_id_async(id)
        foo = entity.foo
        foo += add

        yield ndb.sleep(delay)
        entity.foo = foo

        yield entity.put_async()

    @ndb.tasklet
    def concurrent_tasks(id):
        yield [
            update(id, 100),
            update(id, 100, 0.01),
        ]

    with client_context.new(cache_policy=None).use():
        key = SomeKind(foo=42).put()
        dispose_of(key._key)
        id = key.id()

        concurrent_tasks(id).get_result()

        entity = SomeKind.get_by_id(id)
        assert entity.foo == 242


@pytest.mark.skipif(not USE_REDIS_CACHE, reason="Redis is not configured")
@pytest.mark.usefixtures("redis_context")
def test_parallel_transactions_w_redis_cache(dispose_of):
    """Regression test for Issue #394

    https://github.com/googleapis/python-ndb/issues/394
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.transactional_tasklet()
    def update(id, add, delay=0):
        entity = yield SomeKind.get_by_id_async(id)
        foo = entity.foo
        foo += add

        yield ndb.sleep(delay)
        entity.foo = foo

        yield entity.put_async()

    @ndb.tasklet
    def concurrent_tasks(id):
        yield [
            update(id, 100),
            update(id, 100, 0.01),
        ]

    key = SomeKind(foo=42).put()
    dispose_of(key._key)
    id = key.id()

    SomeKind.get_by_id(id)
    concurrent_tasks(id).get_result()

    entity = SomeKind.get_by_id(id)
    assert entity.foo == 242


def test_rollback_with_context_cache(client_context, dispose_of):
    """Regression test for Issue #398

    https://github.com/googleapis/python-ndb/issues/398
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    class SpuriousError(Exception):
        pass

    @ndb.transactional()
    def update(id, add, fail=False):
        entity = SomeKind.get_by_id(id)
        entity.foo = entity.foo + add
        entity.put()

        if fail:
            raise SpuriousError()

    with client_context.new(cache_policy=None).use():
        key = SomeKind(foo=42).put()
        dispose_of(key._key)
        id = key.id()

        update(id, 100)

        entity = SomeKind.get_by_id(id)
        assert entity.foo == 142

        try:
            update(id, 100, fail=True)
        except SpuriousError:
            pass

        entity = SomeKind.get_by_id(id)
        assert entity.foo == 142
