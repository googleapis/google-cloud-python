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
import itertools
import typing

from google.api import resource_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import imp

from test_utils.test_utils import (
    get_method,
    make_field,
    make_message,
    make_method,
    make_service,
    make_service_with_method_options,
)


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
        for i in m.ref_types
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


def test_service_any_streaming():
    for client, server in itertools.product((True, False), (True, False)):
        service = make_service(
            f'ClientStream{client}:ServerStream{server}',
            methods=(
                (
                    make_method(
                        f"GetMollusc",
                        input_message=make_message(
                            "GetMolluscRequest",
                        ),
                        output_message=make_message(
                            "GetMolluscResponse",
                        ),
                        client_streaming=client,
                        server_streaming=server,
                    ),
                )
            )
        )

        assert service.any_client_streaming == client
        assert service.any_server_streaming == server
