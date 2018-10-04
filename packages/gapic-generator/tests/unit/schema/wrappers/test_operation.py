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

from gapic.schema import metadata
from gapic.schema import wrappers


def test_operation():
    lro_response = wrappers.MessageType(
        fields={},
        nested_messages={},
        nested_enums={},
        message_pb=descriptor_pb2.DescriptorProto(name='LroResponse'),
    )
    operation = wrappers.OperationType(lro_response=lro_response)
    assert operation.name == 'Operation'
    assert str(operation.ident) == 'operation.Operation'
    assert operation.ident.sphinx == '~.operation.Operation'


def test_operation_meta():
    lro_response = wrappers.MessageType(
        fields={},
        nested_messages={},
        nested_enums={},
        message_pb=descriptor_pb2.DescriptorProto(name='LroResponse'),
        meta=metadata.Metadata(address=metadata.Address(
            name='LroResponse',
            module='foo',
        )),
    )
    operation = wrappers.OperationType(lro_response=lro_response)
    assert 'representing a long-running operation' in operation.meta.doc
    assert ':class:`~.foo.LroResponse`' in operation.meta.doc
