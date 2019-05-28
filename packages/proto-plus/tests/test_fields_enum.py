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

import proto


def test_outer_enum_init():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo(color=Color.RED)
    assert foo.color == Color.RED
    assert foo.color == 1
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 1


def test_outer_enum_init_int():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo(color=1)
    assert foo.color == Color.RED
    assert foo.color == 1
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 1


def test_outer_enum_init_str():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo(color='RED')
    assert foo.color == Color.RED
    assert foo.color == 1
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 1


def test_outer_enum_init_dict():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo({'color': 1})
    assert foo.color == Color.RED
    assert foo.color == 1
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 1


def test_outer_enum_init_dict_str():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo({'color': 'BLUE'})
    assert foo.color == Color.BLUE
    assert foo.color == 3
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 3


def test_outer_enum_init_pb2():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(proto.ENUM, number=1, enum=Color)

    foo = Foo(Foo.pb()(color=Color.RED))
    assert foo.color == Color.RED
    assert foo.color == 1
    assert foo.color
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 1


def test_outer_enum_unset():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(proto.ENUM, number=1, enum=Color)

    foo = Foo()
    assert foo.color == Color.COLOR_UNSPECIFIED
    assert foo.color == 0
    assert 'color' not in foo
    assert not foo.color
    assert Foo.pb(foo).color == 0
    assert Foo.serialize(foo) == b''


def test_outer_enum_write():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(proto.ENUM, number=1, enum=Color)

    foo = Foo()
    foo.color = Color.GREEN
    assert foo.color == Color.GREEN
    assert foo.color == 2
    assert Foo.pb(foo).color == 2
    assert foo.color


def test_outer_enum_write_int():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(proto.ENUM, number=1, enum=Color)

    foo = Foo()
    foo.color = 3
    assert foo.color == Color.BLUE
    assert foo.color == 3
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 3
    assert foo.color


def test_outer_enum_write_str():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo()
    foo.color = 'BLUE'
    assert foo.color == Color.BLUE
    assert foo.color == 3
    assert isinstance(foo.color, Color)
    assert Foo.pb(foo).color == 3
    assert foo.color


def test_inner_enum_init():
    class Foo(proto.Message):
        class Color(proto.Enum):
            COLOR_UNSPECIFIED = 0
            RED = 1
            GREEN = 2
            BLUE = 3

        color = proto.Field(proto.ENUM, number=1, enum=Color)

    foo = Foo(color=Foo.Color.RED)
    assert foo.color == Foo.Color.RED
    assert foo.color == 1
    assert foo.color
    assert Foo.pb(foo).color == 1


def test_inner_enum_write():
    class Foo(proto.Message):
        class Color(proto.Enum):
            COLOR_UNSPECIFIED = 0
            RED = 1
            GREEN = 2
            BLUE = 3

        color = proto.Field(Color, number=1)

    foo = Foo()
    foo.color = Foo.Color.GREEN
    assert foo.color == Foo.Color.GREEN
    assert foo.color == 2
    assert isinstance(foo.color, Foo.Color)
    assert Foo.pb(foo).color == 2
    assert foo.color


def test_enum_del():
    class Color(proto.Enum):
        COLOR_UNSPECIFIED = 0
        RED = 1
        GREEN = 2
        BLUE = 3

    class Foo(proto.Message):
        color = proto.Field(Color, number=1)

    foo = Foo(color=Color.BLUE)
    del foo.color
    assert foo.color == Color.COLOR_UNSPECIFIED
    assert foo.color == 0
    assert isinstance(foo.color, Color)
    assert 'color' not in foo
    assert not foo.color
    assert Foo.pb(foo).color == 0
