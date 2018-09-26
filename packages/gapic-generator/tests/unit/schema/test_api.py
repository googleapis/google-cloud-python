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

from typing import Sequence
from unittest import mock

from google.longrunning import operations_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import api
from gapic.schema import naming
from gapic.schema import wrappers


def test_api_build():
    # Put together a couple of minimal protos.
    fd = (
        make_file_pb2(
            name='dep.proto',
            package='google.dep',
            messages=(make_message_pb2(name='ImportedMessage', fields=()),),
        ),
        make_file_pb2(
            name='foo.proto',
            package='google.example.v1',
            messages=(
                make_message_pb2(name='Foo', fields=()),
                make_message_pb2(name='GetFooRequest', fields=(
                    make_field_pb2(name='imported_message', number=1,
                                   type_name='.google.dep.ImportedMessage'),
                )),
                make_message_pb2(name='GetFooResponse', fields=(
                    make_field_pb2(name='foo', number=1,
                                   type_name='.google.example.v1.Foo'),
                )),
            ),
            services=(descriptor_pb2.ServiceDescriptorProto(
                name='FooService',
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name='GetFoo',
                        input_type='google.example.v1.GetFooRequest',
                        output_type='google.example.v1.GetFooResponse',
                    ),
                ),
            ),),
        ),
    )

    # Create an API with those protos.
    api_schema = api.API.build(fd, package='google.example.v1')

    # Establish that the API has the data expected.
    assert isinstance(api_schema, api.API)
    assert len(api_schema.protos) == 2
    assert 'google.dep.ImportedMessage' in api_schema.messages
    assert 'google.example.v1.Foo' in api_schema.messages
    assert 'google.example.v1.GetFooRequest' in api_schema.messages
    assert 'google.example.v1.GetFooResponse' in api_schema.messages
    assert 'google.example.v1.FooService' in api_schema.services
    assert len(api_schema.enums) == 0


def test_proto_build():
    fdp = descriptor_pb2.FileDescriptorProto(
        name='my_proto_file.proto',
        package='google.example.v1',
    )
    proto = api.Proto.build(fdp, file_to_generate=True)
    assert isinstance(proto, api.Proto)


def test_proto_builder_constructor():
    sentinel_message = descriptor_pb2.DescriptorProto()
    sentinel_enum = descriptor_pb2.EnumDescriptorProto()
    sentinel_service = descriptor_pb2.ServiceDescriptorProto()

    # Create a file descriptor proto. It does not matter that none
    # of the sentinels have actual data because this test just ensures
    # they are sent off to the correct methods unmodified.
    fdp = make_file_pb2(
        messages=(sentinel_message,),
        enums=(sentinel_enum,),
        services=(sentinel_service,),
    )

    # Test the load function.
    with mock.patch.object(api._ProtoBuilder, '_load_children') as lc:
        pb = api._ProtoBuilder(fdp, file_to_generate=True)

        # There should be three total calls to load the different types
        # of children.
        assert lc.call_count == 3

        # The enum type should come first.
        _, args, _ = lc.mock_calls[0]
        assert args[0][0] == sentinel_enum
        assert args[1] == pb._load_enum

        # The message type should come second.
        _, args, _ = lc.mock_calls[1]
        assert args[0][0] == sentinel_message
        assert args[1] == pb._load_message

        # The services should come third.
        _, args, _ = lc.mock_calls[2]
        assert args[0][0] == sentinel_service
        assert args[1] == pb._load_service


def test_not_target_file():
    """Establish that services are not ignored for untargeted protos."""
    message_pb = make_message_pb2(name='Foo',
        fields=(make_field_pb2(name='bar', type=3, number=1),)
    )
    service_pb = descriptor_pb2.ServiceDescriptorProto()
    fdp = make_file_pb2(messages=(message_pb,), services=(service_pb,))

    # Actually make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=False)

    # The proto object should have the message, but no service.
    assert len(proto.messages) == 1
    assert len(proto.services) == 0


def test_messages():
    L = descriptor_pb2.SourceCodeInfo.Location

    message_pb = make_message_pb2(name='Foo',
        fields=(make_field_pb2(name='bar', type=3, number=1),)
    )
    locations = (
        L(path=(4, 0), leading_comments='This is the Foo message.'),
        L(path=(4, 0, 2, 0), leading_comments='This is the bar field.'),
    )
    fdp = make_file_pb2(
        messages=(message_pb,),
        locations=locations,
        package='google.example.v2',
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True)

    # Get the message.
    assert len(proto.messages) == 1
    message = proto.messages['google.example.v2.Foo']
    assert isinstance(message, wrappers.MessageType)
    assert message.meta.doc == 'This is the Foo message.'
    assert len(message.fields) == 1
    assert message.fields['bar'].meta.doc == 'This is the bar field.'


def test_messages_reverse_declaration_order():
    # Test that if a message is used as a field higher in the same file,
    # that things still work.
    message_pbs = (
        make_message_pb2(name='Foo', fields=(
            make_field_pb2(name='bar', number=1,
                           type_name='.google.example.v3.Bar'),
            ),
        ),
        make_message_pb2(name='Bar'),
    )
    fdp = make_file_pb2(
        messages=message_pbs,
        package='google.example.v3',
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True)

    # Get the message.
    assert len(proto.messages) == 2
    Foo = proto.messages['google.example.v3.Foo']
    assert Foo.fields['bar'].message == proto.messages['google.example.v3.Bar']


def test_messages_recursive():
    # Test that if a message is used inside itself, that things will still
    # work.
    message_pbs = (
        make_message_pb2(name='Foo', fields=(
            make_field_pb2(name='foo', number=1,
                           type_name='.google.example.v3.Foo'),
            ),
        ),
    )
    fdp = make_file_pb2(
        messages=message_pbs,
        package='google.example.v3',
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True)

    # Get the message.
    assert len(proto.messages) == 1
    Foo = proto.messages['google.example.v3.Foo']
    assert Foo.fields['foo'].message == proto.messages['google.example.v3.Foo']


def test_messages_nested():
    # Test that a nested message works properly.
    message_pbs = (
        make_message_pb2(name='Foo', nested_type=(
            make_message_pb2(name='Bar'),
        )),
    )
    fdp = make_file_pb2(
        messages=message_pbs,
        package='google.example.v3',
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True)

    # Set short variables for the names.
    foo = 'google.example.v3.Foo'
    bar = 'google.example.v3.Foo.Bar'

    # Get the message.
    assert len(proto.messages) == 2
    assert proto.messages[foo].name == 'Foo'
    assert proto.messages[bar].name == 'Bar'

    # Assert that the `top` shim only shows top-level messages.
    assert len(proto.top.messages) == 1
    assert proto.top.messages[foo] is proto.messages[foo]
    assert bar not in proto.top.messages


def test_services():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Set up messages for our RPC.
    request_message_pb = make_message_pb2(name='GetFooRequest',
        fields=(make_field_pb2(name='name', type=9, number=1),)
    )
    response_message_pb = make_message_pb2(name='GetFooResponse', fields=())

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='FooService',
        method=(descriptor_pb2.MethodDescriptorProto(
            name='GetFoo',
            input_type='google.example.v2.GetFooRequest',
            output_type='google.example.v2.GetFooResponse',
        ),),
    )

    # Fake-document our fake stuff.
    locations = (
        L(path=(6, 0), leading_comments='This is the FooService service.'),
        L(path=(6, 0, 2, 0), leading_comments='This is the GetFoo method.'),
        L(path=(4, 0), leading_comments='This is the GetFooRequest message.'),
        L(path=(4, 1), leading_comments='This is the GetFooResponse message.'),
    )

    # Finally, set up the file that encompasses these.
    fdp = make_file_pb2(
        package='google.example.v2',
        messages=(request_message_pb, response_message_pb),
        services=(service_pb,),
        locations=locations,
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True)

    # Establish that our data looks correct.
    assert len(proto.services) == 1
    assert len(proto.messages) == 2
    service = proto.services['google.example.v2.FooService']
    assert service.meta.doc == 'This is the FooService service.'
    assert len(service.methods) == 1
    method = service.methods['GetFoo']
    assert method.meta.doc == 'This is the GetFoo method.'
    assert isinstance(method.input, wrappers.MessageType)
    assert isinstance(method.output, wrappers.MessageType)
    assert method.input.name == 'GetFooRequest'
    assert method.input.meta.doc == 'This is the GetFooRequest message.'
    assert method.output.name == 'GetFooResponse'
    assert method.output.meta.doc == 'This is the GetFooResponse message.'


def test_prior_protos():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Set up a prior proto that mimics google/protobuf/empty.proto
    empty_proto = api.Proto.build(make_file_pb2(
        name='empty.proto', package='google.protobuf',
        messages=(make_message_pb2(name='Empty'),),
    ), file_to_generate=False)

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='PingService',
        method=(descriptor_pb2.MethodDescriptorProto(
            name='Ping',
            input_type='google.protobuf.Empty',
            output_type='google.protobuf.Empty',
        ),),
    )

    # Fake-document our fake stuff.
    locations = (
        L(path=(6, 0), leading_comments='This is the PingService service.'),
        L(path=(6, 0, 2, 0), leading_comments='This is the Ping method.'),
    )

    # Finally, set up the file that encompasses these.
    fdp = make_file_pb2(
        package='google.example.v1',
        services=(service_pb,),
        locations=locations,
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True, prior_protos={
        'google/protobuf/empty.proto': empty_proto,
    })

    # Establish that our data looks correct.
    assert len(proto.services) == 1
    assert len(empty_proto.messages) == 1
    assert len(proto.messages) == 0
    service = proto.services['google.example.v1.PingService']
    assert service.meta.doc == 'This is the PingService service.'
    assert len(service.methods) == 1
    method = service.methods['Ping']
    assert isinstance(method.input, wrappers.MessageType)
    assert isinstance(method.output, wrappers.MessageType)
    assert method.input.name == 'Empty'
    assert method.output.name == 'Empty'
    assert method.meta.doc == 'This is the Ping method.'


def test_lro():
    # Set up a prior proto that mimics google/protobuf/empty.proto
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False)

    # Set up a method with LRO annotations.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='AsyncDoThing',
        input_type='google.example.v3.AsyncDoThingRequest',
        output_type='google.longrunning.Operation',
    )
    method_pb2.options.Extensions[operations_pb2.operation_types].MergeFrom(
        operations_pb2.OperationTypes(
            response='google.example.v3.AsyncDoThingResponse',
            metadata='google.example.v3.AsyncDoThingMetadata',
        ),
    )

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='LongRunningService',
        method=(method_pb2,),
    )

    # Set up the messages, including the annotated ones.
    messages = (
        make_message_pb2(name='AsyncDoThingRequest', fields=()),
        make_message_pb2(name='AsyncDoThingResponse', fields=()),
        make_message_pb2(name='AsyncDoThingMetadata', fields=()),
    )

    # Finally, set up the file that encompasses these.
    fdp = make_file_pb2(
        package='google.example.v3',
        messages=messages,
        services=(service_pb,),
    )

    # Make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=True, prior_protos={
        'google/longrunning/operations.proto': lro_proto,
    })

    # Establish that our data looks correct.
    assert len(proto.services) == 1
    assert len(proto.messages) == 3
    assert len(lro_proto.messages) == 1


def test_enums():
    L = descriptor_pb2.SourceCodeInfo.Location
    enum_pb = descriptor_pb2.EnumDescriptorProto(name='Silly', value=(
        descriptor_pb2.EnumValueDescriptorProto(name='ZERO', number=0),
        descriptor_pb2.EnumValueDescriptorProto(name='ONE', number=1),
        descriptor_pb2.EnumValueDescriptorProto(name='THREE', number=3),
    ))
    fdp = make_file_pb2(package='google.enum.v1', enums=(enum_pb,), locations=(
        L(path=(5, 0), leading_comments='This is the Silly enum.'),
        L(path=(5, 0, 2, 0), leading_comments='This is the zero value.'),
        L(path=(5, 0, 2, 1), leading_comments='This is the one value.'),
    ))
    proto = api.Proto.build(fdp, file_to_generate=True)
    assert len(proto.enums) == 1
    enum = proto.enums['google.enum.v1.Silly']
    assert enum.meta.doc == 'This is the Silly enum.'
    assert isinstance(enum, wrappers.EnumType)
    assert len(enum.values) == 3
    assert all([isinstance(i, wrappers.EnumValueType) for i in enum.values])
    assert enum.values[0].name == 'ZERO'
    assert enum.values[0].meta.doc == 'This is the zero value.'
    assert enum.values[1].name == 'ONE'
    assert enum.values[1].meta.doc == 'This is the one value.'
    assert enum.values[2].name == 'THREE'
    assert enum.values[2].meta.doc == ''


def make_file_pb2(name: str = 'my_proto.proto', package: str = 'example.v1', *,
        messages: Sequence[descriptor_pb2.DescriptorProto] = (),
        enums: Sequence[descriptor_pb2.EnumDescriptorProto] = (),
        services: Sequence[descriptor_pb2.ServiceDescriptorProto] = (),
        locations: Sequence[descriptor_pb2.SourceCodeInfo.Location] = (),
        ) -> descriptor_pb2.FileDescriptorProto:
    return descriptor_pb2.FileDescriptorProto(
        name=name,
        package=package,
        message_type=messages,
        enum_type=enums,
        service=services,
        source_code_info=descriptor_pb2.SourceCodeInfo(location=locations),
    )


def make_message_pb2(
        name: str,
        fields: tuple = (),
        **kwargs
        ) -> descriptor_pb2.DescriptorProto:
    return descriptor_pb2.DescriptorProto(name=name, field=fields, **kwargs)


def make_field_pb2(name: str, number: int,
        type: int = 11,  # 11 == message
        type_name: str = None,
        ) -> descriptor_pb2.FieldDescriptorProto:
    return descriptor_pb2.FieldDescriptorProto(
        name=name,
        number=number,
        type=type,
        type_name=type_name,
    )


def make_naming(**kwargs) -> naming.Naming:
    kwargs.setdefault('name', 'Hatstand')
    kwargs.setdefault('namespace', ('Google', 'Cloud'))
    kwargs.setdefault('version', 'v1')
    kwargs.setdefault('product_name', 'Hatstand')
    kwargs.setdefault('product_url', 'https://cloud.google.com/hatstand/')
    return naming.Naming(**kwargs)
