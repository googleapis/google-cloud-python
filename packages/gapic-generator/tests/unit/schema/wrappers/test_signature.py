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

from google.protobuf import descriptor_pb2

from gapic.schema import wrappers


def test_signature_dispatch_field():
    T = descriptor_pb2.FieldDescriptorProto.Type
    fields = collections.OrderedDict((
        ('foo', make_field(name='foo', type=T.Value('TYPE_INT32'))),
        ('bar', make_field(name='bar', type=T.Value('TYPE_BOOL'))),
    ))
    signature = wrappers.MethodSignature(name='spam', fields=fields)
    assert signature.dispatch_field == fields['foo']


def test_signatures_magic_methods():
    T = descriptor_pb2.FieldDescriptorProto.Type
    fields = collections.OrderedDict((
        ('foo', make_field(name='foo', type=T.Value('TYPE_INT32'))),
        ('bar', make_field(name='bar', type=T.Value('TYPE_BOOL'))),
    ))
    signatures = wrappers.MethodSignatures(all=(
        wrappers.MethodSignature(name='spam', fields=fields),
        wrappers.MethodSignature(name='eggs', fields={
            'foo': fields['foo'],
        }),
    ))
    assert len(signatures) == 2
    assert tuple([i for i in signatures]) == signatures.all
    assert signatures[0] == signatures.all[0]


def test_signatures_single_dispatch():
    T = descriptor_pb2.FieldDescriptorProto.Type
    fields = (
        ('foo', make_field(
            message=wrappers.MessageType(
                fields={},
                message_pb=descriptor_pb2.DescriptorProto(name='Bacon'),
                nested_enums={},
                nested_messages={},
            ),
            name='bar',
            type=T.Value('TYPE_MESSAGE'),
            type_name='bogus.Message',
        )),
        ('bar', make_field(name='foo', type=T.Value('TYPE_INT32'))),
    )
    signatures = wrappers.MethodSignatures(all=(
        wrappers.MethodSignature(
            name='spam',
            fields=collections.OrderedDict(fields),
        ),
        wrappers.MethodSignature(
            name='eggs',
            fields=collections.OrderedDict(reversed(fields)),
        ),
    ))
    assert len(signatures) == 2
    assert len(signatures.single_dispatch) == 1
    assert signatures.single_dispatch[0] == signatures[1]


def make_field(*, message=None, enum=None, **kwargs) -> wrappers.Field:
    kwargs.setdefault('name', 'my_field')
    kwargs.setdefault('number', 1)
    kwargs.setdefault('type',
        descriptor_pb2.FieldDescriptorProto.Type.Value('TYPE_BOOL'),
    )
    field_pb = descriptor_pb2.FieldDescriptorProto(**kwargs)
    return wrappers.Field(field_pb=field_pb, message=message, enum=enum)
