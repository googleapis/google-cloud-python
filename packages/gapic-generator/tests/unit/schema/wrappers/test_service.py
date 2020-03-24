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
    make_enum,
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
    # Resources are labeled via an options extension
    def make_resource_opts(*args):
        opts = descriptor_pb2.MessageOptions()
        opts.Extensions[resource_pb2.resource].pattern.append(
            "/".join("{{{arg}}}/{arg}" for arg in args)
        )
        return opts

    # Regular, top level resource
    squid_resource = make_message("Squid", options=make_resource_opts("squid"))
    squid_request = make_message(
        "CreateSquid",
        fields=(
            make_field('squid', message=squid_resource),
        ),
    )

    # Nested resource
    squamosa_message = make_message(
        "Squamosa",
        options=make_resource_opts("clam", "squamosa"),
    )
    clam_resource = make_message(
        "Clam",
        options=make_resource_opts("clam"),
        fields=(
            make_field('squamosa', message=squamosa_message),
        ),
    )
    clam_request = make_message(
        'CreateClam',
        fields=(
            make_field('clam', message=clam_resource),
            # Red herring, not resources :)
            make_field('zone', 2, enum=make_enum('Zone')),
            make_field('pearls', 3, True, message=make_message('Pearl')),
        ),
    )

    # Some special APIs have request messages that _are_ resources.
    whelk_resource = make_message("Whelk", options=make_resource_opts("whelk"))

    # Not a resource
    octopus_request = make_message(
        "CreateOctopus",
        fields=(
            make_field('Octopus', message=make_message('Octopus')),
        ),
    )

    service = make_service(
        'Molluscs',
        methods=(
            make_method(
                f"{message.name}",
                input_message=message,
            )
            for message in (
                squid_request,
                clam_request,
                whelk_resource,
                octopus_request,
            )
        )
    )

    expected = {
        squid_resource,
        clam_resource,
        whelk_resource,
        squamosa_message,
    }
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
