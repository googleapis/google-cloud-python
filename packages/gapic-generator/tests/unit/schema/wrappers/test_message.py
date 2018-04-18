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


def get_message() -> wrappers.MessageType:
    message_pb = descriptor_pb2.DescriptorProto(name='MyMessage')
    return wrappers.MessageType(
        fields=[],
        message_pb=message_pb,
        meta=metadata.Metadata(
            address=metadata.Address(package=['foo', 'bar'], module='baz'),
            documentation=descriptor_pb2.SourceCodeInfo.Location(
                leading_comments='Lorem ipsum dolor set amet',
            ),
        ),
    )


def test_message_properties():
    message = get_message()
    assert message.name == 'MyMessage'


def test_message_docstring():
    message = get_message()
    assert message.meta.doc == 'Lorem ipsum dolor set amet'


def test_message_python_package():
    message = get_message()
    assert message.pb2_module == 'baz_pb2'
