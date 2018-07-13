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

from google.api import signature_pb2
from google.protobuf import descriptor_pb2

from api_factory.schema import metadata
from api_factory.schema import wrappers


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


def test_method_signature():
    method = get_method()
    assert isinstance(method.signature, signature_pb2.MethodSignature)


def test_method_field_headers():
    method = get_method()
    assert isinstance(method.field_headers, collections.Sequence)
