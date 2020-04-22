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

import pytest

from google.api import client_pb2
from google.api_core import exceptions
from google.longrunning import operations_pb2
from google.protobuf import descriptor_pb2

from gapic.generator import options
from gapic.schema import api
from gapic.schema import imp
from gapic.schema import naming
from gapic.schema import wrappers

from test_utils.test_utils import (
    make_enum_pb2,
    make_field_pb2,
    make_file_pb2,
    make_message_pb2,
    make_naming,
)


def test_api_build():
    # Put together a couple of minimal protos.
    fd = (
        make_file_pb2(
            name='dep.proto',
            package='google.dep',
            messages=(make_message_pb2(name='ImportedMessage', fields=()),),
        ),
        make_file_pb2(
            name='common.proto',
            package='google.example.v1.common',
            messages=(make_message_pb2(name='Bar'),),
        ),
        make_file_pb2(
            name='foo.proto',
            package='google.example.v1',
            messages=(
                make_message_pb2(name='Foo', fields=()),
                make_message_pb2(name='GetFooRequest', fields=(
                    make_field_pb2(name='imported_message', number=1,
                                   type_name='.google.dep.ImportedMessage'),
                    make_field_pb2(name='primitive', number=2, type=1),
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
    assert len(api_schema.all_protos) == 3
    assert len(api_schema.protos) == 2
    assert 'google.dep.ImportedMessage' not in api_schema.messages
    assert 'google.example.v1.common.Bar' in api_schema.messages
    assert 'google.example.v1.Foo' in api_schema.messages
    assert 'google.example.v1.GetFooRequest' in api_schema.messages
    assert 'google.example.v1.GetFooResponse' in api_schema.messages
    assert 'google.example.v1.FooService' in api_schema.services
    assert len(api_schema.enums) == 0
    assert api_schema.protos['foo.proto'].python_modules == (
        imp.Import(package=('google', 'dep'), module='dep_pb2'),
    )

    assert api_schema.requires_package(('google', 'example', 'v1'))
    assert not api_schema.requires_package(('elgoog', 'example', 'v1'))

    # Establish that the subpackages work.
    assert 'common' in api_schema.subpackages
    sub = api_schema.subpackages['common']
    assert len(sub.protos) == 1
    assert 'google.example.v1.common.Bar' in sub.messages
    assert 'google.example.v1.Foo' not in sub.messages


def test_top_level_messages():
    message_pbs = (
        make_message_pb2(name='Mollusc', nested_type=(
            make_message_pb2(name='Squid'),
        )),
    )
    fds = (
        make_file_pb2(
            messages=message_pbs,
            package='google.example.v3',
        ),
    )
    api_schema = api.API.build(fds, package='google.example.v3')
    actual = [m.name for m in api_schema.top_level_messages.values()]
    expected = ['Mollusc']
    assert expected == actual


def test_top_level_enum():
    # Test that a nested enum works properly.
    message_pbs = (
        make_message_pb2(name='Coleoidea', enum_type=(
            make_enum_pb2(
                'Superorder',
                'Decapodiformes',
                'Octopodiformes',
                'Palaeoteuthomorpha',
            ),
        )),
    )
    enum_pbs = (
        make_enum_pb2(
            'Order',
            'Gastropoda',
            'Bivalvia',
            'Cephalopoda',
        ),
    )
    fds = (
        make_file_pb2(
            messages=message_pbs,
            enums=enum_pbs,
            package='google.example.v3',
        ),
    )
    api_schema = api.API.build(fds, package='google.example.v3')
    actual = [e.name for e in api_schema.top_level_enums.values()]
    expected = ['Order']
    assert expected == actual


def test_proto_build():
    fdp = descriptor_pb2.FileDescriptorProto(
        name='my_proto_file.proto',
        package='google.example.v1',
    )
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())
    assert isinstance(proto, api.Proto)


def test_proto_names():
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
                make_message_pb2(name='Bar', fields=(
                    make_field_pb2(name='imported_message', number=1,
                                   type_name='.google.dep.ImportedMessage'),
                    make_field_pb2(name='primitive', number=2, type=1),
                )),
                make_message_pb2(name='Baz', fields=(
                    make_field_pb2(name='foo', number=1,
                                   type_name='.google.example.v1.Foo'),
                )),
            ),
        ),
    )

    # Create an API with those protos.
    api_schema = api.API.build(fd, package='google.example.v1')
    proto = api_schema.protos['foo.proto']
    assert proto.names == {'Foo', 'Bar', 'Baz', 'foo', 'imported_message',
                           'primitive'}
    assert proto.disambiguate('enum') == 'enum'
    assert proto.disambiguate('foo') == '_foo'


def test_proto_keyword_fname():
    # Protos with filenames that happen to be python keywords
    # cannot be directly imported.
    # Check that the file names are unspecialized when building the API object.
    fd = (
        make_file_pb2(
            name='import.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='ImportRequest', fields=()),),
        ),
        make_file_pb2(
            name='import_.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='ImportUnderRequest', fields=()),),
        ),
        make_file_pb2(
            name='class_.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='ClassUnderRequest', fields=()),),
        ),
        make_file_pb2(
            name='class.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='ClassRequest', fields=()),),
        )
    )

    # We can't create new collisions, so check that renames cascade.
    api_schema = api.API.build(fd, package='google.keywords.v1')
    assert set(api_schema.protos.keys()) == {
        'import_.proto',
        'import__.proto',
        'class_.proto',
        'class__.proto',
    }


def test_proto_names_import_collision():
    # Put together a couple of minimal protos.
    fd = (
        make_file_pb2(
            name='a/b/c/spam.proto',
            package='a.b.c',
            messages=(make_message_pb2(name='ImportedMessage', fields=()),),
        ),
        make_file_pb2(
            name='x/y/z/spam.proto',
            package='x.y.z',
            messages=(make_message_pb2(name='OtherMessage', fields=()),),
        ),
        make_file_pb2(
            name='foo.proto',
            package='google.example.v1',
            messages=(
                make_message_pb2(name='Foo', fields=()),
                make_message_pb2(name='Bar', fields=(
                    make_field_pb2(name='imported_message', number=1,
                                   type_name='.a.b.c.ImportedMessage'),
                    make_field_pb2(name='other_message', number=2,
                                   type_name='.x.y.z.OtherMessage'),
                    make_field_pb2(name='primitive', number=3, type=1),
                )),
                make_message_pb2(name='Baz', fields=(
                    make_field_pb2(name='foo', number=1,
                                   type_name='.google.example.v1.Foo'),
                )),
            ),
        ),
    )

    # Create an API with those protos.
    api_schema = api.API.build(fd, package='google.example.v1')
    proto = api_schema.protos['foo.proto']
    assert proto.names == {'Foo', 'Bar', 'Baz', 'foo', 'imported_message',
                           'other_message', 'primitive', 'spam'}


def test_proto_names_import_collision_flattening():
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False, naming=make_naming())

    fd = (
        make_file_pb2(
            name='mollusc.proto',
            package='google.animalia.mollusca',
            messages=(
                make_message_pb2(name='Mollusc',),
                make_message_pb2(name='MolluscResponse',),
                make_message_pb2(name='MolluscMetadata',),
            ),
        ),
        make_file_pb2(
            name='squid.proto',
            package='google.animalia.mollusca',
            messages=(
                make_message_pb2(
                    name='IdentifySquidRequest',
                    fields=(
                        make_field_pb2(
                            name='mollusc',
                            number=1,
                            type_name='.google.animalia.mollusca.Mollusc'
                        ),
                    ),
                ),
                make_message_pb2(
                    name='IdentifySquidResponse',
                    fields=(),
                ),
            ),
            services=(
                descriptor_pb2.ServiceDescriptorProto(
                    name='SquidIdentificationService',
                    method=(
                        descriptor_pb2.MethodDescriptorProto(
                            name='IdentifyMollusc',
                            input_type='google.animalia.mollusca.IdentifySquidRequest',
                            output_type='google.longrunning.Operation',
                        ),
                    ),
                ),
            ),
        ),
    )

    method_options = fd[1].service[0].method[0].options
    # Notice that a signature field collides with the name of an imported module
    method_options.Extensions[client_pb2.method_signature].append('mollusc')
    method_options.Extensions[operations_pb2.operation_info].MergeFrom(
        operations_pb2.OperationInfo(
            response_type='google.animalia.mollusca.MolluscResponse',
            metadata_type='google.animalia.mollusca.MolluscMetadata',
        )
    )
    api_schema = api.API.build(
        fd,
        package='google.animalia.mollusca',
        prior_protos={
            'google/longrunning/operations.proto': lro_proto,
        }
    )

    actual_imports = {
        ref_type.ident.python_import
        for service in api_schema.services.values()
        for method in service.methods.values()
        for ref_type in method.ref_types
    }

    expected_imports = {
        imp.Import(
            package=('google', 'animalia', 'mollusca', 'types'),
            module='mollusc',
            alias='gam_mollusc',
        ),
        imp.Import(
            package=('google', 'animalia', 'mollusca', 'types'),
            module='squid',
        ),
        imp.Import(package=('google', 'api_core'), module='operation',),
    }

    assert expected_imports == actual_imports

    method = (
        api_schema
        .services['google.animalia.mollusca.SquidIdentificationService']
        .methods['IdentifyMollusc']
    )

    actual_response_import = method.lro.response_type.ident.python_import
    expected_response_import = imp.Import(
        package=('google', 'animalia', 'mollusca', 'types'),
        module='mollusc',
        alias='gam_mollusc',
    )
    assert actual_response_import == expected_response_import


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
        pb = api._ProtoBuilder(fdp,
                               file_to_generate=True,
                               naming=make_naming(),
                               )

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
    message_pb = make_message_pb2(
        name='Foo', fields=(make_field_pb2(name='bar', type=3, number=1),)
    )
    service_pb = descriptor_pb2.ServiceDescriptorProto()
    fdp = make_file_pb2(messages=(message_pb,), services=(service_pb,))

    # Actually make the proto object.
    proto = api.Proto.build(fdp, file_to_generate=False, naming=make_naming())

    # The proto object should have the message, but no service.
    assert len(proto.messages) == 1
    assert len(proto.services) == 0


def test_messages():
    L = descriptor_pb2.SourceCodeInfo.Location

    message_pb = make_message_pb2(
        name='Foo', fields=(make_field_pb2(name='bar', type=3, number=1),)
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
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())

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
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())

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
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())

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
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())

    # Set short variables for the names.
    foo = 'google.example.v3.Foo'
    bar = 'google.example.v3.Foo.Bar'

    # Get the message.
    assert len(proto.all_messages) == 2
    assert proto.all_messages[foo].name == 'Foo'
    assert proto.all_messages[bar].name == 'Bar'

    # Assert that the `messages` property only shows top-level messages.
    assert len(proto.messages) == 1
    assert proto.messages[foo] is proto.messages[foo]
    assert bar not in proto.messages


def test_out_of_order_enums():
    # Enums can be referenced as field types before they
    # are defined in the proto file.
    # This happens when they're a nested type within a message.
    messages = (
        make_message_pb2(
            name='Squid',
            fields=(
                make_field_pb2(
                    name='base_color',
                    type_name='google.mollusca.Chromatophore.Color',
                    number=1,
                ),
            ),
        ),
        make_message_pb2(
            name='Chromatophore',
            enum_type=(
                descriptor_pb2.EnumDescriptorProto(name='Color', value=()),
            ),
        )
    )
    fd = (
        make_file_pb2(
            name='squid.proto',
            package='google.mollusca',
            messages=messages,
            services=(
                descriptor_pb2.ServiceDescriptorProto(
                    name='SquidService',
                ),
            ),
        ),
    )
    api_schema = api.API.build(fd, package='google.mollusca')
    field_type = (
        api_schema
        .messages['google.mollusca.Squid']
        .fields['base_color']
        .type
    )
    enum_type = api_schema.enums['google.mollusca.Chromatophore.Color']
    assert field_type == enum_type


def test_undefined_type():
    fd = (
        make_file_pb2(
            name='mollusc.proto',
            package='google.mollusca',
            messages=(
                make_message_pb2(
                    name='Mollusc',
                    fields=(
                        make_field_pb2(
                            name='class',
                            type_name='google.mollusca.Class',
                            number=1,
                        ),
                    )
                ),
            ),
        ),
    )
    with pytest.raises(TypeError):
        api.API.build(fd, package='google.mollusca')


def test_python_modules_nested():
    fd = (
        make_file_pb2(
            name='dep.proto',
            package='google.dep',
            messages=(make_message_pb2(name='ImportedMessage', fields=()),),
        ),
        make_file_pb2(
            name='common.proto',
            package='google.example.v1.common',
            messages=(make_message_pb2(name='Bar'),),
        ),
        make_file_pb2(
            name='foo.proto',
            package='google.example.v1',
            messages=(
                make_message_pb2(
                    name='GetFooRequest',
                    fields=(
                        make_field_pb2(name='primitive', number=2, type=1),
                        make_field_pb2(
                            name='foo',
                            number=3,
                            type=1,
                            type_name='.google.example.v1.GetFooRequest.Foo',
                        ),
                    ),
                    nested_type=(
                        make_message_pb2(
                            name='Foo',
                            fields=(
                                make_field_pb2(
                                    name='imported_message',
                                    number=1,
                                    type_name='.google.dep.ImportedMessage'),
                            ),
                        ),
                    ),
                ),
                make_message_pb2(
                    name='GetFooResponse',
                    fields=(
                        make_field_pb2(
                            name='foo',
                            number=1,
                            type_name='.google.example.v1.GetFooRequest.Foo',
                        ),
                    ),
                ),
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

    api_schema = api.API.build(fd, package='google.example.v1')

    assert api_schema.protos['foo.proto'].python_modules == (
        imp.Import(package=('google', 'dep'), module='dep_pb2'),
    )


def test_services():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Make a silly helper method to not repeat some of the structure.
    def _n(method_name: str):
        return {
            'service': 'google.example.v2.FooService',
            'method': method_name,
        }

    # Set up retry information.
    opts = options.Options(retry={'methodConfig': [
        {'name': [_n('TimeoutableGetFoo')], 'timeout': '30s'},
        {'name': [_n('RetryableGetFoo')], 'retryPolicy': {
            'maxAttempts': 3,
            'initialBackoff': '%dn' % 1e6,
            'maxBackoff': '60s',
            'backoffMultiplier': 1.5,
            'retryableStatusCodes': ['UNAVAILABLE', 'ABORTED'],
        }},
    ]})

    # Set up messages for our RPC.
    request_message_pb = make_message_pb2(
        name='GetFooRequest', fields=(make_field_pb2(name='name', type=9, number=1),)
    )
    response_message_pb = make_message_pb2(name='GetFooResponse', fields=())

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='FooService',
        method=(
            descriptor_pb2.MethodDescriptorProto(
                name='GetFoo',
                input_type='google.example.v2.GetFooRequest',
                output_type='google.example.v2.GetFooResponse',
            ),
            descriptor_pb2.MethodDescriptorProto(
                name='TimeoutableGetFoo',
                input_type='google.example.v2.GetFooRequest',
                output_type='google.example.v2.GetFooResponse',
            ),
            descriptor_pb2.MethodDescriptorProto(
                name='RetryableGetFoo',
                input_type='google.example.v2.GetFooRequest',
                output_type='google.example.v2.GetFooResponse',
            ),
        ),
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
        name='test.proto',
        package='google.example.v2',
        messages=(request_message_pb, response_message_pb),
        services=(service_pb,),
        locations=locations,
    )

    # Make the proto object.
    proto = api.API.build(
        [fdp],
        'google.example.v2',
        opts=opts,
    ).protos['test.proto']

    # Establish that our data looks correct.
    assert len(proto.services) == 1
    assert len(proto.messages) == 2
    service = proto.services['google.example.v2.FooService']
    assert service.meta.doc == 'This is the FooService service.'
    assert len(service.methods) == 3
    method = service.methods['GetFoo']
    assert method.meta.doc == 'This is the GetFoo method.'
    assert isinstance(method.input, wrappers.MessageType)
    assert isinstance(method.output, wrappers.MessageType)
    assert method.input.name == 'GetFooRequest'
    assert method.input.meta.doc == 'This is the GetFooRequest message.'
    assert method.output.name == 'GetFooResponse'
    assert method.output.meta.doc == 'This is the GetFooResponse message.'
    assert not method.timeout
    assert not method.retry

    # Establish that the retry information on a timeout-able method also
    # looks correct.
    timeout_method = service.methods['TimeoutableGetFoo']
    assert timeout_method.timeout == pytest.approx(30.0)
    assert not timeout_method.retry

    # Establish that the retry information on the retryable method also
    # looks correct.
    retry_method = service.methods['RetryableGetFoo']
    assert retry_method.timeout is None
    assert retry_method.retry.max_attempts == 3
    assert retry_method.retry.initial_backoff == pytest.approx(0.001)
    assert retry_method.retry.backoff_multiplier == pytest.approx(1.5)
    assert retry_method.retry.max_backoff == pytest.approx(60.0)
    assert retry_method.retry.retryable_exceptions == {
        exceptions.ServiceUnavailable, exceptions.Aborted,
    }


def test_prior_protos():
    L = descriptor_pb2.SourceCodeInfo.Location

    # Set up a prior proto that mimics google/protobuf/empty.proto
    empty_proto = api.Proto.build(make_file_pb2(
        name='empty.proto', package='google.protobuf',
        messages=(make_message_pb2(name='Empty'),),
    ), file_to_generate=False, naming=make_naming())

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
    }, naming=make_naming())

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
    ), file_to_generate=False, naming=make_naming())

    # Set up a method with LRO annotations.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='AsyncDoThing',
        input_type='google.example.v3.AsyncDoThingRequest',
        output_type='google.longrunning.Operation',
    )
    method_pb2.options.Extensions[operations_pb2.operation_info].MergeFrom(
        operations_pb2.OperationInfo(
            response_type='google.example.v3.AsyncDoThingResponse',
            metadata_type='google.example.v3.AsyncDoThingMetadata',
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
    }, naming=make_naming())

    # Establish that our data looks correct.
    assert len(proto.services) == 1
    assert len(proto.messages) == 3
    assert len(lro_proto.messages) == 1


def test_lro_missing_annotation():
    # Set up a prior proto that mimics google/protobuf/empty.proto
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False, naming=make_naming())

    # Set up a method with an LRO but no annotation.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='AsyncDoThing',
        input_type='google.example.v3.AsyncDoThingRequest',
        output_type='google.longrunning.Operation',
    )

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='LongRunningService',
        method=(method_pb2,),
    )

    # Set up the messages, including the annotated ones.
    messages = (
        make_message_pb2(name='AsyncDoThingRequest', fields=()),
    )

    # Finally, set up the file that encompasses these.
    fdp = make_file_pb2(
        package='google.example.v3',
        messages=messages,
        services=(service_pb,),
    )

    # Make the proto object.
    with pytest.raises(TypeError):
        api.Proto.build(fdp, file_to_generate=True, prior_protos={
            'google/longrunning/operations.proto': lro_proto,
        }, naming=make_naming())


def test_cross_file_lro():
    # Protobuf annotations for longrunning operations use strings to name types.
    # As far as the protobuf compiler is concerned they don't reference the
    # _types_ at all, so the corresponding proto file that owns the types
    # does not need to be imported.
    # This creates a potential issue when building rich structures around
    # LRO returning methods. This test is intended to verify that the issue
    # is handled correctly.

    # Set up a prior proto that mimics google/protobuf/empty.proto
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False, naming=make_naming())

    # Set up a method with LRO annotations.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='AsyncDoThing',
        input_type='google.example.v3.AsyncDoThingRequest',
        output_type='google.longrunning.Operation',
    )
    method_pb2.options.Extensions[operations_pb2.operation_info].MergeFrom(
        operations_pb2.OperationInfo(
            response_type='google.example.v3.AsyncDoThingResponse',
            metadata_type='google.example.v3.AsyncDoThingMetadata',
        ),
    )

    # Set up the service with an RPC.
    service_file = make_file_pb2(
        name='service_file.proto',
        package='google.example.v3',
        messages=(
            make_message_pb2(name='AsyncDoThingRequest', fields=()),
        ),
        services=(
            descriptor_pb2.ServiceDescriptorProto(
                name='LongRunningService',
                method=(method_pb2,),
            ),
        )
    )

    # Set up the messages, including the annotated ones.
    # This file is distinct and is not explicitly imported
    # into the file that defines the service.
    messages_file = make_file_pb2(
        name='messages_file.proto',
        package='google.example.v3',
        messages=(
            make_message_pb2(name='AsyncDoThingResponse', fields=()),
            make_message_pb2(name='AsyncDoThingMetadata', fields=()),
        ),
    )

    api_schema = api.API.build(
        file_descriptors=(
            service_file,
            messages_file,
        ),
        package='google.example.v3',
        prior_protos={'google/longrunning/operations.proto': lro_proto, },
    )

    method = (
        api_schema.
        all_protos['service_file.proto'].
        services['google.example.v3.LongRunningService'].
        methods['AsyncDoThing']
    )

    assert method.lro
    assert method.lro.response_type.name == 'AsyncDoThingResponse'
    assert method.lro.metadata_type.name == 'AsyncDoThingMetadata'


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
    proto = api.Proto.build(fdp, file_to_generate=True, naming=make_naming())
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
