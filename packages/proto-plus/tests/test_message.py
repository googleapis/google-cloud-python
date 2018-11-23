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

import proto


def test_message_constructor_instance():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    foo_original = Foo(bar=42)
    foo_copy = Foo(foo_original)
    assert foo_original.bar == foo_copy.bar == 42
    assert foo_original == foo_copy
    assert foo_original is not foo_copy
    assert isinstance(foo_original, Foo)
    assert isinstance(foo_copy, Foo)
    assert isinstance(Foo.pb(foo_copy), Foo.pb())


def test_message_constructor_underlying_pb2():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    foo_pb2 = Foo.pb()(bar=42)
    foo = Foo(foo_pb2)
    assert foo.bar == Foo.pb(foo).bar == foo_pb2.bar == 42
    assert foo == foo_pb2  # Not communitive. Nothing we can do about that.
    assert foo_pb2 == Foo.pb(foo)
    assert foo_pb2 is not Foo.pb(foo)
    assert isinstance(foo, Foo)
    assert isinstance(Foo.pb(foo), Foo.pb())
    assert isinstance(foo_pb2, Foo.pb())


def test_message_constructor_underlying_pb2_and_kwargs():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    foo_pb2 = Foo.pb()(bar=42)
    foo = Foo(foo_pb2, bar=99)
    assert foo.bar == Foo.pb(foo).bar == 99
    assert foo_pb2.bar == 42
    assert isinstance(foo, Foo)
    assert isinstance(Foo.pb(foo), Foo.pb())
    assert isinstance(foo_pb2, Foo.pb())


def test_message_constructor_dict():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    foo = Foo({'bar': 42})
    assert foo.bar == Foo.pb(foo).bar == 42
    assert foo != {'bar': 42}
    assert isinstance(foo, Foo)
    assert isinstance(Foo.pb(foo), Foo.pb())


def test_message_constructor_kwargs():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    foo = Foo(bar=42)
    assert foo.bar == Foo.pb(foo).bar == 42
    assert isinstance(foo, Foo)
    assert isinstance(Foo.pb(foo), Foo.pb())


def test_message_constructor_invalid():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    with pytest.raises(TypeError):
        Foo(object())


def test_message_constructor_explicit_qualname():
    class Foo(proto.Message):
        __qualname__ = 'Foo'
        bar = proto.Field(proto.INT64, number=1)
    foo_original = Foo(bar=42)
    foo_copy = Foo(foo_original)
    assert foo_original.bar == foo_copy.bar == 42
    assert foo_original == foo_copy
    assert foo_original is not foo_copy
    assert isinstance(foo_original, Foo)
    assert isinstance(foo_copy, Foo)
    assert isinstance(Foo.pb(foo_copy), Foo.pb())


def test_message_contains_primitive():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)
    assert 'bar' in Foo(bar=42)
    assert 'bar' not in Foo(bar=0)
    assert 'bar' not in Foo()


def test_message_contains_composite():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)

    class Baz(proto.Message):
        foo = proto.Field(proto.MESSAGE, number=1, message=Foo)

    assert 'foo' in Baz(foo=Foo(bar=42))
    assert 'foo' in Baz(foo=Foo())
    assert 'foo' not in Baz()


def test_message_contains_repeated_primitive():
    class Foo(proto.Message):
        bar = proto.RepeatedField(proto.INT64, number=1)

    assert 'bar' in Foo(bar=[1, 1, 2, 3, 5])
    assert 'bar' in Foo(bar=[0])
    assert 'bar' not in Foo(bar=[])
    assert 'bar' not in Foo()


def test_message_contains_repeated_composite():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)

    class Baz(proto.Message):
        foo = proto.RepeatedField(proto.MESSAGE, number=1, message=Foo)

    assert 'foo' in Baz(foo=[Foo(bar=42)])
    assert 'foo' in Baz(foo=[Foo()])
    assert 'foo' not in Baz(foo=[])
    assert 'foo' not in Baz()


def test_message_eq_primitives():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)
        baz = proto.Field(proto.STRING, number=2)
        bacon = proto.Field(proto.BOOL, number=3)

    assert Foo() == Foo()
    assert Foo(bar=42, baz='42') == Foo(bar=42, baz='42')
    assert Foo(bar=42, baz='42') != Foo(baz='42')
    assert Foo(bar=42, bacon=True) == Foo(bar=42, bacon=True)
    assert Foo(bar=42, bacon=True) != Foo(bar=42)
    assert Foo(bar=42, baz='42', bacon=True) != Foo(bar=42, bacon=True)
    assert Foo(bacon=False) == Foo()
    assert Foo(bacon=True) != Foo(bacon=False)
    assert Foo(bar=21 * 2) == Foo(bar=42)
    assert Foo() == Foo(bar=0)
    assert Foo() == Foo(bar=0, baz='', bacon=False)
    assert Foo() != Foo(bar=0, baz='0', bacon=False)


def test_message_serialize():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)
        baz = proto.Field(proto.STRING, number=2)
        bacon = proto.Field(proto.BOOL, number=3)

    foo = Foo(bar=42, bacon=True)
    assert Foo.serialize(foo) == Foo.pb(foo).SerializeToString()


def test_message_deserialize():
    class OldFoo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class NewFoo(proto.Message):
        bar = proto.Field(proto.INT64, number=1)

    serialized = OldFoo.serialize(OldFoo(bar=42))
    new_foo = NewFoo.deserialize(serialized)
    assert isinstance(new_foo, NewFoo)
    assert new_foo.bar == 42


def test_message_pb():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    assert isinstance(Foo.pb(Foo()), Foo.pb())
    with pytest.raises(TypeError):
        Foo.pb(object())
