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
    service = make_service()
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


def test_service_no_lro():
    service = make_service()
    assert service.has_lro is False


def test_service_has_lro():
    service = make_service_with_method_options()
    assert service.has_lro


def test_service_no_field_headers():
    service = make_service()
    assert service.has_field_headers is False


def test_service_has_field_headers():
    http_rule = http_pb2.HttpRule(get='/v1/{parent=projects/*}/topics')
    service = make_service_with_method_options(http_rule=http_rule)
    assert service.has_field_headers


def test_module_name():
    service = make_service(name='MyService')
    assert service.module_name == 'my_service'


def make_service(name: str = 'Placeholder', host: str = '',
                 scopes: typing.Tuple[str] = ()) -> wrappers.Service:
    # Declare a few methods, with messages in distinct packages.
    methods = (
        get_method('DoThing', 'foo.bar.ThingRequest', 'foo.baz.ThingResponse'),
        get_method('Jump', 'foo.bacon.JumpRequest', 'foo.bacon.JumpResponse'),
        get_method('Yawn', 'a.b.v1.c.YawnRequest', 'x.y.v1.z.YawnResponse'),
    )

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


def make_service_with_method_options(*,
        http_rule: http_pb2.HttpRule = None,
        ) -> wrappers.Service:
    # Declare a method with options enabled for long-running operations and
    # field headers.
    method = get_method(
        'DoBigThing',
        'foo.bar.ThingRequest',
        'google.longrunning.operations.Operation',
        lro_response_type='foo.baz.ThingResponse',
        lro_metadata_type='foo.qux.ThingMetadata',
        http_rule=http_rule,
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
        lro_metadata_type: str = '',
        http_rule: http_pb2.HttpRule = None,
        ) -> wrappers.Method:
    input_ = get_message(in_type)
    output = get_message(out_type)

    # Define a method descriptor. Set the field headers if appropriate.
    method_pb = descriptor_pb2.MethodDescriptorProto(
        name=name,
        input_type=input_.proto_path,
        output_type=output.proto_path,
    )
    if lro_response_type:
        output = wrappers.OperationType(
            lro_response=get_message(lro_response_type),
            lro_metadata=get_message(lro_metadata_type),
        )
    if http_rule:
        ext_key = annotations_pb2.http
        method_pb.options.Extensions[ext_key].MergeFrom(http_rule)

    return wrappers.Method(
        method_pb=method_pb,
        input=input_,
        output=output,
    )


def get_message(dot_path: str) -> wrappers.MessageType:
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
        fields={},
        message_pb=descriptor_pb2.DescriptorProto(name=name),
        meta=metadata.Metadata(address=metadata.Address(
            package=pkg,
            module=module,
        )),
    )
