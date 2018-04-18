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

from unittest import mock

import pytest

from google.protobuf import descriptor_pb2

from api_factory.schema import metadata
from api_factory.schema import wrappers
from api_factory.schema.api import API
from api_factory.schema.pb import client_pb2


def test_long_name():
    api = make_api(
        client=make_client(name='Genie', namespace=['Agrabah', 'Lamp']),
    )
    assert api.long_name == 'Agrabah Lamp Genie'


def test_warehouse_package_name_placeholder():
    api = make_api(client=make_client(name=''))
    assert api.warehouse_package_name == '<<< PACKAGE NAME >>>'
    assert bool(api.warehouse_package_name) is False


def test_warehouse_package_name_no_namespace():
    api = make_api(client=make_client(name='BigQuery', namespace=[]))
    assert api.warehouse_package_name == 'bigquery'


def test_warehouse_package_name_with_namespace():
    api = make_api(client=make_client(
        name='BigQuery',
        namespace=('Google', 'Cloud'),
    ))
    assert api.warehouse_package_name == 'google-cloud-bigquery'


def test_load():
    sentinel_message = descriptor_pb2.DescriptorProto()
    sentinel_enum = descriptor_pb2.EnumDescriptorProto()
    sentinel_service = descriptor_pb2.ServiceDescriptorProto()

    # Create a file descriptor proto. It does not matter that none
    # of the sentinels have actual data because this test just ensures
    # they are sent off to the correct methods unmodified.
    fdp = descriptor_pb2.FileDescriptorProto(
        name='my_proto_file.proto',
        package='google.example.v1',
        message_type=[sentinel_message],
        enum_type=[sentinel_enum],
        service=[sentinel_service],
    )

    # Create an API object.
    api = make_api()

    # Test the load function.
    with mock.patch.object(api, '_load_children') as lc:
        api.load(fdp)

        # There should be three total calls to load the different types
        # of children.
        assert lc.call_count == 3

        # The message type should come first.
        _, args, kwargs = lc.mock_calls[0]
        assert args[0][0] == sentinel_message
        assert kwargs['loader'] == api._load_descriptor

        # The enum type should come second.
        _, args, kwargs = lc.mock_calls[1]
        assert args[0][0] == sentinel_enum
        assert kwargs['loader'] == api._load_enum

        # The services should come third.
        _, args, kwargs = lc.mock_calls[2]
        assert args[0][0] == sentinel_service
        assert kwargs['loader'] == api._load_service


def test_load_comments_top_level():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Create a file descriptor proto.
    # This has comments which should be largely sharded and ferried off to the
    # correct sub-methods.
    locations = [
        L(path=[4, 0], leading_comments='foo'),
        L(path=[4, 0, 2, 0], leading_comments='bar'),
        L(path=[6, 0], leading_comments='baz'),
    ]
    fdp = descriptor_pb2.FileDescriptorProto(
        name='my_proto_file.proto',
        package='google.example.v1',
        source_code_info=descriptor_pb2.SourceCodeInfo(location=locations)
    )

    # Create an API object.
    api = make_api()

    # Test the load function. This sends empty arrays to each of the
    # individual child-processing function, but sends meaningful slices of
    # documentation (which is what this test is trying to confirm).
    with mock.patch.object(api, '_load_children') as lc:
        api.load(fdp)

        # There are still three total calls, like above.
        assert lc.call_count == 3

        # The `message_type` field has the ID of 4 in `FileDescriptorProto`,
        # so the two whose path begins with 4 should be sent, and in the
        # ad hoc dictionary that this method creates.
        _, args, kwargs = lc.mock_calls[0]
        assert kwargs['loader'] == api._load_descriptor
        assert kwargs['info'] == {
            0: {'TERMINAL': locations[0], 2: {0: {'TERMINAL': locations[1]}}},
        }

        # The `enum_type` field has the ID of 5 in `FileDescriptorProto`,
        # but no location objects were sent with a matching path, so it
        # will just get an empty dictionary.
        _, args, kwargs = lc.mock_calls[1]
        assert kwargs['loader'] == api._load_enum
        assert kwargs['info'] == {}

        # The `service_type` field has the ID of 6 in `FileDescriptorProto`,
        # so it will get the one location object that begins with 6.
        _, args, kwargs = lc.mock_calls[2]
        assert kwargs['loader'] == api._load_service
        assert kwargs['info'] == {0: {'TERMINAL': locations[2]}}


def test_load_children():
    # Set up the data to be sent to the method.
    children = (mock.sentinel.child_zero, mock.sentinel.child_one)
    address = metadata.Address()
    info = {0: mock.sentinel.info_zero, 1: mock.sentinel.info_one}
    loader = mock.Mock(create_autospec=lambda child, address, info: None)

    # Run the `_load_children` method.
    make_api()._load_children(children, loader, address, info)

    # Assert that the loader ran in the expected way (twice, once per child).
    assert loader.call_count == 2
    _, args, kwargs = loader.mock_calls[0]
    assert args[0] == mock.sentinel.child_zero
    assert kwargs['info'] == mock.sentinel.info_zero
    _, args, kwargs = loader.mock_calls[1]
    assert args[0] == mock.sentinel.child_one
    assert kwargs['info'] == mock.sentinel.info_one


def test_get_fields():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Set up data to test with.
    field_pbs = [
        descriptor_pb2.FieldDescriptorProto(name='spam'),
        descriptor_pb2.FieldDescriptorProto(name='eggs'),
    ]
    address = metadata.Address(package=['foo', 'bar'], module='baz')
    info = {1: {'TERMINAL': L(leading_comments='Eggs.')}}

    # Run the method under test.
    fields = make_api()._get_fields(field_pbs, address=address, info=info)

    # Test that we get two field objects back.
    assert len(fields) == 2
    for field in fields.values():
        assert isinstance(field, wrappers.Field)
    items = iter(fields.items())

    # Test that the first field is spam, and it has no documentation
    # (since `info` has no `0` key).
    field_name, field = next(items)
    assert field_name == 'spam'
    assert field.meta.doc == ''

    # Test that the second field is eggs, and it does have documentation
    # (since `info` has a `1` key).
    field_name, field = next(items)
    assert field_name == 'eggs'
    assert field.meta.doc == 'Eggs.'

    # Done.
    with pytest.raises(StopIteration):
        next(items)


def test_get_methods():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Start with an empty API object.
    api = make_api()

    # Load the input and output type for a method into the API object.
    address = metadata.Address(package=['foo', 'bar'], module='baz')
    api._load_descriptor(descriptor_pb2.DescriptorProto(name='In'),
                         address=address, info={})
    api._load_descriptor(descriptor_pb2.DescriptorProto(name='Out'),
                         address=address, info={})

    # Run the method under test.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name='DoThings',
        input_type='foo.bar.In',
        output_type='foo.bar.Out',
    )
    methods = api._get_methods([method_pb], address=address, info={})

    # Test that we get a method object back.
    assert len(methods) == 1
    for method in methods.values():
        assert isinstance(method, wrappers.Method)
    items = iter(methods.items())

    # Test that the method has what we expect, an input and output type
    # and appropriate name.
    method_key, method = next(items)
    assert method_key == 'DoThings'
    assert isinstance(method.input, wrappers.MessageType)
    assert method.input.name == 'In'
    assert isinstance(method.output, wrappers.MessageType)
    assert method.output.name == 'Out'

    # Done.
    with pytest.raises(StopIteration):
        next(items)


def test_load_descriptor():
    message_pb = descriptor_pb2.DescriptorProto(name='Riddle')
    address = metadata.Address(package=['foo', 'bar', 'v1'], module='baz')
    api = make_api()
    api._load_descriptor(message_pb=message_pb, address=address, info={})
    assert 'foo.bar.v1.Riddle' in api.messages
    assert isinstance(api.messages['foo.bar.v1.Riddle'], wrappers.MessageType)
    assert api.messages['foo.bar.v1.Riddle'].message_pb == message_pb


def test_load_enum():
    # Set up the appropriate protos.
    enum_value_pb = descriptor_pb2.EnumValueDescriptorProto(name='A', number=0)
    enum_pb = descriptor_pb2.EnumDescriptorProto(
        name='Enum',
        value=[enum_value_pb],
    )

    # Load it into the API.
    address = metadata.Address(package=['foo', 'bar', 'v1'], module='baz')
    api = make_api()
    api._load_enum(enum_pb, address=address, info={})

    # Assert we got back the right stuff.
    assert 'foo.bar.v1.Enum' in api.enums
    assert isinstance(api.enums['foo.bar.v1.Enum'], wrappers.EnumType)
    assert api.enums['foo.bar.v1.Enum'].enum_pb == enum_pb
    assert len(api.enums['foo.bar.v1.Enum'].values) == 1


def test_load_service():
    service_pb = descriptor_pb2.ServiceDescriptorProto(name='RiddleService')
    address = metadata.Address(package=['foo', 'bar', 'v1'], module='baz')
    api = make_api()
    api._load_service(service_pb, address=address, info={})
    assert 'foo.bar.v1.RiddleService' in api.services
    assert isinstance(api.services['foo.bar.v1.RiddleService'],
                      wrappers.Service)
    assert api.services['foo.bar.v1.RiddleService'].service_pb == service_pb


def make_api(client: client_pb2.Client = None) -> API:
    return API(client=client or make_client())


def make_client(**kwargs) -> client_pb2.Client:
    kwargs.setdefault('name', 'Hatstand')
    kwargs.setdefault('namespace', ('Google', 'Cloud'))
    kwargs.setdefault('version', 'v1')
    return client_pb2.Client(**kwargs)
