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
System tests for queries.
"""

import datetime
import functools
import operator

import grpc
import pytest
import pytz

import test_utils.system

from google.cloud import ndb

from tests.system import KIND, eventually


def _length_equals(n):
    def predicate(sequence):
        return len(sequence) == n

    return predicate


def _equals(n):
    return functools.partial(operator.eq, n)


@pytest.mark.usefixtures("client_context")
def test_fetch_all_of_a_kind(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    results = eventually(query.fetch, _length_equals(5))

    results = sorted(results, key=operator.attrgetter("foo"))
    assert [entity.foo for entity in results] == [0, 1, 2, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_fetch_w_absurdly_short_timeout(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    timeout = 1e-9  # One nanosecend
    with pytest.raises(Exception) as error_context:
        query.fetch(timeout=timeout)

    assert error_context.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED


@pytest.mark.usefixtures("client_context")
def test_fetch_lots_of_a_kind(dispose_of):
    n_entities = 500

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.toplevel
    def make_entities():
        entities = [SomeKind(foo=i) for i in range(n_entities)]
        keys = yield [entity.put_async() for entity in entities]
        raise ndb.Return(keys)

    for key in make_entities():
        dispose_of(key._key)

    query = SomeKind.query()
    results = eventually(query.fetch, _length_equals(n_entities))

    results = sorted(results, key=operator.attrgetter("foo"))
    assert [entity.foo for entity in results][:5] == [0, 1, 2, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_high_limit(dispose_of):
    """Regression test for Issue #236

    https://github.com/googleapis/python-ndb/issues/236
    """
    n_entities = 500

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.toplevel
    def make_entities():
        entities = [SomeKind(foo=i) for i in range(n_entities)]
        keys = yield [entity.put_async() for entity in entities]
        raise ndb.Return(keys)

    for key in make_entities():
        dispose_of(key._key)

    query = SomeKind.query()
    eventually(query.fetch, _length_equals(n_entities))
    results = query.fetch(limit=400)

    assert len(results) == 400


@pytest.mark.usefixtures("client_context")
def test_fetch_and_immediately_cancel(dispose_of):
    # Make a lot of entities so the query call won't complete before we get to
    # call cancel.
    n_entities = 500

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.toplevel
    def make_entities():
        entities = [SomeKind(foo=i) for i in range(n_entities)]
        keys = yield [entity.put_async() for entity in entities]
        raise ndb.Return(keys)

    for key in make_entities():
        dispose_of(key._key)

    query = SomeKind.query()
    future = query.fetch_async()
    future.cancel()
    with pytest.raises(ndb.exceptions.Cancelled):
        future.result()


@pytest.mark.usefixtures("client_context")
def test_ancestor_query(ds_entity):
    root_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, root_id, foo=-1)
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, root_id, KIND, entity_id, foo=i)

    another_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, another_id, foo=42)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query(ancestor=ndb.Key(KIND, root_id))
    results = eventually(query.fetch, _length_equals(6))

    results = sorted(results, key=operator.attrgetter("foo"))
    assert [entity.foo for entity in results] == [-1, 0, 1, 2, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_projection(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=12, bar="none")
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=21, bar="naan")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    query = SomeKind.query(projection=("foo",))
    results = eventually(query.fetch, _length_equals(2))

    results = sorted(results, key=operator.attrgetter("foo"))

    assert results[0].foo == 12
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[0].bar

    assert results[1].foo == 21
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[1].bar


@pytest.mark.usefixtures("client_context")
def test_projection_datetime(ds_entity):
    """Regression test for Issue #261

    https://github.com/googleapis/python-ndb/issues/261
    """
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        foo=datetime.datetime(2010, 5, 12, 2, 42, tzinfo=pytz.UTC),
    )
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        foo=datetime.datetime(2010, 5, 12, 2, 43, tzinfo=pytz.UTC),
    )

    class SomeKind(ndb.Model):
        foo = ndb.DateTimeProperty()
        bar = ndb.StringProperty()

    query = SomeKind.query(projection=("foo",))
    results = eventually(query.fetch, _length_equals(2))

    results = sorted(results, key=operator.attrgetter("foo"))

    assert results[0].foo == datetime.datetime(2010, 5, 12, 2, 42)
    assert results[1].foo == datetime.datetime(2010, 5, 12, 2, 43)


@pytest.mark.usefixtures("client_context")
def test_projection_with_fetch_and_property(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=12, bar="none")
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=21, bar="naan")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    query = SomeKind.query()
    eventually(query.fetch, _length_equals(2))

    results = query.fetch(projection=(SomeKind.foo,))
    results = sorted(results, key=operator.attrgetter("foo"))

    assert results[0].foo == 12
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[0].bar

    assert results[1].foo == 21
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[1].bar


@pytest.mark.usefixtures("client_context")
def test_distinct_on(ds_entity):
    for i in range(6):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i % 2, bar="none")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    query = SomeKind.query(distinct_on=("foo",))
    eventually(SomeKind.query().fetch, _length_equals(6))

    results = query.fetch()
    results = sorted(results, key=operator.attrgetter("foo"))

    assert results[0].foo == 0
    assert results[0].bar == "none"

    assert results[1].foo == 1
    assert results[1].bar == "none"


@pytest.mark.usefixtures("client_context")
def test_namespace(dispose_of, other_namespace):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    entity1 = SomeKind(foo=1, bar="a", namespace=other_namespace)
    entity1.put()
    dispose_of(entity1.key._key)

    entity2 = SomeKind(foo=2, bar="b")
    entity2.put()
    dispose_of(entity2.key._key)

    eventually(SomeKind.query().fetch, _length_equals(1))

    query = SomeKind.query(namespace=other_namespace)
    results = eventually(query.fetch, _length_equals(1))

    assert results[0].foo == 1
    assert results[0].bar == "a"
    assert results[0].key.namespace() == other_namespace


def test_namespace_set_on_client_with_id(dispose_of, other_namespace):
    """Regression test for #337

    https://github.com/googleapis/python-ndb/issues/337
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    client = ndb.Client(namespace=other_namespace)
    with client.context(cache_policy=False):
        id = test_utils.system.unique_resource_id()
        entity1 = SomeKind(id=id, foo=1, bar="a")
        key = entity1.put()
        dispose_of(key._key)
        assert key.namespace() == other_namespace

        results = eventually(SomeKind.query().fetch, _length_equals(1))

        assert results[0].foo == 1
        assert results[0].bar == "a"
        assert results[0].key.namespace() == other_namespace


@pytest.mark.usefixtures("client_context")
def test_filter_equal(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    eventually(SomeKind.query().fetch, _length_equals(5))

    query = SomeKind.query(SomeKind.foo == 2)
    results = query.fetch()
    assert results[0].foo == 2


@pytest.mark.usefixtures("client_context")
def test_filter_not_equal(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    eventually(SomeKind.query().fetch, _length_equals(5))

    query = SomeKind.query(SomeKind.foo != 2)
    results = query.fetch()
    results = sorted(results, key=operator.attrgetter("foo"))
    assert [entity.foo for entity in results] == [0, 1, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_filter_or(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    @ndb.toplevel
    def make_entities():
        keys = yield (
            SomeKind(foo=1, bar="a").put_async(),
            SomeKind(foo=2, bar="b").put_async(),
            SomeKind(foo=1, bar="c").put_async(),
        )
        for key in keys:
            dispose_of(key._key)

    make_entities()
    eventually(SomeKind.query().fetch, _length_equals(3))

    query = SomeKind.query(ndb.OR(SomeKind.foo == 1, SomeKind.bar == "c"))
    results = query.fetch()
    results = sorted(results, key=operator.attrgetter("bar"))
    assert [entity.bar for entity in results] == ["a", "c"]


@pytest.mark.usefixtures("client_context")
def test_order_by_ascending(ds_entity):
    for i in reversed(range(5)):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query().order(SomeKind.foo)
    results = eventually(query.fetch, _length_equals(5))

    assert [entity.foo for entity in results] == [0, 1, 2, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_order_by_descending(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    # query = SomeKind.query()  # Not implemented yet
    query = SomeKind.query().order(-SomeKind.foo)
    results = eventually(query.fetch, _length_equals(5))
    assert len(results) == 5

    assert [entity.foo for entity in results] == [4, 3, 2, 1, 0]


@pytest.mark.usefixtures("client_context")
def test_order_by_with_or_filter(dispose_of):
    """
    Checking to make sure ordering is preserved when merging different
    results sets.
    """

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    @ndb.toplevel
    def make_entities():
        keys = yield (
            SomeKind(foo=0, bar="a").put_async(),
            SomeKind(foo=1, bar="b").put_async(),
            SomeKind(foo=2, bar="a").put_async(),
            SomeKind(foo=3, bar="b").put_async(),
        )
        for key in keys:
            dispose_of(key._key)

    make_entities()
    query = SomeKind.query(ndb.OR(SomeKind.bar == "a", SomeKind.bar == "b"))
    query = query.order(SomeKind.foo)
    results = eventually(query.fetch, _length_equals(4))

    assert [entity.foo for entity in results] == [0, 1, 2, 3]


@pytest.mark.usefixtures("client_context")
def test_keys_only(ds_entity):
    # Assuming unique resource ids are assigned in order ascending with time.
    # Seems to be true so far.
    entity_id1 = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id1, foo=12, bar="none")
    entity_id2 = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id2, foo=21, bar="naan")

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    query = SomeKind.query().order(SomeKind.key)
    results = eventually(
        lambda: query.fetch(keys_only=True), _length_equals(2)
    )

    assert results[0] == ndb.Key("SomeKind", entity_id1)
    assert results[1] == ndb.Key("SomeKind", entity_id2)


@pytest.mark.usefixtures("client_context")
def test_offset_and_limit(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    eventually(SomeKind.query().fetch, _length_equals(5))

    query = SomeKind.query(order_by=["foo"])
    results = query.fetch(offset=2, limit=2)
    assert [entity.foo for entity in results] == [2, 3]


@pytest.mark.usefixtures("client_context")
def test_offset_and_limit_with_or_filter(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    @ndb.toplevel
    def make_entities():
        keys = yield (
            SomeKind(foo=0, bar="a").put_async(),
            SomeKind(foo=1, bar="b").put_async(),
            SomeKind(foo=2, bar="a").put_async(),
            SomeKind(foo=3, bar="b").put_async(),
            SomeKind(foo=4, bar="a").put_async(),
            SomeKind(foo=5, bar="b").put_async(),
        )
        for key in keys:
            dispose_of(key._key)

    make_entities()
    eventually(SomeKind.query().fetch, _length_equals(6))

    query = SomeKind.query(ndb.OR(SomeKind.bar == "a", SomeKind.bar == "b"))
    query = query.order(SomeKind.foo)
    results = query.fetch(offset=1, limit=2)

    assert [entity.foo for entity in results] == [1, 2]


@pytest.mark.usefixtures("client_context")
def test_iter_all_of_a_kind(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query().order("foo")
    results = eventually(lambda: list(query), _length_equals(5))
    assert [entity.foo for entity in results] == [0, 1, 2, 3, 4]


@pytest.mark.usefixtures("client_context")
def test_get_first(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query().order(SomeKind.foo)
    eventually(query.fetch, _length_equals(5))
    assert query.get().foo == 0


@pytest.mark.usefixtures("client_context")
def test_get_only(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query().order(SomeKind.foo)
    eventually(query.fetch, _length_equals(5))
    assert query.filter(SomeKind.foo == 2).get().foo == 2


@pytest.mark.usefixtures("client_context")
def test_get_none(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query().order(SomeKind.foo)
    eventually(query.fetch, _length_equals(5))
    assert query.filter(SomeKind.foo == -1).get() is None


@pytest.mark.usefixtures("client_context")
def test_count_all(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    eventually(query.count, _equals(5))


@pytest.mark.usefixtures("client_context")
def test_count_with_limit(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    eventually(query.count, _equals(5))

    assert query.count(3) == 3


@pytest.mark.usefixtures("client_context")
def test_count_with_filter(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    eventually(query.count, _equals(5))

    assert query.filter(SomeKind.foo == 2).count() == 1


@pytest.mark.usefixtures("client_context")
def test_count_with_multi_query(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    query = SomeKind.query()
    eventually(query.count, _equals(5))

    assert query.filter(SomeKind.foo != 2).count() == 4


@pytest.mark.usefixtures("client_context")
def test_fetch_page(dispose_of):
    page_size = 5
    n_entities = page_size * 2

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    @ndb.toplevel
    def make_entities():
        entities = [SomeKind(foo=i) for i in range(n_entities)]
        keys = yield [entity.put_async() for entity in entities]
        raise ndb.Return(keys)

    for key in make_entities():
        dispose_of(key._key)

    query = SomeKind.query().order(SomeKind.foo)
    eventually(query.fetch, _length_equals(n_entities))

    results, cursor, more = query.fetch_page(page_size)
    assert [entity.foo for entity in results] == [0, 1, 2, 3, 4]
    assert more

    safe_cursor = cursor.urlsafe()
    next_cursor = ndb.Cursor(urlsafe=safe_cursor)
    results, cursor, more = query.fetch_page(
        page_size, start_cursor=next_cursor
    )
    assert [entity.foo for entity in results] == [5, 6, 7, 8, 9]

    results, cursor, more = query.fetch_page(page_size, start_cursor=cursor)
    assert not results
    assert not more


@pytest.mark.usefixtures("client_context")
def test_polymodel_query(ds_entity):
    class Animal(ndb.PolyModel):
        foo = ndb.IntegerProperty()

    class Cat(Animal):
        pass

    animal = Animal(foo=1)
    animal.put()
    cat = Cat(foo=2)
    cat.put()

    query = Animal.query()
    results = eventually(query.fetch, _length_equals(2))

    results = sorted(results, key=operator.attrgetter("foo"))
    assert isinstance(results[0], Animal)
    assert not isinstance(results[0], Cat)
    assert isinstance(results[1], Animal)
    assert isinstance(results[1], Cat)

    query = Cat.query()
    results = eventually(query.fetch, _length_equals(1))

    assert isinstance(results[0], Animal)
    assert isinstance(results[0], Cat)


@pytest.mark.usefixtures("client_context")
def test_polymodel_query_class_projection(ds_entity):
    """Regression test for Issue #248

    https://github.com/googleapis/python-ndb/issues/248
    """

    class Animal(ndb.PolyModel):
        foo = ndb.IntegerProperty()

    class Cat(Animal):
        pass

    animal = Animal(foo=1)
    animal.put()
    cat = Cat(foo=2)
    cat.put()

    query = Animal.query(projection=["class", "foo"])
    results = eventually(query.fetch, _length_equals(3))

    # Mostly reproduces odd behavior of legacy code
    results = sorted(results, key=operator.attrgetter("foo"))

    assert isinstance(results[0], Animal)
    assert not isinstance(results[0], Cat)
    assert results[0].foo == 1
    assert results[0].class_ == ["Animal"]

    assert isinstance(results[1], Animal)
    assert not isinstance(results[1], Cat)
    assert results[1].foo == 2
    assert results[1].class_ == ["Animal"]

    assert isinstance(results[2], Animal)
    assert isinstance(results[2], Cat)  # This would be False in legacy
    assert results[2].foo == 2
    assert results[2].class_ == ["Cat"]


@pytest.mark.usefixtures("client_context")
def test_query_repeated_property(ds_entity):
    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=1, bar=["a", "b", "c"])

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=2, bar=["c", "d", "e"])

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(KIND, entity_id, foo=3, bar=["e", "f", "g"])

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty(repeated=True)

    eventually(SomeKind.query().fetch, _length_equals(3))

    query = SomeKind.query().filter(SomeKind.bar == "c").order(SomeKind.foo)
    results = query.fetch()

    assert len(results) == 2
    assert results[0].foo == 1
    assert results[1].foo == 2


@pytest.mark.usefixtures("client_context")
def test_query_structured_property(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1, bar=OtherKind(one="pish", two="posh", three="pash")
        )
        entity2 = SomeKind(
            foo=2, bar=OtherKind(one="pish", two="posh", three="push")
        )
        entity3 = SomeKind(
            foo=3,
            bar=OtherKind(one="pish", two="moppish", three="pass the peas"),
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))

    query = (
        SomeKind.query()
        .filter(SomeKind.bar.one == "pish", SomeKind.bar.two == "posh")
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 1
    assert results[1].foo == 2


def test_query_structured_property_legacy_data(client_context, dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1, bar=OtherKind(one="pish", two="posh", three="pash")
        )
        entity2 = SomeKind(
            foo=2, bar=OtherKind(one="pish", two="posh", three="push")
        )
        entity3 = SomeKind(
            foo=3,
            bar=OtherKind(one="pish", two="moppish", three="pass the peas"),
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    with client_context.new(legacy_data=True).use():
        keys = make_entities()
        for key in keys:
            dispose_of(key._key)

        eventually(SomeKind.query().fetch, _length_equals(3))
        query = (
            SomeKind.query()
            .filter(SomeKind.bar.one == "pish", SomeKind.bar.two == "posh")
            .order(SomeKind.foo)
        )

        results = query.fetch()
        assert len(results) == 2
        assert results[0].foo == 1
        assert results[1].foo == 2


@pytest.mark.usefixtures("client_context")
def test_query_legacy_structured_property(ds_entity):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{"foo": 1, "bar.one": "pish", "bar.two": "posh", "bar.three": "pash"}
    )

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{"foo": 2, "bar.one": "pish", "bar.two": "posh", "bar.three": "push"}
    )

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{
            "foo": 3,
            "bar.one": "pish",
            "bar.two": "moppish",
            "bar.three": "pass the peas",
        }
    )

    eventually(SomeKind.query().fetch, _length_equals(3))

    query = (
        SomeKind.query()
        .filter(SomeKind.bar.one == "pish", SomeKind.bar.two == "posh")
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 1
    assert results[1].foo == 2


@pytest.mark.usefixtures("client_context")
def test_query_structured_property_with_projection(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1, bar=OtherKind(one="pish", two="posh", three="pash")
        )
        entity2 = SomeKind(
            foo=2, bar=OtherKind(one="bish", two="bosh", three="bush")
        )
        entity3 = SomeKind(
            foo=3,
            bar=OtherKind(one="pish", two="moppish", three="pass the peas"),
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))
    query = (
        SomeKind.query(projection=("foo", "bar.one", "bar.two"))
        .filter(SomeKind.foo < 3)
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 1
    assert results[0].bar.one == "pish"
    assert results[0].bar.two == "posh"
    assert results[1].foo == 2
    assert results[1].bar.one == "bish"
    assert results[1].bar.two == "bosh"

    with pytest.raises(ndb.UnprojectedPropertyError):
        results[0].bar.three

    with pytest.raises(ndb.UnprojectedPropertyError):
        results[1].bar.three


@pytest.mark.usefixtures("client_context")
def test_query_repeated_structured_property_with_properties(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="pish", two="posh", three="pash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="pish", two="bosh", three="bass"),
                OtherKind(one="bish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="fish", two="fosh", three="fash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))
    query = (
        SomeKind.query()
        .filter(SomeKind.bar.one == "pish", SomeKind.bar.two == "posh")
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 1
    assert results[1].foo == 2


def test_query_repeated_structured_property_with_properties_legacy_data(
    client_context, dispose_of
):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="pish", two="posh", three="pash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="pish", two="bosh", three="bass"),
                OtherKind(one="bish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="fish", two="fosh", three="fash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    with client_context.new(legacy_data=True).use():
        keys = make_entities()
        for key in keys:
            dispose_of(key._key)

        eventually(SomeKind.query().fetch, _length_equals(3))
        query = (
            SomeKind.query()
            .filter(SomeKind.bar.one == "pish", SomeKind.bar.two == "posh")
            .order(SomeKind.foo)
        )

        results = query.fetch()
        assert len(results) == 2
        assert results[0].foo == 1
        assert results[1].foo == 2


@pytest.mark.usefixtures("client_context")
def test_query_repeated_structured_property_with_entity_twice(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="pish", two="posh", three="pash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="bish", two="bosh", three="bass"),
                OtherKind(one="pish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="pish", two="fosh", three="fash"),
                OtherKind(one="bish", two="posh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))
    query = (
        SomeKind.query()
        .filter(
            SomeKind.bar == OtherKind(one="pish", two="posh"),
            SomeKind.bar == OtherKind(two="posh", three="pash"),
        )
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 1
    assert results[0].foo == 1


def test_query_repeated_structured_property_with_entity_twice_legacy_data(
    client_context, dispose_of
):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="pish", two="posh", three="pash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="bish", two="bosh", three="bass"),
                OtherKind(one="pish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="pish", two="fosh", three="fash"),
                OtherKind(one="bish", two="posh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    with client_context.new(legacy_data=True).use():
        keys = make_entities()
        for key in keys:
            dispose_of(key._key)

        eventually(SomeKind.query().fetch, _length_equals(3))
        query = (
            SomeKind.query()
            .filter(
                SomeKind.bar == OtherKind(one="pish", two="posh"),
                SomeKind.bar == OtherKind(two="posh", three="pash"),
            )
            .order(SomeKind.foo)
        )

        results = query.fetch()
        assert len(results) == 1
        assert results[0].foo == 1


@pytest.mark.usefixtures("client_context")
def test_query_repeated_structured_property_with_projection(dispose_of):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="angle", two="cankle", three="pash"),
                OtherKind(one="bangle", two="dangle", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="bish", two="bosh", three="bass"),
                OtherKind(one="pish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="pish", two="fosh", three="fash"),
                OtherKind(one="bish", two="posh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))
    query = SomeKind.query(projection=("bar.one", "bar.two")).filter(
        SomeKind.foo < 2
    )

    # This counter-intuitive result is consistent with Legacy NDB behavior and
    # is a result of the odd way Datastore handles projection queries with
    # array valued properties:
    #
    # https://cloud.google.com/datastore/docs/concepts/queries#projections_and_array-valued_properties
    #
    results = query.fetch()
    assert len(results) == 4

    def sort_key(result):
        return (result.bar[0].one, result.bar[0].two)

    results = sorted(results, key=sort_key)

    assert results[0].bar[0].one == "angle"
    assert results[0].bar[0].two == "cankle"
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[0].bar[0].three

    assert results[1].bar[0].one == "angle"
    assert results[1].bar[0].two == "dangle"
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[1].bar[0].three

    assert results[2].bar[0].one == "bangle"
    assert results[2].bar[0].two == "cankle"
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[2].bar[0].three

    assert results[3].bar[0].one == "bangle"
    assert results[3].bar[0].two == "dangle"
    with pytest.raises(ndb.UnprojectedPropertyError):
        results[3].bar[0].three


def test_query_repeated_structured_property_with_projection_legacy_data(
    client_context, dispose_of
):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="angle", two="cankle", three="pash"),
                OtherKind(one="bangle", two="dangle", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="bish", two="bosh", three="bass"),
                OtherKind(one="pish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="pish", two="fosh", three="fash"),
                OtherKind(one="bish", two="posh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    with client_context.new(legacy_data=True).use():
        keys = make_entities()
        for key in keys:
            dispose_of(key._key)

        eventually(SomeKind.query().fetch, _length_equals(3))
        query = SomeKind.query(projection=("bar.one", "bar.two")).filter(
            SomeKind.foo < 2
        )

        # This counter-intuitive result is consistent with Legacy NDB behavior
        # and is a result of the odd way Datastore handles projection queries
        # with array valued properties:
        #
        # https://cloud.google.com/datastore/docs/concepts/queries#projections_and_array-valued_properties
        #
        results = query.fetch()
        assert len(results) == 4

        def sort_key(result):
            return (result.bar[0].one, result.bar[0].two)

        results = sorted(results, key=sort_key)

        assert results[0].bar[0].one == "angle"
        assert results[0].bar[0].two == "cankle"
        with pytest.raises(ndb.UnprojectedPropertyError):
            results[0].bar[0].three

        assert results[1].bar[0].one == "angle"
        assert results[1].bar[0].two == "dangle"
        with pytest.raises(ndb.UnprojectedPropertyError):
            results[1].bar[0].three

        assert results[2].bar[0].one == "bangle"
        assert results[2].bar[0].two == "cankle"
        with pytest.raises(ndb.UnprojectedPropertyError):
            results[2].bar[0].three

        assert results[3].bar[0].one == "bangle"
        assert results[3].bar[0].two == "dangle"
        with pytest.raises(ndb.UnprojectedPropertyError):
            results[3].bar[0].three


@pytest.mark.usefixtures("client_context")
def test_query_legacy_repeated_structured_property(ds_entity):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{
            "foo": 1,
            "bar.one": [u"pish", u"bish"],
            "bar.two": [u"posh", u"bosh"],
            "bar.three": [u"pash", u"bash"],
        }
    )

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{
            "foo": 2,
            "bar.one": [u"bish", u"pish"],
            "bar.two": [u"bosh", u"posh"],
            "bar.three": [u"bass", u"pass"],
        }
    )

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{
            "foo": 3,
            "bar.one": [u"pish", u"bish"],
            "bar.two": [u"fosh", u"posh"],
            "bar.three": [u"fash", u"bash"],
        }
    )

    eventually(SomeKind.query().fetch, _length_equals(3))

    query = (
        SomeKind.query()
        .filter(
            SomeKind.bar == OtherKind(one=u"pish", two=u"posh"),
            SomeKind.bar == OtherKind(two=u"posh", three=u"pash"),
        )
        .order(SomeKind.foo)
    )

    results = query.fetch()
    assert len(results) == 1
    assert results[0].foo == 1


@pytest.mark.usefixtures("client_context")
def test_query_legacy_repeated_structured_property_with_name(ds_entity):
    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, "b", repeated=True)

    entity_id = test_utils.system.unique_resource_id()
    ds_entity(
        KIND,
        entity_id,
        **{
            "foo": 1,
            "b.one": [u"pish", u"bish"],
            "b.two": [u"posh", u"bosh"],
            "b.three": [u"pash", u"bash"],
        }
    )

    eventually(SomeKind.query().fetch, _length_equals(1))

    query = SomeKind.query()

    results = query.fetch()
    assert len(results) == 1
    assert results[0].bar[0].one == u"pish"


@pytest.mark.usefixtures("client_context")
def test_fetch_page_with_repeated_structured_property(dispose_of):
    """Regression test for Issue #254.

    https://github.com/googleapis/python-ndb/issues/254
    """

    class OtherKind(ndb.Model):
        one = ndb.StringProperty()
        two = ndb.StringProperty()
        three = ndb.StringProperty()

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StructuredProperty(OtherKind, repeated=True)

    @ndb.synctasklet
    def make_entities():
        entity1 = SomeKind(
            foo=1,
            bar=[
                OtherKind(one="pish", two="posh", three="pash"),
                OtherKind(one="bish", two="bosh", three="bash"),
            ],
        )
        entity2 = SomeKind(
            foo=2,
            bar=[
                OtherKind(one="bish", two="bosh", three="bass"),
                OtherKind(one="pish", two="posh", three="pass"),
            ],
        )
        entity3 = SomeKind(
            foo=3,
            bar=[
                OtherKind(one="pish", two="fosh", three="fash"),
                OtherKind(one="bish", two="posh", three="bash"),
            ],
        )

        keys = yield (
            entity1.put_async(),
            entity2.put_async(),
            entity3.put_async(),
        )
        raise ndb.Return(keys)

    keys = make_entities()
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(3))
    query = (
        SomeKind.query()
        .filter(
            SomeKind.bar == OtherKind(one="pish", two="posh"),
            SomeKind.bar == OtherKind(two="posh", three="pash"),
        )
        .order(SomeKind.foo)
    )

    with pytest.raises(TypeError):
        query.fetch_page(page_size=10)


@pytest.mark.usefixtures("client_context")
def test_map(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.StringProperty()
        ref = ndb.KeyProperty()

    class OtherKind(ndb.Model):
        foo = ndb.StringProperty()

    foos = ("aa", "bb", "cc", "dd", "ee")
    others = [OtherKind(foo=foo) for foo in foos]
    other_keys = ndb.put_multi(others)
    for key in other_keys:
        dispose_of(key._key)

    things = [SomeKind(foo=foo, ref=key) for foo, key in zip(foos, other_keys)]
    keys = ndb.put_multi(things)
    for key in keys:
        dispose_of(key._key)

    eventually(SomeKind.query().fetch, _length_equals(5))
    eventually(OtherKind.query().fetch, _length_equals(5))

    @ndb.tasklet
    def get_other_foo(thing):
        other = yield thing.ref.get_async()
        raise ndb.Return(other.foo)

    query = SomeKind.query().order(SomeKind.foo)
    assert query.map(get_other_foo) == foos


@pytest.mark.usefixtures("client_context")
def test_map_empty_result_set(dispose_of):
    class SomeKind(ndb.Model):
        foo = ndb.StringProperty()

    def somefunc(x):
        raise Exception("Shouldn't be called.")

    query = SomeKind.query()
    assert query.map(somefunc) == []


@pytest.mark.usefixtures("client_context")
def test_gql(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    eventually(SomeKind.query().fetch, _length_equals(5))

    query = ndb.gql("SELECT * FROM SomeKind WHERE foo = :1", 2)
    results = query.fetch()
    assert results[0].foo == 2

    query = SomeKind.gql("WHERE foo = :1", 2)
    results = query.fetch()
    assert results[0].foo == 2


@pytest.mark.usefixtures("client_context")
def test_IN(ds_entity):
    for i in range(5):
        entity_id = test_utils.system.unique_resource_id()
        ds_entity(KIND, entity_id, foo=i)

    class SomeKind(ndb.Model):
        foo = ndb.IntegerProperty()

    eventually(SomeKind.query().fetch, _length_equals(5))

    query = SomeKind.gql("where foo in (2, 3)").order(SomeKind.foo)
    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 2
    assert results[1].foo == 3

    query = SomeKind.gql("where foo in :1", [2, 3]).order(SomeKind.foo)
    results = query.fetch()
    assert len(results) == 2
    assert results[0].foo == 2
    assert results[1].foo == 3
