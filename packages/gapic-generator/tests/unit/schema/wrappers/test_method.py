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

from api_factory.schema import metadata
from api_factory.schema import wrappers
from api_factory.schema.pb import headers_pb2
from api_factory.schema.pb import overload_pb2


def get_method() -> wrappers.Method:
    # Create the address where this method lives, and the types live,
    # and make them distinct.
    method_addr = metadata.Address(package=['foo', 'bar'], module='baz')
    types_addr = metadata.Address(package=['foo', 'bar'], module='bacon')

    # Create the method pb2 and set an overload in it.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name='DoTheThings',
        input_type='foo.bar.Input',
        output_type='foo.bar.Output',
    )

    # Set an overload in the method descriptor.
    ext_key = overload_pb2.overloads
    method_pb.options.Extensions[ext_key].extend([overload_pb2.Overload()])

    # Set a field header in the method descriptor.
    ext_key = headers_pb2.field_headers
    method_pb.options.Extensions[ext_key].extend([headers_pb2.FieldHeader()])

    # Instantiate the wrapper class.
    return wrappers.Method(
        method_pb=method_pb,
        input=wrappers.MessageType(
            fields=[],
            message_pb=descriptor_pb2.DescriptorProto(name='Input'),
            meta=metadata.Metadata(address=types_addr),
        ),
        output=wrappers.MessageType(
            fields=[],
            message_pb=descriptor_pb2.DescriptorProto(name='Output'),
            meta=metadata.Metadata(address=types_addr),
        ),
        meta=metadata.Metadata(address=method_addr),
    )


def test_method_properties():
    method = get_method()
    assert method.name == 'DoTheThings'


def test_method_types():
    method = get_method()
    assert method.input.name == 'Input'
    assert method.input.pb2_module == 'bacon_pb2'
    assert method.output.name == 'Output'
    assert method.output.pb2_module == 'bacon_pb2'


def test_method_overloads():
    method = get_method()
    for overload in method.overloads:
        assert isinstance(overload, overload_pb2.Overload)


def test_method_field_headers():
    method = get_method()
    for field_header in method.field_headers:
        assert isinstance(field_header, headers_pb2.FieldHeader)
