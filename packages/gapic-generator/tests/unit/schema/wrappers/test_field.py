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

from google.api import annotations_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import wrappers


def test_field_properties():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    field = make_field(name='my_field', number=1, type=Type.Value('TYPE_BOOL'))
    assert field.name == 'my_field'
    assert field.number == 1
    assert field.type.python_type == bool


def test_field_is_primitive():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    primitive_field = make_field(type=Type.Value('TYPE_INT32'))
    assert primitive_field.is_primitive


def test_field_proto_type():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    primitive_field = make_field(type=Type.Value('TYPE_INT32'))
    assert primitive_field.proto_type == 'INT32'


def test_field_not_primitive():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    message = wrappers.MessageType(
        fields={},
        nested_messages={},
        nested_enums={},
        message_pb=descriptor_pb2.DescriptorProto(),
    )
    non_primitive_field = make_field(
        type=Type.Value('TYPE_MESSAGE'),
        type_name='bogus.Message',
        message=message,
    )
    assert not non_primitive_field.is_primitive


def test_ident():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    field = make_field(type=Type.Value('TYPE_BOOL'))
    assert str(field.ident) == 'bool'


def test_ident_repeated():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    REP = descriptor_pb2.FieldDescriptorProto.Label.Value('LABEL_REPEATED')
    field = make_field(type=Type.Value('TYPE_BOOL'), label=REP)
    assert str(field.ident) == 'Sequence[bool]'


def test_repeated():
    REP = descriptor_pb2.FieldDescriptorProto.Label.Value('LABEL_REPEATED')
    field = make_field(label=REP)
    assert field.repeated


def test_not_repeated():
    OPT = descriptor_pb2.FieldDescriptorProto.Label.Value('LABEL_OPTIONAL')
    field = make_field(label=OPT)
    assert not field.repeated


def test_required():
    field = make_field()
    field.options.Extensions[annotations_pb2.required] = True
    assert field.required


def test_not_required():
    field = make_field()
    assert not field.required


def test_ident_sphinx():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    field = make_field(type=Type.Value('TYPE_BOOL'))
    assert field.ident.sphinx == 'bool'


def test_ident_sphinx_repeated():
    Type = descriptor_pb2.FieldDescriptorProto.Type
    REP = descriptor_pb2.FieldDescriptorProto.Label.Value('LABEL_REPEATED')
    field = make_field(type=Type.Value('TYPE_BOOL'), label=REP)
    assert field.ident.sphinx == 'Sequence[bool]'


def test_type_primitives():
    T = descriptor_pb2.FieldDescriptorProto.Type
    assert make_field(type=T.Value('TYPE_FLOAT')).type.python_type == float
    assert make_field(type=T.Value('TYPE_INT64')).type.python_type == int
    assert make_field(type=T.Value('TYPE_BOOL')).type.python_type == bool
    assert make_field(type=T.Value('TYPE_STRING')).type.python_type == str
    assert make_field(type=T.Value('TYPE_BYTES')).type.python_type == bytes


def test_type_message():
    T = descriptor_pb2.FieldDescriptorProto.Type
    message = wrappers.MessageType(
        fields={},
        nested_messages={},
        nested_enums={},
        message_pb=descriptor_pb2.DescriptorProto(),
    )
    field = make_field(
        type=T.Value('TYPE_MESSAGE'),
        type_name='bogus.Message',
        message=message,
    )
    assert field.type == message


def test_type_enum():
    T = descriptor_pb2.FieldDescriptorProto.Type
    enum = wrappers.EnumType(
        values={},
        enum_pb=descriptor_pb2.EnumDescriptorProto(),
    )
    field = make_field(
        type=T.Value('TYPE_ENUM'),
        type_name='bogus.Enumerable',
        enum=enum,
    )
    assert field.type == enum


def test_type_invalid():
    T = descriptor_pb2.FieldDescriptorProto.Type
    with pytest.raises(TypeError):
        make_field(type=T.Value('TYPE_GROUP')).type


def make_field(*, message=None, enum=None, **kwargs) -> wrappers.Field:
    kwargs.setdefault('name', 'my_field')
    kwargs.setdefault('number', 1)
    kwargs.setdefault('type',
        descriptor_pb2.FieldDescriptorProto.Type.Value('TYPE_BOOL'),
    )
    field_pb = descriptor_pb2.FieldDescriptorProto(**kwargs)
    return wrappers.Field(field_pb=field_pb, message=message, enum=enum)
