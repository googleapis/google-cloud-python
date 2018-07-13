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

import io
import os
from typing import Mapping
from unittest import mock

import jinja2

from google.protobuf import descriptor_pb2
from google.protobuf.compiler import plugin_pb2

from api_factory.generator import generator
from api_factory.schema import api
from api_factory.schema import naming
from api_factory.schema import wrappers


def test_proto_builder_constructor():
    # Create a generator.
    g = generator.Generator(api_schema=make_api())
    assert isinstance(g._api, api.API)

    # Assert we have a Jinja environment also, with the expected filters.
    # This is internal implementation baseball, but this is the best place
    # to establish this and templates will depend on it.
    assert isinstance(g._env, jinja2.Environment)
    assert 'snake_case' in g._env.filters
    assert 'subsequent_indent' in g._env.filters
    assert 'wrap' in g._env.filters


def test_get_response():
    # Create a generator with mock data.
    #
    # We want to ensure that templates are rendered for each service,
    # which we prove by sending two services.
    file_pb2 = descriptor_pb2.FileDescriptorProto(
        name='bacon.proto',
        package='foo.bar.v1',
        service=[descriptor_pb2.ServiceDescriptorProto(name='SpamService'),
                 descriptor_pb2.ServiceDescriptorProto(name='EggsService')],
    )
    api_schema = make_api(make_proto(file_pb2))
    g = generator.Generator(api_schema=api_schema)

    # Mock all the rendering methods.
    with mock.patch.object(g, '_render_templates') as _render_templates:
        _render_templates.return_value = [
            plugin_pb2.CodeGeneratorResponse.File(
                name='template_file',
                content='This was a template.',
            ),
        ]

        # Okay, now run the `get_response` method.
        response = g.get_response()

        # First and foremost, we care that we got a valid response
        # object back (albeit not so much what is in it).
        assert isinstance(response, plugin_pb2.CodeGeneratorResponse)

        # Next, determine that the general API templates and service
        # templates were both called; the method should be called
        # once per service plus one for the API as a whole.
        assert _render_templates.call_count == len(file_pb2.service) + 1

        # The service templates should have been called with the
        # filename transformation and the additional `service` variable.
        for call in _render_templates.mock_calls:
            _, args, kwargs = call
            if args[0] != g._env.loader.service_templates:
                continue
            service = kwargs['additional_context']['service']
            assert isinstance(service, wrappers.Service)


def test_render_templates():
    g = generator.Generator(api_schema=make_api())

    # Determine the templates to be rendered.
    templates = ('foo.j2', 'bar.j2')
    with mock.patch.object(jinja2.Environment, 'get_template') as get_template:
        get_template.side_effect = lambda t: jinja2.Template(
            f'Hello, I am `{t}`.',
        )

        # Render the templates.
        files = g._render_templates(templates)

    # Test that we get back the expected content for each template.
    assert len(files) == 2
    assert files[0].name == 'foo'
    assert files[1].name == 'bar'
    assert files[0].content == 'Hello, I am `foo.j2`.\n'
    assert files[1].content == 'Hello, I am `bar.j2`.\n'


def test_render_templates_additional_context():
    g = generator.Generator(api_schema=make_api())

    # Determine the templates to be rendered.
    templates = ('foo.j2',)
    with mock.patch.object(jinja2.Environment, 'get_template') as get_template:
        get_template.return_value = jinja2.Template('A {{ thing }}!')

        # Render the templates.
        files = g._render_templates(templates, additional_context={
            'thing': 'bird',
        })

    # Test that we get back the expected content for each template.
    assert len(files) == 1
    assert files[0].name == 'foo'
    assert files[0].content == 'A bird!\n'


def test_get_output_filename():
    g = generator.Generator(api_schema=make_api(
        naming=make_naming(namespace=(), name='Spam', version='v2'),
    ))
    template_name = '$namespace/$name_$version/foo.py.j2'
    assert g._get_output_filename(template_name) == 'spam_v2/foo.py'


def test_get_output_filename_with_namespace():
    g = generator.Generator(api_schema=make_api(
        naming=make_naming(
            name='Spam',
            namespace=('Ham', 'Bacon'),
            version='v2',
        ),
    ))
    template_name = '$namespace/$name_$version/foo.py.j2'
    assert g._get_output_filename(template_name) == 'ham/bacon/spam_v2/foo.py'


def test_get_output_filename_with_service():
    g = generator.Generator(api_schema=make_api(
        naming=make_naming(namespace=(), name='Spam', version='v2'),
    ))
    template_name = '$name/$service/foo.py.j2'
    assert g._get_output_filename(
        template_name,
        context={
            'service': wrappers.Service(
                methods=[],
                service_pb=descriptor_pb2.ServiceDescriptorProto(name='Eggs'),
            ),
        }
    ) == 'spam/eggs/foo.py'


def make_proto(file_pb: descriptor_pb2.FileDescriptorProto,
        file_to_generate: bool = True, prior_protos: Mapping = None,
        ) -> api.Proto:
    prior_protos = prior_protos or {}
    return api._ProtoBuilder(file_pb,
        file_to_generate=file_to_generate,
        prior_protos=prior_protos,
    ).proto


def make_api(*protos, naming: naming.Naming = None) -> api.API:
    return api.API(
        naming=naming or make_naming(),
        protos={i.name: i for i in protos},
    )


def make_naming(**kwargs) -> naming.Naming:
    kwargs.setdefault('name', 'Hatstand')
    kwargs.setdefault('namespace', ('Google', 'Cloud'))
    kwargs.setdefault('version', 'v1')
    kwargs.setdefault('product_name', 'Hatstand')
    kwargs.setdefault('product_url', 'https://cloud.google.com/hatstand/')
    return naming.Naming(**kwargs)
