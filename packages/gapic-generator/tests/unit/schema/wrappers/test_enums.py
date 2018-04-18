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

from google.protobuf import descriptor_pb2

from api_factory.schema import wrappers


def get_enum() -> wrappers.EnumType:
    enum_value_pbs = [
        descriptor_pb2.EnumValueDescriptorProto(name='RED', number=1),
        descriptor_pb2.EnumValueDescriptorProto(name='GREEN', number=2),
        descriptor_pb2.EnumValueDescriptorProto(name='BLUE', number=3),
    ]
    enum_pb = descriptor_pb2.EnumDescriptorProto(
        name='Color',
        value=enum_value_pbs,
    )
    return wrappers.EnumType(
        enum_pb=enum_pb,
        values=[wrappers.EnumValueType(enum_value_pb=evpb)
                for evpb in enum_value_pbs],
    )


def test_enum_properties():
    enum_type = get_enum()
    assert enum_type.name == 'Color'


def test_enum_value_properties():
    enum_type = get_enum()
    for ev, expected in zip(enum_type.values, ('RED', 'GREEN', 'BLUE')):
        assert ev.name == expected
