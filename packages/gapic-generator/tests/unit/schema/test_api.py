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

from unittest import mock

import pytest

from google.api import annotations_pb2  # type: ignore
from google.api import client_pb2
from google.api import resource_pb2
from google.api_core import exceptions
from google.cloud import extended_operations_pb2 as ex_ops_pb2
from google.gapic.metadata import gapic_metadata_pb2
from google.longrunning import operations_pb2
from google.protobuf import descriptor_pb2
from google.protobuf.json_format import MessageToJson
from google.cloud.location import locations_pb2
from google.iam.v1 import iam_policy_pb2  # type: ignore

from gapic.schema import api
from gapic.schema import imp
from gapic.schema import mixins
from gapic.schema import naming
from gapic.schema import wrappers
from gapic.utils import Options

from test_utils.test_utils import (
    make_enum_pb2,
    make_field_pb2,
    make_file_pb2,
    make_message_pb2,
    make_method,
    make_naming,
    make_oneof_pb2,
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


def test_proto_with_invalid_characters():
    # Protos with filenames that contain `.` in the basename
    # cannot be directly imported. Test that `.` is changed to `_`
    # See https://peps.python.org/pep-0008/#package-and-module-names

    test_cases = [
        {'name': 'k8s.min.proto', 'expected': 'k8s_min.proto'},
        {'name': 'k8s.min.test.proto', 'expected': 'k8s_min_test.proto'}
    ]

    for test_case in test_cases:
        fd = (
            make_file_pb2(
                name=test_case['name'],
                package='google.keywords.v1',
                messages=(make_message_pb2(name='ImportRequest', fields=()),),
            ),
        )
        api_schema = api.API.build(fd, package='google.keywords.v1')
        assert set(api_schema.protos.keys()) == {
            test_case['expected'],
        }


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
        ),
        make_file_pb2(
            name='metadata.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='MetadataRequest', fields=()),),
        ),
        make_file_pb2(
            name='retry.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='RetryRequest', fields=()),),
        ),
        make_file_pb2(
            name='timeout.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='TimeoutRequest', fields=()),),
        ),
        make_file_pb2(
            name='request.proto',
            package='google.keywords.v1',
            messages=(make_message_pb2(name='RequestRequest', fields=()),),
        ),
    )

    # We can't create new collisions, so check that renames cascade.
    api_schema = api.API.build(fd, package='google.keywords.v1')
    assert set(api_schema.protos.keys()) == {
        'import_.proto',
        'import__.proto',
        'class_.proto',
        'class__.proto',
        'metadata_.proto',
        'retry_.proto',
        'timeout_.proto',
        'request_.proto',
    }


def test_proto_oneof():
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
                make_message_pb2(
                    name='Bar',
                    fields=(
                        make_field_pb2(name='imported_message', number=1,
                                       type_name='.google.dep.ImportedMessage',
                                       oneof_index=0),
                        make_field_pb2(
                            name='primitive', number=2, type=1, oneof_index=0),
                    ),
                    oneof_decl=(
                        make_oneof_pb2(name="value_type"),
                    )
                )
            )
        )
    )

    # Create an API with those protos.
    api_schema = api.API.build(fd, package='google.example.v1')
    proto = api_schema.protos['foo.proto']
    assert proto.names == {'imported_message', 'Bar', 'primitive', 'Foo'}
    oneofs = proto.messages["google.example.v1.Bar"].oneofs
    assert len(oneofs) == 1
    assert "value_type" in oneofs.keys()


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
        imp.Import(package=('google', 'api_core'), module='operation_async',),
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
            name="dep.proto",
            package="google.dep",
            messages=(make_message_pb2(name="ImportedMessage", fields=()),),
        ),
        make_file_pb2(
            name="baa.proto",
            package="google.baa",
            messages=(make_message_pb2(name="ImportedMessageBaa", fields=()),),
        ),
        make_file_pb2(
            name="bab.v1.proto",
            package="google.bab.v1",
            messages=(make_message_pb2(name="ImportedMessageBab", fields=()),),
        ),
        make_file_pb2(
            name="common.proto",
            package="google.example.v1.common",
            messages=(make_message_pb2(name="Bar"),),
        ),
        make_file_pb2(
            name="foo.proto",
            package="google.example.v1",
            messages=(
                make_message_pb2(
                    name="GetFooRequest",
                    fields=(
                        make_field_pb2(name="primitive", number=2, type=1),
                        make_field_pb2(
                            name="foo",
                            number=3,
                            type=1,
                            type_name=".google.example.v1.GetFooRequest.Foo",
                        ),
                    ),
                    nested_type=(
                        make_message_pb2(
                            name="Foo",
                            fields=(
                                make_field_pb2(
                                    name="imported_message",
                                    number=1,
                                    type_name=".google.dep.ImportedMessage",
                                ),
                            ),
                        ),
                        make_message_pb2(
                            name="Baa",
                            fields=(
                                make_field_pb2(
                                    name="imported_message_baa",
                                    number=1,
                                    type_name=".google.baa.ImportedMessageBaa",
                                ),
                            ),
                        ),
                        make_message_pb2(
                            name="Bab",
                            fields=(
                                make_field_pb2(
                                    name="imported_message_bab",
                                    number=1,
                                    type_name=".google.bab.v1.ImportedMessageBab",
                                ),
                            ),
                        ),
                    ),
                ),
                make_message_pb2(
                    name="GetFooResponse",
                    fields=(
                        make_field_pb2(
                            name="foo",
                            number=1,
                            type_name=".google.example.v1.GetFooRequest.Foo",
                        ),
                    ),
                ),
            ),
            services=(
                descriptor_pb2.ServiceDescriptorProto(
                    name="FooService",
                    method=(
                        descriptor_pb2.MethodDescriptorProto(
                            name="GetFoo",
                            input_type="google.example.v1.GetFooRequest",
                            output_type="google.example.v1.GetFooResponse",
                        ),
                    ),
                ),
            ),
        ),
    )

    api_schema = api.API.build(fd, package="google.example.v1")

    assert api_schema.protos["foo.proto"].python_modules == (
        imp.Import(package=("google", "baa"), module="baa_pb2"),
        imp.Import(package=("google", "bab", "v1"), module="bab_v1_pb2"),
        imp.Import(package=("google", "dep"), module="dep_pb2"),
    )
    assert (
        api_schema.protos["foo.proto"]
        .all_messages["google.example.v1.GetFooRequest.Bab"]
        .fields["imported_message_bab"]
        .ident.sphinx
        == "google.bab.v1.bab_v1_pb2.ImportedMessageBab"
    )

    # Ensure that we can change the import statements to cater for a
    # dependency that uses proto-plus types.
    # For example,
    # `from google.bar import bar_pb2` becomes `from google.bar.types import bar``
    # `from google.baz.v2 import baz_pb2` becomes `from google.baz_v2.types improt baz_v2`
    api_schema = api.API.build(
        fd,
        package="google.example.v1",
        opts=Options(
            proto_plus_deps="+".join(
                (
                    "google.baa",
                    "google.bab.v1",
                )
            )
        ),
    )
    assert api_schema.protos["foo.proto"].python_modules == (
        imp.Import(package=("google", "baa", "types"), module="baa"),
        imp.Import(package=("google", "bab_v1", "types"), module="bab_v1"),
        imp.Import(package=("google", "dep"), module="dep_pb2"),
    )

    assert (
        api_schema.protos["foo.proto"]
        .all_messages["google.example.v1.GetFooRequest.Bab"]
        .fields["imported_message_bab"]
        .ident.sphinx
        == "google.bab_v1.types.ImportedMessageBab"
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
    opts = Options(retry={'methodConfig': [
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


def test_lro_operation_no_annotation():
    # A method that returns google.longrunning.Operation,
    # but has no operation_info option, is treated as not lro.

    # Set up a prior proto that mimics google/protobuf/empty.proto
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False, naming=make_naming())

    # Set up a method that returns an Operation, but has no annotation.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='GetOperation',
        input_type='google.example.v3.GetOperationRequest',
        output_type='google.longrunning.Operation',
    )

    # Set up the service with an RPC.
    service_pb = descriptor_pb2.ServiceDescriptorProto(
        name='OperationService',
        method=(method_pb2,),
    )

    # Set up the messages, including the annotated ones.
    messages = (
        make_message_pb2(name='GetOperationRequest', fields=()),
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

    service = proto.services['google.example.v3.OperationService']
    method = service.methods['GetOperation']
    assert method.lro is None


def test_lro_bad_annotation():
    # Set up a prior proto that mimics google/protobuf/empty.proto
    lro_proto = api.Proto.build(make_file_pb2(
        name='operations.proto', package='google.longrunning',
        messages=(make_message_pb2(name='Operation'),),
    ), file_to_generate=False, naming=make_naming())

    # Set up a method with an LRO and incomplete annotation.
    method_pb2 = descriptor_pb2.MethodDescriptorProto(
        name='AsyncDoThing',
        input_type='google.example.v3.AsyncDoThingRequest',
        output_type='google.longrunning.Operation',
    )
    method_pb2.options.Extensions[operations_pb2.operation_info].MergeFrom(
        operations_pb2.OperationInfo(
            response_type='google.example.v3.AsyncDoThingResponse',
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


def test_extended_lro():
    initiate_options = descriptor_pb2.MethodOptions()
    initiate_options.Extensions[ex_ops_pb2.operation_service] = "OpsService"

    polling_method_options = descriptor_pb2.MethodOptions()
    polling_method_options.Extensions[ex_ops_pb2.operation_polling_method] = True

    T = descriptor_pb2.FieldDescriptorProto.Type
    operation_fields = tuple(
        make_field_pb2(name=name, type=T.Value("TYPE_STRING"), number=i)
        for i, name in enumerate(("name", "status", "error_code", "error_message"), start=1)
    )
    for f in operation_fields:
        options = descriptor_pb2.FieldOptions()
        options.Extensions[ex_ops_pb2.operation_field] = f.number
        f.options.MergeFrom(options)

    api_schema = api.Proto.build(
        make_file_pb2(
            "extended_lro.proto",
            package="exlro",
            messages=(
                make_message_pb2(name="Operation", fields=operation_fields),
                make_message_pb2(name="InitialRequest"),
                make_message_pb2(name="GetOperationRequest"),
                ),
            services=(
                descriptor_pb2.ServiceDescriptorProto(
                    name="OpsService",
                    method=(
                        descriptor_pb2.MethodDescriptorProto(
                            name="Get",
                            input_type="exlro.GetOperationRequest",
                            output_type="exlro.Operation",
                            options=polling_method_options,
                            ),
                        ),
                    ),
                descriptor_pb2.ServiceDescriptorProto(
                    name="BasicService",
                    method=(
                        descriptor_pb2.MethodDescriptorProto(
                            name="Initiate",
                            input_type="exlro.InitialRequest",
                            output_type="exlro.Operation",
                            options=initiate_options,
                            ),
                        ),
                    ),
                ),
            ),
        file_to_generate=True,
        naming=make_naming(),
    )

    initiate = api_schema.services["exlro.BasicService"].methods["Initiate"]
    assert initiate.extended_lro
    assert initiate.extended_lro.request_type == api_schema.messages["exlro.GetOperationRequest"]
    assert initiate.extended_lro.operation_type == api_schema.messages["exlro.Operation"]


def test_extended_lro_no_such_service():
    initiate_options = descriptor_pb2.MethodOptions()
    initiate_options.Extensions[ex_ops_pb2.operation_service] = "Nonesuch"

    polling_method_options = descriptor_pb2.MethodOptions()
    polling_method_options.Extensions[ex_ops_pb2.operation_polling_method] = True

    T = descriptor_pb2.FieldDescriptorProto.Type
    operation_fields = tuple(
        make_field_pb2(name=name, type=T.Value("TYPE_STRING"), number=i)
        for i, name in enumerate(("name", "status", "error_code", "error_message"), start=1)
    )
    for f in operation_fields:
        options = descriptor_pb2.FieldOptions()
        options.Extensions[ex_ops_pb2.operation_field] = f.number
        f.options.MergeFrom(options)

    with pytest.raises(ValueError):
        api_schema = api.Proto.build(
            make_file_pb2(
                "extended_lro.proto",
                package="exlro",
                messages=(
                    make_message_pb2(
                        name="Operation",
                        fields=operation_fields,
                    ),
                    make_message_pb2(
                        name="InitialRequest"
                    ),
                    make_message_pb2(
                        name="GetOperationRequest"
                    ),
                ),
                services=(
                    descriptor_pb2.ServiceDescriptorProto(
                        name="OpsService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Get",
                                input_type="exlro.GetOperationRequest",
                                output_type="exlro.Operation",
                                options=polling_method_options,
                                ),
                            ),
                        ),
                    descriptor_pb2.ServiceDescriptorProto(
                        name="BasicService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Initiate",
                                input_type="exlro.InitialRequest",
                                output_type="exlro.Operation",
                                options=initiate_options,
                                ),
                            ),
                        ),
                    ),
                ),
            file_to_generate=True,
            naming=make_naming(),
        )


def test_extended_lro_no_polling_method():
    initiate_options = descriptor_pb2.MethodOptions()
    initiate_options.Extensions[ex_ops_pb2.operation_service] = "OpsService"

    T = descriptor_pb2.FieldDescriptorProto.Type
    operation_fields = tuple(
        make_field_pb2(name=name, type=T.Value("TYPE_STRING"), number=i)
        for i, name in enumerate(("name", "status", "error_code", "error_message"), start=1)
    )
    for f in operation_fields:
        options = descriptor_pb2.FieldOptions()
        options.Extensions[ex_ops_pb2.operation_field] = f.number
        f.options.MergeFrom(options)

    with pytest.raises(ValueError):
        api_schema = api.Proto.build(
            make_file_pb2(
                "extended_lro.proto",
                package="exlro",
                messages=(
                    make_message_pb2(
                        name="Operation",
                        fields=operation_fields,
                    ),
                    make_message_pb2(
                        name="InitialRequest",
                    ),
                    make_message_pb2(
                        name="GetOperationRequest",
                    ),
                ),
                services=(
                    descriptor_pb2.ServiceDescriptorProto(
                        name="OpsService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Get",
                                input_type="exlro.GetOperationRequest",
                                output_type="exlro.Operation",
                                ),
                            ),
                        ),
                    descriptor_pb2.ServiceDescriptorProto(
                        name="BasicService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Initiate",
                                input_type="exlro.InitialRequest",
                                output_type="exlro.Operation",
                                options=initiate_options,
                                ),
                            ),
                        ),
                    ),
                ),
            file_to_generate=True,
            naming=make_naming(),
        )


def test_extended_lro_different_output_types():
    initiate_options = descriptor_pb2.MethodOptions()
    initiate_options.Extensions[ex_ops_pb2.operation_service] = "OpsService"

    polling_method_options = descriptor_pb2.MethodOptions()
    polling_method_options.Extensions[ex_ops_pb2.operation_polling_method] = True

    T = descriptor_pb2.FieldDescriptorProto.Type
    operation_fields = tuple(
        make_field_pb2(name=name, type=T.Value("TYPE_STRING"), number=i)
        for i, name in enumerate(("name", "status", "error_code", "error_message"), start=1)
    )
    for f in operation_fields:
        options = descriptor_pb2.FieldOptions()
        options.Extensions[ex_ops_pb2.operation_field] = f.number
        f.options.MergeFrom(options)

    with pytest.raises(ValueError):
        api_schema = api.Proto.build(
            make_file_pb2(
                "extended_lro.proto",
                package="exlro",
                messages=(
                    make_message_pb2(
                        name="Operation",
                        fields=operation_fields,
                    ),
                    make_message_pb2(
                        name="InitialRequest",
                    ),
                    make_message_pb2(
                        name="GetOperationRequest",
                    ),
                    make_message_pb2(
                        name="GetOperationResponse",
                    ),
                ),
                services=(
                    descriptor_pb2.ServiceDescriptorProto(
                        name="OpsService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Get",
                                input_type="exlro.GetOperationRequest",
                                output_type="exlro.GetOperationResponse",
                                options=polling_method_options,
                                ),
                            ),
                        ),
                    descriptor_pb2.ServiceDescriptorProto(
                        name="BasicService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Initiate",
                                input_type="exlro.InitialRequest",
                                output_type="exlro.Operation",
                                options=initiate_options,
                                ),
                            ),
                        ),
                    ),
                ),
            file_to_generate=True,
            naming=make_naming(),
        )


def test_extended_lro_not_an_operation():
    initiate_options = descriptor_pb2.MethodOptions()
    initiate_options.Extensions[ex_ops_pb2.operation_service] = "OpsService"

    polling_method_options = descriptor_pb2.MethodOptions()
    polling_method_options.Extensions[ex_ops_pb2.operation_polling_method] = True

    with pytest.raises(ValueError):
        api_schema = api.Proto.build(
            make_file_pb2(
                "extended_lro.proto",
                package="exlro",
                messages=(
                    make_message_pb2(name="Operation"),
                    make_message_pb2(name="InitialRequest"),
                    make_message_pb2(name="GetOperationRequest"),
                    ),
                services=(
                    descriptor_pb2.ServiceDescriptorProto(
                        name="OpsService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Get",
                                input_type="exlro.GetOperationRequest",
                                output_type="exlro.Operation",
                                options=polling_method_options,
                                ),
                            ),
                        ),
                    descriptor_pb2.ServiceDescriptorProto(
                        name="BasicService",
                        method=(
                            descriptor_pb2.MethodDescriptorProto(
                                name="Initiate",
                                input_type="exlro.InitialRequest",
                                output_type="exlro.Operation",
                                options=initiate_options,
                                ),
                            ),
                        ),
                    ),
                ),
            file_to_generate=True,
            naming=make_naming(),
        )


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


def test_file_level_resources():
    fdp = make_file_pb2(
        name="nomenclature.proto",
        package="nomenclature.linneaen.v1",
        messages=(
            make_message_pb2(
                name="CreateSpeciesRequest",
                fields=(
                    make_field_pb2(name='species', number=1, type=9),
                ),
            ),
            make_message_pb2(
                name="CreateSpeciesResponse",
            ),
        ),
        services=(
            descriptor_pb2.ServiceDescriptorProto(
                name="SpeciesService",
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name="CreateSpecies",
                        input_type="nomenclature.linneaen.v1.CreateSpeciesRequest",
                        output_type="nomenclature.linneaen.v1.CreateSpeciesResponse",
                    ),
                ),
            ),
        ),
    )
    res_pb2 = fdp.options.Extensions[resource_pb2.resource_definition]
    definitions = [
        ("nomenclature.linnaen.com/Species",
         "families/{family}/genera/{genus}/species/{species}"),
        ("nomenclature.linnaen.com/Phylum",
         "kingdoms/{kingdom}/phyla/{phylum}"),
    ]
    for type_, pattern in definitions:
        resource_definition = res_pb2.add()
        resource_definition.type = type_
        resource_definition.pattern.append(pattern)

    species_field = fdp.message_type[0].field[0]
    resource_reference = species_field.options.Extensions[resource_pb2.resource_reference]
    resource_reference.type = "nomenclature.linnaen.com/Species"

    api_schema = api.API.build([fdp], package='nomenclature.linneaen.v1')
    actual = api_schema.protos['nomenclature.proto'].resource_messages
    expected = collections.OrderedDict((
        ("nomenclature.linnaen.com/Species",
         wrappers.CommonResource(
             type_name="nomenclature.linnaen.com/Species",
             pattern="families/{family}/genera/{genus}/species/{species}"
         ).message_type),
        ("nomenclature.linnaen.com/Phylum",
         wrappers.CommonResource(
             type_name="nomenclature.linnaen.com/Phylum",
             pattern="kingdoms/{kingdom}/phyla/{phylum}"
         ).message_type),
    ))

    assert actual == expected

    # The proto file _owns_ the file level resources, but the service needs to
    # see them too because the client class owns all the helper methods.
    service = api_schema.services["nomenclature.linneaen.v1.SpeciesService"]
    actual = service.visible_resources
    assert actual == expected

    # The service doesn't own any method that owns a message that references
    # Phylum, so the service doesn't count it among its resource messages.
    expected.pop("nomenclature.linnaen.com/Phylum")
    expected = frozenset(expected.values())
    actual = service.resource_messages

    assert actual == expected


def test_resources_referenced_but_not_typed(reference_attr="type"):
    fdp = make_file_pb2(
        name="nomenclature.proto",
        package="nomenclature.linneaen.v1",
        messages=(
            make_message_pb2(
                name="Species",
            ),
            make_message_pb2(
                name="CreateSpeciesRequest",
                fields=(
                    make_field_pb2(name='species', number=1, type=9),
                ),
            ),
            make_message_pb2(
                name="CreateSpeciesResponse",
            ),
        ),
        services=(
            descriptor_pb2.ServiceDescriptorProto(
                name="SpeciesService",
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name="CreateSpecies",
                        input_type="nomenclature.linneaen.v1.CreateSpeciesRequest",
                        output_type="nomenclature.linneaen.v1.CreateSpeciesResponse",
                    ),
                ),
            ),
        ),
    )

    # Set up the resource
    species_resource_opts = fdp.message_type[0].options.Extensions[resource_pb2.resource]
    species_resource_opts.type = "nomenclature.linnaen.com/Species"
    species_resource_opts.pattern.append(
        "families/{family}/genera/{genus}/species/{species}")

    # Set up the reference
    name_resource_opts = fdp.message_type[1].field[0].options.Extensions[resource_pb2.resource_reference]
    if reference_attr == "type":
        name_resource_opts.type = species_resource_opts.type
    else:
        name_resource_opts.child_type = species_resource_opts.type

    api_schema = api.API.build([fdp], package="nomenclature.linneaen.v1")
    expected = {api_schema.messages["nomenclature.linneaen.v1.Species"]}
    actual = api_schema.services["nomenclature.linneaen.v1.SpeciesService"].resource_messages

    assert actual == expected


def test_resources_referenced_but_not_typed_child_type():
    test_resources_referenced_but_not_typed("child_type")


def test_map_field_name_disambiguation():
    squid_file_pb = descriptor_pb2.FileDescriptorProto(
        name="mollusc.proto",
        package="animalia.mollusca.v2",
        message_type=(
            descriptor_pb2.DescriptorProto(
                name="Mollusc",
            ),
        ),
    )
    method_types_file_pb = descriptor_pb2.FileDescriptorProto(
        name="mollusc_service.proto",
        package="animalia.mollusca.v2",
        message_type=(
            descriptor_pb2.DescriptorProto(
                name="CreateMolluscRequest",
                field=(
                    descriptor_pb2.FieldDescriptorProto(
                        name="mollusc",
                        type="TYPE_MESSAGE",
                        type_name=".animalia.mollusca.v2.Mollusc",
                        number=1,
                    ),
                    descriptor_pb2.FieldDescriptorProto(
                        name="molluscs_map",
                        type="TYPE_MESSAGE",
                        number=2,
                        type_name=".animalia.mollusca.v2.CreateMolluscRequest.MolluscsMapEntry",
                        label="LABEL_REPEATED",
                    ),
                ),
                nested_type=(
                    descriptor_pb2.DescriptorProto(
                        name="MolluscsMapEntry",
                        field=(
                            descriptor_pb2.FieldDescriptorProto(
                                name="key",
                                type="TYPE_STRING",
                                number=1,
                            ),
                            descriptor_pb2.FieldDescriptorProto(
                                name="value",
                                type="TYPE_MESSAGE",
                                number=2,
                                # We use the same type for the map value as for
                                # the singleton above to better highlight the
                                # problem raised in
                                # https://github.com/googleapis/gapic-generator-python/issues/618.
                                # The module _is_ disambiguated for singleton
                                # fields but NOT for map fields.
                                type_name=".animalia.mollusca.v2.Mollusc"
                            ),
                        ),
                        options=descriptor_pb2.MessageOptions(map_entry=True),
                    ),
                ),
            ),
        ),
    )
    my_api = api.API.build(
        file_descriptors=[squid_file_pb, method_types_file_pb],
    )
    create = my_api.messages['animalia.mollusca.v2.CreateMolluscRequest']
    mollusc = create.fields['mollusc']
    molluscs_map = create.fields['molluscs_map']
    mollusc_ident = str(mollusc.type.ident)
    mollusc_map_ident = str(molluscs_map.message.fields['value'].type.ident)

    # The same module used in the same place should have the same import alias.
    # Because there's a "mollusc" name used, the import should be disambiguated.
    assert mollusc_ident == mollusc_map_ident == "am_mollusc.Mollusc"


def test_gapic_metadata():
    api_schema = api.API.build(
        file_descriptors=[
            descriptor_pb2.FileDescriptorProto(
                name="cephalopod.proto",
                package="animalia.mollusca.v1",
                message_type=[
                    descriptor_pb2.DescriptorProto(
                        name="MolluscRequest",
                    ),
                    descriptor_pb2.DescriptorProto(
                        name="Mollusc",
                    ),
                ],
                service=[
                    descriptor_pb2.ServiceDescriptorProto(
                        name="Squid",
                        method=[
                            descriptor_pb2.MethodDescriptorProto(
                                name="Ramshorn",
                                input_type="animalia.mollusca.v1.MolluscRequest",
                                output_type="animalia.mollusca.v1.Mollusc",
                            ),
                            descriptor_pb2.MethodDescriptorProto(
                                name="Humboldt",
                                input_type="animalia.mollusca.v1.MolluscRequest",
                                output_type="animalia.mollusca.v1.Mollusc",
                            ),
                            descriptor_pb2.MethodDescriptorProto(
                                name="Giant",
                                input_type="animalia.mollusca.v1.MolluscRequest",
                                output_type="animalia.mollusca.v1.Mollusc",
                            ),
                        ],
                    ),
                    descriptor_pb2.ServiceDescriptorProto(
                        name="Octopus",
                        method=[
                            descriptor_pb2.MethodDescriptorProto(
                                name="GiantPacific",
                                input_type="animalia.mollusca.v1.MolluscRequest",
                                output_type="animalia.mollusca.v1.Mollusc",
                            ),
                            descriptor_pb2.MethodDescriptorProto(
                                name="BlueSpot",
                                input_type="animalia.mollusca.v1.MolluscRequest",
                                output_type="animalia.mollusca.v1.Mollusc",
                            ),
                        ]
                    ),
                ],
            )
        ]
    )

    opts = Options.build("transport=grpc")
    expected = gapic_metadata_pb2.GapicMetadata(
        schema="1.0",
        comment="This file maps proto services/RPCs to the corresponding library clients/methods",
        language="python",
        proto_package="animalia.mollusca.v1",
        library_package="animalia.mollusca_v1",
        services={
            "Octopus": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "grpc": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    ),
                    "grpc-async": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusAsyncClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    ),
                }
            ),
            "Squid": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "grpc": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),
                    "grpc-async": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidAsyncClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),
                }
            ),
        }
    )
    actual = api_schema.gapic_metadata(opts)
    assert expected == actual
    expected = MessageToJson(expected, sort_keys=True)
    actual = api_schema.gapic_metadata_json(opts)
    assert expected == actual

    opts = Options.build("transport=rest")
    expected = gapic_metadata_pb2.GapicMetadata(
        schema="1.0",
        comment="This file maps proto services/RPCs to the corresponding library clients/methods",
        language="python",
        proto_package="animalia.mollusca.v1",
        library_package="animalia.mollusca_v1",
        services={
            "Octopus": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "rest": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    )
                }
            ),
            "Squid": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "rest": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),

                }
            ),
        }
    )
    actual = api_schema.gapic_metadata(opts)
    assert expected == actual
    expected = MessageToJson(expected, sort_keys=True)
    actual = api_schema.gapic_metadata_json(opts)
    assert expected == actual

    opts = Options.build("transport=rest+grpc")
    expected = gapic_metadata_pb2.GapicMetadata(
        schema="1.0",
        comment="This file maps proto services/RPCs to the corresponding library clients/methods",
        language="python",
        proto_package="animalia.mollusca.v1",
        library_package="animalia.mollusca_v1",
        services={
            "Octopus": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "grpc": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    ),
                    "grpc-async": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusAsyncClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    ),
                    "rest": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="OctopusClient",
                        rpcs={
                            "BlueSpot": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["blue_spot"]),
                            "GiantPacific": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant_pacific"]),
                        },
                    )
                }
            ),
            "Squid": gapic_metadata_pb2.GapicMetadata.ServiceForTransport(
                clients={
                    "grpc": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),
                    "grpc-async": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidAsyncClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),
                    "rest": gapic_metadata_pb2.GapicMetadata.ServiceAsClient(
                        library_client="SquidClient",
                        rpcs={
                            "Giant": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["giant"]),
                            "Humboldt": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["humboldt"]),
                            "Ramshorn": gapic_metadata_pb2.GapicMetadata.MethodList(methods=["ramshorn"]),
                        },
                    ),

                }
            ),
        }
    )

    actual = api_schema.gapic_metadata(opts)
    assert expected == actual
    expected = MessageToJson(expected, sort_keys=True)
    actual = api_schema.gapic_metadata_json(opts)
    assert expected == actual


def test_http_options(fs):
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),),
        ),)

    opts = Options(service_yaml_config={
        'http': {
            'rules': [
                {
                    'selector': 'Cancel',
                    'post': '/v3/{name=projects/*/locations/*/operations/*}:cancel',
                    'body': '*'
                },
                {
                    'selector': 'Get',
                    'get': '/v3/{name=projects/*/locations/*/operations/*}',
                    'additional_bindings': [{'get': '/v3/{name=/locations/*/operations/*}'}],
                }, ]
        }
    })

    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    http_options = api_schema.http_options
    assert http_options == {
        'Cancel': [wrappers.HttpRule(method='post', uri='/v3/{name=projects/*/locations/*/operations/*}:cancel', body='*')],
        'Get': [
            wrappers.HttpRule(
                method='get', uri='/v3/{name=projects/*/locations/*/operations/*}', body=None),
            wrappers.HttpRule(method='get', uri='/v3/{name=/locations/*/operations/*}', body=None)]
    }


def generate_basic_extended_operations_setup():
    T = descriptor_pb2.FieldDescriptorProto.Type

    operation = make_message_pb2(
        name="Operation",
        fields=(
            make_field_pb2(name=name, type=T.Value("TYPE_STRING"), number=i)
            for i, name in enumerate(("name", "status", "error_code", "error_message"), start=1)
        ),
    )

    for f in operation.field:
        options = descriptor_pb2.FieldOptions()
        # Note: The field numbers were carefully chosen to be the corresponding enum values.
        options.Extensions[ex_ops_pb2.operation_field] = f.number
        f.options.MergeFrom(options)

    options = descriptor_pb2.MethodOptions()
    options.Extensions[ex_ops_pb2.operation_polling_method] = True

    polling_method = descriptor_pb2.MethodDescriptorProto(
        name="Get",
        input_type="google.extended_operations.v1.stuff.GetOperation",
        output_type="google.extended_operations.v1.stuff.Operation",
        options=options,
    )

    delete_input_message = make_message_pb2(name="Input")
    delete_output_message = make_message_pb2(name="Output")
    ops_service = descriptor_pb2.ServiceDescriptorProto(
        name="CustomOperations",
        method=[
            polling_method,
            descriptor_pb2.MethodDescriptorProto(
                name="Delete",
                input_type="google.extended_operations.v1.stuff.Input",
                output_type="google.extended_operations.v1.stuff.Output",
            ),
        ],
    )

    request = make_message_pb2(
        name="GetOperation",
        fields=[
            make_field_pb2(name="name", type=T.Value("TYPE_STRING"), number=1)
        ],
    )

    initial_opts = descriptor_pb2.MethodOptions()
    initial_opts.Extensions[ex_ops_pb2.operation_service] = ops_service.name
    initial_input_message = make_message_pb2(name="Initial")
    initial_method = descriptor_pb2.MethodDescriptorProto(
        name="CreateTask",
        input_type="google.extended_operations.v1.stuff.GetOperation",
        output_type="google.extended_operations.v1.stuff.Operation",
        options=initial_opts,
    )

    regular_service = descriptor_pb2.ServiceDescriptorProto(
        name="RegularService",
        method=[
            initial_method,
        ],
    )

    file_protos = [
        make_file_pb2(
            name="extended_operations.proto",
            package="google.extended_operations.v1.stuff",
            messages=[
                operation,
                request,
                delete_output_message,
                delete_input_message,
                initial_input_message,
            ],
            services=[
                ops_service,
                regular_service,
            ],
        ),
    ]

    return file_protos


def test_extended_operations_lro_operation_service():
    file_protos = generate_basic_extended_operations_setup()
    api_schema = api.API.build(file_protos)
    regular_service = api_schema.services["google.extended_operations.v1.stuff.RegularService"]
    initial_method = regular_service.methods["CreateTask"]

    operation_service = api_schema.services['google.extended_operations.v1.stuff.CustomOperations']
    expected = operation_service
    actual = api_schema.get_custom_operation_service(initial_method)

    assert expected is actual

    assert actual.operation_polling_method is actual.methods["Get"]

    expected = {operation_service}
    actual = api_schema.get_extended_operations_services(regular_service)
    assert expected == actual


def test_extended_operations_lro_operation_service_no_annotation():
    file_protos = generate_basic_extended_operations_setup()
    api_schema = api.API.build(file_protos)
    initial_method = api_schema.services["google.extended_operations.v1.stuff.RegularService"].methods["CreateTask"]

    # It's easier to manipulate data structures after building the API.
    del initial_method.options.Extensions[ex_ops_pb2.operation_service]

    with pytest.raises(ValueError):
        api_schema.get_custom_operation_service(initial_method)


def test_extended_operations_lro_operation_service_no_such_service():
    file_protos = generate_basic_extended_operations_setup()

    api_schema = api.API.build(file_protos)
    initial_method = api_schema.services["google.extended_operations.v1.stuff.RegularService"].methods["CreateTask"]
    initial_method.options.Extensions[ex_ops_pb2.operation_service] = "UnrealService"

    with pytest.raises(ValueError):
        api_schema.get_custom_operation_service(initial_method)


def test_extended_operations_lro_operation_service_not_an_lro():
    file_protos = generate_basic_extended_operations_setup()

    api_schema = api.API.build(file_protos)
    initial_method = api_schema.services["google.extended_operations.v1.stuff.RegularService"].methods["CreateTask"]
    # Hack to pretend that the initial_method is not an LRO
    super(type(initial_method), initial_method).__setattr__(
        "output", initial_method.input)

    with pytest.raises(ValueError):
        api_schema.get_custom_operation_service(initial_method)


def test_extended_operations_lro_operation_service_no_polling_method():
    file_protos = generate_basic_extended_operations_setup()

    api_schema = api.API.build(file_protos)
    initial_method = api_schema.services["google.extended_operations.v1.stuff.RegularService"].methods["CreateTask"]

    operation_service = api_schema.services["google.extended_operations.v1.stuff.CustomOperations"]
    del operation_service.methods["Get"].options.Extensions[ex_ops_pb2.operation_polling_method]

    with pytest.raises(ValueError):
        api_schema.get_custom_operation_service(initial_method)


def methods_from_service(service_pb, name: str):
    service = service_pb.DESCRIPTOR.services_by_name[name]
    res = {}
    for m in service.methods:
        x = descriptor_pb2.MethodDescriptorProto()
        m.CopyToProto(x)
        res[x.name] = x
    return res


def test_mixin_api_methods_locations():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),),
        ),)
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.cloud.location.Locations'
            }
        ],
        'http': {
            'rules': [
                {
                    'selector': 'google.cloud.location.Locations.ListLocations',
                    'get': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
                {
                    'selector': 'google.cloud.location.Locations.GetLocation',
                    'get': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
                {
                    'selector': 'google.example.v1.Example',
                }]
        }
    })
    ms = methods_from_service(locations_pb2, 'Locations')
    assert len(ms) == 2
    m1 = ms['ListLocations']
    m1.options.ClearExtension(annotations_pb2.http)
    m1.options.Extensions[annotations_pb2.http].selector = 'google.cloud.location.Locations.ListLocations'
    m1.options.Extensions[annotations_pb2.http].get = '/v1/{name=examples/*}/*'
    m1.options.Extensions[annotations_pb2.http].body = '*'
    m2 = ms['GetLocation']
    m2.options.ClearExtension(annotations_pb2.http)
    m2.options.Extensions[annotations_pb2.http].selector = 'google.cloud.location.Locations.GetLocation'
    m2.options.Extensions[annotations_pb2.http].get = '/v1/{name=examples/*}/*'
    m2.options.Extensions[annotations_pb2.http].body = '*'
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    assert api_schema.mixin_api_methods == {
        'ListLocations': m1, 'GetLocation': m2}


def test_mixin_api_methods_iam():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),
            make_message_pb2(name='ExampleResponse', fields=())),
            services=(descriptor_pb2.ServiceDescriptorProto(
                name='FooService',
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name='FooMethod',
                        # Input and output types don't matter.
                        input_type='google.example.v1.ExampleRequest',
                        output_type='google.example.v1.ExampleResponse',
                    ),
                ),
            ),),
        ),)
    r1 = {
        'selector': 'google.iam.v1.IAMPolicy.SetIamPolicy',
        'post': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    r2 = {
        'selector': 'google.iam.v1.IAMPolicy.GetIamPolicy',
        'get': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    r3 = {
        'selector': 'google.iam.v1.IAMPolicy.TestIamPermissions',
        'post': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.iam.v1.IAMPolicy'
            }
        ],
        'http': {
            'rules': [r1, r2, r3]
        }
    })
    ms = methods_from_service(iam_policy_pb2, 'IAMPolicy')
    assert len(ms) == 3
    m1 = ms['SetIamPolicy']
    m1.options.ClearExtension(annotations_pb2.http)
    m1.options.Extensions[annotations_pb2.http].selector = r1['selector']
    m1.options.Extensions[annotations_pb2.http].post = r1['post']
    m1.options.Extensions[annotations_pb2.http].body = r1['body']
    m2 = ms['GetIamPolicy']
    m2.options.ClearExtension(annotations_pb2.http)
    m2.options.Extensions[annotations_pb2.http].selector = r2['selector']
    m2.options.Extensions[annotations_pb2.http].get = r2['get']
    m2.options.Extensions[annotations_pb2.http].body = r2['body']
    m3 = ms['TestIamPermissions']
    m3.options.ClearExtension(annotations_pb2.http)
    m3.options.Extensions[annotations_pb2.http].selector = r3['selector']
    m3.options.Extensions[annotations_pb2.http].post = r3['post']
    m3.options.Extensions[annotations_pb2.http].body = r3['body']
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    assert api_schema.mixin_api_methods == {
        'SetIamPolicy': m1, 'GetIamPolicy': m2, 'TestIamPermissions': m3}
    assert not api_schema.has_operations_mixin


def test_mixin_api_methods_iam_overrides():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),
            make_message_pb2(name='ExampleResponse', fields=()),
                      ),
            services=(descriptor_pb2.ServiceDescriptorProto(
                name='FooService',
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name='TestIamPermissions',
                        # Input and output types don't matter.
                        input_type='google.example.v1.ExampleRequest',
                        output_type='google.example.v1.ExampleResponse',
                    ),
                ),
            ),),
        ),
    )
    r1 = {
        'selector': 'google.iam.v1.IAMPolicy.SetIamPolicy',
        'post': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    r2 = {
        'selector': 'google.iam.v1.IAMPolicy.GetIamPolicy',
        'get': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    r3 = {
        'selector': 'google.iam.v1.IAMPolicy.TestIamPermissions',
        'post': '/v1/{resource=examples/*}/*',
        'body': '*'
    }
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.iam.v1.IAMPolicy'
            }
        ],
        'http': {
            'rules': [r1, r2, r3]
        }
    })
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    assert api_schema.mixin_api_methods == {}


def create_service_config_with_all_mixins(http_opt_uri='/v1/{name=examples/*}/*'):
    service_yaml_config = {
        'apis': [
            {
                'name': 'google.cloud.location.Locations',
            },
            {
                'name': 'google.longrunning.Operations',
            },
            {
                'name': 'google.iam.v1.IAMPolicy',
            },
        ],
        'http': {
            'rules': [
                # Locations
                {
                    'selector': 'google.cloud.location.Locations.ListLocations',
                    'get': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.cloud.location.Locations.GetLocation',
                    'get': http_opt_uri,
                    'body': '*'
                },
                # LRO
                {
                    'selector': 'google.longrunning.Operations.CancelOperation',
                    'post': http_opt_uri,
                    'body': '*',
                },
                {
                    'selector': 'google.longrunning.Operations.DeleteOperation',
                    'get': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.WaitOperation',
                    'post': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.GetOperation',
                    'post': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.ListOperations',
                    'post': http_opt_uri,
                    'body': '*'
                },
                # IAM
                {
                    'selector': 'google.iam.v1.IAMPolicy.SetIamPolicy',
                    'post': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.iam.v1.IAMPolicy.GetIamPolicy',
                    'get': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.iam.v1.IAMPolicy.TestIamPermissions',
                    'post': http_opt_uri,
                    'body': '*'
                },
                {
                    'selector': 'google.example.v1.Example',
                }
            ]
        }
    }
    return service_yaml_config


def test_mixin_api_signatures():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),),
        ),)
    opts = Options(service_yaml_config=create_service_config_with_all_mixins())
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    res = api_schema.mixin_api_signatures
    assert res == mixins.MIXINS_MAP


def test_mixin_http_options():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),),
            ),)
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.cloud.location.Locations',
            },
            {
                'name': 'google.longrunning.Operations',
            },
            {
                'name': 'google.iam.v1.IAMPolicy',
            },
        ],
        'http': {
            'rules': [
                # LRO
                {
                    'selector': 'google.longrunning.Operations.CancelOperation',
                    'post': '/v1/{name=examples/*}/*',
                    'body': '*',
                },
                {
                    'selector': 'google.longrunning.Operations.DeleteOperation',
                    'get': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.WaitOperation',
                    'post': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.GetOperation',
                    'post': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
                {
                    'selector': 'google.longrunning.Operations.ListOperations',
                    'post': '/v1/{name=examples/*}/*',
                    'body': '*'
                },
            ]
        }
    })
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    res = api_schema.mixin_http_options
    assert res == {
        'ListOperations': [wrappers.MixinHttpRule('post', '/v1/{name=examples/*}/*', '*')],
        'GetOperation': [wrappers.MixinHttpRule('post', '/v1/{name=examples/*}/*', '*')],
        'DeleteOperation': [wrappers.MixinHttpRule('get', '/v1/{name=examples/*}/*', '*')],
        'CancelOperation': [wrappers.MixinHttpRule('post', '/v1/{name=examples/*}/*', '*')],
        'WaitOperation': [wrappers.MixinHttpRule('post', '/v1/{name=examples/*}/*', '*')],
    }


def test_mixin_api_methods_lro():
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),
            make_message_pb2(name='ExampleResponse', fields=()),
                      ),
            services=(descriptor_pb2.ServiceDescriptorProto(
                name='FooService',
                method=(
                    descriptor_pb2.MethodDescriptorProto(
                        name='FooMethod',
                        # Input and output types don't matter.
                        input_type='google.example.v1.ExampleRequest',
                        output_type='google.example.v1.ExampleResponse',
                    ),
                ),
            ),),
        ),
    )
    r1 = {
        'selector': 'google.longrunning.Operations.CancelOperation',
        'post': '/v1/{name=examples/*}/*',
        'body': '*'
    }
    r2 = {
        'selector': 'google.longrunning.Operations.DeleteOperation',
        'get': '/v1/{name=examples/*}/*',
        'body': '*'
    }
    r3 = {
        'selector': 'google.longrunning.Operations.WaitOperation',
        'post': '/v1/{name=examples/*}/*',
        'body': '*'
    }
    r4 = {
        'selector': 'google.longrunning.Operations.GetOperation',
        'post': '/v1/{name=examples/*}/*',
        'body': '*'
    }
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.longrunning.Operations'
            }
        ],
        'http': {
            'rules': [r1, r2, r3, r4]
        }
    })

    ms = methods_from_service(operations_pb2, 'Operations')
    assert len(ms) == 5
    m1 = ms['CancelOperation']
    m1.options.ClearExtension(annotations_pb2.http)
    m1.options.Extensions[annotations_pb2.http].selector = r1['selector']
    m1.options.Extensions[annotations_pb2.http].post = r1['post']
    m1.options.Extensions[annotations_pb2.http].body = r1['body']
    m2 = ms['DeleteOperation']
    m2.options.ClearExtension(annotations_pb2.http)
    m2.options.Extensions[annotations_pb2.http].selector = r2['selector']
    m2.options.Extensions[annotations_pb2.http].get = r2['get']
    m2.options.Extensions[annotations_pb2.http].body = r2['body']
    m3 = ms['WaitOperation']
    m3.options.ClearExtension(annotations_pb2.http)
    m3.options.Extensions[annotations_pb2.http].selector = r3['selector']
    m3.options.Extensions[annotations_pb2.http].post = r3['post']
    m3.options.Extensions[annotations_pb2.http].body = r3['body']
    m4 = ms['GetOperation']
    m4.options.ClearExtension(annotations_pb2.http)
    m4.options.Extensions[annotations_pb2.http].selector = r4['selector']
    m4.options.Extensions[annotations_pb2.http].post = r4['post']
    m4.options.Extensions[annotations_pb2.http].body = r4['body']

    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    assert api_schema.mixin_api_methods == {
        'CancelOperation': m1, 'DeleteOperation': m2, 'WaitOperation': m3,
        'GetOperation': m4}


def test_has_iam_mixin():
    # Check that has_iam_mixin() property of API returns True when the
    # service YAML contains `google.iam.v1.IAMPolicy`.
    fd = (
        make_file_pb2(
            name='example.proto',
            package='google.example.v1',
            messages=(make_message_pb2(name='ExampleRequest', fields=()),),
        ),)
    opts = Options(service_yaml_config={
        'apis': [
            {
                'name': 'google.iam.v1.IAMPolicy'
            }
        ],
    })
    api_schema = api.API.build(fd, 'google.example.v1', opts=opts)
    assert api_schema.has_iam_mixin
