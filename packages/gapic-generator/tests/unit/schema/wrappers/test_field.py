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
from api_factory.schema.metadata import Address, Metadata


def get_field() -> wrappers.Field:
    field_pb = descriptor_pb2.FieldDescriptorProto(
        name='my_field',
        number=1,
        type=descriptor_pb2.FieldDescriptorProto.Type.Value('TYPE_BOOL'),
    )
    return wrappers.Field(field_pb=field_pb, meta=Metadata(
        address=Address(package=['foo', 'bar'], module='baz'),
        documentation=descriptor_pb2.SourceCodeInfo.Location(
            leading_comments='Lorem ipsum dolor set amet',
        ),
    ))


def test_field_properties():
    field = get_field()
    assert field.name == 'my_field'
    assert field.number == 1
    assert field.type == 8


def test_field_metadata():
    field = get_field()
    assert field.meta.doc == 'Lorem ipsum dolor set amet'
