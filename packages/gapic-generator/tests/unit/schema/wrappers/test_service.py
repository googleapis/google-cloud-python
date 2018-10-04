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

import typing

from google.api import annotations_pb2
from google.api import http_pb2
from google.api import signature_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers


def test_service_properties():
    service = make_service(name='ThingDoer')
    assert service.name == 'ThingDoer'


def test_service_host():
    service = make_service(host='thingdoer.googleapis.com')
    assert service.host == 'thingdoer.googleapis.com'


def test_service_no_host():
    service = make_service()
    assert service.host == '<<< SERVICE ADDRESS >>>'
    assert bool(service.host) is False


def test_service_scopes():
    service = make_service(scopes=('https://foo/user/', 'https://foo/admin/'))
    assert 'https://foo/user/' in service.oauth_scopes
    assert 'https://foo/admin/' in service.oauth_scopes


def test_service_no_scopes():
    service = make_service()
    assert len(service.oauth_scopes) == 0


def test_service_python_modules():
    service = make_service(methods=(
        get_method('DoThing', 'foo.bar.ThingRequest', 'foo.baz.ThingResponse'),
        get_method('Jump', 'foo.bacon.JumpRequest', 'foo.bacon.JumpResponse'),
        get_method('Yawn', 'a.b.v1.c.YawnRequest', 'x.y.v1.z.YawnResponse'),
    ))
    assert service.python_modules == (
        ('a.b.v1', 'c_pb2'),
        ('foo', 'bacon_pb2'),
        ('foo', 'bar_pb2'),
        ('foo', 'baz_pb2'),
        ('x.y.v1', 'z_pb2'),
    )


def test_service_python_modules_lro():
    service = make_service_with_method_options()
    assert service.python_modules == (
        ('foo', 'bar_pb2'),
        ('foo', 'baz_pb2'),
        ('foo', 'qux_pb2'),
        ('google.api_core', 'operation'),
    )


def test_service_python_modules_signature():
    service = make_service_with_method_options(
        in_fields=(
            descriptor_pb2.FieldDescriptorProto(name='secs', type=5),
            descriptor_pb2.FieldDescriptorProto(
                name='d',
                type=11,  # message
                type_name='a.b.c.v2.D',
            ),
        ),
        method_signature=signature_pb2.MethodSignature(fields=['secs', 'd']),
    )
    # type=5 is int, so nothing is added.
    assert service.python_modules == (
        ('a.b.c', 'v2_pb2'),
        ('foo', 'bar_pb2'),
        ('foo', 'baz_pb2'),
        ('foo', 'qux_pb2'),
        ('google.api_core', 'operation'),
    )


def test_service_no_lro():
    service = make_service()
    assert service.has_lro is False


def test_service_has_lro():
    service = make_service_with_method_options()
    assert service.has_lro


def test_module_name():
    service = make_service(name='MyService')
    assert service.module_name == 'my_service'


def make_service(name: str = 'Placeholder', host: str = '',
                 methods: typing.Tuple[wrappers.Method] = (),
                 scopes: typing.Tuple[str] = ()) -> wrappers.Service:
    # Define a service descriptor, and set a host and oauth scopes if
    # appropriate.
    service_pb = descriptor_pb2.ServiceDescriptorProto(name=name)
    if host:
        service_pb.options.Extensions[annotations_pb2.default_host] = host
    service_pb.options.Extensions[annotations_pb2.oauth].scopes.extend(scopes)

    # Return a service object to test.
    return wrappers.Service(
        service_pb=service_pb,
        methods={m.name: m for m in methods},
    )


# FIXME (lukesneeringer): This test method is convoluted and it makes these
#                         tests difficult to understand and maintain.
def make_service_with_method_options(*,
        http_rule: http_pb2.HttpRule = None,
        method_signature: signature_pb2.MethodSignature = None,
        in_fields: typing.Tuple[descriptor_pb2.FieldDescriptorProto] = ()
        ) -> wrappers.Service:
    # Declare a method with options enabled for long-running operations and
    # field headers.
    method = get_method(
        'DoBigThing',
        'foo.bar.ThingRequest',
        'google.longrunning.operations.Operation',
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
        method_signature: signature_pb2.MethodSignature = None,
        ) -> wrappers.Method:
    input_ = get_message(in_type, fields=in_fields)
    output = get_message(out_type)

    # Define a method descriptor. Set the field headers if appropriate.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name=name,
        input_type=input_.ident.proto,
        output_type=output.ident.proto,
    )
    if lro_response_type:
        output = wrappers.OperationType(
            lro_response=get_message(lro_response_type),
            lro_metadata=get_message(lro_metadata_type),
        )
    if http_rule:
        ext_key = annotations_pb2.http
        method_pb.options.Extensions[ext_key].MergeFrom(http_rule)
    if method_signature:
        ext_key = annotations_pb2.method_signature
        method_pb.options.Extensions[ext_key].MergeFrom(method_signature)

    return wrappers.Method(
        method_pb=method_pb,
        input=input_,
        output=output,
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
            message=get_message(i.type_name) if i.type_name else None,
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
