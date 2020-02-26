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
import typing

from google.api import annotations_pb2
from google.api import client_pb2
from google.api import http_pb2
from google.api import resource_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import imp
from gapic.schema import metadata
from gapic.schema import wrappers


def test_service_properties():
    service = make_service(name='ThingDoer')
    assert service.name == 'ThingDoer'
    assert service.client_name == 'ThingDoerClient'
    assert service.transport_name == 'ThingDoerTransport'
    assert service.grpc_transport_name == 'ThingDoerGrpcTransport'


def test_service_host():
    service = make_service(host='thingdoer.googleapis.com')
    assert service.host == 'thingdoer.googleapis.com'


def test_service_no_host():
    service = make_service()
    assert not service.host


def test_service_scopes():
    service = make_service(scopes=('https://foo/user/', 'https://foo/admin/'))
    assert 'https://foo/user/' in service.oauth_scopes
    assert 'https://foo/admin/' in service.oauth_scopes


def test_service_names():
    service = make_service(name='ThingDoer', methods=(
        get_method('DoThing', 'foo.bar.ThingRequest', 'foo.baz.ThingResponse'),
        get_method('Jump', 'foo.bacon.JumpRequest', 'foo.bacon.JumpResponse'),
        get_method('Yawn', 'a.b.v1.c.YawnRequest', 'x.y.v1.z.YawnResponse'),
    ))
    expected_names = {'ThingDoer', 'ThingDoerClient',
                      'do_thing', 'jump', 'yawn'}
    assert service.names == expected_names


def test_service_name_colliding_modules():
    service = make_service(name='ThingDoer', methods=(
        get_method('DoThing', 'foo.bar.ThingRequest', 'foo.bar.ThingResponse'),
        get_method('Jump', 'bacon.bar.JumpRequest', 'bacon.bar.JumpResponse'),
        get_method('Yawn', 'a.b.v1.c.YawnRequest', 'a.b.v1.c.YawnResponse'),
    ))
    expected_names = {'ThingDoer', 'ThingDoerClient',
                      'do_thing', 'jump', 'yawn', 'bar'}
    assert service.names == expected_names


def test_service_no_scopes():
    service = make_service()
    assert len(service.oauth_scopes) == 0


def test_service_python_modules():
    service = make_service(methods=(
        get_method('DoThing', 'foo.bar.ThingRequest', 'foo.baz.ThingResponse'),
        get_method('Jump', 'foo.bacon.JumpRequest', 'foo.bacon.JumpResponse'),
        get_method('Yawn', 'a.b.v1.c.YawnRequest', 'x.y.v1.z.YawnResponse'),
    ))
    imports = {
        i.ident.python_import
        for m in service.methods.values()
        for i in m.ref_types_legacy
    }
    assert imports == {
        imp.Import(package=('a', 'b', 'v1'), module='c'),
        imp.Import(package=('foo',), module='bacon'),
        imp.Import(package=('foo',), module='bar'),
        imp.Import(package=('foo',), module='baz'),
        imp.Import(package=('x', 'y', 'v1'), module='z'),
    }


def test_service_python_modules_lro():
    service = make_service_with_method_options()
    method = service.methods['DoBigThing']
    imports = {i.ident.python_import for i in method.ref_types}
    assert imports == {
        imp.Import(package=('foo',), module='bar'),
        imp.Import(package=('foo',), module='baz'),
        imp.Import(package=('foo',), module='qux'),
        imp.Import(package=('google', 'api_core'), module='operation'),
    }


def test_service_python_modules_signature():
    service = make_service_with_method_options(
        in_fields=(
            # type=5 is int, so nothing is added.
            descriptor_pb2.FieldDescriptorProto(name='secs', type=5),
            descriptor_pb2.FieldDescriptorProto(
                name='d',
                type=14,  # enum
                type_name='a.b.c.v2.D',
            ),
        ),
        method_signature='secs,d',
    )

    # Ensure that the service will have the expected imports.
    method = service.methods['DoBigThing']
    imports = {i.ident.python_import for i in method.ref_types}
    assert imports == {
        imp.Import(package=('a', 'b', 'c'), module='v2'),
        imp.Import(package=('foo',), module='bar'),
        imp.Import(package=('foo',), module='baz'),
        imp.Import(package=('foo',), module='qux'),
        imp.Import(package=('google', 'api_core'), module='operation'),
    }


def test_service_no_lro():
    service = make_service()
    assert service.has_lro is False


def test_service_has_lro():
    service = make_service_with_method_options()
    assert service.has_lro


def test_module_name():
    service = make_service(name='MyService')
    assert service.module_name == 'my_service'


def test_resource_messages():
    # Resources
    squid_options = descriptor_pb2.MessageOptions()
    squid_options.Extensions[resource_pb2.resource].pattern.append(
        "squid/{squid}")
    squid_message = make_message("Squid", options=squid_options)
    clam_options = descriptor_pb2.MessageOptions()
    clam_options.Extensions[resource_pb2.resource].pattern.append(
        "clam/{clam}")
    clam_message = make_message("Clam", options=clam_options)
    whelk_options = descriptor_pb2.MessageOptions()
    whelk_options.Extensions[resource_pb2.resource].pattern.append(
        "whelk/{whelk}")
    whelk_message = make_message("Whelk", options=whelk_options)

    # Not resources
    octopus_message = make_message("Octopus")
    oyster_message = make_message("Oyster")
    nudibranch_message = make_message("Nudibranch")

    service = make_service(
        'Molluscs',
        methods=(
            make_method(
                f"Get{message.name}",
                input_message=make_message(
                    f"{message.name}Request",
                    fields=[make_field(message.name, message=message)]
                )
            )
            for message in (
                squid_message,
                clam_message,
                whelk_message,
                octopus_message,
                oyster_message,
                nudibranch_message
            )
        )
    )

    expected = {squid_message, clam_message, whelk_message}
    actual = service.resource_messages
    assert expected == actual


def make_service(name: str = 'Placeholder', host: str = '',
                 methods: typing.Tuple[wrappers.Method] = (),
                 scopes: typing.Tuple[str] = ()) -> wrappers.Service:
    # Define a service descriptor, and set a host and oauth scopes if
    # appropriate.
    service_pb = descriptor_pb2.ServiceDescriptorProto(name=name)
    if host:
        service_pb.options.Extensions[client_pb2.default_host] = host
    service_pb.options.Extensions[client_pb2.oauth_scopes] = ','.join(scopes)

    # Return a service object to test.
    return wrappers.Service(
        service_pb=service_pb,
        methods={m.name: m for m in methods},
    )


# FIXME (lukesneeringer): This test method is convoluted and it makes these
#                         tests difficult to understand and maintain.
def make_service_with_method_options(
    *,
    http_rule: http_pb2.HttpRule = None,
    method_signature: str = '',
    in_fields: typing.Tuple[descriptor_pb2.FieldDescriptorProto] = ()
) -> wrappers.Service:
    # Declare a method with options enabled for long-running operations and
    # field headers.
    method = get_method(
        'DoBigThing',
        'foo.bar.ThingRequest',
        'google.longrunning.operations_pb2.Operation',
        lro_response_type='foo.baz.ThingResponse',
        lro_metadata_type='foo.qux.ThingMetadata',
        in_fields=in_fields,
        http_rule=http_rule,
        method_signature=method_signature,
    )

    # Define a service descriptor.
    service_pb = descriptor_pb2.ServiceDescriptorProto(name='ThingDoer')

    # Return a service object to test.
    return wrappers.Service(
        service_pb=service_pb,
        methods={method.name: method},
    )


def get_method(name: str,
               in_type: str,
               out_type: str,
               lro_response_type: str = '',
               lro_metadata_type: str = '', *,
               in_fields: typing.Tuple[descriptor_pb2.FieldDescriptorProto] = (),
               http_rule: http_pb2.HttpRule = None,
               method_signature: str = '',
               ) -> wrappers.Method:
    input_ = get_message(in_type, fields=in_fields)
    output = get_message(out_type)
    lro = None

    # Define a method descriptor. Set the field headers if appropriate.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name=name,
        input_type=input_.ident.proto,
        output_type=output.ident.proto,
    )
    if lro_response_type:
        lro = wrappers.OperationInfo(
            response_type=get_message(lro_response_type),
            metadata_type=get_message(lro_metadata_type),
        )
    if http_rule:
        ext_key = annotations_pb2.http
        method_pb.options.Extensions[ext_key].MergeFrom(http_rule)
    if method_signature:
        ext_key = client_pb2.method_signature
        method_pb.options.Extensions[ext_key].append(method_signature)

    return wrappers.Method(
        method_pb=method_pb,
        input=input_,
        output=output,
        lro=lro,
        meta=input_.meta,
    )


def get_message(dot_path: str, *,
                fields: typing.Tuple[descriptor_pb2.FieldDescriptorProto] = (),
                ) -> wrappers.MessageType:
    # Pass explicit None through (for lro_metadata).
    if dot_path is None:
        return None

    # Note: The `dot_path` here is distinct from the canonical proto path
    # because it includes the module, which the proto path does not.
    #
    # So, if trying to test the DescriptorProto message here, the path
    # would be google.protobuf.descriptor.DescriptorProto (whereas the proto
    # path is just google.protobuf.DescriptorProto).
    pieces = dot_path.split('.')
    pkg, module, name = pieces[:-2], pieces[-2], pieces[-1]

    return wrappers.MessageType(
        fields={i.name: wrappers.Field(
            field_pb=i,
            enum=get_enum(i.type_name) if i.type_name else None,
        ) for i in fields},
        nested_messages={},
        nested_enums={},
        message_pb=descriptor_pb2.DescriptorProto(name=name, field=fields),
        meta=metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(pkg),
            module=module,
        )),
    )


def make_method(
        name: str, input_message: wrappers.MessageType = None,
        output_message: wrappers.MessageType = None,
        package: str = 'foo.bar.v1', module: str = 'baz',
        http_rule: http_pb2.HttpRule = None,
        signatures: typing.Sequence[str] = (),
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

    # If there is an HTTP rule, process it.
    if http_rule:
        ext_key = annotations_pb2.http
        method_pb.options.Extensions[ext_key].MergeFrom(http_rule)

    # If there are signatures, include them.
    for sig in signatures:
        ext_key = client_pb2.method_signature
        method_pb.options.Extensions[ext_key].append(sig)

    # Instantiate the wrapper class.
    return wrappers.Method(
        method_pb=method_pb,
        input=input_message,
        output=output_message,
        meta=metadata.Metadata(address=metadata.Address(
            name=name,
            package=package,
            module=module,
            parent=(f'{name}Service',),
        )),
    )


def make_field(name: str, repeated: bool = False,
               message: wrappers.MessageType = None,
               enum: wrappers.EnumType = None,
               meta: metadata.Metadata = None, **kwargs) -> wrappers.Method:
    if message:
        kwargs['type_name'] = str(message.meta.address)
    if enum:
        kwargs['type_name'] = str(enum.meta.address)
    field_pb = descriptor_pb2.FieldDescriptorProto(
        name=name,
        label=3 if repeated else 1,
        **kwargs
    )
    return wrappers.Field(
        enum=enum,
        field_pb=field_pb,
        message=message,
        meta=meta or metadata.Metadata(),
    )


def make_message(name: str, package: str = 'foo.bar.v1', module: str = 'baz',
                 fields: typing.Sequence[wrappers.Field] = (),
                 meta: metadata.Metadata = None,
                 options: descriptor_pb2.MethodOptions = None,
                 ) -> wrappers.MessageType:
    message_pb = descriptor_pb2.DescriptorProto(
        name=name,
        field=[i.field_pb for i in fields],
        options=options,
    )
    return wrappers.MessageType(
        message_pb=message_pb,
        fields=collections.OrderedDict((i.name, i) for i in fields),
        nested_messages={},
        nested_enums={},
        meta=meta or metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(package.split('.')),
            module=module,
        )),
    )


def get_enum(dot_path: str) -> wrappers.EnumType:
    pieces = dot_path.split('.')
    pkg, module, name = pieces[:-2], pieces[-2], pieces[-1]
    return wrappers.EnumType(
        enum_pb=descriptor_pb2.EnumDescriptorProto(name=name),
        meta=metadata.Metadata(address=metadata.Address(
            name=name,
            package=tuple(pkg),
            module=module,
        )),
        values=[],
    )
