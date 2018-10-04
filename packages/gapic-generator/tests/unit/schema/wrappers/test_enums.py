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

from typing import Tuple

from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers


def test_enum_properties():
    enum_type = make_enum(name='Color')
    assert enum_type.name == 'Color'


def test_enum_value_properties():
    enum_type = make_enum(name='Irrelevant', values=(
        ('RED', 1), ('GREEN', 2), ('BLUE', 3),
    ))
    assert len(enum_type.values) == 3
    for ev, expected in zip(enum_type.values, ('RED', 'GREEN', 'BLUE')):
        assert ev.name == expected


def test_enum_ident():
    message = make_enum('Baz', package='foo.v1', module='bar')
    assert str(message.ident) == 'bar.Baz'
    assert message.ident.sphinx == '~.bar.Baz'


def make_enum(name: str, package: str = 'foo.bar.v1', module: str = 'baz',
        values: Tuple[str, int] = (), meta: metadata.Metadata = None,
        ) -> wrappers.EnumType:
    enum_value_pbs = [
        descriptor_pb2.EnumValueDescriptorProto(name=i[0], number=i[1])
        for i in values
    ]
    enum_pb = descriptor_pb2.EnumDescriptorProto(
        name=name,
        value=enum_value_pbs,
    )
    return wrappers.EnumType(
        enum_pb=enum_pb,
        values=[wrappers.EnumValueType(enum_value_pb=evpb)
                for evpb in enum_value_pbs],
        meta=meta or metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(package.split('.')),
            module=module,
        )),
    )
