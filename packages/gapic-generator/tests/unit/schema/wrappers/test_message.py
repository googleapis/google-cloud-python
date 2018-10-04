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

import collections
from typing import Sequence

import pytest

from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers


def test_message_properties():
    message = make_message('MyMessage')
    assert message.name == 'MyMessage'


def test_message_docstring():
    L = descriptor_pb2.SourceCodeInfo.Location

    meta = metadata.Metadata(documentation=L(
        leading_comments='Lorem ipsum',
        trailing_comments='dolor set amet',
    ))
    message = make_message('Name', meta=meta)
    assert message.meta.doc == 'Lorem ipsum'


def test_message_ident():
    message = make_message('Baz', package='foo.v1', module='bar')
    assert str(message.ident) == 'bar.Baz'
    assert message.ident.sphinx == '~.bar.Baz'


def test_get_field():
    fields = (make_field('field_one'), make_field('field_two'))
    message = make_message('Message', fields=fields)
    field_one = message.get_field('field_one')
    assert isinstance(field_one, wrappers.Field)
    assert field_one.name == 'field_one'


def test_get_field_recursive():
    # Create the inner message.
    inner_fields = (make_field('zero'), make_field('one'))
    inner = make_message('Inner', fields=inner_fields, package='foo.v1')

    # Create the outer message, which contains an Inner as a field.
    outer_field = make_field('inner', message=inner)
    outer = make_message('Outer', fields=(outer_field,))

    # Assert that a recusive retrieval works.
    assert outer.get_field('inner', 'zero') == inner_fields[0]
    assert outer.get_field('inner', 'one') == inner_fields[1]


def test_get_field_nonterminal_repeated_error():
    # Create the inner message.
    inner_fields = (make_field('zero'), make_field('one'))
    inner = make_message('Inner', fields=inner_fields, package='foo.v1')

    # Create the outer message, which contains an Inner as a field.
    outer_field = make_field('inner', message=inner, repeated=True)
    outer = make_message('Outer', fields=(outer_field,))

    # Assert that a recusive retrieval fails.
    with pytest.raises(KeyError):
        assert outer.get_field('inner', 'zero') == inner_fields[0]
    with pytest.raises(KeyError):
        assert outer.get_field('inner', 'one') == inner_fields[1]


def make_message(name: str, package: str = 'foo.bar.v1', module: str = 'baz',
        fields: Sequence[wrappers.Field] = (), meta: metadata.Metadata = None,
        ) -> wrappers.MessageType:
    message_pb = descriptor_pb2.DescriptorProto(
        name=name,
        field=[i.field_pb for i in fields],
    )
    return wrappers.MessageType(
        message_pb=message_pb,
        fields=collections.OrderedDict((i.name, i) for i in fields),
        nested_messages={},
        nested_enums={},
        meta=meta or metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(package.split('.')),
            module=module,
        )),
    )


def make_field(name: str, repeated: bool = False,
               message: wrappers.MessageType = None,
               meta: metadata.Metadata = None, **kwargs) -> wrappers.Method:
    if message:
        kwargs['type_name'] = str(message.meta.address)
    field_pb = descriptor_pb2.FieldDescriptorProto(
        name=name,
        label=3 if repeated else 1,
        **kwargs
    )
    return wrappers.Field(
        field_pb=field_pb,
        message=message,
        meta=meta or metadata.Metadata(),
    )
