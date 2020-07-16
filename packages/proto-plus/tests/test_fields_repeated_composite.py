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

from datetime import datetime
from datetime import timezone

import pytest

from google.protobuf import timestamp_pb2

import proto
from proto.datetime_helpers import DatetimeWithNanoseconds


def test_repeated_composite_init():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz(foos=[Foo(bar=42)])
    assert len(baz.foos) == 1
    assert baz.foos == baz.foos
    assert baz.foos[0].bar == 42


def test_repeated_composite_equality():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz(foos=[Foo(bar=42)])
    assert baz.foos == baz.foos


def test_repeated_composite_init_struct():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz(foos=[{"bar": 42}])
    assert len(baz.foos) == 1
    assert baz.foos[0].bar == 42


def test_repeated_composite_falsy_behavior():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    assert not baz.foos
    assert len(baz.foos) == 0


def test_repeated_composite_marshaled():
    class Foo(proto.Message):
        timestamps = proto.RepeatedField(
            proto.MESSAGE, message=timestamp_pb2.Timestamp, number=1,
        )

    foo = Foo(
        timestamps=[DatetimeWithNanoseconds(2012, 4, 21, 15, tzinfo=timezone.utc)]
    )
    foo.timestamps.append(timestamp_pb2.Timestamp(seconds=86400 * 365))
    foo.timestamps.append(DatetimeWithNanoseconds(2017, 10, 14, tzinfo=timezone.utc))
    assert all([isinstance(i, DatetimeWithNanoseconds) for i in foo.timestamps])
    assert all([isinstance(i, timestamp_pb2.Timestamp) for i in Foo.pb(foo).timestamps])
    assert foo.timestamps[0].year == 2012
    assert foo.timestamps[0].month == 4
    assert foo.timestamps[0].hour == 15
    assert foo.timestamps[1].year == 1971
    assert foo.timestamps[1].month == 1
    assert foo.timestamps[1].hour == 0
    assert foo.timestamps[2].year == 2017
    assert foo.timestamps[2].month == 10
    assert foo.timestamps[2].hour == 0


def test_repeated_composite_outer_write():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    baz.foos = [Foo(bar=96), Foo(bar=48)]
    assert len(baz.foos) == 2
    assert baz.foos[0].bar == 96
    assert baz.foos[1].bar == 48


def test_repeated_composite_append():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    baz.foos.append(Foo(bar=96))
    baz.foos.append({"bar": 72})
    assert len(baz.foos) == 2
    assert baz.foos[0].bar == 96
    assert baz.foos[1].bar == 72


def test_repeated_composite_insert():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    baz.foos.insert(0, {"bar": 72})
    baz.foos.insert(0, Foo(bar=96))
    assert len(baz.foos) == 2
    assert baz.foos[0].bar == 96
    assert baz.foos[1].bar == 72


def test_repeated_composite_iadd():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    baz.foos += [Foo(bar=96), Foo(bar=48)]
    assert len(baz.foos) == 2
    assert baz.foos[0].bar == 96
    assert baz.foos[1].bar == 48


def test_repeated_composite_set():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz(foos=[{"bar": 96}, {"bar": 48}])
    baz.foos[1] = Foo(bar=55)
    assert baz.foos[0].bar == 96
    assert baz.foos[1].bar == 55


def test_repeated_composite_set_wrong_type():
    class Foo(proto.Message):
        bar = proto.Field(proto.INT32, number=1)

    class NotFoo(proto.Message):
        eggs = proto.Field(proto.INT32, number=1)

    class Baz(proto.Message):
        foos = proto.RepeatedField(proto.MESSAGE, message=Foo, number=1)

    baz = Baz()
    with pytest.raises(TypeError):
        baz.foos.append(NotFoo(eggs=42))
