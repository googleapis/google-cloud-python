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


def test_int_init():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)
        baz = proto.Field(proto.INT32, number=2)

    foo = Foo(bar=42)
    assert foo.bar == 42
    assert foo.baz == 0
    assert not foo.baz
    assert Foo.pb(foo).bar == 42
    assert Foo.pb(foo).baz == 0


def test_int_rmw():
    class Foo(proto.Message):
        spam = proto.Field(proto.INT32, number=1)
        eggs = proto.Field(proto.INT32, number=2)

    foo = Foo(spam=42)
    foo.eggs = 76  # trombones led the big parade...
    assert foo.spam == 42
    assert foo.eggs == 76
    assert Foo.pb(foo).spam == 42
    assert Foo.pb(foo).eggs == 76
    foo.spam = 144
    assert foo.spam == 144
    assert foo.eggs == 76
    assert Foo.pb(foo).spam == 144
    assert Foo.pb(foo).eggs == 76


def test_int_del():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    foo = Foo(bar=42)
    assert foo.bar == 42
    del foo.bar
    assert foo.bar == 0
    assert not foo.bar


def test_int_size():
    class Foo(proto.Message):
        small = proto.Field(proto.INT32, number=1)
        big = proto.Field(proto.INT64, number=2)

    foo = Foo()
    foo.big = 2 ** 40
    assert foo.big == 2 ** 40
    with pytest.raises(ValueError):
        foo.small = 2 ** 40
    with pytest.raises(ValueError):
        Foo(small=2 ** 40)


def test_int_unsigned():
    class Foo(proto.Message):
        signed = proto.Field(proto.INT32, number=1)
        unsigned = proto.Field(proto.UINT32, number=2)

    foo = Foo()
    foo.signed = -10
    assert foo.signed == -10
    with pytest.raises(ValueError):
        foo.unsigned = -10
    with pytest.raises(ValueError):
        Foo(unsigned=-10)


def test_field_descriptor_idempotent():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    bar_field = Foo.meta.fields["bar"]
    assert bar_field.descriptor is bar_field.descriptor
