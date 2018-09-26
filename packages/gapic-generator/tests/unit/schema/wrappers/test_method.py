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

from google.api import annotations_pb2
from google.api import signature_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers


def test_method_types():
    input_msg = make_message(name='Input', module='baz')
    output_msg = make_message(name='Output', module='baz')
    method = make_method('DoSomething', input_msg, output_msg,
                         package='foo.bar', module='bacon')
    assert method.name == 'DoSomething'
    assert method.input.name == 'Input'
    assert method.output.name == 'Output'


def test_method_signature():
    # Set up a meaningful input message.
    input_msg = make_message(name='Input', fields=(
        make_field('int_field', type=5),
        make_field('bool_field', type=8),
        make_field('float_field', type=2),
    ))

    # Create the method.
    method = make_method('SendStuff', input_message=input_msg)

    # Edit the underlying method pb2 post-hoc to add the appropriate annotation
    # (google.api.signature).
    method.options.Extensions[annotations_pb2.method_signature].MergeFrom(
        signature_pb2.MethodSignature(fields=['int_field', 'float_field'])
    )

    # We should get back just those two fields as part of the signature.
    assert len(method.signatures) == 1
    signature = method.signatures[0]
    assert tuple(signature.fields.keys()) == ('int_field', 'float_field')


def test_method_no_signature():
    assert len(make_method('Ping').signatures) == 0


def test_method_field_headers():
    method = make_method('DoSomething')
    assert isinstance(method.field_headers, collections.Sequence)


def test_method_unary_unary():
    method = make_method('F', client_streaming=False, server_streaming=False)
    assert method.grpc_stub_type == 'unary_unary'


def test_method_unary_stream():
    method = make_method('F', client_streaming=False, server_streaming=True)
    assert method.grpc_stub_type == 'unary_stream'


def test_method_stream_unary():
    method = make_method('F', client_streaming=True, server_streaming=False)
    assert method.grpc_stub_type == 'stream_unary'


def test_method_stream_stream():
    method = make_method('F', client_streaming=True, server_streaming=True)
    assert method.grpc_stub_type == 'stream_stream'


def make_method(
        name: str, input_message: wrappers.MessageType = None,
        output_message: wrappers.MessageType = None,
        package: str = 'foo.bar.v1', module: str = 'baz',
        **kwargs) -> wrappers.Method:
    # Use default input and output messages if they are not provided.
    input_message = input_message or make_message('MethodInput')
    output_message = output_message or make_message('MethodOutput')

    # Create the method pb2.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name=name,
        input_type=str(input_message.meta.address),
        output_type=str(output_message.meta.address),
        **kwargs
    )

    # Instantiate the wrapper class.
    return wrappers.Method(
        method_pb=method_pb,
        input=input_message,
        output=output_message,
        meta=metadata.Metadata(address=metadata.Address(
            name=name,
            package=package,
            module=module,
        )),
    )


def make_message(name: str, package: str = 'foo.bar.v1', module: str = 'baz',
        fields: Sequence[wrappers.Field] = (),
        ) -> wrappers.MessageType:
    message_pb = descriptor_pb2.DescriptorProto(
        name=name,
        field=[i.field_pb for i in fields],
    )
    return wrappers.MessageType(
        message_pb=message_pb,
        nested_messages={},
        nested_enums={},
        fields=collections.OrderedDict((i.name, i) for i in fields),
        meta=metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(package.split('.')),
            module=module,
        )),
    )


def make_field(name: str, repeated: bool = False,
               meta: metadata.Metadata = None, **kwargs) -> wrappers.Method:
    field_pb = descriptor_pb2.FieldDescriptorProto(
        name=name,
        label=3 if repeated else 1,
        **kwargs
    )
    return wrappers.Field(
        field_pb=field_pb,
        meta=meta or metadata.Metadata(),
    )
