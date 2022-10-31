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

import json
from textwrap import dedent
from typing import Mapping
from unittest import mock

import jinja2
import pytest

from google.api import service_pb2
from google.protobuf import descriptor_pb2
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

from gapic.generator import generator
from gapic.samplegen_utils import snippet_metadata_pb2, types, yaml
from ..common_types import (DummyApiSchema, DummyField, DummyIdent, DummyNaming, DummyMessage, DummyMessageTypePB,
                          DummyService, DummyMethod, message_factory, enum_factory)

from gapic.schema import api
from gapic.schema import naming
from gapic.schema import wrappers
from gapic.utils import Options


def mock_generate_sample(*args, **kwargs):
    dummy_snippet_metadata = snippet_metadata_pb2.Snippet()
    dummy_snippet_metadata.client_method.method.service.short_name = args[0]["service"].split(
        ".")[-1]
    dummy_snippet_metadata.client_method.method.short_name = args[0]['rpc']

    return "", dummy_snippet_metadata


def test_custom_template_directory():
    # Create a generator.
    opts = Options.build("python-gapic-templates=/templates/")
    g = generator.Generator(opts)

    # Assert that the Jinja loader will pull from the correct location.
    assert g._env.loader.searchpath == ["/templates"]


def test_get_response():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = ["foo/bar/baz.py.j2", "molluscs/squid/sample.py.j2"]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("I am a template result.")
            cgr = g.get_response(api_schema=make_api(),
                                 opts=Options.build(""))
            lt.assert_called_once()
            gt.assert_has_calls(
                [
                    mock.call("molluscs/squid/sample.py.j2"),
                    mock.call("foo/bar/baz.py.j2"),
                ]
            )
            assert len(cgr.file) == 1
            assert cgr.file[0].name == "foo/bar/baz.py"
            assert cgr.file[0].content == "I am a template result.\n"


def test_get_response_ignores_empty_files():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = ["foo/bar/baz.py.j2", "molluscs/squid/sample.py.j2"]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("# Meaningless comment")
            cgr = g.get_response(api_schema=make_api(),
                                 opts=Options.build(""))
            lt.assert_called_once()
            gt.assert_has_calls(
                [
                    mock.call("molluscs/squid/sample.py.j2"),
                    mock.call("foo/bar/baz.py.j2"),
                ]
            )
            assert len(cgr.file) == 0


def test_get_response_ignores_private_files():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/bar/baz.py.j2",
            "foo/bar/_base.py.j2",
            "molluscs/squid/sample.py.j2",
        ]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("I am a template result.")
            cgr = g.get_response(api_schema=make_api(),
                                 opts=Options.build(""))
            lt.assert_called_once()
            gt.assert_has_calls(
                [
                    mock.call("molluscs/squid/sample.py.j2"),
                    mock.call("foo/bar/baz.py.j2"),
                ]
            )
            assert len(cgr.file) == 1
            assert cgr.file[0].name == "foo/bar/baz.py"
            assert cgr.file[0].content == "I am a template result.\n"


def test_get_response_fails_invalid_file_paths():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/bar/%service/%proto/baz.py.j2",
        ]
        with pytest.raises(ValueError) as ex:
            g.get_response(api_schema=make_api(),
                           opts=Options.build(""))

        ex_str = str(ex.value)
        assert "%proto" in ex_str and "%service" in ex_str


def test_get_response_ignore_gapic_metadata():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = ["gapic/gapic_metadata.json.j2"]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template(
                "This is not something we want to see")
            res = g.get_response(
                api_schema=make_api(),
                opts=Options.build(""),
            )

            # We don't expect any files because opts.metadata is not set.
            assert res.file == CodeGeneratorResponse().file


def test_get_response_ignores_unwanted_transports_and_clients():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/%service/transports/river.py.j2",
            "foo/%service/transports/car.py.j2",
            "foo/%service/transports/grpc.py.j2",
            "foo/%service/transports/__init__.py.j2",
            "foo/%service/transports/base.py.j2",
            "foo/%service/async_client.py.j2",
            "foo/%service/client.py.j2",
            "mollusks/squid/sample.py.j2",
        ]

        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("Service: {{ service.name }}")
            api_schema = make_api(
                make_proto(
                    descriptor_pb2.FileDescriptorProto(
                        service=[
                            descriptor_pb2.ServiceDescriptorProto(
                                name="SomeService"),
                        ]
                    ),
                )
            )

            cgr = g.get_response(
                api_schema=api_schema,
                opts=Options.build("transport=river+car")
            )
            assert len(cgr.file) == 5
            assert {i.name for i in cgr.file} == {
                "foo/some_service/transports/river.py",
                "foo/some_service/transports/car.py",
                "foo/some_service/transports/__init__.py",
                "foo/some_service/transports/base.py",
                # Only generate async client with grpc transport
                "foo/some_service/client.py",
            }

            cgr = g.get_response(
                api_schema=api_schema,
                opts=Options.build("transport=grpc")
            )
            assert len(cgr.file) == 5
            assert {i.name for i in cgr.file} == {
                "foo/some_service/transports/grpc.py",
                "foo/some_service/transports/__init__.py",
                "foo/some_service/transports/base.py",
                "foo/some_service/client.py",
                "foo/some_service/async_client.py",
            }


def test_get_response_enumerates_services():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/%service/baz.py.j2",
            "molluscs/squid/sample.py.j2",
        ]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("Service: {{ service.name }}")
            cgr = g.get_response(
                api_schema=make_api(
                    make_proto(
                        descriptor_pb2.FileDescriptorProto(
                            service=[
                                descriptor_pb2.ServiceDescriptorProto(
                                    name="Spam"),
                                descriptor_pb2.ServiceDescriptorProto(
                                    name="EggsService"
                                ),
                            ]
                        ),
                    )
                ),
                opts=Options.build(""),
            )
            assert len(cgr.file) == 2
            assert {i.name for i in cgr.file} == {
                "foo/spam/baz.py",
                "foo/eggs_service/baz.py",
            }


def test_get_response_enumerates_proto():
    g = make_generator()
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/%proto.py.j2",
            "molluscs/squid/sample.py.j2",
        ]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template("Proto: {{ proto.module_name }}")
            cgr = g.get_response(
                api_schema=make_api(
                    make_proto(
                        descriptor_pb2.FileDescriptorProto(name="a.proto")),
                    make_proto(
                        descriptor_pb2.FileDescriptorProto(name="b.proto")),
                ),
                opts=Options.build(""),
            )
            assert len(cgr.file) == 2
            assert {i.name for i in cgr.file} == {"foo/a.py", "foo/b.py"}


def test_get_response_divides_subpackages():
    # NOTE: autogen-snippets is intentionally disabled for this test
    # The API schema below is incomplete and will result in errors when the
    # snippetgen logic tries to parse it.
    g = make_generator("autogen-snippets=false")
    api_schema = api.API.build(
        [
            descriptor_pb2.FileDescriptorProto(
                name="top.proto",
                package="foo.v1",
                service=[descriptor_pb2.ServiceDescriptorProto(name="Top")],
            ),
            descriptor_pb2.FileDescriptorProto(
                name="a/spam/ham.proto",
                package="foo.v1.spam",
                service=[descriptor_pb2.ServiceDescriptorProto(name="Bacon")],
            ),
            descriptor_pb2.FileDescriptorProto(
                name="a/eggs/yolk.proto",
                package="foo.v1.eggs",
                service=[descriptor_pb2.ServiceDescriptorProto(
                    name="Scramble")],
            ),
        ],
        package="foo.v1",
    )
    with mock.patch.object(jinja2.FileSystemLoader, "list_templates") as lt:
        lt.return_value = [
            "foo/%sub/types/%proto.py.j2",
            "foo/%sub/services/%service.py.j2",
            "molluscs/squid/sample.py.j2",
        ]
        with mock.patch.object(jinja2.Environment, "get_template") as gt:
            gt.return_value = jinja2.Template(
                """
                {{- '' }}Subpackage: {{ '.'.join(api.subpackage_view) }}
            """.strip()
            )
            cgr = g.get_response(api_schema=api_schema,
                                 opts=Options.build("autogen-snippets=false"))
            assert len(cgr.file) == 6
            assert {i.name for i in cgr.file} == {
                "foo/types/top.py",
                "foo/services/top.py",
                "foo/spam/types/ham.py",
                "foo/spam/services/bacon.py",
                "foo/eggs/types/yolk.py",
                "foo/eggs/services/scramble.py",
            }


def test_get_filename():
    g = make_generator()
    template_name = "%namespace/%name_%version/foo.py.j2"
    assert (
        g._get_filename(
            template_name,
            api_schema=make_api(
                naming=make_naming(namespace=(), name="Spam", version="v2"),
            ),
        )
        == "spam_v2/foo.py"
    )


def test_get_filename_with_namespace():
    g = make_generator()
    template_name = "%namespace/%name_%version/foo.py.j2"
    assert (
        g._get_filename(
            template_name,
            api_schema=make_api(
                naming=make_naming(
                    name="Spam", namespace=("Ham", "Bacon"), version="v2",
                ),
            ),
        )
        == "ham/bacon/spam_v2/foo.py"
    )


def test_get_filename_with_service():
    g = make_generator()
    template_name = "%name/%service/foo.py.j2"
    assert (
        g._get_filename(
            template_name,
            api_schema=make_api(
                naming=make_naming(namespace=(), name="Spam", version="v2"),
            ),
            context={
                "service": wrappers.Service(
                    methods=[],
                    service_pb=descriptor_pb2.ServiceDescriptorProto(
                        name="Eggs"),
                    visible_resources={},
                ),
            },
        )
        == "spam/eggs/foo.py"
    )


def test_get_filename_with_proto():
    file_pb2 = descriptor_pb2.FileDescriptorProto(
        name="bacon.proto", package="foo.bar.v1",
    )
    api = make_api(
        make_proto(file_pb2),
        naming=make_naming(namespace=(), name="Spam", version="v2"),
    )

    g = make_generator()
    assert (
        g._get_filename(
            "%name/types/%proto.py.j2",
            api_schema=api,
            context={"proto": api.protos["bacon.proto"]},
        )
        == "spam/types/bacon.py"
    )


def test_get_filename_with_proto_and_sub():
    file_pb2 = descriptor_pb2.FileDescriptorProto(
        name="bacon.proto", package="foo.bar.v2.baz",
    )
    naming = make_naming(
        namespace=("Foo",), name="Bar", proto_package="foo.bar.v2", version="v2",
    )
    api = make_api(
        make_proto(file_pb2, naming=naming), naming=naming, subpackage_view=("baz",),
    )

    g = make_generator()
    assert (
        g._get_filename(
            "%name/types/%sub/%proto.py.j2",
            api_schema=api,
            context={"proto": api.protos["bacon.proto"]},
        )
        == "bar/types/baz/bacon.py"
    )


def test_parse_sample_paths(fs):
    fpath = "sampledir/sample.yaml"
    fs.create_file(
        fpath,
        contents=dedent(
            """
            ---
            type: com.google.api.codegen.samplegen.v1p2.SampleConfigProto
            schema_version: 1.2.0
            samples:
            - service: google.cloud.language.v1.LanguageService
            """
        ),
    )

    with pytest.raises(types.InvalidConfig):
        Options.build("samples=sampledir/,")


@mock.patch("time.gmtime",)
def test_samplegen_config_to_output_files(mock_gmtime, fs):
    # These time values are nothing special,
    # they just need to be deterministic.
    returner = mock.MagicMock()
    returner.tm_year = 2112
    returner.tm_mon = 6
    returner.tm_mday = 1
    returner.tm_hour = 13
    returner.tm_min = 13
    returner.tm_sec = 13
    mock_gmtime.return_value = returner

    fs.create_file(
        "samples.yaml",
        contents=dedent(
            """
            ---
            type: com.google.api.codegen.samplegen.v1p2.SampleConfigProto
            schema_version: 1.2.0
            samples:
            - id: squid_sample
              region_tag: humboldt_tag
              service: Mollusc.v1.Mollusc
              rpc: GetSquidStreaming
            - region_tag: clam_sample
              service: Mollusc.v1.Mollusc
              rpc: GetClam
            """
        ),
    )

    g = generator.Generator(Options.build("samples=samples.yaml",))
    # Need to have the sample template visible to the generator.
    g._env.loader = jinja2.DictLoader({"sample.py.j2": ""})

    api_schema = DummyApiSchema(
        services={"Mollusc": DummyService(
            name="Mollusc",
            methods={
                # For this test the generator only cares about the dictionary keys
                "GetSquidStreaming": DummyMethod(),
                "GetClam": DummyMethod(),
            },
            )},
        naming=DummyNaming(name="mollusc", version="v1", warehouse_package_name="mollusc-cephalopod-teuthida-",
                           versioned_module_name="teuthida_v1", module_namespace="mollusc.cephalopod", proto_package="google.mollusca.v1"),
    )

    with mock.patch("gapic.samplegen.samplegen.generate_sample", side_effect=mock_generate_sample):
        actual_response = g.get_response(
            api_schema, opts=Options.build("autogen-snippets=False"))

    expected_snippet_index_json = {
        "clientLibrary": {
            "apis": [{
                "id": "google.mollusca.v1",
                "version": "v1"
            }],
            "language": "PYTHON",
            "name": "mollusc-cephalopod-teuthida-",
            "version": "0.1.0"
            },
        "snippets": [
            {
                "clientMethod": {
                    "method": {
                        "service": {
                            "shortName": "Mollusc"
                            },
                        "shortName": "GetSquidStreaming"
                        }
                    },
                "file": "squid_sample.py",
                "segments": [
                    {"type": "FULL"},
                    {"type": "SHORT"},
                    {"type": "CLIENT_INITIALIZATION"},
                    {"type": "REQUEST_INITIALIZATION"},
                    {"type": "REQUEST_EXECUTION"},
                    {"type": "RESPONSE_HANDLING"}
                ],
                "title": "squid_sample.py"
                },
            {
                "clientMethod": {
                    "method": {
                        "service": {
                            "shortName": "Mollusc"
                            },
                        "shortName": "GetClam"
                        }
                    },
                "file": "clam_sample.py",
                "segments": [
                    {"type": "FULL"},
                    {"type": "SHORT"},
                    {"type": "CLIENT_INITIALIZATION"},
                    {"type": "REQUEST_INITIALIZATION"},
                    {"type": "REQUEST_EXECUTION"},
                    {"type": "RESPONSE_HANDLING"}
                ],
                "title": "clam_sample.py"
                }
            ]
        }

    assert actual_response.supported_features == CodeGeneratorResponse.Feature.FEATURE_PROTO3_OPTIONAL

    assert len(actual_response.file) == 3
    assert actual_response.file[0] == CodeGeneratorResponse.File(
        name="samples/generated_samples/squid_sample.py", content="\n",)
    assert actual_response.file[1] == CodeGeneratorResponse.File(
        name="samples/generated_samples/clam_sample.py", content="\n",)

    assert actual_response.file[2].name == "samples/generated_samples/snippet_metadata_google.mollusca.v1.json"

    assert json.loads(
        actual_response.file[2].content) == expected_snippet_index_json


@mock.patch(
    "gapic.samplegen.samplegen.generate_sample_specs", return_value=[]
)
@mock.patch(
    "gapic.samplegen.samplegen.generate_sample", return_value=("", snippet_metadata_pb2.Snippet()),
)
def test_generate_autogen_samples(mock_generate_sample, mock_generate_specs):
    opts = Options.build("autogen-snippets")
    g = generator.Generator(opts)
    # Need to have the sample template visible to the generator.
    g._env.loader = jinja2.DictLoader({"sample.py.j2": ""})

    api_schema = make_api(naming=naming.NewNaming(
        name="Mollusc", version="v6"))

    actual_response = g.get_response(api_schema, opts=opts)

    # Just check that generate_sample_specs was called
    # Correctness of the spec is tested in samplegen unit tests
    mock_generate_specs.assert_called_once_with(
        api_schema,
        opts=opts
    )


@mock.patch("time.gmtime",)
def test_samplegen_id_disambiguation(mock_gmtime, fs):
    # These time values are nothing special,
    # they just need to be deterministic.
    returner = mock.MagicMock()
    returner.tm_year = 2112
    returner.tm_mon = 6
    returner.tm_mday = 1
    returner.tm_hour = 13
    returner.tm_min = 13
    returner.tm_sec = 13
    mock_gmtime.return_value = returner

    # Note: The first two samples will have the same nominal ID, the first by
    #       explicit naming and the second by falling back to the region_tag.
    #       The third has no id of any kind, so the generator is required to make a
    #       unique ID for it.
    fs.create_file(
        "samples.yaml",
        contents=dedent(
            """
            ---
            type: com.google.api.codegen.samplegen.v1p2.SampleConfigProto
            schema_version: 1.2.0
            samples:
            - id: squid_sample
              region_tag: humboldt_tag
              rpc: GetSquidStreaming
              service: Mollusc.v1.Mollusc
            # Note that this region tag collides with the id of the previous sample.
            - region_tag: squid_sample
              rpc: GetSquidStreaming
              service: Mollusc.v1.Mollusc
            # No id or region tag.
            - rpc: GetSquidStreaming
              service: Mollusc.v1.Mollusc
            """
        ),
    )
    g = generator.Generator(Options.build("samples=samples.yaml"))
    # Need to have the sample template visible to the generator.
    g._env.loader = jinja2.DictLoader({"sample.py.j2": ""})

    api_schema = DummyApiSchema(
        services={"Mollusc": DummyService(
            name="Mollusc",
            methods={
                # The generator only cares about the dictionary keys
                "GetSquidStreaming": DummyMethod(),
                "GetClam": DummyMethod(),
            },
            )},
        naming=DummyNaming(name="mollusc", version="v1", warehouse_package_name="mollusc-cephalopod-teuthida-",
                           versioned_module_name="teuthida_v1", module_namespace="mollusc.cephalopod", proto_package="google.mollusca.v1"),
    )
    with mock.patch("gapic.samplegen.samplegen.generate_sample", side_effect=mock_generate_sample):
        actual_response = g.get_response(api_schema,
                                     opts=Options.build("autogen-snippets=False"))

    expected_snippet_metadata_json = {
        "clientLibrary": {
            "apis": [
                {
                    "id": "google.mollusca.v1",
                    "version": "v1"
                    }
            ],
            "language": "PYTHON",
            "name": "mollusc-cephalopod-teuthida-",
            "version": "0.1.0"
        },
        "snippets": [
            {
                "clientMethod": {
                    "method": {
                        "service": {
                            "shortName": "Mollusc"
                            },
                        "shortName": "GetSquidStreaming"
                    }
                },
                "file": "squid_sample_1cfd0b3d.py",
                "segments": [
                    {"type": "FULL"},
                    {"type": "SHORT"},
                    {"type": "CLIENT_INITIALIZATION"},
                    {"type": "REQUEST_INITIALIZATION"},
                    {"type": "REQUEST_EXECUTION"},
                    {"type": "RESPONSE_HANDLING"}
                ],
                "title": "squid_sample_1cfd0b3d.py"
                },
            {
                "clientMethod": {
                    "method": {
                        "service": {
                            "shortName": "Mollusc"
                            },
                        "shortName": "GetSquidStreaming"
                    }
                },
                "file": "squid_sample_cf4d4fa4.py",
                "segments": [
                    {"type": "FULL"},
                    {"type": "SHORT"},
                    {"type": "CLIENT_INITIALIZATION"},
                    {"type": "REQUEST_INITIALIZATION"},
                    {"type": "REQUEST_EXECUTION"},
                    {"type": "RESPONSE_HANDLING"}
                ],
                "title": "squid_sample_cf4d4fa4.py"
                },
            {
                "clientMethod": {
                    "method": {
                        "service": {
                            "shortName": "Mollusc"
                            },
                        "shortName": "GetSquidStreaming"
                    }
                },
                "file": "7384949e.py",
                "segments": [
                    {"type": "FULL"},
                    {"type": "SHORT"},
                    {"type": "CLIENT_INITIALIZATION"},
                    {"type": "REQUEST_INITIALIZATION"},
                    {"type": "REQUEST_EXECUTION"},
                    {"type": "RESPONSE_HANDLING"}
                ],
                "title": "7384949e.py"
                }
            ]
    }

    assert actual_response.supported_features == CodeGeneratorResponse.Feature.FEATURE_PROTO3_OPTIONAL
    assert len(actual_response.file) == 4
    assert actual_response.file[0] == CodeGeneratorResponse.File(
        name="samples/generated_samples/squid_sample_1cfd0b3d.py", content="\n",
    )
    assert actual_response.file[1] == CodeGeneratorResponse.File(
        name="samples/generated_samples/squid_sample_cf4d4fa4.py", content="\n",
    )
    assert actual_response.file[2] == CodeGeneratorResponse.File(
        name="samples/generated_samples/7384949e.py", content="\n",
    )
    print(actual_response.file[3].content)
    assert actual_response.file[3].name == "samples/generated_samples/snippet_metadata_google.mollusca.v1.json"
    assert json.loads(
        actual_response.file[3].content) == expected_snippet_metadata_json


def test_generator_duplicate_samples(fs):
    config_fpath = "samples.yaml"
    fs.create_file(
        config_fpath,
        contents=dedent(
            """
            # Note: the samples are duplicates.
            type: com.google.api.codegen.samplegen.v1p2.SampleConfigProto
            schema_version: 1.2.0
            samples:
            - id: squid_sample
              region_tag: humboldt_tag
              rpc: get_squid
            - id: squid_sample
              region_tag: humboldt_tag
              rpc: get_squid
            """
        ),
    )

    generator = make_generator("samples=samples.yaml")
    generator._env.loader = jinja2.DictLoader({"sample.py.j2": ""})
    api_schema = make_api(naming=naming.NewNaming(
        name="Mollusc", version="v6"))

    with pytest.raises(types.DuplicateSample):
        generator.get_response(api_schema=api_schema,
                               opts=Options.build(""))


def make_generator(opts_str: str = "") -> generator.Generator:
    return generator.Generator(Options.build(opts_str))


def make_proto(
    file_pb: descriptor_pb2.FileDescriptorProto,
    file_to_generate: bool = True,
    prior_protos: Mapping = None,
    naming: naming.Naming = None,
) -> api.Proto:
    prior_protos = prior_protos or {}
    return api._ProtoBuilder(
        file_pb,
        file_to_generate=file_to_generate,
        naming=naming or make_naming(),
        prior_protos=prior_protos,
    ).proto


def make_api(
    *protos,
    naming: naming.Naming = None,
    service_yaml_config: service_pb2.Service = None,
    **kwargs
) -> api.API:
    return api.API(
        naming=naming or make_naming(),
        service_yaml_config=service_yaml_config or service_pb2.Service(),
        all_protos={i.name: i for i in protos},
        **kwargs
    )


def make_naming(**kwargs) -> naming.Naming:
    kwargs.setdefault("name", "Hatstand")
    kwargs.setdefault("namespace", ("Google", "Cloud"))
    kwargs.setdefault("version", "v1")
    kwargs.setdefault("product_name", "Hatstand")
    return naming.NewNaming(**kwargs)
