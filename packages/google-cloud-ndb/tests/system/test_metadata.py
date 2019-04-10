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
System tests for metadata.
"""
import time

import pytest

from google.cloud import ndb


@pytest.mark.usefixtures("client_context")
def test_kind_metadata(dispose_of):
    from google.cloud.ndb.metadata import Kind

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()

    class MyKind(ndb.Model):
        bar = ndb.StringProperty()

    entity1 = AnyKind(foo=1, namespace="_test_namespace_")
    entity1.put()
    dispose_of(entity1.key._key)

    entity2 = MyKind(bar="x", namespace="_test_namespace_")
    entity2.put()
    dispose_of(entity2.key._key)

    query = ndb.Query(kind=Kind.KIND_NAME, namespace="_test_namespace_")
    results = query.fetch()
    assert len(results) >= 2

    kinds = [result.kind_name for result in results]
    assert all(kind in kinds for kind in ["AnyKind", "MyKind"]) != []


@pytest.mark.usefixtures("client_context")
def test_get_kinds(dispose_of):
    from google.cloud.ndb.metadata import get_kinds

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()

    class MyKind(ndb.Model):
        bar = ndb.StringProperty()

    class OtherKind(ndb.Model):
        baz = ndb.IntegerProperty()

    class SomeKind(ndb.Model):
        qux = ndb.StringProperty()

    entity1 = AnyKind(foo=1)
    entity1.put()
    dispose_of(entity1.key._key)

    entity2 = MyKind(bar="a")
    entity2.put()
    dispose_of(entity2.key._key)

    entity3 = OtherKind(baz=2)
    entity3.put()
    dispose_of(entity3.key._key)

    entity4 = SomeKind(qux="a")
    entity4.put()
    dispose_of(entity4.key._key)

    kinds = get_kinds()
    assert (
        all(
            kind in kinds
            for kind in ["AnyKind", "MyKind", "OtherKind", "SomeKind"]
        )
        != []
    )

    kinds = get_kinds(start="N")
    assert all(kind in kinds for kind in ["OtherKind", "SomeKind"]) != []
    assert not any(kind in kinds for kind in ["AnyKind", "MyKind"])

    kinds = get_kinds(end="N")
    assert all(kind in kinds for kind in ["AnyKind", "MyKind"]) != []
    assert not any(kind in kinds for kind in ["OtherKind", "SomeKind"])

    kinds = get_kinds(start="L", end="P")
    assert all(kind in kinds for kind in ["MyKind", "OtherKind"]) != []
    assert not any(kind in kinds for kind in ["AnyKind", "SomeKind"])


@pytest.mark.usefixtures("client_context")
def test_namespace_metadata(dispose_of):
    from google.cloud.ndb.metadata import Namespace

    # Why is this not necessary for Kind?
    Namespace._fix_up_properties()

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()

    entity1 = AnyKind(foo=1, namespace="_test_namespace_")
    entity1.put()
    dispose_of(entity1.key._key)

    entity2 = AnyKind(foo=2, namespace="_test_namespace_2_")
    entity2.put()
    dispose_of(entity2.key._key)

    query = ndb.Query(kind=Namespace.KIND_NAME)
    results = query.fetch()
    assert len(results) >= 2

    names = [result.namespace_name for result in results]
    assert (
        all(
            name in names
            for name in ["_test_namespace_", "_test_namespace_2_"]
        )
        != []
    )


@pytest.mark.usefixtures("client_context")
def test_get_namespaces(dispose_of):
    from google.cloud.ndb.metadata import get_namespaces

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()

    entity1 = AnyKind(foo=1, namespace="CoolNamespace")
    entity1.put()
    dispose_of(entity1.key._key)

    entity2 = AnyKind(foo=2, namespace="MyNamespace")
    entity2.put()
    dispose_of(entity2.key._key)

    entity3 = AnyKind(foo=3, namespace="OtherNamespace")
    entity3.put()
    dispose_of(entity3.key._key)

    names = get_namespaces()
    assert (
        all(
            name in names
            for name in ["CoolNamespace", "MyNamespace", "OtherNamespace"]
        )
        != []
    )

    names = get_namespaces(start="L")
    assert (
        all(name in names for name in ["MyNamespace", "OtherNamspace"]) != []
    )

    names = get_namespaces(end="N")
    assert (
        all(name in names for name in ["CoolNamespace", "MyNamespace"]) != []
    )

    names = get_namespaces(start="D", end="N")
    assert all(name in names for name in ["MyNamespace"]) != []


@pytest.mark.usefixtures("client_context")
def test_property_metadata(dispose_of):
    from google.cloud.ndb.metadata import Property

    # Why is this not necessary for Kind?
    Property._fix_up_properties()

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()

    entity1 = AnyKind(foo=1, bar="x")
    entity1.put()
    dispose_of(entity1.key._key)

    query = ndb.Query(kind=Property.KIND_NAME)
    results = query.fetch()
    assert len(results) >= 2

    properties = [
        result.property_name
        for result in results
        if result.kind_name == "AnyKind"
    ]
    assert properties == ["bar", "foo"]


@pytest.mark.usefixtures("client_context")
def test_get_properties_of_kind(dispose_of):
    from google.cloud.ndb.metadata import get_properties_of_kind

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.IntegerProperty()
        qux = ndb.StringProperty()

    entity1 = AnyKind(foo=1, bar="x", baz=3, qux="y")
    entity1.put()
    dispose_of(entity1.key._key)

    properties = _wait_for_metadata_update(get_properties_of_kind, "AnyKind")
    assert properties == ["bar", "baz", "foo", "qux"]

    properties = get_properties_of_kind("AnyKind", start="c")
    assert properties == ["foo", "qux"]

    properties = get_properties_of_kind("AnyKind", end="e")
    assert properties == ["bar", "baz"]

    properties = get_properties_of_kind("AnyKind", start="c", end="p")
    assert properties == ["foo"]


@pytest.mark.usefixtures("client_context")
@pytest.mark.parametrize("namespace", ["DiffNamespace"])
def test_get_properties_of_kind_different_namespace(dispose_of, namespace):
    from google.cloud.ndb.metadata import get_properties_of_kind

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.IntegerProperty()
        qux = ndb.StringProperty()

    entity1 = AnyKind(
        foo=1, bar="x", baz=3, qux="y", namespace="DiffNamespace"
    )
    entity1.put()
    dispose_of(entity1.key._key)

    properties = _wait_for_metadata_update(get_properties_of_kind, "AnyKind")
    assert properties == ["bar", "baz", "foo", "qux"]

    properties = get_properties_of_kind("AnyKind", start="c")
    assert properties == ["foo", "qux"]

    properties = get_properties_of_kind("AnyKind", end="e")
    assert properties == ["bar", "baz"]

    properties = get_properties_of_kind("AnyKind", start="c", end="p")
    assert properties == ["foo"]


@pytest.mark.usefixtures("client_context")
def test_get_representations_of_kind(dispose_of):
    from google.cloud.ndb.metadata import get_representations_of_kind

    class AnyKind(ndb.Model):
        foo = ndb.IntegerProperty()
        bar = ndb.StringProperty()
        baz = ndb.IntegerProperty()
        qux = ndb.StringProperty()

    entity1 = AnyKind(foo=1, bar="x", baz=3, qux="y")
    entity1.put()
    dispose_of(entity1.key._key)

    representations = _wait_for_metadata_update(
        get_representations_of_kind, "AnyKind"
    )
    assert representations == {
        "bar": ["STRING"],
        "baz": ["INT64"],
        "foo": ["INT64"],
        "qux": ["STRING"],
    }

    representations = get_representations_of_kind("AnyKind", start="c")
    assert representations == {"foo": ["INT64"], "qux": ["STRING"]}

    representations = get_representations_of_kind("AnyKind", end="e")
    assert representations == {"bar": ["STRING"], "baz": ["INT64"]}

    representations = get_representations_of_kind(
        "AnyKind", start="c", end="p"
    )
    assert representations == {"foo": ["INT64"]}


def _wait_for_metadata_update(func, arg):
    # Datastore apparently takes some time to update the metadata
    # before queries can be made. We'll give it a few seconds to see
    # if the query works.

    deadline = time.time() + 30
    while True:
        result = func(arg)
        if result:
            break

        assert time.time() < deadline, "Metadata was not updated in time."

        time.sleep(1)
    return result
