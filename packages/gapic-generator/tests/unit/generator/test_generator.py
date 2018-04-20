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
from unittest import mock

import jinja2

from google.protobuf import descriptor_pb2
from google.protobuf.compiler import plugin_pb2

from api_factory.generator import generator
from api_factory.schema import wrappers
from api_factory.schema.api import API
from api_factory.schema.pb import client_pb2


def test_constructor():
    # Crete a bogue and very stripped down request.
    request = plugin_pb2.CodeGeneratorRequest(proto_file=[
        # We are just going to prove that each file is loaded,
        # so it does not matter what is in them.
        descriptor_pb2.FileDescriptorProto(),
        descriptor_pb2.FileDescriptorProto(),
    ])

    # Create a generator, prove it has an API.
    # This is somewhat internal implementation baseball, but realistically
    # the only reasonable way to write these tests is to split them up by
    # internal segment.
    with mock.patch.object(API, 'load') as load:
        g = generator.Generator(request)
        assert load.call_count == 2
    assert isinstance(g._api, API)

    # Assert we have a Jinja environment also, with the expected filters.
    # Still internal implementation baseball, but this is the best place
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
    g = make_generator(proto_file=[file_pb2])

    # Mock all the rendering methods.
    with mock.patch.object(g, '_render_templates') as _render_templates:
        _render_templates.return_value = [
            plugin_pb2.CodeGeneratorResponse.File(
                name='template_file',
                content='This was a template.',
            ),
        ]
        with mock.patch.object(g, '_read_flat_files') as _read_flat_files:
            _read_flat_files.return_value = [
                plugin_pb2.CodeGeneratorResponse.File(
                    name='flat_file',
                    content='This was a flat file.',
                ),
            ]

            # Okay, now run the `get_response` method.
            response = g.get_response()

            # First and foremost, we care that we got a valid response
            # object back (albeit not so much what is in it).
            assert isinstance(response, plugin_pb2.CodeGeneratorResponse)

            # Next, determine that flat files were read.
            assert _read_flat_files.call_count == 1
            _, args, _ = _read_flat_files.mock_calls[0]
            assert args[0].endswith('files')

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
    g = make_generator()

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
    g = make_generator()

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


def test_read_flat_files():
    g = make_generator()

    # This function walks over a directory on the operating system;
    # even though that directory is actually in this repo, fake it.
    with mock.patch.object(os, 'walk') as walk:
        walk.return_value = (
            ('files/', [], ['foo.ext']),
            ('files/other/', [], ['bar.ext']),
        )

        # This function also reads files from disk, fake that too.
        with mock.patch.object(io, 'open') as open:
            open.side_effect = lambda fn, mode: io.StringIO(f'abc-{fn}-{mode}')

            # Okay, now we can run the function.
            files = g._read_flat_files('files/')

            # Each file should have been opened, so one call to `io.open`
            # per file.
            assert open.call_count == len(walk.return_value)

        # `os.walk` should have been called once and exactly once,
        # with unmodified input.
        walk.assert_called_once_with('files/')

        # Lastly, we should have gotten one file back for each file
        # yielded by walk, and each one should have the expected contents
        # (the 'abc' prefix and then the filename and read mode).
        assert len(files) == 2
        assert files[0].name == 'foo.ext'
        assert files[1].name == 'other/bar.ext'
        assert files[0].content == 'abc-files/foo.ext-r'
        assert files[1].content == 'abc-files/other/bar.ext-r'


def test_get_output_filename():
    g = make_generator(proto_file=[make_proto_file(name='Spam', version='v2')])
    template_name = '$namespace/$name_$version/foo.py.j2'
    assert g._get_output_filename(template_name) == 'spam_v2/foo.py'


def test_get_output_filename_with_namespace():
    g = make_generator(proto_file=[make_proto_file(
        name='Spam',
        namespace=['Ham', 'Bacon'],
        version='v2',
    )])
    template_name = '$namespace/$name_$version/foo.py.j2'
    assert g._get_output_filename(template_name) == 'ham/bacon/spam_v2/foo.py'


def test_get_output_filename_with_service():
    g = make_generator(proto_file=[make_proto_file(name='spam', version='v2')])
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


def make_generator(**kwargs):
    return generator.Generator(plugin_pb2.CodeGeneratorRequest(**kwargs))


def make_proto_file(**kwargs):
    proto_file = descriptor_pb2.FileDescriptorProto()
    proto_file.options.Extensions[client_pb2.client].MergeFrom(
        client_pb2.Client(**kwargs),
    )
    return proto_file
